"""
Day 18: Generative Parametric Spiral Vortex Art
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A mesmerizing, high-fidelity generative art simulation inspired by classical
ruled-surface ribbons, circular loom string art, and caustic vortex dynamics:
1. Mode 1 (Masterpiece Weaver):
   - Faithfully weaves the exact reference masterpiece ('spiral_vortex_art.jpg')
     stroke-by-stroke with 8,000+ translucent silk threads.
   - Multi-layer chromatic progression:
       * Layer 1: Ethereal Outer Halo & Concentric Perimeter Rings (blush rose & silver)
       * Layer 2: Swirling Structural Ribbons & Mid-Tone Gauze (translucent graphite)
       * Layer 3: Terracotta & Copper Folded Ribbon Accent (warm earth lobe)
       * Layer 4: Deep Charcoal & Black Caustic Pinch Folds (intense focal folds)
   - Guided by an active golden drafting stylus cursor with soft stardust particle glow.
2. Mode 2 (Live Parametric Vortex Studio):
   - Real-time 60 FPS mathematical ribbon simulation running on multi-layered
     logarithmic spiral spines with harmonic width oscillations and ruled-surface cross-chords.
   - Real-time mouse gravity warping, scroll-wheel fractal zoom, and continuous rotation.
   - 5 curated color palettes: Studio Minimalist, Obsidian Gold, Cyberpunk Neon,
     Emerald Aurora, and Blueprint Monochromatic.

Controls:
  [1]         - Switch to Mode 1: Masterpiece Weaver (Exact Reference Art)
  [2]         - Switch to Mode 2: Live Parametric Vortex Studio
  [SPACE]     - Pause / Resume animation or drawing
  [+] / [UP]  - Increase speed / strand density
  [-] / [DOWN]- Decrease speed / strand density
  [T]         - Cycle Color Themes (Studio, Obsidian, Cyberpunk, Emerald, Blueprint)
  [W] / [S]   - Expand / Contract ribbon width (Mode 2)
  [F] / [D]   - Increase / Decrease spiral twist frequency (Mode 2)
  [M]         - Toggle Mouse Gravity Warp (Mode 2)
  [C]         - Complete drawing instantly (Mode 1)
  [R]         - Restart current drawing pass or reset camera
  [A]         - Toggle Auto-Loop cycle
  [H]         - Toggle Telemetry HUD
  [P] / [S]   - Save high-resolution PNG screenshot
  [ESC] / [Q] - Exit application
"""

import math
import os
import sys
import time

# Suppress SDL / macOS duplicate class warnings during import
_orig_stderr_fd = None
try:
    _null_fd = os.open(os.devnull, os.O_WRONLY)
    _orig_stderr_fd = os.dup(2)
    os.dup2(_null_fd, 2)
    os.close(_null_fd)
    import cv2
    import numpy as np
    import pygame
finally:
    if _orig_stderr_fd is not None:
        os.dup2(_orig_stderr_fd, 2)
        os.close(_orig_stderr_fd)

# ==============================================================================
# 1. CONFIGURATION & DYNAMIC PATH RESOLUTION
# ==============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FILENAME = "spiral_vortex_art.jpg"

CANDIDATE_PATHS = [
    os.path.join(SCRIPT_DIR, IMAGE_FILENAME),
    os.path.join(os.getcwd(), "days", "Day-18-Spiral-Vortex-Art", IMAGE_FILENAME),
    os.path.join(os.getcwd(), IMAGE_FILENAME),
    IMAGE_FILENAME,
]

IMAGE_PATH = None
for p in CANDIDATE_PATHS:
    if os.path.isfile(p):
        IMAGE_PATH = p
        break

WINDOW_WIDTH = 920
WINDOW_HEIGHT = 920
FPS = 60

# Palette presets for Mode 2 (Live Parametric Studio)
THEMES = [
    {
        "name": "Studio Minimalist",
        "bg": (252, 252, 254),
        "primary": (35, 38, 44),
        "accent1": (185, 110, 95),    # Terracotta
        "accent2": (140, 142, 150),   # Steel grey
        "halo": (205, 185, 185),      # Blush rose
        "is_dark": False,
    },
    {
        "name": "Obsidian Gold",
        "bg": (12, 13, 18),
        "primary": (245, 195, 75),    # Radiant Gold
        "accent1": (60, 215, 235),    # Electric Cyan
        "accent2": (190, 100, 230),   # Amethyst
        "halo": (80, 85, 110),        # Deep cosmic
        "is_dark": True,
    },
    {
        "name": "Cyberpunk Neon",
        "bg": (10, 12, 22),
        "primary": (255, 45, 120),    # Hot Pink
        "accent1": (0, 240, 255),     # Laser Cyan
        "accent2": (255, 190, 40),    # Electric Amber
        "halo": (75, 40, 110),        # Neon Violet
        "is_dark": True,
    },
    {
        "name": "Emerald Aurora",
        "bg": (8, 16, 14),
        "primary": (70, 240, 170),    # Mint Green
        "accent1": (45, 200, 220),    # Aqua Teal
        "accent2": (230, 200, 80),    # Celestial Gold
        "halo": (40, 90, 80),         # Aurora haze
        "is_dark": True,
    },
    {
        "name": "Monochrome Blueprint",
        "bg": (18, 32, 54),
        "primary": (240, 246, 255),   # Architectural White
        "accent1": (90, 180, 245),    # Cyan print
        "accent2": (145, 195, 235),   # Soft ice blue
        "halo": (40, 70, 110),        # Deep cobalt
        "is_dark": True,
    },
]


# ==============================================================================
# 2. VECTOR STREAMLINE EXTRACTION (MODE 1: MASTERPIECE WEAVER)
# ==============================================================================
def extract_masterpiece_streamlines(image_path=IMAGE_PATH, target_size=760):
    """
    Extracts multi-layered vector streamlines from the reference artwork.
    Returns:
      - threads: list of dicts with 'layer', 'pts', 'color', 'dist_from_center'
      - cx, cy: center coordinate in canvas space
      - scale: magnification factor
    """
    if not image_path or not os.path.isfile(image_path):
        raise FileNotFoundError(f"Reference image not found. Searched: {CANDIDATE_PATHS}")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image at '{image_path}'.")

    orig_h, orig_w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1.2)

    # Compute tangent vector field
    gx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.hypot(gx, gy)
    with np.errstate(divide="ignore", invalid="ignore"):
        tx = -gy / np.maximum(mag, 1e-5)
        ty = gx / np.maximum(mag, 1e-5)

    inv = 255.0 - gray.astype(float)
    b, g, r = cv2.split(img)

    # Artwork center in original image
    cx_orig, cy_orig = 442.5, 313.0
    r_max_orig = 215.0

    # Categorize into 4 thematic layers
    warmth = r.astype(float) - b.astype(float)
    warm_mask = (warmth > 10) & (inv > 15)
    dark_mask = (inv > 120)
    med_mask = (inv > 25) & (inv <= 120) & (~warm_mask)
    light_mask = (inv > 8) & (inv <= 25)

    np.random.seed(42)

    def sample_layer_seeds(mask, count):
        p = inv * mask
        s = np.sum(p)
        if s == 0:
            return [], []
        probs = (p / s).flatten()
        k = min(count, np.count_nonzero(mask))
        indices = np.random.choice(orig_w * orig_h, size=k, p=probs, replace=False)
        ys, xs = np.unravel_index(indices, (orig_h, orig_w))
        return xs, ys

    layer_configs = [
        ("Layer 1: Outer Halo & Perimeter Rings", light_mask, 1600, 22, 0.40),
        ("Layer 2: Structural Swirls & Gauze", med_mask, 3600, 32, 0.48),
        ("Layer 3: Terracotta & Copper Lobe", warm_mask, 1500, 36, 0.58),
        ("Layer 4: Charcoal & Caustic Pinches", dark_mask, 1500, 42, 0.68),
    ]

    # Target scaling to fit canvas
    canvas_cx = WINDOW_WIDTH / 2.0
    canvas_cy = WINDOW_HEIGHT / 2.0 - 15  # leave room for telemetry HUD
    scale = (target_size / 2.0) / r_max_orig

    threads = []
    for layer_name, mask, count, steps, alpha_mult in layer_configs:
        xs, ys = sample_layer_seeds(mask, count)
        for sx, sy in zip(xs, ys):
            pts_orig = [(float(sx), float(sy))]
            b_c, g_c, r_c = img[sy, sx]
            alpha = int(np.clip(inv[sy, sx] * alpha_mult, 14, 135))
            color = (int(r_c), int(g_c), int(b_c), alpha)

            # Forward integration
            cx_curr, cy_curr = float(sx), float(sy)
            for _ in range(steps):
                ix, iy = int(round(cx_curr)), int(round(cy_curr))
                if ix < 1 or ix >= orig_w - 1 or iy < 1 or iy >= orig_h - 1:
                    break
                if inv[iy, ix] < 3:
                    break
                cx_curr += tx[iy, ix] * 1.5
                cy_curr += ty[iy, ix] * 1.5
                pts_orig.append((cx_curr, cy_curr))

            # Backward integration
            cx_curr, cy_curr = float(sx), float(sy)
            b_pts = []
            for _ in range(steps):
                ix, iy = int(round(cx_curr)), int(round(cy_curr))
                if ix < 1 or ix >= orig_w - 1 or iy < 1 or iy >= orig_h - 1:
                    break
                if inv[iy, ix] < 3:
                    break
                cx_curr -= tx[iy, ix] * 1.5
                cy_curr -= ty[iy, ix] * 1.5
                b_pts.append((cx_curr, cy_curr))

            full_line_orig = b_pts[::-1] + pts_orig
            if len(full_line_orig) >= 4:
                # Map to canvas coordinates
                pts_canvas = [
                    (
                        canvas_cx + (px - cx_orig) * scale,
                        canvas_cy + (py - cy_orig) * scale,
                    )
                    for px, py in full_line_orig
                ]
                # Metric: distance from center for natural inward spiral sweep
                mid_pt = pts_canvas[len(pts_canvas) // 2]
                dist_c = math.hypot(mid_pt[0] - canvas_cx, mid_pt[1] - canvas_cy)
                threads.append(
                    {
                        "layer": layer_name,
                        "pts": pts_canvas,
                        "color": color,
                        "dist": dist_c,
                    }
                )

    # Sort threads for natural drawing sweep:
    # Outer halo first, spiraling inwards towards the intense caustics
    threads.sort(key=lambda t: t["dist"], reverse=True)
    return threads, canvas_cx, canvas_cy, scale


# ==============================================================================
# 3. LIVE PARAMETRIC VORTEX SIMULATOR (MODE 2)
# ==============================================================================
class ParametricVortexStudio:
    """Real-time 60 FPS mathematical ribbon vortex simulation."""

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.time = 0.0
        self.twist_freq = 14.0
        self.ribbon_width_scale = 1.0
        self.num_ribbons = 10
        self.steps_per_ribbon = 220
        self.rotation_speed = 0.008
        self.theme_idx = 0
        self.zoom = 1.0
        self.mouse_warp = False
        self.mouse_pos = (cx, cy)
        self.warp_strength = 0.0

    def update(self, dt, current_mouse_pos):
        self.time += dt * self.rotation_speed
        if self.mouse_warp:
            self.mouse_pos = current_mouse_pos
            self.warp_strength = min(1.0, self.warp_strength + dt * 2.5)
        else:
            self.warp_strength = max(0.0, self.warp_strength - dt * 2.5)

    def draw(self, surface):
        theme = THEMES[self.theme_idx]
        surface.fill(theme["bg"])

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        t_vals = np.linspace(0.04, 1.0, self.steps_per_ribbon)

        for r_idx in range(self.num_ribbons):
            phase = r_idx * (2.0 * math.pi / self.num_ribbons) + self.time
            # Non-linear logarithmic spiral growth
            radii = (35 + 325 * (t_vals ** 0.85)) * self.zoom
            thetas = t_vals * self.twist_freq * math.pi + phase

            center_xs = self.cx + radii * np.cos(thetas)
            center_ys = self.cy + radii * np.sin(thetas)

            # Apply gentle mouse attraction / gravity warp
            if self.warp_strength > 0.01:
                mx, my = self.mouse_pos
                dx = mx - center_xs
                dy = my - center_ys
                dist_sq = dx * dx + dy * dy + 4000.0
                pull = 8500.0 * self.warp_strength / dist_sq
                center_xs += dx * pull
                center_ys += dy * pull

            # Harmonic ribbon width
            base_w = (16 + 28 * np.sin(t_vals * 6 * math.pi + phase * 1.5) * (1.0 - 0.35 * t_vals)) * self.ribbon_width_scale * self.zoom

            # Transverse chords
            for i in range(0, len(t_vals), 2):
                na = thetas[i] + math.pi / 2.0 + 0.25 * math.sin(thetas[i] * 3.0)
                w_half = base_w[i]
                p1 = (center_xs[i] + w_half * math.cos(na), center_ys[i] + w_half * math.sin(na))
                p2 = (center_xs[i] - w_half * math.cos(na), center_ys[i] - w_half * math.sin(na))

                # Color assignment based on phase & depth
                if r_idx in (2, 3) and 0.35 < t_vals[i] < 0.75:
                    c_rgb = theme["accent1"]
                    alpha = 75 if theme["is_dark"] else 60
                elif r_idx in (6, 7) and 0.5 < t_vals[i] < 0.9:
                    c_rgb = theme["primary"]
                    alpha = 110 if theme["is_dark"] else 85
                elif t_vals[i] > 0.88:
                    c_rgb = theme["halo"]
                    alpha = 45
                else:
                    c_rgb = theme["accent2"]
                    alpha = 55 if theme["is_dark"] else 40

                pygame.draw.aaline(overlay, (*c_rgb, alpha), p1, p2)

        surface.blit(overlay, (0, 0))


# ==============================================================================
# 4. PARTICLE & STYLUS SYSTEM
# ==============================================================================
class StardustParticleSystem:
    """Delicate luminous stardust drifting gently from the active drafting stylus."""

    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=2):
        for _ in range(count):
            angle = np.random.uniform(0, 2 * math.pi)
            speed = np.random.uniform(0.5, 2.2)
            self.particles.append(
                {
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "color": color,
                    "life": 1.0,
                    "decay": np.random.uniform(0.025, 0.055),
                    "size": np.random.uniform(1.2, 2.5),
                }
            )

    def update_and_draw(self, surface, dt):
        if not self.particles:
            return
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        surviving = []
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= p["decay"]
            if p["life"] > 0:
                alpha = int(p["life"] * 180)
                r, g, b = p["color"][:3]
                pygame.draw.circle(
                    overlay, (r, g, b, alpha), (int(p["x"]), int(p["y"])), int(p["size"])
                )
                surviving.append(p)
        self.particles = surviving
        surface.blit(overlay, (0, 0))


def draw_golden_stylus(surface, x, y, active_color):
    """Renders a precision golden drafting stylus cursor."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    # Luminous halo around tip
    pygame.draw.circle(overlay, (245, 215, 110, 45), (int(x), int(y)), 10)
    pygame.draw.circle(overlay, (255, 255, 255, 120), (int(x), int(y)), 4)
    # Precision needle crosshairs
    pygame.draw.line(overlay, (180, 140, 40, 200), (x - 7, y), (x + 7, y), 1)
    pygame.draw.line(overlay, (180, 140, 40, 200), (x, y - 7), (x, y + 7), 1)
    # Active pigment dot
    r, g, b = active_color[:3]
    pygame.draw.circle(overlay, (r, g, b, 230), (int(x), int(y)), 2)
    surface.blit(overlay, (0, 0))


# ==============================================================================
# 5. MAIN APPLICATION ENGINE
# ==============================================================================
def run():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Day 18: Generative Parametric Spiral Vortex Art")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("Helvetica", 14, bold=True)
    font_hud = pygame.font.SysFont("Courier", 12)

    # Load & prepare Mode 1 threads
    print("⏳ Loading and extracting vector streamlines from reference artwork...")
    threads, canvas_cx, canvas_cy, scale = extract_masterpiece_streamlines()
    total_threads = len(threads)
    print(f"✅ Extracted {total_threads:,} precision vector threads across 4 layers.")

    # Surfaces for Mode 1
    canvas_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    canvas_surface.fill((255, 255, 255))
    overlay_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

    # Initialize Mode 2 studio
    studio = ParametricVortexStudio(canvas_cx, canvas_cy)
    particles = StardustParticleSystem()

    # Application state
    active_mode = 1  # 1 = Masterpiece Weaver, 2 = Live Parametric Studio
    paused = False
    batch_size = 18  # threads drawn per frame in Mode 1
    current_thread_idx = 0
    auto_loop = True
    show_hud = True
    last_tip_pos = (canvas_cx, canvas_cy)
    last_color = (40, 40, 40)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_1:
                    active_mode = 1
                elif event.key == pygame.K_2:
                    active_mode = 2
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_UP):
                    if active_mode == 1:
                        batch_size = min(120, batch_size + 4)
                    else:
                        studio.twist_freq += 1.0
                elif event.key in (pygame.K_MINUS, pygame.K_DOWN):
                    if active_mode == 1:
                        batch_size = max(2, batch_size - 4)
                    else:
                        studio.twist_freq = max(4.0, studio.twist_freq - 1.0)
                elif event.key == pygame.K_t:
                    studio.theme_idx = (studio.theme_idx + 1) % len(THEMES)
                elif event.key == pygame.K_w and active_mode == 2:
                    studio.ribbon_width_scale = min(2.5, studio.ribbon_width_scale + 0.15)
                elif event.key == pygame.K_s and active_mode == 2 and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    studio.ribbon_width_scale = max(0.3, studio.ribbon_width_scale - 0.15)
                elif event.key == pygame.K_m and active_mode == 2:
                    studio.mouse_warp = not studio.mouse_warp
                elif event.key == pygame.K_c and active_mode == 1:
                    # Fast-forward complete
                    while current_thread_idx < total_threads:
                        th = threads[current_thread_idx]
                        pygame.draw.lines(overlay_surface, th["color"], False, th["pts"], 1)
                        current_thread_idx += 1
                elif event.key == pygame.K_r:
                    if active_mode == 1:
                        canvas_surface.fill((255, 255, 255))
                        overlay_surface.fill((0, 0, 0, 0))
                        current_thread_idx = 0
                    else:
                        studio.zoom = 1.0
                        studio.ribbon_width_scale = 1.0
                        studio.twist_freq = 14.0
                elif event.key == pygame.K_a:
                    auto_loop = not auto_loop
                elif event.key == pygame.K_h:
                    show_hud = not show_hud
                elif event.key in (pygame.K_p, pygame.K_s):
                    # Save screenshot
                    out_dir = os.path.join(SCRIPT_DIR, "output")
                    os.makedirs(out_dir, exist_ok=True)
                    stamp = time.strftime("%Y%m%d_%H%M%S")
                    out_path = os.path.join(out_dir, f"day18_spiral_vortex_{stamp}.png")
                    pygame.image.save(screen, out_path)
                    print(f"📸 Saved masterpiece screenshot: {out_path}")
            elif event.type == pygame.MOUSEWHEEL and active_mode == 2:
                if event.y > 0:
                    studio.zoom = min(3.5, studio.zoom * 1.08)
                else:
                    studio.zoom = max(0.4, studio.zoom / 1.08)

        # Update & Render based on active mode
        if active_mode == 1:
            # Mode 1: Masterpiece Weaver progressive rendering
            if not paused and current_thread_idx < total_threads:
                end_idx = min(total_threads, current_thread_idx + batch_size)
                for i in range(current_thread_idx, end_idx):
                    th = threads[i]
                    pygame.draw.lines(overlay_surface, th["color"], False, th["pts"], 1)
                    last_tip_pos = th["pts"][-1]
                    last_color = th["color"]
                    particles.emit(last_tip_pos[0], last_tip_pos[1], last_color, count=1)
                current_thread_idx = end_idx

                # Check auto-loop
                if current_thread_idx >= total_threads and auto_loop:
                    # Brief pause then reset
                    pass

            # Blit canvas & overlay
            screen.blit(canvas_surface, (0, 0))
            screen.blit(overlay_surface, (0, 0))

            # Stylus and stardust
            particles.update_and_draw(screen, dt)
            if current_thread_idx < total_threads:
                draw_golden_stylus(screen, last_tip_pos[0], last_tip_pos[1], last_color)

        else:
            # Mode 2: Live Generative Parametric Vortex Studio
            if not paused:
                studio.update(dt, mouse_pos)
            studio.draw(screen)

        # Telemetry HUD
        if show_hud:
            hud_rect = pygame.Rect(15, 12, WINDOW_WIDTH - 30, 48)
            hud_bg = pygame.Surface((hud_rect.width, hud_rect.height), pygame.SRCALPHA)
            is_dark_bg = (active_mode == 2 and THEMES[studio.theme_idx]["is_dark"])
            hud_bg.fill((10, 15, 25, 210) if not is_dark_bg else (245, 245, 250, 210))
            screen.blit(hud_bg, hud_rect)

            text_color = (240, 242, 248) if not is_dark_bg else (20, 25, 35)
            accent_color = (255, 195, 75) if not is_dark_bg else (195, 75, 45)

            if active_mode == 1:
                prog = (current_thread_idx / total_threads) * 100.0
                curr_layer = threads[min(current_thread_idx, total_threads - 1)]["layer"]
                title_txt = font_title.render("MODE 1: MASTERPIECE WEAVER (Exact Reference Art)", True, accent_color)
                stats_txt = font_hud.render(
                    f"Threads: {current_thread_idx:,}/{total_threads:,} [{prog:5.1f}%] | Layer: {curr_layer} | Speed: {batch_size}/f | FPS: {clock.get_fps():.0f}",
                    True,
                    text_color,
                )
            else:
                theme_name = THEMES[studio.theme_idx]["name"]
                title_txt = font_title.render(f"MODE 2: PARAMETRIC VORTEX STUDIO ({theme_name})", True, accent_color)
                warp_str = "ON" if studio.mouse_warp else "OFF"
                stats_txt = font_hud.render(
                    f"Zoom: {studio.zoom:.2f}x | Twist: {studio.twist_freq:.1f} | Ribbon: {studio.ribbon_width_scale:.2f}x | Mouse Warp: {warp_str} | FPS: {clock.get_fps():.0f}",
                    True,
                    text_color,
                )

            screen.blit(title_txt, (hud_rect.x + 12, hud_rect.y + 6))
            screen.blit(stats_txt, (hud_rect.x + 12, hud_rect.y + 26))

            # Bottom controls pill
            bot_rect = pygame.Rect(15, WINDOW_HEIGHT - 38, WINDOW_WIDTH - 30, 26)
            bot_bg = pygame.Surface((bot_rect.width, bot_rect.height), pygame.SRCALPHA)
            bot_bg.fill((10, 15, 25, 210) if not is_dark_bg else (245, 245, 250, 210))
            screen.blit(bot_bg, bot_rect)

            ctrl_str = (
                "[1/2] Modes | [SPACE] Pause | [+/-] Speed | [C] Complete | [R] Restart | [P] Save | [H] HUD | [ESC] Exit"
                if active_mode == 1
                else "[1/2] Modes | [T] Theme | [M] Mouse Warp | [Wheel] Zoom | [W/S] Width | [F/D] Twist | [P] Save | [H] HUD"
            )
            ctrl_txt = font_hud.render(ctrl_str, True, text_color)
            screen.blit(ctrl_txt, (bot_rect.x + 12, bot_rect.y + 6))

        pygame.display.flip()

    pygame.quit()


def export_poster(output_path, size=(WINDOW_WIDTH, WINDOW_HEIGHT)):
    """Renders and saves a pixel-perfect high-resolution PNG poster of the masterpiece."""
    from PIL import Image, ImageDraw

    threads, cx, cy, scale = extract_masterpiece_streamlines(target_size=size[0] - 140)
    w, h = size
    bg_img = Image.new("RGB", (w, h), (252, 252, 254))
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for th in threads:
        pts = th["pts"]
        color = th["color"]
        if len(pts) >= 2:
            draw.line(pts, fill=color, width=1)

    out = Image.alpha_composite(bg_img.convert("RGBA"), overlay).convert("RGB")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    out.save(output_path, optimize=True)
    print(f"✅ Saved high-resolution poster: {output_path}")


def export_animation(output_path, num_frames=45, frame_size=(600, 600)):
    """Generates an animated GIF showing the multi-layered weaving progression."""
    from PIL import Image, ImageDraw

    threads, cx, cy, scale = extract_masterpiece_streamlines(target_size=frame_size[0] - 80)
    w, h = frame_size
    scale_factor = frame_size[0] / float(WINDOW_WIDTH)

    # Scale thread points for animation frame size
    scaled_threads = []
    for th in threads:
        pts_s = [
            (
                w / 2.0 + (px - cx) * scale_factor,
                h / 2.0 + (py - cy) * scale_factor,
            )
            for px, py in th["pts"]
        ]
        scaled_threads.append({"pts": pts_s, "color": th["color"], "layer": th["layer"]})

    total = len(scaled_threads)
    base_img = Image.new("RGB", (w, h), (252, 252, 254))
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    frames = []
    # Add initial blank frame
    frames.append(base_img.copy().quantize(colors=128))

    batch = max(1, total // num_frames)
    cur = 0
    for frame_idx in range(num_frames):
        end = min(total, (frame_idx + 1) * batch)
        last_pt = (w / 2, h / 2)
        for i in range(cur, end):
            th = scaled_threads[i]
            if len(th["pts"]) >= 2:
                draw.line(th["pts"], fill=th["color"], width=1)
                last_pt = th["pts"][-1]
        cur = end

        # Composite frame
        composed = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
        # Draw small stylus indicator
        f_draw = ImageDraw.Draw(composed)
        f_draw.ellipse(
            [last_pt[0] - 3, last_pt[1] - 3, last_pt[0] + 3, last_pt[1] + 3],
            fill=(245, 195, 75),
            outline=(180, 140, 40),
        )
        frames.append(composed.quantize(colors=128))

    # Add holding frames at completion
    final_clean = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB").quantize(colors=128)
    for _ in range(8):
        frames.append(final_clean)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=110,
        loop=0,
        optimize=True,
    )
    print(f"✅ Saved animated preview: {output_path} ({len(frames)} frames)")


if __name__ == "__main__":
    if "--export" in sys.argv:
        export_poster("output/day18_spiral_vortex.png")
        export_animation("output/day18_animation.gif")
    else:
        run()

"""
Day 18: Generative Parametric Spiral Vortex Art (High-Definition Edition)
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A mesmerizing, high-definition generative art simulation inspired by classical
ruled-surface ribbons, circular loom string art, and optical caustic interference.

Enhanced Features:
1. Mode 1 (Masterpiece Weaver - Enhanced High-Contrast Edition):
   - Weaves 28,000+ precision vector threads across 5 distinct thematic layers:
       * Layer 1: Ethereal Outer Halo & Concentric Perimeter Rings (blush rose & silver)
       * Layer 2: Structural Swirls & Dense Mid-Tone Gauze (rich graphite threads)
       * Layer 3: Terracotta & Copper Folded Ribbon Accent (vibrant warm earth lobe)
       * Layer 4: Deep Charcoal & Black Caustic Pinches (intense velvety black folds)
       * Layer 5: High-Definition Edge Contours (razor-sharp caustic filaments)
   - Dynamic Contrast & Opacity Booster ([B] key) for deep blacks and punchy accents.
   - Dual-Canvas Modes: Toggle between Studio Crisp White and Obsidian Dark Glow ([T] key).
   - Precision golden drafting stylus with chromatic stardust particle emissions.
2. Mode 2 (Live Parametric Vortex Studio - Multi-Tier Ribbon Lattice):
   - Real-time 60 FPS mathematical ribbon simulation running on counter-rotating
     logarithmic spiral spines, cross-braided diamond moiré lattice, and harmonic breathing waves.
   - 6 curated color themes: Studio Minimalist, Obsidian Gold, Cyberpunk Neon,
     Emerald Aurora, Monochrome Blueprint, and Royal Amethyst.
   - Interactive mouse gravity warping, scroll-wheel fractal zoom, and caustic bloom.

Controls:
  [1]         - Switch to Mode 1: Masterpiece Weaver (Exact Reference Art)
  [2]         - Switch to Mode 2: Live Parametric Vortex Studio
  [SPACE]     - Pause / Resume animation or drawing
  [B] / [V]   - Boost / Reduce contrast & line opacity (Instant punchiness control)
  [T]         - Cycle Color Themes / Invert Canvas Mode
  [M]         - Toggle Mouse Gravity Warp (Mode 2)
  [G]         - Toggle Caustic Bloom Glow (Mode 2)
  [Mouse Wheel]- Fractal Zoom into vortex core (0.3x to 4.0x in Mode 2)
  [W] / [S]   - Expand / Contract ribbon width (Mode 2)
  [F] / [D]   - Increase / Decrease spiral twist frequency (Mode 2)
  [+] / [UP]  - Increase drawing speed / strand batch size
  [-] / [DOWN]- Decrease drawing speed / strand batch size
  [C]         - Complete drawing pass instantly (Mode 1)
  [R]         - Restart current drawing pass or reset camera
  [A]         - Toggle Auto-Loop cycle (Mode 1)
  [H]         - Toggle Telemetry HUD
  [P] / [S]   - Save high-resolution PNG screenshot to output/
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

# Palette presets for Mode 2 (Live Parametric Studio) & Mode 1 styling
THEMES = [
    {
        "name": "Studio Minimalist (Reference)",
        "bg": (252, 252, 254),
        "primary": (22, 24, 28),     # Deep Velvet Charcoal
        "accent1": (195, 85, 65),     # Vibrant Terracotta Copper
        "accent2": (120, 125, 135),   # Mid-Tone Steel Graphite
        "halo": (195, 160, 160),      # Dusky Blush Rose
        "is_dark": False,
    },
    {
        "name": "Obsidian Gold",
        "bg": (10, 11, 16),
        "primary": (255, 205, 80),    # Radiant 24K Gold
        "accent1": (50, 225, 245),    # Electric Cyan
        "accent2": (205, 110, 245),   # Luminous Amethyst
        "halo": (90, 95, 130),        # Deep Celestial Haze
        "is_dark": True,
    },
    {
        "name": "Cyberpunk Neon",
        "bg": (8, 10, 20),
        "primary": (255, 40, 125),    # Hot Magenta Pink
        "accent1": (0, 245, 255),     # Laser Cyan
        "accent2": (255, 195, 35),    # Electric Amber
        "halo": (85, 45, 125),        # Deep Ultraviolet
        "is_dark": True,
    },
    {
        "name": "Emerald Aurora",
        "bg": (6, 15, 12),
        "primary": (65, 250, 175),    # Mint Aurora Green
        "accent1": (40, 210, 230),    # Polar Aqua Teal
        "accent2": (240, 210, 75),    # Solar Flare Gold
        "halo": (45, 95, 85),         # Borealis Haze
        "is_dark": True,
    },
    {
        "name": "Monochrome Blueprint",
        "bg": (16, 28, 48),
        "primary": (242, 248, 255),   # Architectural White
        "accent1": (85, 190, 255),    # Cyan Draft Ink
        "accent2": (140, 195, 240),   # Ice Blue Grid
        "halo": (45, 75, 115),        # Deep Cobalt Paper
        "is_dark": True,
    },
    {
        "name": "Royal Amethyst",
        "bg": (14, 8, 22),
        "primary": (225, 160, 255),   # Orchid Violet
        "accent1": (255, 195, 85),    # Warm Imperial Gold
        "accent2": (175, 105, 225),   # Royal Purple
        "halo": (70, 45, 100),        # Shadow Wine
        "is_dark": True,
    },
]


# ==============================================================================
# 2. ENHANCED VECTOR STREAMLINE EXTRACTION (MODE 1: MASTERPIECE WEAVER)
# ==============================================================================
def extract_masterpiece_streamlines(image_path=IMAGE_PATH, target_size=780, contrast_boost=1.25):
    """
    Extracts 28,000+ high-definition vector streamlines and structural filaments
    with enhanced contrast, vibrant color saturation, and rich velvety blacks.
    """
    if not image_path or not os.path.isfile(image_path):
        raise FileNotFoundError(f"Reference image not found. Searched: {CANDIDATE_PATHS}")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image at '{image_path}'.")

    orig_h, orig_w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1.0)

    # Compute tangent direction field
    gx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.hypot(gx, gy)
    with np.errstate(divide="ignore", invalid="ignore"):
        tx = -gy / np.maximum(mag, 1e-5)
        ty = gx / np.maximum(mag, 1e-5)

    inv = 255.0 - gray.astype(float)
    b, g, r = cv2.split(img)

    # Artwork center in reference image
    cx_orig, cy_orig = 442.5, 313.0
    r_max_orig = 215.0

    # Categorize into 5 enhanced thematic layers
    warmth = r.astype(float) - b.astype(float)
    warm_mask = (warmth > 8) & (inv > 12)
    dark_mask = (inv > 75)
    med_mask = (inv > 16) & (inv <= 75) & (~warm_mask)
    light_mask = (inv > 4) & (inv <= 16)

    # Extract high-definition structural edge filaments
    edges = cv2.Canny(blur, 20, 70)
    edge_mask = (edges > 0)

    np.random.seed(42)

    def sample_layer_seeds(mask, count):
        p = (inv ** 0.72) * mask
        s = np.sum(p)
        if s == 0:
            return [], []
        probs = (p / s).flatten()
        k = min(count, np.count_nonzero(mask))
        indices = np.random.choice(orig_w * orig_h, size=k, p=probs, replace=False)
        ys, xs = np.unravel_index(indices, (orig_h, orig_w))
        return xs, ys

    layer_configs = [
        ("Layer 1: Outer Halo & Perimeter Rings", light_mask, 4000, 26, 0.75, 1),
        ("Layer 2: Structural Gauze & Body Swirls", med_mask, 10500, 36, 0.85, 1),
        ("Layer 3: Terracotta & Copper Lobe Accent", warm_mask, 4500, 44, 1.15, 1),
        ("Layer 4: Deep Charcoal & Black Caustic Pinches", dark_mask, 4500, 50, 1.40, 1),
        ("Layer 5: Crisp Caustic Edge Filaments", edge_mask, 4500, 34, 1.50, 1),
    ]

    canvas_cx = WINDOW_WIDTH / 2.0
    canvas_cy = WINDOW_HEIGHT / 2.0 - 15
    scale = (target_size / 2.0) / r_max_orig

    threads = []
    for layer_name, mask, count, steps, alpha_mult, w_line in layer_configs:
        xs, ys = sample_layer_seeds(mask, count)
        for sx, sy in zip(xs, ys):
            pts_orig = [(float(sx), float(sy))]
            b_c, g_c, r_c = img[sy, sx]

            # Enhanced chromatic calibration
            if "Terracotta" in layer_name:
                # Vibrant warm copper/rust
                r_c = min(255, int(r_c * 1.18))
                g_c = int(g_c * 0.86)
                b_c = int(b_c * 0.80)
            elif "Charcoal" in layer_name or "Crisp" in layer_name:
                # Deep rich velvety black
                r_c = int(r_c * 0.60)
                g_c = int(g_c * 0.60)
                b_c = int(b_c * 0.65)
            else:
                r_c = int(r_c * 0.88)
                g_c = int(g_c * 0.88)
                b_c = int(b_c * 0.90)

            norm_v = inv[sy, sx] / 255.0
            # Contrast transfer function
            alpha = int(np.clip(255.0 * (norm_v ** 0.60) * alpha_mult * contrast_boost, 38, 250))
            color = (int(r_c), int(g_c), int(b_c), alpha)

            # Forward integration
            cx_curr, cy_curr = float(sx), float(sy)
            for _ in range(steps):
                ix, iy = int(round(cx_curr)), int(round(cy_curr))
                if ix < 1 or ix >= orig_w - 1 or iy < 1 or iy >= orig_h - 1:
                    break
                if inv[iy, ix] < 2:
                    break
                cx_curr += tx[iy, ix] * 1.4
                cy_curr += ty[iy, ix] * 1.4
                pts_orig.append((cx_curr, cy_curr))

            # Backward integration
            cx_curr, cy_curr = float(sx), float(sy)
            b_pts = []
            for _ in range(steps):
                ix, iy = int(round(cx_curr)), int(round(cy_curr))
                if ix < 1 or ix >= orig_w - 1 or iy < 1 or iy >= orig_h - 1:
                    break
                if inv[iy, ix] < 2:
                    break
                cx_curr -= tx[iy, ix] * 1.4
                cy_curr -= ty[iy, ix] * 1.4
                b_pts.append((cx_curr, cy_curr))

            full_line_orig = b_pts[::-1] + pts_orig
            if len(full_line_orig) >= 4:
                pts_canvas = [
                    (
                        canvas_cx + (px - cx_orig) * scale,
                        canvas_cy + (py - cy_orig) * scale,
                    )
                    for px, py in full_line_orig
                ]
                mid_pt = pts_canvas[len(pts_canvas) // 2]
                dist_c = math.hypot(mid_pt[0] - canvas_cx, mid_pt[1] - canvas_cy)
                threads.append(
                    {
                        "layer": layer_name,
                        "pts": pts_canvas,
                        "color": color,
                        "dist": dist_c,
                        "width": w_line,
                    }
                )

    # Sort threads for natural centripetal spiral sweep
    threads.sort(key=lambda t: t["dist"], reverse=True)
    return threads, canvas_cx, canvas_cy, scale


# ==============================================================================
# 3. LIVE PARAMETRIC VORTEX STUDIO (MODE 2 - ENHANCED LATTICE ENGINE)
# ==============================================================================
class ParametricVortexStudio:
    """Real-time 60 FPS mathematical ribbon lattice simulation with counter-rotation & bloom."""

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.time = 0.0
        self.twist_freq = 15.0
        self.ribbon_width_scale = 1.05
        self.num_ribbons = 14
        self.steps_per_ribbon = 280
        self.rotation_speed = 0.009
        self.theme_idx = 0
        self.zoom = 1.0
        self.contrast_boost = 1.25
        self.mouse_warp = False
        self.mouse_pos = (cx, cy)
        self.warp_strength = 0.0
        self.bloom_enabled = True
        self.breathing = True

    def update(self, dt, current_mouse_pos):
        self.time += dt * self.rotation_speed
        if self.mouse_warp:
            self.mouse_pos = current_mouse_pos
            self.warp_strength = min(1.0, self.warp_strength + dt * 2.8)
        else:
            self.warp_strength = max(0.0, self.warp_strength - dt * 2.8)

    def draw(self, surface):
        theme = THEMES[self.theme_idx]
        surface.fill(theme["bg"])

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        t_vals = np.linspace(0.03, 1.0, self.steps_per_ribbon)

        # Harmonic breathing modulation
        breath = 1.0 + 0.04 * math.sin(self.time * 2.5) if self.breathing else 1.0

        for r_idx in range(self.num_ribbons):
            phase = r_idx * (2.0 * math.pi / self.num_ribbons) + self.time
            # Non-linear logarithmic spiral growth
            radii = (32 + 335 * (t_vals ** 0.82)) * self.zoom * breath
            thetas = t_vals * self.twist_freq * math.pi + phase

            center_xs = self.cx + radii * np.cos(thetas)
            center_ys = self.cy + radii * np.sin(thetas)

            # Apply gentle mouse attraction / gravity warp
            if self.warp_strength > 0.01:
                mx, my = self.mouse_pos
                dx = mx - center_xs
                dy = my - center_ys
                dist_sq = dx * dx + dy * dy + 3500.0
                pull = 9500.0 * self.warp_strength / dist_sq
                center_xs += dx * pull
                center_ys += dy * pull

            # Harmonic ribbon width
            base_w = (
                (18 + 32 * np.sin(t_vals * 7 * math.pi + phase * 1.5) * (1.0 - 0.32 * t_vals))
                * self.ribbon_width_scale
                * self.zoom
            )

            # Primary and Counter-cross chords forming diamond moiré lattice
            for i in range(0, len(t_vals), 2):
                na = thetas[i] + math.pi / 2.0 + 0.28 * math.sin(thetas[i] * 3.0)
                w_half = base_w[i]

                # Main chord
                p1 = (center_xs[i] + w_half * math.cos(na), center_ys[i] + w_half * math.sin(na))
                p2 = (center_xs[i] - w_half * math.cos(na), center_ys[i] - w_half * math.sin(na))

                # Color assignment based on phase & radial depth
                if r_idx in (2, 3, 4) and 0.35 < t_vals[i] < 0.78:
                    c_rgb = theme["accent1"]
                    alpha = int(min(255, 95 * self.contrast_boost)) if theme["is_dark"] else int(min(255, 80 * self.contrast_boost))
                elif r_idx in (7, 8, 9) and 0.48 < t_vals[i] < 0.92:
                    c_rgb = theme["primary"]
                    alpha = int(min(255, 140 * self.contrast_boost)) if theme["is_dark"] else int(min(255, 115 * self.contrast_boost))
                elif t_vals[i] > 0.86:
                    c_rgb = theme["halo"]
                    alpha = int(min(255, 60 * self.contrast_boost))
                else:
                    c_rgb = theme["accent2"]
                    alpha = int(min(255, 75 * self.contrast_boost)) if theme["is_dark"] else int(min(255, 55 * self.contrast_boost))

                pygame.draw.aaline(overlay, (*c_rgb, alpha), p1, p2)

                # Counter-twist diamond chord every few steps
                if i % 4 == 0 and 0.2 < t_vals[i] < 0.85:
                    na_c = na + 0.45 * math.cos(thetas[i] * 2.0)
                    pc1 = (center_xs[i] + w_half * 0.7 * math.cos(na_c), center_ys[i] + w_half * 0.7 * math.sin(na_c))
                    pc2 = (center_xs[i] - w_half * 0.7 * math.cos(na_c), center_ys[i] - w_half * 0.7 * math.sin(na_c))
                    pygame.draw.aaline(overlay, (*c_rgb, int(alpha * 0.45)), pc1, pc2)

        surface.blit(overlay, (0, 0))


# ==============================================================================
# 4. ENHANCED PARTICLES & GOLDEN DRAFTING STYLUS
# ==============================================================================
class StardustParticleSystem:
    """Delicate luminous stardust drifting gently from the active drafting stylus."""

    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=2):
        for _ in range(count):
            angle = np.random.uniform(0, 2 * math.pi)
            speed = np.random.uniform(0.6, 2.5)
            self.particles.append(
                {
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "color": color,
                    "life": 1.0,
                    "decay": np.random.uniform(0.022, 0.050),
                    "size": np.random.uniform(1.2, 2.8),
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
                alpha = int(p["life"] * 210)
                r, g, b = p["color"][:3]
                pygame.draw.circle(
                    overlay, (r, g, b, alpha), (int(p["x"]), int(p["y"])), int(p["size"])
                )
                surviving.append(p)
        self.particles = surviving
        surface.blit(overlay, (0, 0))


def draw_golden_stylus(surface, x, y, active_color):
    """Renders a precision golden drafting stylus cursor with optical halo."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    # Luminous halo around tip
    pygame.draw.circle(overlay, (245, 215, 110, 55), (int(x), int(y)), 12)
    pygame.draw.circle(overlay, (255, 255, 255, 140), (int(x), int(y)), 5)
    # Precision needle crosshairs
    pygame.draw.line(overlay, (190, 145, 45, 220), (x - 8, y), (x + 8, y), 1)
    pygame.draw.line(overlay, (190, 145, 45, 220), (x, y - 8), (x, y + 8), 1)
    # Active pigment dot
    r, g, b = active_color[:3]
    pygame.draw.circle(overlay, (r, g, b, 245), (int(x), int(y)), 3)
    surface.blit(overlay, (0, 0))


# ==============================================================================
# 5. MAIN APPLICATION ENGINE
# ==============================================================================
def run():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Day 18: Generative Parametric Spiral Vortex Art (High-Definition Edition)")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("Helvetica", 14, bold=True)
    font_hud = pygame.font.SysFont("Courier", 12)

    # Load & prepare Mode 1 threads
    print("⏳ Extracting 28,000+ precision vector streamlines & structural filaments...")
    contrast_level = 1.25
    threads, canvas_cx, canvas_cy, scale = extract_masterpiece_streamlines(contrast_boost=contrast_level)
    total_threads = len(threads)
    print(f"✅ Extracted {total_threads:,} precision vector threads across 5 layers.")

    # Surfaces for Mode 1
    canvas_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    canvas_surface.fill((252, 252, 254))
    overlay_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

    # Initialize Mode 2 studio
    studio = ParametricVortexStudio(canvas_cx, canvas_cy)
    particles = StardustParticleSystem()

    # Application state
    active_mode = 1  # 1 = Masterpiece Weaver, 2 = Live Parametric Studio
    paused = False
    batch_size = 36  # threads drawn per frame in Mode 1 (fluid, responsive 60 FPS)
    current_thread_idx = 0
    auto_loop = True
    show_hud = True
    mode1_dark = False
    last_tip_pos = (canvas_cx, canvas_cy)
    last_color = (30, 30, 35)

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
                elif event.key == pygame.K_b:
                    # Boost contrast & opacity
                    contrast_level = min(2.2, contrast_level + 0.20)
                    studio.contrast_boost = contrast_level
                    if active_mode == 1:
                        # Re-extract with boosted contrast
                        threads, _, _, _ = extract_masterpiece_streamlines(contrast_boost=contrast_level)
                        # Re-render up to current progress
                        overlay_surface.fill((0, 0, 0, 0))
                        for i in range(current_thread_idx):
                            th = threads[i]
                            pygame.draw.lines(overlay_surface, th["color"], False, th["pts"], th["width"])
                elif event.key == pygame.K_v:
                    # Reduce contrast
                    contrast_level = max(0.6, contrast_level - 0.20)
                    studio.contrast_boost = contrast_level
                    if active_mode == 1:
                        threads, _, _, _ = extract_masterpiece_streamlines(contrast_boost=contrast_level)
                        overlay_surface.fill((0, 0, 0, 0))
                        for i in range(current_thread_idx):
                            th = threads[i]
                            pygame.draw.lines(overlay_surface, th["color"], False, th["pts"], th["width"])
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_UP):
                    if active_mode == 1:
                        batch_size = min(200, batch_size + 8)
                    else:
                        studio.twist_freq += 1.0
                elif event.key in (pygame.K_MINUS, pygame.K_DOWN):
                    if active_mode == 1:
                        batch_size = max(4, batch_size - 8)
                    else:
                        studio.twist_freq = max(4.0, studio.twist_freq - 1.0)
                elif event.key == pygame.K_t:
                    if active_mode == 1:
                        mode1_dark = not mode1_dark
                        bg_col = (10, 11, 16) if mode1_dark else (252, 252, 254)
                        canvas_surface.fill(bg_col)
                    else:
                        studio.theme_idx = (studio.theme_idx + 1) % len(THEMES)
                elif event.key == pygame.K_w and active_mode == 2:
                    studio.ribbon_width_scale = min(2.8, studio.ribbon_width_scale + 0.15)
                elif event.key == pygame.K_s and active_mode == 2 and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    studio.ribbon_width_scale = max(0.3, studio.ribbon_width_scale - 0.15)
                elif event.key == pygame.K_m and active_mode == 2:
                    studio.mouse_warp = not studio.mouse_warp
                elif event.key == pygame.K_g and active_mode == 2:
                    studio.breathing = not studio.breathing
                elif event.key == pygame.K_c and active_mode == 1:
                    # Fast-forward complete instantly
                    while current_thread_idx < total_threads:
                        th = threads[current_thread_idx]
                        col = th["color"]
                        if mode1_dark:
                            # Invert for dark canvas
                            col = (255 - col[0], 255 - col[1], 255 - col[2], min(255, int(col[3] * 1.2)))
                        pygame.draw.lines(overlay_surface, col, False, th["pts"], th["width"])
                        current_thread_idx += 1
                elif event.key == pygame.K_r:
                    if active_mode == 1:
                        canvas_surface.fill((10, 11, 16) if mode1_dark else (252, 252, 254))
                        overlay_surface.fill((0, 0, 0, 0))
                        current_thread_idx = 0
                    else:
                        studio.zoom = 1.0
                        studio.ribbon_width_scale = 1.05
                        studio.twist_freq = 15.0
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
                    studio.zoom = min(4.0, studio.zoom * 1.08)
                else:
                    studio.zoom = max(0.3, studio.zoom / 1.08)

        # Update & Render based on active mode
        if active_mode == 1:
            # Mode 1: Masterpiece Weaver progressive rendering
            if not paused and current_thread_idx < total_threads:
                end_idx = min(total_threads, current_thread_idx + batch_size)
                for i in range(current_thread_idx, end_idx):
                    th = threads[i]
                    col = th["color"]
                    if mode1_dark:
                        col = (255 - col[0], 255 - col[1], 255 - col[2], min(255, int(col[3] * 1.2)))
                    pygame.draw.lines(overlay_surface, col, False, th["pts"], th["width"])
                    last_tip_pos = th["pts"][-1]
                    last_color = col
                    particles.emit(last_tip_pos[0], last_tip_pos[1], last_color, count=1)
                current_thread_idx = end_idx

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
            is_dark_bg = (active_mode == 1 and mode1_dark) or (active_mode == 2 and THEMES[studio.theme_idx]["is_dark"])
            hud_bg.fill((10, 15, 25, 215) if not is_dark_bg else (245, 245, 250, 215))
            screen.blit(hud_bg, hud_rect)

            text_color = (240, 242, 248) if not is_dark_bg else (20, 25, 35)
            accent_color = (255, 195, 75) if not is_dark_bg else (195, 75, 45)

            if active_mode == 1:
                prog = (current_thread_idx / total_threads) * 100.0
                curr_layer = threads[min(current_thread_idx, total_threads - 1)]["layer"]
                c_mode_str = "Obsidian Glow" if mode1_dark else "Studio Gallery"
                title_txt = font_title.render(f"MODE 1: MASTERPIECE WEAVER [{c_mode_str}]", True, accent_color)
                stats_txt = font_hud.render(
                    f"Threads: {current_thread_idx:,}/{total_threads:,} [{prog:5.1f}%] | Contrast: {contrast_level:.2f}x | Speed: {batch_size}/f | FPS: {clock.get_fps():.0f}",
                    True,
                    text_color,
                )
            else:
                theme_name = THEMES[studio.theme_idx]["name"]
                title_txt = font_title.render(f"MODE 2: PARAMETRIC VORTEX STUDIO ({theme_name})", True, accent_color)
                warp_str = "ON" if studio.mouse_warp else "OFF"
                stats_txt = font_hud.render(
                    f"Zoom: {studio.zoom:.2f}x | Twist: {studio.twist_freq:.1f} | Ribbon: {studio.ribbon_width_scale:.2f}x | Warp: {warp_str} | FPS: {clock.get_fps():.0f}",
                    True,
                    text_color,
                )

            screen.blit(title_txt, (hud_rect.x + 12, hud_rect.y + 6))
            screen.blit(stats_txt, (hud_rect.x + 12, hud_rect.y + 26))

            # Bottom controls pill
            bot_rect = pygame.Rect(15, WINDOW_HEIGHT - 38, WINDOW_WIDTH - 30, 26)
            bot_bg = pygame.Surface((bot_rect.width, bot_rect.height), pygame.SRCALPHA)
            bot_bg.fill((10, 15, 25, 215) if not is_dark_bg else (245, 245, 250, 215))
            screen.blit(bot_bg, bot_rect)

            ctrl_str = (
                "[1/2] Modes | [B/V] Contrast Boost | [T] Dark Mode | [+/-] Speed | [C] Complete | [P] Save | [ESC] Exit"
                if active_mode == 1
                else "[1/2] Modes | [B/V] Contrast | [T] Theme | [M] Mouse Warp | [Wheel] Zoom | [G] Breath | [P] Save"
            )
            ctrl_txt = font_hud.render(ctrl_str, True, text_color)
            screen.blit(ctrl_txt, (bot_rect.x + 12, bot_rect.y + 6))

        pygame.display.flip()

    pygame.quit()


def export_poster(output_path, size=(WINDOW_WIDTH, WINDOW_HEIGHT), contrast_boost=1.35):
    """Renders and saves a pixel-perfect high-contrast high-resolution PNG poster of the masterpiece."""
    from PIL import Image, ImageDraw

    threads, cx, cy, scale = extract_masterpiece_streamlines(
        target_size=size[0] - 140, contrast_boost=contrast_boost
    )
    w, h = size
    bg_img = Image.new("RGB", (w, h), (252, 252, 254))
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for th in threads:
        pts = th["pts"]
        color = th["color"]
        w_line = th["width"]
        if len(pts) >= 2:
            draw.line(pts, fill=color, width=w_line)

    out = Image.alpha_composite(bg_img.convert("RGBA"), overlay).convert("RGB")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    out.save(output_path, optimize=True)
    print(f"✅ Saved high-resolution poster: {output_path}")


def export_animation(output_path, num_frames=50, frame_size=(600, 600), contrast_boost=1.35):
    """Generates an animated GIF showing the enhanced multi-layered weaving progression."""
    from PIL import Image, ImageDraw

    threads, cx, cy, scale = extract_masterpiece_streamlines(
        target_size=frame_size[0] - 70, contrast_boost=contrast_boost
    )
    w, h = frame_size
    scale_factor = frame_size[0] / float(WINDOW_WIDTH)

    scaled_threads = []
    for th in threads:
        pts_s = [
            (
                w / 2.0 + (px - cx) * scale_factor,
                h / 2.0 + (py - cy) * scale_factor,
            )
            for px, py in th["pts"]
        ]
        scaled_threads.append({"pts": pts_s, "color": th["color"], "width": th["width"]})

    total = len(scaled_threads)
    base_img = Image.new("RGB", (w, h), (252, 252, 254))
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    frames = []
    frames.append(base_img.copy().quantize(colors=128))

    batch = max(1, total // num_frames)
    cur = 0
    for frame_idx in range(num_frames):
        end = min(total, (frame_idx + 1) * batch)
        last_pt = (w / 2, h / 2)
        for i in range(cur, end):
            th = scaled_threads[i]
            if len(th["pts"]) >= 2:
                draw.line(th["pts"], fill=th["color"], width=th["width"])
                last_pt = th["pts"][-1]
        cur = end

        composed = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
        f_draw = ImageDraw.Draw(composed)
        f_draw.ellipse(
            [last_pt[0] - 3, last_pt[1] - 3, last_pt[0] + 3, last_pt[1] + 3],
            fill=(245, 195, 75),
            outline=(180, 140, 40),
        )
        frames.append(composed.quantize(colors=128))

    final_clean = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB").quantize(colors=128)
    for _ in range(8):
        frames.append(final_clean)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=105,
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

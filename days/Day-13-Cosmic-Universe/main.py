"""
Day 13: Cosmic Universe - Fine Pencil Hatching Simulation & Stellar Ignition
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A smooth, elegant, and authentic generative colored-pencil drawing simulation that
draws the cosmic universe nebula steadily from the top-left corner across to the opposite corner:
1. Starts precisely at corner (0, 0) in deep cosmic space with subtle ambient stars.
2. A fine pencil nib (3-pixel width) sweeps in continuous back-and-forth diagonal hatching bands
   (x + y = d), systematically sketching and shading across the entire canvas.
3. An authentic colored pencil stylus leads the drawing front, with a lead tip colored by the
   active pixel, warm cedar wood collar, hexagonal cosmic barrel, and micro-stardust graphite sparks.
4. 100% pixel-perfect replica of the master artwork—zero digital noise, zero blur, pristine crispness.
5. Upon reaching the far corner (1280, 640), brilliant stars ignite with astronomical 4-point cross
   diffraction spikes, transitioning into an interactive Living Cosmos mode.

Controls:
  [SPACE]     - Pause / Resume drawing
  [R]         - Restart drawing from corner (0, 0)
  [+] / [UP]  - Increase pencil drawing speed
  [-] / [DOWN]- Decrease pencil drawing speed
  [1] - [4]   - Speed presets (Slow, Normal, Fast, Hyper-lapse)
  [S]         - Save high-resolution screenshot
  [F]         - Toggle fullscreen mode
  [ESC/Q]     - Exit application
"""

import math
import os
import random
import sys
import numpy as np
import pygame

# 1. Configuration & Canvas Constants
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "cosmic_universe.jpg"

IMAGE_PATH = os.path.join(SCRIPT_DIR, IMAGE_NAME)
if not os.path.exists(IMAGE_PATH):
    IMAGE_PATH = IMAGE_NAME

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 640
FPS = 60

# Palette constants
SPACE_VOID = (5, 6, 16)
PENCIL_WIDTH = 3       # Spacing between diagonal hatching bands (pixels)
PENCIL_RADIUS = 2      # Radius of pencil nib contact patch (diameter 5 px)
DEFAULT_SPEED = 120    # Points rendered per frame (~21 seconds total)


def load_master_and_generate_pencil_path(image_path, width, height, pencil_width=3):
    """
    Loads reference masterpiece, creates scaled master surface,
    and builds continuous diagonal zig-zag pencil hatching path
    starting at corner (0, 0) and completing at (width, height).
    """
    if not os.path.exists(image_path):
        print(f"Error: Masterpiece image not found at '{image_path}'")
        sys.exit(1)

    raw_image = pygame.image.load(image_path)
    # High-quality smooth scaled master surface (100% exact pixel replica)
    scaled = pygame.transform.smoothscale(raw_image, (width, height))
    if pygame.display.get_surface():
        master_surface = scaled.convert()
    else:
        master_surface = scaled

    # Precompute diagonal hatching lines: x + y = d
    # Starting at corner (0, 0) with d = 0 up to (width + height)
    max_d = width + height
    bands = []
    for d in range(0, max_d + pencil_width, pencil_width):
        x_min = max(0, d - height)
        x_max = min(width, d)
        if x_min <= x_max:
            bands.append((d, x_min, x_max))

    # Build continuous zig-zag pencil trajectory
    pencil_path = []
    for i, (d, x_min, x_max) in enumerate(bands):
        line_len = math.hypot(x_max - x_min, x_max - x_min)
        steps = max(2, int(line_len / 2.5))

        # Alternate direction: even diagonals stroke down-left, odd stroke up-right
        if i % 2 == 0:
            xs = np.linspace(x_min, x_max, steps)
        else:
            xs = np.linspace(x_max, x_min, steps)

        for x in xs:
            pencil_path.append((int(x), int(d - x)))

    # Stellar core detection via brightness analysis
    arr = pygame.surfarray.array3d(master_surface)  # shape (width, height, 3)
    gray = (arr[:, :, 0] * 0.299 + arr[:, :, 1] * 0.587 + arr[:, :, 2] * 0.114)

    stars = []
    block_size = 14
    for bx in range(0, arr.shape[0] - block_size, block_size):
        for by in range(0, arr.shape[1] - block_size, block_size):
            sub = gray[bx:bx + block_size, by:by + block_size]
            max_val = np.max(sub)
            if max_val > 220:
                local_idx = np.unravel_index(np.argmax(sub), sub.shape)
                sx = bx + local_idx[0]
                sy = by + local_idx[1]
                r, g, b = arr[sx, sy]
                stars.append({
                    "x": int(sx),
                    "y": int(sy),
                    "brightness": float(max_val),
                    "color": (int(r), int(g), int(b)),
                    "phase": random.uniform(0, math.pi * 2),
                })

    stars.sort(key=lambda s: s["brightness"], reverse=True)

    # Key landmark celestial coordinates
    landmarks = {
        "primary_star": (int(width * (315 / 2560)), int(height * (786 / 1280))),
        "upper_gold_star": (int(width * (1692 / 2560)), int(height * (295 / 1280))),
        "cyan_core": (int(width * (654 / 2560)), int(height * (295 / 1280))),
        "horizon_core": (int(width * (1878 / 2560)), int(height * (724 / 1280))),
    }

    return {
        "master_surface": master_surface,
        "pencil_path": pencil_path,
        "stars": stars,
        "landmarks": landmarks,
    }


def draw_pencil(surface, tip_pos, lead_color=(255, 200, 100), angle_deg=50):
    """
    Renders an authentic colored-pencil stylus tilted at an ergonomic angle.
    - Lead tip matches current cosmic pigment.
    - Tapered cedar wood cone.
    - 3D-shaded hexagonal barrel with golden ferrule.
    - Tip contact point with subtle graphite glow.
    """
    cx, cy = tip_pos
    rad = math.radians(angle_deg)
    ux = math.cos(rad)
    uy = -math.sin(rad)
    # Perpendicular unit vector
    px = -uy
    py = ux

    d_lead = 7
    w_lead = 2.2
    d_wood = 18
    w_wood = 5.0
    d_barrel = 56
    w_barrel = 5.0

    # Contact point glow
    pygame.draw.circle(surface, (255, 255, 255, 180), (cx, cy), 2)
    pygame.draw.circle(surface, (*lead_color[:3], 90), (cx, cy), 6)

    # Lead tip polygon
    p_tip = (cx, cy)
    p_lead_l = (cx + ux * d_lead + px * w_lead, cy + uy * d_lead + py * w_lead)
    p_lead_r = (cx + ux * d_lead - px * w_lead, cy + uy * d_lead - py * w_lead)
    pygame.draw.polygon(surface, lead_color, [p_tip, p_lead_l, p_lead_r])
    pygame.draw.polygon(surface, (255, 255, 255), [p_tip, p_lead_l, p_lead_r], 1)

    # Cedar wood collar
    p_wood_l = (cx + ux * d_wood + px * w_wood, cy + uy * d_wood + py * w_wood)
    p_wood_r = (cx + ux * d_wood - px * w_wood, cy + uy * d_wood - py * w_wood)
    pygame.draw.polygon(surface, (222, 184, 135), [p_lead_l, p_wood_l, p_wood_r, p_lead_r])
    pygame.draw.polygon(surface, (180, 140, 95), [p_lead_l, p_wood_l, p_wood_r, p_lead_r], 1)

    # Hexagonal barrel facets (highlight top, shadow bottom)
    p_bar_l = (cx + ux * d_barrel + px * w_barrel, cy + uy * d_barrel + py * w_barrel)
    p_bar_r = (cx + ux * d_barrel - px * w_barrel, cy + uy * d_barrel - py * w_barrel)
    p_bar_mid = (cx + ux * d_barrel, cy + uy * d_barrel)
    p_wood_mid = (cx + ux * d_wood, cy + uy * d_wood)

    pygame.draw.polygon(surface, (45, 75, 135), [p_wood_l, p_bar_l, p_bar_mid, p_wood_mid])
    pygame.draw.polygon(surface, (22, 38, 75), [p_wood_mid, p_bar_mid, p_bar_r, p_wood_r])

    # Golden ferrule decorative ring
    d_f1 = 46
    d_f2 = 50
    p_f1_l = (cx + ux * d_f1 + px * w_barrel, cy + uy * d_f1 + py * w_barrel)
    p_f1_r = (cx + ux * d_f1 - px * w_barrel, cy + uy * d_f1 - py * w_barrel)
    p_f2_l = (cx + ux * d_f2 + px * w_barrel, cy + uy * d_f2 + py * w_barrel)
    p_f2_r = (cx + ux * d_f2 - px * w_barrel, cy + uy * d_f2 - py * w_barrel)
    pygame.draw.polygon(surface, (255, 215, 0), [p_f1_l, p_f2_l, p_f2_r, p_f1_r])

    # Clean outer contour
    pygame.draw.polygon(surface, (15, 20, 35), [p_wood_l, p_bar_l, p_bar_r, p_wood_r], 1)


def draw_diffraction_spike(surface, center, length, color, core_radius=6, spike_width=2):
    """Renders a clean astronomical 4-point cross diffraction spike with glowing core."""
    cx, cy = center
    r, g, b = color

    # Outer soft halo
    for rad in range(int(core_radius * 2.5), 0, -2):
        alpha = int(55 * (1.0 - rad / (core_radius * 2.5)))
        pygame.draw.circle(surface, (r, g, b, alpha), (cx, cy), rad)

    # Core luminous disc
    pygame.draw.circle(surface, (255, 255, 255, 255), (cx, cy), core_radius)
    pygame.draw.circle(surface, (r, g, b, 220), (cx, cy), int(core_radius * 1.4))

    # Horizontal and vertical diffraction spikes
    p_left = (max(0, cx - length), cy)
    p_right = (min(CANVAS_WIDTH, cx + length), cy)
    pygame.draw.line(surface, (r, g, b, 210), p_left, p_right, spike_width)
    pygame.draw.line(surface, (255, 255, 255, 240), (cx - int(length * 0.35), cy), (cx + int(length * 0.35), cy), 1)

    p_top = (cx, max(0, cy - length))
    p_bottom = (cx, min(CANVAS_HEIGHT, cy + length))
    pygame.draw.line(surface, (r, g, b, 210), p_top, p_bottom, spike_width)
    pygame.draw.line(surface, (255, 255, 255, 240), (cx, cy - int(length * 0.35)), (cx, cy + int(length * 0.35)), 1)

    # Diagonal anamorphic streaks
    diag_len = int(length * 0.35)
    for sx, sy in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
        pygame.draw.line(surface, (r, g, b, 100), (cx, cy), (cx + sx * diag_len, cy + sy * diag_len), 1)


class StardustParticle:
    """Floating stardust micro-particle emitting from pencil tip or mouse."""

    def __init__(self, x, y, color=None):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.radius = random.uniform(1.0, 2.5)
        self.color = color if color else random.choice([(255, 240, 180), (140, 230, 255), (255, 190, 230)])
        self.life = random.randint(25, 60)
        self.max_life = self.life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = int(255 * (self.life / self.max_life))
        r, g, b = self.color
        pygame.draw.circle(surface, (r, g, b, alpha), (int(self.x), int(self.y)), int(self.radius))


def main():
    # 2. Setup Pygame
    pygame.init()
    pygame.display.set_caption("🌌 Day 13: Cosmic Universe - Pencil Hatching | 30 Days Python")

    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Preload assets and calculate diagonal pencil trajectory
    assets = load_master_and_generate_pencil_path(
        IMAGE_PATH, CANVAS_WIDTH, CANVAS_HEIGHT, pencil_width=PENCIL_WIDTH
    )
    master_surface = assets["master_surface"]
    pencil_path = assets["pencil_path"]
    total_path_points = len(pencil_path)
    stars = assets["stars"]
    landmarks = assets["landmarks"]

    # Layer surfaces
    paint_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    paint_layer.fill(SPACE_VOID)
    overlay_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)

    # Ambient deep space background stars
    random.seed(42)
    ambient_stars = []
    for _ in range(160):
        ax = random.randint(0, CANVAS_WIDTH)
        ay = random.randint(0, CANVAS_HEIGHT)
        arad = random.choice([1, 1, 2])
        abright = random.randint(70, 180)
        ambient_stars.append((ax, ay, arad, abright))

    for ax, ay, arad, abright in ambient_stars:
        pygame.draw.circle(paint_layer, (abright, abright, int(abright * 1.1)), (ax, ay), arad)

    # HUD Font
    try:
        font_hud = pygame.font.SysFont("couriernew", 14, bold=True)
    except Exception:
        font_hud = pygame.font.Font(None, 14)

    running = True
    fullscreen = False
    is_paused = False

    # Drawing state
    current_pt_idx = 0
    points_per_frame = DEFAULT_SPEED
    drawing_complete = False
    stellar_progress = 0.0

    particles = []

    while running:
        clock.tick(FPS)

        # Handle user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                elif event.key == pygame.K_r:
                    # Restart drawing from corner (0, 0)
                    current_pt_idx = 0
                    drawing_complete = False
                    is_paused = False
                    stellar_progress = 0.0
                    paint_layer.fill(SPACE_VOID)
                    for ax, ay, arad, abright in ambient_stars:
                        pygame.draw.circle(paint_layer, (abright, abright, int(abright * 1.1)), (ax, ay), arad)
                    particles.clear()
                elif event.key in (pygame.K_UP, pygame.K_PLUS, pygame.K_EQUALS):
                    points_per_frame = min(600, points_per_frame + 30)
                elif event.key in (pygame.K_DOWN, pygame.K_MINUS):
                    points_per_frame = max(30, points_per_frame - 30)
                elif event.key == pygame.K_1:
                    points_per_frame = 60    # Slow & Meditative
                elif event.key == pygame.K_2:
                    points_per_frame = 120   # Standard Studio
                elif event.key == pygame.K_3:
                    points_per_frame = 240   # Quick Sketch
                elif event.key == pygame.K_4:
                    points_per_frame = 480   # Hyper-lapse
                elif event.key == pygame.K_s:
                    snap_name = "cosmic_universe_screenshot.png"
                    pygame.image.save(screen, snap_name)
                    print(f"Saved screenshot: {snap_name}")
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                for _ in range(2):
                    particles.append(StardustParticle(mx, my))

        # -------------------------------------------------------------
        # PENCIL HATCHING DRAWING STEP
        # -------------------------------------------------------------
        pencil_tip = None
        current_lead_color = (255, 200, 100)

        if not drawing_complete and not is_paused:
            for _ in range(points_per_frame):
                if current_pt_idx >= total_path_points:
                    drawing_complete = True
                    break

                px, py = pencil_path[current_pt_idx]
                pencil_tip = (px, py)

                # Copy pencil-nib patch from master surface onto canvas
                x1 = max(0, px - PENCIL_RADIUS)
                y1 = max(0, py - PENCIL_RADIUS)
                x2 = min(CANVAS_WIDTH, px + PENCIL_RADIUS + 1)
                y2 = min(CANVAS_HEIGHT, py + PENCIL_RADIUS + 1)
                w = x2 - x1
                h = y2 - y1

                if w > 0 and h > 0:
                    patch = master_surface.subsurface(pygame.Rect(x1, y1, w, h))
                    paint_layer.blit(patch, (x1, y1))

                current_pt_idx += 1

            # Get current lead color from active pencil tip
            if pencil_tip:
                tx = max(0, min(CANVAS_WIDTH - 1, pencil_tip[0]))
                ty = max(0, min(CANVAS_HEIGHT - 1, pencil_tip[1]))
                current_lead_color = master_surface.get_at((tx, ty))[:3]
                if random.random() < 0.35:
                    particles.append(StardustParticle(tx, ty, current_lead_color))
        elif drawing_complete:
            # Fully lock master surface when drawing completes (100% exact replica)
            paint_layer.blit(master_surface, (0, 0))

        # Clear overlay layer for dynamic lighting, star flares, pencil, and HUD
        overlay_layer.fill((0, 0, 0, 0))

        # -------------------------------------------------------------
        # STELLAR IGNITION & DIFFRACTION FLARES
        # -------------------------------------------------------------
        progress_pct = min(1.0, current_pt_idx / total_path_points)
        if progress_pct >= 0.80:
            if stellar_progress < 1.0:
                stellar_progress = min(1.0, stellar_progress + 0.02)

            num_ignited = int(len(stars) * stellar_progress)
            time_ticks = pygame.time.get_ticks() * 0.003

            # Render stars with gentle organic twinkle
            for i in range(num_ignited):
                s = stars[i]
                twinkle = 1.0 + 0.16 * math.sin(time_ticks + s["phase"])
                r_rad = max(1.0, 1.8 * twinkle)

                pygame.draw.circle(overlay_layer, s["color"], (s["x"], s["y"]), int(r_rad))
                pygame.draw.circle(overlay_layer, (255, 255, 255), (s["x"], s["y"]), max(1, int(r_rad * 0.5)))

            # Primary 4-point golden diffraction star in lower-left
            p_x, p_y = landmarks["primary_star"]
            draw_diffraction_spike(
                overlay_layer,
                (p_x, p_y),
                int(140 * stellar_progress),
                (255, 220, 90),
                core_radius=7,
                spike_width=3,
            )

            # Secondary upper golden star
            u_x, u_y = landmarks["upper_gold_star"]
            draw_diffraction_spike(
                overlay_layer,
                (u_x, u_y),
                int(80 * stellar_progress),
                (255, 240, 160),
                core_radius=5,
                spike_width=2,
            )

            # Cyan core star
            c_x, c_y = landmarks["cyan_core"]
            draw_diffraction_spike(
                overlay_layer,
                (c_x, c_y),
                int(65 * stellar_progress),
                (140, 240, 255),
                core_radius=4,
                spike_width=2,
            )

            # Horizon incandescent core warm breathing aura
            h_x, h_y = landmarks["horizon_core"]
            pulse = 1.0 + 0.05 * math.sin(time_ticks * 0.8)
            for rad in range(int(85 * stellar_progress), 0, -5):
                alpha = int((80 * (1.0 - rad / (85.0 * stellar_progress))) * pulse)
                pygame.draw.circle(overlay_layer, (255, 245, 205, alpha), (h_x, h_y), rad)

        # -------------------------------------------------------------
        # RENDER PENCIL STYLUS CURSOR
        # -------------------------------------------------------------
        if not drawing_complete and pencil_tip:
            draw_pencil(overlay_layer, pencil_tip, current_lead_color, angle_deg=50)

        # Update and draw stardust particles
        particles = [p for p in particles if p.update()]
        for p in particles:
            p.draw(overlay_layer)

        # -------------------------------------------------------------
        # CLEAN STATUS BAR & CONTROLS HUD
        # -------------------------------------------------------------
        hud_bg = pygame.Surface((CANVAS_WIDTH, 28), pygame.SRCALPHA)
        hud_bg.fill((6, 8, 18, 185))
        overlay_layer.blit(hud_bg, (0, CANVAS_HEIGHT - 28))

        pct = int(progress_pct * 100)
        if is_paused:
            phase_label = "PAUSED (Press [SPACE] to resume)"
        elif pct < 25:
            phase_label = "Pencil Shading: Corner (0,0) & Upper Deep Cosmos"
        elif pct < 60:
            phase_label = "Pencil Hatching: Ethereal Nebula Clouds & Azure Filaments"
        elif pct < 95:
            phase_label = "Pencil Detailing: Golden Cosmic Cliffs & Horizon Core"
        else:
            phase_label = "Completed: Pristine Cosmic Universe (Living Cosmos)"

        # Progress bar
        bar_w = int(CANVAS_WIDTH * (pct / 100.0))
        pygame.draw.rect(overlay_layer, (255, 195, 50), (0, CANVAS_HEIGHT - 3, bar_w, 3))

        speed_factor = round(points_per_frame / DEFAULT_SPEED, 1)
        status_text = f"✏️ PENCIL SHADING | {phase_label} [{pct}%] | Speed: {points_per_frame}pts/f ({speed_factor}x)"
        rendered_status = font_hud.render(status_text, True, (240, 245, 255))
        overlay_layer.blit(rendered_status, (14, CANVAS_HEIGHT - 21))

        controls_text = "[SPACE] Pause | [R] Restart | [+/-] Speed | [S] Snap | [F] Full | [ESC] Exit"
        rendered_ctrl = font_hud.render(controls_text, True, (180, 205, 235))
        overlay_layer.blit(rendered_ctrl, (CANVAS_WIDTH - rendered_ctrl.get_width() - 14, CANVAS_HEIGHT - 21))

        # Composite everything to screen
        screen.blit(paint_layer, (0, 0))
        screen.blit(overlay_layer, (0, 0))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

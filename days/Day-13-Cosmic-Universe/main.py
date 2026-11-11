"""
Day 13: Cosmic Universe - Progressive Corner Drawing & Vice-Versa Simulation
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
An authentic, satisfying generative drawing simulation that brings the cosmic universe
nebula to life steadily, revealing small visible portions as the drawing tool glides
from corner to corner across the canvas:
1. Corner-to-Corner Progressive Drawing: Starts at one corner (e.g., Top-Left (0, 0))
   and sweeps along continuous diagonal bands across to the opposite corner (1280, 640).
2. Visible Portion Revealing: Rather than digital static or sudden reveals, every stroke
   paints a clearly visible circular portion (radius ~24 px) of the cosmic universe,
   letting you watch each star cluster, glowing nebula pillar, and golden cliff emerge piece by piece.
3. Vice-Versa Mode:
   - Forward: Draws from Top-Left (0, 0) to Bottom-Right (1280, 640).
   - Vice-Versa: Draws from Bottom-Right (1280, 640) back to Top-Left (0, 0), revealing
     the golden horizon cliffs first and sweeping up to the deep cosmos!
   - Auto-Loop: Continuously draws from corner to corner and vice-versa in a hypnotic cycle.
4. Ergonomic Stylus & Lead Indicator: An authentic colored-pencil stylus leads the stroke,
   complete with active pigment tip, cedar wood collar, 3D barrel, active brush radius ring,
   and floating stardust graphite particles.
5. Zero Sudden Pops: Every single pixel is progressively drawn by overlapping strokes—100%
   genuine drawing coverage without any abrupt full-image replacement.
6. Stellar Ignition: Upon reaching the opposite corner, celestial stars ignite with 4-point
   cross diffraction spikes into an interactive Living Cosmos mode.

Controls:
  [SPACE]     - Pause / Resume drawing
  [V]         - Toggle Vice-Versa corner direction (Top-Left <-> Bottom-Right)
  [R]         - Restart current drawing from corner
  [A]         - Toggle Auto-Loop Vice-Versa cycle (on by default)
  [+] / [UP]  - Increase drawing speed (+1 pt/frame)
  [-] / [DOWN]- Decrease drawing speed (-1 pt/frame)
  [1] - [4]   - Speed presets (1: Meditative, 2: Standard, 3: Fast, 4: Turbo)
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

# Palette & Brush Constants
SPACE_VOID = (5, 6, 16)
BRUSH_RADIUS = 24     # Visible portion radius (diameter ~48 px)
DEFAULT_SPEED = 5     # Points rendered per frame (~22 seconds per pass)


def load_master_and_generate_trajectories(image_path, width, height, brush_radius=24):
    """
    Loads reference masterpiece, creates scaled master surface,
    and builds continuous diagonal corner-to-corner trajectories
    (Forward and Vice-Versa) ensuring 100% canvas coverage.
    """
    if not os.path.exists(image_path):
        print(f"Error: Masterpiece image not found at '{image_path}'")
        sys.exit(1)

    raw_image = pygame.image.load(image_path)
    scaled = pygame.transform.smoothscale(raw_image, (width, height))
    if pygame.display.get_surface():
        master_surface = scaled.convert()
    else:
        master_surface = scaled

    # Step size between diagonal bands ensures smooth overlapping coverage
    step_d = int(brush_radius * 0.85)

    # Diagonal bands: x + y = d, from -brush_radius to width + height + brush_radius
    bands = []
    for d in range(-brush_radius, width + height + brush_radius + step_d, step_d):
        x_min = max(-brush_radius, d - height - brush_radius)
        x_max = min(width + brush_radius, d + brush_radius)
        if x_min <= x_max:
            bands.append((d, x_min, x_max))

    # Build continuous zig-zag forward trajectory from Top-Left to Bottom-Right
    forward_path = []
    for i, (d, x_min, x_max) in enumerate(bands):
        line_len = math.hypot(x_max - x_min, x_max - x_min)
        steps = max(3, int(line_len / (brush_radius * 0.4)))

        # Alternate direction for continuous serpentine motion
        if i % 2 == 0:
            xs = np.linspace(x_min, x_max, steps)
        else:
            xs = np.linspace(x_max, x_min, steps)

        for x in xs:
            forward_path.append((int(x), int(d - x)))

    # Vice-Versa trajectory: exact reverse from Bottom-Right to Top-Left
    reverse_path = forward_path[::-1]

    # Precompute circular alpha mask for smooth portion blitting
    mask_size = 2 * brush_radius + 1
    brush_mask = pygame.Surface((mask_size, mask_size), pygame.SRCALPHA)
    pygame.draw.circle(brush_mask, (255, 255, 255, 255), (brush_radius, brush_radius), brush_radius)

    # Stellar core detection via brightness analysis
    arr = pygame.surfarray.array3d(master_surface)
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

    # Key landmark coordinates
    landmarks = {
        "primary_star": (int(width * (315 / 2560)), int(height * (786 / 1280))),
        "upper_gold_star": (int(width * (1692 / 2560)), int(height * (295 / 1280))),
        "cyan_core": (int(width * (654 / 2560)), int(height * (295 / 1280))),
        "horizon_core": (int(width * (1878 / 2560)), int(height * (724 / 1280))),
    }

    return {
        "master_surface": master_surface,
        "forward_path": forward_path,
        "reverse_path": reverse_path,
        "brush_mask": brush_mask,
        "brush_radius": brush_radius,
        "stars": stars,
        "landmarks": landmarks,
    }


def draw_pencil(surface, tip_pos, lead_color=(255, 200, 100), angle_deg=50, brush_radius=24):
    """
    Renders an authentic colored-pencil stylus with a luminous brush ring.
    - Luminous ring marks the active small portion being painted.
    - Lead tip matches active cosmic pigment.
    - Cedar wood collar and 3D hexagonal barrel with golden ferrule.
    """
    cx, cy = tip_pos

    # Subtle glowing brush outline indicating active visible portion
    pygame.draw.circle(surface, (*lead_color[:3], 45), (cx, cy), brush_radius, 1)
    pygame.draw.circle(surface, (255, 255, 255, 75), (cx, cy), max(2, brush_radius // 2), 1)

    rad = math.radians(angle_deg)
    ux = math.cos(rad)
    uy = -math.sin(rad)
    px = -uy
    py = ux

    d_lead = 8
    w_lead = 2.5
    d_wood = 20
    w_wood = 5.5
    d_barrel = 62
    w_barrel = 5.5

    # Contact point core glow
    pygame.draw.circle(surface, (255, 255, 255, 220), (cx, cy), 3)
    pygame.draw.circle(surface, (*lead_color[:3], 120), (cx, cy), 8)

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

    # Golden ferrule ring
    d_f1 = 52
    d_f2 = 56
    p_f1_l = (cx + ux * d_f1 + px * w_barrel, cy + uy * d_f1 + py * w_barrel)
    p_f1_r = (cx + ux * d_f1 - px * w_barrel, cy + uy * d_f1 - py * w_barrel)
    p_f2_l = (cx + ux * d_f2 + px * w_barrel, cy + uy * d_f2 + py * w_barrel)
    p_f2_r = (cx + ux * d_f2 - px * w_barrel, cy + uy * d_f2 - py * w_barrel)
    pygame.draw.polygon(surface, (255, 215, 0), [p_f1_l, p_f2_l, p_f2_r, p_f1_r])

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
        self.life = random.randint(25, 55)
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
    pygame.display.set_caption("🌌 Day 13: Cosmic Universe - Progressive Corner & Vice-Versa | 30 Days Python")

    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Preload trajectories and assets
    assets = load_master_and_generate_trajectories(
        IMAGE_PATH, CANVAS_WIDTH, CANVAS_HEIGHT, brush_radius=BRUSH_RADIUS
    )
    master_surface = assets["master_surface"]
    forward_path = assets["forward_path"]
    reverse_path = assets["reverse_path"]
    brush_mask = assets["brush_mask"]
    brush_rad = assets["brush_radius"]
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
    auto_loop = True

    # Mode: "FORWARD" (Top-Left -> Bottom-Right) or "VICE_VERSA" (Bottom-Right -> Top-Left)
    current_mode = "FORWARD"
    current_path = forward_path
    total_path_points = len(current_path)

    current_pt_idx = 0
    points_per_frame = DEFAULT_SPEED
    drawing_complete = False
    stellar_progress = 0.0
    completion_pause_timer = 0  # Pause frames after completion before auto-vice-versa

    particles = []

    def reset_canvas(mode):
        nonlocal current_mode, current_path, total_path_points, current_pt_idx, drawing_complete, stellar_progress, completion_pause_timer
        current_mode = mode
        current_path = forward_path if mode == "FORWARD" else reverse_path
        total_path_points = len(current_path)
        current_pt_idx = 0
        drawing_complete = False
        stellar_progress = 0.0
        completion_pause_timer = 0
        paint_layer.fill(SPACE_VOID)
        for ax, ay, arad, abright in ambient_stars:
            pygame.draw.circle(paint_layer, (abright, abright, int(abright * 1.1)), (ax, ay), arad)
        particles.clear()

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
                elif event.key == pygame.K_v:
                    # Toggle Vice-Versa corner direction
                    new_mode = "VICE_VERSA" if current_mode == "FORWARD" else "FORWARD"
                    reset_canvas(new_mode)
                elif event.key == pygame.K_r:
                    # Restart current corner drawing
                    reset_canvas(current_mode)
                elif event.key == pygame.K_a:
                    auto_loop = not auto_loop
                elif event.key in (pygame.K_UP, pygame.K_PLUS, pygame.K_EQUALS):
                    points_per_frame = min(30, points_per_frame + 1)
                elif event.key in (pygame.K_DOWN, pygame.K_MINUS):
                    points_per_frame = max(1, points_per_frame - 1)
                elif event.key == pygame.K_1:
                    points_per_frame = 3     # Meditative
                elif event.key == pygame.K_2:
                    points_per_frame = 5     # Standard (~22s)
                elif event.key == pygame.K_3:
                    points_per_frame = 10    # Fast (~11s)
                elif event.key == pygame.K_4:
                    points_per_frame = 20    # Turbo (~5s)
                elif event.key == pygame.K_s:
                    snap_name = f"cosmic_universe_{current_mode.lower()}.png"
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
        # PROGRESSIVE CORNER-TO-CORNER DRAWING STEP
        # -------------------------------------------------------------
        pencil_tip = None
        current_lead_color = (255, 200, 100)

        if not drawing_complete and not is_paused:
            for _ in range(points_per_frame):
                if current_pt_idx >= total_path_points:
                    drawing_complete = True
                    break

                px, py = current_path[current_pt_idx]
                pencil_tip = (px, py)

                # Transfer circular visible portion onto paint layer
                x1 = px - brush_rad
                y1 = py - brush_rad
                src_x1 = max(0, x1)
                src_y1 = max(0, y1)
                src_x2 = min(CANVAS_WIDTH, x1 + 2 * brush_rad + 1)
                src_y2 = min(CANVAS_HEIGHT, y1 + 2 * brush_rad + 1)
                w = src_x2 - src_x1
                h = src_y2 - src_y1

                if w > 0 and h > 0:
                    patch = master_surface.subsurface(pygame.Rect(src_x1, src_y1, w, h)).copy()
                    mask_sub = brush_mask.subsurface(pygame.Rect(src_x1 - x1, src_y1 - y1, w, h))
                    patch.blit(mask_sub, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    paint_layer.blit(patch, (src_x1, src_y1))

                current_pt_idx += 1

            # Get current lead color from active drawing tip
            if pencil_tip:
                tx = max(0, min(CANVAS_WIDTH - 1, pencil_tip[0]))
                ty = max(0, min(CANVAS_HEIGHT - 1, pencil_tip[1]))
                current_lead_color = master_surface.get_at((tx, ty))[:3]
                if random.random() < 0.40:
                    particles.append(StardustParticle(tx, ty, current_lead_color))
        elif drawing_complete:
            # Handle post-completion celebration & Auto-Loop Vice-Versa
            if auto_loop:
                completion_pause_timer += 1
                if completion_pause_timer >= 180:  # 3 seconds pause with ignited stars
                    # Switch to Vice-Versa direction
                    next_mode = "VICE_VERSA" if current_mode == "FORWARD" else "FORWARD"
                    reset_canvas(next_mode)

        # Clear overlay layer for dynamic effects, pencil, and HUD
        overlay_layer.fill((0, 0, 0, 0))

        # -------------------------------------------------------------
        # STELLAR IGNITION & DIFFRACTION FLARES
        # -------------------------------------------------------------
        progress_pct = min(1.0, current_pt_idx / total_path_points)
        if progress_pct >= 0.85:
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

            # Primary golden star diffraction spike
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
            # Angle adapts ergonomically to motion direction
            angle = 50 if current_mode == "FORWARD" else 130
            draw_pencil(overlay_layer, pencil_tip, current_lead_color, angle_deg=angle, brush_radius=brush_rad)

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
        mode_label = "Top-Left (0,0) -> Bottom-Right" if current_mode == "FORWARD" else "Vice-Versa: Bottom-Right -> Top-Left"

        if is_paused:
            status_text = f"⏸️ PAUSED | Mode: {mode_label} [{pct}%]"
        elif drawing_complete:
            status_text = f"✨ MASTERPIECE COMPLETE | Mode: {mode_label} [100%]"
        else:
            status_text = f"✏️ DRAWING: {mode_label} [{pct}%] | Speed: {points_per_frame}pts/f"

        rendered_status = font_hud.render(status_text, True, (240, 245, 255))
        overlay_layer.blit(rendered_status, (14, CANVAS_HEIGHT - 21))

        controls_text = "[SPACE] Pause | [V] Vice-Versa | [R] Restart | [A] Auto-Loop | [+/-] Speed | [ESC] Exit"
        rendered_ctrl = font_hud.render(controls_text, True, (180, 205, 235))
        overlay_layer.blit(rendered_ctrl, (CANVAS_WIDTH - rendered_ctrl.get_width() - 14, CANVAS_HEIGHT - 21))

        # Progress bar
        bar_w = int(CANVAS_WIDTH * (pct / 100.0))
        bar_color = (255, 195, 50) if current_mode == "FORWARD" else (140, 220, 255)
        pygame.draw.rect(overlay_layer, bar_color, (0, CANVAS_HEIGHT - 3, bar_w, 3))

        # Composite everything to screen
        screen.blit(paint_layer, (0, 0))
        screen.blit(overlay_layer, (0, 0))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

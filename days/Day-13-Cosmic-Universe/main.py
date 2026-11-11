"""
Day 13: Cosmic Universe - Progressive Corner Drawing & Vice-Versa Simulation
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A smooth, authentic generative digital painting simulation that draws the
exact, pristine Cosmic Universe image slowly and steadily from corner to corner:
1. Exact Image Fidelity: 100% faithful reproduction of the original cosmic universe image
   (no fake geometric shapes, no giant circles, no artificial overlays).
2. Visible Portion Revealing: The pencil glides across the canvas from one corner,
   progressively revealing small, clear portions (radius ~24 px) of the magnificent nebula.
3. Corner-to-Corner Trajectories:
   - Forward: Draws from Top-Left (0, 0) across diagonal zig-zag bands to Bottom-Right (1280, 640).
   - Vice-Versa: Draws from Bottom-Right (1280, 640) back to Top-Left (0, 0), revealing
     the golden cliffs first and sweeping towards deep space.
   - Auto-Loop: Alternates between Forward and Vice-Versa drawing passes.
4. Ergonomic Pencil Stylus: A classic colored-pencil stylus leads the stroke with an active
   pigment lead tip, cedar wood collar, 3D barrel, and floating stardust graphite particles.

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
    # Scaled master surface (100% exact pixel replica)
    scaled = pygame.transform.smoothscale(raw_image, (width, height))
    master_surface = scaled.convert() if pygame.display.get_surface() else scaled

    # Step size between diagonal bands ensures smooth overlapping coverage
    step_d = int(brush_radius * 0.85)

    # Diagonal bands: x + y = d, from 0 to width + height
    bands = []
    for d in range(0, width + height + step_d, step_d):
        x_min = max(0, d - height)
        x_max = min(width, d)
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

    # Ensure the very corners are explicitly drawn
    if forward_path[0] != (0, 0):
        forward_path.insert(0, (0, 0))
    if forward_path[-1] != (width, height):
        forward_path.append((width, height))

    # Vice-Versa trajectory: exact reverse from Bottom-Right to Top-Left
    reverse_path = forward_path[::-1]

    return {
        "master_surface": master_surface,
        "forward_path": forward_path,
        "reverse_path": reverse_path,
        "brush_radius": brush_radius,
    }


def draw_pencil(surface, tip_pos, lead_color=(255, 200, 100), angle_deg=50, brush_radius=24):
    """
    Renders an authentic colored-pencil stylus with a subtle brush guide ring.
    - Luminous ring marks the active portion being painted.
    - Lead tip matches active cosmic pigment.
    - Cedar wood collar and 3D hexagonal barrel with golden ferrule.
    """
    cx, cy = tip_pos

    # Subtle glowing brush guide ring indicating active visible portion
    pygame.draw.circle(surface, (*lead_color[:3], 60), (cx, cy), brush_radius, 1)

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
    pygame.display.set_caption("🌌 Day 13: Cosmic Universe - 100% Exact Image Drawing | 30 Days Python")

    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Preload trajectories and assets
    assets = load_master_and_generate_trajectories(
        IMAGE_PATH, CANVAS_WIDTH, CANVAS_HEIGHT, brush_radius=BRUSH_RADIUS
    )
    master_surface = assets["master_surface"]
    forward_path = assets["forward_path"]
    reverse_path = assets["reverse_path"]
    brush_rad = assets["brush_radius"]

    # Layer surfaces (convert to match display format perfectly)
    paint_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT)).convert()
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
    completion_pause_timer = 0  # Pause frames after completion before auto-vice-versa

    particles = []

    def reset_canvas(mode):
        nonlocal current_mode, current_path, total_path_points, current_pt_idx, drawing_complete, completion_pause_timer
        current_mode = mode
        current_path = forward_path if mode == "FORWARD" else reverse_path
        total_path_points = len(current_path)
        current_pt_idx = 0
        drawing_complete = False
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
                    # Ensure canvas is 100% covered by the master image
                    paint_layer.blit(master_surface, (0, 0))
                    break

                px, py = current_path[current_pt_idx]
                pencil_tip = (px, py)

                # Transfer exact visible portion from master surface onto canvas
                x1 = max(0, px - brush_rad)
                y1 = max(0, py - brush_rad)
                x2 = min(CANVAS_WIDTH, px + brush_rad + 1)
                y2 = min(CANVAS_HEIGHT, py + brush_rad + 1)
                w = x2 - x1
                h = y2 - y1

                if w > 0 and h > 0:
                    patch = master_surface.subsurface(pygame.Rect(x1, y1, w, h))
                    paint_layer.blit(patch, (x1, y1))

                current_pt_idx += 1

            # Get current lead color from active drawing tip
            if pencil_tip:
                tx = max(0, min(CANVAS_WIDTH - 1, pencil_tip[0]))
                ty = max(0, min(CANVAS_HEIGHT - 1, pencil_tip[1]))
                current_lead_color = master_surface.get_at((tx, ty))[:3]
                if random.random() < 0.40:
                    particles.append(StardustParticle(tx, ty, current_lead_color))
        elif drawing_complete:
            # Handle post-completion pause & Auto-Loop Vice-Versa
            if auto_loop:
                completion_pause_timer += 1
                if completion_pause_timer >= 180:  # 3 seconds pause on finished masterpiece
                    # Switch to Vice-Versa direction
                    next_mode = "VICE_VERSA" if current_mode == "FORWARD" else "FORWARD"
                    reset_canvas(next_mode)

        # Clear overlay layer for dynamic pencil and HUD only
        overlay_layer.fill((0, 0, 0, 0))

        # -------------------------------------------------------------
        # RENDER PENCIL STYLUS CURSOR (While drawing)
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

        progress_pct = min(1.0, current_pt_idx / total_path_points)
        pct = int(progress_pct * 100)
        mode_label = "Top-Left (0,0) -> Bottom-Right" if current_mode == "FORWARD" else "Vice-Versa: Bottom-Right -> Top-Left"

        if is_paused:
            status_text = f"⏸️ PAUSED | Mode: {mode_label} [{pct}%]"
        elif drawing_complete:
            status_text = f"✨ MASTERPIECE COMPLETE | 100% Exact Cosmic Universe | Mode: {mode_label}"
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

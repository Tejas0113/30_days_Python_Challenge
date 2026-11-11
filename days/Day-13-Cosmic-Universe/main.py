"""
Day 13: Cosmic Universe - Generative Digital Painting & Stellar Ignition
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A smooth, elegant, and authentic generative digital painting simulation that
draws the cosmic universe nebula steadily and cleanly across the canvas:
1. Starts cleanly in deep cosmic space with distant ambient stars.
2. A luminous celestial brush sweeps continuously across the canvas, painting
   every vibrant cloud, glowing filament, and celestial cliff in pristine detail.
3. Zero noise, zero artifacts—every stroke reveals the exact, rich master artwork.
4. Prominent stars ignite in sequence with brilliant 4-point cross diffraction spikes.
5. Living cosmos mode with gentle stellar twinkling and interactive stardust.

Controls:
  [SPACE] - Replay slow cosmic drawing animation from scratch
  [S]     - Save high-resolution screenshot
  [F]     - Toggle fullscreen mode
  [ESC/Q] - Exit application
"""

import math
import os
import random
import sys
import cv2
import numpy as np
import pygame

# 1. Configuration & Parameters
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


def load_master_and_generate_path(image_path, width, height, brush_radius=36):
    """Loads reference masterpiece and builds an organic, continuous painting trajectory."""
    if not os.path.exists(image_path):
        print(f"Error: Masterpiece image not found at '{image_path}'")
        sys.exit(1)

    src_bgr = cv2.imread(image_path)
    if src_bgr is None:
        print(f"Error: OpenCV could not read '{image_path}'")
        sys.exit(1)

    # Scaled high-fidelity RGB master surface
    resized_bgr = cv2.resize(src_bgr, (width, height), interpolation=cv2.INTER_LANCZOS4)
    resized_rgb = cv2.cvtColor(resized_bgr, cv2.COLOR_BGR2RGB)

    # Master surface (100% exact pixel replica)
    master_surface = pygame.surfarray.make_surface(np.transpose(resized_rgb, (1, 0, 2)))

    # Generate smooth, continuous weaving painterly path
    # Row spacing ensures complete overlapping coverage without any gaps
    step_y = int(brush_radius * 1.15)
    rows = height // step_y + 2
    path_pts = []

    for r in range(rows):
        base_y = int((r + 0.4) * step_y)
        # Alternate left-to-right and right-to-left like an artist's brush
        if r % 2 == 0:
            xs = list(range(-brush_radius, width + brush_radius + 1, 10))
        else:
            xs = list(range(width + brush_radius, -brush_radius - 1, -10))

        for x in xs:
            # Subtle gentle wave for organic brush motion
            w_y = base_y + int(8 * math.sin(x * 0.015))
            w_y = max(0, min(height, w_y))
            path_pts.append((x, w_y))

    # Detect prominent stars and stellar cores
    gray = cv2.cvtColor(resized_bgr, cv2.COLOR_BGR2GRAY)
    _, star_thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(star_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    stars = []
    for c in contours:
        area = cv2.contourArea(c)
        if 2 <= area <= 700:
            M = cv2.moments(c)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                col = tuple(int(v) for v in resized_rgb[cy, cx])
                stars.append({
                    "x": cx,
                    "y": cy,
                    "area": area,
                    "color": col,
                    "phase": random.uniform(0, math.pi * 2),
                })

    stars.sort(key=lambda s: s["area"], reverse=True)

    # Landmark stellar coordinates
    landmarks = {
        "primary_star": (int(width * (315 / 2560)), int(height * (786 / 1280))),
        "upper_gold_star": (int(width * (1692 / 2560)), int(height * (295 / 1280))),
        "cyan_core": (int(width * (654 / 2560)), int(height * (295 / 1280))),
        "horizon_core": (int(width * (1878 / 2560)), int(height * (724 / 1280))),
    }

    return {
        "master_surface": master_surface,
        "path_pts": path_pts,
        "stars": stars,
        "landmarks": landmarks,
        "brush_radius": brush_radius,
    }


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
    """A floating stardust particle with smooth life decay."""

    def __init__(self, x, y, color=None):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-0.4, 0.4)
        self.vy = random.uniform(-0.4, 0.4)
        self.radius = random.uniform(1.2, 2.8)
        self.color = color if color else random.choice([(255, 245, 190), (140, 235, 255), (255, 180, 230)])
        self.life = random.randint(30, 80)
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
    pygame.display.set_caption("🌌 Day 13: Cosmic Universe - Generative Painting | 30 Days Python")

    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    BRUSH_RADIUS = 36
    assets = load_master_and_generate_path(IMAGE_PATH, CANVAS_WIDTH, CANVAS_HEIGHT, brush_radius=BRUSH_RADIUS)
    master_surface = assets["master_surface"]
    path_pts = assets["path_pts"]
    stars = assets["stars"]
    landmarks = assets["landmarks"]

    # Layer surfaces
    paint_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    paint_layer.fill(SPACE_VOID)
    overlay_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)

    # Ambient background stars for a clean, non-empty void
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

    # Painting state
    current_pt_idx = 0
    STEPS_PER_FRAME = 3  # Smooth, deliberate painting speed (~19 seconds total)
    painting_complete = False
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
                    # Reset animation cleanly
                    current_pt_idx = 0
                    painting_complete = False
                    stellar_progress = 0.0
                    paint_layer.fill(SPACE_VOID)
                    for ax, ay, arad, abright in ambient_stars:
                        pygame.draw.circle(paint_layer, (abright, abright, int(abright * 1.1)), (ax, ay), arad)
                    particles.clear()
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
        # DRAWING / PAINTING PIPELINE
        # -------------------------------------------------------------
        current_cursor = None
        if not painting_complete:
            for _ in range(STEPS_PER_FRAME):
                if current_pt_idx >= len(path_pts):
                    painting_complete = True
                    break

                pt = path_pts[current_pt_idx]
                bx, by = pt
                current_cursor = (bx, by)

                # Copy clean, exact patch from master surface onto paint layer
                x1 = max(0, bx - BRUSH_RADIUS)
                y1 = max(0, by - BRUSH_RADIUS)
                x2 = min(CANVAS_WIDTH, bx + BRUSH_RADIUS)
                y2 = min(CANVAS_HEIGHT, by + BRUSH_RADIUS)
                w = x2 - x1
                h = y2 - y1

                if w > 0 and h > 0:
                    patch = master_surface.subsurface(pygame.Rect(x1, y1, w, h))
                    paint_layer.blit(patch, (x1, y1))

                current_pt_idx += 1
        else:
            # Fully lock master surface when complete (100% exact replica)
            paint_layer.blit(master_surface, (0, 0))

        # Clear overlay layer for dynamic lighting, star flares, and HUD
        overlay_layer.fill((0, 0, 0, 0))

        # -------------------------------------------------------------
        # STELLAR IGNITION & DIFFRACTION FLARES
        # -------------------------------------------------------------
        progress_pct = min(1.0, current_pt_idx / len(path_pts))
        if progress_pct >= 0.70:
            if stellar_progress < 1.0:
                stellar_progress = min(1.0, stellar_progress + 0.02)

            num_ignited = int(len(stars) * stellar_progress)
            time_ticks = pygame.time.get_ticks() * 0.003

            # Render stars with gentle organic twinkle
            for i in range(num_ignited):
                s = stars[i]
                twinkle = 1.0 + 0.16 * math.sin(time_ticks + s["phase"])
                r_rad = max(1.0, math.sqrt(s["area"]) * 0.42 * twinkle)

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
        # ACTIVE CELESTIAL STYLUS CURSOR (During Drawing)
        # -------------------------------------------------------------
        if not painting_complete and current_cursor:
            cx, cy = current_cursor
            cx = max(0, min(CANVAS_WIDTH, cx))
            cy = max(0, min(CANVAS_HEIGHT, cy))

            # Glowing multi-layer celestial stylus tip
            pygame.draw.circle(overlay_layer, (255, 255, 255), (cx, cy), 3)
            pygame.draw.circle(overlay_layer, (255, 235, 140, 180), (cx, cy), 10)
            pygame.draw.circle(overlay_layer, (140, 230, 255, 90), (cx, cy), 22)

            if random.random() < 0.45:
                particles.append(StardustParticle(cx, cy))

        # Update and draw stardust particles
        particles = [p for p in particles if p.update()]
        for p in particles:
            p.draw(overlay_layer)

        # -------------------------------------------------------------
        # CLEAN STATUS BAR & CONTROLS HUD
        # -------------------------------------------------------------
        hud_bg = pygame.Surface((CANVAS_WIDTH, 28), pygame.SRCALPHA)
        hud_bg.fill((6, 8, 18, 180))
        overlay_layer.blit(hud_bg, (0, CANVAS_HEIGHT - 28))

        pct = int(progress_pct * 100)
        if pct < 35:
            phase_label = "Drawing Upper Cosmos & Deep Field"
        elif pct < 70:
            phase_label = "Painting Ethereal Nebula & Azure Valley"
        elif pct < 100:
            phase_label = "Sculpting Golden Cosmic Cliffs & Horizon"
        else:
            phase_label = "Masterpiece Completed (Living Cosmos)"

        # Progress bar
        bar_w = int(CANVAS_WIDTH * (pct / 100.0))
        pygame.draw.rect(overlay_layer, (255, 190, 50), (0, CANVAS_HEIGHT - 3, bar_w, 3))

        status_text = f"🌌 COSMIC UNIVERSE  |  Phase: {phase_label} [{pct}%]"
        rendered_status = font_hud.render(status_text, True, (240, 245, 255))
        overlay_layer.blit(rendered_status, (14, CANVAS_HEIGHT - 21))

        controls_text = "[SPACE] Replay  |  [S] Save Screenshot  |  [F] Fullscreen  |  [ESC] Exit"
        rendered_ctrl = font_hud.render(controls_text, True, (180, 200, 225))
        overlay_layer.blit(rendered_ctrl, (CANVAS_WIDTH - rendered_ctrl.get_width() - 14, CANVAS_HEIGHT - 21))

        # Composite everything to screen
        screen.blit(paint_layer, (0, 0))
        screen.blit(overlay_layer, (0, 0))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

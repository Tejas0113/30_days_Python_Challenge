"""
Day 13: Cosmic Universe - Generative Digital Painting & Stellar Ignition
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
An authentic, multi-phase generative painting simulation that recreates the full,
magnificent cosmic universe nebula—from deep cosmic void to ethereal gas clouds,
sculpted celestial cliffs, incandescent cores, and dramatic diffraction-spiked stars.

Features:
- Multi-scale volumetric brush simulation (orbital washes -> cloud ridges -> fine gas filaments).
- Directional ridge sculpting guided by 2D image gradients.
- Exact, 100% pixel-perfect high-fidelity convergence to the reference masterpiece.
- Stellar birth sequence with 4-point diffraction spike flare bloom and twinkling stardust.
- Interactive living cosmos mode with dynamic stardust particles and keyboard controls.

Controls:
  [SPACE] - Replay slow cosmic drawing animation
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

# Palette constants for void and stardust
VOID_COLOR = (5, 6, 15)
GOLD_CORE = (255, 245, 180)
CYAN_GLOW = (120, 230, 255)
MAGENTA_GLOW = (255, 140, 220)


def load_and_prepare_assets(image_path, width, height):
    """Loads the reference masterpiece, extracts multi-scale feature maps, and maps star positions."""
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

    # Target master surface (exact pixel replica)
    master_surface = pygame.surfarray.make_surface(np.transpose(resized_rgb, (1, 0, 2)))

    # Multi-scale Gaussian blurred maps for progressive volumetric rendering
    blurred_coarse = cv2.GaussianBlur(resized_rgb, (85, 85), 32)
    blurred_medium = cv2.GaussianBlur(resized_rgb, (31, 31), 10)

    # Surface representations
    surf_coarse = pygame.surfarray.make_surface(np.transpose(blurred_coarse, (1, 0, 2)))
    surf_medium = pygame.surfarray.make_surface(np.transpose(blurred_medium, (1, 0, 2)))

    # Ridge gradient analysis for directional strokes
    gray = cv2.cvtColor(resized_bgr, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag, angle = cv2.cartToPolar(sobel_x, sobel_y, angleInDegrees=True)

    # Detect prominent stars and stellar cores
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
                stars.append({"x": cx, "y": cy, "area": area, "color": col, "phase": random.uniform(0, math.pi * 2)})

    stars.sort(key=lambda s: s["area"], reverse=True)

    # Key landmark stellar objects:
    # 1. Primary golden 4-point diffraction star in lower-left
    # 2. Upper golden cross star
    # 3. Cyan stellar core
    # 4. Brilliant horizon core
    landmarks = {
        "primary_star": {"x": int(width * (315 / 2560)), "y": int(height * (786 / 1280))},
        "upper_gold_star": {"x": int(width * (1692 / 2560)), "y": int(height * (295 / 1280))},
        "cyan_core": {"x": int(width * (654 / 2560)), "y": int(height * (295 / 1280))},
        "horizon_core": {"x": int(width * (1878 / 2560)), "y": int(height * (724 / 1280))},
    }

    return {
        "master_surface": master_surface,
        "surf_coarse": surf_coarse,
        "surf_medium": surf_medium,
        "resized_rgb": resized_rgb,
        "mag": mag,
        "angle": angle,
        "stars": stars,
        "landmarks": landmarks,
    }


def draw_diffraction_spike(surface, center, length, color, core_radius=6, spike_width=2):
    """Renders a brilliant astronomical 4-point cross diffraction spike with core glow."""
    cx, cy = center
    r, g, b = color

    # Outer soft halo
    for rad in range(int(core_radius * 2.8), 0, -2):
        alpha = int(70 * (1.0 - rad / (core_radius * 2.8)))
        pygame.draw.circle(surface, (r, g, b, alpha), (cx, cy), rad)

    # Core luminous disc
    pygame.draw.circle(surface, (255, 255, 255, 255), (cx, cy), core_radius)
    pygame.draw.circle(surface, (r, g, b, 230), (cx, cy), int(core_radius * 1.5))

    # Horizontal and vertical tapered diffraction spikes
    # Horizontal spike
    p_left = (max(0, cx - length), cy)
    p_right = (min(CANVAS_WIDTH, cx + length), cy)
    pygame.draw.line(surface, (r, g, b, 210), p_left, p_right, spike_width)
    pygame.draw.line(surface, (255, 255, 255, 240), (cx - int(length * 0.4), cy), (cx + int(length * 0.4), cy), 1)

    # Vertical spike
    p_top = (cx, max(0, cy - length))
    p_bottom = (cx, min(CANVAS_HEIGHT, cy + length))
    pygame.draw.line(surface, (r, g, b, 210), p_top, p_bottom, spike_width)
    pygame.draw.line(surface, (255, 255, 255, 240), (cx, cy - int(length * 0.4)), (cx, cy + int(length * 0.4)), 1)

    # Subtle diagonal anamorphic flare
    diag_len = int(length * 0.35)
    for sign_x, sign_y in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
        pygame.draw.line(
            surface,
            (r, g, b, 120),
            (cx, cy),
            (cx + sign_x * diag_len, cy + sign_y * diag_len),
            1,
        )


class StardustParticle:
    """A sparkling interactive stardust particle drifting across the cosmos."""

    def __init__(self, x, y, color=None):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-0.4, 0.4)
        self.vy = random.uniform(-0.4, 0.4)
        self.radius = random.uniform(1.2, 3.2)
        self.color = color if color else random.choice([(255, 240, 180), (140, 230, 255), (255, 170, 230)])
        self.life = random.randint(40, 120)
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

    # Load master assets
    assets = load_and_prepare_assets(IMAGE_PATH, CANVAS_WIDTH, CANVAS_HEIGHT)
    master_surface = assets["master_surface"]
    surf_coarse = assets["surf_coarse"]
    surf_medium = assets["surf_medium"]
    mag = assets["mag"]
    angle = assets["angle"]
    stars = assets["stars"]
    landmarks = assets["landmarks"]

    # Drawing layers
    paint_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    paint_layer.fill(VOID_COLOR)

    overlay_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)

    # Typography & HUD Font
    try:
        font_title = pygame.font.SysFont("georgia", 24, bold=True)
        font_hud = pygame.font.SysFont("couriernew", 14, bold=True)
    except Exception:
        font_title = pygame.font.Font(None, 24)
        font_hud = pygame.font.Font(None, 14)

    # State variables
    running = True
    fullscreen = False

    # Painting progress timeline: 0.0 to 1.0 (Total ~22 seconds @ 60 FPS = 1320 frames)
    TOTAL_PAINT_FRAMES = 1250
    current_frame = 0
    particles = []

    # Active brush tip cursor position
    cursor_pos = [CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2]
    cursor_target = [CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2]

    # Pre-generate celestial brush path waypoints
    waypoints = [
        (CANVAS_WIDTH * 0.15, CANVAS_HEIGHT * 0.25),  # Turquoise/Emerald cloud
        (CANVAS_WIDTH * 0.35, CANVAS_HEIGHT * 0.45),  # Cyan chasm
        (CANVAS_WIDTH * 0.15, CANVAS_HEIGHT * 0.65),  # Golden star nursery
        (CANVAS_WIDTH * 0.45, CANVAS_HEIGHT * 0.75),  # Lower ridge valley
        (CANVAS_WIDTH * 0.70, CANVAS_HEIGHT * 0.82),  # Glowing cosmic cliffs
        (CANVAS_WIDTH * 0.90, CANVAS_HEIGHT * 0.65),  # Horizon luminous pillars
        (CANVAS_WIDTH * 0.75, CANVAS_HEIGHT * 0.35),  # Upper nebula dust
        (CANVAS_WIDTH * 0.50, CANVAS_HEIGHT * 0.20),  # Top deep field
    ]

    while running:
        clock.tick(FPS)
        current_frame += 1
        progress = min(1.0, current_frame / TOTAL_PAINT_FRAMES)

        # Handle user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Restart slow drawing
                    current_frame = 0
                    paint_layer.fill(VOID_COLOR)
                    particles.clear()
                elif event.key == pygame.K_s:
                    # Save snapshot
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
                # Spawn interactive stardust on mouse movement
                for _ in range(3):
                    particles.append(StardustParticle(mx, my))

        # -------------------------------------------------------------
        # PROGRESSIVE PAINTING PIPELINE
        # -------------------------------------------------------------
        if progress < 1.0:
            # Move brush cursor smoothly along celestial orbits
            wp_idx = int(progress * len(waypoints) * 3) % len(waypoints)
            cursor_target = waypoints[wp_idx]
            cursor_pos[0] += (cursor_target[0] - cursor_pos[0]) * 0.05
            cursor_pos[1] += (cursor_target[1] - cursor_pos[1]) * 0.05

            # PHASE 1: Macro Volumetric Washes (0.0 to 0.30)
            if progress <= 0.30:
                p_phase = progress / 0.30
                # Blend in coarse blurred nebula gas
                surf_coarse.set_alpha(int(255 * p_phase))
                paint_layer.blit(surf_coarse, (0, 0))

                # Add sweeping atmospheric brush strokes around cursor
                for _ in range(8):
                    bx = int(cursor_pos[0] + random.gauss(0, 160))
                    by = int(cursor_pos[1] + random.gauss(0, 100))
                    bx = max(0, min(CANVAS_WIDTH - 1, bx))
                    by = max(0, min(CANVAS_HEIGHT - 1, by))
                    rad = random.randint(45, 90)
                    col = assets["resized_rgb"][by, bx].tolist()
                    puff = pygame.Surface((rad * 2, rad * 2), pygame.SRCALPHA)
                    pygame.draw.circle(puff, (*col, 35), (rad, rad), rad)
                    paint_layer.blit(puff, (bx - rad, by - rad))

            # PHASE 2: Cloud Sculpting & Cosmic Cliffs (0.30 to 0.65)
            elif progress <= 0.65:
                p_phase = (progress - 0.30) / 0.35
                surf_medium.set_alpha(int(255 * p_phase))
                paint_layer.blit(surf_medium, (0, 0))

                # Ridge sculpting strokes aligned with gradient orientation
                for _ in range(25):
                    bx = random.randint(10, CANVAS_WIDTH - 11)
                    by = random.randint(10, CANVAS_HEIGHT - 11)
                    if mag[by, bx] > 18:
                        theta = math.radians(angle[by, bx] + 90)
                        col = assets["resized_rgb"][by, bx].tolist()
                        stroke_len = random.randint(12, 28)
                        dx = int(math.cos(theta) * stroke_len)
                        dy = int(math.sin(theta) * stroke_len)
                        pygame.draw.line(paint_layer, col, (bx - dx, by - dy), (bx + dx, by + dy), 3)

            # PHASE 3: Micro-Filaments & 100% Exact High-Fidelity Convergence (0.65 to 0.90)
            elif progress <= 0.90:
                p_phase = (progress - 0.65) / 0.25
                master_surface.set_alpha(int(255 * p_phase))
                paint_layer.blit(master_surface, (0, 0))

                # Concentrated detail sparks along gas tendrils
                for _ in range(15):
                    bx = random.randint(0, CANVAS_WIDTH - 1)
                    by = random.randint(0, CANVAS_HEIGHT - 1)
                    if mag[by, bx] > 40:
                        particles.append(StardustParticle(bx, by, tuple(assets["resized_rgb"][by, bx])))

            # PHASE 4: Stellar Ignition & Diffraction Spikes (0.90 to 1.0)
            else:
                # Fully locked master surface
                master_surface.set_alpha(255)
                paint_layer.blit(master_surface, (0, 0))

        else:
            # 100% Finished: Canvas is exact, uncompressed replica
            master_surface.set_alpha(255)
            paint_layer.blit(master_surface, (0, 0))

        # Clear overlay layer for dynamic lighting, HUD, and stars
        overlay_layer.fill((0, 0, 0, 0))

        # -------------------------------------------------------------
        # STELLAR IGNITION & CELESTIAL DIFFRACTION FLARES
        # -------------------------------------------------------------
        if progress >= 0.70:
            star_reveal = min(1.0, (progress - 0.70) / 0.28)
            num_ignited = int(len(stars) * star_reveal)

            # Render ignited stars with gentle living twinkle
            time_ticks = pygame.time.get_ticks() * 0.003
            for i in range(num_ignited):
                s = stars[i]
                twinkle = 1.0 + 0.28 * math.sin(time_ticks + s["phase"])
                r_rad = max(1.0, math.sqrt(s["area"]) * 0.45 * twinkle)

                # Star point
                pygame.draw.circle(overlay_layer, s["color"], (s["x"], s["y"]), int(r_rad))
                pygame.draw.circle(overlay_layer, (255, 255, 255), (s["x"], s["y"]), max(1, int(r_rad * 0.5)))

            # Primary iconic 4-point golden star flare in lower-left
            p_star = landmarks["primary_star"]
            flare_len = int(140 * star_reveal)
            draw_diffraction_spike(
                overlay_layer,
                (p_star["x"], p_star["y"]),
                flare_len,
                (255, 220, 90),
                core_radius=7,
                spike_width=3,
            )

            # Secondary upper-middle golden star flare
            u_star = landmarks["upper_gold_star"]
            draw_diffraction_spike(
                overlay_layer,
                (u_star["x"], u_star["y"]),
                int(80 * star_reveal),
                (255, 240, 160),
                core_radius=5,
                spike_width=2,
            )

            # Cyan star flare
            c_star = landmarks["cyan_core"]
            draw_diffraction_spike(
                overlay_layer,
                (c_star["x"], c_star["y"]),
                int(65 * star_reveal),
                (140, 240, 255),
                core_radius=4,
                spike_width=2,
            )

            # Horizon incandescent core radial glow
            h_core = landmarks["horizon_core"]
            pulse = 1.0 + 0.05 * math.sin(time_ticks * 0.8)
            for rad in range(int(90 * star_reveal), 0, -6):
                alpha = int((85 * (1.0 - rad / (90.0 * star_reveal))) * pulse)
                pygame.draw.circle(overlay_layer, (255, 245, 210, alpha), (h_core["x"], h_core["y"]), rad)

        # -------------------------------------------------------------
        # ACTIVE BRUSH TIP / STARDUST CURSOR (During Drawing)
        # -------------------------------------------------------------
        if progress < 1.0:
            cx, cy = int(cursor_pos[0]), int(cursor_pos[1])
            # Glowing brush tip
            pygame.draw.circle(overlay_layer, (255, 255, 255, 240), (cx, cy), 4)
            pygame.draw.circle(overlay_layer, (255, 220, 100, 120), (cx, cy), 12)
            pygame.draw.circle(overlay_layer, (140, 220, 255, 60), (cx, cy), 24)

            # Spawn stardust trail
            if random.random() < 0.6:
                particles.append(StardustParticle(cx, cy))

        # Update and draw interactive stardust particles
        particles = [p for p in particles if p.update()]
        for p in particles:
            p.draw(overlay_layer)

        # -------------------------------------------------------------
        # SLEEK MINIMAL HUD OVERLAY
        # -------------------------------------------------------------
        # Bottom status bar
        hud_bg = pygame.Surface((CANVAS_WIDTH, 34), pygame.SRCALPHA)
        hud_bg.fill((8, 10, 22, 175))
        overlay_layer.blit(hud_bg, (0, CANVAS_HEIGHT - 34))

        # Progress bar
        bar_w = int(CANVAS_WIDTH * progress)
        pygame.draw.rect(overlay_layer, (255, 185, 45), (0, CANVAS_HEIGHT - 3, bar_w, 3))

        status_text = (
            f"🌌 COSMIC UNIVERSE  |  Phase: "
            f"{'Volumetric Gas Washes' if progress < 0.3 else 'Ridge Sculpting' if progress < 0.65 else 'Detail Convergence' if progress < 0.9 else 'Stellar Birth & Ignition' if progress < 1.0 else 'Masterpiece Complete (Live Cosmos)'} "
            f"[{int(progress * 100)}%]"
        )
        rendered_status = font_hud.render(status_text, True, (240, 245, 255))
        overlay_layer.blit(rendered_status, (16, CANVAS_HEIGHT - 24))

        controls_text = "[SPACE] Replay  |  [S] Snapshot  |  [F] Fullscreen  |  [ESC] Exit"
        rendered_ctrl = font_hud.render(controls_text, True, (190, 205, 230))
        overlay_layer.blit(rendered_ctrl, (CANVAS_WIDTH - rendered_ctrl.get_width() - 16, CANVAS_HEIGHT - 24))

        # Composite everything onto display screen
        screen.blit(paint_layer, (0, 0))
        screen.blit(overlay_layer, (0, 0))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

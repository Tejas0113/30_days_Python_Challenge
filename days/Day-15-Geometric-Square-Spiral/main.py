"""
Day 15: Geometric Square Spiral Vortex Art - Generative Kinetic Neon Engine
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A mesmerizing, high-performance generative kinetic artwork elevating the classic
91-degree expanding square spiral into a glowing multi-layered neon vortex:
1. Core Mathematical Concept:
   - Based on expanding polygonal spiral geometry: length increments by step L_k = L_0 + k * step.
   - Turning by exactly 91.0° (90° + 1.0° precession) generates a magnificent 4-arm rotating
     vortex tunnel where each side precesses by 1° on every turn.
2. Next-Level Generative Artistry:
   - Multi-Pass Neon Bloom: Outer ambient halo, mid neon glow, and high-intensity laser spine.
   - Harmonic Breathing Precession: Smooth sinusoidal oscillation of the turn angle
     (theta(t) = 91.0° + A * sin(omega * t)), causing the 4 arms to coil, twist, and breathe.
   - Dual Counter-Rotating Harmonics: Interlocking primary and secondary spirals spinning
     in opposite directions for deep kinetic dimensionality.
   - Centrifugal Stardust Aura: Luminescent particles drifting outward along the spiral arms.
3. Dynamic Chromatic Themes:
   - Cyberpunk Neon (Electric Cyan, Hot Magenta, Laser Violet, Solar Gold)
   - Spectral Rainbow (Continuous silky HSV chromatic gradient)
   - Solar Flare (Crimson, Molten Orange, Solar Gold, Incandescent White)
   - Cosmic Aurora (Emerald, Celestial Turquoise, Mystic Violet, Starlight White)
   - Monochromatic Silver (Platinum, Mercury Silver, Diamond White)

Controls:
  [SPACE]      - Pause / Resume rotation
  [C]          - Cycle Chromatic Color Themes
  [B]          - Toggle Harmonic Breathing Angle (On / Off)
  [M]          - Cycle Spiral Modes (Classic 91°, Dual Counter-Rotating, Pulsing Tesseract)
  [LEFT/RIGHT] - Interactively adjust turn angle (89.0° - 94.0° by 0.1°)
  [UP/DOWN]    - Adjust rotation speed
  [R]          - Reset angle to classic 91.0°
  [S]          - Save high-resolution screenshot
  [F]          - Toggle fullscreen mode
  [ESC/Q]      - Exit application
"""

import colorsys
import math
import os
import random
import sys
import numpy as np
import pygame

# 1. Canvas & Visual Constants
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 800
FPS = 60

# Palette Constants
VOID_BG = (7, 9, 16)

# Chromatic Color Themes
THEMES = [
    {
        "name": "Cyberpunk Neon",
        "colors": [
            (0, 240, 255),    # Electric Cyan
            (255, 20, 147),   # Deep Pink / Neon Magenta
            (160, 32, 255),   # Laser Violet
            (255, 215, 0),    # Solar Gold
            (0, 255, 180),    # Neon Mint
        ],
        "bg": (6, 8, 15),
    },
    {
        "name": "Spectral Rainbow",
        "mode": "hsv",
        "bg": (5, 6, 12),
    },
    {
        "name": "Solar Flare",
        "colors": [
            (220, 20, 60),    # Crimson
            (255, 90, 0),     # Molten Orange
            (255, 190, 20),   # Solar Gold
            (255, 245, 180),  # Incandescent White
            (255, 130, 40),   # Radiant Amber
        ],
        "bg": (12, 6, 8),
    },
    {
        "name": "Cosmic Aurora",
        "colors": [
            (0, 230, 180),    # Celestial Turquoise
            (40, 255, 120),   # Emerald Aurora
            (130, 40, 255),   # Mystic Violet
            (220, 245, 255),  # Starlight White
            (20, 160, 255),   # Azure Blue
        ],
        "bg": (5, 10, 14),
    },
    {
        "name": "Monochrome Silver",
        "colors": [
            (255, 255, 255),  # Pure Diamond White
            (200, 210, 225),  # Platinum
            (150, 160, 175),  # Mercury Silver
            (110, 120, 135),  # Slate Silver
            (240, 245, 255),  # Highlight Silver
        ],
        "bg": (8, 9, 12),
    },
]


class StardustParticle:
    """A floating luminescent particle drifting outward from the vortex core."""

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.6, 2.4)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.x = cx + self.vx * random.uniform(5, 40)
        self.y = cy + self.vy * random.uniform(5, 40)
        self.life = random.randint(40, 100)
        self.max_life = self.life
        self.radius = random.uniform(1.0, 2.2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 1.01  # Centrifugal acceleration
        self.vy *= 1.01
        self.life -= 1
        return self.life > 0

    def draw(self, surface, color):
        if self.life <= 0:
            return
        alpha = int(220 * (self.life / self.max_life))
        r, g, b = color[:3]
        pygame.draw.circle(surface, (r, g, b, alpha), (int(self.x), int(self.y)), int(self.radius))


def get_segment_color(index, total_segments, theme, time_phase=0.0):
    """Calculates smooth chromatic gradient color for a spiral segment."""
    if theme.get("mode") == "hsv":
        # Continuous spectral rainbow flow
        hue = (index / float(total_segments) * 2.2 + time_phase * 0.08) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 0.95, 1.0)
        return int(r * 255), int(g * 255), int(b * 255)
    else:
        # Multi-stop linear palette interpolation
        palette = theme["colors"]
        n_stops = len(palette)
        t = ((index / float(total_segments)) * (n_stops - 1) + time_phase * 0.4) % (n_stops - 1)
        idx = int(t)
        frac = t - idx
        c1 = palette[idx]
        c2 = palette[(idx + 1) % n_stops]
        r = int(c1[0] + (c2[0] - c1[0]) * frac)
        g = int(c1[1] + (c2[1] - c1[1]) * frac)
        b = int(c1[2] + (c2[2] - c1[2]) * frac)
        return r, g, b


def generate_square_spiral_points(cx, cy, base_angle, turn_angle_deg, num_steps=360, length_scale=1.0):
    """
    Computes exact vertex coordinates for an expanding polygonal square spiral.
    length(k) = (4.0 + k * 1.35) * length_scale
    angle(k)  = base_angle - k * turn_angle
    """
    theta_rad = math.radians(turn_angle_deg)
    points = [(cx, cy)]
    x, y = float(cx), float(cy)
    angle = base_angle

    for k in range(num_steps):
        seg_len = (4.0 + k * 1.35) * length_scale
        x += seg_len * math.cos(angle)
        y += seg_len * math.sin(angle)
        points.append((x, y))
        angle -= theta_rad

    return points


def render_neon_spiral(screen, glow_layer, points, theme, time_phase, alpha_mult=1.0, width_mult=1.0):
    """Renders multi-pass glowing neon bloom for spiral segments."""
    n_pts = len(points)
    for k in range(n_pts - 1):
        p1 = points[k]
        p2 = points[k + 1]

        # Cull offscreen segments
        if (p1[0] < -50 and p2[0] < -50) or (p1[0] > CANVAS_WIDTH + 50 and p2[0] > CANVAS_WIDTH + 50) or \
           (p1[1] < -50 and p2[1] < -50) or (p1[1] > CANVAS_HEIGHT + 50 and p2[1] > CANVAS_HEIGHT + 50):
            continue

        r, g, b = get_segment_color(k, n_pts, theme, time_phase)

        # 1. Outer Diffuse Bloom Halo (Width 6-8 px, soft alpha)
        halo_alpha = int(45 * alpha_mult)
        if halo_alpha > 2:
            pygame.draw.line(glow_layer, (r, g, b, halo_alpha), p1, p2, int(6 * width_mult))

        # 2. Mid Vibrant Neon Corona (Width 2-3 px, saturated alpha)
        mid_alpha = int(145 * alpha_mult)
        if mid_alpha > 2:
            pygame.draw.line(glow_layer, (r, g, b, mid_alpha), p1, p2, max(2, int(2.5 * width_mult)))

        # 3. High-Intensity Core Laser Spine
        core_r = min(255, int(r * 0.75 + 255 * 0.25))
        core_g = min(255, int(g * 0.75 + 255 * 0.25))
        core_b = min(255, int(b * 0.75 + 255 * 0.25))
        pygame.draw.line(screen, (core_r, core_g, core_b), p1, p2, 1)


def main():
    # 2. Setup Pygame
    pygame.init()
    pygame.display.set_caption("🌀 Day 15: Geometric Square Spiral Vortex Art | 30 Days Python")

    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Dedicated transparent surface for multi-pass neon bloom blending
    glow_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)

    # HUD Font
    try:
        font_hud = pygame.font.SysFont("couriernew", 13, bold=True)
    except Exception:
        font_hud = pygame.font.Font(None, 14)

    running = True
    fullscreen = False
    is_paused = False
    breathing_enabled = True

    # Geometry & Kinetic States
    current_angle_deg = 91.0       # The classic 91.0° square spiral angle
    target_angle_deg = 91.0
    rotation_angle = 0.0           # Global continuous spinning angle
    rotation_speed = 0.012         # Rotation speed in radians/frame (~0.7° per frame)
    NUM_SEGMENTS = 360             # Number of expanding spiral segments

    theme_idx = 0                  # Default: Cyberpunk Neon
    mode_idx = 0                   # 0: Classic 91°, 1: Dual Counter-Rotating, 2: Breathing Tesseract
    MODES = ["Single Neon Vortex", "Dual Counter-Rotating", "Breathing Tesseract"]

    particles = []
    time_phase = 0.0

    while running:
        clock.tick(FPS)
        current_theme = THEMES[theme_idx]

        # Handle user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                elif event.key == pygame.K_c:
                    theme_idx = (theme_idx + 1) % len(THEMES)
                elif event.key == pygame.K_b:
                    breathing_enabled = not breathing_enabled
                elif event.key == pygame.K_m:
                    mode_idx = (mode_idx + 1) % len(MODES)
                elif event.key == pygame.K_LEFT:
                    target_angle_deg = max(88.0, target_angle_deg - 0.1)
                elif event.key == pygame.K_RIGHT:
                    target_angle_deg = min(95.0, target_angle_deg + 0.1)
                elif event.key in (pygame.K_UP, pygame.K_PLUS, pygame.K_EQUALS):
                    rotation_speed = min(0.06, rotation_speed + 0.003)
                elif event.key in (pygame.K_DOWN, pygame.K_MINUS):
                    rotation_speed = max(0.001, rotation_speed - 0.003)
                elif event.key == pygame.K_r:
                    target_angle_deg = 91.0
                    rotation_speed = 0.012
                elif event.key == pygame.K_s:
                    snap_name = f"square_spiral_{THEMES[theme_idx]['name'].lower().replace(' ', '_')}.png"
                    pygame.image.save(screen, snap_name)
                    print(f"Saved screenshot: {snap_name}")
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)

        # -------------------------------------------------------------
        # KINETIC & MATHEMATICAL UPDATE
        # -------------------------------------------------------------
        if not is_paused:
            rotation_angle += rotation_speed
            time_phase += 1.0

        # Smooth interpolation to target turn angle
        current_angle_deg += (target_angle_deg - current_angle_deg) * 0.1

        # Calculate effective turn angle with optional harmonic breathing
        time_s = pygame.time.get_ticks() * 0.001
        effective_angle = current_angle_deg
        if breathing_enabled:
            # Subtle sinusoidal oscillation (±0.65°) producing breathing tesseract motion
            breath_amplitude = 0.65 if mode_idx == 2 else 0.40
            effective_angle += breath_amplitude * math.sin(time_s * 1.2)

        cx, cy = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2

        # Spawn drifting stardust particles from core
        if random.random() < 0.45:
            particles.append(StardustParticle(cx, cy))

        # -------------------------------------------------------------
        # RENDER GENERATIVE ARTWORK
        # -------------------------------------------------------------
        # 1. Clear background with deep void tone
        screen.fill(current_theme["bg"])
        glow_layer.fill((0, 0, 0, 0))

        # 2. Render Secondary Counter-Rotating Spiral (for Dual Modes)
        if mode_idx in (1, 2):
            dual_pts = generate_square_spiral_points(
                cx, cy,
                base_angle=-rotation_angle * 0.85,
                turn_angle_deg=180.0 - effective_angle,
                num_steps=int(NUM_SEGMENTS * 0.82),
                length_scale=0.92,
            )
            render_neon_spiral(screen, glow_layer, dual_pts, current_theme, -time_phase * 0.8, alpha_mult=0.55, width_mult=0.8)

        # 3. Render Primary Expanding Square Spiral Vortex (The 91° Core Masterpiece)
        primary_pts = generate_square_spiral_points(
            cx, cy,
            base_angle=rotation_angle,
            turn_angle_deg=effective_angle,
            num_steps=NUM_SEGMENTS,
            length_scale=1.0,
        )
        render_neon_spiral(screen, glow_layer, primary_pts, current_theme, time_phase, alpha_mult=1.0, width_mult=1.0)

        # 4. Central Radiant Core Jewel (Glowing geometric center star)
        pulse = 1.0 + 0.15 * math.sin(time_s * 3.0)
        c_rgb = get_segment_color(0, NUM_SEGMENTS, current_theme, time_phase)
        pygame.draw.circle(glow_layer, (*c_rgb, 90), (cx, cy), int(16 * pulse))
        pygame.draw.circle(glow_layer, (*c_rgb, 180), (cx, cy), int(8 * pulse))
        pygame.draw.circle(screen, (255, 255, 255), (cx, cy), max(2, int(4 * pulse)))

        # 5. Update & Render Stardust Particles
        particles = [p for p in particles if p.update()]
        for p in particles:
            p.draw(glow_layer, c_rgb)

        # 6. Composite Multi-Pass Bloom Layer to Screen
        screen.blit(glow_layer, (0, 0))

        # 7. Minimalist High-Tech HUD Status Bar
        hud_bg = pygame.Surface((CANVAS_WIDTH, 26), pygame.SRCALPHA)
        hud_bg.fill((6, 8, 16, 205))
        screen.blit(hud_bg, (0, CANVAS_HEIGHT - 26))

        mode_name = MODES[mode_idx]
        theme_name = current_theme["name"]
        breath_str = "ON" if breathing_enabled else "OFF"
        pause_str = "PAUSED | " if is_paused else ""

        status_text = (
            f"🌀 SQUARE SPIRAL | {pause_str}Angle: {effective_angle:.1f}° (Target: {target_angle_deg:.1f}°) | "
            f"Mode: {mode_name} | Theme: {theme_name} | Breath: {breath_str}"
        )
        rendered_status = font_hud.render(status_text, True, (240, 245, 255))
        screen.blit(rendered_status, (14, CANVAS_HEIGHT - 19))

        controls_text = "[SPACE] Pause | [C] Theme | [B] Breath | [M] Mode | [LEFT/RIGHT] Angle | [S] Snap"
        rendered_ctrl = font_hud.render(controls_text, True, (160, 180, 210))
        screen.blit(rendered_ctrl, (CANVAS_WIDTH - rendered_ctrl.get_width() - 14, CANVAS_HEIGHT - 19))

        # Bottom neon progress accent line matching current theme
        pygame.draw.line(screen, c_rgb, (0, CANVAS_HEIGHT - 1), (CANVAS_WIDTH, CANVAS_HEIGHT - 1), 1)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

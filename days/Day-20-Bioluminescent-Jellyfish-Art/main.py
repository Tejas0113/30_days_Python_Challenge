"""
Day 20: Bioluminescent Deep-Sea Jellyfish Generative Art
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A peaceful, breathtaking generative art simulation of deep-sea bioluminescence,
procedural hydrodynamics, and organic marine life.

Features:
1. Procedural Jellyfish Anatomy & Hydrodynamics:
   - Translucent pulsating bell (bell dome deformed with harmonic contraction waves)
   - Multi-segment Verlet-integrated trailing tentacles with hydrodynamic fluid drag
   - Frilled inner oral arms with glowing bioluminescent margin rims
   - Rhythmic pulsating bioluminescent organ core (rhopalia & gonadal rings)
2. Ambient Deep-Sea Ecosystem:
   - 350+ drifting bioluminescent marine snow / phytoplankton particles
   - Water current vector field with mouse turbulence and hydrodynamic ripple shockwaves
3. Interactive Features:
   - Click anywhere to spawn hydrodynamic shockwaves that push tentacles and marine snow
   - [Left Click + Drag] to generate water currents that guide the floating jellyfish
   - 6 bioluminescent chromatic palettes (Azure, Emerald, Crimson, Ultraviolet, Gold, Moon Pearl)
   - Real-time particle glow bloom, stardust trails, and telemetry HUD

Controls:
  [SPACE]     - Pause / Resume oceanic simulation
  [Left Click]- Create hydrodynamic shockwave / ripple
  [T]         - Cycle Bioluminescent Color Themes
  [+] / [UP]  - Spawn an additional floating jellyfish
  [-] / [DOWN]- Remove a jellyfish
  [G]         - Toggle Luminous Glow Bloom
  [C]         - Spawn celebratory multi-specimen bloom
  [H]         - Toggle Telemetry HUD
  [P]         - Save high-resolution PNG screenshot to output/
  [ESC] / [Q] - Exit application
"""

import math
import os
import random
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
# 1. CONFIGURATION & CHROMATIC PALETTES
# ==============================================================================
WINDOW_WIDTH = 920
WINDOW_HEIGHT = 920
FPS = 60

THEMES = [
    {
        "name": "Abyssal Azure",
        "bg_top": (4, 8, 18),
        "bg_bot": (2, 4, 10),
        "bell": (40, 195, 255),
        "organ": (120, 240, 255),
        "tentacles": (30, 150, 240),
        "snow": (140, 220, 255),
        "glow": (20, 100, 200),
    },
    {
        "name": "Emerald Phantasm",
        "bg_top": (3, 16, 12),
        "bg_bot": (2, 8, 6),
        "bell": (55, 245, 175),
        "organ": (160, 255, 210),
        "tentacles": (35, 195, 140),
        "snow": (150, 250, 200),
        "glow": (25, 140, 95),
    },
    {
        "name": "Crimson Siren",
        "bg_top": (18, 5, 8),
        "bg_bot": (8, 2, 4),
        "bell": (255, 65, 95),
        "organ": (255, 180, 140),
        "tentacles": (220, 45, 75),
        "snow": (255, 160, 170),
        "glow": (180, 25, 45),
    },
    {
        "name": "Neon Ultraviolet",
        "bg_top": (14, 5, 20),
        "bg_bot": (6, 2, 10),
        "bell": (215, 65, 255),
        "organ": (255, 185, 255),
        "tentacles": (175, 45, 235),
        "snow": (225, 165, 255),
        "glow": (145, 25, 195),
    },
    {
        "name": "Golden Sunburst",
        "bg_top": (18, 14, 4),
        "bg_bot": (8, 6, 2),
        "bell": (255, 195, 55),
        "organ": (255, 245, 160),
        "tentacles": (230, 155, 35),
        "snow": (255, 230, 140),
        "glow": (195, 125, 20),
    },
    {
        "name": "Ghostly Moon Pearl",
        "bg_top": (8, 12, 16),
        "bg_bot": (4, 6, 8),
        "bell": (230, 245, 255),
        "organ": (255, 255, 255),
        "tentacles": (175, 210, 235),
        "snow": (210, 235, 250),
        "glow": (110, 150, 190),
    },
]


# ==============================================================================
# 2. HYDRODYNAMIC TENTACLE & BEZIER BELL MODEL
# ==============================================================================
class Tentacle:
    """Verlet-integrated multi-segment spring chain with hydrodynamic drag."""

    def __init__(self, start_x, start_y, length=24, seg_len=7.0):
        self.num_segs = length
        self.seg_len = seg_len
        self.points = [[start_x, start_y + i * seg_len] for i in range(self.num_segs)]
        self.prev_points = [[p[0], p[1]] for p in self.points]

    def update(self, anchor_x, anchor_y, current_vx=0.0, current_vy=0.0):
        # Anchor top to bell margin
        self.points[0] = [anchor_x, anchor_y]

        # Verlet integration + hydrodynamic water resistance
        for i in range(1, self.num_segs):
            x, y = self.points[i]
            px, py = self.prev_points[i]

            # Inertia velocity with dampening
            vx = (x - px) * 0.91 + current_vx * 0.25
            vy = (y - py) * 0.91 + 0.18 + current_vy * 0.25  # gentle downward buoyancy

            self.prev_points[i] = [x, y]
            self.points[i] = [x + vx, y + vy]

        # Distance constraint relaxation (2 passes)
        for _ in range(2):
            for i in range(self.num_segs - 1):
                p1 = self.points[i]
                p2 = self.points[i + 1]
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                dist = math.hypot(dx, dy)
                if dist > 0.001:
                    diff = (dist - self.seg_len) / dist
                    if i == 0:
                        p2[0] -= dx * diff
                        p2[1] -= dy * diff
                    else:
                        p1[0] += dx * diff * 0.5
                        p1[1] += dy * diff * 0.5
                        p2[0] -= dx * diff * 0.5
                        p2[1] -= dy * diff * 0.5


class Jellyfish:
    """Procedural deep-sea organism with contracting bell and glowing anatomy."""

    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.base_scale = scale
        self.vx = random.uniform(-0.4, 0.4)
        self.vy = random.uniform(-0.6, -0.2)

        # Pulse animation state
        self.phase = random.uniform(0, 2 * math.pi)
        self.pulse_speed = random.uniform(1.6, 2.2)

        # Bell dimensions
        self.radius = 42.0 * self.base_scale
        self.height = 36.0 * self.base_scale

        # Create tentacles along bell rim
        self.num_tentacles = 10
        self.tentacles = []
        for i in range(self.num_tentacles):
            t_len = random.randint(18, 30)
            self.tentacles.append(Tentacle(self.x, self.y, length=t_len, seg_len=7.0 * scale))

        # Create central frilled oral arms
        self.num_arms = 4
        self.oral_arms = [
            Tentacle(self.x, self.y, length=random.randint(14, 22), seg_len=6.0 * scale)
            for _ in range(self.num_arms)
        ]

    def update(self, dt, shockwaves):
        self.phase += dt * self.pulse_speed
        # Asymmetric pulse wave: quick contraction, slow elastic expansion
        pulse_raw = math.sin(self.phase)
        # Power pulse for natural locomotion
        if pulse_raw > 0:
            pulse = math.pow(pulse_raw, 1.8)
            # Upward propulsion thrust during contraction
            thrust = 0.55 * pulse * self.base_scale
            self.vy -= thrust * 0.08
        else:
            pulse = -math.pow(-pulse_raw, 0.8) * 0.5

        # Ambient drag and buoyancy
        self.vx *= 0.985
        self.vy = self.vy * 0.985 + 0.03  # gentle sink between pulses

        # Apply external shockwaves
        for sw in shockwaves:
            dx = self.x - sw["x"]
            dy = self.y - sw["y"]
            dist = math.hypot(dx, dy)
            if dist > 1.0 and dist < sw["radius"] + 80:
                force = (1.0 - dist / (sw["radius"] + 80)) * 6.0
                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force

        self.x += self.vx
        self.y += self.vy

        # Screen wrap / bounce boundaries
        margin = 80
        if self.x < -margin:
            self.x = WINDOW_WIDTH + margin
        elif self.x > WINDOW_WIDTH + margin:
            self.x = -margin
        if self.y < -margin:
            self.y = WINDOW_HEIGHT + margin
        elif self.y > WINDOW_HEIGHT + margin:
            self.y = -margin

        # Dynamic deformed bell width and height
        cur_w = self.radius * (1.0 - 0.22 * pulse)
        cur_h = self.height * (1.0 + 0.35 * pulse)

        # Update tentacles anchored along bell rim
        for i, ten in enumerate(self.tentacles):
            t_ratio = i / float(self.num_tentacles - 1)
            # Elliptical arc along bell bottom rim
            angle = math.pi * (0.08 + 0.84 * t_ratio)
            rim_x = self.x + cur_w * math.cos(angle)
            rim_y = self.y + cur_h * 0.25 + 6.0 * math.sin(angle)
            ten.update(rim_x, rim_y, self.vx * 0.6, self.vy * 0.6)

        # Update central oral arms
        for i, arm in enumerate(self.oral_arms):
            offset_x = (i - 1.5) * (cur_w * 0.22)
            arm.update(self.x + offset_x, self.y + cur_h * 0.2, self.vx * 0.8, self.vy * 0.8)

    def draw(self, surface, theme, bloom=True):
        cur_pulse = math.sin(self.phase)
        cur_w = self.radius * (1.0 - 0.22 * cur_pulse)
        cur_h = self.height * (1.0 + 0.35 * cur_pulse)

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        c_bell = theme["bell"]
        c_org = theme["organ"]
        c_tent = theme["tentacles"]
        c_glow = theme["glow"]

        # 1. Outer luminous aura
        if bloom:
            glow_r = int(cur_w * 1.5)
            pygame.draw.circle(
                overlay,
                (c_glow[0], c_glow[1], c_glow[2], 26),
                (int(self.x), int(self.y)),
                glow_r,
            )

        # 2. Draw outer tentacles
        for ten in self.tentacles:
            pts = [(int(p[0]), int(p[1])) for p in ten.points]
            if len(pts) >= 2:
                # Translucent flowing line
                pygame.draw.lines(overlay, (c_tent[0], c_tent[1], c_tent[2], 65), False, pts, 1)

        # 3. Draw frilled oral arms
        for arm in self.oral_arms:
            pts = [(int(p[0]), int(p[1])) for p in arm.points]
            if len(pts) >= 2:
                pygame.draw.lines(overlay, (c_org[0], c_org[1], c_org[2], 110), False, pts, 2)

        # 4. Translucent pulsating bell dome (Bezier-like polygon)
        num_pts = 32
        bell_pts = []
        for i in range(num_pts + 1):
            theta = math.pi * (i / float(num_pts))
            bx = self.x - cur_w * math.cos(theta)
            # Upper dome curve
            by = self.y - cur_h * math.sin(theta)
            bell_pts.append((bx, by))

        # Bottom scalloped rim
        scallop_pts = []
        for i in range(num_pts, -1, -1):
            theta = math.pi * (i / float(num_pts))
            bx = self.x - cur_w * math.cos(theta)
            # Undulating scallop edge
            scallop = 3.5 * math.sin(theta * 10.0 + self.phase * 2.0)
            by = self.y + cur_h * 0.18 + scallop
            scallop_pts.append((bx, by))

        full_bell = bell_pts + scallop_pts
        if len(full_bell) >= 6:
            # Translucent fill
            pygame.draw.polygon(overlay, (c_bell[0], c_bell[1], c_bell[2], 55), full_bell)
            # Glowing rim outline
            pygame.draw.lines(overlay, (c_bell[0], c_bell[1], c_bell[2], 180), True, full_bell, 2)

        # 5. Internal glowing organ core (rhopalia & gonadal rings)
        organ_pulse = 0.5 + 0.5 * math.sin(self.phase * 2.0)
        org_alpha = int(140 + 95 * organ_pulse)
        org_r = int(cur_w * 0.38)

        # 4 cloverleaf gonads
        for k in range(4):
            ang = k * (math.pi / 2.0) + self.phase * 0.15
            gx = self.x + (cur_w * 0.22) * math.cos(ang)
            gy = self.y - (cur_h * 0.32) + (cur_h * 0.15) * math.sin(ang)
            pygame.draw.circle(
                overlay,
                (c_org[0], c_org[1], c_org[2], org_alpha),
                (int(gx), int(gy)),
                int(org_r * 0.45),
            )

        # Central luminous apex
        pygame.draw.circle(
            overlay,
            (c_org[0], c_org[1], c_org[2], int(org_alpha * 0.8)),
            (int(self.x), int(self.y - cur_h * 0.3)),
            int(org_r * 0.65),
        )

        surface.blit(overlay, (0, 0))


# ==============================================================================
# 3. BIOLUMINESCENT PHYTOPLANKTON & SHOCKWAVE SYSTEM
# ==============================================================================
class DeepSeaEnvironment:
    """Simulates drifting marine snow, phytoplankton, and hydrodynamic shockwaves."""

    def __init__(self, num_particles=380):
        self.num_particles = num_particles
        self.particles = []
        for _ in range(num_particles):
            self.particles.append(
                {
                    "x": random.uniform(0, WINDOW_WIDTH),
                    "y": random.uniform(0, WINDOW_HEIGHT),
                    "vx": random.uniform(-0.25, 0.25),
                    "vy": random.uniform(-0.15, 0.35),
                    "size": random.uniform(1.0, 2.6),
                    "phase": random.uniform(0, 2 * math.pi),
                    "blink_speed": random.uniform(1.2, 3.2),
                }
            )
        self.shockwaves = []

    def add_shockwave(self, x, y):
        self.shockwaves.append({"x": x, "y": y, "radius": 4.0, "life": 1.0, "max_radius": 180.0})

    def update(self, dt):
        # Update particles
        for p in self.particles:
            p["phase"] += dt * p["blink_speed"]
            p["x"] += p["vx"] + 0.15 * math.sin(p["phase"] * 0.5)
            p["y"] += p["vy"]

            # Screen wrap
            if p["x"] < 0:
                p["x"] = WINDOW_WIDTH
            elif p["x"] > WINDOW_WIDTH:
                p["x"] = 0
            if p["y"] < 0:
                p["y"] = WINDOW_HEIGHT
            elif p["y"] > WINDOW_HEIGHT:
                p["y"] = 0

            # React to shockwaves
            for sw in self.shockwaves:
                dx = p["x"] - sw["x"]
                dy = p["y"] - sw["y"]
                dist = math.hypot(dx, dy)
                if 1.0 < dist < sw["radius"] + 40:
                    force = (1.0 - dist / (sw["radius"] + 40)) * 3.5
                    p["x"] += (dx / dist) * force
                    p["y"] += (dy / dist) * force

        # Update shockwaves
        active_sw = []
        for sw in self.shockwaves:
            sw["radius"] += dt * 260.0
            sw["life"] = max(0.0, 1.0 - (sw["radius"] / sw["max_radius"]))
            if sw["life"] > 0:
                active_sw.append(sw)
        self.shockwaves = active_sw

    def draw(self, surface, theme):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        c_snow = theme["snow"]

        # Draw marine snow
        for p in self.particles:
            alpha_pulse = 0.4 + 0.6 * math.sin(p["phase"])
            alpha = int(np.clip(180 * alpha_pulse, 35, 230))
            pygame.draw.circle(
                overlay,
                (c_snow[0], c_snow[1], c_snow[2], alpha),
                (int(p["x"]), int(p["y"])),
                int(p["size"]),
            )

        # Draw shockwave ripples
        for sw in self.shockwaves:
            alpha = int(sw["life"] * 140)
            pygame.draw.circle(
                overlay,
                (c_snow[0], c_snow[1], c_snow[2], alpha),
                (int(sw["x"]), int(sw["y"])),
                int(sw["radius"]),
                2,
            )

        surface.blit(overlay, (0, 0))


# ==============================================================================
# 4. MAIN APPLICATION ENGINE
# ==============================================================================
def draw_gradient_background(surface, top_color, bot_color):
    """Draws vertical abyssal water gradient."""
    h = WINDOW_HEIGHT
    for y in range(0, h, 4):
        ratio = y / float(h)
        r = int(top_color[0] * (1 - ratio) + bot_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bot_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bot_color[2] * ratio)
        pygame.draw.rect(surface, (r, g, b), (0, y, WINDOW_WIDTH, 4))


def run():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Day 20: Bioluminescent Deep-Sea Jellyfish Generative Art")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("Helvetica", 14, bold=True)
    font_hud = pygame.font.SysFont("Courier", 12)

    # Environment & specimen initialization
    env = DeepSeaEnvironment(num_particles=400)
    jellyfish_list = [
        Jellyfish(WINDOW_WIDTH * 0.50, WINDOW_HEIGHT * 0.48, scale=1.35),
        Jellyfish(WINDOW_WIDTH * 0.22, WINDOW_HEIGHT * 0.35, scale=0.95),
        Jellyfish(WINDOW_WIDTH * 0.78, WINDOW_HEIGHT * 0.62, scale=1.05),
        Jellyfish(WINDOW_WIDTH * 0.38, WINDOW_HEIGHT * 0.78, scale=0.80),
        Jellyfish(WINDOW_WIDTH * 0.68, WINDOW_HEIGHT * 0.22, scale=0.75),
    ]

    theme_idx = 0
    show_hud = True
    bloom_enabled = True
    paused = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    env.add_shockwave(event.pos[0], event.pos[1])
                elif event.button == 3:  # Right click spawns new jellyfish
                    jellyfish_list.append(
                        Jellyfish(event.pos[0], event.pos[1], scale=random.uniform(0.7, 1.25))
                    )
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_t:
                    theme_idx = (theme_idx + 1) % len(THEMES)
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_UP):
                    # Spawn new jellyfish
                    rx = random.uniform(80, WINDOW_WIDTH - 80)
                    ry = random.uniform(80, WINDOW_HEIGHT - 80)
                    jellyfish_list.append(Jellyfish(rx, ry, scale=random.uniform(0.75, 1.3)))
                elif event.key in (pygame.K_MINUS, pygame.K_DOWN):
                    if len(jellyfish_list) > 1:
                        jellyfish_list.pop()
                elif event.key == pygame.K_g:
                    bloom_enabled = not bloom_enabled
                elif event.key == pygame.K_c:
                    # Multi-specimen bloom
                    jellyfish_list.clear()
                    for _ in range(7):
                        rx = random.uniform(100, WINDOW_WIDTH - 100)
                        ry = random.uniform(100, WINDOW_HEIGHT - 100)
                        jellyfish_list.append(Jellyfish(rx, ry, scale=random.uniform(0.65, 1.35)))
                elif event.key == pygame.K_h:
                    show_hud = not show_hud
                elif event.key in (pygame.K_p, pygame.K_s) and (pygame.key.get_mods() & pygame.KMOD_CTRL or event.key == pygame.K_p):
                    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
                    os.makedirs(out_dir, exist_ok=True)
                    stamp = time.strftime("%Y%m%d_%H%M%S")
                    out_path = os.path.join(out_dir, f"day20_jellyfish_{stamp}.png")
                    pygame.image.save(screen, out_path)
                    print(f"📸 Saved screenshot: {out_path}")

        # Update
        if not paused:
            env.update(dt)
            for j in jellyfish_list:
                j.update(dt, env.shockwaves)

        # Draw deep-sea backdrop
        theme = THEMES[theme_idx]
        draw_gradient_background(screen, theme["bg_top"], theme["bg_bot"])

        # Draw marine snow & shockwaves
        env.draw(screen, theme)

        # Draw jellyfish specimens (sorted by scale so small ones are in background)
        jellyfish_list.sort(key=lambda j: j.base_scale)
        for j in jellyfish_list:
            j.draw(screen, theme, bloom=bloom_enabled)

        # Telemetry HUD
        if show_hud:
            hud_rect = pygame.Rect(15, 12, WINDOW_WIDTH - 30, 48)
            hud_bg = pygame.Surface((hud_rect.width, hud_rect.height), pygame.SRCALPHA)
            hud_bg.fill((6, 12, 20, 215))
            screen.blit(hud_bg, hud_rect)

            title_txt = font_title.render(
                f"DAY 20: BIOLUMINESCENT DEEP-SEA JELLYFISH ({theme['name'].upper()})",
                True,
                (120, 240, 255),
            )
            stats_txt = font_hud.render(
                f"Specimens: {len(jellyfish_list)} | Plankton: {env.num_particles} | Bloom: {'ON' if bloom_enabled else 'OFF'} | FPS: {clock.get_fps():.0f}",
                True,
                (230, 242, 255),
            )
            screen.blit(title_txt, (hud_rect.x + 12, hud_rect.y + 6))
            screen.blit(stats_txt, (hud_rect.x + 12, hud_rect.y + 26))

            # Bottom controls pill
            bot_rect = pygame.Rect(15, WINDOW_HEIGHT - 38, WINDOW_WIDTH - 30, 26)
            bot_bg = pygame.Surface((bot_rect.width, bot_rect.height), pygame.SRCALPHA)
            bot_bg.fill((6, 12, 20, 215))
            screen.blit(bot_bg, bot_rect)

            ctrl_str = (
                "[Click] Shockwave | [T] Theme | [+/-] Spawn/Remove | [G] Bloom | [C] Bloom Swarm | [P] Save | [ESC] Exit"
            )
            ctrl_txt = font_hud.render(ctrl_str, True, (230, 242, 255))
            screen.blit(ctrl_txt, (bot_rect.x + 12, bot_rect.y + 6))

        pygame.display.flip()

    pygame.quit()


# ==============================================================================
# 5. ASSET EXPORT FUNCTIONS
# ==============================================================================
def export_poster(output_path, size=(WINDOW_WIDTH, WINDOW_HEIGHT)):
    """Renders and saves a high-resolution PNG poster of the bioluminescent deep-sea scene."""
    from PIL import Image, ImageDraw

    w, h = size
    theme = THEMES[0]  # Abyssal Azure

    # Gradient background
    bg = Image.new("RGB", (w, h))
    for y in range(h):
        ratio = y / float(h)
        r = int(theme["bg_top"][0] * (1 - ratio) + theme["bg_bot"][0] * ratio)
        g = int(theme["bg_top"][1] * (1 - ratio) + theme["bg_bot"][1] * ratio)
        b = int(theme["bg_top"][2] * (1 - ratio) + theme["bg_bot"][2] * ratio)
        for x in range(w):
            bg.putpixel((x, y), (r, g, b))

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. Marine snow
    random.seed(42)
    c_snow = theme["snow"]
    for _ in range(450):
        px = random.uniform(0, w)
        py = random.uniform(0, h)
        sz = random.uniform(1.0, 2.8)
        alpha = random.randint(40, 220)
        draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=(c_snow[0], c_snow[1], c_snow[2], alpha))

    # 2. Jellyfish specimens
    specimens = [
        (w * 0.48, h * 0.45, 1.45, 0.4),
        (w * 0.22, h * 0.32, 0.95, 1.2),
        (w * 0.78, h * 0.58, 1.10, 2.3),
        (w * 0.35, h * 0.78, 0.85, 3.1),
        (w * 0.68, h * 0.20, 0.75, 4.2),
    ]

    c_bell = theme["bell"]
    c_org = theme["organ"]
    c_tent = theme["tentacles"]
    c_glow = theme["glow"]

    for x, y, scale, phase in specimens:
        cur_w = 42.0 * scale * (1.0 - 0.15 * math.sin(phase))
        cur_h = 36.0 * scale * (1.0 + 0.25 * math.sin(phase))

        # Aura
        glow_r = cur_w * 1.6
        draw.ellipse(
            [x - glow_r, y - glow_r, x + glow_r, y + glow_r],
            fill=(c_glow[0], c_glow[1], c_glow[2], 30),
        )

        # Tentacles
        for i in range(12):
            t_ratio = i / 11.0
            ang = math.pi * (0.08 + 0.84 * t_ratio)
            rx = x + cur_w * math.cos(ang)
            ry = y + cur_h * 0.25
            pts = [(rx, ry)]
            cur_x, cur_y = rx, ry
            for s in range(24):
                cur_x += math.sin(phase + s * 0.28 + i) * 2.8 * scale
                cur_y += 7.0 * scale
                pts.append((cur_x, cur_y))
            draw.line(pts, fill=(c_tent[0], c_tent[1], c_tent[2], 75), width=1)

        # Oral arms
        for i in range(4):
            offset_x = (i - 1.5) * (cur_w * 0.22)
            pts = [(x + offset_x, y + cur_h * 0.2)]
            cur_x, cur_y = x + offset_x, y + cur_h * 0.2
            for s in range(18):
                cur_x += math.sin(phase * 1.5 + s * 0.35 + i * 2) * 3.5 * scale
                cur_y += 6.5 * scale
                pts.append((cur_x, cur_y))
            draw.line(pts, fill=(c_org[0], c_org[1], c_org[2], 120), width=2)

        # Bell dome
        bell_pts = []
        for i in range(33):
            theta = math.pi * (i / 32.0)
            bx = x - cur_w * math.cos(theta)
            by = y - cur_h * math.sin(theta)
            bell_pts.append((bx, by))
        for i in range(32, -1, -1):
            theta = math.pi * (i / 32.0)
            bx = x - cur_w * math.cos(theta)
            scallop = 3.5 * math.sin(theta * 10.0 + phase * 2.0)
            by = y + cur_h * 0.18 + scallop
            bell_pts.append((bx, by))

        draw.polygon(bell_pts, fill=(c_bell[0], c_bell[1], c_bell[2], 65), outline=(c_bell[0], c_bell[1], c_bell[2], 200))

        # Organs
        for k in range(4):
            ang = k * (math.pi / 2.0) + phase * 0.15
            gx = x + (cur_w * 0.22) * math.cos(ang)
            gy = y - (cur_h * 0.32) + (cur_h * 0.15) * math.sin(ang)
            org_r = cur_w * 0.18
            draw.ellipse(
                [gx - org_r, gy - org_r, gx + org_r, gy + org_r],
                fill=(c_org[0], c_org[1], c_org[2], 210),
            )

    out = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    out.save(output_path, optimize=True)
    print(f"✅ Saved Day 20 poster: {output_path}")


def export_animation(output_path, num_frames=45, frame_size=(600, 600)):
    """Generates an animated preview GIF of pulsating bioluminescent deep-sea jellyfish."""
    from PIL import Image, ImageDraw

    w, h = frame_size
    theme = THEMES[0]
    frames = []

    # Pre-render background
    bg = Image.new("RGB", (w, h))
    for y in range(h):
        ratio = y / float(h)
        r = int(theme["bg_top"][0] * (1 - ratio) + theme["bg_bot"][0] * ratio)
        g = int(theme["bg_top"][1] * (1 - ratio) + theme["bg_bot"][1] * ratio)
        b = int(theme["bg_top"][2] * (1 - ratio) + theme["bg_bot"][2] * ratio)
        for x in range(w):
            bg.putpixel((x, y), (r, g, b))

    # Base specimens scaled for 600x600
    scale_fac = w / float(WINDOW_WIDTH)
    specimens = [
        {"x": w * 0.48, "y": h * 0.46, "scale": 1.35 * scale_fac, "vy": -0.8},
        {"x": w * 0.22, "y": h * 0.35, "scale": 0.95 * scale_fac, "vy": -0.5},
        {"x": w * 0.78, "y": h * 0.60, "scale": 1.05 * scale_fac, "vy": -0.6},
        {"x": w * 0.35, "y": h * 0.78, "scale": 0.80 * scale_fac, "vy": -0.4},
        {"x": w * 0.68, "y": h * 0.22, "scale": 0.75 * scale_fac, "vy": -0.3},
    ]

    c_bell = theme["bell"]
    c_org = theme["organ"]
    c_tent = theme["tentacles"]
    c_snow = theme["snow"]

    # Fixed particles
    random.seed(42)
    plankton = [
        (random.uniform(0, w), random.uniform(0, h), random.uniform(1.0, 2.2), random.uniform(0, 2 * math.pi))
        for _ in range(220)
    ]

    for frame_idx in range(num_frames):
        t = frame_idx * (2.0 * math.pi / num_frames)
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Marine snow
        for px, py, sz, phase in plankton:
            py_anim = (py + frame_idx * 0.6) % h
            alpha = int(140 + 80 * math.sin(phase + t * 2.0))
            draw.ellipse([px - sz, py_anim - sz, px + sz, py_anim + sz], fill=(c_snow[0], c_snow[1], c_snow[2], alpha))

        # Jellyfish
        for spec in specimens:
            phase = t * 2.0 + spec["x"] * 0.02
            pulse = math.sin(phase)
            cur_w = 42.0 * spec["scale"] * (1.0 - 0.20 * pulse)
            cur_h = 36.0 * spec["scale"] * (1.0 + 0.30 * pulse)
            jx = spec["x"] + math.sin(t + spec["y"]) * 8.0
            jy = spec["y"] + math.sin(phase) * 6.0

            # Tentacles
            for i in range(8):
                t_ratio = i / 7.0
                ang = math.pi * (0.1 + 0.8 * t_ratio)
                rx = jx + cur_w * math.cos(ang)
                ry = jy + cur_h * 0.25
                pts = [(rx, ry)]
                cur_x, cur_y = rx, ry
                for s in range(16):
                    cur_x += math.sin(phase + s * 0.32 + i) * 2.4 * spec["scale"]
                    cur_y += 6.0 * spec["scale"]
                    pts.append((cur_x, cur_y))
                draw.line(pts, fill=(c_tent[0], c_tent[1], c_tent[2], 70), width=1)

            # Bell
            bell_pts = []
            for i in range(25):
                theta = math.pi * (i / 24.0)
                bx = jx - cur_w * math.cos(theta)
                by = jy - cur_h * math.sin(theta)
                bell_pts.append((bx, by))
            for i in range(24, -1, -1):
                theta = math.pi * (i / 24.0)
                bx = jx - cur_w * math.cos(theta)
                scallop = 2.5 * math.sin(theta * 8.0 + phase * 2.0)
                by = jy + cur_h * 0.18 + scallop
                bell_pts.append((bx, by))

            draw.polygon(bell_pts, fill=(c_bell[0], c_bell[1], c_bell[2], 65), outline=(c_bell[0], c_bell[1], c_bell[2], 210))

            # Internal organ core
            org_pulse = 0.5 + 0.5 * math.sin(phase * 2.0)
            org_alpha = int(150 + 90 * org_pulse)
            for k in range(4):
                ang = k * (math.pi / 2.0) + phase * 0.15
                gx = jx + (cur_w * 0.20) * math.cos(ang)
                gy = jy - (cur_h * 0.30) + (cur_h * 0.14) * math.sin(ang)
                org_r = cur_w * 0.16
                draw.ellipse(
                    [gx - org_r, gy - org_r, gx + org_r, gy + org_r],
                    fill=(c_org[0], c_org[1], c_org[2], org_alpha),
                )

        composed = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
        frames.append(composed.quantize(colors=128))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        optimize=True,
    )
    print(f"✅ Saved Day 20 animated preview: {output_path} ({len(frames)} frames)")


if __name__ == "__main__":
    if "--export" in sys.argv:
        export_poster("assets/day20_jellyfish_art.png")
        export_animation("assets/day20_animation.gif")
    else:
        run()

"""
Day 21: 3D Quantum Torus Knot & Hopf Fibration Art
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A mesmerizing 3D generative art simulation exploring the topology of (p, q) torus knots,
harmonic wave energy packets, and quantum Hopf fibration geometry in 3D space.

Features:
1. 3D Perspective Projection & Depth Sorting:
   - 2,400+ luminous 3D quantum nodes circulating along topological torus knots
   - Depth-based atmospheric fogging, perspective radius scaling, and radiant particle halos
   - Smooth 3D camera controls: click & drag to orbit pitch and yaw with realistic rotational inertia
2. 4 Mathematical Knot Topologies:
   - Mode 1: Trefoil Quantum Knot (p=2, q=3) - The fundamental prime knot of quantum vortices
   - Mode 2: Cinqfoil Sacred Knot (p=5, q=2) - Five-lobed sacred geometry star braid
   - Mode 3: Solar Septagram Knot (p=7, q=3) - Dense high-frequency harmonic toroidal braid
   - Mode 4: Hopf Fibration Nested Torus (p=1, q=1) - Concentric nested torus fibers in 4D->3D
3. Dynamic Energy Dynamics:
   - Harmonic standing waves rippling along the knot spine ([W]/[S] keys)
   - Translucent constellation filaments linking harmonic winding neighbors ([L] key)
   - 6 curated chromatic themes: Cyberpunk Neon, Electric Cyan & Gold, Celestial Aurora,
     Solar Flare Amber, Deep Abyss Violet, and Pearl Monochrome.

Controls:
  [1] - [4]   - Switch Knot Topology (Trefoil, Cinqfoil, Septagram, Hopf Fibration)
  [SPACE]     - Pause / Resume orbital motion and wave oscillations
  [Left Drag] - Orbit 3D camera (Pitch and Yaw)
  [Mouse Wheel]- 3D perspective zoom in / out (0.3x to 4.0x)
  [T]         - Cycle Chromatic Color Themes
  [L]         - Toggle Constellation Filaments (Connecting energy lines)
  [W] / [S]   - Increase / Decrease harmonic wave amplitude
  [+] / [UP]  - Speed up orbital circulation and wave frequency
  [-] / [DOWN]- Slow down orbital circulation and wave frequency
  [R]         - Reset 3D camera view, zoom, and parameters
  [H]         - Toggle Telemetry HUD
  [P]         - Save high-resolution PNG screenshot to output/
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
# 1. CONFIGURATION & CONSTANTS
# ==============================================================================
WINDOW_WIDTH = 920
WINDOW_HEIGHT = 920
FPS = 60
NUM_NODES = 2400

THEMES = [
    {
        "name": "Cyberpunk Neon",
        "bg": (8, 10, 18),
        "primary": (255, 45, 130),    # Hot Magenta
        "secondary": (0, 245, 255),   # Laser Cyan
        "tertiary": (255, 205, 40),   # Electric Gold
        "filament": (70, 170, 230, 60),
    },
    {
        "name": "Electric Cyan & Gold",
        "bg": (6, 12, 20),
        "primary": (40, 235, 255),    # Electric Cyan
        "secondary": (255, 215, 65),  # 24K Radiant Gold
        "tertiary": (165, 250, 185),  # Mint Flare
        "filament": (50, 195, 225, 55),
    },
    {
        "name": "Celestial Aurora",
        "bg": (6, 15, 14),
        "primary": (60, 255, 175),    # Emerald Aurora
        "secondary": (80, 210, 255),  # Celestial Blue
        "tertiary": (235, 140, 255),  # Ethereal Violet
        "filament": (60, 205, 175, 50),
    },
    {
        "name": "Solar Flare Amber",
        "bg": (16, 8, 6),
        "primary": (255, 105, 30),    # Solar Amber
        "secondary": (255, 220, 75),  # Radiant Flare
        "tertiary": (255, 45, 60),    # Crimson Corona
        "filament": (220, 115, 45, 55),
    },
    {
        "name": "Deep Abyss Violet",
        "bg": (10, 6, 18),
        "primary": (195, 95, 255),    # Orchid Violet
        "secondary": (95, 165, 255),  # Abyssal Blue
        "tertiary": (255, 140, 200),  # Blossom Rose
        "filament": (145, 95, 215, 55),
    },
    {
        "name": "Pearl Monochrome",
        "bg": (14, 15, 18),
        "primary": (245, 248, 255),   # Luminous Pearl
        "secondary": (160, 175, 195), # Silver Steel
        "tertiary": (210, 225, 245),  # Ice Platinum
        "filament": (160, 180, 215, 50),
    },
]


# ==============================================================================
# 2. 3D TORUS KNOT & HOPF FIBRATION GENERATOR
# ==============================================================================
class TorusKnot3D:
    """Computes 3D coordinates for (p, q) torus knots and Hopf fibration manifolds."""

    def __init__(self, num_nodes=NUM_NODES):
        self.num_nodes = num_nodes
        self.mode = 1  # 1 = Trefoil (2,3), 2 = Cinqfoil (5,2), 3 = Septagram (7,3), 4 = Hopf
        self.R = 210.0  # Major radius of torus
        self.r = 85.0   # Minor radius of tube
        self.wave_amplitude = 28.0
        self.wave_freq = 3.2
        self.circulation_speed = 0.014
        self.indices = np.arange(self.num_nodes, dtype=float)

    def compute_positions(self, t):
        """Returns (N, 3) 3D coordinates for the active topological knot."""
        n = self.indices
        total = float(self.num_nodes)

        if self.mode == 1:
            # Mode 1: Trefoil Knot (p=2, q=3)
            # Winding angles
            p, q = 2, 3
            phi = (n / total) * 2.0 * math.pi + t * 0.4
            r_eff = self.R + self.r * np.cos(q * phi)
            x = r_eff * np.cos(p * phi)
            y = r_eff * np.sin(p * phi)
            # Harmonic wave running along knot spine
            wave = self.wave_amplitude * np.sin(phi * 12.0 - t * self.wave_freq)
            z = -self.r * np.sin(q * phi) + wave
            return np.column_stack((x, y, z))

        elif self.mode == 2:
            # Mode 2: Cinqfoil Sacred Knot (p=5, q=2)
            p, q = 5, 2
            phi = (n / total) * 2.0 * math.pi + t * 0.35
            r_eff = self.R * 0.95 + self.r * 1.15 * np.cos(q * phi)
            x = r_eff * np.cos(p * phi)
            y = r_eff * np.sin(p * phi)
            wave = self.wave_amplitude * np.sin(phi * 15.0 - t * self.wave_freq)
            z = -self.r * 1.15 * np.sin(q * phi) + wave
            return np.column_stack((x, y, z))

        elif self.mode == 3:
            # Mode 3: Solar Septagram Knot (p=7, q=3)
            p, q = 7, 3
            phi = (n / total) * 2.0 * math.pi + t * 0.3
            r_eff = self.R * 0.92 + self.r * 1.25 * np.cos(q * phi)
            x = r_eff * np.cos(p * phi)
            y = r_eff * np.sin(p * phi)
            wave = self.wave_amplitude * np.sin(phi * 21.0 - t * self.wave_freq)
            z = -self.r * 1.25 * np.sin(q * phi) + wave
            return np.column_stack((x, y, z))

        else:
            # Mode 4: Hopf Fibration Nested Torus Manifold
            # Multiple nested circles rotated by Villarceau angles
            num_rings = 24
            nodes_per_ring = self.num_nodes // num_rings
            ring_idx = n // nodes_per_ring
            node_in_ring = n % nodes_per_ring

            theta = (node_in_ring / float(nodes_per_ring)) * 2.0 * math.pi + t * 0.8
            psi = (ring_idx / float(num_rings)) * 2.0 * math.pi + t * 0.25

            # Nested torus radii
            R_hopf = self.R * (0.65 + 0.45 * np.sin(psi))
            r_hopf = self.r * (0.8 + 0.3 * np.cos(psi))

            x = (R_hopf + r_hopf * np.cos(theta)) * np.cos(psi)
            y = (R_hopf + r_hopf * np.cos(theta)) * np.sin(psi)
            wave = self.wave_amplitude * 0.8 * np.sin(theta * 3.0 + psi * 2.0 - t * 2.5)
            z = r_hopf * np.sin(theta) + wave
            return np.column_stack((x, y, z))


# ==============================================================================
# 3. 3D PERSPECTIVE CAMERA & DEPTH SORTING
# ==============================================================================
class Camera3D:
    """Manages 3D rotation, pitch/yaw damping, perspective divide, and depth sorting."""

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.rot_x = 0.52
        self.rot_y = 0.0
        self.zoom = 1.05
        self.focal_length = 760.0
        self.distance = 960.0

        self.is_dragging = False
        self.last_mouse_pos = (0, 0)
        self.vel_x = 0.0
        self.vel_y = 0.007

    def handle_mouse_down(self, pos):
        self.is_dragging = True
        self.last_mouse_pos = pos

    def handle_mouse_up(self):
        self.is_dragging = False

    def handle_mouse_motion(self, pos):
        if self.is_dragging:
            dx = pos[0] - self.last_mouse_pos[0]
            dy = pos[1] - self.last_mouse_pos[1]
            self.vel_y = dx * 0.005
            self.vel_x = -dy * 0.005
            self.last_mouse_pos = pos

    def update(self, auto_rotate=True):
        if not self.is_dragging and auto_rotate:
            self.rot_y += self.vel_y
            self.rot_x += self.vel_x
            self.vel_y = self.vel_y * 0.96 + 0.007 * 0.04
            self.vel_x *= 0.94
        elif self.is_dragging:
            self.rot_y += self.vel_y
            self.rot_x += self.vel_x

        self.rot_x = max(-1.45, min(1.45, self.rot_x))

    def project(self, points):
        """Projects 3D points (N, 3) to 2D screen coordinates with perspective divide."""
        cos_x, sin_x = math.cos(self.rot_x), math.sin(self.rot_x)
        y1 = points[:, 1] * cos_x - points[:, 2] * sin_x
        z1 = points[:, 1] * sin_x + points[:, 2] * cos_x
        x1 = points[:, 0]

        cos_y, sin_y = math.cos(self.rot_y), math.sin(self.rot_y)
        x2 = x1 * cos_y + z1 * sin_y
        z2 = -x1 * sin_y + z1 * cos_y
        y2 = y1

        z_cam = z2 + self.distance
        z_safe = np.maximum(z_cam, 50.0)
        factor = (self.focal_length * self.zoom) / z_safe
        sx = self.cx + x2 * factor
        sy = self.cy + y2 * factor

        return np.column_stack((sx, sy)), z2, factor


# ==============================================================================
# 4. MAIN APPLICATION ENGINE
# ==============================================================================
def run():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Day 21: 3D Quantum Torus Knot & Hopf Fibration Art")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("Helvetica", 14, bold=True)
    font_hud = pygame.font.SysFont("Courier", 12)

    cx, cy = WINDOW_WIDTH / 2.0, WINDOW_HEIGHT / 2.0 - 15
    knot = TorusKnot3D(NUM_NODES)
    camera = Camera3D(cx, cy)

    theme_idx = 0
    show_filaments = True
    show_hud = True
    paused = False
    sim_time = 0.0

    mode_names = [
        "1: Trefoil Quantum Knot (p=2, q=3)",
        "2: Cinqfoil Sacred Knot (p=5, q=2)",
        "3: Solar Septagram Knot (p=7, q=3)",
        "4: Hopf Fibration Nested Torus",
    ]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    camera.handle_mouse_down(event.pos)
                elif event.button == 4:
                    camera.zoom = min(4.0, camera.zoom * 1.08)
                elif event.button == 5:
                    camera.zoom = max(0.3, camera.zoom / 1.08)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    camera.handle_mouse_up()
            elif event.type == pygame.MOUSEMOTION:
                camera.handle_mouse_motion(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_1:
                    knot.mode = 1
                elif event.key == pygame.K_2:
                    knot.mode = 2
                elif event.key == pygame.K_3:
                    knot.mode = 3
                elif event.key == pygame.K_4:
                    knot.mode = 4
                elif event.key == pygame.K_t:
                    theme_idx = (theme_idx + 1) % len(THEMES)
                elif event.key == pygame.K_l:
                    show_filaments = not show_filaments
                elif event.key == pygame.K_w:
                    knot.wave_amplitude = min(90.0, knot.wave_amplitude + 6.0)
                elif event.key == pygame.K_s and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    knot.wave_amplitude = max(0.0, knot.wave_amplitude - 6.0)
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_UP):
                    knot.circulation_speed = min(0.06, knot.circulation_speed + 0.003)
                    knot.wave_freq = min(7.0, knot.wave_freq + 0.4)
                elif event.key in (pygame.K_MINUS, pygame.K_DOWN):
                    knot.circulation_speed = max(0.002, knot.circulation_speed - 0.003)
                    knot.wave_freq = max(0.4, knot.wave_freq - 0.4)
                elif event.key == pygame.K_r:
                    camera.rot_x = 0.52
                    camera.rot_y = 0.0
                    camera.zoom = 1.05
                    knot.wave_amplitude = 28.0
                elif event.key == pygame.K_h:
                    show_hud = not show_hud
                elif event.key in (pygame.K_p, pygame.K_s) and (pygame.key.get_mods() & pygame.KMOD_CTRL or event.key == pygame.K_p):
                    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
                    os.makedirs(out_dir, exist_ok=True)
                    stamp = time.strftime("%Y%m%d_%H%M%S")
                    out_path = os.path.join(out_dir, f"day21_torus_knot_{stamp}.png")
                    pygame.image.save(screen, out_path)
                    print(f"📸 Saved screenshot: {out_path}")

        if not paused:
            sim_time += dt
            camera.update(auto_rotate=True)
        else:
            camera.update(auto_rotate=False)

        theme = THEMES[theme_idx]
        screen.fill(theme["bg"])

        # Compute 3D positions & project
        points_3d = knot.compute_positions(sim_time)
        pts_2d, depths, factors = camera.project(points_3d)
        sort_order = np.argsort(depths)

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        # 1. Connecting filaments along topological knot curve
        if show_filaments:
            filament_col = theme["filament"]
            step = 1 if knot.mode in (1, 2, 3) else 2
            for i in range(0, knot.num_nodes - step, 2):
                p1 = pts_2d[i]
                p2 = pts_2d[i + step]
                if 0 <= p1[0] < WINDOW_WIDTH and 0 <= p1[1] < WINDOW_HEIGHT:
                    if 0 <= p2[0] < WINDOW_WIDTH and 0 <= p2[1] < WINDOW_HEIGHT:
                        avg_depth = (depths[i] + depths[i + step]) / 2.0
                        depth_norm = np.clip((avg_depth + 450.0) / 900.0, 0.15, 1.0)
                        f_alpha = int(filament_col[3] * depth_norm * 1.2)
                        pygame.draw.aaline(
                            overlay,
                            (filament_col[0], filament_col[1], filament_col[2], f_alpha),
                            p1,
                            p2,
                        )

        # 2. Draw depth-sorted luminous nodes
        c_prim = theme["primary"]
        c_sec = theme["secondary"]
        c_tert = theme["tertiary"]

        for idx in sort_order:
            px, py = pts_2d[idx]
            if not (-20 <= px <= WINDOW_WIDTH + 20 and -20 <= py <= WINDOW_HEIGHT + 20):
                continue

            factor = factors[idx]
            depth_ratio = np.clip((depths[idx] + 450.0) / 900.0, 0.15, 1.0)

            t_ratio = (idx % 300) / 300.0
            if t_ratio < 0.5:
                u = t_ratio * 2.0
                r_c = int(c_prim[0] * (1 - u) + c_sec[0] * u)
                g_c = int(c_prim[1] * (1 - u) + c_sec[1] * u)
                b_c = int(c_prim[2] * (1 - u) + c_sec[2] * u)
            else:
                u = (t_ratio - 0.5) * 2.0
                r_c = int(c_sec[0] * (1 - u) + c_tert[0] * u)
                g_c = int(c_sec[1] * (1 - u) + c_tert[1] * u)
                b_c = int(c_sec[2] * (1 - u) + c_tert[2] * u)

            node_radius = max(1.2, 3.6 * factor)
            alpha = int(np.clip(255 * depth_ratio, 45, 255))

            if factor > 0.8:
                halo_radius = int(node_radius * 2.2)
                halo_alpha = int(alpha * 0.3)
                pygame.draw.circle(
                    overlay,
                    (r_c, g_c, b_c, halo_alpha),
                    (int(px), int(py)),
                    halo_radius,
                )

            pygame.draw.circle(
                overlay,
                (r_c, g_c, b_c, alpha),
                (int(px), int(py)),
                int(node_radius),
            )

        screen.blit(overlay, (0, 0))

        # Telemetry HUD
        if show_hud:
            hud_rect = pygame.Rect(15, 12, WINDOW_WIDTH - 30, 48)
            hud_bg = pygame.Surface((hud_rect.width, hud_rect.height), pygame.SRCALPHA)
            hud_bg.fill((10, 15, 25, 215))
            screen.blit(hud_bg, hud_rect)

            active_mode_str = mode_names[knot.mode - 1]
            title_txt = font_title.render(f"DAY 21: {active_mode_str.upper()}", True, (255, 205, 80))
            stats_txt = font_hud.render(
                f"Nodes: {knot.num_nodes:,} | Zoom: {camera.zoom:.2f}x | Wave: {knot.wave_amplitude:.0f}px | Filaments: {'ON' if show_filaments else 'OFF'} | FPS: {clock.get_fps():.0f}",
                True,
                (240, 245, 255),
            )
            screen.blit(title_txt, (hud_rect.x + 12, hud_rect.y + 6))
            screen.blit(stats_txt, (hud_rect.x + 12, hud_rect.y + 26))

            bot_rect = pygame.Rect(15, WINDOW_HEIGHT - 38, WINDOW_WIDTH - 30, 26)
            bot_bg = pygame.Surface((bot_rect.width, bot_rect.height), pygame.SRCALPHA)
            bot_bg.fill((10, 15, 25, 215))
            screen.blit(bot_bg, bot_rect)

            ctrl_str = "[1-4] Knot Modes | [Drag] Orbit 3D | [Wheel] Zoom | [T] Theme | [L] Filaments | [W/S] Wave | [P] Save | [ESC] Exit"
            ctrl_txt = font_hud.render(ctrl_str, True, (240, 245, 255))
            screen.blit(ctrl_txt, (bot_rect.x + 12, bot_rect.y + 6))

        pygame.display.flip()

    pygame.quit()


# ==============================================================================
# 5. ASSET EXPORT FUNCTIONS
# ==============================================================================
def export_poster(output_path, size=(WINDOW_WIDTH, WINDOW_HEIGHT)):
    """Renders and exports a high-resolution PNG poster of the 3D quantum torus knot."""
    from PIL import Image, ImageDraw

    cx, cy = size[0] / 2.0, size[1] / 2.0 - 15
    knot = TorusKnot3D(2600)
    camera = Camera3D(cx, cy)
    camera.rot_x = 0.54
    camera.rot_y = 0.42
    camera.zoom = 1.12

    theme = THEMES[1]  # Electric Cyan & Gold
    points_3d = knot.compute_positions(1.8)
    pts_2d, depths, factors = camera.project(points_3d)
    sort_order = np.argsort(depths)

    w, h = size
    bg_img = Image.new("RGB", (w, h), theme["bg"])
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    filament_col = theme["filament"]
    for i in range(0, knot.num_nodes - 1, 2):
        p1 = (pts_2d[i][0], pts_2d[i][1])
        p2 = (pts_2d[i + 1][0], pts_2d[i + 1][1])
        if 0 <= p1[0] < w and 0 <= p1[1] < h and 0 <= p2[0] < w and 0 <= p2[1] < h:
            avg_depth = (depths[i] + depths[i + 1]) / 2.0
            depth_norm = np.clip((avg_depth + 450.0) / 900.0, 0.2, 1.0)
            f_alpha = int(filament_col[3] * depth_norm * 1.5)
            draw.line([p1, p2], fill=(filament_col[0], filament_col[1], filament_col[2], f_alpha), width=1)

    c_prim = theme["primary"]
    c_sec = theme["secondary"]
    c_tert = theme["tertiary"]

    for idx in sort_order:
        px, py = pts_2d[idx]
        if not (-10 <= px <= w + 10 and -10 <= py <= h + 10):
            continue
        factor = factors[idx]
        depth_ratio = np.clip((depths[idx] + 450.0) / 900.0, 0.2, 1.0)

        t_ratio = (idx % 300) / 300.0
        if t_ratio < 0.5:
            u = t_ratio * 2.0
            r_c = int(c_prim[0] * (1 - u) + c_sec[0] * u)
            g_c = int(c_prim[1] * (1 - u) + c_sec[1] * u)
            b_c = int(c_prim[2] * (1 - u) + c_sec[2] * u)
        else:
            u = (t_ratio - 0.5) * 2.0
            r_c = int(c_sec[0] * (1 - u) + c_tert[0] * u)
            g_c = int(c_sec[1] * (1 - u) + c_tert[1] * u)
            b_c = int(c_sec[2] * (1 - u) + c_tert[2] * u)

        node_r = max(1.5, 3.8 * factor)
        alpha = int(np.clip(255 * depth_ratio, 50, 255))

        if factor > 0.8:
            halo_r = node_r * 2.4
            draw.ellipse(
                [px - halo_r, py - halo_r, px + halo_r, py + halo_r],
                fill=(r_c, g_c, b_c, int(alpha * 0.35)),
            )

        draw.ellipse([px - node_r, py - node_r, px + node_r, py + node_r], fill=(r_c, g_c, b_c, alpha))

    out = Image.alpha_composite(bg_img.convert("RGBA"), overlay).convert("RGB")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    out.save(output_path, optimize=True)
    print(f"✅ Saved Day 21 poster: {output_path}")


def export_animation(output_path, num_frames=48, frame_size=(600, 600)):
    """Generates an animated preview GIF of the rotating 3D quantum torus knot."""
    from PIL import Image, ImageDraw

    cx, cy = frame_size[0] / 2.0, frame_size[1] / 2.0
    knot = TorusKnot3D(1600)
    camera = Camera3D(cx, cy)
    camera.rot_x = 0.52
    camera.zoom = 1.08

    theme = THEMES[1]
    w, h = frame_size
    frames = []

    c_prim = theme["primary"]
    c_sec = theme["secondary"]
    c_tert = theme["tertiary"]
    filament_col = theme["filament"]

    for frame_idx in range(num_frames):
        t = frame_idx * (2.0 * math.pi / num_frames)
        camera.rot_y = t

        points_3d = knot.compute_positions(t * 1.5)
        pts_2d, depths, factors = camera.project(points_3d)
        sort_order = np.argsort(depths)

        bg_img = Image.new("RGB", (w, h), theme["bg"])
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for i in range(0, knot.num_nodes - 1, 2):
            p1 = (pts_2d[i][0], pts_2d[i][1])
            p2 = (pts_2d[i + 1][0], pts_2d[i + 1][1])
            if 0 <= p1[0] < w and 0 <= p1[1] < h and 0 <= p2[0] < w and 0 <= p2[1] < h:
                avg_depth = (depths[i] + depths[i + 1]) / 2.0
                depth_norm = np.clip((avg_depth + 450.0) / 900.0, 0.2, 1.0)
                f_alpha = int(filament_col[3] * depth_norm * 1.4)
                draw.line([p1, p2], fill=(filament_col[0], filament_col[1], filament_col[2], f_alpha), width=1)

        for idx in sort_order:
            px, py = pts_2d[idx]
            if not (-10 <= px <= w + 10 and -10 <= py <= h + 10):
                continue
            factor = factors[idx]
            depth_ratio = np.clip((depths[idx] + 450.0) / 900.0, 0.2, 1.0)

            t_ratio = (idx % 300) / 300.0
            if t_ratio < 0.5:
                u = t_ratio * 2.0
                r_c = int(c_prim[0] * (1 - u) + c_sec[0] * u)
                g_c = int(c_prim[1] * (1 - u) + c_sec[1] * u)
                b_c = int(c_prim[2] * (1 - u) + c_sec[2] * u)
            else:
                u = (t_ratio - 0.5) * 2.0
                r_c = int(c_sec[0] * (1 - u) + c_tert[0] * u)
                g_c = int(c_sec[1] * (1 - u) + c_tert[1] * u)
                b_c = int(c_sec[2] * (1 - u) + c_tert[2] * u)

            node_r = max(1.2, 3.2 * factor)
            alpha = int(np.clip(255 * depth_ratio, 50, 255))

            if factor > 0.85:
                halo_r = node_r * 2.2
                draw.ellipse(
                    [px - halo_r, py - halo_r, px + halo_r, py + halo_r],
                    fill=(r_c, g_c, b_c, int(alpha * 0.3)),
                )

            draw.ellipse([px - node_r, py - node_r, px + node_r, py + node_r], fill=(r_c, g_c, b_c, alpha))

        composed = Image.alpha_composite(bg_img.convert("RGBA"), overlay).convert("RGB")
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
    print(f"✅ Saved Day 21 animated preview: {output_path} ({len(frames)} frames)")


if __name__ == "__main__":
    if "--export" in sys.argv:
        export_poster("assets/day21_torus_knot.png")
        export_animation("assets/day21_animation.gif")
    else:
        run()

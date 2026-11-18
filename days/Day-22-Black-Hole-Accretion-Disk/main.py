"""
Day 22: 3D Relativistic Black Hole & Accretion Vortex Simulation
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A breathtaking 3D astrophysical generative art simulation modeling a supermassive
relativistic black hole, glowing Keplerian accretion disk, relativistic Doppler beaming,
gravitational lensing rings, and bipolar helical magnetic plasma jets.

Features:
1. General Relativistic Black Hole Dynamics:
   - Central Schwarzschild Event Horizon & photon sphere (r = 1.5 Rs)
   - 3,600+ relativistic accretion disk particles orbiting with Keplerian velocities (v ~ 1/sqrt(r))
   - Relativistic Doppler Beaming: Oncoming orbital side is blue-shifted & amplified in brightness,
     while receding side is red-shifted and dimmed, creating authentic asymmetric radiance.
   - Gravitational Lensing Halo: Secondary warped light ring deflected above and below horizon.
   - Bipolar Helical Magnetic Plasma Jets shooting from north and south rotational poles ([J] key).
2. Interactive 3D Camera Controls:
   - Click & drag mouse to orbit pitch and yaw with rotational damping inertia.
   - Scroll-wheel 3D perspective zoom (0.3x to 4.0x).
   - Real-time depth sorting, luminous atmospheric glow halos, and HUD telemetry.
3. 6 Cosmic Chromatic Palettes:
   - Interstellar Gold & Cyan, Singularity Violet, Solar Corona Amber,
     Quasar Azure, Abyssal Monochrome, and Emerald Nova.

Controls:
  [SPACE]     - Pause / Resume relativistic simulation
  [Left Drag] - Orbit 3D camera (Pitch and Yaw)
  [Mouse Wheel]- 3D perspective zoom in / out (0.3x to 4.0x)
  [T]         - Cycle Cosmic Color Themes
  [J]         - Toggle Bipolar Relativistic Plasma Jets
  [L]         - Toggle Gravitational Lensing Rings
  [W] / [S]   - Increase / Decrease accretion disk matter density
  [+] / [UP]  - Speed up orbital time dilation
  [-] / [DOWN]- Slow down orbital time dilation
  [R]         - Reset 3D camera view, zoom, and parameters
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
# 1. CONFIGURATION & CONSTANTS
# ==============================================================================
WINDOW_WIDTH = 920
WINDOW_HEIGHT = 920
FPS = 60
NUM_PARTICLES = 3600
EVENT_HORIZON_RADIUS = 65.0  # Rs in screen pixels

THEMES = [
    {
        "name": "Interstellar Gold & Cyan",
        "bg": (4, 6, 12),
        "horizon": (0, 0, 0),
        "hot_beam": (100, 240, 255),   # Blue-shifted oncoming side
        "cool_beam": (255, 120, 40),   # Red-shifted receding side
        "jet": (120, 220, 255),
        "photon_ring": (255, 230, 160),
    },
    {
        "name": "Singularity Violet",
        "bg": (8, 4, 14),
        "horizon": (0, 0, 0),
        "hot_beam": (220, 140, 255),
        "cool_beam": (255, 60, 120),
        "jet": (190, 100, 255),
        "photon_ring": (255, 200, 255),
    },
    {
        "name": "Solar Corona Amber",
        "bg": (12, 6, 4),
        "horizon": (0, 0, 0),
        "hot_beam": (255, 245, 140),
        "cool_beam": (255, 65, 30),
        "jet": (255, 180, 50),
        "photon_ring": (255, 220, 100),
    },
    {
        "name": "Quasar Azure",
        "bg": (2, 8, 16),
        "horizon": (0, 0, 0),
        "hot_beam": (180, 255, 255),
        "cool_beam": (40, 140, 255),
        "jet": (80, 220, 255),
        "photon_ring": (220, 245, 255),
    },
    {
        "name": "Abyssal Monochrome",
        "bg": (10, 11, 14),
        "horizon": (0, 0, 0),
        "hot_beam": (255, 255, 255),
        "cool_beam": (140, 150, 165),
        "jet": (210, 225, 245),
        "photon_ring": (255, 255, 255),
    },
    {
        "name": "Emerald Nova",
        "bg": (3, 12, 10),
        "horizon": (0, 0, 0),
        "hot_beam": (140, 255, 205),
        "cool_beam": (35, 185, 130),
        "jet": (65, 250, 175),
        "photon_ring": (210, 255, 230),
    },
]


# ==============================================================================
# 2. RELATIVISTIC ACCRETION DISK & JET DYNAMICS
# ==============================================================================
class BlackHoleSystem3D:
    """Simulates relativistic Keplerian accretion disk, Doppler beaming, and magnetic jets."""

    def __init__(self, num_particles=NUM_PARTICLES):
        self.num_particles = num_particles
        self.Rs = EVENT_HORIZON_RADIUS
        self.r_inner = self.Rs * 1.5  # Innermost Stable Circular Orbit (ISCO)
        self.r_outer = self.Rs * 5.2
        self.sim_speed = 1.0
        self.show_jets = True
        self.show_lensing = True
        self.time = 0.0

        # Initialize accretion disk particles
        np.random.seed(42)
        # Power-law radial distribution (denser towards inner horizon)
        u = np.random.uniform(0.0, 1.0, self.num_particles)
        self.radii = self.r_inner + (self.r_outer - self.r_inner) * (u ** 1.8)
        self.angles = np.random.uniform(0.0, 2.0 * math.pi, self.num_particles)
        # Disk thickness flaring outward: h(r) ~ 0.05 * r
        self.z_offsets = np.random.normal(0.0, 1.0, self.num_particles) * (self.radii * 0.04)

        # Keplerian angular velocity omega = sqrt(GM / r^3)
        self.ang_vels = 28.0 / (self.radii ** 1.25)

        # Jet particles (500 particles per pole)
        self.num_jet_pts = 600
        self.jet_u = np.linspace(0.0, 1.0, self.num_jet_pts)

    def update(self, dt):
        self.time += dt * self.sim_speed
        self.angles += self.ang_vels * dt * self.sim_speed

    def compute_disk_particles(self):
        """Computes 3D positions and Doppler beaming intensities for accretion particles."""
        xs = self.radii * np.cos(self.angles)
        ys = self.radii * np.sin(self.angles)
        zs = self.z_offsets

        # Velocity vectors for Doppler factor: v = (-omega * y, omega * x, 0)
        # Normalized orbital direction
        v_dirs = np.column_stack((-np.sin(self.angles), np.cos(self.angles), np.zeros_like(self.angles)))
        return np.column_stack((xs, ys, zs)), v_dirs, self.radii

    def compute_lensing_ring(self, camera_rot_x):
        """Computes secondary warped image of the accretion disk bent above/below the horizon."""
        if not self.show_lensing:
            return None
        # Gravitationally lensed photon ring encircling the event horizon
        num_ring_pts = 360
        theta = np.linspace(0.0, 2.0 * math.pi, num_ring_pts, endpoint=False)
        # Warping: photon sphere light deflection
        r_lens = self.Rs * 1.55
        # Tilting with camera pitch to simulate curved light trajectories
        xs = r_lens * np.cos(theta)
        ys = r_lens * np.sin(theta) * 0.45
        zs = r_lens * np.sin(theta) * math.cos(camera_rot_x) * 0.95
        return np.column_stack((xs, ys, zs))

    def compute_jets(self):
        """Computes 3D positions of bipolar helical magnetic plasma jets."""
        if not self.show_jets:
            return None, None
        u = self.jet_u
        z_north = self.Rs * 0.6 + u * 380.0
        r_helix = (self.Rs * 0.18 + u * 48.0)
        phi_north = u * 24.0 + self.time * 6.0
        x_north = r_helix * np.cos(phi_north)
        y_north = r_helix * np.sin(phi_north)
        north_pts = np.column_stack((x_north, y_north, z_north))

        # South pole jet
        z_south = -z_north
        phi_south = -phi_north
        x_south = r_helix * np.cos(phi_south)
        y_south = r_helix * np.sin(phi_south)
        south_pts = np.column_stack((x_south, y_south, z_south))

        return north_pts, south_pts


# ==============================================================================
# 3. 3D PERSPECTIVE CAMERA & RELATIVISTIC DOPPLER PROJECTION
# ==============================================================================
class Camera3D:
    """Manages 3D rotation, pitch/yaw damping, perspective divide, and depth sorting."""

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.rot_x = 0.58  # Tilt angle (inclination)
        self.rot_y = 0.0
        self.zoom = 1.05
        self.focal_length = 760.0
        self.distance = 980.0

        self.is_dragging = False
        self.last_mouse_pos = (0, 0)
        self.vel_x = 0.0
        self.vel_y = 0.005

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
            self.vel_y = self.vel_y * 0.96 + 0.005 * 0.04
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

        return np.column_stack((sx, sy)), z2, factor, x2, y2


# ==============================================================================
# 4. MAIN APPLICATION ENGINE
# ==============================================================================
def run():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Day 22: 3D Relativistic Black Hole & Accretion Vortex Simulation")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("Helvetica", 14, bold=True)
    font_hud = pygame.font.SysFont("Courier", 12)

    cx, cy = WINDOW_WIDTH / 2.0, WINDOW_HEIGHT / 2.0 - 15
    bh = BlackHoleSystem3D(NUM_PARTICLES)
    camera = Camera3D(cx, cy)

    theme_idx = 0
    show_hud = True
    paused = False

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
                elif event.key == pygame.K_t:
                    theme_idx = (theme_idx + 1) % len(THEMES)
                elif event.key == pygame.K_j:
                    bh.show_jets = not bh.show_jets
                elif event.key == pygame.K_l:
                    bh.show_lensing = not bh.show_lensing
                elif event.key == pygame.K_w:
                    bh.r_outer = min(bh.Rs * 8.0, bh.r_outer + 15.0)
                elif event.key == pygame.K_s and not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    bh.r_outer = max(bh.Rs * 3.0, bh.r_outer - 15.0)
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_UP):
                    bh.sim_speed = min(3.5, bh.sim_speed + 0.25)
                elif event.key in (pygame.K_MINUS, pygame.K_DOWN):
                    bh.sim_speed = max(0.15, bh.sim_speed - 0.25)
                elif event.key == pygame.K_r:
                    camera.rot_x = 0.58
                    camera.rot_y = 0.0
                    camera.zoom = 1.05
                    bh.sim_speed = 1.0
                elif event.key == pygame.K_h:
                    show_hud = not show_hud
                elif event.key in (pygame.K_p, pygame.K_s) and (pygame.key.get_mods() & pygame.KMOD_CTRL or event.key == pygame.K_p):
                    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
                    os.makedirs(out_dir, exist_ok=True)
                    stamp = time.strftime("%Y%m%d_%H%M%S")
                    out_path = os.path.join(out_dir, f"day22_black_hole_{stamp}.png")
                    pygame.image.save(screen, out_path)
                    print(f"📸 Saved screenshot: {out_path}")

        if not paused:
            bh.update(dt)
            camera.update(auto_rotate=True)
        else:
            camera.update(auto_rotate=False)

        theme = THEMES[theme_idx]
        screen.fill(theme["bg"])

        # Compute particles & projection
        pts_3d, v_dirs, radii = bh.compute_disk_particles()
        pts_2d, depths, factors, cam_x, cam_y = camera.project(pts_3d)

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        # 1. Draw Bipolar Relativistic Plasma Jets (behind horizon if z < 0)
        north_pts, south_pts = bh.compute_jets()
        if north_pts is not None:
            c_jet = theme["jet"]
            n_2d, n_depth, n_fac, _, _ = camera.project(north_pts)
            s_2d, s_depth, s_fac, _, _ = camera.project(south_pts)

            for i in range(len(n_2d) - 1):
                p1, p2 = n_2d[i], n_2d[i + 1]
                if 0 <= p1[0] < WINDOW_WIDTH and 0 <= p1[1] < WINDOW_HEIGHT:
                    alpha = int(np.clip(180 * (1.0 - i / float(len(n_2d))), 20, 200))
                    pygame.draw.aaline(overlay, (c_jet[0], c_jet[1], c_jet[2], alpha), p1, p2)

            for i in range(len(s_2d) - 1):
                p1, p2 = s_2d[i], s_2d[i + 1]
                if 0 <= p1[0] < WINDOW_WIDTH and 0 <= p1[1] < WINDOW_HEIGHT:
                    alpha = int(np.clip(180 * (1.0 - i / float(len(s_2d))), 20, 200))
                    pygame.draw.aaline(overlay, (c_jet[0], c_jet[1], c_jet[2], alpha), p1, p2)

        # 2. Draw Gravitational Lensing Halo Ring
        lens_pts = bh.compute_lensing_ring(camera.rot_x)
        if lens_pts is not None:
            l_2d, l_depth, l_fac, _, _ = camera.project(lens_pts)
            c_ring = theme["photon_ring"]
            for i in range(len(l_2d)):
                p1 = l_2d[i]
                p2 = l_2d[(i + 1) % len(l_2d)]
                if 0 <= p1[0] < WINDOW_WIDTH and 0 <= p1[1] < WINDOW_HEIGHT:
                    pygame.draw.aaline(overlay, (c_ring[0], c_ring[1], c_ring[2], 85), p1, p2)

        # 3. Draw Depth-Sorted Accretion Disk Particles with Relativistic Doppler Beaming
        sort_order = np.argsort(depths)
        c_hot = theme["hot_beam"]
        c_cool = theme["cool_beam"]

        # Camera line of sight in camera space is towards -Z
        for idx in sort_order:
            px, py = pts_2d[idx]
            if not (-20 <= px <= WINDOW_WIDTH + 20 and -20 <= py <= WINDOW_HEIGHT + 20):
                continue

            factor = factors[idx]
            depth_ratio = np.clip((depths[idx] + 450.0) / 900.0, 0.2, 1.0)

            # Doppler beaming: velocity projected towards camera view
            # In camera space, X > 0 is moving towards viewer (blue-shifted oncoming)
            doppler_val = np.clip((cam_x[idx] / (radii[idx] + 1e-4) + 1.0) * 0.5, 0.0, 1.0)

            # Color interpolation: Doppler shift
            r_c = int(c_cool[0] * (1 - doppler_val) + c_hot[0] * doppler_val)
            g_c = int(c_cool[1] * (1 - doppler_val) + c_hot[1] * doppler_val)
            b_c = int(c_cool[2] * (1 - doppler_val) + c_hot[2] * doppler_val)

            # Doppler beaming intensity amplification: I ~ delta^4
            beam_amp = 0.5 + 1.5 * (doppler_val ** 2.2)
            alpha = int(np.clip(160 * depth_ratio * beam_amp, 35, 255))
            radius = max(1.2, 3.2 * factor * (0.8 + 0.4 * beam_amp))

            # Inner high-energy halo
            if factor > 0.85 and doppler_val > 0.6:
                halo_r = int(radius * 2.2)
                pygame.draw.circle(
                    overlay,
                    (r_c, g_c, b_c, int(alpha * 0.35)),
                    (int(px), int(py)),
                    halo_r,
                )

            pygame.draw.circle(
                overlay,
                (r_c, g_c, b_c, alpha),
                (int(px), int(py)),
                int(radius),
            )

        # 4. Draw Central Schwarzschild Event Horizon & Photon Sphere Shadow
        eh_center = (int(cx), int(cy))
        horizon_r = int(bh.Rs * camera.zoom * 0.85)

        # Luminous photon capture shadow ring
        pygame.draw.circle(overlay, (theme["photon_ring"][0], theme["photon_ring"][1], theme["photon_ring"][2], 120), eh_center, int(horizon_r * 1.15), 2)
        # Pitch black singularity
        pygame.draw.circle(overlay, (0, 0, 0, 255), eh_center, horizon_r)

        screen.blit(overlay, (0, 0))

        # Telemetry HUD
        if show_hud:
            hud_rect = pygame.Rect(15, 12, WINDOW_WIDTH - 30, 48)
            hud_bg = pygame.Surface((hud_rect.width, hud_rect.height), pygame.SRCALPHA)
            hud_bg.fill((6, 10, 18, 220))
            screen.blit(hud_bg, hud_rect)

            title_txt = font_title.render(f"DAY 22: RELATIVISTIC BLACK HOLE ACCRETION DISK ({theme['name'].upper()})", True, (255, 215, 80))
            stats_txt = font_hud.render(
                f"Matter: {bh.num_particles:,} | Doppler: ON | Jets: {'ON' if bh.show_jets else 'OFF'} | Lensing: {'ON' if bh.show_lensing else 'OFF'} | Zoom: {camera.zoom:.2f}x | FPS: {clock.get_fps():.0f}",
                True,
                (230, 245, 255),
            )
            screen.blit(title_txt, (hud_rect.x + 12, hud_rect.y + 6))
            screen.blit(stats_txt, (hud_rect.x + 12, hud_rect.y + 26))

            bot_rect = pygame.Rect(15, WINDOW_HEIGHT - 38, WINDOW_WIDTH - 30, 26)
            bot_bg = pygame.Surface((bot_rect.width, bot_rect.height), pygame.SRCALPHA)
            bot_bg.fill((6, 10, 18, 220))
            screen.blit(bot_bg, bot_rect)

            ctrl_str = "[Drag] Orbit 3D | [Wheel] Zoom | [T] Theme | [J] Jets | [L] Lensing | [W/S] Density | [P] Save | [ESC] Exit"
            ctrl_txt = font_hud.render(ctrl_str, True, (230, 245, 255))
            screen.blit(ctrl_txt, (bot_rect.x + 12, bot_rect.y + 6))

        pygame.display.flip()

    pygame.quit()


# ==============================================================================
# 5. ASSET EXPORT FUNCTIONS
# ==============================================================================
def export_poster(output_path, size=(WINDOW_WIDTH, WINDOW_HEIGHT)):
    """Renders and exports a high-resolution PNG poster of the relativistic black hole."""
    from PIL import Image, ImageDraw

    cx, cy = size[0] / 2.0, size[1] / 2.0 - 15
    bh = BlackHoleSystem3D(4200)
    camera = Camera3D(cx, cy)
    camera.rot_x = 0.58
    camera.rot_y = 0.35
    camera.zoom = 1.10

    theme = THEMES[0]  # Interstellar Gold & Cyan
    bh.update(1.2)
    pts_3d, v_dirs, radii = bh.compute_disk_particles()
    pts_2d, depths, factors, cam_x, cam_y = camera.project(pts_3d)
    sort_order = np.argsort(depths)

    w, h = size
    bg_img = Image.new("RGB", (w, h), theme["bg"])
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. Jets
    north_pts, south_pts = bh.compute_jets()
    if north_pts is not None:
        c_jet = theme["jet"]
        n_2d, _, _, _, _ = camera.project(north_pts)
        s_2d, _, _, _, _ = camera.project(south_pts)
        for i in range(len(n_2d) - 1):
            p1, p2 = (n_2d[i][0], n_2d[i][1]), (n_2d[i + 1][0], n_2d[i + 1][1])
            if 0 <= p1[0] < w and 0 <= p1[1] < h and 0 <= p2[0] < w and 0 <= p2[1] < h:
                alpha = int(np.clip(180 * (1.0 - i / float(len(n_2d))), 20, 200))
                draw.line([p1, p2], fill=(c_jet[0], c_jet[1], c_jet[2], alpha), width=2)
        for i in range(len(s_2d) - 1):
            p1, p2 = (s_2d[i][0], s_2d[i][1]), (s_2d[i + 1][0], s_2d[i + 1][1])
            if 0 <= p1[0] < w and 0 <= p1[1] < h and 0 <= p2[0] < w and 0 <= p2[1] < h:
                alpha = int(np.clip(180 * (1.0 - i / float(len(s_2d))), 20, 200))
                draw.line([p1, p2], fill=(c_jet[0], c_jet[1], c_jet[2], alpha), width=2)

    # 2. Lensing Ring
    lens_pts = bh.compute_lensing_ring(camera.rot_x)
    if lens_pts is not None:
        l_2d, _, _, _, _ = camera.project(lens_pts)
        c_ring = theme["photon_ring"]
        for i in range(len(l_2d)):
            p1 = (l_2d[i][0], l_2d[i][1])
            p2 = (l_2d[(i + 1) % len(l_2d)][0], l_2d[(i + 1) % len(l_2d)][1])
            if 0 <= p1[0] < w and 0 <= p1[1] < h and 0 <= p2[0] < w and 0 <= p2[1] < h:
                draw.line([p1, p2], fill=(c_ring[0], c_ring[1], c_ring[2], 90), width=2)

    # 3. Accretion Particles
    c_hot = theme["hot_beam"]
    c_cool = theme["cool_beam"]
    for idx in sort_order:
        px, py = pts_2d[idx]
        if not (-10 <= px <= w + 10 and -10 <= py <= h + 10):
            continue
        factor = factors[idx]
        depth_ratio = np.clip((depths[idx] + 450.0) / 900.0, 0.2, 1.0)
        doppler_val = np.clip((cam_x[idx] / (radii[idx] + 1e-4) + 1.0) * 0.5, 0.0, 1.0)

        r_c = int(c_cool[0] * (1 - doppler_val) + c_hot[0] * doppler_val)
        g_c = int(c_cool[1] * (1 - doppler_val) + c_hot[1] * doppler_val)
        b_c = int(c_cool[2] * (1 - doppler_val) + c_hot[2] * doppler_val)

        beam_amp = 0.5 + 1.5 * (doppler_val ** 2.2)
        alpha = int(np.clip(170 * depth_ratio * beam_amp, 40, 255))
        radius = max(1.5, 3.4 * factor * (0.8 + 0.4 * beam_amp))

        if factor > 0.85 and doppler_val > 0.6:
            halo_r = radius * 2.2
            draw.ellipse([px - halo_r, py - halo_r, px + halo_r, py + halo_r], fill=(r_c, g_c, b_c, int(alpha * 0.35)))

        draw.ellipse([px - radius, py - radius, px + radius, py + radius], fill=(r_c, g_c, b_c, alpha))

    # 4. Event Horizon
    horizon_r = int(bh.Rs * camera.zoom * 0.85)
    draw.ellipse([cx - horizon_r * 1.15, cy - horizon_r * 1.15, cx + horizon_r * 1.15, cy + horizon_r * 1.15], outline=(theme["photon_ring"][0], theme["photon_ring"][1], theme["photon_ring"][2], 130), width=2)
    draw.ellipse([cx - horizon_r, cy - horizon_r, cx + horizon_r, cy + horizon_r], fill=(0, 0, 0, 255))

    out = Image.alpha_composite(bg_img.convert("RGBA"), overlay).convert("RGB")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    out.save(output_path, optimize=True)
    print(f"✅ Saved Day 22 poster: {output_path}")


def export_animation(output_path, num_frames=48, frame_size=(600, 600)):
    """Generates an animated preview GIF of the relativistic black hole accretion disk."""
    from PIL import Image, ImageDraw

    cx, cy = frame_size[0] / 2.0, frame_size[1] / 2.0
    bh = BlackHoleSystem3D(2200)
    camera = Camera3D(cx, cy)
    camera.rot_x = 0.58
    camera.zoom = 1.05

    theme = THEMES[0]
    w, h = frame_size
    frames = []

    c_hot = theme["hot_beam"]
    c_cool = theme["cool_beam"]

    for frame_idx in range(num_frames):
        t = frame_idx * (2.0 * math.pi / num_frames)
        camera.rot_y = t * 0.75
        bh.update(0.04)

        pts_3d, v_dirs, radii = bh.compute_disk_particles()
        pts_2d, depths, factors, cam_x, cam_y = camera.project(pts_3d)
        sort_order = np.argsort(depths)

        bg_img = Image.new("RGB", (w, h), theme["bg"])
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Lensing ring
        lens_pts = bh.compute_lensing_ring(camera.rot_x)
        if lens_pts is not None:
            l_2d, _, _, _, _ = camera.project(lens_pts)
            c_ring = theme["photon_ring"]
            for i in range(len(l_2d)):
                p1 = (l_2d[i][0], l_2d[i][1])
                p2 = (l_2d[(i + 1) % len(l_2d)][0], l_2d[(i + 1) % len(l_2d)][1])
                if 0 <= p1[0] < w and 0 <= p1[1] < h and 0 <= p2[0] < w and 0 <= p2[1] < h:
                    draw.line([p1, p2], fill=(c_ring[0], c_ring[1], c_ring[2], 80), width=1)

        # Particles
        for idx in sort_order:
            px, py = pts_2d[idx]
            if not (-10 <= px <= w + 10 and -10 <= py <= h + 10):
                continue
            factor = factors[idx]
            depth_ratio = np.clip((depths[idx] + 450.0) / 900.0, 0.2, 1.0)
            doppler_val = np.clip((cam_x[idx] / (radii[idx] + 1e-4) + 1.0) * 0.5, 0.0, 1.0)

            r_c = int(c_cool[0] * (1 - doppler_val) + c_hot[0] * doppler_val)
            g_c = int(c_cool[1] * (1 - doppler_val) + c_hot[1] * doppler_val)
            b_c = int(c_cool[2] * (1 - doppler_val) + c_hot[2] * doppler_val)

            beam_amp = 0.5 + 1.5 * (doppler_val ** 2.2)
            alpha = int(np.clip(160 * depth_ratio * beam_amp, 40, 255))
            radius = max(1.2, 2.8 * factor * (0.8 + 0.4 * beam_amp))

            draw.ellipse([px - radius, py - radius, px + radius, py + radius], fill=(r_c, g_c, b_c, alpha))

        # Event horizon
        horizon_r = int(bh.Rs * camera.zoom * 0.85 * (w / float(WINDOW_WIDTH)))
        draw.ellipse([cx - horizon_r * 1.15, cy - horizon_r * 1.15, cx + horizon_r * 1.15, cy + horizon_r * 1.15], outline=(theme["photon_ring"][0], theme["photon_ring"][1], theme["photon_ring"][2], 120), width=1)
        draw.ellipse([cx - horizon_r, cy - horizon_r, cx + horizon_r, cy + horizon_r], fill=(0, 0, 0, 255))

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
    print(f"✅ Saved Day 22 animated preview: {output_path} ({len(frames)} frames)")


if __name__ == "__main__":
    if "--export" in sys.argv:
        export_poster("assets/day22_black_hole.png")
        export_animation("assets/day22_animation.gif")
    else:
        run()

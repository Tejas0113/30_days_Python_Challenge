"""
Day 19: 3D Kinetic Phyllotaxis Spiral Galaxy
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
Core mathematical engine for 3D kinetic phyllotaxis spiral galaxy simulation
based on the Golden Ratio (phi = 1.6180339...) and the Golden Angle (137.507764°).

Features:
- Mathematical core supporting 4 distinct 3D spiral topologies:
    1. Fibonacci Sunflower Galaxy (Golden Angle phyllotaxis with transverse wave undulation)
    2. 3D Nautilus Shell Vortex (Logarithmic spiral expanding along 3D Z-axis)
    3. Fermat's Dual-Chiral Vortex (Counter-rotating dual spiral arms)
    4. Toroidal Phyllotaxis Knot (Spiral wrapped on surface of a 3D donut torus)
- 3D perspective projection and depth-sorting pipeline
- Chromatic themes and real-time kinetic rotation
"""

import math
import os
import sys
import time

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

WINDOW_WIDTH = 920
WINDOW_HEIGHT = 920
FPS = 60

GOLDEN_ANGLE = 137.50776405003785 * (math.pi / 180.0)
NUM_NODES = 2200

THEMES = [
    {
        "name": "Cyberpunk Neon",
        "bg": (8, 10, 18),
        "primary": (255, 45, 130),
        "secondary": (0, 245, 255),
        "tertiary": (255, 205, 40),
        "filament": (70, 160, 220, 60),
    },
    {
        "name": "Electric Cyan & Gold",
        "bg": (6, 12, 20),
        "primary": (40, 230, 255),
        "secondary": (255, 210, 65),
        "tertiary": (160, 245, 180),
        "filament": (50, 190, 220, 55),
    },
]


class PhyllotaxisGalaxy3D:
    def __init__(self, num_nodes=NUM_NODES):
        self.num_nodes = num_nodes
        self.mode = 1
        self.wave_amplitude = 45.0
        self.wave_freq = 2.4
        self.rotation_speed = 0.012
        self.indices = np.arange(self.num_nodes, dtype=float)

    def compute_positions(self, t):
        n = self.indices
        if self.mode == 1:
            theta = n * GOLDEN_ANGLE
            r = 14.5 * np.sqrt(n)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = self.wave_amplitude * np.sin(0.018 * r - t * self.wave_freq) * (1.0 + 0.3 * np.cos(theta * 2.0))
            return np.column_stack((x, y, z))
        elif self.mode == 2:
            theta = n * 0.065
            r = 18.0 * np.exp(0.0017 * n)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = (n - self.num_nodes / 2.0) * 0.38 + self.wave_amplitude * 0.6 * np.sin(theta * 2.0 - t * 2.0)
            return np.column_stack((x, y, z))
        elif self.mode == 3:
            sign = np.where(n % 2 == 0, 1.0, -1.0)
            theta = n * GOLDEN_ANGLE * sign + (t * 0.8 * sign)
            r = 13.8 * np.sqrt(n)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = self.wave_amplitude * 1.2 * np.sin(n * 0.04 - t * 3.0) * sign
            return np.column_stack((x, y, z))
        else:
            R_torus = 220.0
            r_tube = 75.0 + self.wave_amplitude * 0.5 * np.sin(n * 0.05 + t * 2.5)
            u = n * GOLDEN_ANGLE
            v = n * 0.035 + t * 0.6
            x = (R_torus + r_tube * np.cos(v)) * np.cos(u)
            y = (R_torus + r_tube * np.cos(v)) * np.sin(u)
            z = r_tube * np.sin(v)
            return np.column_stack((x, y, z))


class Camera3D:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.rot_x = 0.55
        self.rot_y = 0.0
        self.zoom = 1.05
        self.focal_length = 750.0
        self.distance = 950.0

    def project(self, points):
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


def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    galaxy = PhyllotaxisGalaxy3D()
    camera = Camera3D(WINDOW_WIDTH / 2.0, WINDOW_HEIGHT / 2.0)
    running = True
    t = 0.0
    while running:
        dt = clock.tick(FPS) / 1000.0
        t += dt
        camera.rot_y += 0.008
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.fill(THEMES[0]["bg"])
        pts, depths, factors = camera.project(galaxy.compute_positions(t))
        for p in pts:
            pygame.draw.circle(screen, THEMES[0]["primary"], (int(p[0]), int(p[1])), 2)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    run()

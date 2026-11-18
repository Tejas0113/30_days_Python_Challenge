"""
Day 22: 3D Relativistic Black Hole & Accretion Vortex Simulation
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
Relativistic Keplerian accretion disk simulation with Doppler beaming intensity
amplification (I ~ delta^4) and blue/redshift spectral coloring.
"""

import math
import os
import random
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
NUM_PARTICLES = 3600
EVENT_HORIZON_RADIUS = 65.0

THEMES = [
    {
        "name": "Interstellar Gold & Cyan",
        "bg": (4, 6, 12),
        "horizon": (0, 0, 0),
        "hot_beam": (100, 240, 255),
        "cool_beam": (255, 120, 40),
        "jet": (120, 220, 255),
        "photon_ring": (255, 230, 160),
    },
]


class BlackHoleSystem3D:
    def __init__(self, num_particles=NUM_PARTICLES):
        self.num_particles = num_particles
        self.Rs = EVENT_HORIZON_RADIUS
        self.r_inner = self.Rs * 1.5
        self.r_outer = self.Rs * 5.2
        self.sim_speed = 1.0
        self.time = 0.0

        np.random.seed(42)
        u = np.random.uniform(0.0, 1.0, self.num_particles)
        self.radii = self.r_inner + (self.r_outer - self.r_inner) * (u ** 1.8)
        self.angles = np.random.uniform(0.0, 2.0 * math.pi, self.num_particles)
        self.z_offsets = np.random.normal(0.0, 1.0, self.num_particles) * (self.radii * 0.04)
        self.ang_vels = 28.0 / (self.radii ** 1.25)

    def update(self, dt):
        self.time += dt * self.sim_speed
        self.angles += self.ang_vels * dt * self.sim_speed

    def compute_disk_particles(self):
        xs = self.radii * np.cos(self.angles)
        ys = self.radii * np.sin(self.angles)
        zs = self.z_offsets
        v_dirs = np.column_stack((-np.sin(self.angles), np.cos(self.angles), np.zeros_like(self.angles)))
        return np.column_stack((xs, ys, zs)), v_dirs, self.radii


def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    bh = BlackHoleSystem3D()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        bh.update(dt)
        screen.fill(THEMES[0]["bg"])
        pts_3d, _, _ = bh.compute_disk_particles()
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        for p in pts_3d[::2]:
            pygame.draw.circle(screen, THEMES[0]["cool_beam"], (int(cx + p[0]), int(cy + p[1] * 0.4)), 1)
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy), int(bh.Rs))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    run()

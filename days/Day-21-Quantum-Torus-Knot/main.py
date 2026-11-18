"""
Day 21: 3D Quantum Torus Knot & Hopf Fibration Art
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
Core mathematical engine for 3D (p, q) torus knot topology and Hopf fibration.
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
NUM_NODES = 2400

THEMES = [
    {
        "name": "Cyberpunk Neon",
        "bg": (8, 10, 18),
        "primary": (255, 45, 130),
        "secondary": (0, 245, 255),
        "tertiary": (255, 205, 40),
        "filament": (70, 170, 230, 60),
    },
]


class TorusKnot3D:
    def __init__(self, num_nodes=NUM_NODES):
        self.num_nodes = num_nodes
        self.mode = 1
        self.R = 210.0
        self.r = 85.0
        self.indices = np.arange(self.num_nodes, dtype=float)

    def compute_positions(self, t):
        n = self.indices
        total = float(self.num_nodes)
        p, q = 2, 3
        phi = (n / total) * 2.0 * math.pi + t * 0.4
        r_eff = self.R + self.r * np.cos(q * phi)
        x = r_eff * np.cos(p * phi)
        y = r_eff * np.sin(p * phi)
        z = -self.r * np.sin(q * phi)
        return np.column_stack((x, y, z))


def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    knot = TorusKnot3D()
    running = True
    t = 0.0
    while running:
        dt = clock.tick(FPS) / 1000.0
        t += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(THEMES[0]["bg"])
        pts = knot.compute_positions(t)
        for p in pts:
            sx = int(WINDOW_WIDTH / 2.0 + p[0])
            sy = int(WINDOW_HEIGHT / 2.0 + p[1])
            pygame.draw.circle(screen, THEMES[0]["primary"], (sx, sy), 2)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    run()

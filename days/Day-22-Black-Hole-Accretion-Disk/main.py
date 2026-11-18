"""
Day 22: 3D Relativistic Black Hole & Accretion Vortex Simulation
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
Core relativistic black hole physics model with Schwarzschild event horizon
and photon sphere capture boundary.
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
    def __init__(self):
        self.Rs = EVENT_HORIZON_RADIUS
        self.r_inner = self.Rs * 1.5
        self.r_outer = self.Rs * 5.2
        self.sim_speed = 1.0


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
        screen.fill(THEMES[0]["bg"])
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        pygame.draw.circle(screen, THEMES[0]["photon_ring"], (cx, cy), int(bh.Rs * 1.15), 2)
        pygame.draw.circle(screen, (0, 0, 0), (cx, cy), int(bh.Rs))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    run()

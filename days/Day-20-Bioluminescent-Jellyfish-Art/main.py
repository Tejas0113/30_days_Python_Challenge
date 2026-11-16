"""
Day 20: Bioluminescent Deep-Sea Jellyfish Generative Art
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
Procedural anatomy and Verlet-integrated tentacle physics engine for
deep-sea bioluminescent jellyfish simulation in Pygame.

Features:
- Translucent pulsating bell dome with asymmetric locomotion propulsion
- Multi-segment Verlet-integrated spring tentacles with hydrodynamic water drag
- Frilled oral arms and cloverleaf bioluminescent organ cores (rhopalia)
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
]


class Tentacle:
    def __init__(self, start_x, start_y, length=24, seg_len=7.0):
        self.num_segs = length
        self.seg_len = seg_len
        self.points = [[start_x, start_y + i * seg_len] for i in range(self.num_segs)]
        self.prev_points = [[p[0], p[1]] for p in self.points]

    def update(self, anchor_x, anchor_y, current_vx=0.0, current_vy=0.0):
        self.points[0] = [anchor_x, anchor_y]
        for i in range(1, self.num_segs):
            x, y = self.points[i]
            px, py = self.prev_points[i]
            vx = (x - px) * 0.91 + current_vx * 0.25
            vy = (y - py) * 0.91 + 0.18 + current_vy * 0.25
            self.prev_points[i] = [x, y]
            self.points[i] = [x + vx, y + vy]

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
    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.base_scale = scale
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-0.5, -0.1)
        self.phase = random.uniform(0, 2 * math.pi)
        self.pulse_speed = random.uniform(1.6, 2.2)
        self.radius = 42.0 * self.base_scale
        self.height = 36.0 * self.base_scale
        self.tentacles = [
            Tentacle(self.x, self.y, length=random.randint(18, 30), seg_len=7.0 * scale)
            for _ in range(10)
        ]
        self.oral_arms = [
            Tentacle(self.x, self.y, length=random.randint(14, 22), seg_len=6.0 * scale)
            for _ in range(4)
        ]

    def update(self, dt):
        self.phase += dt * self.pulse_speed
        pulse_raw = math.sin(self.phase)
        if pulse_raw > 0:
            thrust = 0.55 * math.pow(pulse_raw, 1.8) * self.base_scale
            self.vy -= thrust * 0.08
        self.vx *= 0.985
        self.vy = self.vy * 0.985 + 0.03
        self.x += self.vx
        self.y += self.vy

        cur_w = self.radius * (1.0 - 0.22 * math.sin(self.phase))
        cur_h = self.height * (1.0 + 0.35 * math.sin(self.phase))
        for i, ten in enumerate(self.tentacles):
            t_ratio = i / float(len(self.tentacles) - 1)
            angle = math.pi * (0.08 + 0.84 * t_ratio)
            rx = self.x + cur_w * math.cos(angle)
            ry = self.y + cur_h * 0.25 + 6.0 * math.sin(angle)
            ten.update(rx, ry, self.vx * 0.6, self.vy * 0.6)


def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    jelly = Jellyfish(WINDOW_WIDTH / 2.0, WINDOW_HEIGHT / 2.0, scale=1.3)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        jelly.update(dt)
        screen.fill(THEMES[0]["bg_bot"])
        pygame.draw.circle(screen, THEMES[0]["bell"], (int(jelly.x), int(jelly.y)), int(jelly.radius))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    run()

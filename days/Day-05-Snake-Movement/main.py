"""
Day 05: Interactive Predatory Snake Movement
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A fluid, bio-inspired predatory snake simulation featuring:
- Inverse Kinematics spine following with segment distance constraints.
- Proximity-based predatory physics: cruising stalk at a distance (> 350px),
  accelerating into a rapid strike surge (up to 16 px/frame) as it nears the cursor.
- Organic transverse traveling wave slither with velocity-linked undulation frequency.
- Anatomical tapering from wedge viper head down to tail tip with glowing scales,
  golden reptile eyes tracking the mouse, and a darting forked tongue.
- Dual-engine architecture: High-performance 60 FPS Pygame mode with an automatic
  zero-dependency Tkinter Canvas fallback.
"""

import math
import sys
import random

# Color Themes: (Head RGB, Tail RGB, Dorsal Highlight, Eye Iris)
THEMES = [
    {
        "name": "Emerald Viper",
        "head": (0, 255, 140),
        "tail": (0, 180, 220),
        "dorsal": (220, 255, 240),
        "eye": (255, 215, 0),
        "bg": (11, 15, 22),
    },
    {
        "name": "Crimson Coral",
        "head": (255, 45, 85),
        "tail": (255, 140, 0),
        "dorsal": (255, 220, 230),
        "eye": (255, 255, 255),
        "bg": (18, 10, 16),
    },
    {
        "name": "Cyberpunk Neon",
        "head": (255, 0, 220),
        "tail": (0, 240, 255),
        "dorsal": (255, 255, 255),
        "eye": (0, 255, 170),
        "bg": (10, 10, 20),
    },
    {
        "name": "Arctic Frost",
        "head": (140, 220, 255),
        "tail": (60, 110, 240),
        "dorsal": (240, 250, 255),
        "eye": (255, 220, 100),
        "bg": (8, 14, 24),
    }
]


class SnakePhysics:
    """Core Inverse Kinematics and predatory proximity physics."""
    def __init__(self, x, y, num_segments=48, seg_len=9):
        self.num_segments = num_segments
        self.seg_len = seg_len
        self.positions = [[x - i * seg_len, y] for i in range(num_segments)]
        self.angles = [0.0] * num_segments
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 0.0
        self.wave_phase = 0.0
        self.state = "STALKING"
        self.dist_to_target = 0.0

    def update(self, target_x, target_y):
        head_x, head_y = self.positions[0]
        dx = target_x - head_x
        dy = target_y - head_y
        dist = math.hypot(dx, dy)
        self.dist_to_target = dist

        # Proximity-based predatory speed profile:
        # Distance > 350px: Stalking cruising speed (~3.6 px/frame)
        # Distance 20px - 350px: Strike surge! Closer = exponential acceleration up to 16.0 px/frame!
        # Distance < 15px: Smooth deceleration to coil around cursor
        if dist > 350:
            desired_speed = 3.6 + 0.6 * math.sin(self.wave_phase * 0.5)
            self.state = "STALKING (Away)"
        elif dist > 15:
            proximity = (350.0 - dist) / 335.0  # 0.0 (far) to 1.0 (very close)
            # Exponential strike burst: surges up to 16.0 px/frame!
            desired_speed = 3.6 + 12.4 * (proximity ** 1.5)
            self.state = "STRIKING ⚡ (Close)"
        else:
            desired_speed = (dist / 15.0) * 3.0
            self.state = "COILING (Reached)"

        # Smooth steering with inertia
        if dist > 1.0:
            target_angle = math.atan2(dy, dx)
            desired_vx = math.cos(target_angle) * desired_speed
            desired_vy = math.sin(target_angle) * desired_speed
            turn_ease = 0.14 if dist > 200 else 0.22  # sharper turn when striking
            self.vx += (desired_vx - self.vx) * turn_ease
            self.vy += (desired_vy - self.vy) * turn_ease
        else:
            self.vx *= 0.8
            self.vy *= 0.8

        self.speed = math.hypot(self.vx, self.vy)
        new_head_x = head_x + self.vx
        new_head_y = head_y + self.vy
        self.positions[0] = [new_head_x, new_head_y]

        if self.speed > 0.05:
            self.angles[0] = math.atan2(self.vy, self.vx)

        # Slither wave advances proportionally to actual movement
        self.wave_phase += self.speed * 0.075

        # Inverse Kinematics constraint solver for body segments
        for i in range(1, self.num_segments):
            prev_x, prev_y = self.positions[i - 1]
            curr_x, curr_y = self.positions[i]
            seg_dx = prev_x - curr_x
            seg_dy = prev_y - curr_y
            seg_dist = math.hypot(seg_dx, seg_dy)

            if seg_dist > 0.001:
                angle = math.atan2(seg_dy, seg_dx)
                self.angles[i] = angle
                self.positions[i] = [
                    prev_x - math.cos(angle) * self.seg_len,
                    prev_y - math.sin(angle) * self.seg_len
                ]


# ==============================================================================
# PYGAME IMPLEMENTATION (Primary 60 FPS Engine)
# ==============================================================================
def run_pygame():
    import pygame

    pygame.init()
    WIDTH, HEIGHT = 1100, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Day 05: Interactive Predatory Snake - 30 Days Python Challenge")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 14, bold=True)
    title_font = pygame.font.SysFont("sans-serif", 18, bold=True)

    snake = SnakePhysics(WIDTH // 2, HEIGHT // 2, num_segments=52, seg_len=10)
    theme_idx = 0
    paused = False

    # Ambient floating dust particles for atmospheric depth
    dust = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), "r": random.randint(1, 2), "alpha": random.randint(20, 70)} for _ in range(35)]

    running = True
    while running:
        theme = THEMES[theme_idx]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_c:
                    theme_idx = (theme_idx + 1) % len(THEMES)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Click triggers sudden sprint lunge
                snake.vx *= 1.8
                snake.vy *= 1.8

        target_x, target_y = pygame.mouse.get_pos()

        if not paused:
            snake.update(target_x, target_y)

        # ----------------- RENDER -----------------
        screen.fill(theme["bg"])

        # Draw ambient dust particles
        for p in dust:
            p["y"] = (p["y"] - 0.2) % HEIGHT
            pygame.draw.circle(screen, (100, 130, 160), (int(p["x"]), int(p["y"])), p["r"])

        # Target Bait Pulse Reticle
        pulse = (math.sin(pygame.time.get_ticks() * 0.008) + 1.0) * 0.5
        bait_r = int(9 + pulse * 4)
        pygame.draw.circle(screen, (255, 60, 100), (target_x, target_y), bait_r, 2)
        pygame.draw.circle(screen, (255, 255, 255), (target_x, target_y), 3)

        # Draw Snake Body from Tail to Head
        for i in range(snake.num_segments - 1, 0, -1):
            px, py = snake.positions[i]
            body_ratio = i / float(snake.num_segments)

            # Transverse wave displacement (organic slither)
            normal = snake.angles[i] + math.pi / 2
            amp = math.sin(body_ratio * math.pi) * 8.0
            wave = math.sin(snake.wave_phase - i * 0.35) * amp
            wx = px + math.cos(normal) * wave
            wy = py + math.sin(normal) * wave

            # Radius tapering: thickest at neck/torso, slender at tail tip
            radius = max(3, int(18 * math.sqrt(1.0 - (body_ratio ** 1.3))))

            # Chromatic interpolation from head to tail
            h_col = theme["head"]
            t_col = theme["tail"]
            r_c = int(h_col[0] * (1 - body_ratio) + t_col[0] * body_ratio)
            g_c = int(h_col[1] * (1 - body_ratio) + t_col[1] * body_ratio)
            b_c = int(h_col[2] * (1 - body_ratio) + t_col[2] * body_ratio)

            # Outer glow aura
            glow_c = (max(0, r_c - 60), max(0, g_c - 60), max(0, b_c - 60))
            pygame.draw.circle(screen, glow_c, (int(wx), int(wy)), radius + 2)

            # Main scale disk
            pygame.draw.circle(screen, (r_c, g_c, b_c), (int(wx), int(wy)), radius)

            # Dorsal spine highlight dot
            if radius > 5:
                pygame.draw.circle(screen, theme["dorsal"], (int(wx), int(wy)), max(1, radius // 4))

        # Draw Sculpted Viper Head
        hx, hy = snake.positions[0]
        h_angle = snake.angles[0]
        head_radius = 21

        # Head base
        pygame.draw.circle(screen, theme["head"], (int(hx), int(hy)), head_radius)

        # Viper eyes (perpendicular to heading)
        eye_offset = 9
        eye_forward = 8
        e_norm = h_angle + math.pi / 2

        for side in (-1, 1):
            ex = hx + math.cos(h_angle) * eye_forward + math.cos(e_norm) * (side * eye_offset)
            ey = hy + math.sin(h_angle) * eye_forward + math.sin(e_norm) * (side * eye_offset)
            # Eye socket
            pygame.draw.circle(screen, (15, 20, 25), (int(ex), int(ey)), 5)
            # Glowing iris
            pygame.draw.circle(screen, theme["eye"], (int(ex), int(ey)), 4)
            # Slit pupil oriented towards target
            pygame.draw.circle(screen, (0, 0, 0), (int(ex), int(ey)), 2)

        # Darting forked red tongue
        if (int(snake.wave_phase * 2) % 12) < 4:
            tx = hx + math.cos(h_angle) * (head_radius + 14)
            ty = hy + math.sin(h_angle) * (head_radius + 14)
            pygame.draw.line(screen, (255, 45, 60), (hx, hy), (tx, ty), 2)
            # Fork tips
            f1_x = tx + math.cos(h_angle + 0.45) * 7
            f1_y = ty + math.sin(h_angle + 0.45) * 7
            f2_x = tx + math.cos(h_angle - 0.45) * 7
            f2_y = ty + math.sin(h_angle - 0.45) * 7
            pygame.draw.line(screen, (255, 45, 60), (tx, ty), (f1_x, f1_y), 2)
            pygame.draw.line(screen, (255, 45, 60), (tx, ty), (f2_x, f2_y), 2)

        # ----------------- HUD OVERLAY -----------------
        hud_bg = pygame.Surface((310, 115), pygame.SRCALPHA)
        hud_bg.fill((10, 15, 25, 200))
        screen.blit(hud_bg, (15, 15))
        pygame.draw.rect(screen, (0, 240, 255), (15, 15, 310, 115), 1, border_radius=4)

        t_surf = title_font.render("🐍 DAY 05: PREDATORY SNAKE", True, (0, 240, 255))
        screen.blit(t_surf, (25, 22))

        st_col = (255, 70, 90) if "STRIKING" in snake.state else ((0, 255, 140) if "STALKING" in snake.state else (255, 215, 0))
        lines = [
            f"State:    {snake.state}",
            f"Distance: {int(snake.dist_to_target)} px",
            f"Speed:    {snake.speed:.1f} px/frame",
            f"Theme:    {theme['name']} (Press C to switch)",
        ]
        for l_idx, line_txt in enumerate(lines):
            col = st_col if l_idx == 0 else (200, 220, 240)
            txt_surf = font.render(line_txt, True, col)
            screen.blit(txt_surf, (25, 48 + l_idx * 18))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# ==============================================================================
# TKINTER FALLBACK IMPLEMENTATION (Zero External Dependencies)
# ==============================================================================
def run_tkinter():
    import tkinter as tk

    root = tk.Tk()
    root.title("Day 05: Interactive Predatory Snake - Tkinter Fallback")
    WIDTH, HEIGHT = 1000, 700
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.configure(bg="#0b0f16")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0b0f16", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    snake = SnakePhysics(WIDTH // 2, HEIGHT // 2, num_segments=45, seg_len=9)
    target = [WIDTH // 2, HEIGHT // 2]
    theme_idx = [0]

    def on_mouse_move(event):
        target[0] = event.x
        target[1] = event.y

    def on_key(event):
        if event.keysym in ("c", "C"):
            theme_idx[0] = (theme_idx[0] + 1) % len(THEMES)
        elif event.keysym == "Escape":
            root.destroy()

    canvas.bind("<Motion>", on_mouse_move)
    root.bind("<Key>", on_key)

    def loop():
        snake.update(target[0], target[1])
        canvas.delete("all")
        theme = THEMES[theme_idx[0]]

        # Target reticle
        tx, ty = target
        canvas.create_oval(tx - 10, ty - 10, tx + 10, ty + 10, outline="#ff3c5a", width=2)
        canvas.create_oval(tx - 3, ty - 3, tx + 3, ty + 3, fill="#ffffff", outline="")

        # Draw snake body
        for i in range(snake.num_segments - 1, 0, -1):
            px, py = snake.positions[i]
            body_ratio = i / float(snake.num_segments)
            normal = snake.angles[i] + math.pi / 2
            amp = math.sin(body_ratio * math.pi) * 7.0
            wave = math.sin(snake.wave_phase - i * 0.35) * amp
            wx = px + math.cos(normal) * wave
            wy = py + math.sin(normal) * wave
            radius = max(3, int(16 * math.sqrt(1.0 - (body_ratio ** 1.3))))

            h_col = theme["head"]
            t_col = theme["tail"]
            r_c = int(h_col[0] * (1 - body_ratio) + t_col[0] * body_ratio)
            g_c = int(h_col[1] * (1 - body_ratio) + t_col[1] * body_ratio)
            b_c = int(h_col[2] * (1 - body_ratio) + t_col[2] * body_ratio)
            hex_col = f"#{r_c:02x}{g_c:02x}{b_c:02x}"

            canvas.create_oval(wx - radius, wy - radius, wx + radius, wy + radius, fill=hex_col, outline="")

        # Head
        hx, hy = snake.positions[0]
        h_col = f"#{theme['head'][0]:02x}{theme['head'][1]:02x}{theme['head'][2]:02x}"
        canvas.create_oval(hx - 18, hy - 18, hx + 18, hy + 18, fill=h_col, outline="")

        # Eyes
        h_ang = snake.angles[0]
        e_norm = h_ang + math.pi / 2
        for side in (-1, 1):
            ex = hx + math.cos(h_ang) * 8 + math.cos(e_norm) * (side * 8)
            ey = hy + math.sin(h_ang) * 8 + math.sin(e_norm) * (side * 8)
            canvas.create_oval(ex - 4, ey - 4, ex + 4, ey + 4, fill="#ffd700", outline="#000000")
            canvas.create_oval(ex - 2, ey - 2, ex + 2, ey + 2, fill="#000000", outline="")

        # HUD Text
        info = f"Day 05: Predatory Snake | State: {snake.state} | Dist: {int(snake.dist_to_target)}px | Speed: {snake.speed:.1f}px | [C] Theme"
        canvas.create_text(20, 25, anchor="w", text=info, fill="#00f0ff", font=("Monospace", 11, "bold"))

        root.after(16, loop)

    loop()
    root.mainloop()


def main():
    try:
        import pygame
        run_pygame()
    except (ImportError, Exception):
        print("💡 Pygame not detected or encountered display issue. Running high-performance Tkinter mode...")
        run_tkinter()


if __name__ == "__main__":
    main()

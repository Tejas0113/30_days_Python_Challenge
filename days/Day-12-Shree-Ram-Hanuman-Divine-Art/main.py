"""
Day 12: Lord Shree Ram & Hanuman Ji - Divine Art Animation
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A cinematic and devotional creative-coding animation built with Python, Pygame, and OpenCV.
Sequentially draws the sacred silhouette of Lord Shree Ram and Lord Hanuman Ji with a glowing
golden pen tip, smoothly transitions into high-contrast solid silhouettes, and reveals radiant
edge-to-edge golden sunburst rays along with a seamless, flowing horizontal 'JAI SHRI RAM' mantra stream.

Reference & Credits:
Based on the divine art by Gracyclub:
https://github.com/Gracyclub/Shree-Ram-Hanuman-Divine-art
"""

import math
import os
import sys
import cv2
import numpy as np
import pygame

# 1. Configuration & Parameters
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "ram_hanuman.jpg"

# Look for image in script directory first, then fallback to current working directory
IMAGE_PATH = os.path.join(SCRIPT_DIR, IMAGE_NAME)
if not os.path.exists(IMAGE_PATH):
    IMAGE_PATH = IMAGE_NAME

WINDOW_WIDTH = 540              # Optimal 9:16 portrait display width
DRAW_SPEED = 70                 # Fast sketch drawing speed (points per frame)
STROKE_COLOR = (255, 215, 60)   # Golden outline for live drawing
CURSOR_COLOR = (255, 255, 240)  # Glowing pen tip
MANTRA_TEXT = "  JAI SHRI RAM  "


def load_and_preprocess(image_path, width):
    """Loads image, calculates scaled dimensions, and extracts contours and silhouette mask."""
    src_bgr = cv2.imread(image_path)
    if src_bgr is None:
        print(f"Error: Could not load image from '{image_path}'")
        sys.exit(1)

    orig_h, orig_w, _ = src_bgr.shape
    height = int(width * (orig_h / orig_w))

    resized = cv2.resize(src_bgr, (width, height))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 7, 75, 75)

    # Contours for sequential line drawing
    edges = cv2.Canny(blurred, 35, 120)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=lambda c: cv2.arcLength(c, False), reverse=True)

    drawing_paths = []
    for c in contours:
        if len(c) > 25:
            path = [(int(pt[0][0]), int(pt[0][1])) for pt in c]
            drawing_paths.append(path)

    # Separate central figures cleanly
    _, raw_mask = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY_INV)

    # Connected components analysis to isolate only main deities
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(raw_mask)
    isolated_mask = np.zeros_like(raw_mask)

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        cx, cy = centroids[i]
        if area > 400 and (cy > height * 0.25):
            isolated_mask[labels == i] = 255

    # Completely fill all holes inside body (ensures Lord Ram's torso is solid)
    contours_fill, _ = cv2.findContours(isolated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    solid_mask = np.zeros_like(isolated_mask)
    cv2.drawContours(solid_mask, contours_fill, -1, 255, thickness=cv2.FILLED)

    # Create an RGBA Surface for Solid Pure Black Silhouette
    fill_rgba = np.zeros((height, width, 4), dtype=np.uint8)
    fill_rgba[:, :] = [5, 3, 2, 0]  # Deep jet-black tone
    fill_rgba[:, :, 3] = solid_mask

    return height, drawing_paths, fill_rgba


def main():
    # 2. Extract Clean Outlines and Completely Solid Silhouette
    window_height, drawing_paths, fill_rgba = load_and_preprocess(IMAGE_PATH, WINDOW_WIDTH)

    # 3. Setup Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, window_height))
    pygame.display.set_caption("🚩 Lord Shree Ram & Hanuman Ji - Divine Light & Silhouette | Day 12")
    clock = pygame.time.Clock()

    try:
        font = pygame.font.SysFont("arial", 16, bold=True)
    except Exception:
        font = pygame.font.Font(None, 16)

    rendered_unit = font.render(MANTRA_TEXT, True, (25, 15, 8))
    unit_w, unit_h = rendered_unit.get_size()
    row_spacing = unit_h + 14
    total_rows = (window_height // row_spacing) + 2

    # Surfaces for layers
    drawn_layer = pygame.Surface((WINDOW_WIDTH, window_height), pygame.SRCALPHA)
    solid_fill_surface = pygame.image.frombuffer(
        fill_rgba.tobytes(), (WINDOW_WIDTH, window_height), "RGBA"
    )

    # 4. State & Animation Trackers
    path_idx = 0
    point_idx = 0
    current_cursor = None
    drawing_finished = False

    h_offset = 0.0
    reveal_alpha = 0.0

    # Exact center of the divine sunburst
    center_x = int(WINDOW_WIDTH * 0.51)
    center_y = int(window_height * 0.49)
    max_radius = int(math.hypot(WINDOW_WIDTH, window_height)) * 2

    # 5. Main Execution Loop
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False

        # -------------------------------------------------------------
        # PHASE 1: Fast Cursor Sketching (Pitch Dark Background)
        # -------------------------------------------------------------
        if not drawing_finished:
            screen.fill((10, 6, 4))

            for _ in range(DRAW_SPEED):
                if path_idx >= len(drawing_paths):
                    drawing_finished = True
                    break

                current_path = drawing_paths[path_idx]
                if point_idx < len(current_path) - 1:
                    p1 = current_path[point_idx]
                    p2 = current_path[point_idx + 1]
                    pygame.draw.line(drawn_layer, STROKE_COLOR, p1, p2, 2)
                    current_cursor = p2
                    point_idx += 1
                else:
                    path_idx += 1
                    point_idx = 0

            screen.blit(drawn_layer, (0, 0))

            if current_cursor:
                pygame.draw.circle(screen, (255, 180, 50), current_cursor, 8)
                pygame.draw.circle(screen, CURSOR_COLOR, current_cursor, 4)

        # -------------------------------------------------------------
        # PHASE 2: High-Contrast Sunburst + Unidirectional Text + Divine Light
        # -------------------------------------------------------------
        else:
            if reveal_alpha < 255:
                reveal_alpha = min(255.0, reveal_alpha + 4.0)

            # 1. Warm Golden Base Screen
            screen.fill((255, 185, 45))

            # 2. Prominent High-Contrast Sunburst Rays
            rays_layer = pygame.Surface((WINDOW_WIDTH, window_height), pygame.SRCALPHA)
            num_beams = 32
            angle_slice = (2 * math.pi) / num_beams

            for i in range(0, num_beams, 2):
                a1 = i * angle_slice
                a2 = (i + 1) * angle_slice

                p1 = (center_x, center_y)
                p2 = (center_x + int(max_radius * math.cos(a1)), center_y + int(max_radius * math.sin(a1)))
                p3 = (center_x + int(max_radius * math.cos(a2)), center_y + int(max_radius * math.sin(a2)))

                # Saffron-golden beam with rich contrast
                ray_alpha = int(reveal_alpha * 0.65)
                pygame.draw.polygon(rays_layer, (215, 110, 15, ray_alpha), [p1, p2, p3])

            screen.blit(rays_layer, (0, 0))

            # 3. Horizontal Mantra Scrolling (All Rows Move in One Single Direction)
            h_offset = (h_offset + 1.2) % unit_w
            for r in range(total_rows):
                y_pos = r * row_spacing
                start_x = -unit_w + h_offset  # Uniform flow across all lines

                curr_x = start_x
                while curr_x < WINDOW_WIDTH + unit_w:
                    screen.blit(rendered_unit, (int(curr_x), y_pos))
                    curr_x += unit_w

            # 4. Solid Black Silhouette Layer (Lord Ram & Hanuman Ji)
            solid_fill_surface.set_alpha(int(reveal_alpha))
            screen.blit(solid_fill_surface, (0, 0))

            # 5. Divine Sun & Radiant Glow Burst Over the Waist/Hands
            divine_light = pygame.Surface((WINDOW_WIDTH, window_height), pygame.SRCALPHA)

            # Soft atmospheric warm glow
            for rad in range(120, 0, -5):
                g_alpha = int((reveal_alpha * 0.45) * (1.0 - (rad / 120.0)))
                pygame.draw.circle(divine_light, (255, 230, 130, g_alpha), (center_x, center_y), rad)

            # Radiant Sun Flare blooming directly at the center
            pulse = 1.0 + 0.08 * math.sin(pygame.time.get_ticks() * 0.006)
            pygame.draw.circle(divine_light, (255, 255, 240, int(reveal_alpha * 0.95)), (center_x, center_y), int(16 * pulse))
            pygame.draw.circle(divine_light, (255, 215, 70, int(reveal_alpha * 0.65)), (center_x, center_y), int(36 * pulse))

            # Draw light burst ON TOP so it naturally illuminates the deities
            screen.blit(divine_light, (0, 0))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


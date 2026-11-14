"""
Day 17: Albino Python Realistic Vector Sketch Art
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A smooth, authentic generative digital sketch simulation that draws the
exact, pristine Albino Python artwork slowly, steadily, and photorealistically:
1. Exact Image Fidelity: 100% faithful reproduction of 'python snake image.jpeg'
   (no fake geometric polygons, no blocky artifacts, exact crimson gradient and scales).
2. Dual-Phase Drawing Pipeline:
   - Phase 1 (Contour Underdrawing): An ergonomic artist pencil traces the smooth
     anatomical curves, coiled body outlines, cephalic head plates, ruby eye, and forked tongue.
   - Phase 2 (Volumetric Scale Shading): The pencil sweeps across the coils, smoothly
     revealing small, realistic portions (brush radius ~26 px) of the magnificent 3D scales.
3. Corner-to-Corner Trajectories:
   - Forward: Sweeps from Top-Left (0, 0) across diagonal bands to Bottom-Right.
   - Vice-Versa: Sweeps from Bottom-Right back to Top-Left, revealing lower coils first.
   - Auto-Loop: Seamlessly cycles between Forward and Vice-Versa drawing passes.
4. Ergonomic Artist Stylus: A classic colored-pencil stylus leads the stroke with an active
   graphite lead tip, cedar wood collar, 3D barrel, and floating stardust pigment particles.

Controls:
  [SPACE]     - Pause / Resume drawing
  [V]         - Toggle Vice-Versa direction (Top-Left <-> Bottom-Right)
  [R]         - Restart current drawing from beginning
  [A]         - Toggle Auto-Loop cycle (on by default)
  [+] / [UP]  - Increase drawing speed (+1 pt/frame)
  [-] / [DOWN]- Decrease drawing speed (-1 pt/frame)
  [1] - [4]   - Speed presets (1: Meditative, 2: Standard, 3: Fast, 4: Turbo)
  [C] / [F]   - Fast-forward / Complete drawing instantly
  [S]         - Save high-resolution PNG screenshot
  [ESC/Q]     - Exit application cleanly
"""

import math
import os
import random
import sys
import numpy as np

# Suppress duplicate dylib warning on macOS during module import
_old_stderr = os.dup(2)
_devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(_devnull, 2)
os.close(_devnull)
try:
    import pygame
    import cv2
finally:
    os.dup2(_old_stderr, 2)
    os.close(_old_stderr)

# ==============================================================================
# 1. CONFIGURATION & CANVAS CONSTANTS
# ==============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FILENAME = "python snake image.jpeg"

CANDIDATE_PATHS = [
    os.path.join(SCRIPT_DIR, IMAGE_FILENAME),
    os.path.join(os.getcwd(), "days", "Day-17-Python Sketch", IMAGE_FILENAME),
    os.path.join(os.getcwd(), IMAGE_FILENAME),
    IMAGE_FILENAME,
]

IMAGE_PATH = None
for p in CANDIDATE_PATHS:
    if os.path.isfile(p):
        IMAGE_PATH = p
        break

# Display dimensions matching portrait ratio (574 x 1024)
CANVAS_WIDTH = 574
CANVAS_HEIGHT = 1024
FPS = 60

# Palette & Brush Constants
DEEP_CRIMSON_VOID = (28, 3, 6)
SKETCH_STROKE_COLOR = (245, 225, 230)
BRUSH_RADIUS = 26
DEFAULT_SPEED = 4


# ==============================================================================
# 2. IMAGE PREPROCESSING & TRAJECTORY GENERATION
# ==============================================================================
def load_master_and_generate_trajectories(image_path, width, height, brush_radius=BRUSH_RADIUS):
    """
    Loads reference masterpiece, creates scaled master surface,
    extracts anatomical contour paths for Phase 1 underdrawing,
    and builds continuous diagonal trajectories for Phase 2 scale rendering.
    """
    if not image_path or not os.path.isfile(image_path):
        raise FileNotFoundError(
            f"Could not find '{IMAGE_FILENAME}'.\nSearched in: {CANDIDATE_PATHS}"
        )

    raw_image = pygame.image.load(image_path)
    scaled = pygame.transform.smoothscale(raw_image, (width, height))
    master_surface = scaled.convert() if pygame.display.get_surface() else scaled

    # 1. Extract clean contour sketch paths for Phase 1 using OpenCV
    cv_img = cv2.imread(image_path)
    cv_scaled = cv2.resize(cv_img, (width, height), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(cv_scaled, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 7, 50, 50)
    edges = cv2.Canny(blurred, 35, 110)

    # Isolate snake body contours
    b, g, r = cv2.split(cv_scaled)
    snake_mask = ((g > 35) | (b > 35) | (r > 195)).astype(np.uint8)
    edges = cv2.bitwise_and(edges, edges, mask=snake_mask)

    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=lambda c: cv2.arcLength(c, False), reverse=True)

    sketch_paths = []
    for cnt in contours:
        if len(cnt) >= 10:
            pts = [(int(pt[0][0]), int(pt[0][1])) for pt in cnt]
            sketch_paths.append(pts)

    # 2. Build continuous diagonal corner-to-corner trajectories for Phase 2
    step_d = int(brush_radius * 0.85)
    bands = []
    for d in range(0, width + height + step_d, step_d):
        x_min = max(0, d - height)
        x_max = min(width, d)
        if x_min <= x_max:
            bands.append((d, x_min, x_max))

    # Forward: Top-Left (0, 0) -> Bottom-Right (width, height)
    forward_path = []
    for i, (d, x_min, x_max) in enumerate(bands):
        line_len = math.hypot(x_max - x_min, x_max - x_min)
        steps = max(3, int(line_len / (brush_radius * 0.4)))
        if i % 2 == 0:
            xs = np.linspace(x_min, x_max, steps)
        else:
            xs = np.linspace(x_max, x_min, steps)
        for x in xs:
            forward_path.append((int(x), int(d - x)))

    # Vice-Versa: Bottom-Right (width, height) -> Top-Left (0, 0)
    vice_versa_path = list(reversed(forward_path))

    return master_surface, sketch_paths, forward_path, vice_versa_path


# ==============================================================================
# 3. ERGONOMIC ARTIST STYLUS & PARTICLES
# ==============================================================================
class GraphiteParticle:
    """Atmospheric graphite / pigment speck that drifts gently from the pencil tip."""
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.6, 2.4)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 0.4
        self.color = color
        self.alpha = 240
        self.radius = random.uniform(1.2, 2.5)
        self.decay = random.uniform(7.0, 14.0)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha = max(0, self.alpha - self.decay)
        return self.alpha > 0

    def draw(self, surface):
        if self.alpha <= 0:
            return
        temp = pygame.Surface((int(self.radius * 4 + 2), int(self.radius * 4 + 2)), pygame.SRCALPHA)
        col = (*self.color[:3], int(self.alpha))
        center = (int(self.radius * 2 + 1), int(self.radius * 2 + 1))
        pygame.draw.circle(temp, col, center, int(self.radius))
        surface.blit(temp, (int(self.x - center[0]), int(self.y - center[1])))


def draw_artist_stylus(surface, tip_pos, prev_pos, lead_color):
    """
    Renders an authentic, ergonomic artist drawing pencil with:
    - Pointed pigment lead tip
    - Conical cedar wood sharpening collar
    - Octagonal colored pencil shaft
    - Active graphite glow at contact point
    """
    tx, ty = tip_pos

    # Determine movement angle (draw pencil trailing behind tip)
    if prev_pos and prev_pos != tip_pos:
        dx = tip_pos[0] - prev_pos[0]
        dy = tip_pos[1] - prev_pos[1]
        move_angle = math.atan2(dy, dx)
    else:
        move_angle = math.pi * 0.25

    # Pencil body extends backwards (-angle) tilted naturally at 28 degrees
    body_angle = move_angle + math.pi + math.radians(28)
    cos_a = math.cos(body_angle)
    sin_a = math.sin(body_angle)
    perp_x = -sin_a
    perp_y = cos_a

    lead_len = 10
    collar_len = 24
    shaft_len = 85
    radius = 6.5

    # 1. Lead Tip
    lead_base = (tx + cos_a * lead_len, ty + sin_a * lead_len)
    lead_pts = [
        (tx, ty),
        (lead_base[0] + perp_x * 2.8, lead_base[1] + perp_y * 2.8),
        (lead_base[0] - perp_x * 2.8, lead_base[1] - perp_y * 2.8),
    ]
    pygame.draw.polygon(surface, lead_color, [(int(x), int(y)) for x, y in lead_pts])
    pygame.draw.polygon(surface, (40, 10, 15), [(int(x), int(y)) for x, y in lead_pts], 1)

    # 2. Sharpened Wood Collar (Cedar Cone)
    collar_base = (tx + cos_a * (lead_len + collar_len), ty + sin_a * (lead_len + collar_len))
    wood_pts = [
        (lead_base[0] + perp_x * 2.8, lead_base[1] + perp_y * 2.8),
        (collar_base[0] + perp_x * radius, collar_base[1] + perp_y * radius),
        (collar_base[0] - perp_x * radius, collar_base[1] - perp_y * radius),
        (lead_base[0] - perp_x * 2.8, lead_base[1] - perp_y * 2.8),
    ]
    pygame.draw.polygon(surface, (225, 185, 140), [(int(x), int(y)) for x, y in wood_pts])
    pygame.draw.polygon(surface, (155, 110, 75), [(int(x), int(y)) for x, y in wood_pts], 1)

    # 3. Colored Pencil Barrel
    shaft_top = (tx + cos_a * (lead_len + collar_len + shaft_len), ty + sin_a * (lead_len + collar_len + shaft_len))
    shaft_pts = [
        (collar_base[0] + perp_x * radius, collar_base[1] + perp_y * radius),
        (shaft_top[0] + perp_x * radius, shaft_top[1] + perp_y * radius),
        (shaft_top[0] - perp_x * radius, shaft_top[1] - perp_y * radius),
        (collar_base[0] - perp_x * radius, collar_base[1] - perp_y * radius),
    ]
    # Burgundy / Crimson pencil body matching albino python palette
    pygame.draw.polygon(surface, (145, 18, 32), [(int(x), int(y)) for x, y in shaft_pts])
    # Specular ridge on barrel
    ridge_1 = (collar_base[0] + perp_x * (radius * 0.35), collar_base[1] + perp_y * (radius * 0.35))
    ridge_2 = (shaft_top[0] + perp_x * (radius * 0.35), shaft_top[1] + perp_y * (radius * 0.35))
    pygame.draw.line(surface, (215, 65, 80), (int(ridge_1[0]), int(ridge_1[1])), (int(ridge_2[0]), int(ridge_2[1])), 2)
    pygame.draw.polygon(surface, (75, 8, 15), [(int(x), int(y)) for x, y in shaft_pts], 1)

    # 4. Active Contact Glow
    glow = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*lead_color[:3], 95), (10, 10), 8)
    pygame.draw.circle(glow, (255, 245, 250, 210), (10, 10), 3)
    surface.blit(glow, (tx - 10, ty - 10))


# ==============================================================================
# 4. HEAD-UP DISPLAY (HUD)
# ==============================================================================
def draw_hud(surface, font, phase, progress, speed, is_paused, mode_name, auto_loop):
    """Renders a sleek bottom status bar with telemetry and control hints."""
    hud_h = 36
    hud_y = CANVAS_HEIGHT - hud_h
    hud_surf = pygame.Surface((CANVAS_WIDTH, hud_h), pygame.SRCALPHA)
    hud_surf.fill((12, 2, 4, 220))
    pygame.draw.line(hud_surf, (165, 25, 42, 220), (0, 0), (CANVAS_WIDTH, 0), 1)

    status_icon = "⏸ PAUSED" if is_paused else "▶ DRAWING"
    loop_str = "Auto-Loop: ON" if auto_loop else "Auto-Loop: OFF"
    text_str = (
        f"{status_icon} | {phase} [{progress:.0f}%] | "
        f"{mode_name} | {speed}x | {loop_str}"
    )

    rendered = font.render(text_str, True, (240, 225, 230))
    hud_surf.blit(rendered, (14, 9))

    # Controls hint
    hint = font.render("[SPACE] Pause  [V] Vice-Versa  [+/-] Speed  [S] Save  [ESC] Exit", True, (185, 145, 155))
    hud_surf.blit(hint, (CANVAS_WIDTH - hint.get_width() - 14, 9))

    surface.blit(hud_surf, (0, hud_y))


# ==============================================================================
# 5. MAIN DRAWING ENGINE LOOP
# ==============================================================================
def main():
    print("=" * 68)
    print("🐍  DAY 17: ALBINO PYTHON REALISTIC DIGITAL SKETCH ART  🐍")
    print("30 Days Python Challenge by Tejas (@Tejas0113)")
    print("=" * 68)

    if not IMAGE_PATH:
        print(f"❌ Error: Masterpiece '{IMAGE_FILENAME}' not found!")
        print("Please place the image in 'days/Day-17-Python Sketch/'.")
        sys.exit(1)

    print(f"📷 Loading Artwork: {IMAGE_PATH}")
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    pygame.display.set_caption("🐍 Albino Python Sketch Art | 30 Days Python Challenge | Day 17")
    clock = pygame.time.Clock()

    try:
        font = pygame.font.SysFont("menlo,consolas,monaco,courier", 11, bold=True)
    except Exception:
        font = pygame.font.Font(None, 14)

    # 1. Load Master Image & Generate Paths
    master_surface, sketch_paths, forward_path, vice_versa_path = load_master_and_generate_trajectories(
        IMAGE_PATH, CANVAS_WIDTH, CANVAS_HEIGHT, BRUSH_RADIUS
    )

    print(f"✅ Extracted {len(sketch_paths)} Anatomical Contour Paths (Phase 1).")
    print(f"✅ Generated {len(forward_path)} Smooth Shading Trajectory Points (Phase 2).")

    # Drawing Surfaces
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(DEEP_CRIMSON_VOID)

    contour_layer = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.SRCALPHA)

    # State Variables
    is_paused = False
    speed = DEFAULT_SPEED
    auto_loop = True
    active_mode = "Forward"  # "Forward" or "Vice-Versa"
    active_trajectory = forward_path
    
    # Phase Tracking:
    # Phase 1: Contour & Scale Underdrawing
    # Phase 2: Volumetric Scale Shading & Progressive Revealing
    phase = 1
    sketch_path_idx = 0
    sketch_pt_idx = 0
    traj_idx = 0

    tip_pos = (0, 0)
    prev_tip_pos = (0, 0)
    particles = []
    drawing_completed = False

    print("\n🎮 Interactive Controls:")
    print("   [SPACE]     : Pause / Resume drawing")
    print("   [V]         : Toggle Vice-Versa direction")
    print("   [R]         : Restart current drawing pass")
    print("   [A]         : Toggle Auto-Loop cycle")
    print("   [+] / [-]   : Adjust drawing speed")
    print("   [1] - [4]   : Speed presets (1x, 3x, 6x, 12x)")
    print("   [C] / [F]   : Fast-forward / Complete instantly")
    print("   [S]         : Save high-resolution PNG poster")
    print("   [ESC/Q]     : Quit application")
    print("-" * 68)

    running = True
    while running:
        clock.tick(FPS)

        # -------------------------------------------------------------
        # Event Handling
        # -------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_UP):
                    speed = min(speed + 1, 24)
                elif event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE, pygame.K_DOWN):
                    speed = max(speed - 1, 1)
                elif event.key == pygame.K_1:
                    speed = 1
                elif event.key == pygame.K_2:
                    speed = 4
                elif event.key == pygame.K_3:
                    speed = 8
                elif event.key == pygame.K_4:
                    speed = 16
                elif event.key == pygame.K_v:
                    # Toggle Forward <-> Vice-Versa
                    active_mode = "Vice-Versa" if active_mode == "Forward" else "Forward"
                    active_trajectory = vice_versa_path if active_mode == "Vice-Versa" else forward_path
                    traj_idx = 0
                    canvas.fill(DEEP_CRIMSON_VOID)
                    contour_layer.fill((0, 0, 0, 0))
                    phase = 1
                    sketch_path_idx = 0
                    sketch_pt_idx = 0
                    drawing_completed = False
                elif event.key == pygame.K_r:
                    # Restart current pass
                    phase = 1
                    sketch_path_idx = 0
                    sketch_pt_idx = 0
                    traj_idx = 0
                    canvas.fill(DEEP_CRIMSON_VOID)
                    contour_layer.fill((0, 0, 0, 0))
                    drawing_completed = False
                elif event.key == pygame.K_a:
                    auto_loop = not auto_loop
                elif event.key in (pygame.K_c, pygame.K_f):
                    # Fast-forward to completed drawing
                    canvas.blit(master_surface, (0, 0))
                    traj_idx = len(active_trajectory)
                    phase = 2
                    drawing_completed = True
                elif event.key == pygame.K_s:
                    # Export Screenshot
                    output_dir = os.path.join(SCRIPT_DIR, "output")
                    os.makedirs(output_dir, exist_ok=True)
                    out_path = os.path.join(output_dir, "python_snake_sketch_export.png")
                    pygame.image.save(canvas, out_path)
                    print(f"✨ Artwork saved successfully to: {out_path}")

        # -------------------------------------------------------------
        # Phase 1: Anatomical Contour Sketching (Underdrawing)
        # -------------------------------------------------------------
        if phase == 1 and not is_paused:
            # Advance contour sketch lines
            lines_per_frame = max(4, speed * 6)
            for _ in range(lines_per_frame):
                if sketch_path_idx >= len(sketch_paths):
                    phase = 2
                    traj_idx = 0
                    break

                curr_path = sketch_paths[sketch_path_idx]
                if sketch_pt_idx < len(curr_path) - 1:
                    p1 = curr_path[sketch_pt_idx]
                    p2 = curr_path[sketch_pt_idx + 1]
                    pygame.draw.line(contour_layer, SKETCH_STROKE_COLOR, p1, p2, 1)
                    prev_tip_pos = tip_pos
                    tip_pos = p2
                    sketch_pt_idx += 1

                    if random.random() < 0.25:
                        particles.append(GraphiteParticle(tip_pos[0], tip_pos[1], SKETCH_STROKE_COLOR))
                else:
                    sketch_path_idx += 1
                    sketch_pt_idx = 0

        # -------------------------------------------------------------
        # Phase 2: Volumetric Scale Shading & Progressive Revealing
        # -------------------------------------------------------------
        elif phase == 2 and not is_paused and not drawing_completed:
            for _ in range(speed):
                if traj_idx >= len(active_trajectory):
                    drawing_completed = True
                    # Ensure 100% canvas coverage
                    canvas.blit(master_surface, (0, 0))
                    # If auto-loop is enabled, alternate direction
                    if auto_loop:
                        active_mode = "Vice-Versa" if active_mode == "Forward" else "Forward"
                        active_trajectory = vice_versa_path if active_mode == "Vice-Versa" else forward_path
                        traj_idx = 0
                        drawing_completed = False
                        canvas.fill(DEEP_CRIMSON_VOID)
                        contour_layer.fill((0, 0, 0, 0))
                        phase = 1
                        sketch_path_idx = 0
                        sketch_pt_idx = 0
                    break

                px, py = active_trajectory[traj_idx]
                prev_tip_pos = tip_pos
                tip_pos = (px, py)
                traj_idx += 1

                # Transfer exact visible portion from master surface onto canvas
                x1 = max(0, px - BRUSH_RADIUS)
                y1 = max(0, py - BRUSH_RADIUS)
                x2 = min(CANVAS_WIDTH, px + BRUSH_RADIUS + 1)
                y2 = min(CANVAS_HEIGHT, py + BRUSH_RADIUS + 1)
                w = x2 - x1
                h = y2 - y1

                if w > 0 and h > 0:
                    patch = master_surface.subsurface(pygame.Rect(x1, y1, w, h))
                    canvas.blit(patch, (x1, y1))

                # Emit subtle pigment particle
                if random.random() < 0.2:
                    lead_c = master_surface.get_at((max(0, min(CANVAS_WIDTH - 1, px)), max(0, min(CANVAS_HEIGHT - 1, py))))
                    particles.append(GraphiteParticle(px, py, lead_c))

        # -------------------------------------------------------------
        # Rendering Frame
        # -------------------------------------------------------------
        screen.blit(canvas, (0, 0))

        # Show underdrawing contours during Phase 1
        if phase == 1:
            screen.blit(contour_layer, (0, 0))

        # Update & draw graphite particles
        particles = [p for p in particles if p.update()]
        for p in particles:
            p.draw(screen)

        # Draw Ergonomic Artist Stylus
        if not drawing_completed or (phase == 2 and traj_idx < len(active_trajectory)):
            try:
                lead_color = master_surface.get_at((
                    max(0, min(CANVAS_WIDTH - 1, tip_pos[0])),
                    max(0, min(CANVAS_HEIGHT - 1, tip_pos[1]))
                ))
            except Exception:
                lead_color = SKETCH_STROKE_COLOR
            draw_artist_stylus(screen, tip_pos, prev_tip_pos, lead_color)

        # Telemetry & HUD
        if phase == 1:
            progress = min(100.0, (sketch_path_idx / max(1, len(sketch_paths))) * 100.0)
            phase_name = "Phase 1: Contour Underdrawing"
        else:
            progress = min(100.0, (traj_idx / max(1, len(active_trajectory))) * 100.0)
            phase_name = "Phase 2: Scale Shading" if not drawing_completed else "Masterpiece Complete"

        draw_hud(screen, font, phase_name, progress, speed, is_paused, active_mode, auto_loop)
        pygame.display.flip()

    pygame.quit()
    print("👋 Albino Python sketch application closed cleanly.")


if __name__ == "__main__":
    main()

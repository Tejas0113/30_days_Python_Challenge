"""
Day 17: Albino Python Realistic Vector Sketch Art
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A generative vector sketch animation that recreates the stunning albino
python artwork with exact form, scale detailing, glowing crimson eye, and rich
crimson color combination matching 'python snake image.jpeg'.

Features:
  - Dynamic path resolution: runs seamlessly anywhere without FileNotFoundError
  - Normalized world coordinates: setworldcoordinates(-450, -450, 450, 450) for perfect visibility
  - Python Turtle graphics animation with classic black arrow cursor
  - Smart crimson paper-tone background detection (no black boundary cuts across empty canvas)
  - Interactive keyboard controls:
      [Space]   : Pause / Resume animation
      [+] / [-] : Speed up / Slow down drawing
      [C]       : Fast-forward / Complete drawing instantly
      [S]       : Save high-res screenshot / poster
      [Q / Esc] : Graceful exit
  - Robust exception handling: clean exit on window close without crashes
"""

import math
import os
import sys
import time
import tkinter as tk
import turtle
import cv2
import numpy as np

# ==============================================================================
# 1. CONFIGURATION & DYNAMIC PATH RESOLUTION
# ==============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FILENAME = "python snake image.jpeg"

# Search in script directory, working directory, and repository days path
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

# Viewport & Coordinate Configuration (World Coordinates [-450, -450, 450, 450])
WORLD_COORDINATES = (-450, -450, 450, 450)
TARGET_HEIGHT = 800         # Fits comfortably in [-400, 400], leaving 50px top/bottom padding
WINDOW_WIDTH = 850          # Generous desktop canvas window
WINDOW_HEIGHT = 850
NUM_COLORS = 24             # High-fidelity chromatic palette (crimson, ivory, peach, ruby eye)
EPSILON_FACTOR = 0.0035     # Precision contour simplification for organic curves
MIN_CONTOUR_AREA = 10       # Eliminates micro-noise while retaining small scales
INK_EDGE_LOW = 35           # Canny low threshold for scale boundaries
INK_EDGE_HIGH = 105         # Canny high threshold for scale boundaries
DEFAULT_BATCH_SIZE = 8      # Fast, fluid animated drawing speed


def load_source_image():
    """Dynamically resolves and validates the reference snake artwork."""
    if not IMAGE_PATH or not os.path.isfile(IMAGE_PATH):
        raise FileNotFoundError(
            f"Could not locate '{IMAGE_FILENAME}'.\n"
            f"Searched paths: {CANDIDATE_PATHS}"
        )
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        raise ValueError(f"Failed to decode image from '{IMAGE_PATH}'.")
    return img


# ==============================================================================
# 2. VECTOR EXTRACTION & CHROMATIC CLUSTERING
# ==============================================================================
def quantize_palette(img_bgr, k=NUM_COLORS):
    """Clusters image into k dominant chromatic centroids using Lloyd's K-Means."""
    data = np.float32(img_bgr).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 0.5)
    _, labels, centers = cv2.kmeans(
        data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    centers = np.uint8(centers)
    quantized = centers[labels.flatten()].reshape(img_bgr.shape)
    return quantized, centers


def extract_vector_elements(image_path=None, target_height=TARGET_HEIGHT):
    """
    Extracts ordered vector polygons and ink scale contours from the snake artwork.
    Normalized into the centered world coordinate space.
    Returns:
      - polygons: list of (hex_color, points, area) sorted large-to-small
      - ink_lines: list of polyline point lists for scale and contour inking
      - paper_hex: detected background crimson tone
      - target_width, target_height: scaled dimensions
      - resized: resized BGR image
      - bg_bgr: background BGR tuple
    """
    img = load_source_image() if image_path is None else cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to load reference image.")

    orig_h, orig_w = img.shape[:2]
    scale = target_height / orig_h
    target_width = int(orig_w * scale)
    resized = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_AREA)

    # Edge-preserving bilateral filter: smooths fine skin noise while preserving scale contours
    smooth = cv2.bilateralFilter(resized, d=7, sigmaColor=40, sigmaSpace=40)

    # K-Means 24-cluster chromatic quantization
    quantized, centers = quantize_palette(smooth, NUM_COLORS)

    # Identify background crimson tone from peripheral borders
    border_samples = np.vstack([
        quantized[:15, :15].reshape(-1, 3),
        quantized[:15, -15:].reshape(-1, 3),
        quantized[-15:, :15].reshape(-1, 3),
        quantized[-15:, -15:].reshape(-1, 3),
    ])
    bg_bgr = np.median(border_samples, axis=0).astype(np.uint8)
    paper_hex = "#{:02x}{:02x}{:02x}".format(int(bg_bgr[2]), int(bg_bgr[1]), int(bg_bgr[0]))

    # Segment snake body against crimson backdrop
    dist_to_bg = np.linalg.norm(quantized.astype(float) - bg_bgr.astype(float), axis=2)
    r = smooth[:, :, 2].astype(float)
    g = smooth[:, :, 1].astype(float)
    b = smooth[:, :, 0].astype(float)
    snake_mask = ((g > 40) | (b > 40) | (r > 190) | (dist_to_bg > 36)).astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    snake_mask = cv2.morphologyEx(snake_mask, cv2.MORPH_CLOSE, kernel)

    # 1. Extract vector color polygons
    polygons = []
    for color in centers:
        # Skip pure background clusters
        if np.linalg.norm(color.astype(float) - bg_bgr.astype(float)) < 24:
            continue

        mask = cv2.inRange(quantized, color, color)
        mask = cv2.bitwise_and(mask, mask, mask=snake_mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        hex_color = "#{:02x}{:02x}{:02x}".format(int(color[2]), int(color[1]), int(color[0]))

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < MIN_CONTOUR_AREA:
                continue

            epsilon = EPSILON_FACTOR * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) >= 3:
                # Convert OpenCV (top-left) to Turtle (center-origin) coordinates
                pts = [(pt[0][0] - target_width / 2.0, target_height / 2.0 - pt[0][1]) for pt in approx]
                polygons.append((hex_color, pts, area))

    # Sort polygons: largest area first (draw body base flats first, scale details & eye on top)
    polygons.sort(key=lambda item: item[2], reverse=True)

    # 2. Extract fine scale edges, cephalic plate borders, and forked tongue
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, INK_EDGE_LOW, INK_EDGE_HIGH)
    edges = cv2.bitwise_and(edges, edges, mask=snake_mask)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    ink_lines = []
    for cnt in contours:
        if cv2.arcLength(cnt, False) >= 8:
            approx = cv2.approxPolyDP(cnt, 0.8, False)
            if len(approx) >= 2:
                pts = [(pt[0][0] - target_width / 2.0, target_height / 2.0 - pt[0][1]) for pt in approx]
                ink_lines.append(pts)

    return polygons, ink_lines, paper_hex, target_width, target_height, resized, bg_bgr


# ==============================================================================
# 3. INTERACTIVE TURTLE ANIMATION ENGINE
# ==============================================================================
class PythonSnakeSketchApp:
    def __init__(self, polygons, ink_lines, paper_hex, width, height, raw_resized, bg_bgr):
        self.polygons = polygons
        self.ink_lines = ink_lines
        self.paper_hex = paper_hex
        self.width = width
        self.height = height
        self.raw_resized = raw_resized
        self.bg_bgr = bg_bgr

        # Animation states
        self.is_paused = False
        self.fast_forward = False
        self.running = True
        self.batch_size = DEFAULT_BATCH_SIZE
        self.phase = "Init"

        self.setup_screen()
        self.bind_events()

    def setup_screen(self):
        """Initializes Turtle screen, normalized world coordinates, and drawing pen."""
        self.screen = turtle.Screen()
        self.screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

        # Set normalized world coordinate viewport [-450, -450, 450, 450]
        # This guarantees perfect centering, balanced margins, and zero clipping on any display
        self.screen.setworldcoordinates(*WORLD_COORDINATES)
        self.screen.bgcolor(self.paper_hex)
        self.update_title("Loading Python Snake Vector Model...")

        # Disable auto-refresh for smooth performance buffering
        self.screen.tracer(0, 0)

        # Main drawing turtle (classic black arrow cursor)
        self.pen = turtle.Turtle()
        self.pen.shape("arrow")
        self.pen.shapesize(0.65, 0.65)
        self.pen.speed(0)
        self.pen.pensize(1)

        # Intercept window close to exit cleanly
        try:
            root = self.screen._root
            root.protocol("WM_DELETE_WINDOW", self.on_close)
        except Exception:
            pass

    def update_title(self, status):
        """Updates window title bar with progress and control tips."""
        try:
            pause_str = "[PAUSED] " if self.is_paused else ""
            title = (
                f"{pause_str}🐍 Albino Python Sketch | {status} | "
                f"Speed: {self.batch_size}x | [Space] Pause [C] Fast [S] Save [Q] Quit"
            )
            self.screen.title(title)
        except Exception:
            pass

    def bind_events(self):
        """Binds keyboard controls for real-time interactivity."""
        self.screen.listen()
        self.screen.onkey(self.toggle_pause, "space")
        self.screen.onkey(self.speed_up, "plus")
        self.screen.onkey(self.speed_up, "equal")
        self.screen.onkey(self.speed_up, "Up")
        self.screen.onkey(self.speed_down, "minus")
        self.screen.onkey(self.speed_down, "underscore")
        self.screen.onkey(self.speed_down, "Down")
        self.screen.onkey(self.complete_instantly, "c")
        self.screen.onkey(self.complete_instantly, "C")
        self.screen.onkey(self.save_artwork, "s")
        self.screen.onkey(self.save_artwork, "S")
        self.screen.onkey(self.on_close, "q")
        self.screen.onkey(self.on_close, "Q")
        self.screen.onkey(self.on_close, "Escape")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        status = "Paused" if self.is_paused else f"{self.phase}"
        self.update_title(status)

    def speed_up(self):
        self.batch_size = min(self.batch_size + 4, 120)
        self.update_title(f"{self.phase} (Speed: {self.batch_size}x)")

    def speed_down(self):
        self.batch_size = max(self.batch_size - 2, 1)
        self.update_title(f"{self.phase} (Speed: {self.batch_size}x)")

    def complete_instantly(self):
        self.fast_forward = True
        self.batch_size = 250

    def on_close(self):
        self.running = False
        try:
            turtle.bye()
        except Exception:
            pass

    def save_artwork(self):
        """Exports the rendered masterpiece as a high-resolution PNG image."""
        try:
            output_dir = os.path.join(SCRIPT_DIR, "output")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "python_snake_sketch_export.png")

            # Render full vector image directly to canvas for perfect fidelity
            canvas = np.full_like(self.raw_resized, self.bg_bgr)

            # Draw polygons
            for hex_col, pts, _ in self.polygons:
                rgb = [int(hex_col[i:i+2], 16) for i in (1, 3, 5)]
                bgr = (rgb[2], rgb[1], rgb[0])
                cv_pts = np.array([
                    [int(p[0] + self.width / 2.0), int(self.height / 2.0 - p[1])]
                    for p in pts
                ], dtype=np.int32)
                cv2.fillPoly(canvas, [cv_pts], bgr)
                cv2.polylines(canvas, [cv_pts], True, (max(0, bgr[0]-25), max(0, bgr[1]-25), max(0, bgr[2]-25)), 1, cv2.LINE_AA)

            # Draw ink scale lines
            for pts in self.ink_lines:
                cv_pts = np.array([
                    [int(p[0] + self.width / 2.0), int(self.height / 2.0 - p[1])]
                    for p in pts
                ], dtype=np.int32)
                cv2.polylines(canvas, [cv_pts], False, (15, 5, 45), 1, cv2.LINE_AA)

            cv2.imwrite(output_path, canvas)
            print(f"✨ Artwork saved successfully: {output_path}")
            self.update_title(f"Saved to {os.path.basename(output_path)}!")
        except Exception as e:
            print(f"Error saving artwork: {e}")

    def run(self):
        """Executes the dual-phase drawing pipeline with live user feedback."""
        try:
            # --------------------------------------------------------------
            # Phase 1: Draw Vector Color Polygons (Anatomic Coils & Flats)
            # --------------------------------------------------------------
            self.phase = "Phase 1/2: Anatomic Body Flats & Shading"
            total_polys = len(self.polygons)
            print(f"\n🎨 Phase 1: Drawing {total_polys} Anatomic Body Polygons (Pearlescent albino flats)...")

            for i, (hex_col, pts, _) in enumerate(self.polygons):
                if not self.running:
                    return

                while self.is_paused and self.running:
                    time.sleep(0.04)
                    try:
                        self.screen.update()
                    except Exception:
                        return

                self.pen.penup()
                self.pen.goto(pts[0])
                self.pen.pendown()

                # Outline color subtly darker than fill for realistic scale boundaries
                self.pen.pencolor("#3d0810")
                self.pen.fillcolor(hex_col)
                self.pen.begin_fill()

                for pt in pts[1:]:
                    self.pen.goto(pt)
                self.pen.goto(pts[0])
                self.pen.end_fill()

                if (i % self.batch_size == 0) or (i == total_polys - 1) or self.fast_forward:
                    self.screen.update()
                    progress = int((i + 1) / total_polys * 100)
                    self.update_title(f"Phase 1: Coils & Flats ({progress}%)")

            # --------------------------------------------------------------
            # Phase 2: Inking Scale Patterns & Head Features
            # --------------------------------------------------------------
            self.phase = "Phase 2/2: Inking Scales & Head Features"
            total_inks = len(self.ink_lines)
            print(f"✒️  Phase 2: Inking {total_inks} Scale Edges, Cephalic Plates & Eye...")

            self.pen.pencolor("#2b040a")
            self.pen.pensize(1.2)

            for j, pts in enumerate(self.ink_lines):
                if not self.running:
                    return

                while self.is_paused and self.running:
                    time.sleep(0.04)
                    try:
                        self.screen.update()
                    except Exception:
                        return

                self.pen.penup()
                self.pen.goto(pts[0])
                self.pen.pendown()

                for pt in pts[1:]:
                    self.pen.goto(pt)

                if (j % self.batch_size == 0) or (j == total_inks - 1) or self.fast_forward:
                    self.screen.update()
                    progress = int((j + 1) / total_inks * 100)
                    self.update_title(f"Phase 2: Inking Scales ({progress}%)")

            # Finished
            self.pen.hideturtle()
            self.screen.update()
            self.phase = "Masterpiece Complete"
            print("🐍 Albino Python vector sketch complete! Press [S] to Save, [Q] to Exit.")
            self.update_title("Masterpiece Complete! [S] Save [Q] Exit")

            # Keep window interactive until user quits
            self.screen.exitonclick()

        except (turtle.Terminator, tk.TclError):
            # Graceful window close handling
            print("\nWindow closed. Exiting Python snake sketch.")
        except KeyboardInterrupt:
            print("\nAnimation stopped by user.")


# ==============================================================================
# 4. ENTRY POINT
# ==============================================================================
def main():
    print("=" * 65)
    print("🐍  DAY 17: ALBINO PYTHON REALISTIC VECTOR SKETCH ART  🐍")
    print("30 Days Python Challenge by Tejas (@Tejas0113)")
    print("=" * 65)

    if not IMAGE_PATH:
        print(f"❌ Error: Image '{IMAGE_FILENAME}' not found!")
        print("Please ensure the image is inside 'days/Day-17-Python Sketch/'.")
        sys.exit(1)

    print(f"📷 Source Image: {IMAGE_PATH}")
    print("⚙️  Extracting vector scales, chromatic palette, and contour inking...")
    start_time = time.time()

    polygons, ink_lines, paper_hex, width, height, raw_resized, bg_bgr = extract_vector_elements(
        IMAGE_PATH, TARGET_HEIGHT
    )

    elapsed = time.time() - start_time
    print(f"✅ Vectorization finished in {elapsed:.2f}s:")
    print(f"   • Vector Color Polygons : {len(polygons)}")
    print(f"   • Scale Contour Strokes : {len(ink_lines)}")
    print(f"   • Canvas Crimson Tone   : {paper_hex}")
    print(f"   • Dimensions            : {width} x {height}")
    print(f"   • World Coordinates     : {WORLD_COORDINATES}")

    print("\n🎮 Interactive Keyboard Controls:")
    print("   [Space]   : Pause / Resume animation")
    print("   [+] / [-] : Speed up / Slow down drawing rate")
    print("   [C]       : Fast-forward / Complete instantly")
    print("   [S]       : Save high-resolution PNG poster")
    print("   [Q / Esc] : Quit application")
    print("-" * 65)

    app = PythonSnakeSketchApp(
        polygons, ink_lines, paper_hex, width, height, raw_resized, bg_bgr
    )
    app.run()


if __name__ == "__main__":
    main()

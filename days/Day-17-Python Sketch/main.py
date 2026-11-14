"""
Day 17: Albino Python Realistic Vector Sketch Art
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
A generative vector sketch animation that recreates the stunning albino
python artwork with exact form, scale detailing, glowing crimson eye, and rich
crimson color combination matching 'python snake image.jpeg'.
"""

import math
import os
import sys
import time
import tkinter as tk
import turtle
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

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

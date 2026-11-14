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

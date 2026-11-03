# 🌀 Day 06: Cosmic Vortex Generative Art

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day06_animation.gif" alt="Cosmic Vortex Generative Art Preview" width="500px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 240, 255, 0.35);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art-9cf?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 6 explores procedural geometric beauty with the **Cosmic Vortex**, a generative art visualizer crafted using Python's standard `turtle` and `colorsys` libraries.

By combining progressive radial step scaling with intentional angular divergence ($100^\circ$ vs $109^\circ$), the algorithm builds an intricate, swirling vortex of 250 overlapping chromatic petals that radiate outward like a vibrant interstellar galaxy.

---

## 🧠 Concepts & Mathematical Mechanics

### 1. Asymmetric Angular Divergence
The hypnotic curvature of the vortex stems from non-orthogonal, mismatched turning angles:
- **Left Turn**: Turns $100^\circ$ after extending by distance $i$.
- **Right Turns**: Dual nested loops apply subsequent $109^\circ$ clockwise turns.
- Because $\Delta\theta = 109^\circ - 100^\circ = 9^\circ$, the orientation axis systematically diverges on each step, causing successive petals to overlap in an interlocking spiral spiral vortex rather than collapsing into a closed geometric polygon.

### 2. Parametric Step Scaling
As the loop index $i$ progresses from $0$ to $249$:
- Step distance `fd(i)` expands linearly, pushing the petal tips further from the origin.
- The inner nested segment `fd(i * j)` with $j \in \{0, 1\}$ introduces an asymmetrical outer wing on each petal that scales dynamically with radius.
- An embedded circular arc `circle(30)` forms a curved core aperture, providing visual depth and vortex density.

### 3. Continuous HSV Chromatic Progression
Color values are mapped dynamically using Python's built-in `colorsys` module:
- Hue begins at $h = 0.5$ (cyan/turquoise) and shifts by $\Delta h = 0.008$ per loop iteration.
- Converted via `colorsys.hsv_to_rgb(h % 1.0, 1.0, 1.0)` to full-saturation, peak-luminance RGB coordinates, yielding electric neon gradients cycling from cool cyans and blues through magentas, fiery reds, golds, and emerald greens.

### 4. Accelerated Frame Buffering
`t.tracer(3)` instructs Python Turtle to update the visual canvas once every 3 drawing steps, striking an ideal balance between high rendering speed and an enjoyable, smooth drawing animation.

---

## 🚀 How to Run

From the repository root:

```bash
python days/Day-06-Cosmic-Vortex/main.py
```

> **Tip:** Close the window or press `Ctrl + C` in the terminal to exit gracefully.

---

<p align="center">
  <a href="../../README.md"><b>⬅️ Return to 30 Days Challenge Tracker</b></a>
</p>

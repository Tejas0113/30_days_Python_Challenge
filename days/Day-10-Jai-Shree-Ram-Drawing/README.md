# 🏹 Day 10: Lord Shri Ram Sketch & Happy Diwali Devotional Art

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day10_animation.gif" alt="Lord Shri Ram Happy Diwali Drawing Preview" width="460px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(255, 153, 51, 0.35);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Vector%20Sketching-ff9933?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 10 celebrates the auspicious festival of Diwali and the divine return of Lord Shri Ram to Ayodhya with **Lord Shri Ram Sketch & Happy Diwali Devotional Art**.

Implemented in 100% pure standard Python using `turtle`, the program animates a saffron-gold vector sketch of Lord Shri Ram stroke-by-stroke—featuring the majestic Kodanda Bow, the Tarkash quiver of arrows, flowing matted hair (*Jata*), and serene facial features—accompanied by traditional glowing terracotta diyas and a warm **Happy Diwali** blessing.

---

## 🧠 Concepts & Mathematical Mechanics

### 1. Vector Stroke Extraction & RDP Simplification
The artwork is discretized into continuous vector polylines extracted from the sacred iconography:
- **Ramer-Douglas-Peucker (RDP) Algorithm**: Simplifies dense pixel contours by recursively discarding points with perpendicular distance less than $\epsilon = 1.0\text{ px}$:

  $$\mathbf{d}(P, AB) = \frac{|\vec{AB} \times \vec{AP}|}{|\vec{AB}|}$$

- This compresses tens of thousands of coordinate entries into 529 smooth, topologically continuous stroke paths totaling 5,845 vector points without losing fine details like the arrow feathers, tilak, or eye contours.

### 2. Zero-Dependency In-Memory Vector Packaging
To ensure that `main.py` runs instantly on any machine without requiring OpenCV (`cv2`) or missing external image files:
- The vector stroke data is compressed using standard `zlib` and `base64`.
- The 22 KB payload is embedded directly into the script and dynamically decompressed in under 1 millisecond into Turtle-ready floating-point coordinates.

### 3. Saffron-Gold Palette & Night Contrast
- **Sacred Saffron & Gold (`#FF9933`, `#FFA028`, `#FFD700`)**: Symbolizes divine radiance, spiritual strength, and auspiciousness.
- **Deep Midnight Navy (`#05070E`)**: Provides maximal contrast and emulates the illuminated night sky of Diwali in Ayodhya.

### 4. Procedural Terracotta Diya Generation
The bottom greeting is flanked by two traditional Diwali oil lamps (*diyas*):
- Symmetrical curved polygons form the earthen bowl and golden rim.
- Layered inner and outer flame teardrops (`#FF7A00` $\to$ `#FFA500` $\to$ `#FFFCE0`) create glowing visual warmth.

### 5. High-Performance Frame Buffering (`tracer(4, 6)`)
`turtle.tracer(4, 6)` instructs Turtle to update every 4 drawing operations with a 6 ms delay, creating a smooth, captivating drawing animation where viewers watch the portrait come to life in real time.

---

## 🚀 How to Run

From the repository root:

```bash
python days/Day-10-Jai-Shree-Ram-Drawing/main.py
```

> **Tip:** Close the window or press `Ctrl + C` in the terminal to exit gracefully.

---

<p align="center">
  <a href="../../README.md"><b>⬅️ Return to 30 Days Challenge Tracker</b></a>
</p>

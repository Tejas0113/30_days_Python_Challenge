# 🌸 Day 02: Turtle Flower Drawing

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day02_preview.png" alt="Turtle Flower Drawing Preview" width="520px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(255, 60, 120, 0.25);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art-9cf?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 2 explores procedural generative drawing through a multi-layered botanical scene rendered with Python's standard `turtle`, `math`, and `random` libraries.

The scene features an illuminated starry night background, a curved organic stem, detailed serrated leaves with midrib accents, and layered concentric crimson-and-coral flower petals surrounding a spiral phyllotaxis floret center.

---

## 🧠 Concepts & Mathematical Mechanics

### 1. Parametric Petal Geometry
Each petal is formed using two intersecting circular arcs with complementary angles:
- Circular arc span $\alpha$ and radius $R$ define the fullness and taper of each petal.
- Layered radial transformations rotate around the central receptacle with alternating chromatic shifts (deep crimson, radiant rose, soft gold).

### 2. Spiral Phyllotaxis Center
The floret pattern at the center of the blossom mimics natural plant phyllotaxis (Fermat's spiral):
$$r = c\sqrt{n}, \quad \theta = n \times 137.5^\circ$$
Golden-angle distribution distributes dots uniformly without clumping or voids.

### 3. Smooth Fullscreen Scaling
The canvas coordinates are mapped to a normalized virtual window coordinate space (`setworldcoordinates`), ensuring the artwork scales harmoniously to fullscreen displays without distortion.

---

## 🚀 How to Run

From the repository root:

```bash
python days/Day-02-Flower-Drawing/main.py
```

---

<p align="center">
  <a href="../../README.md"><b>⬅️ Return to 30 Days Challenge Tracker</b></a>
</p>

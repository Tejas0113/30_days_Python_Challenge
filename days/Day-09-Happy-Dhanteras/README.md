# 🪔 Day 09: Happy Dhanteras Animated Festival Poster

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day09_animation.gif" alt="Happy Dhanteras Animation Preview" width="480px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(255, 215, 0, 0.35);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Animation-ffd700?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 9 celebrates the auspicious festival of Dhanteras with the **Happy Dhanteras Animated Festival Poster**, an interactive digital greeting crafted using Python's standard `turtle`, `math`, and `random` libraries.

The visualizer unites cubic Bézier vector geometry, harmonic flame flicker physics, real-time particle fireworks, falling gold coins, and sacred typography to create an illuminated celebration on a deep midnight-blue canvas (`#080D25`).

---

## 🧠 Concepts & Mathematical Mechanics

### 1. Cubic Bézier Curve Geometry
To produce smooth, organic contours without manual pixel arrays, the script implements third-order parametric Bézier curves:

$$\mathbf{B}(u) = (1-u)^3 \mathbf{P}_0 + 3(1-u)^2 u\,\mathbf{P}_1 + 3(1-u) u^2\,\mathbf{P}_2 + u^3 \mathbf{P}_3, \quad u \in [0, 1]$$

- **Brass Kalash (Pot of Abundance)**: Curved body contours, neck indentations, and flared metallic rims are mapped via chained Bézier control points.
- **Realistic Clay Diyas**: Curved bowl silhouettes, inner oil pools, and cotton wick tips utilize cubic Bézier curves filled with warm earthen terracotta tones (`#A95719`).
- **Mango Leaves & Coconut**: Angular leaf veins and textured coconut fibers complete the sacred iconography.

### 2. Multi-Harmonic Flame Flicker & Wind Sway
Each diya flame exhibits natural wind responsiveness through dual-frequency sinusoidal wave harmonics:

$$\begin{aligned}
\text{sway} &= A_1 \sin(\phi) + A_2 \sin(0.55\phi) \\
\text{height} &= H_0 + B_1 \sin(1.7\phi) + B_2 \sin(0.7\phi)
\end{aligned}$$

- **Triple-Layered Teardrop Polygons**: The flame is composed of an outer vermilion-orange flame (`#FF7A18`), an inner golden flame (`#FFD23F`), and a luminous white-gold core (`#FFF4BC`).
- **Radial Ambient Glow**: Surrounding `dot()` overlays dynamically shift with flame sway to mimic radiant light diffusion in a dark room.

### 3. Multi-Ring Particle Fireworks Physics
Exploding fireworks simulate realistic atmospheric ballistic dynamics:
- **Velocity Vectors**: Particles fragment in radial concentric rings with velocities $v_x = v \cos(\theta), v_y = v \sin(\theta)$.
- **Drag & Damping**: Air resistance decelerates particles continuously: $v_x \leftarrow 0.985 \cdot v_x,\; v_y \leftarrow 0.985 \cdot v_y$.
- **Gravity Acceleration**: Downward gravitational pull bends particle arcs: $v_y \leftarrow v_y - g$.
- **Trail Sparks**: Rockets ascending from the ground leave glowing fading trails before detonation.

### 4. Continuous Falling Gold Coin Shower
A continuous particle system renders gold coins fluttering down the lateral margins:
- Randomized horizontal positions ($x \in [-430, -250] \cup [250, 430]$) keep the central greeting legible.
- Coins fall at varying speeds ($v \in [2, 5]\text{ px/frame}$) and recycle seamlessly to the top of the canvas when crossing the lower boundary.

### 5. High-Performance Frame Buffering (`tracer(0, 0)`)
By disabling automated updates (`screen.tracer(0, 0)`) and orchestrating updates through `screen.ontimer(main_animation, 25)`, the simulation achieves a smooth, flicker-free ~40 FPS refresh rate.

---

## 🚀 How to Run

From the repository root:

```bash
python days/Day-09-Happy-Dhanteras/main.py
```

> **Tip:** Close the window or press `Ctrl + C` in the terminal to exit gracefully.

---

<p align="center">
  <a href="../../README.md"><b>⬅️ Return to 30 Days Challenge Tracker</b></a>
</p>


# 🌀 Day 18: Generative Parametric Spiral Vortex Art

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day18_animation.gif" alt="Generative Parametric Spiral Vortex Art Preview" width="540px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(185, 110, 95, 0.35);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Parametric%20Caustics-B96E5F?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 18 delivers a mesmerizing, high-fidelity generative simulation: **Generative Parametric Spiral Vortex Art**.

Inspired by circular loom thread weaving, mathematical ruled-surface ribbons, and optical caustic interference, this project implements a dual-mode art engine running silky-smooth at 60 FPS in **Pygame-CE**:

1. **Mode 1: The Masterpiece Weaver (Exact Reference Artwork)**:
   - Faithfully weaves the exact reference artwork (`spiral_vortex_art.jpg`) stroke-by-stroke with **8,200+ translucent vector silk threads**.
   - Structured across 4 chromatic and anatomical layers:
     - **Layer 1: Outer Halo & Perimeter Rings**: Ethereal blush rose (`#C8B4B4`) and silver (`#8A8A92`) concentric boundary loops.
     - **Layer 2: Structural Ribbons & Mid-Tone Gauze**: Translucent graphite threads forming the swirling body and inner vortex eye.
     - **Layer 3: Terracotta & Copper Folded Ribbon Accent**: Warm earth tone (`#B96E5F`) folded ribbon lobe in the upper right.
     - **Layer 4: Deep Charcoal & Black Caustic Pinches**: Intense focal pinch fold in the lower left (`#121316`).
   - Guided by an active golden drafting stylus cursor with soft drifting stardust particles.

2. **Mode 2: Live Parametric Vortex Studio**:
   - Real-time mathematical ribbon simulation driven by multi-layered logarithmic spiral spines, harmonic ribbon widths, and ruled-surface cross-chords.
   - **Interactive Mouse Gravity Warp**: Move or drag the mouse to dynamically bend, twist, and pull the vortex field with spring physics.
   - **Scroll-Wheel Fractal Zoom**: Zoom seamlessly into the hypnotic central singularity.
   - **5 Curated Color Themes**: Studio Minimalist, Obsidian Gold, Cyberpunk Neon, Emerald Aurora, and Monochrome Blueprint.

---

## 🧠 Algorithmic Pipeline & Mechanics

```
┌─────────────────────────────────┐
│      Reference Masterpiece      │
│      spiral_vortex_art.jpg      │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Vector Tangent Field Analysis   │ Sobel gradients & structure tensor ((-gy, gx) / ||g||)
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 4-Layer Probabilistic Sampling  │ Halo, Mid-Tone Gauze, Terracotta Lobe, Charcoal Caustics
└────────────────┬────────────────┘
                 │
      ┌──────────┴──────────────────────────┐
      ▼                                     ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│ Mode 1: Masterpiece Weaver│ │ Mode 2: Parametric Studio │
│ • 8,200+ vector threads   │ │ • Real-time 60 FPS math   │
│ • Golden stylus & stardust│ │ • Logarithmic spiral spine│
│ • Alpha gauze caustics    │ │ • Mouse gravity warping   │
│ • Centripetal spiral sweep│ │ • 5 live color palettes   │
└─────────────┬─────────────┘ └─────────────┬─────────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │ Hardware Pygame Compositor  │
              │ • 32-bit SRCALPHA surface   │
              │ • Dynamic telemetry HUD     │
              │ • Instant screenshot export │
              └─────────────────────────────┘
```

### 1. Vector Tangent Field Integration
The engine converts the raster artwork into a continuous vector direction field using Sobel operator gradients:
$$\mathbf{T}(x, y) = \frac{(-G_y, G_x)}{\sqrt{G_x^2 + G_y^2 + \epsilon}}$$
Streamlines are integrated bi-directionally along $\mathbf{T}(x, y)$ using Runge-Kutta / Euler integration, tracing out natural silk fibers that naturally congregate where caustics fold and pinch.

### 2. Ruled Surface & Transverse Chords (Mode 2)
In the Parametric Studio, ribbons are generated from $K$ logarithmic spiral curves:
$$r_k(t) = \left(r_0 + R_0 t^{0.85}\right) \cdot Z, \quad \theta_k(t) = t \cdot \omega \pi + \phi_k + \Omega t$$
Transverse ruled-surface cross-chords connect opposing edges $\mathbf{p}_1(t) = \mathbf{c}(t) + W(t)\mathbf{n}(t)$ and $\mathbf{p}_2(t) = \mathbf{c}(t) - W(t)\mathbf{n}(t)$ with harmonic width modulation:
$$W(t) = \left(w_0 + w_1 \sin(6\pi t + 1.5\phi_k)(1 - 0.35t)\right) \cdot S_w$$

---

## 🎮 Interactive Keyboard & Mouse Controls

| Key / Input | Action | Mode | Description |
| :---: | :--- | :---: | :--- |
| **`[1]`** | **Masterpiece Weaver** | Global | Switches to Mode 1 (Exact reference reproduction) |
| **`[2]`** | **Parametric Studio** | Global | Switches to Mode 2 (Interactive real-time ribbon studio) |
| **`[SPACE]`** | **Pause / Resume** | Global | Freezes animation / drawing loop |
| **`[T]`** | **Cycle Themes** | Mode 2 | Cycles 5 palettes (Studio, Obsidian, Cyberpunk, Emerald, Blueprint) |
| **`[M]`** | **Mouse Gravity Warp**| Mode 2 | Toggles mouse gravitational field pull on ribbons |
| **`[Mouse Wheel]`**| **Fractal Zoom** | Mode 2 | Smoothly zooms in/out of the vortex core ($0.4\times$ to $3.5\times$) |
| **`[W]` / `[S]`** | **Ribbon Width** | Mode 2 | Expands or contracts transverse chord width |
| **`[F]` / `[D]`** | **Spiral Twist** | Mode 2 | Increases or decreases twist frequency |
| **`[+]` / `[-]`** | **Speed / Density** | Both | Adjusts thread batch rate (Mode 1) or frequency (Mode 2) |
| **`[C]`** | **Fast-Forward** | Mode 1 | Instantly completes drawing the full artwork |
| **`[R]`** | **Restart / Reset** | Both | Restarts drawing pass or resets camera/parameters |
| **`[A]`** | **Auto-Loop** | Mode 1 | Toggles automatic reset on completion |
| **`[H]`** | **Toggle HUD** | Global | Hides/shows telemetry info banner |
| **`[P]` / `[S]`** | **Export PNG** | Global | Saves high-resolution screenshot to `output/` |
| **`[ESC]` / `[Q]`**| **Exit** | Global | Safely shuts down application |

---

## 🛠️ Installation & Dependencies

Ensure Python 3.10+ is installed:

```bash
pip install pygame-ce opencv-python-headless numpy pillow
```

---

## 🚀 How to Run

Run directly from the repository root:

```bash
python "days/Day-18-Spiral-Vortex-Art/main.py"
```

Or navigate into the project directory:

```bash
cd "days/Day-18-Spiral-Vortex-Art"
python main.py
```

To run in headless export mode (generating poster & animation preview):

```bash
python main.py --export
```

---

## 📁 Project Structure

```text
Day-18-Spiral-Vortex-Art/
├── README.md               # Comprehensive project documentation
├── main.py                 # Complete executable dual-mode art engine
└── spiral_vortex_art.jpg   # Reference generative artwork
```

---

<p align="center">
  <b>30 Days Python Challenge</b> · Made with ❤️ and Python by <a href="https://github.com/Tejas0113">@Tejas0113</a>
</p>

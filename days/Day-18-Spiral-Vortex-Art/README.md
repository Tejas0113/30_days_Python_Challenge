# 🌀 Day 18: Generative Parametric Spiral Vortex Art (High-Definition Edition)

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day18_animation.gif" alt="Generative Parametric Spiral Vortex Art Preview" width="540px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(195, 85, 65, 0.40);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Parametric%20Caustics-C35541?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 18 delivers a mesmerizing, high-definition generative simulation: **Generative Parametric Spiral Vortex Art (High-Definition Edition)**.

Inspired by circular loom thread weaving, mathematical ruled-surface ribbons, and optical caustic interference, this project implements a dual-mode art engine running silky-smooth at 60 FPS in **Pygame-CE**:

1. **Mode 1: The Masterpiece Weaver (Enhanced High-Contrast Edition)**:
   - Faithfully weaves the reference artwork (`spiral_vortex_art.jpg`) stroke-by-stroke with **28,000+ precision vector threads** across 5 distinct thematic layers:
     - **Layer 1: Outer Halo & Perimeter Rings**: Ethereal blush rose (`#C8B4B4`) and silver (`#8A8A92`) concentric boundary loops.
     - **Layer 2: Structural Gauze & Body Swirls**: Dense graphite threads forming the swirling body and inner vortex eye.
     - **Layer 3: Terracotta & Copper Folded Ribbon Accent**: Rich, vibrant warm earth tone (`#C35541`) folded ribbon lobe in the upper right.
     - **Layer 4: Deep Charcoal & Black Caustic Pinches**: Intense, velvety black focal pinch fold (`#101114`) in the lower left.
     - **Layer 5: Crisp Caustic Edge Filaments**: Razor-sharp structural boundary contours defining the folds, eyes, and perimeter.
   - **Dynamic Contrast & Opacity Booster (`[B]` / `[V]`)**: Instantly dials up/down thread opacity and visual punchiness on the fly.
   - **Dual-Canvas Modes (`[T]`)**: Seamlessly toggle between Studio Gallery White and Obsidian Dark Glow.
   - Guided by an active golden drafting stylus cursor with soft drifting stardust particles.

2. **Mode 2: Live Parametric Vortex Studio (Diamond Moiré Lattice)**:
   - Real-time 60 FPS mathematical ribbon simulation driven by multi-layered logarithmic spiral spines, harmonic ribbon widths, and cross-braided diamond moiré ruled-surface chords.
   - **Harmonic Breathing Organism**: Ribbons smoothly expand and contract with organic wave pulsation (`[G]`).
   - **Interactive Mouse Gravity Warp**: Move or drag the mouse to dynamically bend, twist, and pull the vortex field with spring physics (`[M]`).
   - **Scroll-Wheel Fractal Zoom**: Zoom seamlessly into the hypnotic central singularity ($0.3\times$ to $4.0\times$).
   - **6 Curated Color Themes**: Studio Minimalist, Obsidian Gold, Cyberpunk Neon, Emerald Aurora, Monochrome Blueprint, and Royal Amethyst.

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
│ Vector Tangent Field & Canny    │ Sobel gradients ((-gy, gx) / ||g||) + Canny structural edges
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 5-Layer Probabilistic Sampling  │ Halo, Structural Gauze, Terracotta Lobe, Charcoal, Edge Filaments
└────────────────┬────────────────┘
                 │
      ┌──────────┴──────────────────────────┐
      ▼                                     ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│ Mode 1: Masterpiece Weaver│ │ Mode 2: Parametric Studio │
│ • 28,000+ vector threads  │ │ • Real-time 60 FPS math   │
│ • Golden stylus & stardust│ │ • Counter-twist diamond   │
│ • Contrast booster [B/V]  │ │ • Mouse gravity warping   │
│ • Dark/Light canvas [T]   │ │ • 6 live color palettes   │
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

---

## 🎮 Interactive Keyboard & Mouse Controls

| Key / Input | Action | Mode | Description |
| :---: | :--- | :---: | :--- |
| **`[1]`** | **Masterpiece Weaver** | Global | Switches to Mode 1 (Exact reference reproduction) |
| **`[2]`** | **Parametric Studio** | Global | Switches to Mode 2 (Interactive real-time ribbon studio) |
| **`[SPACE]`** | **Pause / Resume** | Global | Freezes animation / drawing loop |
| **`[B]` / `[V]`** | **Boost / Reduce Contrast**| Both | Dynamically dials up/down thread opacity and visual punchiness |
| **`[T]`** | **Theme / Canvas Mode** | Both | Cycles themes (Mode 2) or toggles Dark/Light canvas (Mode 1) |
| **`[M]`** | **Mouse Gravity Warp**| Mode 2 | Toggles mouse gravitational field pull on ribbons |
| **`[G]`** | **Harmonic Breathing**| Mode 2 | Toggles organic harmonic pulsation |
| **`[Mouse Wheel]`**| **Fractal Zoom** | Mode 2 | Smoothly zooms in/out of the vortex core ($0.3\times$ to $4.0\times$) |
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

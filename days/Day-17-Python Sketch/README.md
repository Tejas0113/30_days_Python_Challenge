# 🐍 Day 17: Albino Python Realistic Digital Sketch Art

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day17_animation.gif" alt="Albino Python Realistic Digital Sketch Art Preview" width="520px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(118, 1, 7, 0.45);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Digital%20Sketching-760107?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 17 elevates the challenge with a high-fidelity digital art drawing simulation: **Albino Python Realistic Digital Sketch Art**.

Translating a photorealistic illustration of a coiled albino python on deep crimson paper (`python snake image.jpeg`), this project implements an authentic multi-stage sketch animation engine that delivers **100% exact visual fidelity with silky-smooth rendering**:
1. **Exact Reference Fidelity (Zero Blocky Noise)**: Faithfully reproduces every pearlescent scale, iridescent highlight, peach underbelly ventral plate, glowing ruby-red eye, forked tongue, and rich crimson vignette.
2. **Phase 1: Anatomical Contour Underdrawing**: An ergonomic artist stylus glides along the OpenCV-extracted anatomical contours, sketching out the coiled body, head plates, eye, and tongue in delicate graphite strokes.
3. **Phase 2: Progressive Volumetric Shading & Scale Revealing**: The pencil sweeps across the snake in continuous diagonal bands, smoothly rendering small portions (brush radius ~26 px) of the photorealistic 3D scales.
4. **Ergonomic 3D Artist Stylus**: An authentic pencil model leads the stroke with an active pigment lead tip, cedar wood cone, colored barrel, and floating graphite dust particles.

---

## 🧠 Algorithmic Pipeline & Mechanics

```
┌─────────────────────────────────┐
│     Reference Masterpiece       │
│    python snake image.jpeg      │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ OpenCV Bilateral Contour Pass   │ Extracts 1,300+ smooth anatomical sketch paths
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Continuous Diagonal Trajectory  │ Generates serpentine corner-to-corner sweep bands
└────────────────┬────────────────┘
                 │
      ┌──────────┴──────────────────────────┐
      ▼                                     ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│ Phase 1: Underdrawing     │ │ Phase 2: Scale Shading    │
│ • Graphite sketch lines   │ │ • Progressive revelation  │
│ • S-coils & head plates   │ │ • Exact pixel fidelity    │
│ • Fierce ruby eye & tongue│ │ • Active lead tip color   │
└─────────────┬─────────────┘ └─────────────┬─────────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │ Hardware 60 FPS Pygame Loop │
              │ • 3D artist pencil model    │
              │ • Real-time telemetry HUD   │
              │ • Vice-Versa & loop control │
              └─────────────────────────────┘
```

### 1. Dynamic Path Resolution
Eliminates brittle hardcoded absolute filesystem paths (`/days/...`) that cause immediate crashes on Unix/macOS environments. Automatically locates `python snake image.jpeg` whether invoked from the repository root, within the project folder, or via an IDE run configuration.

### 2. Anatomical Contour Sketching (Phase 1)
Extracts over 1,300 ordered contour curves using Canny gradient thresholds ($T_1 = 35, T_2 = 110$) and bilateral filtering. The artist's pencil traces the body curves, jawline, eye socket, and forked tongue, leaving delicate pencil sketch lines on the crimson canvas.

### 3. Continuous Diagonal Trajectory Generation (Phase 2)
Generates continuous zig-zag diagonal bands across the canvas ($x + y = d$), ensuring complete, seamless coverage from Top-Left to Bottom-Right (or Vice-Versa). At each point, small portions (radius ~26 px) of the master image are revealed directly under the pencil tip.

### 4. Dynamic Lead Color & Graphite Particles
The pencil tip samples the exact RGB pigment of the active contact coordinate, dynamically adapting its lead color as it passes over pearlescent scales, pinkish scutes, or the incandescent ruby iris. Subtle graphite dust particles drift gently from the active stroke.

---

## 🎮 Interactive Keyboard Controls

During animation, interact with the canvas in real time:

| Key | Action | Description |
| :---: | :--- | :--- |
| **`[SPACE]`** | **Pause / Resume** | Freezes the drawing loop to inspect individual pencil strokes |
| **`[V]`** | **Vice-Versa** | Inverts sweep direction between Top-Left and Bottom-Right |
| **`[R]`** | **Restart** | Restarts the current drawing pass from the beginning |
| **`[A]`** | **Auto-Loop** | Toggles continuous cyclic redrawing |
| **`[+]` / `[UP]`** | **Speed Up** | Increases stroke points rendered per frame |
| **`[-]` / `[DOWN]`** | **Slow Down** | Reduces speed for meditative viewing |
| **`[1]` – `[4]`** | **Speed Presets** | Instant presets (1: Meditative, 2: Standard, 3: Fast, 4: Turbo) |
| **`[C]` / `[F]`** | **Fast-Forward** | Instantly reveals the complete finished artwork |
| **`[S]`** | **Save Artwork** | Exports a pixel-perfect high-resolution PNG to `output/` |
| **`[ESC]` / `[Q]`** | **Exit** | Safely shuts down window |

---

## 🛠️ Installation & Dependencies

Ensure Python 3.10+ is installed:

```bash
pip install pygame-ce opencv-python numpy pillow
```

---

## 🚀 How to Run

Run directly from the repository root:

```bash
python "days/Day-17-Python Sketch/main.py"
```

Or navigate to the project folder:

```bash
cd "days/Day-17-Python Sketch"
python main.py
```

---

## 📁 Project Structure

```text
Day-17-Python Sketch/
├── README.md                  # Comprehensive project documentation
├── main.py                    # Complete executable sketch & animation script
└── python snake image.jpeg    # Reference albino python crouching artwork
```

---

<p align="center">
  <b>30 Days Python Challenge</b> · Made with ❤️ and Python by <a href="https://github.com/Tejas0113">@Tejas0113</a>
</p>

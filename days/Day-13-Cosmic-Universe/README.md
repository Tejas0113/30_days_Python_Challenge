# 🌌 Day 13: Cosmic Universe - Progressive Corner Drawing & Vice-Versa Simulation

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day13_animation.gif" alt="Cosmic Universe Progressive Corner Drawing and Vice-Versa Animation" width="640px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(120, 230, 255, 0.4);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Visual%20Simulation-00f0ff?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 13 delivers an authentic, deeply satisfying digital drawing simulation: **Cosmic Universe - Progressive Corner Drawing & Vice-Versa Simulation**.

The application draws the exact, pristine Cosmic Universe image slowly and steadily from corner to corner:
1. **100% Exact Image Fidelity**: Faithful, bit-for-bit reproduction of the original cosmic universe image without artificial geometric overlays, fake circles, or cartoon spikes. Every star, glowing gas filament, and golden cosmic cliff is directly revealed from the master artwork.
2. **Visible Portion Revealing**: As the pencil glides across the canvas, every stroke transfers a distinct, visible circular portion (radius $24\text{ px}$, diameter $\sim 48\text{ px}$) of the real cosmic nebula, letting you watch the entire universe emerge piece by piece.
3. **Corner-to-Corner Trajectories**:
   - **Forward**: Begins cleanly in deep cosmic space at **Top-Left Corner $(0, 0)$** and sweeps along continuous diagonal bands across to **Bottom-Right Corner $(1280, 640)$**.
   - **Vice-Versa**: Draws from **Bottom-Right Corner $(1280, 640)$** back to **Top-Left Corner $(0, 0)$**, sculpting the incandescent horizon cliffs first and sweeping towards deep space.
   - **Auto-Loop**: Automatically alternates between Forward and Vice-Versa passes in a continuous, hypnotic loop.
4. **Ergonomic Colored Pencil Stylus**: An authentic vector stylus leads the active drawing front:
   - Dynamic lead tip adopting the exact color of the active cosmic pigment.
   - Active brush radius guide ring showing the visible portion being revealed.
   - Sharpened cedar wood cone and 3D hexagonal barrel with golden ferrule.
   - Micro-stardust particles emitting from the contact point.
5. **Zero Sudden Image Jumps**: Overlapping strokes achieve 100% genuine canvas coverage—there are no sudden flashes or abrupt replacements.

---

## 🧠 Concepts & Mathematical Mechanics

### 1. Diagonal Serpentine Manifold & Coverage ($x + y = d$)
To simulate natural hand hatching, the canvas is parameterized by diagonal level sets:

$$d = x + y, \quad d \in [0, W + H]$$

For each diagonal band $d$ spaced by $\Delta d = \lfloor R \cdot 0.85 \rfloor = 20\text{ px}$:
- Bounding coordinate range: $x_{\min} = \max(0, d - H)$, $x_{\max} = \min(W, d)$
- Direction alternates per band $i$ for continuous serpentine continuity:
  $$\mathbf{x}(s) = \begin{cases} (1 - s) x_{\min} + s\, x_{\max}, & i \text{ is even} \\ (1 - s) x_{\max} + s\, x_{\min}, & i \text{ is odd} \end{cases}$$
- **Forward Trajectory**: $\mathcal{P}_{\text{fwd}} = [\mathbf{p}_0, \mathbf{p}_1, \dots, \mathbf{p}_N]$ from $(0, 0) \to (W, H)$.
- **Vice-Versa Trajectory**: $\mathcal{P}_{\text{rev}} = \mathcal{P}_{\text{fwd}}^{-1} = [\mathbf{p}_N, \mathbf{p}_{N-1}, \dots, \mathbf{p}_0]$ from $(W, H) \to (0, 0)$.

### 2. High-Fidelity Master Pixel Sampling
At each drawing step $\mathbf{p} = (p_x, p_y)$, the exact pixel patch is copied from the scaled master surface:

$$\Omega_{\text{brush}}(\mathbf{p}) = [p_x - R, p_x + R] \times [p_y - R, p_y + R]$$

Ensuring that by the time the trajectory reaches the opposite corner, 100% of the canvas has been covered with zero missing pixels, rendering the identical cosmic universe master image.

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3.10+
- **Core Libraries**:
  - `pygame` / `pygame-ce` — 60 FPS hardware-accelerated rendering, alpha compositing, and user interaction.
  - `numpy` — Fast array operations and surface coordinate buffers.
  - `pillow` — Preview asset exports.

---

## 🚀 How to Run

From the repository root:

```bash
python days/Day-13-Cosmic-Universe/main.py
```

### 🎮 Keyboard & Mouse Controls

| Input | Action |
| :---: | :--- |
| **`[SPACE]`** | Pause / Resume drawing animation |
| **`[V]`** | Toggle Vice-Versa corner direction (Top-Left $\leftrightarrow$ Bottom-Right) |
| **`[R]`** | Restart current drawing from corner |
| **`[A]`** | Toggle Auto-Loop Vice-Versa cycle (on by default) |
| **`[+]` / `[UP]`** | Increase drawing speed (+1 pt/frame) |
| **`[-]` / `[DOWN]`** | Decrease drawing speed (-1 pt/frame) |
| **`[1]` - `[4]`** | Preset speeds (1: Meditative, 2: Standard, 3: Fast, 4: Turbo) |
| **`[S]`** | Save high-resolution screenshot (`cosmic_universe_*.png`) |
| **`[F]`** | Toggle fullscreen mode |
| **`[ESC]` / `[Q]`** | Exit application cleanly |
| **Mouse Move** | Interactive luminous stardust particles drift across canvas |

---

<p align="center">
  <a href="../../README.md"><b>⬅️ Return to 30 Days Challenge Tracker</b></a>
</p>

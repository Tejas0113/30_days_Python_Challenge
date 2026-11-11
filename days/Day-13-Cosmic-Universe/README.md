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

Instead of abrupt reveals or noisy digital static, the drawing tool glides from corner to corner, progressively rendering clearly visible portions of the cosmic universe onto the canvas:
1. **Corner-to-Corner Progressive Drawing**: Begins cleanly in deep cosmic space (`#050610`) at one corner and sweeps along continuous diagonal bands across the entire canvas.
2. **Visible Portion Revealing**: Every stroke renders a distinct circular portion (radius $24\text{ px}$, diameter $\sim 48\text{ px}$) of the cosmic nebula, letting you watch each stellar filament, cyan gas cloud, and fiery golden cosmic ridge emerge piece by piece.
3. **Vice-Versa Mode**:
   - **Forward**: Draws from Top-Left `(0, 0)` down to Bottom-Right `(1280, 640)`.
   - **Vice-Versa**: Draws from Bottom-Right `(1280, 640)` up to Top-Left `(0, 0)`, sculpting the incandescent horizon cliffs first and sweeping towards deep space.
   - **Auto-Loop**: Automatically alternates between Forward and Vice-Versa passes in a continuous, hypnotic loop.
4. **Ergonomic Colored Pencil Stylus**: An authentic vector stylus leads the active drawing front:
   - Dynamic lead tip adopting the exact color of the active cosmic pigment.
   - Active brush radius guide ring showing the visible portion being revealed.
   - Sharpened cedar wood cone and 3D hexagonal barrel with golden ferrule.
   - Graphite and stardust micro-particles emitting from the contact point.
5. **Zero Sudden Image Jumps**: Overlapping circular portions achieve 100% genuine canvas coverage—there are no sudden flashes or abrupt replacements.
6. **Stellar Ignition & Living Cosmos Mode**: Upon completing each pass, astronomical 4-point cross diffraction spikes flare on prominent star cores with gentle organic twinkling and interactive cursor stardust.

---

## 🧠 Concepts & Mathematical Mechanics

### 1. Diagonal Serpentine Manifold & Coverage ($x + y = d$)
To simulate natural hand hatching, the canvas is parameterized by diagonal level sets:

$$d = x + y, \quad d \in [-R, W + H + R]$$

For each diagonal band $d$ spaced by $\Delta d = \lfloor R \cdot 0.85 \rfloor = 20\text{ px}$:
- Bounding coordinate range: $x_{\min} = \max(-R, d - H - R)$, $x_{\max} = \min(W + R, d + R)$
- Direction alternates per band $i$ for continuous serpentine continuity:
  $$\mathbf{x}(s) = \begin{cases} (1 - s) x_{\min} + s\, x_{\max}, & i \text{ is even} \\ (1 - s) x_{\max} + s\, x_{\min}, & i \text{ is odd} \end{cases}$$
- **Forward Trajectory**: $\mathcal{P}_{\text{fwd}} = [\mathbf{p}_0, \mathbf{p}_1, \dots, \mathbf{p}_N]$ from $(0, 0) \to (W, H)$.
- **Vice-Versa Trajectory**: $\mathcal{P}_{\text{rev}} = \mathcal{P}_{\text{fwd}}^{-1} = [\mathbf{p}_N, \mathbf{p}_{N-1}, \dots, \mathbf{p}_0]$ from $(W, H) \to (0, 0)$.

### 2. Multiplicative Alpha Circle Blitting
At each drawing step $\mathbf{p} = (p_x, p_y)$, a circular portion is transferred from the scaled master surface using an alpha-multiplied circular mask:

$$\Omega_{\text{brush}}(\mathbf{x}) = \begin{cases} 1.0, & \|\mathbf{x} - \mathbf{p}\| \le R \\ 0.0, & \text{otherwise} \end{cases}$$

$$\mathbf{C}_{\text{canvas}}(\mathbf{x}) \leftarrow \mathbf{C}_{\text{canvas}}(\mathbf{x}) \odot (1 - \Omega) + \mathbf{C}_{\text{master}}(\mathbf{x}) \odot \Omega$$

This produces authentic painterly edges while ensuring that when the trajectory completes, the union $\bigcup \Omega_{\text{brush}}$ covers 100% of the canvas with zero missing pixels.

### 3. Astronomical 4-Point Diffraction Spike Optics
Prominent stars exhibit diffraction spikes caused by telescope spider vanes. Modeled mathematically using linear intensity decays with core Gaussian bloom:

$$I_{\text{spike}}(d) = I_0 \cdot \max\left(0, 1 - \frac{|d|}{L}\right)$$

Rendered with central luminous white discs, golden outer halos ($R \approx 20\text{ px}$), and orthogonal spikes spanning $L \approx 140\text{ px}$.

### 4. Harmonic Stellar Twinkle Physics
In the Living Cosmos phase, stars shimmer organically using sinusoidal phase shifts:

$$r_{\text{eff}}(t) = r_0 \left(1.0 + 0.16 \sin\left(\omega t + \phi_k\right)\right), \quad \phi_k \sim \mathcal{U}(0, 2\pi)$$

delivering a natural, breathing night sky.

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3.10+
- **Core Libraries**:
  - `pygame` / `pygame-ce` — 60 FPS hardware-accelerated rendering, alpha compositing, and user interaction.
  - `numpy` — Fast array operations, surface coordinate buffers, and brightness analysis.
  - `pillow` — Lanczos resampling and preview asset exports.

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

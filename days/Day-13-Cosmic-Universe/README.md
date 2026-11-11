# 🌌 Day 13: Cosmic Universe - Generative Digital Painting & Stellar Ignition

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day13_animation.gif" alt="Cosmic Universe Generative Painting Animation Preview" width="640px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(120, 230, 255, 0.4);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Volumetric%20Painting-00f0ff?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 13 brings an authentic, hypnotic generative painting experience: **Cosmic Universe - Generative Digital Painting & Stellar Ignition**.

The program simulates the steady, organic brushwork of a digital master artist, slowly bringing the entire celestial masterpiece to life in a 60 FPS hardware-accelerated Pygame window:
1. **Clean Cosmic Void Inception**: Begins in a deep interstellar space canvas (`#050610`) populated by subtle ambient stars.
2. **Organic Celestial Brush Trajectory**: A glowing celestial stylus (white core + warm golden corona) glides smoothly across the canvas in rhythmic, undulating sweeps, progressively painting the exact, saturated colors of the nebula.
3. **Zero Noise, 100% Exact High-Fidelity Convergence**: Every single stroke reveals the pristine master artwork—from the emerald-turquoise clouds on the left to the radiant azure valley, rose-magenta stellar nursery, and fiery golden cosmic cliffs along the horizon. No noise, no blur, no missed details.
4. **Stellar Birth & Diffraction Flare Ignition**: As the painting nears completion, the prominent stars ignite in sequence—featuring the iconic 4-point golden cross star in the lower-left with radiating horizontal and vertical diffraction spikes, the upper golden star, and the cyan nursery core.
5. **Living Cosmos Interactive Mode**: Once painted, the universe remains alive with gentle stellar twinkling, breathing incandescent core flares, and real-time interactive stardust that responds to cursor movement.

---

## 🧠 Concepts & Mathematical Mechanics

### 1. Multi-Scale Volumetric Gaussian Pyramid Blur Decomposition
Atmospheric nebula clouds possess multi-scale spatial characteristics. The reference image $I_0$ is decomposed into a pyramid of Gaussian-blurred representations:

$$I_\sigma(x, y) = I_0(x, y) * G_\sigma(x, y), \quad \text{where } G_\sigma(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2 + y^2}{2\sigma^2}}$$

- **Coarse Atmospheric Map ($\sigma = 32$)**: Guides large orbital wash strokes (radius $45\text{--}90\text{ px}$) during early cloud inception.
- **Medium Texture Map ($\sigma = 10$)**: Supplies volumetric density for the billowing pillars.
- **Master Fidelity Map ($\sigma = 0$)**: Guarantees zero loss of high-frequency micro-features during the final convergence phase.

### 2. 2D Sobel Directional Gradient Ridge Sculpting
To paint clouds and ridges naturally, brush strokes must align with the physical flow of the gas contours. First-order Sobel derivatives calculate spatial gradient vectors:

$$G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix} * I, \quad G_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix} * I$$

$$\|\nabla I\| = \sqrt{G_x^2 + G_y^2}, \quad \theta = \operatorname{atan2}(G_y, G_x) + \frac{\pi}{2}$$

Brush strokes are oriented tangentially along $\theta$ with stroke length modulated by gradient magnitude $\|\nabla I\|$, reproducing the natural, turbulent swirls of cosmic dust clouds.

### 3. Astronomical 4-Point Diffraction Spike Optics
Prominent stars exhibit diffraction spikes caused by the spider vanes of astronomical telescopes. These are modeled mathematically using linear intensity decays with core Gaussian bloom:

$$I_{\text{spike}}(d) = I_0 \cdot \max\left(0, 1 - \frac{|d|}{L}\right)$$

Rendered with central luminous white discs, golden outer halos ($R \approx 20\text{ px}$), and orthogonal spikes spanning $L \approx 140\text{ px}$.

### 4. Harmonic Stellar Twinkle Physics
In the Living Cosmos phase, stars shimmer organically using sinusoidal phase shifts:

$$r_{\text{eff}}(t) = r_0 \left(1.0 + 0.28 \sin\left(\omega t + \phi_k\right)\right), \quad \phi_k \sim \mathcal{U}(0, 2\pi)$$

preventing uniform blinking and delivering a natural, breathing night sky.

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3.10+
- **Core Libraries**:
  - `pygame` / `pygame-ce` — 60 FPS hardware-accelerated rendering, alpha compositing, and user interaction.
  - `opencv-python-headless` — Bilateral filtering, multi-scale Gaussian blurring, and Sobel gradient field extraction.
  - `numpy` — Fast array operations, surface transposed coordinate buffers, and polar transformations.
  - `pillow` — Lanczos resampling and high-res asset exports.

---

## 🚀 How to Run

From the repository root:

```bash
python days/Day-13-Cosmic-Universe/main.py
```

### 🎮 Keyboard & Mouse Controls

| Input | Action |
| :---: | :--- |
| **Mouse Move** | Spawns interactive glowing stardust that drifts across the cosmos |
| **`[SPACE]`** | Replays the slow generative painting sequence from scratch |
| **`[S]`** | Saves a high-resolution screenshot (`cosmic_universe_screenshot.png`) |
| **`[F]`** | Toggles fullscreen mode |
| **`[ESC]` / `[Q]`** | Exits application cleanly |

---

<p align="center">
  <a href="../../README.md"><b>⬅️ Return to 30 Days Challenge Tracker</b></a>
</p>


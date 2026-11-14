# 🐍 Day 17: Albino Python Realistic Vector Sketch Art

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day17_animation.gif" alt="Albino Python Realistic Vector Sketch Art Preview" width="520px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(118, 1, 7, 0.45);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Vector%20Inking-760107?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 17 brings the elegance of nature to life through algorithmic creative coding: **Albino Python Realistic Vector Sketch Art**.

Translating a photorealistic illustration of a coiled albino python on deep crimson paper (`python snake image.jpeg`), this project builds a complete dual-phase vector drawing animation engine that faithfully reproduces:
1. **The Exact Chromatic Palette**: Deep crimson vignette backdrop (`#760107` / `#9E080D`), pearlescent albino body scales, soft peach underbelly ventral scutes, and a glowing ruby-red eye with a vertical viper pupil.
2. **Phase 1: Anatomic Coils & Flats**: Deconstructs the snake's muscular S-coiled form into geometric color polygons using 24-cluster K-Means quantization and area-sorted rendering.
3. **Phase 2: Scale Inking & Head Features**: Traces thousands of overlapping diamond scale contours, cephalic head plates, nostrils, and the delicate forked tongue with a precision inking pen.

---

## 🧠 Algorithmic Pipeline & Architecture

```
┌─────────────────────────────────┐
│     Reference Snake Image       │
│    python snake image.jpeg      │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│    Bilateral Surface Filter     │ Smooths micro-noise while locking scale ridges
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ 24-Cluster K-Means Palette      │ Captures crimson gradients, ivory scales & ruby eye
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Background Calibration & Mask   │ Samples paper tone (#760107); isolates serpent body
└────────────────┬────────────────┘
                 │
      ┌──────────┴──────────────────────────┐
      ▼                                     ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│ Phase 1: Anatomic Flats   │ │ Phase 2: Scale & Head Ink │
│ • Area-sorted hierarchy   │ │ • Canny edge detection    │
│ • Pearlescent body coils  │ │ • Cephalic plates & eye   │
│ • Ventral belly shading   │ │ • Forked tongue contour   │
└─────────────┬─────────────┘ └─────────────┬─────────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │ Python Turtle Graphics Loop │
              │ • Normalized world coords   │
              │ • setworldcoordinates 450   │
              │ • Live progress & controls  │
              └─────────────────────────────┘
```

### 1. Dynamic Path Resolution
Eliminates brittle hardcoded absolute filesystem paths (`/days/...`) that cause immediate crashes on Unix/macOS environments. Automatically locates `python snake image.jpeg` whether invoked from the repository root, within the project folder, or via an IDE run configuration.

### 2. Normalized World Coordinates Viewport (`setworldcoordinates`)
Configures Turtle with `setworldcoordinates(-450, -450, 450, 450)` over an $850 \times 850$ canvas. This guarantees:
- **Zero Edge Clipping**: Generous padding on all four borders so no coils or tongue tips are cut off.
- **Harmonious Aspect Ratio**: Proportions remain crisp and undistorted across different monitor sizes or window resizing.
- **Isotropic Centering**: All extracted vector coordinates are aligned relative to $(0, 0)$ center-origin.

### 3. K-Means Chromatic Quantization ($K = 24$)
Groups continuous tone gradients into 24 discrete color clusters using Lloyd's Euclidean distance minimization:

$$\arg\min_{\mathbf{S}} \sum_{i=1}^{k} \sum_{\mathbf{x} \in S_i} \|\mathbf{x} - \boldsymbol{\mu}_i\|^2$$

This isolates the rich crimson background tones, ivory and alabaster dorsal scales, soft blush ventral scutes, and the incandescent ruby iris.

### 4. Area-Sorted Layer Hierarchy
Polygons are sorted by descending contour area ($\text{Area} \downarrow$):
- **Base Flats First**: Large body coils and musculature foundations are laid down first as solid colored flats.
- **Details on Top**: Small scale facets, cephalic head plates, and specular highlights are drawn last, ensuring critical details are never obscured by larger shapes.

### 5. Scale Inking & Feature Pass
Extracts high-frequency scale boundaries using Canny gradient thresholds ($T_1 = 35, T_2 = 105$). Turtle switches to an inking pen (`pensize = 1.2`, `#2B040A`) and sketches individual scale outlines, cephalic plates, nostril pits, and the delicate forked tongue.

---

## 🎮 Interactive Keyboard Controls

During animation, interact with the canvas in real time:

| Key | Action | Description |
| :---: | :--- | :--- |
| **`[Space]`** | **Pause / Resume** | Freezes the drawing loop to inspect individual polygon strokes |
| **`[+]` / `[=]` / `[↑]`** | **Speed Up** | Increases shapes drawn per frame buffer update |
| **`[-]` / `[_]` / `[↓]`** | **Slow Down** | Reduces speed to closely follow the pen cursor motion |
| **`[C]`** | **Fast-Forward** | Instantly completes all remaining polygons and ink lines |
| **`[S]`** | **Save Artwork** | Exports a pixel-perfect high-resolution PNG to `output/` |
| **`[Q]` / `[Esc]`** | **Graceful Exit** | Safely shuts down window without terminal tracebacks |

---

## 🛠️ Installation & Dependencies

Ensure Python 3.10+ is installed along with OpenCV and NumPy:

```bash
pip install opencv-python numpy pillow
```

> **Note**: `turtle` and `tkinter` are included by default in standard Python distributions.

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

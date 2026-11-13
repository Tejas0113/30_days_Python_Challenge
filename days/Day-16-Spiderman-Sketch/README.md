# 🕷️ Day 16: Spider-Man Comic Vector Sketch Art

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day16_animation.gif" alt="Spider-Man Comic Vector Sketch Art Preview" width="520px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(220, 38, 38, 0.35);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Vector%20Inking-dc2626?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 16 brings Marvel's iconic web-slinger to life through algorithmic creative coding: **Spider-Man Comic Vector Sketch Art**.

Inspired by viral computational art reels where Python Turtle sketches complex comic illustrations piece by piece, this project transforms a high-contrast raster drawing of Spider-Man into a dynamic, two-phase vector drawing animation:
1. **Phase 1: Vector Color Polygons (Comic Flats)**: Deconstructs the suit into geometric color polygons using K-Means clustering and Douglas-Peucker contour simplification. Turtle glides across the canvas, laying down each polygon with dark comic seams.
2. **Phase 2: Silk Web Lines & Comic Inking**: Traces the intricate web patterns across Spider-Man's mask and suit, plus dramatic ink cross-hatching and muscle outlines with a fine-point inking pen.

The result is a responsive, hardware-friendly digital sketch experience rendered directly on off-white vintage comic paper.

---

## 🧠 Algorithmic Pipeline & Mechanics

```
┌─────────────────────────┐
│  Source Image (Raster)  │
│ Spider-Man-Pose6.jpg    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    Bilateral Filter     │ Smooths grain while keeping comic borders sharp
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ K-Means Quantization    │ Clusters colors into 16 distinct palette centroids
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Background Calibration  │ Samples paper tone (#C1B9B1); separates foreground
└────────────┬────────────┘
             │
      ┌──────┴──────────────────────────────┐
      ▼                                     ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│ Phase 1: Vector Polygons  │ │ Phase 2: Web Line Inking  │
│ • Area-sorted hierarchy   │ │ • Canny edge detection    │
│ • approxPolyDP decimation │ │ • Silk contour tracing    │
│ • Stained-glass borders   │ │ • Fine-point pen overlay  │
└─────────────┬─────────────┘ └─────────────┬─────────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │ Python Turtle Graphics Loop │
              │ • Arrow cursor motion       │
              │ • Live progress & HUD       │
              │ • Keyboard interactivity    │
              └─────────────────────────────┘
```

### 1. Dynamic Path Resolution
Eliminates brittle hardcoded absolute filesystem paths (`/days/...`) that cause immediate crashes on Unix/macOS environments. Automatically locates `Spider-Man-Pose6-683x1024.jpg` whether invoked from the repository root, within the project folder, or via an IDE run configuration.

### 2. Normalized World Coordinates Viewport (`setworldcoordinates`)
Configures Turtle with `setworldcoordinates(-450, -450, 450, 450)` over a $850 \times 850$ canvas. This guarantees:
- **Zero Edge Clipping**: Generous padding on all four borders so no parts of Spider-Man are cut off.
- **Harmonious Aspect Ratio**: Proportions remain crisp and undistorted across different monitor sizes or window resizing.
- **Isotropic Centering**: All extracted vector coordinates are aligned relative to $(0, 0)$ center-origin.

### 3. K-Means Chromatic Quantization
Groups continuous tone gradients into $K = 18$ discrete color clusters using Lloyd's Euclidean distance minimization:

$$\arg\min_{\mathbf{S}} \sum_{i=1}^{k} \sum_{\mathbf{x} \in S_i} \|\mathbf{x} - \boldsymbol{\mu}_i\|^2$$

This isolates the rich scarlet and crimson reds of the suit, deep navy blues of the torso, pure white eye lenses, and dark comic ink tones.

### 3. Smart Background Paper Tone Isolation
Samples corner border regions to detect the natural warm gray / vintage paper background (`#C1B9B1`). By masking the subject against this paper tone, the engine prevents ugly black polygon borders from cutting through empty canvas space.

### 4. Area-Sorted Layer Hierarchy
Polygons are sorted by descending contour area ($\text{Area} \downarrow$):
- **Base Flats First**: Large torso, thigh, and mask silhouettes are laid down first as solid colored foundations.
- **Details on Top**: Small muscle cuts, eye lens reflections, and highlight facets are drawn last, ensuring critical details are never obscured by larger shapes.

### 5. Silk Web Lines & Comic Inking Pass
Extracts high-frequency contours using Canny gradient thresholds ($T_1 = 45, T_2 = 120$). Turtle switches to an inking pen (`pensize = 1.2`, `#151413`) and sketches Spider-Man's iconic suit webbing, muscle contours, and dynamic cross-hatch shadows.

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
python days/Day-16-Spiderman-Sketch/main.py
```

Or navigate to the project folder:

```bash
cd days/Day-16-Spiderman-Sketch
python main.py
```

---

## 📁 Project Structure

```text
Day-16-Spiderman-Sketch/
├── README.md                       # Comprehensive project documentation
├── main.py                         # Complete executable sketch & animation script
└── Spider-Man-Pose6-683x1024.jpg   # Source Spider-Man crouching pose artwork
```

---

<p align="center">
  <b>30 Days Python Challenge</b> · Made with ❤️ and Python by <a href="https://github.com/Tejas0113">@Tejas0113</a>
</p>

# 🐍 Day 17: Albino Python Realistic Vector Sketch Art

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="../../assets/day17_animation.gif" alt="Albino Python Realistic Vector Sketch Art Preview" width="520px" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(130, 5, 11, 0.45);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-Generative%20Art%20%26%20Vector%20Sketching-82050B?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 17 delivers an authentic generative vector sketching simulation: **Albino Python Realistic Vector Sketch Art**.

Translating the reference masterpiece of a coiled albino python on deep crimson paper (`python snake image.jpeg`), this project implements a true vector sketching engine using **Python Turtle graphics** and **OpenCV**:
1. **Authentic Vector Sketching**: An active arrow-pen physically sketches out the artwork stroke-by-stroke, drawing anatomical color polygons and delicately inking scales, head plates, and features.
2. **Vibrant Crimson Canvas Background**: Faithfully calibrated to `#82050B`, matching the rich crimson red of the reference artwork without muddy vignette borders cutting across empty canvas.
3. **Dual-Phase Vector Pipeline**:
   - **Phase 1: Anatomic Body Polygons**: Traces and fills over 1,000 chromatic vector polygons (ivory, pearl, blush rose, and peach underbelly scutes), sorted by area to lay down base anatomical forms first.
   - **Phase 2: High-Definition Inking**: Inks over 1,400 delicate contour lines across the coiled body, jawline, glowing ruby-red eye, and cephalic scales.
4. **Normalized Centered Viewport**: Configured with `setworldcoordinates(-450, -450, 450, 450)` on an $850 \times 850$ canvas, perfectly centering the crouching python with generous breathing room.

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
│ Dynamic Path Resolution         │ Seamless execution across any directory or OS
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Bilateral Filter & K-Means      │ 24-cluster chromatic quantization for pearlescent tones
└────────────────┬────────────────┘
                 │
      ┌──────────┴──────────────────────────┐
      ▼                                     ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│ Phase 1: Vector Polygons  │ │ Phase 2: Contour Inking   │
│ • 1,000+ chromatic flats  │ │ • 1,400+ scale contours   │
│ • Ivory, peach & scutes   │ │ • Ruby eye & jawline      │
│ • Sorted large to small   │ │ • Fine Canny edge inking  │
└─────────────┬─────────────┘ └─────────────┬─────────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │ Python Turtle Sketch Engine │
              │ • Normalized [-450, 450]    │
              │ • Classic arrow-pen stylus  │
              │ • Rich #82050B crimson bg   │
              │ • Real-time interactive keys│
              └─────────────────────────────┘
```

### 1. Dynamic Path Resolution
Eliminates hardcoded absolute filesystem paths that fail across environments. Automatically resolves `python snake image.jpeg` from the script folder, parent workspace, or root path.

### 2. Chromatic Quantization (24 Clusters)
Applies edge-preserving bilateral filtering ($d=7, \sigma_c=40, \sigma_s=40$) to smooth sensor grain while preserving crisp scale boundaries, followed by Lloyd's K-Means clustering to extract dominant pearlescent, blush rose, and ivory tones.

### 3. Dual-Phase Drawing Execution
- **Phase 1 (Anatomical Base Polygons)**: Draws the broad body musculature, ventral scutes, and dorsal highlights in descending area order.
- **Phase 2 (Ink Detailing)**: Switches pen to fine line drawing, tracing scale borders, cephalic head plates, ruby iris, and forked tongue.

---

## 🎮 Interactive Keyboard Controls

Control the Turtle sketch simulation in real time:

| Key | Action | Description |
| :---: | :--- | :--- |
| **`[SPACE]`** | **Pause / Resume** | Freezes the drawing loop to inspect individual vector strokes |
| **`[+]`** | **Speed Up** | Increases batch step size for faster drawing progression |
| **`[-]`** | **Slow Down** | Decreases batch step size for meditative, deliberate sketching |
| **`[C]`** | **Complete Instantly** | Fast-forwards directly to the finished masterpiece |
| **`[S]`** | **Save Artwork** | Saves high-resolution PostScript / PNG export |
| **`[ESC]` / `[Q]`** | **Exit** | Gracefully closes the Turtle canvas |

---

## 🛠️ Installation & Dependencies

Ensure Python 3.10+ is installed:

```bash
pip install opencv-python numpy pillow
```

*(Note: Turtle is part of the Python standard library).*

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
├── main.py                    # Complete executable vector sketch script
└── python snake image.jpeg    # Reference albino python artwork
```

---

<p align="center">
  <b>30 Days Python Challenge</b> · Made with ❤️ and Python by <a href="https://github.com/Tejas0113">@Tejas0113</a>
</p>

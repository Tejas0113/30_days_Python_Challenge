# ⏰ Day 03: Animated Analog Clock

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Category-GUI%20%26%20Automation-orange?style=for-the-badge" alt="Category" />
</p>

---

## 📖 Overview

Day 3 features a real-time **Animated Analog Clock** created with Python's built-in `turtle` and `time` modules.

The clock accurately reads your local system time and calculates the precise angular headings for the hour, minute, and second hands, rendering them dynamically on a high-contrast dark dial with automatic screen double-buffering.

---

## 🧠 Concepts & Mathematical Mechanics

### 1. Trigonometric Angular Calculations
In standard mathematics and Turtle graphics, $0^\circ$ faces East (right), but on a clock dial, $12:00$ points North (straight UP at $90^\circ$):

- **Second Hand**: Complete revolution every 60 seconds ($360^\circ / 60 = 6^\circ/\text{s}$):
  $$\theta_{\text{sec}} = 90^\circ - (6^\circ \times \text{seconds})$$

- **Minute Hand**: Advances $6^\circ$ per minute plus fractional motion per second ($0.1^\circ/\text{s}$):
  $$\theta_{\text{min}} = 90^\circ - (6^\circ \times \text{minutes} + 0.1^\circ \times \text{seconds})$$

- **Hour Hand**: Advances $30^\circ$ per hour ($360^\circ / 12$) plus fractional motion per minute ($0.5^\circ/\text{min}$):
  $$\theta_{\text{hour}} = 90^\circ - (30^\circ \times \text{hours}_{12} + 0.5^\circ \times \text{minutes})$$

### 2. Double-Buffered Real-time Rendering
Using `screen.tracer(0)` disables automatic redraws while turtles update their positions. Calling `screen.update()` refreshes the display frame instantaneously, preventing hand flickering during ticks.

### 3. Graceful Closure
The animation loop catches `turtle.TerminatorError` so the program exits cleanly when the GUI window is closed by the user.

---

## 🚀 How to Run

From the repository root:

```bash
python days/Day-03-Automated-Clock/main.py
```

---

<p align="center">
  <a href="../../README.md"><b>⬅️ Return to 30 Days Challenge Tracker</b></a>
</p>


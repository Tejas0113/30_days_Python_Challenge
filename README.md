<div align="center">

  <img src="assets/banner.png" alt="30 Days of Python Challenge Banner" width="100%" style="border-radius: 12px; margin-bottom: 20px;" />

  <a href="https://github.com/Tejas0113/30_days_Python_Challenge">
    <img src="assets/logo.png" alt="30 Days Python Challenge Logo" width="160px" style="border-radius: 50%; box-shadow: 0 0 35px rgba(0, 240, 255, 0.45);" />
  </a>

  # 🐍 30 Days of Python Challenge
  ### *Level Up Your Python Skills — A Developer's Daily Journey to Mastery*

  <p align="center">
    <strong>An intensive, hands-on 30-day journey building 30 real-world Python applications, generative art, games, automation bots, web APIs, and autonomous AI systems.</strong>
  </p>

  <p align="center">
    <!-- PROGRESS_BADGE_START -->
<img src="https://img.shields.io/badge/Progress-3%2F30%20(10.0%25)-00f0ff?style=for-the-badge&logo=python&logoColor=white" alt="Progress Badge" /> <img src="https://img.shields.io/badge/Days%20Done-3%20%2F%2030-22c55e?style=for-the-badge" alt="Days Done" /> <img src="https://img.shields.io/badge/Days%20Remaining-27-f59e0b?style=for-the-badge" alt="Days Left" />
<!-- PROGRESS_BADGE_END -->
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Version" />
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License" />
    <img src="https://img.shields.io/badge/Maintained%3F-Yes%20%E2%9C%94-brightgreen?style=flat-square" alt="Maintained" />
    <img src="https://img.shields.io/badge/Code%20Style-Black-000000.svg?style=flat-square" alt="Code Style" />
    <a href="https://github.com/Tejas0113/30_days_Python_Challenge/stargazers">
      <img src="https://img.shields.io/github/stars/Tejas0113/30_days_Python_Challenge?style=flat-square&color=gold" alt="Stars" />
    </a>
    <a href="https://github.com/Tejas0113/30_days_Python_Challenge/network/members">
      <img src="https://img.shields.io/github/forks/Tejas0113/30_days_Python_Challenge?style=flat-square&color=blue" alt="Forks" />
    </a>
  </p>

  <p align="center">
    <a href="#-quick-start">🚀 Quick Start</a> •
    <a href="#-challenge-progress-tracker">📊 Live Tracker</a> •
    <a href="#-day-01-spotlight--infinite-rainbow-spiral">🌀 Day 1 Spotlight</a> •
    <a href="#-30-day-roadmap--curriculum">🗺️ 30-Day Roadmap</a> •
    <a href="#-automated-sync--ci">⚙️ Auto-Sync CI</a> •
    <a href="#-connect--author">👨‍💻 Author</a>
  </p>

  ---

</div>

<br/>

## 🎯 About The Challenge

Welcome to the **30 Days of Python Challenge**! This repository documents an immersive, daily coding expedition aimed at mastering modern Python through practical, production-ready projects.

Rather than sticking to textbook theory, every single day focuses on writing standalone code that builds an exciting application — ranging from **mathematical generative art** and **retro arcade games** to **multi-threaded cybersecurity tools**, **FastAPI microservices**, **computer vision apps**, and **autonomous AI agents**.

### 🌟 Core Principles
- ⚡ **Daily Consistency**: 1 Day = 1 Complete Project.
- 🧱 **Clean Architecture**: Modular code, type hints, informative docstrings, and robust error handling.
- 🤖 **Zero Manual Overhead**: Automatic progress calculation and README synchronization on every Git push via GitHub Actions.
- 🎨 **Visual & Functional**: Every project is interactive, visual, or directly useful in a developer's toolkit.

---

## 📊 Challenge Progress Tracker

<!-- PROGRESS_BAR_START -->
```text
[███░░░░░░░░░░░░░░░░░░░░░░░░░] 10.0% (3/30 Days Completed)
```
<!-- PROGRESS_BAR_END -->

<div align="center">

| 🏆 Milestone | Goal | Status |
| :--- | :--- | :---: |
| **Stage 1: Foundations & Visuals** | Days 01 – 10 (Generative Art, Games, CLI Utilities) | `IN PROGRESS 🚀` |
| **Stage 2: Fullstack, APIs & Systems** | Days 11 – 20 (REST APIs, Microservices, Sockets) | `PENDING ⏳` |
| **Stage 3: Advanced AI & High-Performance** | Days 21 – 30 (Computer Vision, Data Science, AI Agent) | `PENDING ⏳` |

</div>

---

## 🌀 Day 01 Spotlight — Infinite Rainbow Spiral

<div align="center">
  <a href="days/Day-01-Infinite-Spiral">
    <img src="assets/day01_animation.gif" alt="Infinite Rainbow Spiral Animation" width="460px" style="border-radius: 14px; box-shadow: 0 10px 40px rgba(0, 240, 255, 0.3);" />
  </a>
  <br/>
  <p><em>🌀 Live preview of Day 01: Procedural high-FPS rotating rainbow spiral rendered via turtle & colorsys</em></p>
</div>

### 🔍 Highlights of Day 01
- **Color Mathematics**: Uses the **HSV (Hue, Saturation, Value)** color space via Python's built-in `colorsys` module to generate vibrant, electric neon rainbow gradients.
- **Geometric Divergence**: By turning at **$59^\circ$** inside a 6-phase loop (instead of $60^\circ$), each successive arm diverges by $1^\circ$, forming an intricate rotating hypnotic vortex.
- **Double Buffering at 60 FPS**: Utilizes `screen.tracer(0)` and `screen.update()` to eliminate line-by-line rendering lag and screen tearing, achieving silky smooth animation.
- **Graceful Shutdown**: Intercepts `turtle.Terminator` and `KeyboardInterrupt` so the program exits cleanly when closed.

**Run Day 01 locally:**
```bash
python day01_spiral.py
# or
python days/Day-01-Infinite-Spiral/main.py
```

👉 **[Read full Day 01 documentation & math breakdown ➡️](days/Day-01-Infinite-Spiral/README.md)**

---

## 🗺️ 30-Day Roadmap & Curriculum

<!-- CHALLENGE_TABLE_START -->
| Day | Project Title | Key Concepts | Category | Status | Code | Preview |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **Day 01** | [Infinite Rainbow Spiral](days/Day-01-Infinite-Spiral) | `Turtle Graphics, HSV Color Space, 60 FPS Frame Buffering` | Generative Art | `✅ Completed` | [Source](days/Day-01-Infinite-Spiral/main.py) | [View GIF](assets/day01_animation.gif) |
| **Day 02** | [Turtle Flower Drawing](days/Day-02-Flower-Drawing) | `Turtle Graphics, Mathematical Petal Curves, Starfield` | Generative Art | `✅ Completed` | [Source](days/Day-02-Flower-Drawing/main.py) | [Preview](assets/day02_preview.png) |
| **Day 03** | [Animated Analog Clock](days/Day-03-Automated-Clock) | `Turtle Graphics, Time Module, Trigonometric Hand Angles` | GUI & Automation | `✅ Completed` | [Source](days/Day-03-Automated-Clock/main.py) | 🖼️ Ready |
| **Day 04** | **Real-time Weather CLI & Visualizer** | `REST APIs, Requests, JSON Parsing, Rich Terminal UI` | CLI Tools | `⏳ Up Next` | *(Building)* | 🚀 |
| **Day 05** | Advanced Password Vault & Generator | `Cryptography, SHA-256, Fernet, Secure Memory Handling` | Cybersecurity | `🔒 Planned` | — | — |
| **Day 06** | Bulk File Organizer & Renamer | `OS, Shutil, Pathlib, Regex, File System Manipulation` | Productivity | `🔒 Planned` | — | — |
| **Day 07** | Markdown to Clean HTML/PDF Converter | `Python-Markdown, Regex Parsing, CSS Ingestion, WeasyPrint` | Document Tools | `🔒 Planned` | — | — |
| **Day 08** | Multi-threaded Fast Port Scanner | `Socket Programming, ThreadPoolExecutor, Network Protocols` | Networking | `🔒 Planned` | — | — |
| **Day 09** | Personal Finance & Expense Tracker | `SQLite3, Relational Queries, Aggregation, Tabulate` | Database & Finance | `🔒 Planned` | — | — |
| **Day 10** | Modern Pomodoro Productivity Timer | `CustomTkinter / Tkinter, Audio Alerts, State Machine` | GUI Applications | `🔒 Planned` | — | — |
| **Day 11** | Automated YouTube Video Downloader | `Pytubefix / yt-dlp wrapper, Streams, Progress Callbacks` | Media Tools | `🔒 Planned` | — | — |
| **Day 12** | Live Cryptocurrency Ticker & Alert Bot | `CoinGecko API, WebSockets / Polling, Push Notifications` | Financial Tech | `🔒 Planned` | — | — |
| **Day 13** | QR Code Generator & Scanner Suite | `qrcode, OpenCV (cv2), Image Processing, Binary Encoding` | Computer Vision | `🔒 Planned` | — | — |
| **Day 14** | Dynamic Typing Speed Test CLI | `Curses / Time, WPM Calculation, Accuracy Rate, Key Listeners` | CLI Games | `🔒 Planned` | — | — |
| **Day 15** | FastAPI Microservice with Swagger UI | `FastAPI, Pydantic, RESTful CRUD, OpenAPI Documentation` | Backend Web API | `🔒 Planned` | — | — |
| **Day 16** | Automated Email Newsletter Dispatcher | `SMTPlib, Email MIME, Jinja2 Templates, Secure TLS` | Automation | `🔒 Planned` | — | — |
| **Day 17** | Intelligent Wikipedia & Knowledge Bot | `NLP, Wikipedia API, Text Summarization, CLI Chat` | AI & NLP | `🔒 Planned` | — | — |
| **Day 18** | System Resource Monitor Dashboard | `Psutil, CPU/RAM/Disk Metrics, Realtime Terminal Graphs` | SysAdmin & DevOps | `🔒 Planned` | — | — |
| **Day 19** | Audio Spectrum Visualizer | `NumPy, Wave, Pygame / Matplotlib, Fast Fourier Transform (FFT)` | Signal Processing | `🔒 Planned` | — | — |
| **Day 20** | Custom URL Shortener & Analytics | `Flask / SQLite, Base62 Encoding, Click Tracking, Redirects` | Fullstack Web | `🔒 Planned` | — | — |
| **Day 21** | Image Watermarking & Batch Filter Tool | `Pillow (PIL), Alpha Compositing, EXIF Data, Batch Processing` | Image Processing | `🔒 Planned` | — | — |
| **Day 22** | Command-Line Git Branch & Commit Explorer | `GitPython / Subprocess, Git Plumbing, Branch Visualizer` | Developer Tools | `🔒 Planned` | — | — |
| **Day 23** | Stock Market Backtesting & Trend Predictor | `Pandas, Moving Averages (SMA/EMA), Matplotlib plotting` | Data Science | `🔒 Planned` | — | — |
| **Day 24** | Chat Application with Sockets & Threads | `TCP Socket Server, Client Broadcasting, Threading, Chat Protocol` | Network Engineering | `🔒 Planned` | — | — |
| **Day 25** | PDF Merged, Watermarked & Encrypted Toolkit | `pypdf / PyPDF2, Encryption, Split/Merge, Page Rotation` | PDF Processing | `🔒 Planned` | — | — |
| **Day 26** | Interactive Data Dashboard with Streamlit | `Streamlit, Plotly, Interactive Filters, CSV File Ingestion` | Data Apps | `🔒 Planned` | — | — |
| **Day 27** | Regex Playground & Tester CLI | `Re module, Match Highlighting, Regex Explanation Engine` | Algorithms | `🔒 Planned` | — | — |
| **Day 28** | Motion Detection & Face Tracking Camera | `OpenCV, Haar Cascades, Frame Differencing, Webcam Stream` | Computer Vision & AI | `🔒 Planned` | — | — |
| **Day 29** | Algorithmic Pathfinding Visualizer (A* & Dijkstra) | `Graph Theory, Priority Queue, Heuristics, Pygame Grid` | Algorithms & DS | `🔒 Planned` | — | — |
| **Day 30** | Grand Finale: AI-Powered Autonomous Agent CLI | `LLM API Integration, Function Calling, Task Loop, Terminal UI` | Artificial Intelligence | `🔒 Planned` | — | — |
<!-- CHALLENGE_TABLE_END -->

---

## ⚙️ Automated Sync & CI

This repository is equipped with an automated tracking engine designed to keep the README, progress bar, badges, and challenge table synchronized automatically with every commit.

```
📁 Git Commit / Change
       │
       ▼
🪝 Automated Pre-Commit Hook (.git/hooks/pre-commit)
       │
       ▼
🐍 Tracker Script (scripts/update_tracker.py)
       │
       ├── 🔍 Scans `days/` directory & `day*.py` files
       ├── 📈 Computes completion percentage & stats
       ├── 🎨 Updates high-tech progress bar & badges
       └── 📝 Commits updated README.md automatically
```

### 🛠️ Developer CLI Shortcuts

#### 1. Bootstrap a New Challenge Day in One Command:
```bash
python scripts/new_day.py 2 "Retro Arcade Snake Game" "Classic arcade snake game built in Python" "Pygame, Collision, Event Loop"
```
*Creates the day's folder, starter code template, day README, and updates the master tracker table instantly.*

#### 2. Install Automatic Pre-Commit Hook:
```bash
python scripts/setup_git_hook.py
```
*Ensures every `git commit` automatically updates README progress without manual intervention.*

#### 3. Manually Re-sync Tracker:
```bash
python scripts/update_tracker.py
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Tejas0113/30_days_Python_Challenge.git
cd 30_days_Python_Challenge
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate on macOS / Linux:
source .venv/bin/activate

# Activate on Windows:
# .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Day 01
```bash
python day01_spiral.py
```

---

## 📁 Repository Structure

```tree
30_days_Python_Challenge/
├── assets/
│   ├── banner.png                 # Panoramic repo header banner
│   ├── logo.png                   # Cyberpunk Python 30 badge logo
│   ├── day01_preview.png          # High-resolution Day 1 still preview
│   └── day01_animation.gif        # Smooth 60 FPS animation loop
├── days/
│   └── Day-01-Infinite-Spiral/    # Day 01 project folder
│       ├── main.py                # Source code
│       └── README.md              # Project-specific documentation & math
├── scripts/
│   ├── github_workflow_update_readme.yml # GitHub Actions CI workflow template
│   ├── new_day.py                 # CLI: Scaffolds a new day & syncs table
│   ├── setup_git_hook.py          # Auto-hook: Syncs README on git commit
│   └── update_tracker.py          # Auto-calculates stats & updates README
├── .gitignore                     # Ignores virtual environments & build artifacts
├── day01_spiral.py                # Day 1 standalone script (root access)
├── LICENSE                        # MIT License
├── README.md                      # Master aesthetic challenge dashboard
└── requirements.txt               # Project dependencies
```

---

## 🤝 Contributing

Contributions, feedback, and suggestions are warmly welcome!
1. **Fork** the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m "feat: add amazing feature"`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a **Pull Request**.

---

## 👨‍💻 Connect & Author

<div align="center">

**Crafted with ❤️ and Python by [Tejas (@Tejas0113)](https://github.com/Tejas0113)**

[![GitHub](https://img.shields.io/badge/GitHub-Tejas0113-181717?style=for-the-badge&logo=github)](https://github.com/Tejas0113)

⭐ **If you find this repository inspiring or helpful, please consider giving it a star!** ⭐

</div>

---

<div align="center">
  <sub>Released under the <a href="LICENSE">MIT License</a>. Copyright &copy; 2026 Tejas0113.</sub>
</div>

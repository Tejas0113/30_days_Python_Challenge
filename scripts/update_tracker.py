#!/usr/bin/env python3
"""
30 Days Python Challenge - Automated Progress & README Tracker
Author: Tejas (@Tejas0113)

This script scans the repository for completed days, recalculates progress statistics,
and automatically updates the master README.md (badges, visual progress bar, and challenge table).
Outputs/previews are kept inside individual day READMEs to maintain a clean master dashboard.
"""

import os
import re
import sys
from pathlib import Path

# 30 Days Python Challenge Curriculum - Creative, Visual & Interactive Projects
CURRICULUM = [
    {
        "day": 1,
        "title": "Infinite Rainbow Spiral",
        "description": "Dynamic rotating rainbow spiral using HSV color wheel and smooth 60 FPS buffer rendering.",
        "concepts": "Turtle Graphics, HSV Color Space, Frame Buffering",
        "category": "Generative Art",
        "folder": "Day-01-Infinite-Spiral",
        "entry": "days/Day-01-Infinite-Spiral/main.py",
    },
    {
        "day": 2,
        "title": "Turtle Flower Drawing",
        "description": "Procedural multi-layered blossom with Fermat spiral center floret, curved stem, and starry background.",
        "concepts": "Turtle Graphics, Parametric Curves, Spiral Phyllotaxis",
        "category": "Generative Art",
        "folder": "Day-02-Flower-Drawing",
        "entry": "days/Day-02-Flower-Drawing/main.py",
    },
    {
        "day": 3,
        "title": "Animated Analog Clock",
        "description": "Real-time system-synced analog clock with trigonometric hour, minute, and second hand animations.",
        "concepts": "Tkinter Canvas, Datetime, Trigonometric Hand Angles",
        "category": "GUI & Automation",
        "folder": "Day-03-Automated-Clock",
        "entry": "days/Day-03-Automated-Clock/main.py",
    },
    {
        "day": 4,
        "title": "Rotating Spiral Flower Design",
        "description": "Procedural rotating rainbow flower using nested circular arcs, HSV chromatic gradients, and 50 FPS double-buffered animation.",
        "concepts": "Turtle Graphics, HSV Color Space, Geometric Rotation, Ontimer Animation",
        "category": "Generative Art",
        "folder": "Day-04-Design-of-Spiral-Flower",
        "entry": "days/Day-04-Design-of-Spiral-Flower/main.py",
    },
    {
        "day": 5,
        "title": "Neon Arcade Pong Game",
        "description": "Classic 2-player paddle arcade with ball bounce physics, paddle collision bounding boxes, and score display.",
        "concepts": "Turtle / Pygame, Elastic Collisions, Keyboard Input Binding",
        "category": "2D Game Dev",
        "folder": "Day-05-Neon-Arcade-Pong",
        "entry": "days/Day-05-Neon-Arcade-Pong/main.py",
    },
    {
        "day": 6,
        "title": "Procedural Fractal Tree & Forest",
        "description": "Recursive branching tree with wind animation, depth-based color gradients, and falling blossom particles.",
        "concepts": "Recursive Algorithms, Branching Angles, Dynamic Color Gradients",
        "category": "Generative Art",
        "folder": "Day-06-Fractal-Tree",
        "entry": "days/Day-06-Fractal-Tree/main.py",
    },
    {
        "day": 7,
        "title": "Retro Snake Arcade",
        "description": "Iconic arcade snake game featuring grid movement, dynamic food spawning, score tracking, and tail collision.",
        "concepts": "Grid Coordinates, List Queues, Game Loops, Collision Detection",
        "category": "2D Game Dev",
        "folder": "Day-07-Retro-Snake",
        "entry": "days/Day-07-Retro-Snake/main.py",
    },
    {
        "day": 8,
        "title": "Conway's Game of Life Simulation",
        "description": "Interactive cellular automata grid simulation modeling birth, survival, and death patterns (gliders, pulsars).",
        "concepts": "Cellular Automata, 2D Array Grids, State Evolution Rules",
        "category": "Simulation",
        "folder": "Day-08-Conways-Game-of-Life",
        "entry": "days/Day-08-Conways-Game-of-Life/main.py",
    },
    {
        "day": 9,
        "title": "Interactive Kaleidoscope & Mandala",
        "description": "Real-time drawing canvas replicating mouse/keyboard strokes across 8-fold rotational and mirror symmetries.",
        "concepts": "Rotational Symmetry, Polar-to-Cartesian Mapping, Event Listeners",
        "category": "Generative Art",
        "folder": "Day-09-Interactive-Kaleidoscope",
        "entry": "days/Day-09-Interactive-Kaleidoscope/main.py",
    },
    {
        "day": 10,
        "title": "Flappy Bird Physics Clone",
        "description": "Side-scrolling arcade game with gravity acceleration, flap velocity impulses, moving pipe pairs, and hitboxes.",
        "concepts": "Gravity & Velocity Vectors, Obstacle Spawning, AABB Hitboxes",
        "category": "2D Game Dev",
        "folder": "Day-10-Flappy-Bird",
        "entry": "days/Day-10-Flappy-Bird/main.py",
    },
    {
        "day": 11,
        "title": "Gravitational Solar System Simulator",
        "description": "Multi-body planetary orbital mechanics simulation using Newton's law of universal gravitation with glowing orbit trails.",
        "concepts": "Newtonian Gravity, Orbital Mechanics, Vector Acceleration",
        "category": "Physics Simulation",
        "folder": "Day-11-Solar-System-Simulator",
        "entry": "days/Day-11-Solar-System-Simulator/main.py",
    },
    {
        "day": 12,
        "title": "Matrix Digital Rain Visualizer",
        "description": "Hypnotic falling green Japanese katakana & code rain with decaying phosphorescent light trails.",
        "concepts": "Terminal Buffering, Glyph Streams, Decay Timing",
        "category": "Visual Effects",
        "folder": "Day-12-Matrix-Rain-Visualizer",
        "entry": "days/Day-12-Matrix-Rain-Visualizer/main.py",
    },
    {
        "day": 13,
        "title": "Sorting Algorithm Visualizer",
        "description": "Animated visual comparison of Bubble, Selection, Insertion, and Quick Sort with real-time bar height swaps and colors.",
        "concepts": "Sorting Algorithms, Visual Bar Swaps, Algorithmic Complexity",
        "category": "Algorithm Visualizer",
        "folder": "Day-13-Sorting-Visualizer",
        "entry": "days/Day-13-Sorting-Visualizer/main.py",
    },
    {
        "day": 14,
        "title": "Double Pendulum Chaos Simulator",
        "description": "Physics simulation of a chaotic double pendulum tracing unpredictable, beautiful kaleidoscopic phase space trails.",
        "concepts": "Chaos Theory, Lagrangian Mechanics, Numerical Integration",
        "category": "Physics Simulation",
        "folder": "Day-14-Double-Pendulum-Chaos",
        "entry": "days/Day-14-Double-Pendulum-Chaos/main.py",
    },
    {
        "day": 15,
        "title": "Retro Space Invaders Arcade",
        "description": "Galactic arcade defender with alien marching grids, player laser cannons, defensive barriers, and mystery UFOs.",
        "concepts": "Sprite Arrays, Projectile Management, Marching Movement Logic",
        "category": "2D Game Dev",
        "folder": "Day-15-Space-Invaders",
        "entry": "days/Day-15-Space-Invaders/main.py",
    },
    {
        "day": 16,
        "title": "Algorithmic Maze Generator & Solver",
        "description": "Procedural maze generation using Recursive Backtracking / Depth-First Search with live visual pathfinding resolution.",
        "concepts": "Depth-First Search (DFS), Recursive Backtracking, Graph Traversal",
        "category": "Algorithm Visualizer",
        "folder": "Day-16-Maze-Generator-Solver",
        "entry": "days/Day-16-Maze-Generator-Solver/main.py",
    },
    {
        "day": 17,
        "title": "Particle Fireworks & Sparkle Engine",
        "description": "Colorful fireworks bursting into hundreds of glowing particles with gravity drag, air resistance, and alpha decay.",
        "concepts": "Particle Systems, Velocity Decay, Radial Burst Physics",
        "category": "Particle Systems",
        "folder": "Day-17-Particle-Fireworks",
        "entry": "days/Day-17-Particle-Fireworks/main.py",
    },
    {
        "day": 18,
        "title": "Mandelbrot & Julia Set Fractal Explorer",
        "description": "Interactive deep-zoom visualizer rendering the infinite boundary of the Mandelbrot and Julia set complex equations.",
        "concepts": "Complex Numbers, Escape-Time Formula, Color Paletting",
        "category": "Mathematical Art",
        "folder": "Day-18-Mandelbrot-Fractal",
        "entry": "days/Day-18-Mandelbrot-Fractal/main.py",
    },
    {
        "day": 19,
        "title": "Audio Spectrum & Beat Visualizer",
        "description": "Real-time equalizer bars and circular audio spectrum responding dynamically to audio waveforms and frequency beats.",
        "concepts": "Fast Fourier Transform (FFT), Frequency Bins, Dynamic Scaling",
        "category": "Audio & Signal Processing",
        "folder": "Day-19-Audio-Spectrum-Visualizer",
        "entry": "days/Day-19-Audio-Spectrum-Visualizer/main.py",
    },
    {
        "day": 20,
        "title": "Elastic Balls Collision Physics Sandbox",
        "description": "Interactive physics simulation of multi-sized colored spheres colliding elastically with conservation of momentum.",
        "concepts": "2D Vector Math, Elastic Collision Response, Momentum Conservation",
        "category": "Physics Simulation",
        "folder": "Day-20-Bouncing-Balls-Physics",
        "entry": "days/Day-20-Bouncing-Balls-Physics/main.py",
    },
    {
        "day": 21,
        "title": "2D Raycasting Pseudo-3D Engine",
        "description": "Retro Wolfenstein 3D-style raycasting engine rendering pseudo-3D first-person perspective walls from a 2D grid.",
        "concepts": "Raycasting, DDA Algorithm, Field of View (FOV), Wall Slicing",
        "category": "Graphics Engine",
        "folder": "Day-21-Raycasting-Engine",
        "entry": "days/Day-21-Raycasting-Engine/main.py",
    },
    {
        "day": 22,
        "title": "A* & Dijkstra Pathfinding Visualizer",
        "description": "Visual grid navigation tool calculating shortest paths around user-drawn walls with real-time open/closed set animations.",
        "concepts": "A* Search, Dijkstra Algorithm, Priority Queues, Manhattan Distance",
        "category": "Algorithm Visualizer",
        "folder": "Day-22-Pathfinding-Visualizer",
        "entry": "days/Day-22-Pathfinding-Visualizer/main.py",
    },
    {
        "day": 23,
        "title": "Interactive Water Ripple Wave Sandbox",
        "description": "Dynamic fluid grid simulating water ripple propagation, reflections against boundaries, and mouse droplet disturbances.",
        "concepts": "Discrete Wave Equation, Velocity Damping, Surface Disturbance",
        "category": "Physics Simulation",
        "folder": "Day-23-Water-Ripple-Simulation",
        "entry": "days/Day-23-Water-Ripple-Simulation/main.py",
    },
    {
        "day": 24,
        "title": "Classic Asteroids Vector Space Combat",
        "description": "360-degree rotational spaceship combat with inertia physics, screen wrap-around, and splitting floating asteroids.",
        "concepts": "Angular Momentum, Toroidal Screen Wrap, Polygonal Splitting",
        "category": "2D Game Dev",
        "folder": "Day-24-Asteroids-Arcade",
        "entry": "days/Day-24-Asteroids-Arcade/main.py",
    },
    {
        "day": 25,
        "title": "Cyberpunk Digital Synth & Piano",
        "description": "Playable graphical synthesizer keyboard generating synthesized musical notes with glowing neon key feedback.",
        "concepts": "Audio Synthesis, Sine Waves, GUI Keypress Binding",
        "category": "GUI & Audio",
        "folder": "Day-25-Visual-Synthesizer",
        "entry": "days/Day-25-Visual-Synthesizer/main.py",
    },
    {
        "day": 26,
        "title": "3D Perspective Infinite Starfield Flight",
        "description": "Hyperspace warp simulation projecting thousands of 3D stars through a perspective camera to create high-speed flight.",
        "concepts": "3D-to-2D Perspective Projection, Z-axis Warp, Velocity Trails",
        "category": "Visual Effects",
        "folder": "Day-26-Starfield-Warp-Flight",
        "entry": "days/Day-26-Starfield-Warp-Flight/main.py",
    },
    {
        "day": 27,
        "title": "Craig Reynolds Boids Flocking Simulation",
        "description": "Autonomous swarm intelligence modeling bird flocks and fish schools using Separation, Alignment, and Cohesion forces.",
        "concepts": "Flocking Algorithms, Autonomous Agents, Vector Steering",
        "category": "Autonomous Systems",
        "folder": "Day-27-Boids-Flocking-Simulation",
        "entry": "days/Day-27-Boids-Flocking-Simulation/main.py",
    },
    {
        "day": 28,
        "title": "Live ASCII Art Video Streamer",
        "description": "Real-time video/webcam feed converter transforming frames into animated high-contrast ASCII character mosaic art.",
        "concepts": "OpenCV, Grayscale Luminance Mapping, Terminal Canvas Rendering",
        "category": "Computer Vision Art",
        "folder": "Day-28-ASCII-Art-Streamer",
        "entry": "days/Day-28-ASCII-Art-Streamer/main.py",
    },
    {
        "day": 29,
        "title": "Hand Gesture Air Canvas Painter",
        "description": "Touchless virtual drawing studio using hand tracking and index-finger gestures to paint colored strokes in mid-air.",
        "concepts": "MediaPipe / OpenCV, Hand Landmarks, Gesture Recognition",
        "category": "Computer Vision & AI",
        "folder": "Day-29-Air-Canvas-Painter",
        "entry": "days/Day-29-Air-Canvas-Painter/main.py",
    },
    {
        "day": 30,
        "title": "Grand Finale: 3D Wireframe Engine & Cyber Arcade",
        "description": "Pure Python 3D math engine and retro arcade suite uniting procedural visuals, particle systems, and high score dashboards.",
        "concepts": "3D Transformation Matrices, Particle FX, Multi-Game Engine",
        "category": "3D Graphics & Games",
        "folder": "Day-30-Cyber-Arcade-Universe",
        "entry": "days/Day-30-Cyber-Arcade-Universe/main.py",
    },
]


def check_day_completion(day_info: dict, repo_root: Path) -> bool:
    """Checks whether code exists for a given day."""
    # Check folder entry
    folder_entry = repo_root / day_info["entry"]
    if folder_entry.exists() and folder_entry.stat().st_size > 0:
        return True

    # Check days/ directory pattern (e.g. days/Day-01-*/main.py)
    day_num = day_info["day"]
    days_dir = repo_root / "days"
    if days_dir.exists():
        for day_folder in days_dir.glob(f"Day-{day_num:02d}*"):
            main_file = day_folder / "main.py"
            if main_file.exists() and main_file.stat().st_size > 0:
                return True

    # Check root day pattern
    root_pattern = f"day{day_num:02d}*.py"
    matches = list(repo_root.glob(root_pattern))
    if matches and any(m.stat().st_size > 0 for m in matches):
        return True

    return False


def generate_progress_bar(completed: int, total: int = 30, width: int = 28) -> str:
    """Generates a high-tech unicode progress bar."""
    filled_len = int(round(width * completed / float(total)))
    bar = "█" * filled_len + "░" * (width - filled_len)
    percent = (completed / float(total)) * 100.0
    return f"```text\n[{bar}] {percent:.1f}% ({completed}/{total} Days Completed)\n```"


def build_markdown_table(repo_root: Path, completed_count: int) -> str:
    """Constructs the comprehensive 30-day challenge table without preview/output clutter."""
    headers = [
        "| Day | Project Title | Key Concepts | Category | Status | Code |",
        "| :---: | :--- | :--- | :--- | :---: | :---: |"
    ]
    rows = []

    for item in CURRICULUM:
        day_num = item["day"]
        day_str = f"Day {day_num:02d}"
        title = item["title"]
        concepts = item["concepts"]
        category = item["category"]
        folder = item["folder"]
        entry = item["entry"]

        is_done = check_day_completion(item, repo_root)

        if is_done:
            status_badge = "`✅ Completed`"
            code_link = f"[Source]({entry})"
            folder_link = f"[{title}](days/{folder})"
        elif day_num == completed_count + 1:
            status_badge = "`⏳ Up Next`"
            folder_link = f"**{title}**"
            code_link = "*(Building)*"
        else:
            status_badge = "`🔒 Planned`"
            folder_link = title
            code_link = "—"

        row = f"| **{day_str}** | {folder_link} | `{concepts}` | {category} | {status_badge} | {code_link} |"
        rows.append(row)

    return "\n".join(headers + rows)


def update_readme(repo_root: Path):
    """Scans repo, calculates statistics, and updates README.md."""
    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        print(f"❌ README.md not found in {repo_root}")
        return False

    # Determine completion
    completed_days = 0
    for item in CURRICULUM:
        if check_day_completion(item, repo_root):
            completed_days += 1

    total_days = len(CURRICULUM)
    percentage = (completed_days / total_days) * 100.0

    print(f"📊 Challenge Stats: {completed_days}/{total_days} days completed ({percentage:.1f}%)")

    content = readme_path.read_text(encoding="utf-8")

    # 1. Update Progress Badges
    badge_pattern = r"(<!-- PROGRESS_BADGE_START -->)(.*?)(<!-- PROGRESS_BADGE_END -->)"
    new_badge = (
        r"\1\n"
        f'<img src="https://img.shields.io/badge/Progress-{completed_days}%2F{total_days}%20({percentage:.1f}%25)-00f0ff?style=for-the-badge&logo=python&logoColor=white" alt="Progress Badge" /> '
        f'<img src="https://img.shields.io/badge/Days%20Done-{completed_days}%20%2F%20{total_days}-22c55e?style=for-the-badge" alt="Days Done" /> '
        f'<img src="https://img.shields.io/badge/Days%20Remaining-{total_days - completed_days}-f59e0b?style=for-the-badge" alt="Days Left" />\n'
        r"\3"
    )
    content = re.sub(badge_pattern, new_badge, content, flags=re.DOTALL)

    # 2. Update Progress Bar
    bar_pattern = r"(<!-- PROGRESS_BAR_START -->)(.*?)(<!-- PROGRESS_BAR_END -->)"
    bar_str = generate_progress_bar(completed_days, total_days)
    new_bar = f"\\1\n{bar_str}\n\\3"
    content = re.sub(bar_pattern, new_bar, content, flags=re.DOTALL)

    # 3. Update Challenge Table
    table_pattern = r"(<!-- CHALLENGE_TABLE_START -->)(.*?)(<!-- CHALLENGE_TABLE_END -->)"
    table_str = build_markdown_table(repo_root, completed_days)
    new_table = f"\\1\n{table_str}\n\\3"
    content = re.sub(table_pattern, new_table, content, flags=re.DOTALL)

    # 4. Remove any legacy Day Spotlight section if present
    content = re.sub(
        r"## 🌀 Day 01 Spotlight — Infinite Rainbow Spiral.*?(?=## 🗺️ 30-Day Roadmap)",
        "",
        content,
        flags=re.DOTALL
    )

    readme_path.write_text(content, encoding="utf-8")
    print("✅ README.md successfully updated!")
    return True


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    update_readme(root_dir)

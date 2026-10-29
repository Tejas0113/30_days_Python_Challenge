#!/usr/bin/env python3
"""
30 Days Python Challenge - Automated Progress & README Tracker
Author: Tejas (@Tejas0113)

This script scans the repository for completed days, recalculates progress statistics,
and automatically updates the master README.md (badges, visual progress bar, and challenge table).
"""

import os
import re
import sys
from pathlib import Path

# Predefined curriculum for 30 Days Python Challenge
CURRICULUM = [
    {
        "day": 1,
        "title": "Infinite Rainbow Spiral",
        "concepts": "Turtle Graphics, HSV Color Space, 60 FPS Frame Buffering",
        "category": "Generative Art",
        "folder": "Day-01-Infinite-Spiral",
        "entry": "days/Day-01-Infinite-Spiral/main.py",
        "preview": "assets/day01_animation.gif"
    },
    {
        "day": 2,
        "title": "Retro Arcade Snake Game",
        "concepts": "Pygame / Turtle, Collision Detection, Event Loop & State",
        "category": "Game Dev",
        "folder": "Day-02-Snake-Game",
        "entry": "days/Day-02-Snake-Game/main.py",
        "preview": ""
    },
    {
        "day": 3,
        "title": "Automated Web Scraping Engine",
        "concepts": "BeautifulSoup4, Requests, Data Extraction & CSV Pipeline",
        "category": "Web Automation",
        "folder": "Day-03-Web-Scraper",
        "entry": "days/Day-03-Web-Scraper/main.py",
        "preview": ""
    },
    {
        "day": 4,
        "title": "Real-time Weather CLI & Visualizer",
        "concepts": "REST APIs, Requests, JSON Parsing, Rich Terminal UI",
        "category": "CLI Tools",
        "folder": "Day-04-Weather-CLI",
        "entry": "days/Day-04-Weather-CLI/main.py",
        "preview": ""
    },
    {
        "day": 5,
        "title": "Advanced Password Vault & Generator",
        "concepts": "Cryptography, SHA-256, Fernet, Secure Memory Handling",
        "category": "Cybersecurity",
        "folder": "Day-05-Password-Vault",
        "entry": "days/Day-05-Password-Vault/main.py",
        "preview": ""
    },
    {
        "day": 6,
        "title": "Bulk File Organizer & Renamer",
        "concepts": "OS, Shutil, Pathlib, Regex, File System Manipulation",
        "category": "Productivity",
        "folder": "Day-06-File-Organizer",
        "entry": "days/Day-06-File-Organizer/main.py",
        "preview": ""
    },
    {
        "day": 7,
        "title": "Markdown to Clean HTML/PDF Converter",
        "concepts": "Python-Markdown, Regex Parsing, CSS Ingestion, WeasyPrint",
        "category": "Document Tools",
        "folder": "Day-07-Markdown-Converter",
        "entry": "days/Day-07-Markdown-Converter/main.py",
        "preview": ""
    },
    {
        "day": 8,
        "title": "Multi-threaded Fast Port Scanner",
        "concepts": "Socket Programming, ThreadPoolExecutor, Network Protocols",
        "category": "Networking",
        "folder": "Day-08-Port-Scanner",
        "entry": "days/Day-08-Port-Scanner/main.py",
        "preview": ""
    },
    {
        "day": 9,
        "title": "Personal Finance & Expense Tracker",
        "concepts": "SQLite3, Relational Queries, Aggregation, Tabulate",
        "category": "Database & Finance",
        "folder": "Day-09-Expense-Tracker",
        "entry": "days/Day-09-Expense-Tracker/main.py",
        "preview": ""
    },
    {
        "day": 10,
        "title": "Modern Pomodoro Productivity Timer",
        "concepts": "CustomTkinter / Tkinter, Audio Alerts, State Machine",
        "category": "GUI Applications",
        "folder": "Day-10-Pomodoro-Timer",
        "entry": "days/Day-10-Pomodoro-Timer/main.py",
        "preview": ""
    },
    {
        "day": 11,
        "title": "Automated YouTube Video Downloader",
        "concepts": "Pytubefix / yt-dlp wrapper, Streams, Progress Callbacks",
        "category": "Media Tools",
        "folder": "Day-11-Video-Downloader",
        "entry": "days/Day-11-Video-Downloader/main.py",
        "preview": ""
    },
    {
        "day": 12,
        "title": "Live Cryptocurrency Ticker & Alert Bot",
        "concepts": "CoinGecko API, WebSockets / Polling, Push Notifications",
        "category": "Financial Tech",
        "folder": "Day-12-Crypto-Ticker",
        "entry": "days/Day-12-Crypto-Ticker/main.py",
        "preview": ""
    },
    {
        "day": 13,
        "title": "QR Code Generator & Scanner Suite",
        "concepts": "qrcode, OpenCV (cv2), Image Processing, Binary Encoding",
        "category": "Computer Vision",
        "folder": "Day-13-QR-Code-Suite",
        "entry": "days/Day-13-QR-Code-Suite/main.py",
        "preview": ""
    },
    {
        "day": 14,
        "title": "Dynamic Typing Speed Test CLI",
        "concepts": "Curses / Time, WPM Calculation, Accuracy Rate, Key Listeners",
        "category": "CLI Games",
        "folder": "Day-14-Typing-Test",
        "entry": "days/Day-14-Typing-Test/main.py",
        "preview": ""
    },
    {
        "day": 15,
        "title": "FastAPI Microservice with Swagger UI",
        "concepts": "FastAPI, Pydantic, RESTful CRUD, OpenAPI Documentation",
        "category": "Backend Web API",
        "folder": "Day-15-FastAPI-Service",
        "entry": "days/Day-15-FastAPI-Service/main.py",
        "preview": ""
    },
    {
        "day": 16,
        "title": "Automated Email Newsletter Dispatcher",
        "concepts": "SMTPlib, Email MIME, Jinja2 Templates, Secure TLS",
        "category": "Automation",
        "folder": "Day-16-Email-Dispatcher",
        "entry": "days/Day-16-Email-Dispatcher/main.py",
        "preview": ""
    },
    {
        "day": 17,
        "title": "Intelligent Wikipedia & Knowledge Bot",
        "concepts": "NLP, Wikipedia API, Text Summarization, CLI Chat",
        "category": "AI & NLP",
        "folder": "Day-17-Knowledge-Bot",
        "entry": "days/Day-17-Knowledge-Bot/main.py",
        "preview": ""
    },
    {
        "day": 18,
        "title": "System Resource Monitor Dashboard",
        "concepts": "Psutil, CPU/RAM/Disk Metrics, Realtime Terminal Graphs",
        "category": "SysAdmin & DevOps",
        "folder": "Day-18-System-Monitor",
        "entry": "days/Day-18-System-Monitor/main.py",
        "preview": ""
    },
    {
        "day": 19,
        "title": "Audio Spectrum Visualizer",
        "concepts": "NumPy, Wave, Pygame / Matplotlib, Fast Fourier Transform (FFT)",
        "category": "Signal Processing",
        "folder": "Day-19-Audio-Visualizer",
        "entry": "days/Day-19-Audio-Visualizer/main.py",
        "preview": ""
    },
    {
        "day": 20,
        "title": "Custom URL Shortener & Analytics",
        "concepts": "Flask / SQLite, Base62 Encoding, Click Tracking, Redirects",
        "category": "Fullstack Web",
        "folder": "Day-20-URL-Shortener",
        "entry": "days/Day-20-URL-Shortener/main.py",
        "preview": ""
    },
    {
        "day": 21,
        "title": "Image Watermarking & Batch Filter Tool",
        "concepts": "Pillow (PIL), Alpha Compositing, EXIF Data, Batch Processing",
        "category": "Image Processing",
        "folder": "Day-21-Image-Watermarker",
        "entry": "days/Day-21-Image-Watermarker/main.py",
        "preview": ""
    },
    {
        "day": 22,
        "title": "Command-Line Git Branch & Commit Explorer",
        "concepts": "GitPython / Subprocess, Git Plumbing, Branch Visualizer",
        "category": "Developer Tools",
        "folder": "Day-22-Git-Explorer",
        "entry": "days/Day-22-Git-Explorer/main.py",
        "preview": ""
    },
    {
        "day": 23,
        "title": "Stock Market Backtesting & Trend Predictor",
        "concepts": "Pandas, Moving Averages (SMA/EMA), Matplotlib plotting",
        "category": "Data Science",
        "folder": "Day-23-Stock-Backtester",
        "entry": "days/Day-23-Stock-Backtester/main.py",
        "preview": ""
    },
    {
        "day": 24,
        "title": "Chat Application with Sockets & Threads",
        "concepts": "TCP Socket Server, Client Broadcasting, Threading, Chat Protocol",
        "category": "Network Engineering",
        "folder": "Day-24-Socket-Chat",
        "entry": "days/Day-24-Socket-Chat/main.py",
        "preview": ""
    },
    {
        "day": 25,
        "title": "PDF Merged, Watermarked & Encrypted Toolkit",
        "concepts": "pypdf / PyPDF2, Encryption, Split/Merge, Page Rotation",
        "category": "PDF Processing",
        "folder": "Day-25-PDF-Toolkit",
        "entry": "days/Day-25-PDF-Toolkit/main.py",
        "preview": ""
    },
    {
        "day": 26,
        "title": "Interactive Data Dashboard with Streamlit",
        "concepts": "Streamlit, Plotly, Interactive Filters, CSV File Ingestion",
        "category": "Data Apps",
        "folder": "Day-26-Data-Dashboard",
        "entry": "days/Day-26-Data-Dashboard/main.py",
        "preview": ""
    },
    {
        "day": 27,
        "title": "Regex Playground & Tester CLI",
        "concepts": "Re module, Match Highlighting, Regex Explanation Engine",
        "category": "Algorithms",
        "folder": "Day-27-Regex-Tester",
        "entry": "days/Day-27-Regex-Tester/main.py",
        "preview": ""
    },
    {
        "day": 28,
        "title": "Motion Detection & Face Tracking Camera",
        "concepts": "OpenCV, Haar Cascades, Frame Differencing, Webcam Stream",
        "category": "Computer Vision & AI",
        "folder": "Day-28-Motion-Detector",
        "entry": "days/Day-28-Motion-Detector/main.py",
        "preview": ""
    },
    {
        "day": 29,
        "title": "Algorithmic Pathfinding Visualizer (A* & Dijkstra)",
        "concepts": "Graph Theory, Priority Queue, Heuristics, Pygame Grid",
        "category": "Algorithms & DS",
        "folder": "Day-29-Pathfinding-Visualizer",
        "entry": "days/Day-29-Pathfinding-Visualizer/main.py",
        "preview": ""
    },
    {
        "day": 30,
        "title": "Grand Finale: AI-Powered Autonomous Agent CLI",
        "concepts": "LLM API Integration, Function Calling, Task Loop, Terminal UI",
        "category": "Artificial Intelligence",
        "folder": "Day-30-AI-Agent",
        "entry": "days/Day-30-AI-Agent/main.py",
        "preview": ""
    }
]


def check_day_completion(day_info, repo_root: Path) -> bool:
    """Checks whether code exists for a given day."""
    # Check folder entry
    folder_entry = repo_root / day_info["entry"]
    if folder_entry.exists() and folder_entry.stat().st_size > 0:
        return True

    # Check root day files (e.g. day01_spiral.py or day01.py)
    day_num = day_info["day"]
    root_pattern = f"day{day_num:02d}*.py"
    matches = list(repo_root.glob(root_pattern))
    if matches:
        return True

    return False


def generate_progress_bar(completed: int, total: int = 30, width: int = 28) -> str:
    """Generates a high-tech unicode progress bar."""
    filled_len = int(round(width * completed / float(total)))
    bar = "█" * filled_len + "░" * (width - filled_len)
    percent = (completed / float(total)) * 100.0
    return f"```text\n[{bar}] {percent:.1f}% ({completed}/{total} Days Completed)\n```"


def build_markdown_table(repo_root: Path, completed_count: int) -> str:
    """Constructs the comprehensive 30-day challenge table."""
    headers = [
        "| Day | Project Title | Key Concepts | Category | Status | Code | Preview |",
        "| :---: | :--- | :--- | :--- | :---: | :---: | :---: |"
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
        preview = item["preview"]

        is_done = check_day_completion(item, repo_root)

        if is_done:
            status_badge = "`✅ Completed`"
            code_link = f"[Source]({entry})"
            folder_link = f"[{title}](days/{folder})"
            preview_elem = f"[View GIF]({preview})" if preview else "🖼️ Ready"
        elif day_num == completed_count + 1:
            status_badge = "`⏳ Up Next`"
            folder_link = f"**{title}**"
            code_link = "*(Building)*"
            preview_elem = "🚀"
        else:
            status_badge = "`🔒 Planned`"
            folder_link = title
            code_link = "—"
            preview_elem = "—"

        row = f"| **{day_str}** | {folder_link} | `{concepts}` | {category} | {status_badge} | {code_link} | {preview_elem} |"
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

    readme_path.write_text(content, encoding="utf-8")
    print(f"✅ README.md successfully updated!")
    return True


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    update_readme(root_dir)

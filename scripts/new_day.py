#!/usr/bin/env python3
"""
30 Days Python Challenge - Day Generator CLI
Author: Tejas (@Tejas0113)

Usage:
    python scripts/new_day.py <day_number>
    python scripts/new_day.py <day_number> "<title>" ["<description>"] ["<concepts>"]
    
Example:
    python scripts/new_day.py 4
    python scripts/new_day.py 4 "Neon Arcade Pong Game" "Classic 2-player arcade" "Turtle, Pygame, Physics"
"""

import sys
import subprocess
from pathlib import Path

# Add scripts directory to sys.path for curriculum import
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))


def create_day(day_num: int, title: str, description: str = "", concepts: str = ""):
    repo_root = Path(__file__).resolve().parent.parent
    day_slug = title.replace(" ", "-").replace("/", "-")
    folder_name = f"Day-{day_num:02d}-{day_slug}"
    target_dir = repo_root / "days" / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)

    main_py = target_dir / "main.py"
    if not main_py.exists():
        main_py.write_text(
            f'''"""
Day {day_num:02d}: {title}
30 Days Python Challenge by Tejas (@Tejas0113)

Description:
{description or title}
"""

def main():
    print("🚀 Day {day_num:02d}: {title} initialized!")
    # TODO: Implement project logic here


if __name__ == "__main__":
    main()
''',
            encoding="utf-8"
        )
        print(f"Created {main_py}")

    readme_md = target_dir / "README.md"
    if not readme_md.exists():
        readme_md.write_text(
            f'''# 🚀 Day {day_num:02d}: {title}

> **30 Days of Python Challenge** · Level Up Your Python Skills  
> Created by **[@Tejas0113](https://github.com/Tejas0113)**

---

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed%20%E2%9C%85-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Language-Python%203.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</p>

---

## 📖 Overview

{description or title}

---

## 🧠 Concepts & Topics Covered

- {concepts or "Core Python Concepts"}

---

## 🚀 How to Run

From the repository root:

```bash
python days/{folder_name}/main.py
```

---

<p align="center">
  <a href="../../README.md"><b>⬅️ Return to 30 Days Challenge Tracker</b></a>
</p>
''',
            encoding="utf-8"
        )
        print(f"Created {readme_md}")

    # Run update_tracker.py to update README.md automatically
    tracker_script = repo_root / "scripts" / "update_tracker.py"
    if tracker_script.exists():
        subprocess.run([sys.executable, str(tracker_script)], check=True)

    print(f"\n🎉 Successfully initialized Day {day_num:02d} ({title}) and updated README.md!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("    python scripts/new_day.py <day_number>")
        print("    python scripts/new_day.py <day_number> \"<title>\" [\"<description>\"] [\"<concepts>\"]")
        sys.exit(1)

    day_num = int(sys.argv[1])

    if len(sys.argv) == 2:
        try:
            from update_tracker import CURRICULUM
            match = next((item for item in CURRICULUM if item["day"] == day_num), None)
            if match:
                title = match["title"]
                desc = match.get("description", "")
                concepts = match.get("concepts", "")
            else:
                title = f"Project {day_num}"
                desc = ""
                concepts = ""
        except Exception:
            title = f"Project {day_num}"
            desc = ""
            concepts = ""
    else:
        title = sys.argv[2]
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        concepts = sys.argv[4] if len(sys.argv) > 4 else ""

    create_day(day_num, title, desc, concepts)

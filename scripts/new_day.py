#!/usr/bin/env python3
"""
30 Days Python Challenge - Day Generator CLI
Author: Tejas (@Tejas0113)

Usage:
    python scripts/new_day.py <day_number> "<title>" "<description>" [concepts...]
    
Example:
    python scripts/new_day.py 2 "Retro Arcade Snake Game" "Classic arcade snake game in Python" "Pygame, Game Loops, Collision"
"""

import sys
import subprocess
from pathlib import Path


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
    if len(sys.argv) < 3:
        print("Usage: python scripts/new_day.py <day_number> \"<title>\" [\"<description>\"] [\"<concepts>\"]")
        sys.exit(1)

    day_num = int(sys.argv[1])
    title = sys.argv[2]
    desc = sys.argv[3] if len(sys.argv) > 3 else ""
    concepts = sys.argv[4] if len(sys.argv) > 4 else ""

    create_day(day_num, title, desc, concepts)

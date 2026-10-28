#!/usr/bin/env python3
"""
30 Days Python Challenge - Git Hook Installer
Author: Tejas (@Tejas0113)

Installs a pre-commit hook that automatically updates the README.md
progress bar, badges, and challenge table every time you make a git commit.
"""

import sys
from pathlib import Path

HOOK_CONTENT = """#!/bin/sh
# 30 Days Python Challenge - Automated README updater
python3 scripts/update_tracker.py
git add README.md
"""


def install_hook():
    repo_root = Path(__file__).resolve().parent.parent
    hooks_dir = repo_root / ".git" / "hooks"

    if not hooks_dir.exists():
        print("❌ .git directory not found. Please initialize git first.")
        sys.exit(1)

    pre_commit_file = hooks_dir / "pre-commit"
    pre_commit_file.write_text(HOOK_CONTENT, encoding="utf-8")
    pre_commit_file.chmod(0o755)

    print("✅ Pre-commit hook installed successfully!")
    print("💡 Now every time you commit a new day or change, README.md will automatically update!")


if __name__ == "__main__":
    install_hook()

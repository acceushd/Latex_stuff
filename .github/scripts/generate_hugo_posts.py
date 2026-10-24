#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
latex_root = repo / "latex_files"
posts_dir = repo / "site" / "content" / "posts"

posts_dir.mkdir(parents=True, exist_ok=True)

for main_tex in sorted(latex_root.glob("*/main.tex")):
    name = main_tex.parent.name
    relative_dir = main_tex.parent.relative_to(repo).as_posix()

    result = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "log",
            "-1",
            "--format=%cI",
            "--",
            relative_dir,
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    lastmod = result.stdout.strip()

    if not lastmod:
        print(f"Skipping {name}: no Git history found")
        continue

    post = posts_dir / f"{name}.md"
    title = json.dumps(name)

    content = (
        "---\n"
        f"title: {title}\n"
        f"date: {json.dumps(lastmod)}\n"
        f"lastmod: {json.dumps(lastmod)}\n"
        "draft: false\n"
        "---\n"
        "\n"
        f'{{{{< pdf-list "{name}" >}}}}\n'
    )

    post.write_text(content, encoding="utf-8")
    print(f"Generated {post.relative_to(repo)} (last updated {lastmod})")

"""Build card.svg, the neofetch-style card shown in README.md.

    python build.py            # re-reads photo.jpg and refreshes GitHub stats
"""
import json
import os
import urllib.request
from html import escape
from pathlib import Path

USER = "gelodotdev"
HERE = Path(__file__).parent
ART = HERE / "portrait.txt"
WIDTH = 51  # characters in the info column

INFO = [
    ("header", "gelo@dotdev"),
    ("OS", "Windows 11, Kali Linux, Android"),
    ("Host", "BITS (Boarderz IT Solutions)"),
    ("Kernel", "Full-Stack Developer"),
    ("School", "ISAT University, BS Information Technology"),
    ("IDE", "VS Code, Cursor, Antigravity, PhpStorm"),
    ("gap", ""),
    ("Languages.Code", "PHP, JavaScript, C/C++, Kotlin, C#"),
    ("Languages.Markup", "HTML, CSS, Blade, SQL, JSON"),
    ("Frameworks", "Laravel, React, Bootstrap, Tailwind"),
    ("Languages.Real", "English, Filipino"),
    ("gap", ""),
    ("Hobbies.Software", "IoT web apps, AI agent tooling"),
    ("Hobbies.Hardware", "ESP32, Arduino, sensors"),
    ("Hobbies.Other", "Digital & traditional art"),
    ("gap", ""),
    ("header", "Contact"),
    ("Email", "sujedeangielou06@gmail.com"),
    ("GitHub", USER),
    ("Location", "Iloilo City, Philippines"),
    ("gap", ""),
    ("header", "GitHub Stats"),
]


def api(path):
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={"Accept": "application/vnd.github+json"})
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=20) as res:
        return json.load(res)


def stats():
    user = api(f"users/{USER}")
    repos = api(f"users/{USER}/repos?per_page=100")
    commits = api(f"search/commits?q=author:{USER}")["total_count"]
    return [
        ("Repos", str(user["public_repos"])),
        ("Stars", str(sum(r["stargazers_count"] for r in repos))),
        ("Commits", f"{commits:,}"),
        ("Followers", str(user["followers"])),
    ]


def info_line(kind, value):
    if kind == "gap":
        return ""
    if kind == "header":
        return f'{escape(value)} <tspan class="dim">{"-" * (WIDTH - len(value) - 1)}</tspan>'
    dots = "." * max(2, WIDTH - len(kind) - len(value) - 3)
    return f'<tspan class="key">{escape(kind)}</tspan>: <tspan class="dim">{dots}</tspan> <tspan class="val">{escape(value)}</tspan>'


def text_block(x, y, step, size, lines):
    rows = "".join(f'<tspan x="{x}" y="{y + i * step}">{line}</tspan>' for i, line in enumerate(lines))
    return f'<text font-size="{size}" xml:space="preserve">{rows}</text>'


def main():
    if (HERE / "photo.jpg").exists():
        from ascii import portrait
        ART.write_text("\n".join(portrait(HERE / "photo.jpg")) + "\n", encoding="utf-8")
    art = [escape(line) for line in ART.read_text(encoding="utf-8").splitlines()]
    info = [info_line(k, v) for k, v in INFO + stats()]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="985" height="560" viewBox="0 0 985 560" font-family="Consolas, 'Cascadia Mono', 'DejaVu Sans Mono', monospace">
<style>text{{fill:#c9d1d9;white-space:pre}}.key{{fill:#ffa657}}.val{{fill:#a5d6ff}}.dim{{fill:#616e7f}}</style>
<rect width="985" height="560" rx="15" fill="#161b22"/>
{text_block(20, 30, 14.4, 12, art)}
{text_block(470, 36, 20, 16, info)}
</svg>
'''
    (HERE / "card.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()

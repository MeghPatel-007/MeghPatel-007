import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    GITHUB_USERNAME, DISPLAY_NAME, ROLE, LOCATION, EDUCATION, FOCUS, PORTFOLIO_URL, SECTIONS
)
from theme import (
    FONT_FAMILY, BG, BG2, FRAME, MUTED, INK, BORDER_RADIUS, TITLEBAR_H, PAD, DOT_COLORS,
    KEY as KEY_COLOR, GREEN, ACCENT, INFO_STAGGER, INFO_DUR
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "info-card.svg"))
STATIC = bool(os.environ.get("STATIC"))

W = 480
KEY_X = PAD
VAL_X = PAD + 96
LINE_H = 20.5

def esc(s):
    return html.escape(str(s))

def rise(inner, i):
    """fade + slight upward slide, staggered by row index; freezes visible."""
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * INFO_STAGGER
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="{INFO_DUR:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="{INFO_DUR:.2f}s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')

# 1. Build row data dynamically from config
rows = [
    ("host",),
    ("kv", "Name", DISPLAY_NAME),
    ("kv", "Username", GITHUB_USERNAME),
    ("kv", "Role", ROLE),
    ("kv", "Location", LOCATION),
    ("kv", "Education", EDUCATION),
    ("kv", "Focus", FOCUS),
]

for sec_name, sec_items in SECTIONS.items():
    rows.append(("kv", sec_name, ", ".join(sec_items)))

rows.append(("kv", "Website", PORTFOLIO_URL))
rows.append(("kv", "GitHub", f"https://github.com/{GITHUB_USERNAME}"))

# 2. Render rows to calculate exact content height dynamically
rows_content = []
y = TITLEBAR_H + 25
for i, row in enumerate(rows):
    kind = row[0]
    if kind == "host":
        host_text = f"{GITHUB_USERNAME.lower()}@github"
        host_width = round(len(host_text) * 9.6)
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
                 f'<tspan fill="{GREEN}">{GITHUB_USERNAME.lower()}</tspan><tspan fill="{MUTED}">@</tspan>'
                 f'<tspan fill="{ACCENT}">github</tspan></text>'
                 f'<line x1="{KEY_X+host_width}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY_COLOR}" font-size="12.5" font-weight="700">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{val}</text>')
    
    rows_content.append(rise(inner, i))
    y += LINE_H

H = round(y + PAD - 5)

# 3. Assemble and save the SVG
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="{FONT_FAMILY}">',
    '<defs>',
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">',
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
    f'</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="{BORDER_RADIUS}" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="{BORDER_RADIUS}" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dotcol in enumerate(DOT_COLORS):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">{GITHUB_USERNAME.lower()}@github: ~$ neofetch</text>')

parts.extend(rows_content)
parts.append("</svg>")

svg = "".join(parts)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"wrote {OUT} {len(svg)} bytes; {W} x {H}")

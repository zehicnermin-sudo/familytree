# -*- coding: utf-8 -*-
"""
Verification of node coordinate generation against actual SVG content.
"""
import re
import json
from generate_master_bosnian_poster import BilateralPosterEngine, raw_data

engine = BilateralPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_bilateral()

all_x = [n["x"] for n in nodes] + [n["x"] + n["w"] for n in nodes]
all_y = [n["y"] for n in nodes] + [n["y"] + n["h"] for n in nodes]
raw_min_x = min(all_x) - 100
shift_x = -raw_min_x
shift_y = 0

print(f"Computed shift_x: {shift_x}, shift_y: {shift_y}")

# Let's check Fatima Sajtan
for n in nodes:
    if "Fatima" in n["name"]:
        cx = n["x"] + shift_x + n["w"]/2
        cy = n["y"] + shift_y + n["h"]/2
        print(f"Fatima ({n.get('branch')}): x={n['x'] + shift_x}, y={n['y'] + shift_y}, cx={cx}, cy={cy}")

# Let's check what is in Porodicno_Stablo_Zehic_A0.svg for Fatima
with open("Porodicno_Stablo_Zehic_A0.svg", "r", encoding="utf-8") as f:
    svg = f.read()

for m in re.finditer(r'<g transform="translate\(([^,]+),\s*([^)]+)\)">(.*?)</g>', svg, re.DOTALL):
    tx = float(m.group(1))
    ty = float(m.group(2))
    chunk = m.group(3)
    if "Fatima" in chunk:
        # print first text
        name_m = re.search(r'<text[^>]*font-weight="900"[^>]*>([^<]+)</text>', chunk)
        name_str = name_m.group(1) if name_m else "???"
        print(f"SVG Match: '{name_str}' at ({tx}, {ty}), center=({tx+119}, {ty+35})")

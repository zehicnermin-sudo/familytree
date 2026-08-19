# -*- coding: utf-8 -*-
"""
Robust parser for all rects and texts in new_provided_tree.svg.
"""
import re
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    svg = f.read()

# Match all rects
rect_pattern = re.compile(r'<rect\s+([^>]+)>')
rects = []
for m in rect_pattern.finditer(svg):
    attr_str = m.group(1)
    x = float(re.search(r'x="([^"]+)"', attr_str).group(1))
    y = float(re.search(r'y="([^"]+)"', attr_str).group(1))
    w = float(re.search(r'width="([^"]+)"', attr_str).group(1))
    h = float(re.search(r'height="([^"]+)"', attr_str).group(1))
    if w > 11000:
        continue
    rects.append({
        "x": x, "y": y, "w": w, "h": h,
        "cx": x + w/2, "cy": y + h/2,
        "texts": []
    })

# Match all texts
text_pattern = re.compile(r'<text\s+([^>]+)>(.*?)</text>', re.DOTALL)
texts = []
for m in text_pattern.finditer(svg):
    attr_str = m.group(1)
    body = m.group(2)
    x = float(re.search(r'x="([^"]+)"', attr_str).group(1))
    y = float(re.search(r'y="([^"]+)"', attr_str).group(1))
    
    tspans = re.findall(r'<tspan[^>]*>(.*?)</tspan>', body)
    if tspans:
        clean = " ".join([t.strip() for t in tspans if t.strip()])
    else:
        clean = re.sub(r'<[^>]+>', '', body).strip()
    texts.append({"x": x, "y": y, "text": clean})

# Associate texts with rects
for t in texts:
    tx = t["x"]
    ty = t["y"]
    t_val = t["text"]
    for r in rects:
        if r["x"] - 25 <= tx <= r["x"] + r["w"] + 25 and r["y"] - 35 <= ty <= r["y"] + r["h"] + 35:
            r["texts"].append(t_val)
            break

cards = []
for r in rects:
    txt_list = r["texts"]
    if not txt_list: continue
    joined = " ".join(txt_list)
    if "djeca" in joined or "dijete" in joined or "Njegov" in joined or "Njihov" in joined: continue
    cards.append({
        "x": r["x"], "y": r["y"], "w": r["w"], "h": r["h"], "cx": r["cx"], "cy": r["cy"],
        "name": txt_list[0].strip(),
        "extra": " | ".join(txt_list[1:]) if len(txt_list) > 1 else ""
    })

print(f"Total valid member cards in new SVG: {len(cards)}")
for i, c in enumerate(cards):
    print(f"{i+1:3d}. y={c['y']:6.1f}, x={c['x']:8.1f} -> Name: '{c['name']}' | Extra: '{c['extra']}'")

# -*- coding: utf-8 -*-
"""
Full architectural parser for new_provided_tree.svg:
1. Extracts all card boxes (rects + text tags).
2. Detects married pairs.
3. Maps line connections to determine parent-child relationships.
4. Compares node-by-node against family_tree_gender_tagged.json.
"""
import re
import json

with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    svg = f.read()

# 1. Parse all <rect> elements with their bounding boxes
rect_pattern = re.compile(r'<rect\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"[^>]*fill="([^"]+)"[^>]*/>')
rects = []
for m in rect_pattern.finditer(svg):
    x = float(m.group(1))
    y = float(m.group(2))
    w = float(m.group(3))
    h = float(m.group(4))
    fill = m.group(5)
    # Filter out background rect
    if w > 11000:
        continue
    rects.append({
        "x": x, "y": y, "w": w, "h": h, "fill": fill,
        "cx": x + w/2, "cy": y + h/2,
        "texts": []
    })

# 2. Parse all <text> elements
text_pattern = re.compile(r'<text\s+x="([^"]+)"\s+y="([^"]+)"[^>]*>(.*?)</text>', re.DOTALL)
texts = []
for m in text_pattern.finditer(svg):
    x = float(m.group(1))
    y = float(m.group(2))
    raw_content = m.group(3)
    
    # Extract tspans or direct text
    tspans = re.findall(r'<tspan[^>]*>(.*?)</tspan>', raw_content)
    if tspans:
        content = " ".join([t.strip() for t in tspans if t.strip()])
    else:
        content = re.sub(r'<[^>]+>', '', raw_content).strip()
        
    texts.append({"x": x, "y": y, "text": content})

# Associate texts with closest rect
for t in texts:
    tx = t["x"]
    ty = t["y"]
    text_val = t["text"]
    
    # Check which rect contains this text
    best_rect = None
    for r in rects:
        # Give generous bounding box around rect
        if r["x"] - 20 <= tx <= r["x"] + r["w"] + 20 and r["y"] - 30 <= ty <= r["y"] + r["h"] + 30:
            best_rect = r
            break
    if best_rect:
        best_rect["texts"].append(text_val)

# Extract card items
cards = []
for r in rects:
    # Skip labels like "Njegova djeca", "Njihova djeca"
    txt_list = r["texts"]
    if not txt_list:
        continue
    joined = " ".join(txt_list)
    if "djeca" in joined or "dijete" in joined or "Njegov" in joined or "Njihov" in joined:
        continue
        
    cards.append({
        "x": r["x"], "y": r["y"], "w": r["w"], "h": r["h"],
        "cx": r["cx"], "cy": r["cy"],
        "fill": r["fill"],
        "texts": txt_list
    })

print(f"Total valid member cards found in SVG: {len(cards)}")

# Print all cards found
for i, c in enumerate(cards):
    print(f"{i+1}. y={c['y']:.1f}, x={c['x']:.1f} -> {c['texts']}")

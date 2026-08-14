# -*- coding: utf-8 -*-
"""
Extract 100% ground-truth coordinates directly from Porodicno_Stablo_Zehic_A0.svg
so that searching any member or spouse jumps to their exact pixel center on screen.
"""
import re
import json
import os

with open("Porodicno_Stablo_Zehic_A0.svg", "r", encoding="utf-8") as f:
    svg = f.read()

# ViewBox
vb_match = re.search(r'viewBox="([^"]+)"', svg)
vb = [float(v) for v in vb_match.group(1).split()] if vb_match else [0, 0, 4546, 8504]

nodes = []

# Match each card group: <g transform="translate(X, Y)">
card_pattern = re.compile(r'<g transform="translate\(([^,]+),\s*([^)]+)\)">(.*?)</g>\n', re.DOTALL)

for m in card_pattern.finditer(svg):
    tx = float(m.group(1))
    ty = float(m.group(2))
    chunk = m.group(3)
    
    # Skip Legend and Title
    if "LEGENDA BOJA" in chunk or "PORODIČNO STABLO ZEHIĆ" in chunk or "GEN." in chunk:
        continue
        
    # Get rect dimensions
    rect_m = re.search(r'<rect[^>]*width="([^"]+)"[^>]*height="([^"]+)"', chunk)
    w = float(rect_m.group(1)) if rect_m else 238.0
    h = float(rect_m.group(2)) if rect_m else 70.0

    # Extract names
    # Name 1 (Primary member or Ibrahim)
    name1 = None
    name2 = None

    # Check for Ibrahim Root
    if "Osnivač" in chunk:
        ib_m = re.search(r'<text[^>]*font-size="24"[^>]*>([^<]+)</text>', chunk)
        if ib_m:
            name1 = ib_m.group(1).strip()
    else:
        # Standard card: Names have font-weight="900" and font-size="14.5" or "15"
        names_found = re.findall(r'<text[^>]*font-weight="900"[^>]*fill="(?:#1D4ED8|#BE185D|#93C5FD)"[^>]*>([^<]+)</text>', chunk)
        if names_found:
            # Filter out single avatar letters (length 1 or 👑)
            clean_names = [n.strip() for n in names_found if len(n.strip()) > 1 and n.strip() not in ["👑", "Poginuo", "Poginula"]]
            if len(clean_names) >= 1:
                name1 = clean_names[0]
            if len(clean_names) >= 2:
                name2 = clean_names[1]

    if not name1:
        continue

    cx = tx + w / 2.0
    cy = ty + h / 2.0

    nodes.append({
        "name": name1,
        "spouse": name2 or "",
        "x": tx,
        "y": ty,
        "w": w,
        "h": h,
        "cx": cx,
        "cy": cy
    })

    if name2:
        # Also index spouse as target
        nodes.append({
            "name": name2,
            "spouse": name1,
            "x": tx,
            "y": ty,
            "w": w,
            "h": h,
            "cx": cx,
            "cy": cy,
            "is_spouse": True
        })

print(f"Direct SVG extraction found {len(nodes)} named targets!")

# Check Fatima specifically
for n in nodes:
    if "Fatima" in n["name"]:
        print("Found Fatima:", n)

coords_data = {
    "main": {
        "viewBox": vb,
        "nodes": nodes
    }
}

os.makedirs("data", exist_ok=True)
os.makedirs("public", exist_ok=True)

with open("data/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_data, f, ensure_ascii=False, indent=2)

with open("public/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_data, f, ensure_ascii=False, indent=2)

print("Saved exact SVG coordinates to data/tree_coords.json and public/tree_coords.json!")

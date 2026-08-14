# -*- coding: utf-8 -*-
"""
Extract exact coordinates of all nodes from Porodicno_Stablo_Zehic_A0.svg and branch SVGs
to enable instant zero-DOM-search and zero-lag mobile zooming/navigation.
"""
import os
import re
import json

coords_data = {}

def extract_from_svg(svg_path, tree_key):
    if not os.path.exists(svg_path):
        return []
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    vb_match = re.search(r'viewBox="([^"]+)"', content)
    vb = vb_match.group(1).split() if vb_match else [0, 0, 4546, 8504]
    
    nodes = []
    # Pattern to match cards with <g transform="translate(x, y)">
    pattern = re.compile(r'<g transform="translate\(([^,]+),\s*([^)]+)\)">(.*?)</g>', re.DOTALL)
    for m in pattern.finditer(content):
        x = float(m.group(1))
        y = float(m.group(2))
        chunk = m.group(3)
        
        # Extract names from text tags
        texts = re.findall(r'<text[^>]*>(.*?)</text>', chunk)
        if not texts:
            continue
            
        # Clean text
        clean_texts = [t.strip() for t in texts if t.strip() and not t.startswith("GEN.") and "LEGENDA" not in t]
        if not clean_texts:
            continue
            
        name = clean_texts[0]
        spouse_name = clean_texts[1] if len(clean_texts) > 1 and "🗓" not in clean_texts[1] and "u." not in clean_texts[1] and "r." not in clean_texts[1] else ""
        
        nodes.append({
            "name": name,
            "spouse": spouse_name,
            "x": x,
            "y": y,
            "cx": x + 119,
            "cy": y + 35,
            "tree": tree_key
        })
    return {"viewBox": [float(v) for v in vb], "nodes": nodes}

coords_data["main"] = extract_from_svg("Porodicno_Stablo_Zehic_A0.svg", "main")
coords_data["adem"] = extract_from_svg("Branche_Adem.svg", "adem")
coords_data["osman"] = extract_from_svg("Branche_Osman.svg", "osman")
coords_data["meho"] = extract_from_svg("Branche_Meho.svg", "meho")

os.makedirs("data", exist_ok=True)
os.makedirs("public", exist_ok=True)

with open("data/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_data, f, ensure_ascii=False, indent=2)

with open("public/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_data, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(coords_data['main']['nodes'])} main nodes coordinates!")

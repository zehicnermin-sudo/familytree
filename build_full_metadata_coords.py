# -*- coding: utf-8 -*-
"""
Build complete metadata-rich coordinate index for all 416 members.
Links each database record with its exact SVG canvas (cx, cy) coordinate.
"""
import json
import os
from generate_master_bosnian_poster import BilateralPosterEngine, raw_data

engine = BilateralPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_bilateral()

all_x = [n["x"] for n in nodes] + [n["x"] + n["w"] for n in nodes]
raw_min_x = min(all_x) - 100
shift_x = -raw_min_x
shift_y = 0

# Build parent mapping from raw_data
parent_map = {}
def map_parents(node_list, p_name=""):
    for item in node_list:
        name = item.get("name", "")
        if name:
            parent_map[name.lower()] = p_name
        children = item.get("children", [])
        if children:
            map_parents(children, name)

for root_b in raw_data.get("children", []):
    r_name = root_b.get("name", "")
    map_parents([root_b], "Ibrahim")

all_targets = []

for n in nodes:
    x = n["x"] + shift_x
    y = n["y"] + shift_y
    w, h = n["w"], n["h"]
    cx = x + w / 2.0
    cy = y + h / 2.0
    
    name = n["name"]
    branch = n.get("branch", "")
    gender = n.get("gender", "M")
    gen = n.get("generation", 1)
    
    # lookup parent name
    p_name = parent_map.get(name.lower(), "")
    
    spouse = n.get("spouse", {})
    spouse_name = spouse.get("name", "") if (n.get("has_spouse") and spouse) else ""

    all_targets.append({
        "name": name,
        "parent": p_name,
        "spouse": spouse_name,
        "branch": branch,
        "gen": gen,
        "gender": gender,
        "x": x,
        "y": y,
        "cx": cx,
        "cy": cy
    })

    if spouse_name:
        all_targets.append({
            "name": spouse_name,
            "parent": "",
            "spouse": name,
            "branch": branch,
            "gen": gen,
            "gender": spouse.get("gender", "F" if gender == "M" else "M"),
            "x": x,
            "y": y,
            "cx": cx,
            "cy": cy,
            "is_spouse": True
        })

print(f"Generated {len(all_targets)} rich coordinate records!")

coords_data = {
    "main": {
        "viewBox": [0, 0, 4546, 8504],
        "nodes": all_targets
    }
}

os.makedirs("data", exist_ok=True)
os.makedirs("public", exist_ok=True)

with open("data/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_data, f, ensure_ascii=False, indent=2)

with open("public/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_data, f, ensure_ascii=False, indent=2)

print("Updated data/tree_coords.json and public/tree_coords.json!")

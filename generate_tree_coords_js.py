# -*- coding: utf-8 -*-
"""
Generates a standalone tree_coords.js and data/tree_coords.json with exact coordinates
for all 416 members, with zero dependency on fetch or network latency.
"""
import json
import os
from generate_master_bosnian_poster import BilateralPosterEngine, raw_data

engine = BilateralPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_bilateral()

raw_min_x = min(n["x"] for n in nodes) - 40
shift_x = -raw_min_x
shift_y = 0

parent_map = {}
def map_parents(node_list, p_name=""):
    for item in node_list:
        name = item.get("name", "")
        if name:
            parent_map[name.lower().strip()] = p_name.strip()
        children = item.get("children", [])
        if children:
            map_parents(children, name)

for root_b in raw_data.get("children", []):
    map_parents([root_b], "Ibrahim")

all_targets = []

for n in nodes:
    x = round(n["x"] + shift_x, 1)
    y = round(n["y"] + shift_y, 1)
    w, h = n["w"], n["h"]
    cx = round(x + w / 2.0, 1)
    cy = round(y + h / 2.0, 1)
    
    name = n["name"].strip()
    branch = n.get("branch", "").strip()
    gender = n.get("gender", "M").strip()
    gen = n.get("generation", 1)
    
    p_name = parent_map.get(name.lower(), "")
    
    spouse = n.get("spouse", {})
    spouse_name = spouse.get("name", "").strip() if (n.get("has_spouse") and spouse) else ""

    all_targets.append({
        "name": name,
        "parent": p_name,
        "spouse": spouse_name,
        "branch": branch,
        "gen": gen,
        "gender": gender,
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
            "cx": cx,
            "cy": cy,
            "is_spouse": True
        })

print(f"Generated {len(all_targets)} coordinate records!")

coords_payload = {"main": {"viewBox": [0, 0, 4546, 8504], "nodes": all_targets}}

# 1. Write tree_coords.js
js_content = f"window.ZEHIC_TREE_COORDS = {json.dumps(coords_payload, ensure_ascii=False)};"

with open("tree_coords.js", "w", encoding="utf-8") as f:
    f.write(js_content)

with open("public/tree_coords.js", "w", encoding="utf-8") as f:
    f.write(js_content)

# 2. Write JSON fallbacks
with open("data/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_payload, f, ensure_ascii=False)

with open("public/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_payload, f, ensure_ascii=False)

with open("tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_payload, f, ensure_ascii=False)

print("Saved tree_coords.js, public/tree_coords.js and json files successfully!")

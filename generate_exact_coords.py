# -*- coding: utf-8 -*-
"""
Accurately generates data/tree_coords.json and public/tree_coords.json
using the true node objects and their exact calculated (cx, cy) canvas positions.
"""
import json
import os

from generate_master_bosnian_poster import BilateralPosterEngine, raw_data

engine = BilateralPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_bilateral()

shift_x = 2273
shift_y = top_off + 40

main_nodes = []

for n in nodes:
    x = n["x"] + shift_x
    y = n["y"] + shift_y
    w, h = n["w"], n["h"]
    name = n["name"]
    spouse_name = n.get("spouse", {}).get("name", "") if n.get("has_spouse") and n.get("spouse") else ""
    
    main_nodes.append({
        "name": name,
        "spouse": spouse_name,
        "x": x,
        "y": y,
        "cx": x + w / 2,
        "cy": y + h / 2,
        "branch": n.get("branch", "root"),
        "gen": n.get("generation", 1),
        "gender": n.get("gender", "M")
    })

# Also include spouse as a searchable direct target
spouse_nodes = []
for n in nodes:
    if n.get("has_spouse") and n.get("spouse"):
        sp = n["spouse"]
        x = n["x"] + shift_x
        y = n["y"] + shift_y
        w, h = n["w"], n["h"]
        sp_name = sp.get("name", "")
        if sp_name:
            spouse_nodes.append({
                "name": sp_name,
                "spouse": n["name"],
                "x": x,
                "y": y,
                "cx": x + w / 2,
                "cy": y + h / 2,
                "branch": n.get("branch", "root"),
                "gen": n.get("generation", 1),
                "gender": sp.get("gender", "F"),
                "is_spouse_card": True
            })

all_main_nodes = main_nodes + spouse_nodes

coords_data = {
    "main": {
        "viewBox": [0, 0, 4546, 8504],
        "nodes": all_main_nodes
    }
}

os.makedirs("data", exist_ok=True)
os.makedirs("public", exist_ok=True)

with open("data/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_data, f, ensure_ascii=False, indent=2)

with open("public/tree_coords.json", "w", encoding="utf-8") as f:
    json.dump(coords_data, f, ensure_ascii=False, indent=2)

print(f"Successfully exported {len(all_main_nodes)} exact card coordinates (main & spouses)!")

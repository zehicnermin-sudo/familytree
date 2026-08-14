# -*- coding: utf-8 -*-
"""
Map database members directly to their exact placed cards in Porodicno_Stablo_Zehic_A0.svg.
"""
import json
import os
from generate_master_bosnian_poster import BilateralPosterEngine, raw_data

engine = BilateralPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_bilateral()

all_x = [n["x"] for n in nodes] + [n["x"] + n["w"] for n in nodes]
raw_min_x = min(all_x) - 100
shift_x = -raw_min_x  # exactly 2273.0 or 2293.0
shift_y = 0

print(f"Shift X: {shift_x}, Shift Y: {shift_y}")

mapped_nodes = []

for n in nodes:
    x = n["x"] + shift_x
    y = n["y"] + shift_y
    w, h = n["w"], n["h"]
    cx = x + w / 2.0
    cy = y + h / 2.0
    
    parent_name = n.get("parent_name", "")
    spouse = n.get("spouse", {})
    spouse_name = spouse.get("name", "") if (n.get("has_spouse") and spouse) else ""

    item = {
        "id": n.get("id", ""),
        "name": n["name"],
        "spouse": spouse_name,
        "parent": parent_name,
        "branch": n.get("branch", ""),
        "gen": n.get("generation", 1),
        "gender": n.get("gender", "M"),
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "cx": cx,
        "cy": cy
    }
    mapped_nodes.append(item)
    
    # If there is a spouse, also add spouse entry pointing to same card
    if spouse_name:
        mapped_nodes.append({
            "id": f"sp_{n.get('id', '')}",
            "name": spouse_name,
            "spouse": n["name"],
            "parent": "",
            "branch": n.get("branch", ""),
            "gen": n.get("generation", 1),
            "gender": spouse.get("gender", "F" if n.get("gender") == "M" else "M"),
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "cx": cx,
            "cy": cy,
            "is_spouse": True
        })

print(f"Total mapped nodes: {len(mapped_nodes)}")

# Let's test Fatima Sajtana
for m in mapped_nodes:
    if "Fatima" in m["name"]:
        print(f"Fatima -> Gen:{m['gen']}, Branch:{m['branch']}, Parent:{m['parent']}, Spouse:{m['spouse']}, cx={m['cx']}, cy={m['cy']}")

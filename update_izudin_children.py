# -*- coding: utf-8 -*-
"""
Update Izudin & Maksida lineage:
1. Alma: gender F (roze), notes "u. Brnjik", child Adin (gender M, plava).
2. Amra: gender F (roze), notes "u. Mumbašići", child Faris (gender M, plava).
"""
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Find Osman -> Šaćir -> Avdo -> Izudin
root = data["root"]
osman_node = None
for b in root["children_branches"]:
    if "Osman" in b["branch_name"]:
        osman_node = b["person"]
        break

sacir_node = None
for ch in osman_node.get("children", []):
    if ch.get("id") == "sacir_osman" or ch.get("name") == "Šaćir":
        sacir_node = ch
        break

avdo_node = None
for ch in sacir_node.get("children", []):
    if ch["name"] == "Avdo":
        avdo_node = ch
        break

izudin_node = None
for ch in avdo_node.get("children", []):
    if ch["name"] == "Izudin":
        izudin_node = ch
        break

print("Found Izudin:", izudin_node["name"])

# Update children of Izudin
izudin_node["children"] = [
    {
        "id": "alma_izudin",
        "name": "Alma",
        "gen": 6,
        "gender": "F",
        "notes": "u. Brnjik",
        "children": [
            {
                "id": "adin_alma",
                "name": "Adin",
                "gen": 7,
                "gender": "M",
                "notes": ""
            }
        ]
    },
    {
        "id": "amra_izudin",
        "name": "Amra",
        "gen": 6,
        "gender": "F",
        "notes": "u. Mumbašići",
        "children": [
            {
                "id": "faris_amra",
                "name": "Faris",
                "gen": 7,
                "gender": "M",
                "notes": ""
            }
        ]
    }
]

print("Updated Alma and Amra with children Adin and Faris!")

with open("family_tree_gender_tagged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("family_tree_structured.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved updated json datasets!")

# -*- coding: utf-8 -*-
"""
Add children to Omer's daughters (under Šaćir):
1. Zehrina -> Emina (F, roze), Edina (F, roze)
2. Nermina -> Almin (M, plava), Kenan (M, plava), Neyla (F, roze)
3. Zekira -> Aldin (M, plava), Naida (F, roze)
"""
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

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

omer_node = None
for ch in sacir_node.get("children", []):
    if ch["name"] == "Omer":
        omer_node = ch
        break

print("Found Omer under Šaćir:", omer_node["name"])

for ch in omer_node.get("children", []):
    if ch["name"] == "Zehrina":
        ch["children"] = [
            {"id": "emina_zehrina", "name": "Emina", "gen": 6, "gender": "F", "notes": ""},
            {"id": "edina_zehrina", "name": "Edina", "gen": 6, "gender": "F", "notes": ""}
        ]
        print("Added Emina & Edina to Zehrina")
    elif ch["name"] == "Nermina":
        ch["children"] = [
            {"id": "almin_nermina", "name": "Almin", "gen": 6, "gender": "M", "notes": ""},
            {"id": "kenan_nermina", "name": "Kenan", "gen": 6, "gender": "M", "notes": ""},
            {"id": "neyla_nermina", "name": "Neyla", "gen": 6, "gender": "F", "notes": ""}
        ]
        print("Added Almin, Kenan & Neyla to Nermina")
    elif ch["name"] == "Zekira":
        ch["children"] = [
            {"id": "aldin_zekira", "name": "Aldin", "gen": 6, "gender": "M", "notes": ""},
            {"id": "naida_zekira", "name": "Naida", "gen": 6, "gender": "F", "notes": ""}
        ]
        print("Added Aldin & Naida to Zekira")

with open("family_tree_gender_tagged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("family_tree_structured.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved all updates successfully!")

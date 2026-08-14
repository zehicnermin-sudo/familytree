# -*- coding: utf-8 -*-
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

root = data["root"]
osman_branch = None
for b in root["children_branches"]:
    if "Osman" in b["branch_name"]:
        osman_branch = b["person"]
        break

sacir_node = None
for ch in osman_branch.get("children", []):
    if ch.get("id") == "sacir_osman" or ch.get("name") == "Šaćir":
        sacir_node = ch
        break

print("Found exact Šaćir:", sacir_node["name"], sacir_node.get("id"))

# 1. Update under Avdo (son of Šaćir)
avdo_node = None
omer_node = None
for ch in sacir_node.get("children", []):
    if ch["name"] == "Avdo":
        avdo_node = ch
    elif ch["name"] == "Omer":
        omer_node = ch

print("Found Avdo under Šaćir:", avdo_node["name"])
print("Found Omer under Šaćir:", omer_node["name"])

# Avdo -> Izudin & Mevludin
for ch in avdo_node.get("children", []):
    if ch["name"] == "Izudin":
        ch["spouse"] = {
            "name": "Maksida",
            "notes": "Supruga",
            "gender": "F"
        }
        print("Added Maksida to Izudin")
    elif ch["name"] == "Mevludin":
        ch["spouse"] = {
            "name": "Remzija",
            "notes": "Supruga",
            "gender": "F"
        }
        print("Added Remzija to Mevludin")
        # Mevludin -> Asmir
        for m_ch in ch.get("children", []):
            if m_ch["name"] == "Asmir":
                m_ch["spouse"] = {
                    "name": "Admira",
                    "notes": "Supruga",
                    "gender": "F"
                }
                print("Added Admira to Asmir")

# 2. Update under Omer (son of Šaćir) -> Nermin
for ch in omer_node.get("children", []):
    if ch["name"] == "Nermin":
        ch["spouse"] = {
            "name": "Ševala",
            "notes": "Supruga",
            "gender": "F"
        }
        print("Added Ševala to Nermin")

with open("family_tree_gender_tagged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("family_tree_structured.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("All 4 spouses successfully added!")

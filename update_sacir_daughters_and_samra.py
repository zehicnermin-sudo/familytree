# -*- coding: utf-8 -*-
"""
Update Šaćir lineage:
1. Mevla: "u. Šahići-Centar"
2. Seida: "u. Šepak"
3. Azijada: "u. Atmačići"
4. Samra: 2 children -> Ajla (F, roze), Dženan (M, plava)
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

print("Found Šaćir:", sacir_node["name"])

# 1. Update daughters of Šaćir: Mevla, Seida, Azijada
for ch in sacir_node.get("children", []):
    if ch["name"] == "Mevla":
        ch["notes"] = "u. Šahići-Centar"
        ch["gender"] = "F"
        print("Updated Mevla -> u. Šahići-Centar")
    elif ch["name"] == "Seida":
        ch["notes"] = "u. Šepak"
        ch["gender"] = "F"
        print("Updated Seida -> u. Šepak")
    elif ch["name"] == "Azijada":
        ch["notes"] = "u. Atmačići"
        ch["gender"] = "F"
        print("Updated Azijada -> u. Atmačići")
    elif ch["name"] == "Avdo":
        # Avdo -> Mevludin -> Samra
        for a_ch in ch.get("children", []):
            if a_ch["name"] == "Mevludin":
                for m_ch in a_ch.get("children", []):
                    if m_ch["name"] == "Samra":
                        m_ch["children"] = [
                            {
                                "id": "ajla_samra",
                                "name": "Ajla",
                                "gen": 7,
                                "gender": "F",
                                "notes": ""
                            },
                            {
                                "id": "dzenan_samra",
                                "name": "Dženan",
                                "gen": 7,
                                "gender": "M",
                                "notes": ""
                            }
                        ]
                        print("Added children Ajla (F) and Dženan (M) to Samra!")

with open("family_tree_gender_tagged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("family_tree_structured.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved all updates successfully!")

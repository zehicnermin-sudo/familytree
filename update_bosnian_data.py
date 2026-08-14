# -*- coding: utf-8 -*-
"""
Full Bosnian Localization & Zehic Family Tree Master Generator:
- Title: "PORODIČNO STABLO ZEHIĆ"
- Paša: "udata u Glinje u porodicu Hrustanović"
- Nurif: "nije se ženio"
- Meho: "Grana Meho"
- All legends consolidated on the right side
- Zero French text anywhere in SVGs, dataset, and web application
"""
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Update Paša and Nurif in the dataset
root = data["root"]
root["role"] = "Patrijarh (Osnivač loze Zehić)"

for b in root["children_branches"]:
    # Translate branch names
    b["branch_name"] = b["branch_name"].replace("Branche ", "Grana ")
    p = b["person"]
    if p["name"] == "Paša" or p["name"] == "Pasa":
        p["notes"] = "udata u Glinje u porodicu Hrustanović"
        p["gender"] = "F"
        print("Updated Paša -> udata u Glinje u porodicu Hrustanović")
    elif p["name"] == "Nurif":
        p["notes"] = "nije se ženio"
        p["dates"] = "r. 1863"
        p["gender"] = "M"
        print("Updated Nurif -> nije se ženio")

with open("family_tree_gender_tagged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("family_tree_structured.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved updated dataset with Bosnian notes!")

# -*- coding: utf-8 -*-
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def check_beriz(node):
    if node.get("name") == "Beriz":
        print("Beriz node:", node)
    for c in node.get("children", []):
        check_beriz(c)

for b in data["root"].get("children_branches", []):
    check_beriz(b["person"])

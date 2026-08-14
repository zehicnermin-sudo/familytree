# -*- coding: utf-8 -*-
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def check_mustafa(node):
    if node.get("name") == "Mustafa":
        print("Mustafa node:", node)
    for c in node.get("children", []):
        check_mustafa(c)

for b in data["root"].get("children_branches", []):
    check_mustafa(b["person"])

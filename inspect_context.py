# -*- coding: utf-8 -*-
"""
Inspect specific ambiguous names in context
"""
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def find_person(node, path=""):
    name = node.get("name")
    cur_path = f"{path} -> {name}"
    if name in ["Bekrija", "Bahrija", "Pašaga", "Hida", "Husnija", "Nurija"]:
        print(f"Person: {name} (Gender: {node.get('gender')}, Notes: {node.get('notes')}) at {cur_path}")
        if "spouse" in node:
            print(f"   Spouse: {node['spouse']}")
    if "spouse" in node:
        sp_name = node["spouse"].get("name")
        if sp_name in ["Bekrija", "Bahrija", "Pašaga", "Hida", "Husnija", "Nurija"]:
            print(f"Spouse: {sp_name} (Gender: {node['spouse'].get('gender')}, Notes: {node['spouse'].get('notes')}) at {cur_path}")
    for c in node.get("children", []):
        find_person(c, cur_path)

find_person(data["root"])
for b in data["root"].get("children_branches", []):
    find_person(b["person"], b["branch_name"])


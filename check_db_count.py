# -*- coding: utf-8 -*-
"""
Parse and compare the user's provided SVG structure with family_tree_gender_tagged.json
"""
import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read current database
with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    master_tree = json.load(f)

# Flatten current tree
current_list = []
def flatten(node, parent="", branch=""):
    name = node.get("name", "").strip()
    b = branch or node.get("branch", "")
    sp = node.get("spouse", {})
    sp_name = sp.get("name", "").strip() if sp else ""
    current_list.append({
        "name": name,
        "parent": parent,
        "branch": b,
        "spouse": sp_name,
        "notes": node.get("notes", ""),
        "children": [c.get("name") for c in node.get("children", [])]
    })
    for c in node.get("children", []):
        flatten(c, name, b if b != "Korijen" else c.get("name", ""))

flatten(master_tree, "", "Korijen")

print(f"Current master database members: {len(current_list)}")

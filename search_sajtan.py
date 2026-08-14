# -*- coding: utf-8 -*-
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def search_nodes(node, path=""):
    name = node.get("name", "")
    notes = node.get("notes", "")
    sp_name = node.get("spouse", {}).get("name", "") if "spouse" in node else ""
    
    if any(k in name.lower() or k in notes.lower() or k in sp_name.lower() for k in ["sajtan", "ismet", "hajrija", "izet", "muzijet"]):
        print(f"Found: {name} (Spouse: {sp_name}) [Path: {path}]")
        print(f"  Node JSON: {json.dumps(node, ensure_ascii=False)}")
    
    for ch in node.get("children", []):
        search_nodes(ch, f"{path} > {name}")

for b in data["root"]["children_branches"]:
    search_nodes(b["person"], b["branch_name"])

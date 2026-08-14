# -*- coding: utf-8 -*-
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def check_poginuli(node, path=""):
    name = node.get("name", "")
    gender = node.get("gender", "")
    notes = node.get("notes", "")
    if "pogin" in notes.lower():
        print(f"Primary: {name} ({gender}) -> notes: '{notes}' [Path: {path}]")
    
    if "spouse" in node:
        sp = node["spouse"]
        sp_name = sp.get("name", "")
        sp_gender = sp.get("gender", "")
        sp_notes = sp.get("notes", "")
        if "pogin" in sp_notes.lower():
            print(f"Spouse: {sp_name} ({sp_gender}) of {name} -> notes: '{sp_notes}'")

    for ch in node.get("children", []):
        check_poginuli(ch, f"{path} > {name}")

root = data["root"]
for b in root.get("children_branches", []):
    check_poginuli(b["person"], b["branch_name"])

# -*- coding: utf-8 -*-
"""
Audit all 401 names in family tree
"""
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

people = []

def traverse(node):
    p = {
        "id": node.get("id"),
        "name": node.get("name"),
        "gender": node.get("gender"),
        "notes": node.get("notes", ""),
        "has_spouse": "spouse" in node
    }
    people.append(p)
    if "spouse" in node:
        sp = node["spouse"]
        people.append({
            "id": sp.get("id", "sp_" + str(node.get("id"))),
            "name": sp.get("name"),
            "gender": sp.get("gender"),
            "notes": sp.get("notes", ""),
            "is_spouse": True
        })
    for c in node.get("children", []):
        traverse(c)

traverse(data["root"])
for b in data["root"].get("children_branches", []):
    traverse(b["person"])

print(f"Total entries: {len(people)}")

unique_names = {}
for p in people:
    n = p["name"]
    g = p["gender"]
    if n not in unique_names:
        unique_names[n] = []
    unique_names[n].append(p)

for n, instances in sorted(unique_names.items()):
    genders = set(inst["gender"] for inst in instances)
    notes = [inst["notes"] for inst in instances if inst["notes"]]
    print(f"Name: '{n}' -> Genders: {genders} (count: {len(instances)}) | Notes: {notes}")

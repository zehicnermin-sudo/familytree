# -*- coding: utf-8 -*-
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

people = []

def traverse(node):
    people.append({
        "name": node.get("name"),
        "gender": node.get("gender"),
        "notes": node.get("notes", ""),
        "has_spouse": "spouse" in node
    })
    if "spouse" in node:
        sp = node["spouse"]
        people.append({
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

unique_names = {}
for p in people:
    n = p["name"]
    if n not in unique_names:
        unique_names[n] = []
    unique_names[n].append(p)

for n, instances in sorted(unique_names.items())[:60]:
    genders = set(inst["gender"] for inst in instances)
    notes = [inst["notes"] for inst in instances if inst["notes"]]
    print(f"{n} | {list(genders)} | count: {len(instances)} | notes: {notes}")

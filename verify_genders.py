# -*- coding: utf-8 -*-
"""
Verification report of all female and male names in the tree
"""
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

females = set()
males = set()

def collect(node):
    g = node.get("gender")
    n = node.get("name")
    if g == "F":
        females.add(n)
    else:
        males.add(n)
    if "spouse" in node:
        sp = node["spouse"]
        sp_g = sp.get("gender")
        sp_n = sp.get("name")
        if sp_g == "F":
            females.add(sp_n)
        else:
            males.add(sp_n)
    for c in node.get("children", []):
        collect(c)

collect(data["root"])
for b in data["root"].get("children_branches", []):
    collect(b["person"])

print("--- ŽENSKA IMENA (ROZE BOJA) ---")
for fn in sorted(females):
    print(f"🌸 {fn}")

print("\n--- MUŠKA IMENA (PLAVA BOJA) ---")
for mn in sorted(males):
    print(f"🔵 {mn}")

# -*- coding: utf-8 -*-
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

counts = {}
total = 0

def count_persons(node, branch_name):
    global total
    c = 1
    if "spouse" in node:
        c += 1
    for ch in node.get("children", []):
        c += count_persons(ch, branch_name)
    return c

root = data["root"]
for b in root.get("children_branches", []):
    b_name = b["branch_name"]
    p = b["person"]
    bc = count_persons(p, b_name)
    counts[b_name] = bc
    total += bc

print("Tacan zbir po granama:")
for k, v in counts.items():
    print(f"  {k}: {v}")
print(f"  Ibrahim (Korijen): 1")
print(f"Ukupno clanova na posteru: {total + 1}")

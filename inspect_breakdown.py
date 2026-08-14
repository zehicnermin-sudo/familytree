# -*- coding: utf-8 -*-
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for b in data["root"]["children_branches"]:
    b_name = b["branch_name"]
    blood_count = 0
    spouse_count = 0

    def traverse(node):
        global blood_count, spouse_count
        blood_count += 1
        if "spouse" in node:
            spouse_count += 1
        for ch in node.get("children", []):
            traverse(ch)

    traverse(b["person"])
    print(f"{b_name}: {blood_count} krvnih srodnika + {spouse_count} supruznika = {blood_count + spouse_count} ukupno")

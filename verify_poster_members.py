# -*- coding: utf-8 -*-
"""
Verify which members exist in:
1. Porodicno_Stablo_Zehic_A0.svg
2. Branche_Adem.svg
3. Branche_Osman.svg
4. Branche_Meho.svg
5. data/members.json
6. tree_coords.js
"""
import json
import re
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Check data/members.json
with open("data/members.json", "r", encoding="utf-8") as f:
    db_members = json.load(f)

print(f"data/members.json: {len(db_members)} members")

# 2. Check tree_coords.js
with open("tree_coords.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Extract main nodes
coords_json_str = re.search(r'window\.ZEHIC_TREE_COORDS\s*=\s*(\{.*?\});', js_content, re.DOTALL)
if coords_json_str:
    coords_data = json.loads(coords_json_str.group(1))
    print(f"tree_coords.js main nodes: {len(coords_data.get('main', {}).get('nodes', []))}")
    print(f"tree_coords.js adem nodes: {len(coords_data.get('adem', {}).get('nodes', []))}")
    print(f"tree_coords.js osman nodes: {len(coords_data.get('osman', {}).get('nodes', []))}")
    print(f"tree_coords.js meho nodes: {len(coords_data.get('meho', {}).get('nodes', []))}")

# 3. Check text elements in Porodicno_Stablo_Zehic_A0.svg
with open("Porodicno_Stablo_Zehic_A0.svg", "r", encoding="utf-8") as f:
    svg_a0 = f.read()

a0_texts = re.findall(r'<text\s+[^>]*>(.*?)</text>', svg_a0, re.DOTALL)
print(f"Porodicno_Stablo_Zehic_A0.svg: {len(a0_texts)} text tags")

# 4. Check if any member from db is missing in tree_coords or A0 SVG
missing_in_a0 = []
for m in db_members:
    name = m["ime"].strip()
    if name not in svg_a0:
        missing_in_a0.append(m)

print(f"Missing members in Porodicno_Stablo_Zehic_A0.svg: {len(missing_in_a0)}")
for m in missing_in_a0[:20]:
    print(f"  - {m['ime']} (Grana: {m['grana']}, Roditelj: {m['ime_roditelja']})")


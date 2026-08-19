# -*- coding: utf-8 -*-
"""
Check if there are any specific differences between the user's uploaded SVG and our JSON/SVG:
- Names spelled differently?
- Spouses added or changed?
- Children added?
- Notes/locations/dates changed?
"""
import json
import re
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read user's SVG
with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    user_svg = f.read()

# Load DB members
with open("data/members.json", "r", encoding="utf-8") as f:
    db_members = json.load(f)

# Extract all names and notes from user_svg
# Look for <text ...><tspan ...>Name</tspan></text>
# and <text ...>Extra</text>
text_re = re.compile(r'<text\s+x="([^"]+)"\s+y="([^"]+)"[^>]*>(.*?)</text>', re.DOTALL)
user_entries = []

for m in text_re.finditer(user_svg):
    x = float(m.group(1))
    y = float(m.group(2))
    raw = m.group(3)
    tspans = re.findall(r'<tspan[^>]*>(.*?)</tspan>', raw)
    if tspans:
        txt = " ".join([t.strip() for t in tspans if t.strip()])
    else:
        txt = re.sub(r'<[^>]+>', '', raw).strip()
    if txt and not txt.startswith("Njihov") and not txt.startswith("Njegov") and txt not in ["Supruga", "Suprug", "djeca", "dijete"]:
        user_entries.append({"x": x, "y": y, "text": txt})

print(f"Total raw text entries in user's SVG: {len(user_entries)}")
for i, e in enumerate(user_entries):
    print(f"{i+1:3d}. (y={e['y']:6.1f}, x={e['x']:8.1f}) -> '{e['text']}'")

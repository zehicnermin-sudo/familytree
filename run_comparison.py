# -*- coding: utf-8 -*-
"""
Parse and compare the user's provided SVG against the current 416 members database.
"""
import json
import sqlite3
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Load current database members (416 members)
with open("data/members.json", "r", encoding="utf-8") as f:
    db_members = json.load(f)

print(f"Loaded {len(db_members)} members from current database (data/members.json).")

# 2. Extract and parse cards from user's provided SVG
# Let's read new_provided_tree.svg
with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    svg_content = f.read()

# Let's inspect all <text> elements in the SVG
# Every card has <rect> and <text>
text_blocks = re.findall(r'<text\s+[^>]*>(.*?)</text>', svg_content, re.DOTALL)
clean_texts = []
for tb in text_blocks:
    # clean tspans
    t = re.sub(r'<tspan[^>]*>(.*?)</tspan>', r'\1', tb)
    t = re.sub(r'<[^>]+>', '', t).strip()
    if t and not t.startswith("Njihov") and not t.startswith("Njegov") and t not in ["Supruga", "Suprug", "djeca", "dijete"]:
        clean_texts.append(t)

print(f"Found {len(clean_texts)} total meaningful text labels in user SVG.")

# Let's extract person boxes from user SVG using coordinates and lines
# Match each <rect> and its associated text
rect_re = re.compile(r'<rect\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"[^>]*/>')
text_re = re.compile(r'<text\s+x="([^"]+)"\s+y="([^"]+)"[^>]*>(.*?)</text>', re.DOTALL)

rects = []
for m in rect_re.finditer(svg_content):
    x = float(m.group(1))
    y = float(m.group(2))
    w = float(m.group(3))
    h = float(m.group(4))
    if w > 11000: continue
    rects.append({"x": x, "y": y, "w": w, "h": h, "texts": []})

for m in text_re.finditer(svg_content):
    x = float(m.group(1))
    y = float(m.group(2))
    raw = m.group(3)
    tspans = re.findall(r'<tspan[^>]*>(.*?)</tspan>', raw)
    txt = " ".join([t.strip() for t in tspans if t.strip()]) if tspans else re.sub(r'<[^>]+>', '', raw).strip()
    
    # assign to nearest rect
    for r in rects:
        if r["x"] - 30 <= x <= r["x"] + r["w"] + 30 and r["y"] - 35 <= y <= r["y"] + r["h"] + 35:
            r["texts"].append(txt)
            break

svg_people = []
for r in rects:
    if not r["texts"]: continue
    full_str = " ".join(r["texts"])
    if "djeca" in full_str or "dijete" in full_str or "Njegov" in full_str or "Njihov" in full_str: continue
    
    name = r["texts"][0].strip()
    notes = " ".join(r["texts"][1:]).strip() if len(r["texts"]) > 1 else ""
    svg_people.append({
        "name": name,
        "notes": notes,
        "x": r["x"],
        "y": r["y"]
    })

print(f"Extracted {len(svg_people)} person boxes from SVG.")

# 3. Compare with DB members
db_lookup = {}
for m in db_members:
    key = m["ime"].lower().strip()
    if key not in db_lookup:
        db_lookup[key] = []
    db_lookup[key].append(m)

svg_names = set([p["name"].lower().strip() for p in svg_people])

print("\n" + "="*70)
print("POREĐENJE SA TRENUTNIM STABLOM")
print("="*70)

# Check who in SVG is new or modified
new_in_svg = []
for p in svg_people:
    name_key = p["name"].lower().strip()
    if name_key not in db_lookup:
        new_in_svg.append(p)

print(f"\n1. Članovi iz novog SVG-a koji NISU u trenutnoj bazi: {len(new_in_svg)}")
for n in new_in_svg:
    print(f"   • Ime: {n['name']} | Napomene: {n['notes']} (y={n['y']}, x={n['x']})")


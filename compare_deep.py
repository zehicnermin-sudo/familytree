# -*- coding: utf-8 -*-
"""
Deep Comparator:
Analyzes the entire newly provided SVG tree against family_tree_gender_tagged.json.
Produces a detailed categorized report in Bosnian.
"""
import re
import json
import io
import sys

# Ensure UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Parse new_provided_tree.svg
with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    svg = f.read()

rect_pattern = re.compile(r'<rect\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"[^>]*fill="([^"]+)"[^>]*/>')
rects = []
for m in rect_pattern.finditer(svg):
    x = float(m.group(1))
    y = float(m.group(2))
    w = float(m.group(3))
    h = float(m.group(4))
    fill = m.group(5)
    if w > 11000:
        continue
    rects.append({
        "x": x, "y": y, "w": w, "h": h, "fill": fill,
        "cx": x + w/2, "cy": y + h/2,
        "texts": []
    })

text_pattern = re.compile(r'<text\s+x="([^"]+)"\s+y="([^"]+)"[^>]*>(.*?)</text>', re.DOTALL)
texts = []
for m in text_pattern.finditer(svg):
    x = float(m.group(1))
    y = float(m.group(2))
    raw_content = m.group(3)
    tspans = re.findall(r'<tspan[^>]*>(.*?)</tspan>', raw_content)
    if tspans:
        content = " ".join([t.strip() for t in tspans if t.strip()])
    else:
        content = re.sub(r'<[^>]+>', '', raw_content).strip()
    texts.append({"x": x, "y": y, "text": content})

for t in texts:
    tx = t["x"]
    ty = t["y"]
    text_val = t["text"]
    best_rect = None
    for r in rects:
        if r["x"] - 25 <= tx <= r["x"] + r["w"] + 25 and r["y"] - 35 <= ty <= r["y"] + r["h"] + 35:
            best_rect = r
            break
    if best_rect:
        best_rect["texts"].append(text_val)

new_cards = []
for r in rects:
    txt_list = r["texts"]
    if not txt_list:
        continue
    joined = " ".join(txt_list)
    if "djeca" in joined or "dijete" in joined or "Njegov" in joined or "Njihov" in joined:
        continue
    new_cards.append({
        "x": r["x"], "y": r["y"], "w": r["w"], "h": r["h"],
        "texts": txt_list,
        "primary_name": txt_list[0] if txt_list else "",
        "notes": " ".join(txt_list[1:]) if len(txt_list) > 1 else ""
    })

print(f"Total cards extracted from new SVG: {len(new_cards)}")

# 2. Parse current master dataset (family_tree_gender_tagged.json)
with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    master_json = json.load(f)

current_members_dict = {}
current_spouses_dict = {}

def index_master(node, branch="Korijen", parent=""):
    name = node.get("name", "").strip()
    notes = node.get("notes", "").strip()
    dates = node.get("dates", "").strip()
    gen = node.get("generation", 1)
    sp = node.get("spouse", {})
    sp_name = sp.get("name", "").strip() if sp else ""
    sp_notes = sp.get("notes", "").strip() if sp else ""
    
    current_members_dict[name.lower()] = {
        "name": name,
        "branch": branch,
        "parent": parent,
        "notes": notes,
        "dates": dates,
        "gen": gen,
        "spouse": sp_name,
        "spouse_notes": sp_notes,
        "children": [c.get("name") for c in node.get("children", [])]
    }
    
    if sp_name:
        current_spouses_dict[sp_name.lower()] = {
            "name": sp_name,
            "spouse_of": name,
            "branch": branch,
            "notes": sp_notes
        }
        
    for c in node.get("children", []):
        index_master(c, branch if branch != "Korijen" else c.get("name", ""), name)

index_master(master_json, "Korijen", "")

print(f"Total indexed master members: {len(current_members_dict)}, spouses: {len(current_spouses_dict)}")

# 3. Analyze differences
print("\n" + "="*70)
print("ANALIZA ČLANOVA IZ NOVOG SVG-A U ODNOSU NA TRENUTNU BAZU")
print("="*70)

new_svg_names = []
for c in new_cards:
    p_name = c["primary_name"].strip()
    if p_name:
        new_svg_names.append((p_name, c["notes"], c["y"], c["x"]))

# Check each new card against current database
found_in_db = []
not_in_db = []

for name, notes, y, x in new_svg_names:
    clean_n = name.lower()
    if clean_n in current_members_dict:
        found_in_db.append((name, notes, current_members_dict[clean_n]))
    elif clean_n in current_spouses_dict:
        found_in_db.append((name, notes, current_spouses_dict[clean_n]))
    else:
        not_in_db.append((name, notes, y, x))

print(f"\n✅ Pronađeno u trenutnoj bazi: {len(found_in_db)}")
print(f"❓ NIJE pronađeno ili ima novo/drugačije ime: {len(not_in_db)}")

if not_in_db:
    print("\n--- STAVKE KOJE NISU DIREKTNO U BAZI ILI IMAJU NOVO IME ---")
    for name, notes, y, x in not_in_db:
        print(f"  • Ime: '{name}' | Napomene: '{notes}' (y={y}, x={x})")

# Check which master members are NOT in the new SVG
new_names_set = set([n[0].lower() for n in new_svg_names])
missing_from_new_svg = []
for name_lower, data in current_members_dict.items():
    if name_lower not in new_names_set and not any(name_lower in n for n in new_names_set):
        missing_from_new_svg.append(data)

print(f"\n📊 Ukupno članova u trenutnoj bazi koji nisu u novom SVG-u (jer je novi SVG možda samo dio stabla): {len(missing_from_new_svg)}")

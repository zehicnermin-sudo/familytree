# -*- coding: utf-8 -*-
"""
Precise hierarchy comparator between new_provided_tree.svg and family_tree_gender_tagged.json.
"""
import re
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. Load current master dataset
with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    master_json = json.load(f)

db_members = []
def flatten_db(node, branch_name="", parent_name=""):
    name = node.get("name", "").strip()
    dates = node.get("dates", "").strip()
    notes = node.get("notes", "").strip()
    gen = node.get("generation", 1)
    gender = node.get("gender", "M")
    sp = node.get("spouse", {})
    sp_name = sp.get("name", "").strip() if sp else ""
    sp_notes = sp.get("notes", "").strip() if sp else ""
    
    current_branch = branch_name or node.get("branch", "")
    
    db_members.append({
        "name": name,
        "branch": current_branch,
        "parent": parent_name,
        "dates": dates,
        "notes": notes,
        "gen": gen,
        "gender": gender,
        "spouse": sp_name,
        "spouse_notes": sp_notes,
        "children": [c.get("name") for c in node.get("children", [])]
    })
    
    for c in node.get("children", []):
        flatten_db(c, current_branch if current_branch != "Korijen" else c.get("name", ""), name)

flatten_db(master_json, "Korijen", "")

print(f"Total database members (including root): {len(db_members)}")

# 2. Parse new_provided_tree.svg
with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    svg = f.read()

# Let's inspect the entire SVG lines and rects
rect_pattern = re.compile(r'<rect\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"[^>]*fill="([^"]+)"[^>]*/>')
rects = []
for m in rect_pattern.finditer(svg):
    x = float(m.group(1))
    y = float(m.group(2))
    w = float(m.group(3))
    h = float(m.group(4))
    fill = m.group(5)
    if w > 11000: continue
    rects.append({"x": x, "y": y, "w": w, "h": h, "cx": x + w/2, "cy": y + h/2, "texts": []})

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
    for r in rects:
        if r["x"] - 25 <= tx <= r["x"] + r["w"] + 25 and r["y"] - 35 <= ty <= r["y"] + r["h"] + 35:
            r["texts"].append(text_val)
            break

cards = []
for r in rects:
    txt_list = r["texts"]
    if not txt_list: continue
    joined = " ".join(txt_list)
    if "djeca" in joined or "dijete" in joined or "Njegov" in joined or "Njihov" in joined: continue
    cards.append({
        "x": r["x"], "y": r["y"], "w": r["w"], "h": r["h"], "cx": r["cx"], "cy": r["cy"],
        "name": txt_list[0].strip(),
        "extra": " | ".join(txt_list[1:]) if len(txt_list) > 1 else ""
    })

print(f"Total cards found in new SVG: {len(cards)}")

# Group cards by Y level (Generation)
y_levels = sorted(list(set([round(c["y"], 0) for c in cards])))
print(f"Y levels (Generations): {y_levels}")

# Let's print out all cards with their Y level
for yl in y_levels:
    c_at_y = [c for c in cards if round(c["y"], 0) == yl]
    print(f"\n--- Y Level = {yl} ({len(c_at_y)} cards) ---")
    for c in c_at_y:
        print(f"  • {c['name']} (Extra: {c['extra']}) [x={c['x']}]")

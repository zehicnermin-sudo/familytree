# -*- coding: utf-8 -*-
"""
Deep Forensic Diff between:
1. User's latest provided SVG (new_provided_tree.svg)
2. Current database (family_tree_gender_tagged.json & data/members.json)
"""
import re
import json
import sqlite3
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read user's provided SVG
with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    svg_text = f.read()

print(f"SVG length: {len(svg_text)} characters, {len(svg_text.splitlines())} lines.")

# Load database
with open("data/members.json", "r", encoding="utf-8") as f:
    db_members = json.load(f)

db_names = set()
for m in db_members:
    db_names.add(m["ime"].strip())
    if m.get("supruznik_ime"):
        db_names.add(m["supruznik_ime"].strip())

print(f"Database contains {len(db_members)} members with {len(db_names)} unique person names.")

# Extract all names from user's provided SVG
text_matches = re.findall(r'<text\s+[^>]*>(.*?)</text>', svg_text, re.DOTALL)
svg_names = []
for t in text_matches:
    # clean tspans
    t_clean = re.sub(r'<tspan[^>]*>(.*?)</tspan>', r'\1', t)
    t_clean = re.sub(r'<[^>]+>', '', t_clean).strip()
    # ignore non-names
    if not t_clean: continue
    if t_clean in ["Supruga", "Suprug", "djeca", "dijete", "Njegova djeca", "Njihova djeca", "Njegovo dijete", "Njihovo dijete", "Njegova", "Njihova"]: continue
    if re.match(r'^\d{4}\s*–\s*\d{4}$', t_clean): continue
    if re.match(r'^r\.\s*\d{4}$', t_clean): continue
    if t_clean.startswith("r. ") or t_clean.startswith("u. ") or t_clean.startswith("n. "): continue
    svg_names.append(t_clean)

print(f"Extracted {len(svg_names)} candidate names from SVG.")

missing_in_db = []
for sn in svg_names:
    if sn not in db_names and not any(sn.lower() == dn.lower() for dn in db_names):
        missing_in_db.append(sn)

print(f"\nNames in SVG but NOT in database: {len(missing_in_db)}")
for m in missing_in_db:
    print(f"  • {m}")


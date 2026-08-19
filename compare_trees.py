# -*- coding: utf-8 -*-
"""
Deep comparison script:
1. Parses all members, spouses, notes, and lineage from new_provided_tree.svg.
2. Compares against current master database family_tree_gender_tagged.json.
3. Identifies every addition, change, spelling difference, or structural modification.
"""
import re
import json

# 1. Parse new_provided_tree.svg
with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    new_svg = f.read()

# Extract all <rect> and <text> elements
new_texts = re.findall(r'<text[^>]*>(.*?)</text>', new_svg, re.DOTALL)
clean_new_names = []
for t in new_texts:
    # clean tspans and html
    cleaned = re.sub(r'<tspan[^>]*>', ' ', t)
    cleaned = re.sub(r'</tspan>', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    if cleaned and not cleaned.startswith("Njihov") and not cleaned.startswith("Njegov") and not cleaned.startswith("djeca") and not cleaned.startswith("dijete") and cleaned != "Supruga" and cleaned != "Suprug":
        clean_new_names.append(cleaned)

print(f"Extracted {len(clean_new_names)} total text items from new SVG.")

# 2. Parse current master dataset
with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    master_data = json.load(f)

current_members = []
current_spouses = []

def extract_current(node, branch_name="", parent_name=""):
    name = node.get("name", "").strip()
    notes = node.get("notes", "").strip()
    dates = node.get("dates", "").strip()
    spouse = node.get("spouse", {})
    sp_name = spouse.get("name", "").strip() if spouse else ""
    sp_notes = spouse.get("notes", "").strip() if spouse else ""
    
    current_members.append({
        "name": name,
        "branch": branch_name or node.get("branch", ""),
        "parent": parent_name,
        "notes": notes,
        "dates": dates,
        "spouse": sp_name,
        "spouse_notes": sp_notes
    })
    
    if sp_name:
        current_spouses.append({
            "name": sp_name,
            "spouse_of": name,
            "branch": branch_name or node.get("branch", ""),
            "notes": sp_notes
        })
        
    for child in node.get("children", []):
        extract_current(child, branch_name or node.get("name", ""), name)

extract_current(master_data, "Korijen", "")

print(f"Master dataset has {len(current_members)} members and {len(current_spouses)} spouses.")

# Write analysis script to parse structure of new_provided_tree.svg

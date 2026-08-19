# -*- coding: utf-8 -*-
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

CARD_W = 204
CARD_H = 34
CARD_H_COUPLE = 58
V_GAP = 5
COL_W = 224
GAP_FROM_ROOT = 60

def compute_subtree_height(node):
    has_sp = "spouse" in node
    self_h = CARD_H_COUPLE if has_sp else CARD_H
    children = node.get("children", [])
    if not children:
        node["_span_h"] = self_h
        return self_h
    ch_heights = [compute_subtree_height(c) for c in children]
    total_ch_h = sum(ch_heights) + (len(children) - 1) * V_GAP
    node["_span_h"] = max(self_h, total_ch_h)
    return node["_span_h"]

root_node = raw_data["root"]
adem_node = next(b["person"] for b in root_node["children_branches"] if b["branch_name"] == "Grana Adem")
right_branches = [b["person"] for b in root_node["children_branches"] if b["branch_name"] != "Grana Adem"]

adem_h = compute_subtree_height(adem_node)
right_hs = [compute_subtree_height(b) for b in right_branches]
total_right_h = sum(right_hs) + (len(right_branches) - 1) * 30

max_h = max(adem_h, total_right_h)

print(f"Compact Adem Height: {adem_h} px")
print(f"Compact Right Wing Height: {total_right_h} px")
print(f"Max Tree Height: {max_h} px")

# Number of generations left (Adem = 7 cols -> ~7 * 224 = 1568 px)
# Number of generations right (Osman = 7 cols -> ~7 * 224 = 1568 px)
# Center Root: ~230 + 120 = 350 px
# Total Width: ~1568 + 1568 + 350 = 3486 px
total_w = 7 * COL_W * 2 + 350
print(f"Estimated Total Width: {total_w} px")
print(f"Aspect Ratio (Width : Height): {total_w / (max_h + 200):.2f} : 1")
print(f"ISO A3 Aspect Ratio: 1.414 : 1 (Landscape) or 0.707 : 1 (Portrait)")

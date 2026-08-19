# -*- coding: utf-8 -*-
import re

with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    svg = f.read()

rect_matches = re.findall(r'<rect\s+x="([^"]+)"\s+y="([^"]+)"\s+width="([^"]+)"\s+height="([^"]+)"', svg)
all_rect_ys = [float(r[1]) for r in rect_matches if float(r[2]) < 11000]

print("Distinct Y values for all rects:", sorted(list(set(all_rect_ys))))
print(f"Total rects found: {len(all_rect_ys)}")

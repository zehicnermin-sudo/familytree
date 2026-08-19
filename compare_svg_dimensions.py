# -*- coding: utf-8 -*-
import re

with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    new_svg = f.read()

with open("Porodicno_Stablo_Zehic_A0.svg", "r", encoding="utf-8") as f:
    current_svg = f.read()

new_vb = re.search(r'viewBox="([^"]+)"', new_svg).group(1) if re.search(r'viewBox="([^"]+)"', new_svg) else ""
new_w = re.search(r'width="([^"]+)"', new_svg).group(1) if re.search(r'width="([^"]+)"', new_svg) else ""
new_h = re.search(r'height="([^"]+)"', new_svg).group(1) if re.search(r'height="([^"]+)"', new_svg) else ""

curr_vb = re.search(r'viewBox="([^"]+)"', current_svg).group(1) if re.search(r'viewBox="([^"]+)"', current_svg) else ""
curr_w = re.search(r'width="([^"]+)"', current_svg).group(1) if re.search(r'width="([^"]+)"', current_svg) else ""
curr_h = re.search(r'height="([^"]+)"', current_svg).group(1) if re.search(r'height="([^"]+)"', current_svg) else ""

print(f"New provided SVG:")
print(f"  viewBox: {new_vb}, width: {new_w}, height: {new_h}")
print(f"  Length: {len(new_svg)} chars, {len(new_svg.splitlines())} lines")

print(f"\nCurrent Porodicno_Stablo_Zehic_A0.svg:")
print(f"  viewBox: {curr_vb}, width: {curr_w}, height: {curr_h}")
print(f"  Length: {len(current_svg)} chars, {len(current_svg.splitlines())} lines")

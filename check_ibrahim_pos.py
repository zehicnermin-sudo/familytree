# -*- coding: utf-8 -*-
import re

with open("Porodicno_Stablo_Zehic_A0.svg", "r", encoding="utf-8") as f:
    svg = f.read()

vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
print("ViewBox:", vb)

# Find Ibrahim
ib = re.search(r'<g transform="translate\(([^,]+),\s*([^)]+)\)">[^<]*<rect[^>]*>[^<]*<rect[^>]*>[^<]*<circle[^>]*>[^<]*<text[^>]*>👑[^<]*</text>[^<]*<text[^>]*>Ibrahim', svg)
if ib:
    print("Found Ibrahim at:", ib.group(1), ib.group(2))
else:
    # generic search
    for m in re.finditer(r'<g transform="translate\(([^,]+),\s*([^)]+)\)">', svg):
        pos = m.start()
        chunk = svg[pos:pos+400]
        if "Ibrahim" in chunk and ("Osnivač" in chunk or "👑" in chunk):
            print("Found Ibrahim match at:", m.group(1), m.group(2))

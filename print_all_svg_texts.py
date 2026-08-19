# -*- coding: utf-8 -*-
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("new_provided_tree.svg", "r", encoding="utf-8") as f:
    svg = f.read()

lines = svg.splitlines()

texts = []
for line in lines:
    m = re.search(r'<text[^>]*>(.*?)</text>', line)
    if m:
        val = m.group(1)
        val = re.sub(r'<[^>]+>', ' ', val)
        val = re.sub(r'\s+', ' ', val).strip()
        texts.append(val)

print(f"Total text tags: {len(texts)}")
for i, t in enumerate(texts):
    print(f"{i+1:3d}: {t}")

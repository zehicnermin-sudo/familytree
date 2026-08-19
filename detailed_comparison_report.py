# -*- coding: utf-8 -*-
"""
Generate a comprehensive, detailed comparison report comparing the new tree version
against the previous master database.
"""
import json
import sqlite3
import re
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("data/members.json", "r", encoding="utf-8") as f:
    db_members = json.load(f)

# Group DB members by branch
db_by_branch = {}
for m in db_members:
    b = m.get("grana", "Ostalo")
    if b not in db_by_branch:
        db_by_branch[b] = []
    db_by_branch[b].append(m)

print("TRENUTNO STANJE U BAZI:")
for b, mems in db_by_branch.items():
    print(f"  • {b}: {len(mems)} članova")

total_db = len(db_members)
print(f"Ukupno u bazi: {total_db} članova (uključujući supružnike i korijen).")


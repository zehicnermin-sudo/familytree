# -*- coding: utf-8 -*-
"""
Export SQLite database to data/members.json and public/members.json for Vercel Serverless & Static Deployment
(NEVER write to api/members.json to avoid Vercel route collision with api/members.js)
"""
import os
import json
import sqlite3

os.makedirs("data", exist_ok=True)
os.makedirs("public", exist_ok=True)

# Remove api/members.json if exists
if os.path.exists("api/members.json"):
    os.remove("api/members.json")

conn = sqlite3.connect("porodicno_stablo_zehic.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT * FROM clanovi ORDER BY generacija ASC, grana ASC, ime ASC")
rows = [dict(row) for row in cur.fetchall()]

with open("data/members.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

with open("public/members.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

conn.close()
print(f"Exported {len(rows)} members to data/members.json and public/members.json!")

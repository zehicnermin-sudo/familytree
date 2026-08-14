# -*- coding: utf-8 -*-
"""
Create SQLite Database and SQL Dump for Zehic Family Tree:
- Populates all 401+ members with lineage, branch, generation, gender, notes, spouse, parent relations.
"""
import sys
import io
import json
import sqlite3

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Connect to SQLite
db_path = "porodicno_stablo_zehic.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Drop table if exists
cur.execute("DROP TABLE IF EXISTS clanovi")

# Create clean relational table
cur.execute("""
CREATE TABLE clanovi (
    id TEXT PRIMARY KEY,
    ime TEXT NOT NULL,
    prezime TEXT DEFAULT 'Zehić',
    spol TEXT NOT NULL, -- 'M' ili 'Ž'
    generacija INTEGER NOT NULL,
    grana TEXT NOT NULL,
    datumi TEXT,
    napomene TEXT,
    roditelj_id TEXT,
    ime_roditelja TEXT,
    supruznik_ime TEXT,
    supruznik_napomene TEXT,
    je_supruznik INTEGER DEFAULT 0
)
""")

# Indexes for fast search
cur.execute("CREATE INDEX idx_ime ON clanovi(ime)")
cur.execute("CREATE INDEX idx_grana ON clanovi(grana)")
cur.execute("CREATE INDEX idx_generacija ON clanovi(generacija)")
cur.execute("CREATE INDEX idx_spol ON clanovi(spol)")

members = []

def extract_members(node, branch_name="Glavno Stablo", parent_id=None, parent_name=None):
    n_id = str(node.get("id", f"node_{len(members)+1}"))
    name = node.get("name", "").strip()
    gender = "M" if node.get("gender") == "M" else "Ž"
    gen = node.get("gen", 1)
    dates = node.get("dates", "")
    notes = node.get("notes", "")

    sp_name = ""
    sp_notes = ""
    has_sp = "spouse" in node

    if has_sp:
        sp = node["spouse"]
        sp_name = sp.get("name", "").strip()
        sp_notes = sp.get("notes", "")
        sp_gender = "Ž" if sp.get("gender") == "F" else "M"
        sp_dates = sp.get("dates", "")
        sp_id = f"sp_{n_id}"

        # Add spouse row
        members.append((
            sp_id, sp_name, "", sp_gender, gen, branch_name, sp_dates, sp_notes,
            n_id, name, name, notes, 1
        ))

    # Add primary person row
    members.append((
        n_id, name, "Zehić" if not has_sp or gender == "M" else "Zehić",
        gender, gen, branch_name, dates, notes,
        parent_id, parent_name, sp_name, sp_notes, 0
    ))

    # Recurse children
    for c in node.get("children", []):
        extract_members(c, branch_name, n_id, name)

# Process root
root = data["root"]
extract_members(root, "Korijen", None, None)

for b in root.get("children_branches", []):
    b_name = b["branch_name"]
    extract_members(b["person"], b_name, "ibrahim_root", "Ibrahim")

# Insert into database
cur.executemany("""
INSERT OR REPLACE INTO clanovi (
    id, ime, prezime, spol, generacija, grana, datumi, napomene,
    roditelj_id, ime_roditelja, supruznik_ime, supruznik_napomene, je_supruznik
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", members)

conn.commit()

# Export SQL Dump
with open("porodicno_stablo_zehic.sql", "w", encoding="utf-8") as f:
    for line in conn.iterdump():
        f.write(f"{line}\n")

cur.execute("SELECT COUNT(*) FROM clanovi")
total_count = cur.fetchone()[0]

cur.execute("SELECT grana, COUNT(*) FROM clanovi GROUP BY grana")
branch_counts = cur.fetchall()

cur.execute("SELECT spol, COUNT(*) FROM clanovi GROUP BY spol")
gender_counts = cur.fetchall()

conn.close()

print(f"Successfully created SQLite database: {db_path}")
print(f"Successfully created SQL dump: porodicno_stablo_zehic.sql")
print(f"Total records in database: {total_count}")
print("Grane:", branch_counts)
print("Spol:", gender_counts)

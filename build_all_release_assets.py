# -*- coding: utf-8 -*-
"""
Master Release Builder for Porodično Stablo Zehić:
1. Compiles SQL Database (porodicno_stablo_zehic.db & members.json)
2. Compiles fast in-memory client datasets (members_data.js & tree_coords.js)
3. Renders all SVGs (A0 Bilateral Poster + Horizontal Branches)
4. Converts all SVGs to high-resolution A3 PDFs & Full Poster PDFs
5. Syncs all release assets to public/ directory for direct downloads
"""
import subprocess
import os
import shutil
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*70)
print("POKRETANJE KOMPLETNOG BUILD PROCESA ZA WEB, SVGs, PDFs I BAZU ZA PRETRAGU")
print("="*70)

# Step 1: Database
print("\n[1/6] Izgradnja SQLite baze i JSON kataloga...")
subprocess.run(["python", "build_sql_database.py"], check=True)

# Step 2: Search memory dataset & coords
print("\n[2/6] Generisanje JS memorijskih setova za pretragu (members_data.js)...")
subprocess.run(["python", "generate_members_data_js.py"], check=True)

print("\n[3/6] Generisanje koordinata za instantno pozicioniranje (tree_coords.js)...")
subprocess.run(["python", "generate_tree_coords_js.py"], check=True)

# Step 3: Master Vector SVG Posters
print("\n[4/6] Renderovanje bilateralnog master postera i grana (SVG)...")
subprocess.run(["python", "generate_master_bosnian_poster.py"], check=True)
subprocess.run(["python", "generate_horizontal_branches.py"], check=True)

# Step 4: A3 PDFs
print("\n[5/6] Generisanje A3 PDF formata za preuzimanje...")
subprocess.run(["python", "generate_a3_posters.py"], check=True)

# Step 5: Poster PDFs
print("\n[6/6] Generisanje Poster PDF formata (A0/A1 1-list) za preuzimanje...")
subprocess.run(["python", "generate_single_page_pdfs.py"], check=True)

# Step 6: Sync to public/
print("\n[FINISH] Sinhronizacija svih fajlova u public/ folder...")
subprocess.run(["python", "sync_public.py"], check=True)

print("\n" + "="*70)
print("SVI PDF, SVG I PRETRAŽIVAČKI PODACI SU USPJEŠNO KREIRANI I SINHRONIZOVANI!")
print("="*70)

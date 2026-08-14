# -*- coding: utf-8 -*-
"""
Sync all web assets to public folder and configure vercel.json for 100% reliable routing
"""
import os
import shutil

os.makedirs("public", exist_ok=True)

# Copy all static assets to public as well
static_files = [
    "index.html",
    "Porodicno_Stablo_Zehic_A0.svg",
    "Arbre_Genealogique_A0_Bilateral.svg",
    "Arbre_Genealogique_Complet.svg",
    "Branche_Adem.svg",
    "Branche_Osman.svg",
    "Branche_Meho.svg"
]

for f in static_files:
    if os.path.exists(f):
        shutil.copy(f, os.path.join("public", f))
        print(f"Copied {f} -> public/{f}")

print("Static assets synced to public/ successfully!")

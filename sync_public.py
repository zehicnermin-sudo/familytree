# -*- coding: utf-8 -*-
import shutil
import os

files_to_sync = [
    "index.html",
    "tree_coords.js",
    "members_data.js",
    "tree_coords.json",
    "Porodicno_Stablo_Zehic_A0.svg",
    "Branche_Adem.svg",
    "Branche_Osman.svg",
    "Branche_Meho.svg",
    "Porodicno_Stablo_Zehic_A3.pdf",
    "Grana_Adem_A3.pdf",
    "Grana_Osman_A3.pdf",
    "Grana_Meho_A3.pdf",
    "Porodicno_Stablo_Zehic_A0.pdf",
    "Grana_Adem.pdf",
    "Grana_Osman.pdf",
    "Grana_Meho.pdf"
]

os.makedirs("public", exist_ok=True)
os.makedirs("public/data", exist_ok=True)

for f in files_to_sync:
    if os.path.exists(f):
        shutil.copy(f, os.path.join("public", f))

if os.path.exists("data/members.json"):
    shutil.copy("data/members.json", "public/data/members.json")
    shutil.copy("data/members.json", "public/members.json")

if os.path.exists("data/tree_coords.json"):
    shutil.copy("data/tree_coords.json", "public/data/tree_coords.json")
    shutil.copy("data/tree_coords.json", "public/tree_coords.json")

print("All assets successfully synced to public/ directory!")

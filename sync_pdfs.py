# -*- coding: utf-8 -*-
import os
import shutil

os.makedirs("public", exist_ok=True)

files = [
    "index.html",
    "Porodicno_Stablo_Zehic_A0.svg",
    "Porodicno_Stablo_Zehic_A0.pdf",
    "Grana_Adem.pdf",
    "Grana_Osman.pdf",
    "Grana_Meho.pdf",
    "Branche_Adem.svg",
    "Branche_Osman.svg",
    "Branche_Meho.svg"
]

for f in files:
    if os.path.exists(f):
        shutil.copy(f, os.path.join("public", f))

print("Synced PDFs and web assets to public/!")

# -*- coding: utf-8 -*-
import os

files_to_remove = [
    "Porodicno_Stablo_Zehic_Gore_Dole.svg",
    "Porodicno_Stablo_Zehic_Gore_Dole.pdf",
    "public/Porodicno_Stablo_Zehic_Gore_Dole.svg",
    "public/Porodicno_Stablo_Zehic_Gore_Dole.pdf",
    "Porodicno_Stablo_Zehic_Vertikalno.svg",
    "Porodicno_Stablo_Zehic_Vertikalno.pdf",
    "public/Porodicno_Stablo_Zehic_Vertikalno.svg",
    "public/Porodicno_Stablo_Zehic_Vertikalno.pdf",
    "Porodicno_Stablo_Zehic_Horizontalno.svg",
    "Porodicno_Stablo_Zehic_Horizontalno.pdf",
    "public/Porodicno_Stablo_Zehic_Horizontalno.svg",
    "public/Porodicno_Stablo_Zehic_Horizontalno.pdf",
    "generate_all_layout_modes.py",
    "generate_up_down_horizontal_poster.py",
    "gen_up_down_pdf.py",
    "generate_layout_pdfs.py"
]

for f in files_to_remove:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed: {f}")

print("Cleaned up extra layout files successfully!")

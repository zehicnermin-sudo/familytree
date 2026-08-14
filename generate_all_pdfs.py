# -*- coding: utf-8 -*-
"""
Generate high-resolution vector PDF files for entire family tree and all branches
"""
import os
import subprocess

current_dir = os.path.abspath(os.getcwd())
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

files_to_convert = [
    ("Porodicno_Stablo_Zehic_A0.svg", "Porodicno_Stablo_Zehic_A0.pdf"),
    ("Branche_Adem.svg", "Grana_Adem.pdf"),
    ("Branche_Osman.svg", "Grana_Osman.pdf"),
    ("Branche_Meho.svg", "Grana_Meho.pdf")
]

os.makedirs("public", exist_ok=True)

for svg_name, pdf_name in files_to_convert:
    svg_abs = os.path.join(current_dir, svg_name)
    pdf_abs = os.path.join(current_dir, pdf_name)
    pdf_public = os.path.join(current_dir, "public", pdf_name)

    if os.path.exists(svg_abs):
        cmd = [
            edge_path,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_abs}",
            f"file:///{svg_abs.replace(os.sep, '/')}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(pdf_abs):
            import shutil
            shutil.copy(pdf_abs, pdf_public)
            size_kb = round(os.path.getsize(pdf_abs) / 1024, 1)
            print(f"Generated {pdf_name} ({size_kb} KB)")
        else:
            print(f"Failed to generate {pdf_name}: {res.stderr}")

print("PDF generation completed successfully!")

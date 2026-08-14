# -*- coding: utf-8 -*-
"""
Generate Precision ISO A3 Vector PDFs (420mm x 297mm Landscape) for Zehic Family Tree:
1. Porodicno_Stablo_Zehic_A3.svg / .pdf (Glavno Stablo A3)
2. Grana_Adem_A3.svg / .pdf
3. Grana_Osman_A3.svg / .pdf
4. Grana_Meho_A3.svg / .pdf
"""
import os
import re
import subprocess
import shutil

current_dir = os.path.abspath(os.getcwd())
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

files = [
    ("Porodicno_Stablo_Zehic_A0.svg", "Porodicno_Stablo_Zehic_A3.svg", "Porodicno_Stablo_Zehic_A3.pdf", "landscape"),
    ("Branche_Adem.svg", "Grana_Adem_A3.svg", "Grana_Adem_A3.pdf", "landscape"),
    ("Branche_Osman.svg", "Grana_Osman_A3.svg", "Grana_Osman_A3.pdf", "landscape"),
    ("Branche_Meho.svg", "Grana_Meho_A3.svg", "Grana_Meho_A3.pdf", "landscape")
]

os.makedirs("public", exist_ok=True)
os.makedirs("scratch", exist_ok=True)

for src_svg, a3_svg_name, a3_pdf_name, orientation in files:
    src_abs = os.path.join(current_dir, src_svg)
    if not os.path.exists(src_abs):
        continue

    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract viewBox
    vb_match = re.search(r'viewBox="([^"]+)"', content)
    if vb_match:
        parts = vb_match.group(1).split()
        vb_w = float(parts[2])
        vb_h = float(parts[3])
    else:
        vb_w = 5800.0
        vb_h = 7400.0

    # Determine optimal A3 orientation (landscape or portrait based on aspect ratio)
    if vb_h > vb_w * 1.2:
        page_size = "297mm 420mm" # A3 portrait
        a3_w_mm = 297
        a3_h_mm = 420
    else:
        page_size = "420mm 297mm" # A3 landscape
        a3_w_mm = 420
        a3_h_mm = 297

    # Adapt SVG root attributes for standard A3
    a3_svg_content = re.sub(
        r'<svg[^>]+>',
        f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{a3_w_mm}mm" height="{a3_h_mm}mm" viewBox="0 0 {vb_w} {vb_h}" xml:space="preserve" style="font-family: \'Plus Jakarta Sans\', \'Segoe UI\', Arial, Helvetica, sans-serif;">',
        content,
        count=1
    )

    a3_svg_abs = os.path.join(current_dir, a3_svg_name)
    with open(a3_svg_abs, "w", encoding="utf-8") as f:
        f.write(a3_svg_content)

    # HTML wrapper for exact ISO A3 print
    wrapper_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: {page_size};
    margin: 0;
}}
html, body {{
    margin: 0;
    padding: 0;
    width: {a3_w_mm}mm;
    height: {a3_h_mm}mm;
    background: #F8FAFC;
    overflow: hidden;
}}
svg {{
    width: {a3_w_mm}mm;
    height: {a3_h_mm}mm;
    display: block;
}}
</style>
</head>
<body>
{a3_svg_content}
</body>
</html>"""

    html_file = os.path.join(current_dir, "scratch", f"{a3_svg_name}.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(wrapper_html)

    pdf_abs = os.path.join(current_dir, a3_pdf_name)
    pdf_public = os.path.join(current_dir, "public", a3_pdf_name)

    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_abs}",
        f"file:///{html_file.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(pdf_abs):
        shutil.copy(pdf_abs, pdf_public)
        shutil.copy(a3_svg_abs, os.path.join(current_dir, "public", a3_svg_name))
        size_kb = round(os.path.getsize(pdf_abs) / 1024, 1)
        print(f"Generated ISO A3 PDF: {a3_pdf_name} ({size_kb} KB, Page: {page_size})")
    else:
        print(f"Failed {a3_pdf_name}")

print("A3 PDF Generation completed successfully!")

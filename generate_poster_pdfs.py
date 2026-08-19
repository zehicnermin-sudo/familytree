# -*- coding: utf-8 -*-
"""
Generate Precision ISO A0, A1, and A2 Vector PDFs for Zehic Family Tree:
- Glavno Stablo: A0 (841x1189mm), A1 (594x841mm), A2 (420x594mm)
- Grana Adem: A1, A2
- Grana Osman: A1, A2
- Grana Meho: A1, A2
"""
import os
import re
import subprocess
import shutil

current_dir = os.path.abspath(os.getcwd())
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

os.makedirs("public", exist_ok=True)
os.makedirs("scratch", exist_ok=True)

# List of targets: (src_svg, format_name, width_mm, height_mm, output_pdf_name)
targets = [
    # Glavno Stablo
    ("Porodicno_Stablo_Zehic_A0.svg", "A0", 841, 1189, "Porodicno_Stablo_Zehic_A0.pdf"),
    ("Porodicno_Stablo_Zehic_A0.svg", "A1", 594, 841,  "Porodicno_Stablo_Zehic_A1.pdf"),
    ("Porodicno_Stablo_Zehic_A0.svg", "A2", 420, 594,  "Porodicno_Stablo_Zehic_A2.pdf"),

    # Grana Adem
    ("Branche_Adem.svg", "A1", 594, 841, "Grana_Adem_A1.pdf"),
    ("Branche_Adem.svg", "A2", 420, 594, "Grana_Adem_A2.pdf"),
    ("Branche_Adem.svg", "A0", 841, 1189, "Grana_Adem.pdf"),

    # Grana Osman
    ("Branche_Osman.svg", "A1", 594, 841, "Grana_Osman_A1.pdf"),
    ("Branche_Osman.svg", "A2", 420, 594, "Grana_Osman_A2.pdf"),
    ("Branche_Osman.svg", "A0", 841, 1189, "Grana_Osman.pdf"),

    # Grana Meho
    ("Branche_Meho.svg", "A1", 594, 841, "Grana_Meho_A1.pdf"),
    ("Branche_Meho.svg", "A2", 420, 594, "Grana_Meho_A2.pdf"),
    ("Branche_Meho.svg", "A0", 841, 1189, "Grana_Meho.pdf"),
]

for src_svg, fmt, w_mm, h_mm, out_pdf in targets:
    src_abs = os.path.join(current_dir, src_svg)
    if not os.path.exists(src_abs):
        print(f"Skipping {src_svg} (not found)")
        continue

    with open(src_abs, "r", encoding="utf-8") as f:
        content = f.read()

    vb_match = re.search(r'viewBox="([^"]+)"', content)
    if vb_match:
        parts = vb_match.group(1).split()
        vb_w = float(parts[2])
        vb_h = float(parts[3])
    else:
        vb_w = 3414.0
        vb_h = 5457.0

    # Determine portrait vs landscape
    if vb_w > vb_h * 1.1:
        # Landscape
        actual_w = max(w_mm, h_mm)
        actual_h = min(w_mm, h_mm)
    else:
        # Portrait
        actual_w = min(w_mm, h_mm)
        actual_h = max(w_mm, h_mm)

    page_size = f"{actual_w}mm {actual_h}mm"

    # Adapt SVG root attributes for crisp vector print
    clean_svg = re.sub(
        r'<svg[^>]+>',
        f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%" viewBox="0 0 {vb_w} {vb_h}" xml:space="preserve" style="font-family: \'Plus Jakarta Sans\', \'Segoe UI\', Arial, sans-serif;">',
        content,
        count=1
    )

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
    width: {actual_w}mm;
    height: {actual_h}mm;
    background: #F8FAFC;
    overflow: hidden;
}}
svg {{
    width: {actual_w}mm;
    height: {actual_h}mm;
    display: block;
}}
</style>
</head>
<body>
{clean_svg}
</body>
</html>"""

    html_file = os.path.join(current_dir, "scratch", f"{out_pdf}.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(wrapper_html)

    pdf_abs = os.path.join(current_dir, out_pdf)
    pdf_public = os.path.join(current_dir, "public", out_pdf)

    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_abs}",
        f"file:///{html_file.replace(os.sep, '/')}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(pdf_abs):
        shutil.copy(pdf_abs, pdf_public)
        size_kb = round(os.path.getsize(pdf_abs) / 1024, 1)
        print(f"Generated ISO {fmt} PDF: {out_pdf} ({size_kb} KB, Page: {page_size})")
    else:
        print(f"Failed {out_pdf}: {res.stderr}")

print("All ISO A0, A1, and A2 poster PDFs generated successfully!")

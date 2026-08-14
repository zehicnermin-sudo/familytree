# -*- coding: utf-8 -*-
"""
Generate True 1-Page Seamless Poster PDFs matching exact SVG canvas dimensions
"""
import os
import re
import subprocess
import shutil

current_dir = os.path.abspath(os.getcwd())
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

files_to_convert = [
    ("Porodicno_Stablo_Zehic_A0.svg", "Porodicno_Stablo_Zehic_A0.pdf", "Glavni Poster"),
    ("Branche_Adem.svg", "Grana_Adem.pdf", "Grana Adem"),
    ("Branche_Osman.svg", "Grana_Osman.pdf", "Grana Osman"),
    ("Branche_Meho.svg", "Grana_Meho.pdf", "Grana Meho")
]

os.makedirs("public", exist_ok=True)
os.makedirs("scratch", exist_ok=True)

for svg_name, pdf_name, label in files_to_convert:
    svg_abs = os.path.join(current_dir, svg_name)
    if not os.path.exists(svg_abs):
        continue

    with open(svg_abs, "r", encoding="utf-8") as f:
        content = f.read()

    # Find viewBox or width/height
    vb_match = re.search(r'viewBox="([^"]+)"', content)
    if vb_match:
        parts = vb_match.group(1).split()
        w = float(parts[2])
        h = float(parts[3])
    else:
        w_match = re.search(r'width="([^"]+)"', content)
        h_match = re.search(r'height="([^"]+)"', content)
        w = float(w_match.group(1).replace("px", ""))
        h = float(h_match.group(1).replace("px", ""))

    # Create 1-page standalone HTML container with exact page sizing
    wrapper_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: {w}px {h}px;
    margin: 0;
}}
html, body {{
    margin: 0;
    padding: 0;
    width: {w}px;
    height: {h}px;
    background: #F8FAFC;
    overflow: hidden;
}}
svg {{
    width: {w}px;
    height: {h}px;
    display: block;
}}
</style>
</head>
<body>
{content}
</body>
</html>"""

    html_file = os.path.join(current_dir, "scratch", f"{svg_name}.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(wrapper_html)

    pdf_abs = os.path.join(current_dir, pdf_name)
    pdf_public = os.path.join(current_dir, "public", pdf_name)

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
        print(f"Generated Single-Page 1-Sheet PDF: {pdf_name} ({size_kb} KB, Dimensions: {int(w)}x{int(h)} px)")
    else:
        print(f"Failed {pdf_name}: {res.stderr}")

print("All single-page 1-sheet PDFs generated successfully!")

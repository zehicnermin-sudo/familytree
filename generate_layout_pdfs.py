# -*- coding: utf-8 -*-
"""
Generate Single-Page PDFs for all layouts:
1. Porodicno_Stablo_Zehic_A0.pdf (Bilateralni)
2. Porodicno_Stablo_Zehic_Vertikalno.pdf (Uspravni / Top-Down)
3. Porodicno_Stablo_Zehic_Horizontalno.pdf (Horizontalni / Left-Right)
4. Grana_Adem.pdf
5. Grana_Osman.pdf
6. Grana_Meho.pdf
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
    ("Porodicno_Stablo_Zehic_A0.svg", "Porodicno_Stablo_Zehic_A0.pdf"),
    ("Porodicno_Stablo_Zehic_Vertikalno.svg", "Porodicno_Stablo_Zehic_Vertikalno.pdf"),
    ("Porodicno_Stablo_Zehic_Horizontalno.svg", "Porodicno_Stablo_Zehic_Horizontalno.pdf"),
    ("Branche_Adem.svg", "Grana_Adem.pdf"),
    ("Branche_Osman.svg", "Grana_Osman.pdf"),
    ("Branche_Meho.svg", "Grana_Meho.pdf")
]

os.makedirs("public", exist_ok=True)
os.makedirs("scratch", exist_ok=True)

for svg_name, pdf_name in files:
    svg_abs = os.path.join(current_dir, svg_name)
    if not os.path.exists(svg_abs):
        continue

    with open(svg_abs, "r", encoding="utf-8") as f:
        content = f.read()

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
    subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(pdf_abs):
        shutil.copy(pdf_abs, pdf_public)
        size_kb = round(os.path.getsize(pdf_abs) / 1024, 1)
        print(f"Generated {pdf_name} ({size_kb} KB, {int(w)}x{int(h)} px)")

    # Also copy svg to public
    shutil.copy(svg_abs, os.path.join("public", svg_name))

print("All layouts & PDFs synced to public/ successfully!")

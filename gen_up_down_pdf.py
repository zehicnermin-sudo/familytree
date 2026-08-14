# -*- coding: utf-8 -*-
"""
Generate single-page PDF for Up/Down Tree
"""
import os
import re
import subprocess
import shutil

current_dir = os.path.abspath(os.getcwd())
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

svg_name = "Porodicno_Stablo_Zehic_Gore_Dole.svg"
pdf_name = "Porodicno_Stablo_Zehic_Gore_Dole.pdf"

svg_abs = os.path.join(current_dir, svg_name)
with open(svg_abs, "r", encoding="utf-8") as f:
    content = f.read()

vb_match = re.search(r'viewBox="([^"]+)"', content)
if vb_match:
    parts = vb_match.group(1).split()
    w = float(parts[2])
    h = float(parts[3])

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
    print(f"Generated {pdf_name} ({size_kb} KB, Dimensions: {int(w)}x{int(h)} px)")

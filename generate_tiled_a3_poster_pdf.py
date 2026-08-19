# -*- coding: utf-8 -*-
"""
Generate Tiled Multi-Page A3 Poster PDF (4x A3 Sheets):
Allows printing the entire master family poster on any standard A3 printer
and assembling it into a massive, crystal-clear 1.2m wall poster!
"""
import os
import re
import subprocess
import shutil

print("Generating Tiled 4x A3 Poster PDF...")

src_svg = "Porodicno_Stablo_Zehic_A0.svg"
if not os.path.exists(src_svg):
    print("Master SVG not found!")
    exit(1)

with open(src_svg, "r", encoding="utf-8") as f:
    content = f.read()

# Extract width and height
vb_match = re.search(r'viewBox="([^"]+)"', content)
if vb_match:
    parts = vb_match.group(1).split()
    total_w = float(parts[2])
    total_h = float(parts[3])
else:
    total_w = 4546.0
    total_h = 8504.0

# 2x2 Grid (4 A3 Pages in Landscape) or 2x3 Grid (6 A3 Pages)
# Total width 4546, Total height 8504 -> 2 Columns x 3 Rows = 6 A3 Pages gives optimal aspect ratio & max legibility!
cols = 2
rows = 3
tile_w = total_w / cols
tile_h = total_h / rows
overlap = 120 # px overlap for alignment & gluing

html_pages = []

for r in range(rows):
    for c in range(cols):
        min_x = max(0, c * tile_w - overlap/2)
        min_y = max(0, r * tile_h - overlap/2)
        w_slice = min(total_w - min_x, tile_w + overlap)
        h_slice = min(total_h - min_y, tile_h + overlap)

        page_num = r * cols + c + 1
        
        # Sliced SVG viewBox
        sliced_svg = re.sub(
            r'viewBox="[^"]+"',
            f'viewBox="{min_x} {min_y} {w_slice} {h_slice}"',
            content,
            count=1
        )
        
        html_pages.append(f'''
        <div class="page-container">
            <div class="page-header">DIO {page_num} od {cols*rows} (Red {r+1}, Kolona {c+1}) • Porodično Stablo Zehić — A3 Format za sastavljanje</div>
            {sliced_svg}
            <div class="cut-guide">✂️ Linija za preklapanje i spajanje sa susjednim A3 listom</div>
        </div>
        ''')

combined_html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Porodicno Stablo Zehic - Tiled Poster A3</title>
<style>
@page {{
    size: 420mm 297mm;
    margin: 0;
}}
html, body {{
    margin: 0;
    padding: 0;
    background: #F8FAFC;
    font-family: sans-serif;
}}
.page-container {{
    width: 420mm;
    height: 297mm;
    page-break-after: always;
    overflow: hidden;
    position: relative;
    box-sizing: border-box;
}}
.page-header {{
    position: absolute;
    top: 6mm;
    left: 10mm;
    font-size: 11px;
    font-weight: 800;
    color: #64748B;
    background: rgba(255,255,255,0.9);
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid #CBD5E1;
    z-index: 100;
}}
.cut-guide {{
    position: absolute;
    bottom: 6mm;
    right: 10mm;
    font-size: 10px;
    font-weight: 700;
    color: #94A3B8;
    background: rgba(255,255,255,0.9);
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px dashed #CBD5E1;
    z-index: 100;
}}
svg {{
    width: 420mm;
    height: 297mm;
    display: block;
}}
</style>
</head>
<body>
{''.join(html_pages)}
</body>
</html>'''

os.makedirs("scratch", exist_ok=True)
with open("scratch/tiled_poster_a3.html", "w", encoding="utf-8") as f:
    f.write(combined_html)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

pdf_target = "Porodicno_Stablo_Zehic_Poster_Tiled_6xA3.pdf"
pdf_public = "public/Porodicno_Stablo_Zehic_Poster_Tiled_6xA3.pdf"
html_abs = os.path.abspath("scratch/tiled_poster_a3.html")

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={os.path.abspath(pdf_target)}",
    f"file:///{html_abs.replace(os.sep, '/')}"
]
subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_target):
    shutil.copy(pdf_target, pdf_public)
    size_kb = round(os.path.getsize(pdf_target) / 1024, 1)
    print(f"[SUCCESS] Generated Tiled Poster PDF: {pdf_target} ({size_kb} KB, 6 Pages A3 Landscape)")
else:
    print("[ERROR] Failed to generate Tiled Poster PDF")

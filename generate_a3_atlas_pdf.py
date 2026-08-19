# -*- coding: utf-8 -*-
"""
Generate Ultra-High Legibility Multi-Page A3 Family Atlas / Booklet for Zehic Family Tree:
Specifically crafted so that when printed on standard ISO A3 paper (420mm x 297mm),
EVERY single name, date, spouse, and note is large, crisp, bold, and 100% readable!

Pages:
- Page 1: Glavni Pregled & Korijen (Ibrahim & Hanča + 5 Grana)
- Page 2: Grana Adem — Loza Avde & Muje
- Page 3: Grana Adem — Loza Hasana, Saliha, Mustafe, Mehmeda
- Page 4: Grana Osman — Loza Salkana
- Page 5: Grana Osman — Loza Šaćira, Šahbaza, Ahmeta, Mustafe, Husejna
- Page 6: Grana Meho — Cjelokupna loza Mehe & Cure
"""
import json
import os
import re
import subprocess
import shutil
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

root_node = raw_data["root"]

# Typography & styling tailored for ISO A3 (420mm x 297mm)
# In SVG: width = 2970, height = 2100 (10 px = 1.41 mm, giving huge, crisp print resolution)
PAGE_W = 2970
PAGE_H = 2100

MALE_TEXT = "#1E3A8A"
MALE_BG = "#EFF6FF"
MALE_BORDER = "#3B82F6"
MALE_AV_BG = "#DBEAFE"
MALE_AV_TEXT = "#1D4ED8"

FEMALE_TEXT = "#831843"
FEMALE_BG = "#FDF2F8"
FEMALE_BORDER = "#EC4899"
FEMALE_AV_BG = "#FCE7F3"
FEMALE_AV_TEXT = "#BE185D"

BRANCH_COLORS = {
    "Grana Adem": {"border": "#16A34A", "badge_bg": "#DCFCE7", "badge_txt": "#14532D", "line": "#16A34A"},
    "Grana Osman": {"border": "#0284C7", "badge_bg": "#E0F2FE", "badge_txt": "#0C4A6E", "line": "#0284C7"},
    "Grana Meho": {"border": "#D97706", "badge_bg": "#FEF3C7", "badge_txt": "#78350F", "line": "#D97706"},
    "Grana Nurif": {"border": "#E11D48", "badge_bg": "#FFE4E6", "badge_txt": "#881337", "line": "#E11D48"},
    "Grana Paša": {"border": "#9333EA", "badge_bg": "#F3E8FF", "badge_txt": "#581C87", "line": "#9333EA"}
}

def render_card_svg(x, y, w, h, node, branch_color):
    name = node.get("name", "")
    gender = node.get("gender", "M")
    is_male = (gender == "M")
    spouse = node.get("spouse")
    has_spouse = spouse is not None
    notes = node.get("notes", "")
    dates = node.get("dates", "")

    bg = MALE_BG if is_male else FEMALE_BG
    border = MALE_BORDER if is_male else FEMALE_BORDER
    text_color = MALE_TEXT if is_male else FEMALE_TEXT
    av_bg = MALE_AV_BG if is_male else FEMALE_AV_BG
    av_text = MALE_AV_TEXT if is_male else FEMALE_AV_TEXT

    badge_svg = ""
    if "Pogin" in notes:
        badge_text = "Poginula" if not is_male else "Poginuo"
        badge_svg = f'''<rect x="{w-120}" y="8" width="112" height="26" rx="13" fill="#FEE2E2" stroke="#EF4444" stroke-width="1.5"/><text x="{w-64}" y="26" font-size="14" font-weight="900" fill="#B91C1C" text-anchor="middle">{badge_text}</text>'''
    elif notes and notes not in ["Supruga", "Suprug"]:
        clean_n = notes
        if len(clean_n) > 20: clean_n = clean_n[:19] + "…"
        badge_svg = f'''<rect x="{w-160}" y="8" width="152" height="26" rx="13" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.5"/><text x="{w-84}" y="26" font-size="13" font-weight="800" fill="#334155" text-anchor="middle">{clean_n}</text>'''

    dates_str = f" ({dates})" if dates else ""

    if not has_spouse:
        initial = name[0] if name else "?"
        return f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="3" width="{w}" height="{h}" rx="14" fill="#000" opacity="0.08" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{bg}" stroke="{border}" stroke-width="2.5" />
    <rect x="0" y="0" width="8" height="{h}" rx="4" fill="{branch_color}" />
    <circle cx="36" cy="{h/2}" r="20" fill="{av_bg}" />
    <text x="36" y="{h/2 + 7}" font-size="18" font-weight="900" fill="{av_text}" text-anchor="middle">{initial}</text>
    <text x="68" y="{h/2 - 2}" font-size="22" font-weight="900" fill="{text_color}">{name}</text>
    <text x="68" y="{h/2 + 22}" font-size="14" font-weight="700" fill="#64748B">{dates_str or 'Potomak'}</text>
    {badge_svg}
</g>'''
    else:
        sp_name = spouse.get("name", "")
        sp_notes = spouse.get("notes", "")
        sp_dates = spouse.get("dates", "")
        sp_badge = f'<text x="{w-16}" y="{h-16}" font-size="13" font-weight="800" fill="#BE185D" text-anchor="end">{sp_notes or "Supruga"}</text>' if sp_notes else ''

        return f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="4" width="{w}" height="{h}" rx="16" fill="#000" opacity="0.1" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="#FFFFFF" stroke="{border}" stroke-width="3" />
    <rect x="0" y="0" width="10" height="{h}" rx="5" fill="{branch_color}" />
    
    <!-- Primary person -->
    <rect x="10" y="0" width="{w-10}" height="{h/2}" fill="{bg}" rx="14" style="border-bottom-left-radius:0; border-bottom-right-radius:0;" />
    <circle cx="38" cy="{h/4}" r="18" fill="{av_bg}" />
    <text x="38" y="{h/4 + 6}" font-size="16" font-weight="900" fill="{av_text}" text-anchor="middle">{name[0] if name else '?'}</text>
    <text x="68" y="{h/4 + 7}" font-size="22" font-weight="900" fill="{text_color}">{name}{dates_str}</text>
    {badge_svg}

    <!-- Line divider -->
    <line x1="16" y1="{h/2}" x2="{w-16}" y2="{h/2}" stroke="#CBD5E1" stroke-width="1.5" />
    <circle cx="{w/2}" cy="{h/2}" r="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" />
    <text x="{w/2}" y="{h/2 + 5}" font-size="12" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>

    <!-- Spouse -->
    <circle cx="38" cy="{3*h/4}" r="18" fill="{FEMALE_AV_BG}" />
    <text x="38" y="{3*h/4 + 6}" font-size="15" font-weight="900" fill="{FEMALE_AV_TEXT}" text-anchor="middle">💍</text>
    <text x="68" y="{3*h/4 + 7}" font-size="20" font-weight="900" fill="{FEMALE_TEXT}">{sp_name}</text>
    {sp_badge}
</g>'''

class A3TreeLayout:
    def __init__(self, node_list, page_title, page_subtitle, branch_key):
        self.node_list = node_list
        self.page_title = page_title
        self.page_subtitle = page_subtitle
        self.branch_key = branch_key
        self.branch_info = BRANCH_COLORS.get(branch_key, BRANCH_COLORS["Grana Adem"])

    def compute_span(self, node):
        has_sp = "spouse" in node
        h = 105 if has_sp else 65
        children = node.get("children", [])
        if not children:
            node["_span"] = h
            return h
        ch_spans = [self.compute_span(c) for c in children]
        total = sum(ch_spans) + (len(children)-1) * 16
        node["_span"] = max(h, total)
        return node["_span"]

    def render_page_svg(self):
        # Calculate tree layout
        card_w = 320
        col_w = 380
        start_x = 100
        start_y = 220

        # Calculate spans
        for root in self.node_list:
            self.compute_span(root)

        total_tree_h = sum(n["_span"] for n in self.node_list) + (len(self.node_list)-1)*30
        
        # Scale factor if tree is taller than page content area (1750px)
        avail_h = 1750
        scale = 1.0
        if total_tree_h > avail_h:
            scale = avail_h / total_tree_h

        svg_elements = []
        lines = []

        def place(node, col, cur_y):
            has_sp = "spouse" in node
            ch = 105 if has_sp else 65
            span = node["_span"]

            ny = cur_y + (span - ch) / 2
            nx = start_x + (col - 1) * col_w

            svg_elements.append(render_card_svg(nx, ny, card_w, ch, node, self.branch_info["border"]))

            parent_out_x = nx + card_w
            parent_cy = ny + ch / 2

            children = node.get("children", [])
            if children:
                bus_x = parent_out_x + (col_w - card_w) / 2
                lines.append(f'<line x1="{parent_out_x}" y1="{parent_cy}" x2="{bus_x}" y2="{parent_cy}" stroke="{self.branch_info["line"]}" stroke-width="3" />')
                
                ch_y = cur_y
                child_pts = []
                for c in children:
                    c_pt = place(c, col + 1, ch_y)
                    child_pts.append(c_pt)
                    lines.append(f'<line x1="{bus_x}" y1="{c_pt[1]}" x2="{c_pt[0]}" y2="{c_pt[1]}" stroke="{self.branch_info["line"]}" stroke-width="3" />')
                    ch_y += c["_span"] + 16

                min_cy = min(p[1] for p in child_pts)
                max_cy = max(p[1] for p in child_pts)
                lines.append(f'<line x1="{bus_x}" y1="{min(parent_cy, min_cy)}" x2="{bus_x}" y2="{max(parent_cy, max_cy)}" stroke="{self.branch_info["line"]}" stroke-width="3" />')

            return (nx, parent_cy)

        cur_root_y = start_y
        for r in self.node_list:
            place(r, 1, cur_root_y)
            cur_root_y += r["_span"] + 30

        # Build full page SVG
        page_svg = f'''<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}px" height="{PAGE_H}px" viewBox="0 0 {PAGE_W} {PAGE_H}" style="font-family: 'Plus Jakarta Sans', 'Segoe UI', Arial, sans-serif;">
<rect x="0" y="0" width="{PAGE_W}" height="{PAGE_H}" fill="#F8FAFC" />

<!-- Page Header Banner -->
<rect x="60" y="40" width="{PAGE_W - 120}" height="130" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="3" />
<rect x="60" y="40" width="18" height="130" rx="9" fill="{self.branch_info["border"]}" />

<text x="110" y="96" font-size="36" font-weight="900" fill="#0F172A">{self.page_title}</text>
<text x="110" y="140" font-size="20" font-weight="700" fill="#475569">{self.page_subtitle}</text>

<rect x="{PAGE_W - 360}" y="70" width="260" height="65" rx="32" fill="{self.branch_info["badge_bg"]}" stroke="{self.branch_info["border"]}" stroke-width="2" />
<text x="{PAGE_W - 230}" y="112" font-size="22" font-weight="900" fill="{self.branch_info["badge_txt"]}" text-anchor="middle">FORMAT A3 • JASAN ISPIS</text>

<!-- Tree Content Scaled -->
<g transform="translate(0, {start_y * (1 - scale)}) scale({scale})">
{''.join(lines)}
{''.join(svg_elements)}
</g>

<!-- Footer -->
<text x="100" y="{PAGE_H - 40}" font-size="16" font-weight="700" fill="#94A3B8">Porodično Stablo Zehić • Visokorezolucijski A3 Format • 100% Čitljivost imena i rodbinskih veza</text>
<text x="{PAGE_W - 100}" y="{PAGE_H - 40}" font-size="16" font-weight="800" fill="#64748B" text-anchor="end">Ibrahim Zehić (Osnivač loze)</text>
</svg>'''
        return page_svg

print("Generating A3 Multi-Page Atlas SVGs and PDF...")

# Extract subtrees
# 1. Root & 5 Main Branches
root_children_for_p1 = []
for b in root_node.get("children_branches", []):
    p = dict(b["person"])
    # strip deeper children for overview page
    p_shallow = dict(p)
    p_shallow["children"] = [
        {"name": c.get("name"), "gender": c.get("gender", "M"), "dates": c.get("dates", ""), "notes": c.get("notes", "")}
        for c in p.get("children", [])[:6]
    ]
    root_children_for_p1.append(p_shallow)

ibrahim_p1 = dict(root_node)
ibrahim_p1["children"] = root_children_for_p1

# 2. Adem Sub-branches
adem_person = next(b["person"] for b in root_node["children_branches"] if b["branch_name"] == "Grana Adem")
adem_ch = adem_person.get("children", [])
adem_p1_nodes = [c for c in adem_ch if c.get("name") in ["Avdo", "Mujo"]]
adem_p2_nodes = [c for c in adem_ch if c.get("name") not in ["Avdo", "Mujo"]]

# 3. Osman Sub-branches
osman_person = next(b["person"] for b in root_node["children_branches"] if b["branch_name"] == "Grana Osman")
osman_ch = osman_person.get("children", [])
osman_p1_nodes = [c for c in osman_ch if c.get("name") == "Salkan"]
osman_p2_nodes = [c for c in osman_ch if c.get("name") != "Salkan"]

# 4. Meho Branch
meho_person = next(b["person"] for b in root_node["children_branches"] if b["branch_name"] == "Grana Meho")

pages_configs = [
    ([ibrahim_p1], "PORODIČNO STABLO ZEHIĆ — PREGLED & KORIJEN", "Osnivač Ibrahim & Hanča te 5 glavnih porodičnih grana (Adem, Osman, Meho, Nurif, Paša)", "Grana Adem"),
    (adem_p1_nodes, "GRANA ADEM — DIO 1 (LOZA AVDE & MUJE)", "Detaljno potomstvo Avde i Muje Zehića sa suprugama i svim generacijama", "Grana Adem"),
    (adem_p2_nodes, "GRANA ADEM — DIO 2 (LOZA HASANA, SALIHA, MUSTAFE & MEHMEDA)", "Detaljno potomstvo Hasana, Saliha, Mustafe i Mehmeda Zehića", "Grana Adem"),
    (osman_p1_nodes, "GRANA OSMAN — DIO 1 (LOZA SALKANA ZEHIĆA)", "Brojno potomstvo Salkana Zehića sa svim sinovima, kćerkama i unucima", "Grana Osman"),
    (osman_p2_nodes, "GRANA OSMAN — DIO 2 (LOZA ŠAĆIRA, ŠAHBAZA, AHMETA, MUSTAFE & HUSEJNA)", "Potomstvo Šaćira, Šahbaza, Ahmeta, Mustafe i Husejna Zehića", "Grana Osman"),
    ([meho_person], "GRANA MEHO — CJELOKUPNO POTOMSTVO", "Potomstvo Mehe i Cure Zehić preko loze Mehmeda, Zedina i njihovih potomaka", "Grana Meho")
]

os.makedirs("a3_atlas_pages", exist_ok=True)
html_pages = []

for idx, (node_sublist, title, subtitle, b_key) in enumerate(pages_configs, 1):
    layout = A3TreeLayout(node_sublist, title, subtitle, b_key)
    svg_str = layout.render_page_svg()
    
    svg_filename = f"a3_atlas_pages/page_{idx}.svg"
    with open(svg_filename, "w", encoding="utf-8") as f:
        f.write(svg_str)
        
    html_pages.append(f'''
    <div class="page-container">
        {svg_str}
    </div>
    ''')
    print(f"Rendered Atlas Page {idx}: {title}")

# Combined Multi-Page HTML for Chromium/Edge A3 Printing
combined_html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Porodicno Stablo Zehic - A3 Atlas</title>
<style>
@page {{
    size: 420mm 297mm;
    margin: 0;
}}
html, body {{
    margin: 0;
    padding: 0;
    background: #F8FAFC;
}}
.page-container {{
    width: 420mm;
    height: 297mm;
    page-break-after: always;
    overflow: hidden;
    display: block;
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

with open("scratch/a3_atlas_full.html", "w", encoding="utf-8") as f:
    f.write(combined_html)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

pdf_target = "Porodicno_Stablo_Zehic_A3_Atlas.pdf"
pdf_public = "public/Porodicno_Stablo_Zehic_A3_Atlas.pdf"
html_abs = os.path.abspath("scratch/a3_atlas_full.html")

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
    print(f"\n[SUCCESS] Generated Ultra-Legible Multi-Page A3 Atlas PDF: {pdf_target} ({size_kb} KB, 6 Pages A3 Landscape)")
else:
    print("\n[ERROR] Failed to generate A3 Atlas PDF")

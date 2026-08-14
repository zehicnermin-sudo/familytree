# -*- coding: utf-8 -*-
"""
Generate Multi-Layout Tree Engine:
1. Bilateralni (Centar -> Lijevo/Desno) - [Porodicno_Stablo_Zehic_A0.svg]
2. Uspravni / Vertikalni (Vrh -> Dno) - [Porodicno_Stablo_Zehic_Vertikalno.svg]
3. Horizontalni (Lijevo -> Desno) - [Porodicno_Stablo_Zehic_Horizontalno.svg]
"""
import os
import json
import subprocess
import shutil

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

CARD_W = 238
CARD_H = 48
CARD_H_COUPLE = 80
V_GAP = 14
H_GAP = 20
GEN_V_HEIGHT = 160
COL_W = 284

MALE_TEXT_COLOR = "#1D4ED8"
MALE_AVATAR_BG = "#DBEAFE"
MALE_AVATAR_TEXT = "#1E40AF"

FEMALE_TEXT_COLOR = "#BE185D"
FEMALE_AVATAR_BG = "#FCE7F3"
FEMALE_AVATAR_TEXT = "#9D174D"

THEMES = {
    "root": {
        "name": "Zajednički korijen",
        "bg": "#1E293B", "border": "#0F172A", "primary": "#0F172A", "card_bg": "#FFFFFF",
        "text": "#0F172A", "subtext": "#64748B", "line": "#475569", "tag_bg": "#E2E8F0"
    },
    "Grana Adem": {
        "name": "Grana Adem (1855–1938)",
        "bg": "#F0FDF4", "card_bg": "#FFFFFF", "border": "#16A34A", "primary": "#15803D",
        "text": "#14532D", "subtext": "#166534", "line": "#16A34A", "tag_bg": "#DCFCE7"
    },
    "Grana Meho": {
        "name": "Grana Meho (1867–1941)",
        "bg": "#FFFBEB", "card_bg": "#FFFFFF", "border": "#D97706", "primary": "#B45309",
        "text": "#78350F", "subtext": "#92400E", "line": "#D97706", "tag_bg": "#FEF3C7"
    },
    "Grana Osman": {
        "name": "Grana Osman (1860–1937)",
        "bg": "#F0F9FF", "card_bg": "#FFFFFF", "border": "#0284C7", "primary": "#0369A1",
        "text": "#0C4A6E", "subtext": "#075985", "line": "#0284C7", "tag_bg": "#E0F2FE"
    },
    "Grana Nurif": {
        "name": "Grana Nurif",
        "bg": "#FFF1F2", "card_bg": "#FFFFFF", "border": "#E11D48", "primary": "#BE123C",
        "text": "#881337", "subtext": "#9F1239", "line": "#E11D48", "tag_bg": "#FFE4E6"
    },
    "Grana Paša": {
        "name": "Grana Paša",
        "bg": "#FAF5FF", "card_bg": "#FFFFFF", "border": "#9333EA", "primary": "#7E22CE",
        "text": "#581C87", "subtext": "#6B21A8", "line": "#9333EA", "tag_bg": "#F3E8FF"
    }
}

# ==========================================
# 1. TOP-DOWN VERTICAL TREE GENERATOR
# ==========================================
def generate_vertical_tree(data):
    all_nodes = []
    all_lines = []

    def compute_vertical_width(node):
        has_sp = "spouse" in node
        self_w = CARD_W
        children = node.get("children", [])
        if not children:
            node["_span_w"] = self_w
            return self_w
        ch_widths = [compute_vertical_width(c) for c in children]
        total_ch_w = sum(ch_widths) + (len(children) - 1) * H_GAP
        node["_span_w"] = max(self_w, total_ch_w)
        return node["_span_w"]

    # Wrap root and branches
    root_node = data["root"]
    branches = root_node["children_branches"]

    for b in branches:
        compute_vertical_width(b["person"])

    total_branch_w = sum(b["person"]["_span_w"] for b in branches) + (len(branches) - 1) * H_GAP * 3
    root_span_w = max(CARD_W, total_branch_w)

    top_offset = 240
    start_x = 100

    def place_vertical_node(node, left_x, gen_idx, branch_name):
        has_sp = "spouse" in node
        node_h = CARD_H_COUPLE if has_sp else CARD_H
        span_w = node["_span_w"]

        card_x = left_x + (span_w - CARD_W) / 2
        card_y = top_offset + (gen_idx - 1) * GEN_V_HEIGHT

        all_nodes.append({
            "id": node.get("id"),
            "name": node.get("name"),
            "dates": node.get("dates", ""),
            "notes": node.get("notes", ""),
            "gender": node.get("gender", "M"),
            "spouse": node.get("spouse"),
            "gen": gen_idx,
            "branch": branch_name,
            "x": card_x,
            "y": card_y,
            "w": CARD_W,
            "h": node_h,
            "has_spouse": has_sp
        })

        parent_out_x = card_x + CARD_W / 2
        parent_out_y = card_y + node_h

        children = node.get("children", [])
        if children:
            bus_y = parent_out_y + (GEN_V_HEIGHT - node_h) / 2
            all_lines.append({
                "x1": parent_out_x, "y1": parent_out_y,
                "x2": parent_out_x, "y2": bus_y,
                "branch": branch_name
            })

            ch_cur_x = left_x
            child_xs = []
            for c in children:
                c_span_w = c["_span_w"]
                c_in_pt = place_vertical_node(c, ch_cur_x, gen_idx + 1, branch_name)
                child_xs.append(c_in_pt[0])
                all_lines.append({
                    "x1": c_in_pt[0], "y1": bus_y,
                    "x2": c_in_pt[0], "y2": c_in_pt[1],
                    "branch": branch_name
                })
                ch_cur_x += c_span_w + H_GAP

            all_lines.append({
                "x1": min(child_xs), "y1": bus_y,
                "x2": max(child_xs), "y2": bus_y,
                "branch": branch_name
            })

        return (parent_out_x, card_y)

    # Place Ibrahim (Root)
    root_cx = start_x + total_branch_w / 2
    all_nodes.append({
        "id": root_node["id"],
        "name": root_node["name"],
        "role": "Osnivač loze Zehić",
        "dates": "Zajednički Predak",
        "gender": "M",
        "gen": 1,
        "branch": "root",
        "x": root_cx - CARD_W / 2,
        "y": top_offset,
        "w": CARD_W,
        "h": 90,
        "is_root": True
    })

    root_bus_y = top_offset + 90 + 35
    all_lines.append({
        "x1": root_cx, "y1": top_offset + 90,
        "x2": root_cx, "y2": root_bus_y,
        "branch": "root"
    })

    cur_bx = start_x
    branch_in_xs = []
    for b in branches:
        b_name = b["branch_name"]
        p = b["person"]
        in_pt = place_vertical_node(p, cur_bx, 2, b_name)
        branch_in_xs.append(in_pt[0])
        all_lines.append({
            "x1": in_pt[0], "y1": root_bus_y,
            "x2": in_pt[0], "y2": in_pt[1],
            "branch": b_name
        })
        cur_bx += p["_span_w"] + H_GAP * 3

    all_lines.append({
        "x1": min(branch_in_xs), "y1": root_bus_y,
        "x2": max(branch_in_xs), "y2": root_bus_y,
        "branch": "root"
    })

    # Render Vertical SVG
    raw_min_x = min(n["x"] for n in all_nodes) - 80
    raw_max_x = max(n["x"] + n["w"] for n in all_nodes) + 80
    raw_min_y = 0
    raw_max_y = max(n["y"] + n["h"] for n in all_nodes) + 120

    width = int(raw_max_x - raw_min_x)
    height = int(raw_max_y - raw_min_y)

    shift_x = -raw_min_x
    shift_y = 0

    svg = []
    svg.append(f'''<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     x="0px" y="0px" width="{width}px" height="{height}px" viewBox="0 0 {width} {height}" 
     xml:space="preserve" style="font-family: 'Plus Jakarta Sans', 'Segoe UI', Arial, Helvetica, sans-serif;">

<rect x="0" y="0" width="{width}" height="{height}" fill="#F8FAFC" />

<!-- Glavni Naslov -->
<g transform="translate({width/2}, 45)">
    <rect x="-380" y="2" width="760" height="85" rx="18" fill="#E2E8F0" />
    <rect x="-380" y="0" width="760" height="85" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />
    <text x="0" y="38" font-size="28" font-weight="900" fill="#0F172A" text-anchor="middle">PORODIČNO STABLO ZEHIĆ</text>
    <text x="0" y="66" font-size="16" font-weight="700" fill="#475569" text-anchor="middle">Potomstvo Ibrahima Zehića • Uspravni Vertikalni Prikaz (Od Vrha ka Dnu)</text>
</g>

<!-- Desna Legenda -->
<g transform="translate({width - 580}, 25)">
    <rect x="0" y="2" width="550" height="200" rx="16" fill="#E2E8F0" />
    <rect x="0" y="0" width="550" height="200" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />
    
    <text x="20" y="26" font-size="13" font-weight="800" fill="#1E293B">LEGENDA BOJA, GRANA &amp; OZNAKA</text>
    <line x1="20" y1="34" x2="530" y2="34" stroke="#E2E8F0" stroke-width="1.2" />

    <text x="20" y="52" font-size="11.5" font-weight="800" fill="#475569">PORODIČNE GRANE:</text>
    <circle cx="28" cy="70" r="6.5" fill="#16A34A" />
    <text x="42" y="74" font-size="12" font-weight="700" fill="#14532D">Grana Adem (177)</text>

    <circle cx="28" cy="94" r="6.5" fill="#0284C7" />
    <text x="42" y="98" font-size="12" font-weight="700" fill="#0C4A6E">Grana Osman (152)</text>

    <circle cx="28" cy="118" r="6.5" fill="#D97706" />
    <text x="42" y="122" font-size="12" font-weight="700" fill="#78350F">Grana Meho (69)</text>

    <circle cx="28" cy="142" r="6.5" fill="#E11D48" />
    <text x="42" y="146" font-size="12" font-weight="700" fill="#881337">Nurif &amp; Paša</text>

    <line x1="260" y1="42" x2="260" y2="185" stroke="#E2E8F0" stroke-width="1.2" />

    <text x="280" y="52" font-size="11.5" font-weight="800" fill="#475569">OZNAKE PO SPOLU &amp; BRAKU:</text>
    <rect x="280" y="64" width="14" height="14" rx="4" fill="#DBEAFE" stroke="#1D4ED8" stroke-width="2"/>
    <text x="302" y="76" font-size="12.5" font-weight="900" fill="#1D4ED8">Muško ime (Plava)</text>

    <rect x="280" y="92" width="14" height="14" rx="4" fill="#FCE7F3" stroke="#BE185D" stroke-width="2"/>
    <text x="302" y="104" font-size="12.5" font-weight="900" fill="#BE185D">Žensko ime (Roze)</text>

    <g transform="translate(280, 126)">
        <line x1="0" y1="0" x2="22" y2="0" stroke="#CBD5E1" stroke-width="1.5" />
        <circle cx="11" cy="0" r="7.5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
        <text x="11" y="3" font-size="8" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>
        <text x="28" y="4" font-size="12" font-weight="700" fill="#475569">Bračni par (Brak)</text>
    </g>

    <g transform="translate(280, 156)">
        <rect x="0" y="-8" width="62" height="16" rx="8" fill="#FEE2E2" stroke="#EF4444" stroke-width="1" />
        <text x="31" y="3.5" font-size="8.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>
        <text x="68" y="4" font-size="12" font-weight="700" fill="#475569">Poginuo</text>
    </g>
</g>
''')

    # Generation Row Markers on Left Margin
    max_gen = max(n.get("gen", 1) for n in all_nodes)
    for g in range(1, max_gen + 1):
        gy = top_offset + (g - 1) * GEN_V_HEIGHT + 20
        svg.append(f'''
<g transform="translate(50, {gy})">
    <rect x="0" y="-14" width="70" height="28" rx="14" fill="#1E293B" />
    <text x="35" y="4" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g}</text>
</g>''')

    # Lines
    for line in all_lines:
        b_theme = THEMES.get(line["branch"], THEMES["root"])
        stroke_color = b_theme.get("line", "#475569")
        x1 = line['x1'] + shift_x
        y1 = line['y1'] + shift_y
        x2 = line['x2'] + shift_x
        y2 = line['y2'] + shift_y
        svg.append(f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />''')

    # Cards
    for n in all_nodes:
        x = n["x"] + shift_x
        y = n["y"] + shift_y
        w, h = n["w"], n["h"]
        is_root = n.get("is_root", False)
        branch = n.get("branch", "root")
        theme = THEMES.get(branch, THEMES["root"])
        
        name = n["name"]
        dates = n.get("dates", "")
        notes = n.get("notes", "")
        gender = n.get("gender", "M")
        is_male = (gender == "M")
        has_spouse = n.get("has_spouse", False)
        spouse = n.get("spouse")

        if is_root:
            svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="3" width="{w}" height="{h}" rx="16" fill="#0B0F19" opacity="0.3" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="#1E293B" stroke="#3B82F6" stroke-width="3" />
    <circle cx="36" cy="{h/2}" r="22" fill="#334155" />
    <text x="36" y="{h/2 + 7}" font-size="20" font-weight="900" fill="#F8FAFC" text-anchor="middle">👑</text>
    <text x="70" y="40" font-size="24" font-weight="900" fill="#93C5FD">{name}</text>
    <text x="70" y="66" font-size="13.5" font-weight="700" fill="#94A3B8">(Osnivač loze Zehić)</text>
</g>''')
        elif not has_spouse:
            border_c = theme.get("border", "#94A3B8")
            bar_c = theme.get("primary", "#475569")
            name_color = MALE_TEXT_COLOR if is_male else FEMALE_TEXT_COLOR
            av_bg = MALE_AVATAR_BG if is_male else FEMALE_AVATAR_BG
            av_text = MALE_AVATAR_TEXT if is_male else FEMALE_AVATAR_TEXT
            initial = name[0] if name else "?"

            badge = ""
            if "Poginu" in notes:
                badge = f'''<rect x="{w - 74}" y="6" width="68" height="18" rx="9" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/><text x="{w - 40}" y="19" font-size="9.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>'''
            elif notes and notes not in ["Supruga", "Suprug"]:
                clean_n = notes.replace("u. ", "u. ").replace("r. ", "r. ")
                if len(clean_n) > 20:
                    clean_n = clean_n[:18] + "…"
                badge = f'''<rect x="{w - 110}" y="6" width="104" height="18" rx="9" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/><text x="{w - 58}" y="19" font-size="9" font-weight="700" fill="#334155" text-anchor="middle">{clean_n}</text>'''

            svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="2" width="{w}" height="{h}" rx="10" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{border_c}" stroke-width="2" />
    <path d="M 0 10 Q 0 0 10 0 L {w-10} 0 Q {w} 0 {w} 10 L {w} 4 L 0 4 Z" fill="{bar_c}" />
    
    <circle cx="22" cy="{h/2 + 2}" r="13" fill="{av_bg}" />
    <text x="22" y="{h/2 + 6.5}" font-size="11" font-weight="900" fill="{av_text}" text-anchor="middle">{initial}</text>
    {badge}
    <text x="44" y="27" font-size="15" font-weight="900" fill="{name_color}">{name}</text>
''')
            if dates:
                svg.append(f'''<text x="44" y="42" font-size="10.5" font-weight="700" fill="#64748B">🗓 {dates}</text>''')
            elif notes and "Poginu" not in notes and notes not in ["Supruga", "Suprug"]:
                display_note = notes[:22] + "…" if len(notes) > 24 else notes
                svg.append(f'''<text x="44" y="42" font-size="9.5" font-weight="600" fill="#64748B">{display_note}</text>''')
            svg.append('</g>\n')

        else:
            border_c = theme.get("border", "#94A3B8")
            bar_c = theme.get("primary", "#475569")
            is_male_p = (gender == "M")
            sp_gender = spouse.get("gender", "F" if is_male_p else "M")
            is_male_s = (sp_gender == "M")

            name_color_p = MALE_TEXT_COLOR if is_male_p else FEMALE_TEXT_COLOR
            av_bg_p = MALE_AVATAR_BG if is_male_p else FEMALE_AVATAR_BG
            av_text_p = MALE_AVATAR_TEXT if is_male_p else FEMALE_AVATAR_TEXT

            name_color_s = MALE_TEXT_COLOR if is_male_s else FEMALE_TEXT_COLOR
            av_bg_s = MALE_AVATAR_BG if is_male_s else FEMALE_AVATAR_BG
            av_text_s = MALE_AVATAR_TEXT if is_male_s else FEMALE_AVATAR_TEXT

            initial_p = name[0] if name else "?"
            sp_name = spouse.get("name", "")
            initial_s = sp_name[0] if sp_name else "?"
            sp_notes = spouse.get("notes", "")

            badge = ""
            if "Poginu" in notes:
                badge = f'''<rect x="{w - 74}" y="6" width="68" height="18" rx="9" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/><text x="{w - 40}" y="19" font-size="9.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>'''

            has_real_sp_note = sp_notes and sp_notes not in ["Supruga", "Suprug"]
            sp_y_name = 62 if not has_real_sp_note else 59

            svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="2" width="{w}" height="{h}" rx="12" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="{border_c}" stroke-width="2" />
    <path d="M 0 12 Q 0 0 12 0 L {w-12} 0 Q {w} 0 {w} 12 L {w} 4 L 0 4 Z" fill="{bar_c}" />

    <circle cx="20" cy="22" r="11" fill="{av_bg_p}" />
    <text x="20" y="26" font-size="10.5" font-weight="900" fill="{av_text_p}" text-anchor="middle">{initial_p}</text>
    <text x="38" y="26" font-size="14.5" font-weight="900" fill="{name_color_p}">{name}</text>
    {badge}
''')
            if dates:
                svg.append(f'''<text x="38" y="37" font-size="9.5" font-weight="700" fill="#64748B">🗓 {dates}</text>''')

            svg.append(f'''
    <line x1="10" y1="41" x2="{w-10}" y2="41" stroke="#E2E8F0" stroke-width="1" />
    <circle cx="{w/2}" cy="41" r="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
    <text x="{w/2}" y="44.5" font-size="8.5" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>

    <circle cx="20" cy="{sp_y_name + 1}" r="11" fill="{av_bg_s}" />
    <text x="20" y="{sp_y_name + 5}" font-size="10.5" font-weight="900" fill="{av_text_s}" text-anchor="middle">{initial_s}</text>
    <text x="38" y="{sp_y_name + 5}" font-size="14.5" font-weight="900" fill="{name_color_s}">{sp_name}</text>
''')
            if has_real_sp_note:
                display_sp_note = sp_notes[:22] + "…" if len(sp_notes) > 24 else sp_notes
                svg.append(f'''<text x="38" y="{sp_y_name + 16}" font-size="9.5" font-weight="600" fill="#64748B">{display_sp_note}</text>''')

            svg.append('</g>\n')

    svg.append('</svg>')
    return "".join(svg)

# ==========================================
# 2. FULL HORIZONTAL TREE (LEFT-TO-RIGHT)
# ==========================================
def generate_full_horizontal_tree(data):
    all_nodes = []
    all_lines = []

    def compute_h_height(node):
        has_sp = "spouse" in node
        self_h = CARD_H_COUPLE if has_sp else CARD_H
        children = node.get("children", [])
        if not children:
            node["_span_h"] = self_h
            return self_h
        ch_heights = [compute_h_height(c) for c in children]
        total_ch_h = sum(ch_heights) + (len(children) - 1) * V_GAP
        node["_span_h"] = max(self_h, total_ch_h)
        return node["_span_h"]

    root_node = data["root"]
    branches = root_node["children_branches"]

    for b in branches:
        compute_h_height(b["person"])

    total_branch_h = sum(b["person"]["_span_h"] for b in branches) + (len(branches) - 1) * V_GAP * 3
    top_offset = 260
    start_x = 100
    start_y = top_offset

    def place_h_node(node, col_idx, top_y, branch_name):
        has_sp = "spouse" in node
        node_h = CARD_H_COUPLE if has_sp else CARD_H
        span_h = node["_span_h"]

        node_y = top_y + (span_h - node_h) / 2
        card_x = start_x + (col_idx - 1) * COL_W

        all_nodes.append({
            "id": node.get("id"),
            "name": node.get("name"),
            "dates": node.get("dates", ""),
            "notes": node.get("notes", ""),
            "gender": node.get("gender", "M"),
            "spouse": node.get("spouse"),
            "gen": col_idx,
            "branch": branch_name,
            "x": card_x,
            "y": node_y,
            "w": CARD_W,
            "h": node_h,
            "has_spouse": has_sp
        })

        parent_in_x = card_x
        parent_out_x = card_x + CARD_W
        parent_center_y = node_y + node_h / 2

        children = node.get("children", [])
        if children:
            ch_cur_y = top_y
            child_attach_points = []
            bus_x = parent_out_x + (COL_W - CARD_W) / 2

            all_lines.append({
                "x1": parent_out_x, "y1": parent_center_y,
                "x2": bus_x, "y2": parent_center_y,
                "branch": branch_name
            })

            for c in children:
                c_span_h = c["_span_h"]
                c_in_pt = place_h_node(c, col_idx + 1, ch_cur_y, branch_name)
                child_attach_points.append(c_in_pt)
                all_lines.append({
                    "x1": bus_x, "y1": c_in_pt[1],
                    "x2": c_in_pt[0], "y2": c_in_pt[1],
                    "branch": branch_name
                })
                ch_cur_y += c_span_h + V_GAP

            min_ch_y = min(p[1] for p in child_attach_points)
            max_ch_y = max(p[1] for p in child_attach_points)
            bus_top = min(parent_center_y, min_ch_y)
            bus_bottom = max(parent_center_y, max_ch_y)

            all_lines.append({
                "x1": bus_x, "y1": bus_top,
                "x2": bus_x, "y2": bus_bottom,
                "branch": branch_name
            })

        return (parent_in_x, parent_center_y)

    # Place Ibrahim
    root_center_y = start_y + total_branch_h / 2
    all_nodes.append({
        "id": root_node["id"],
        "name": root_node["name"],
        "role": "Osnivač loze Zehić",
        "dates": "Zajednički Predak",
        "gender": "M",
        "gen": 1,
        "branch": "root",
        "x": start_x,
        "y": root_center_y - 45,
        "w": CARD_W,
        "h": 90,
        "is_root": True
    })

    root_bus_x = start_x + CARD_W + (COL_W - CARD_W) / 2
    all_lines.append({
        "x1": start_x + CARD_W, "y1": root_center_y,
        "x2": root_bus_x, "y2": root_center_y,
        "branch": "root"
    })

    cur_by = start_y
    branch_in_points = []
    for b in branches:
        b_name = b["branch_name"]
        p = b["person"]
        in_pt = place_h_node(p, 2, cur_by, b_name)
        branch_in_points.append(in_pt)
        all_lines.append({
            "x1": root_bus_x, "y1": in_pt[1],
            "x2": in_pt[0], "y2": in_pt[1],
            "branch": b_name
        })
        cur_by += p["_span_h"] + V_GAP * 3

    min_by = min(p[1] for p in branch_in_points)
    max_by = max(p[1] for p in branch_in_points)
    all_lines.append({
        "x1": root_bus_x, "y1": min(root_center_y, min_by),
        "x2": root_bus_x, "y2": max(root_center_y, max_by),
        "branch": "root"
    })

    raw_min_x = min(n["x"] for n in all_nodes) - 80
    raw_max_x = max(n["x"] + n["w"] for n in all_nodes) + 80
    raw_min_y = 0
    raw_max_y = max(n["y"] + n["h"] for n in all_nodes) + 120

    width = int(raw_max_x - raw_min_x)
    height = int(raw_max_y - raw_min_y)

    shift_x = -raw_min_x
    shift_y = 0

    svg = []
    svg.append(f'''<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     x="0px" y="0px" width="{width}px" height="{height}px" viewBox="0 0 {width} {height}" 
     xml:space="preserve" style="font-family: 'Plus Jakarta Sans', 'Segoe UI', Arial, Helvetica, sans-serif;">

<rect x="0" y="0" width="{width}" height="{height}" fill="#F8FAFC" />

<!-- Header -->
<g transform="translate({width/2 - 180}, 45)">
    <rect x="-380" y="2" width="760" height="85" rx="18" fill="#E2E8F0" />
    <rect x="-380" y="0" width="760" height="85" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />
    <text x="0" y="38" font-size="28" font-weight="900" fill="#0F172A" text-anchor="middle">PORODIČNO STABLO ZEHIĆ</text>
    <text x="0" y="66" font-size="16" font-weight="700" fill="#475569" text-anchor="middle">Potomstvo Ibrahima Zehića • Horizontalni Prikaz (S Lijeva na Desno)</text>
</g>

<!-- Desna Legenda -->
<g transform="translate({width - 580}, 25)">
    <rect x="0" y="2" width="550" height="200" rx="16" fill="#E2E8F0" />
    <rect x="0" y="0" width="550" height="200" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />
    <text x="20" y="26" font-size="13" font-weight="800" fill="#1E293B">LEGENDA BOJA, GRANA &amp; OZNAKA</text>
    <line x1="20" y1="34" x2="530" y2="34" stroke="#E2E8F0" stroke-width="1.2" />

    <text x="20" y="52" font-size="11.5" font-weight="800" fill="#475569">PORODIČNE GRANE:</text>
    <circle cx="28" cy="70" r="6.5" fill="#16A34A" />
    <text x="42" y="74" font-size="12" font-weight="700" fill="#14532D">Grana Adem (177)</text>

    <circle cx="28" cy="94" r="6.5" fill="#0284C7" />
    <text x="42" y="98" font-size="12" font-weight="700" fill="#0C4A6E">Grana Osman (152)</text>

    <circle cx="28" cy="118" r="6.5" fill="#D97706" />
    <text x="42" y="122" font-size="12" font-weight="700" fill="#78350F">Grana Meho (69)</text>

    <circle cx="28" cy="142" r="6.5" fill="#E11D48" />
    <text x="42" y="146" font-size="12" font-weight="700" fill="#881337">Nurif &amp; Paša</text>

    <line x1="260" y1="42" x2="260" y2="185" stroke="#E2E8F0" stroke-width="1.2" />

    <text x="280" y="52" font-size="11.5" font-weight="800" fill="#475569">OZNAKE PO SPOLU &amp; BRAKU:</text>
    <rect x="280" y="64" width="14" height="14" rx="4" fill="#DBEAFE" stroke="#1D4ED8" stroke-width="2"/>
    <text x="302" y="76" font-size="12.5" font-weight="900" fill="#1D4ED8">Muško ime (Plava)</text>

    <rect x="280" y="92" width="14" height="14" rx="4" fill="#FCE7F3" stroke="#BE185D" stroke-width="2"/>
    <text x="302" y="104" font-size="12.5" font-weight="900" fill="#BE185D">Žensko ime (Roze)</text>

    <g transform="translate(280, 126)">
        <line x1="0" y1="0" x2="22" y2="0" stroke="#CBD5E1" stroke-width="1.5" />
        <circle cx="11" cy="0" r="7.5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
        <text x="11" y="3" font-size="8" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>
        <text x="28" y="4" font-size="12" font-weight="700" fill="#475569">Bračni par (Brak)</text>
    </g>

    <g transform="translate(280, 156)">
        <rect x="0" y="-8" width="62" height="16" rx="8" fill="#FEE2E2" stroke="#EF4444" stroke-width="1" />
        <text x="31" y="3.5" font-size="8.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>
        <text x="68" y="4" font-size="12" font-weight="700" fill="#475569">Poginuo</text>
    </g>
</g>
''')

    # Generation Axis Markers (Left to Right)
    axis_y = top_offset - 45
    max_gen = max(n.get("gen", 1) for n in all_nodes)
    for g in range(1, max_gen + 1):
        gx = start_x + shift_x + (g - 1) * COL_W + CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g}</text>
</g>''')

    # Lines
    for line in all_lines:
        b_theme = THEMES.get(line["branch"], THEMES["root"])
        stroke_color = b_theme.get("line", "#475569")
        x1 = line['x1'] + shift_x
        y1 = line['y1'] + shift_y
        x2 = line['x2'] + shift_x
        y2 = line['y2'] + shift_y
        svg.append(f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />''')

    # Cards
    for n in all_nodes:
        x = n["x"] + shift_x
        y = n["y"] + shift_y
        w, h = n["w"], n["h"]
        is_root = n.get("is_root", False)
        branch = n.get("branch", "root")
        theme = THEMES.get(branch, THEMES["root"])
        
        name = n["name"]
        dates = n.get("dates", "")
        notes = n.get("notes", "")
        gender = n.get("gender", "M")
        is_male = (gender == "M")
        has_spouse = n.get("has_spouse", False)
        spouse = n.get("spouse")

        if is_root:
            svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="3" width="{w}" height="{h}" rx="16" fill="#0B0F19" opacity="0.3" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="#1E293B" stroke="#3B82F6" stroke-width="3" />
    <circle cx="36" cy="{h/2}" r="22" fill="#334155" />
    <text x="36" y="{h/2 + 7}" font-size="20" font-weight="900" fill="#F8FAFC" text-anchor="middle">👑</text>
    <text x="70" y="40" font-size="24" font-weight="900" fill="#93C5FD">{name}</text>
    <text x="70" y="66" font-size="13.5" font-weight="700" fill="#94A3B8">(Osnivač loze Zehić)</text>
</g>''')
        elif not has_spouse:
            border_c = theme.get("border", "#94A3B8")
            bar_c = theme.get("primary", "#475569")
            name_color = MALE_TEXT_COLOR if is_male else FEMALE_TEXT_COLOR
            av_bg = MALE_AVATAR_BG if is_male else FEMALE_AVATAR_BG
            av_text = MALE_AVATAR_TEXT if is_male else FEMALE_AVATAR_TEXT
            initial = name[0] if name else "?"

            badge = ""
            if "Poginu" in notes:
                badge = f'''<rect x="{w - 74}" y="6" width="68" height="18" rx="9" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/><text x="{w - 40}" y="19" font-size="9.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>'''
            elif notes and notes not in ["Supruga", "Suprug"]:
                clean_n = notes.replace("u. ", "u. ").replace("r. ", "r. ")
                if len(clean_n) > 20:
                    clean_n = clean_n[:18] + "…"
                badge = f'''<rect x="{w - 110}" y="6" width="104" height="18" rx="9" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/><text x="{w - 58}" y="19" font-size="9" font-weight="700" fill="#334155" text-anchor="middle">{clean_n}</text>'''

            svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="2" width="{w}" height="{h}" rx="10" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{border_c}" stroke-width="2" />
    <path d="M 0 10 Q 0 0 10 0 L {w-10} 0 Q {w} 0 {w} 10 L {w} 4 L 0 4 Z" fill="{bar_c}" />
    
    <circle cx="22" cy="{h/2 + 2}" r="13" fill="{av_bg}" />
    <text x="22" y="{h/2 + 6.5}" font-size="11" font-weight="900" fill="{av_text}" text-anchor="middle">{initial}</text>
    {badge}
    <text x="44" y="27" font-size="15" font-weight="900" fill="{name_color}">{name}</text>
''')
            if dates:
                svg.append(f'''<text x="44" y="42" font-size="10.5" font-weight="700" fill="#64748B">🗓 {dates}</text>''')
            elif notes and "Poginu" not in notes and notes not in ["Supruga", "Suprug"]:
                display_note = notes[:22] + "…" if len(notes) > 24 else notes
                svg.append(f'''<text x="44" y="42" font-size="9.5" font-weight="600" fill="#64748B">{display_note}</text>''')
            svg.append('</g>\n')

        else:
            border_c = theme.get("border", "#94A3B8")
            bar_c = theme.get("primary", "#475569")
            is_male_p = (gender == "M")
            sp_gender = spouse.get("gender", "F" if is_male_p else "M")
            is_male_s = (sp_gender == "M")

            name_color_p = MALE_TEXT_COLOR if is_male_p else FEMALE_TEXT_COLOR
            av_bg_p = MALE_AVATAR_BG if is_male_p else FEMALE_AVATAR_BG
            av_text_p = MALE_AVATAR_TEXT if is_male_p else FEMALE_AVATAR_TEXT

            name_color_s = MALE_TEXT_COLOR if is_male_s else FEMALE_TEXT_COLOR
            av_bg_s = MALE_AVATAR_BG if is_male_s else FEMALE_AVATAR_BG
            av_text_s = MALE_AVATAR_TEXT if is_male_s else FEMALE_AVATAR_TEXT

            initial_p = name[0] if name else "?"
            sp_name = spouse.get("name", "")
            initial_s = sp_name[0] if sp_name else "?"
            sp_notes = spouse.get("notes", "")

            badge = ""
            if "Poginu" in notes:
                badge = f'''<rect x="{w - 74}" y="6" width="68" height="18" rx="9" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/><text x="{w - 40}" y="19" font-size="9.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>'''

            has_real_sp_note = sp_notes and sp_notes not in ["Supruga", "Suprug"]
            sp_y_name = 62 if not has_real_sp_note else 59

            svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="2" width="{w}" height="{h}" rx="12" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="{border_c}" stroke-width="2" />
    <path d="M 0 12 Q 0 0 12 0 L {w-12} 0 Q {w} 0 {w} 12 L {w} 4 L 0 4 Z" fill="{bar_c}" />

    <circle cx="20" cy="22" r="11" fill="{av_bg_p}" />
    <text x="20" y="26" font-size="10.5" font-weight="900" fill="{av_text_p}" text-anchor="middle">{initial_p}</text>
    <text x="38" y="26" font-size="14.5" font-weight="900" fill="{name_color_p}">{name}</text>
    {badge}
''')
            if dates:
                svg.append(f'''<text x="38" y="37" font-size="9.5" font-weight="700" fill="#64748B">🗓 {dates}</text>''')

            svg.append(f'''
    <line x1="10" y1="41" x2="{w-10}" y2="41" stroke="#E2E8F0" stroke-width="1" />
    <circle cx="{w/2}" cy="41" r="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
    <text x="{w/2}" y="44.5" font-size="8.5" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>

    <circle cx="20" cy="{sp_y_name + 1}" r="11" fill="{av_bg_s}" />
    <text x="20" y="{sp_y_name + 5}" font-size="10.5" font-weight="900" fill="{av_text_s}" text-anchor="middle">{initial_s}</text>
    <text x="38" y="{sp_y_name + 5}" font-size="14.5" font-weight="900" fill="{name_color_s}">{sp_name}</text>
''')
            if has_real_sp_note:
                display_sp_note = sp_notes[:22] + "…" if len(sp_notes) > 24 else sp_notes
                svg.append(f'''<text x="38" y="{sp_y_name + 16}" font-size="9.5" font-weight="600" fill="#64748B">{display_sp_note}</text>''')

            svg.append('</g>\n')

    svg.append('</svg>')
    return "".join(svg)

# Run generation
vert_svg = generate_vertical_tree(raw_data)
with open("Porodicno_Stablo_Zehic_Vertikalno.svg", "w", encoding="utf-8") as f:
    f.write(vert_svg)

horiz_svg = generate_full_horizontal_tree(raw_data)
with open("Porodicno_Stablo_Zehic_Horizontalno.svg", "w", encoding="utf-8") as f:
    f.write(horiz_svg)

print("Generated Vertical & Full Horizontal Tree SVGs successfully!")

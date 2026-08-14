# -*- coding: utf-8 -*-
"""
Generate Bilateral Up/Down Tree (Ibrahim in Middle, 2 branches UP, 2-3 branches DOWN)
All cards and text are strictly horizontal (vodoravno) for optimal readability!
"""
import os
import json
import re
import subprocess
import shutil

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

CARD_W = 238
CARD_H = 48
CARD_H_COUPLE = 80
H_GAP = 18
GEN_STEP_Y = 150

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

def compute_horizontal_span(node):
    has_sp = "spouse" in node
    self_w = CARD_W
    children = node.get("children", [])
    if not children:
        node["_span_w"] = self_w
        return self_w
    ch_widths = [compute_horizontal_span(c) for c in children]
    total_ch_w = sum(ch_widths) + (len(children) - 1) * H_GAP
    node["_span_w"] = max(self_w, total_ch_w)
    return node["_span_w"]

def generate_up_down_tree():
    all_nodes = []
    all_lines = []

    root_node = raw_data["root"]
    branches = root_node["children_branches"]

    # Assign branches:
    # UPWARD (Na Gore): Adem + Nurif
    # DOWNWARD (Na Dole): Osman + Meho + Paša
    up_branches = [b for b in branches if b["branch_name"] in ["Grana Adem", "Grana Nurif"]]
    down_branches = [b for b in branches if b["branch_name"] in ["Grana Osman", "Grana Meho", "Grana Paša"]]

    for b in branches:
        compute_horizontal_span(b["person"])

    up_total_w = sum(b["person"]["_span_w"] for b in up_branches) + (len(up_branches) - 1) * (H_GAP * 4)
    down_total_w = sum(b["person"]["_span_w"] for b in down_branches) + (len(down_branches) - 1) * (H_GAP * 4)
    max_total_w = max(up_total_w, down_total_w)

    # Let Center Y be 0
    center_y = 0

    # Place UPWARD branches (Gen 2 -> Gen 8 going UP, y decreases)
    def place_upward_node(node, left_x, gen_idx, branch_name):
        has_sp = "spouse" in node
        node_h = CARD_H_COUPLE if has_sp else CARD_H
        span_w = node["_span_w"]

        card_x = left_x + (span_w - CARD_W) / 2
        card_y = center_y - (gen_idx - 1) * GEN_STEP_Y - node_h

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
            "has_spouse": has_sp,
            "direction": "UP"
        })

        parent_out_x = card_x + CARD_W / 2
        parent_out_y = card_y # Top of parent card
        parent_in_y = card_y + node_h # Bottom of parent card (connects to its parent below)

        children = node.get("children", [])
        if children:
            bus_y = parent_out_y - (GEN_STEP_Y - node_h) / 2
            all_lines.append({
                "x1": parent_out_x, "y1": parent_out_y,
                "x2": parent_out_x, "y2": bus_y,
                "branch": branch_name
            })

            ch_cur_x = left_x
            child_xs = []
            for c in children:
                c_span_w = c["_span_w"]
                c_attach_pt = place_upward_node(c, ch_cur_x, gen_idx + 1, branch_name)
                child_xs.append(c_attach_pt[0])
                all_lines.append({
                    "x1": c_attach_pt[0], "y1": bus_y,
                    "x2": c_attach_pt[0], "y2": c_attach_pt[1],
                    "branch": branch_name
                })
                ch_cur_x += c_span_w + H_GAP

            all_lines.append({
                "x1": min(child_xs), "y1": bus_y,
                "x2": max(child_xs), "y2": bus_y,
                "branch": branch_name
            })

        return (parent_out_x, parent_in_y)

    # Place DOWNWARD branches (Gen 2 -> Gen 8 going DOWN, y increases)
    def place_downward_node(node, left_x, gen_idx, branch_name):
        has_sp = "spouse" in node
        node_h = CARD_H_COUPLE if has_sp else CARD_H
        span_w = node["_span_w"]

        card_x = left_x + (span_w - CARD_W) / 2
        card_y = center_y + (gen_idx - 1) * GEN_STEP_Y

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
            "has_spouse": has_sp,
            "direction": "DOWN"
        })

        parent_out_x = card_x + CARD_W / 2
        parent_out_y = card_y + node_h # Bottom of parent card
        parent_in_y = card_y # Top of parent card (connects to its parent above)

        children = node.get("children", [])
        if children:
            bus_y = parent_out_y + (GEN_STEP_Y - node_h) / 2
            all_lines.append({
                "x1": parent_out_x, "y1": parent_out_y,
                "x2": parent_out_x, "y2": bus_y,
                "branch": branch_name
            })

            ch_cur_x = left_x
            child_xs = []
            for c in children:
                c_span_w = c["_span_w"]
                c_attach_pt = place_downward_node(c, ch_cur_x, gen_idx + 1, branch_name)
                child_xs.append(c_attach_pt[0])
                all_lines.append({
                    "x1": c_attach_pt[0], "y1": bus_y,
                    "x2": c_attach_pt[0], "y2": c_attach_pt[1],
                    "branch": branch_name
                })
                ch_cur_x += c_span_w + H_GAP

            all_lines.append({
                "x1": min(child_xs), "y1": bus_y,
                "x2": max(child_xs), "y2": bus_y,
                "branch": branch_name
            })

        return (parent_out_x, parent_in_y)

    # Align UPWARD branches horizontally centered
    up_start_x = (max_total_w - up_total_w) / 2 + 100
    cur_x = up_start_x
    up_branch_attach_points = []
    for b in up_branches:
        p = b["person"]
        b_name = b["branch_name"]
        pt = place_upward_node(p, cur_x, 2, b_name)
        up_branch_attach_points.append(pt)
        cur_x += p["_span_w"] + H_GAP * 4

    # Align DOWNWARD branches horizontally centered
    down_start_x = (max_total_w - down_total_w) / 2 + 100
    cur_x = down_start_x
    down_branch_attach_points = []
    for b in down_branches:
        p = b["person"]
        b_name = b["branch_name"]
        pt = place_downward_node(p, cur_x, 2, b_name)
        down_branch_attach_points.append(pt)
        cur_x += p["_span_w"] + H_GAP * 4

    # Place Ibrahim in the exact horizontal middle at center_y
    root_cx = 100 + max_total_w / 2
    root_cy = center_y - 45 # Ibrahim card is 90px tall, centered vertically
    all_nodes.append({
        "id": root_node["id"],
        "name": root_node["name"],
        "role": "Osnivač loze Zehić",
        "dates": "Zajednički Predak",
        "gender": "M",
        "gen": 1,
        "branch": "root",
        "x": root_cx - CARD_W / 2,
        "y": root_cy,
        "w": CARD_W,
        "h": 90,
        "is_root": True
    })

    # Connect Ibrahim to UPWARD branches
    up_bus_y = root_cy - 35
    all_lines.append({
        "x1": root_cx, "y1": root_cy,
        "x2": root_cx, "y2": up_bus_y,
        "branch": "root"
    })
    for pt in up_branch_attach_points:
        all_lines.append({
            "x1": pt[0], "y1": up_bus_y,
            "x2": pt[0], "y2": pt[1],
            "branch": "root"
        })
    up_xs = [pt[0] for pt in up_branch_attach_points] + [root_cx]
    all_lines.append({
        "x1": min(up_xs), "y1": up_bus_y,
        "x2": max(up_xs), "y2": up_bus_y,
        "branch": "root"
    })

    # Connect Ibrahim to DOWNWARD branches
    down_bus_y = root_cy + 90 + 35
    all_lines.append({
        "x1": root_cx, "y1": root_cy + 90,
        "x2": root_cx, "y2": down_bus_y,
        "branch": "root"
    })
    for pt in down_branch_attach_points:
        all_lines.append({
            "x1": pt[0], "y1": down_bus_y,
            "x2": pt[0], "y2": pt[1],
            "branch": "root"
        })
    down_xs = [pt[0] for pt in down_branch_attach_points] + [root_cx]
    all_lines.append({
        "x1": min(down_xs), "y1": down_bus_y,
        "x2": max(down_xs), "y2": down_bus_y,
        "branch": "root"
    })

    # Coordinate boundaries
    raw_min_x = min(n["x"] for n in all_nodes) - 80
    raw_max_x = max(n["x"] + n["w"] for n in all_nodes) + 80
    raw_min_y = min(n["y"] for n in all_nodes) - 220 # Room for header/legend at top
    raw_max_y = max(n["y"] + n["h"] for n in all_nodes) + 120

    width = int(raw_max_x - raw_min_x)
    height = int(raw_max_y - raw_min_y)

    shift_x = -raw_min_x
    shift_y = -raw_min_y

    svg = []
    svg.append(f'''<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     x="0px" y="0px" width="{width}px" height="{height}px" viewBox="0 0 {width} {height}" 
     xml:space="preserve" style="font-family: 'Plus Jakarta Sans', 'Segoe UI', Arial, Helvetica, sans-serif;">

<rect x="0" y="0" width="{width}" height="{height}" fill="#F8FAFC" />

<!-- Header Gore Lijevo -->
<g transform="translate(60, 45)">
    <rect x="0" y="2" width="760" height="85" rx="18" fill="#E2E8F0" />
    <rect x="0" y="0" width="760" height="85" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />
    <text x="380" y="38" font-size="28" font-weight="900" fill="#0F172A" text-anchor="middle">PORODIČNO STABLO ZEHIĆ</text>
    <text x="380" y="66" font-size="15.5" font-weight="700" fill="#475569" text-anchor="middle">Ibrahim u Sredini • Grana Adem Gore ⬆ • Grane Osman &amp; Meho Dole ⬇</text>
</g>

<!-- Desna Legenda -->
<g transform="translate({width - 580}, 25)">
    <rect x="0" y="2" width="540" height="195" rx="16" fill="#E2E8F0" />
    <rect x="0" y="0" width="540" height="195" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />
    <text x="20" y="26" font-size="13" font-weight="800" fill="#1E293B">LEGENDA BOJA, GRANA &amp; OZNAKA</text>
    <line x1="20" y1="34" x2="520" y2="34" stroke="#E2E8F0" stroke-width="1.2" />

    <text x="20" y="52" font-size="11.5" font-weight="800" fill="#475569">PORODIČNE GRANE:</text>
    <circle cx="28" cy="70" r="6.5" fill="#16A34A" />
    <text x="42" y="74" font-size="12" font-weight="700" fill="#14532D">Grana Adem (177) ⬆</text>

    <circle cx="28" cy="94" r="6.5" fill="#0284C7" />
    <text x="42" y="98" font-size="12" font-weight="700" fill="#0C4A6E">Grana Osman (152) ⬇</text>

    <circle cx="28" cy="118" r="6.5" fill="#D97706" />
    <text x="42" y="122" font-size="12" font-weight="700" fill="#78350F">Grana Meho (69) ⬇</text>

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

    # Generation Axis Markers on Left Flank
    # Upward Generacija
    for g in range(2, 9):
        gy = center_y - (g - 1) * GEN_STEP_Y + shift_y - 20
        svg.append(f'''
<g transform="translate(50, {gy})">
    <rect x="0" y="-12" width="75" height="24" rx="12" fill="#16A34A" />
    <text x="37" y="4" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g} ⬆</text>
</g>''')

    # Center Ibrahim Gen 1
    root_gen_y = root_cy + 45 + shift_y
    svg.append(f'''
<g transform="translate(50, {root_gen_y})">
    <rect x="0" y="-14" width="75" height="28" rx="14" fill="#0F172A" />
    <text x="37" y="4" font-size="11" font-weight="900" fill="#93C5FD" text-anchor="middle">GEN. 1 👑</text>
</g>''')

    # Downward Generacija
    for g in range(2, 9):
        gy = center_y + (g - 1) * GEN_STEP_Y + shift_y + 20
        svg.append(f'''
<g transform="translate(50, {gy})">
    <rect x="0" y="-12" width="75" height="24" rx="12" fill="#0284C7" />
    <text x="37" y="4" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g} ⬇</text>
</g>''')

    # Render Lines
    for line in all_lines:
        b_theme = THEMES.get(line["branch"], THEMES["root"])
        stroke_color = b_theme.get("line", "#475569")
        x1 = line['x1'] + shift_x
        y1 = line['y1'] + shift_y
        x2 = line['x2'] + shift_x
        y2 = line['y2'] + shift_y
        svg.append(f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />''')

    # Render Cards
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

# Output files
up_down_svg = generate_up_down_tree()
with open("Porodicno_Stablo_Zehic_Gore_Dole.svg", "w", encoding="utf-8") as f:
    f.write(up_down_svg)

with open("public/Porodicno_Stablo_Zehic_Gore_Dole.svg", "w", encoding="utf-8") as f:
    f.write(up_down_svg)

print("Generated Porodicno_Stablo_Zehic_Gore_Dole.svg successfully!")

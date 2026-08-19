# -*- coding: utf-8 -*-
"""
Adobe Illustrator Compatible Horizontal Branch Generator
"""
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

CARD_W = 270
CARD_H = 56
CARD_H_COUPLE = 92
V_GAP = 14
COL_W = 324

MALE_TEXT_COLOR = "#1D4ED8"
MALE_AVATAR_BG = "#DBEAFE"
MALE_AVATAR_TEXT = "#1E40AF"

FEMALE_TEXT_COLOR = "#BE185D"
FEMALE_AVATAR_BG = "#FCE7F3"
FEMALE_AVATAR_TEXT = "#9D174D"

THEMES = {
    "Grana Adem": {
        "title": "GRANA ADEM (1855 – 1938)",
        "subtitle": "177 Članova • Potomstvo Adema i Mejre • Horizontalni Prikaz",
        "border": "#16A34A", "primary": "#15803D", "line": "#16A34A", "tag_bg": "#DCFCE7"
    },
    "Grana Meho": {
        "title": "GRANA MEHO (1867 – 1941)",
        "subtitle": "69 Članova • Potomstvo Mehe i Cure • Horizontalni Prikaz",
        "border": "#D97706", "primary": "#B45309", "line": "#D97706", "tag_bg": "#FEF3C7"
    },
    "Grana Osman": {
        "title": "GRANA OSMAN (1860 – 1937)",
        "subtitle": "152 Člana • Potomstvo Osmana i Hate • Horizontalni Prikaz",
        "border": "#0284C7", "primary": "#0369A1", "line": "#0284C7", "tag_bg": "#E0F2FE"
    }
}

class HorizontalBranchEngine:
    def __init__(self, data):
        self.data = data

    def compute_subtree_height(self, node):
        has_sp = "spouse" in node
        self_h = CARD_H_COUPLE if has_sp else CARD_H
        children = node.get("children", [])
        if not children:
            node["_span_h"] = self_h
            return self_h
        ch_heights = [self.compute_subtree_height(c) for c in children]
        total_ch_h = sum(ch_heights) + (len(children) - 1) * V_GAP
        node["_span_h"] = max(self_h, total_ch_h)
        return node["_span_h"]

    def layout_horizontal_branch(self, branch_person, branch_key):
        theme = THEMES[branch_key]
        self.compute_subtree_height(branch_person)

        total_h = branch_person["_span_h"]
        top_offset = 240
        start_x = 100
        start_y = top_offset

        all_nodes = []
        all_lines = []

        def place_node(node, col_idx, top_y):
            has_sp = "spouse" in node
            node_h = CARD_H_COUPLE if has_sp else CARD_H
            span_h = node["_span_h"]

            node_y = top_y + (span_h - node_h) / 2
            card_x = start_x + (col_idx - 1) * COL_W

            card_info = {
                "id": node.get("id"),
                "name": node.get("name"),
                "dates": node.get("dates", ""),
                "notes": node.get("notes", ""),
                "gender": node.get("gender", "M"),
                "spouse": node.get("spouse"),
                "gen": node.get("gen", 2),
                "x": card_x,
                "y": node_y,
                "w": CARD_W,
                "h": node_h,
                "has_spouse": has_sp
            }
            all_nodes.append(card_info)

            parent_in_x = card_x
            parent_out_x = card_x + CARD_W
            parent_center_y = node_y + node_h / 2

            children = node.get("children", [])
            if children:
                ch_cur_y = top_y
                child_attach_points = []
                bus_x = parent_out_x + (COL_W - CARD_W) / 2

                all_lines.append({
                    "type": "stem",
                    "x1": parent_out_x,
                    "y1": parent_center_y,
                    "x2": bus_x,
                    "y2": parent_center_y
                })

                for c in children:
                    c_span_h = c["_span_h"]
                    c_in_pt = place_node(c, col_idx + 1, ch_cur_y)
                    child_attach_points.append(c_in_pt)
                    all_lines.append({
                        "type": "stem",
                        "x1": bus_x,
                        "y1": c_in_pt[1],
                        "x2": c_in_pt[0],
                        "y2": c_in_pt[1]
                    })
                    ch_cur_y += c_span_h + V_GAP

                min_ch_y = min(p[1] for p in child_attach_points)
                max_ch_y = max(p[1] for p in child_attach_points)
                bus_top = min(parent_center_y, min_ch_y)
                bus_bottom = max(parent_center_y, max_ch_y)

                all_lines.append({
                    "type": "bus",
                    "x1": bus_x,
                    "y1": bus_top,
                    "x2": bus_x,
                    "y2": bus_bottom
                })

            return (parent_in_x, parent_center_y)

        place_node(branch_person, 1, start_y)

        raw_min_x = min(n["x"] for n in all_nodes) - 80
        raw_max_x = max(n["x"] + n["w"] for n in all_nodes) + 80
        raw_min_y = 0
        raw_max_y = max(n["y"] + n["h"] for n in all_nodes) + 100

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
''')

        # Header
        svg.append(f'''
<g transform="translate({width/2 - 180}, 45)">
    <rect x="-380" y="2" width="760" height="105" rx="18" fill="#E2E8F0" />
    <rect x="-380" y="0" width="760" height="105" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />
    <text x="0" y="44" font-size="28" font-weight="900" fill="#0F172A" text-anchor="middle">{theme['title']}</text>
    <text x="0" y="74" font-size="15" font-weight="700" fill="#475569" text-anchor="middle">{theme['subtitle']}</text>
</g>

<!-- Desna Legenda -->
<g transform="translate({width - 400}, 48)">
    <rect x="0" y="2" width="340" height="100" rx="14" fill="#E2E8F0" />
    <rect x="0" y="0" width="340" height="100" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" />
    <text x="16" y="24" font-size="12" font-weight="800" fill="#1E293B">LEGENDA OZNAKA</text>
    
    <rect x="16" y="38" width="13" height="13" rx="3" fill="#DBEAFE" stroke="#1D4ED8" stroke-width="1.5"/>
    <text x="36" y="49" font-size="11.5" font-weight="800" fill="#1D4ED8">Muško ime (Plava)</text>
    
    <rect x="16" y="66" width="13" height="13" rx="3" fill="#FCE7F3" stroke="#BE185D" stroke-width="1.5"/>
    <text x="36" y="77" font-size="11.5" font-weight="800" fill="#BE185D">Žensko ime (Roze)</text>

    <!-- Marriage Vector Icon -->
    <g transform="translate(180, 44)">
        <line x1="0" y1="0" x2="20" y2="0" stroke="#CBD5E1" stroke-width="1.5" />
        <circle cx="10" cy="0" r="7" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
        <text x="10" y="3" font-size="7.5" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>
        <text x="26" y="4" font-size="11.5" font-weight="700" fill="#475569">Brak</text>
    </g>

    <!-- Fallen Vector Badge -->
    <g transform="translate(180, 72)">
        <rect x="0" y="-7" width="56" height="15" rx="7.5" fill="#FEE2E2" stroke="#EF4444" stroke-width="1" />
        <text x="28" y="3" font-size="8" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>
        <text x="62" y="4" font-size="11.5" font-weight="600" fill="#64748B">Poginuo</text>
    </g>
</g>
''')

        # Generation Axis Markers
        axis_y = top_offset - 45
        max_gen = max(n.get("gen", 2) for n in all_nodes)
        for g in range(2, max_gen + 1):
            col_idx = g - 1
            gx = start_x + shift_x + (col_idx - 1) * COL_W + CARD_W / 2
            svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g}</text>
</g>''')

        # Lines
        for line in all_lines:
            x1 = line['x1'] + shift_x
            y1 = line['y1'] + shift_y
            x2 = line['x2'] + shift_x
            y2 = line['y2'] + shift_y
            svg.append(f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{theme['line']}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" />''')

        # Cards
        for n in all_nodes:
            x = n["x"] + shift_x
            y = n["y"] + shift_y
            w, h = n["w"], n["h"]
            name = n["name"]
            dates = n.get("dates", "")
            notes = n.get("notes", "")
            gender = n.get("gender", "M")
            is_male = (gender == "M")

            has_spouse = n.get("has_spouse", False)
            spouse = n.get("spouse")

            border_c = theme["border"]
            bar_c = theme["primary"]

            if not has_spouse:
                name_color = MALE_TEXT_COLOR if is_male else FEMALE_TEXT_COLOR
                av_bg = MALE_AVATAR_BG if is_male else FEMALE_AVATAR_BG
                av_text = MALE_AVATAR_TEXT if is_male else FEMALE_AVATAR_TEXT
                initial = name[0] if name else "?"
                badge = ""
                if "Pogin" in notes:
                    badge_text = "Poginula" if not is_male else "Poginuo"
                    badge_w = 80 if badge_text == "Poginula" else 72
                    badge = f'''<rect x="{w - badge_w - 6}" y="6" width="{badge_w}" height="20" rx="10" fill="#FEE2E2" stroke="#EF4444" stroke-width="1.2"/><text x="{w - badge_w/2 - 6}" y="20" font-size="11" font-weight="900" fill="#B91C1C" text-anchor="middle">{badge_text}</text>'''
                elif notes and notes not in ["Supruga", "Suprug"]:
                    clean_n = notes.replace("u. ", "u. ").replace("r. ", "r. ")
                    if len(clean_n) > 20:
                        clean_n = clean_n[:18] + "…"
                    badge = f'''<rect x="{w - 120}" y="6" width="114" height="20" rx="10" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1.2"/><text x="{w - 63}" y="20" font-size="10.5" font-weight="800" fill="#334155" text-anchor="middle">{clean_n}</text>'''

                svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="3" width="{w}" height="{h}" rx="12" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="{border_c}" stroke-width="2.5" />
    <path d="M 0 12 Q 0 0 12 0 L {w-12} 0 Q {w} 0 {w} 12 L {w} 5 L 0 5 Z" fill="{bar_c}" />
    
    <circle cx="26" cy="{h/2 + 2}" r="16" fill="{av_bg}" />
    <text x="26" y="{h/2 + 7.5}" font-size="14" font-weight="900" fill="{av_text}" text-anchor="middle">{initial}</text>
    
    {badge}
    
    <text x="52" y="31" font-size="20" font-weight="900" fill="{name_color}">{name}</text>
''')
                if dates:
                    svg.append(f'''<text x="52" y="48" font-size="12" font-weight="700" fill="#64748B">🗓 {dates}</text>''')
                elif notes and "Pogin" not in notes and notes not in ["Supruga", "Suprug"]:
                    display_n = notes
                    if len(display_n) > 22:
                        display_n = display_n[:20] + "…"
                    svg.append(f'''<text x="52" y="48" font-size="11.5" font-weight="700" fill="#64748B">{display_n}</text>''')
                svg.append('</g>\n')

            else:
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
                if "Pogin" in notes:
                    badge_text = "Poginula" if not is_male_p else "Poginuo"
                    badge_w = 80 if badge_text == "Poginula" else 72
                    badge = f'''<rect x="{w - badge_w - 6}" y="6" width="{badge_w}" height="20" rx="10" fill="#FEE2E2" stroke="#EF4444" stroke-width="1.2"/><text x="{w - badge_w/2 - 6}" y="20" font-size="11" font-weight="900" fill="#B91C1C" text-anchor="middle">{badge_text}</text>'''

                has_real_sp_note = sp_notes and sp_notes not in ["Supruga", "Suprug"]
                sp_y_name = 70 if not has_real_sp_note else 66

                svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="3" width="{w}" height="{h}" rx="14" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="#FFFFFF" stroke="{border_c}" stroke-width="2.5" />
    <path d="M 0 14 Q 0 0 14 0 L {w-14} 0 Q {w} 0 {w} 14 L {w} 5 L 0 5 Z" fill="{bar_c}" />

    <!-- Person Top Row -->
    <circle cx="24" cy="24" r="14" fill="{av_bg_p}" />
    <text x="24" y="29" font-size="13" font-weight="900" fill="{av_text_p}" text-anchor="middle">{initial_p}</text>
    <text x="46" y="30" font-size="19" font-weight="900" fill="{name_color_p}">{name}</text>
    {badge}
''')
                if dates:
                    svg.append(f'''<text x="46" y="42" font-size="11" font-weight="700" fill="#64748B">🗓 {dates}</text>''')

                # Dividing Line with Marriage Rings Symbol
                svg.append(f'''
    <line x1="12" y1="47" x2="{w-12}" y2="47" stroke="#E2E8F0" stroke-width="1.2" />
    <circle cx="{w/2}" cy="47" r="9" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
    <text x="{w/2}" y="51" font-size="10" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>

    <!-- Spouse Bottom Row -->
    <circle cx="24" cy="{sp_y_name + 2}" r="14" fill="{av_bg_s}" />
    <text x="24" y="{sp_y_name + 7}" font-size="13" font-weight="900" fill="{av_text_s}" text-anchor="middle">{initial_s}</text>
    <text x="46" y="{sp_y_name + 7}" font-size="19" font-weight="900" fill="{name_color_s}">{sp_name}</text>
''')
                if has_real_sp_note:
                    display_sp_note = sp_notes
                    if len(display_sp_note) > 24:
                        display_sp_note = display_sp_note[:22] + "…"
                    svg.append(f'''<text x="46" y="{sp_y_name + 20}" font-size="11.5" font-weight="700" fill="#64748B">{display_sp_note}</text>''')

                svg.append('</g>\n')

        svg.append('</svg>')
        return "".join(svg)

engine = HorizontalBranchEngine(raw_data)

for b in raw_data["root"]["children_branches"]:
    b_name = b["branch_name"]
    p = b["person"]
    if b_name in THEMES:
        svg_code = engine.layout_horizontal_branch(p, b_name)
        out_name = "Branche_Adem.svg" if "Adem" in b_name else ("Branche_Meho.svg" if "Meho" in b_name else "Branche_Osman.svg")
        with open(out_name, "w", encoding="utf-8") as f:
            f.write(svg_code)
        print(f"Generated 100% Illustrator Compatible {out_name}!")

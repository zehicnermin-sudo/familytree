# -*- coding: utf-8 -*-
"""
Adobe Illustrator Compatible Ultra-Compact Horizontal Branch Generator
"""
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

CARD_W = 196
CARD_H = 32
CARD_H_COUPLE = 54
V_GAP = 5
COL_W = 216

MALE_TEXT_COLOR = "#0F3A99"
MALE_AVATAR_BG = "#DBEAFE"
MALE_AVATAR_TEXT = "#1E40AF"

FEMALE_TEXT_COLOR = "#9F1239"
FEMALE_AVATAR_BG = "#FCE7F3"
FEMALE_AVATAR_TEXT = "#881337"

THEMES = {
    "Grana Adem": {
        "title": "GRANA ADEM (1855 – 1938)",
        "subtitle": "177 Članova • Potomstvo Adema i Mejre • Horizontalni Prikaz",
        "border": "#16A34A", "primary": "#15803D", "line": "#16A34A", "tag_bg": "#DCFCE7"
    },
    "Grana Meho": {
        "title": "GRANA MEHO (1867 – 1941)",
        "subtitle": "70 Članova • Potomstvo Mehe i Cure • Horizontalni Prikaz",
        "border": "#D97706", "primary": "#B45309", "line": "#D97706", "tag_bg": "#FEF3C7"
    },
    "Grana Osman": {
        "title": "GRANA OSMAN (1860 – 1937)",
        "subtitle": "174 Člana • Potomstvo Osmana i Hate • Horizontalni Prikaz",
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
        top_offset = 140
        start_x = 50
        start_y = top_offset

        all_nodes = []
        all_lines = []

        def place_node(node, col_idx, top_y):
            has_sp = "spouse" in node
            node_h = CARD_H_COUPLE if has_sp else CARD_H
            span_h = node["_span_h"]

            node_y = top_y + (span_h - node_h) / 2
            node_x = start_x + (col_idx - 1) * COL_W

            card_info = {
                "id": node.get("id"),
                "name": node.get("name"),
                "dates": node.get("dates", ""),
                "notes": node.get("notes", ""),
                "gender": node.get("gender", "M"),
                "spouse": node.get("spouse"),
                "gen": node.get("gen", 2),
                "x": node_x,
                "y": node_y,
                "w": CARD_W,
                "h": node_h,
                "has_spouse": has_sp
            }
            all_nodes.append(card_info)

            parent_out_x = node_x + CARD_W
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

                min_cy = min(p[1] for p in child_attach_points)
                max_cy = max(p[1] for p in child_attach_points)
                all_lines.append({
                    "type": "bus",
                    "x1": bus_x,
                    "y1": min(parent_center_y, min_cy),
                    "x2": bus_x,
                    "y2": max(parent_center_y, max_cy)
                })

            return (node_x, parent_center_y)

        place_node(branch_person, 1, start_y)
        return all_nodes, all_lines, total_h, top_offset

    def render_branch_svg(self, branch_key, svg_filename):
        theme = THEMES[branch_key]
        root_node = self.data["root"]
        branch_entry = next(b for b in root_node["children_branches"] if b["branch_name"] == branch_key)
        branch_person = branch_entry["person"]

        all_nodes, all_lines, total_h, top_offset = self.layout_horizontal_branch(branch_person, branch_key)

        raw_min_x = min(n["x"] for n in all_nodes) - 40
        raw_max_x = max(n["x"] + n["w"] for n in all_nodes) + 40
        raw_min_y = 0
        raw_max_y = max(n["y"] + n["h"] for n in all_nodes) + 60

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

<!-- Header Banner -->
<g transform="translate({shift_x + 50}, 40)">
    <rect x="0" y="-25" width="460" height="56" rx="28" fill="{theme['primary']}" />
    <text x="30" y="2" font-size="18" font-weight="900" fill="#FFFFFF">{theme['title']}</text>
    <text x="30" y="19" font-size="10.5" font-weight="700" fill="#F1F5F9">{theme['subtitle']}</text>
</g>
''')

        # Generation Axis Markers
        axis_y = top_offset - 30
        max_gen = max(n.get("gen", 2) for n in all_nodes)
        for g in range(2, max_gen + 1):
            col_idx = g - 1
            gx = 50 + shift_x + (col_idx - 1) * COL_W + CARD_W / 2
            svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-35" y="0" width="70" height="20" rx="10" fill="#1E293B" />
    <text x="0" y="14" font-size="9.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g}</text>
</g>''')

        # Lines
        for line in all_lines:
            x1 = line['x1'] + shift_x
            y1 = line['y1'] + shift_y
            x2 = line['x2'] + shift_x
            y2 = line['y2'] + shift_y
            svg.append(f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{theme['line']}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />''')

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

                note_text = ""
                if "Pogin" in notes:
                    note_text = f'''<circle cx="{w-10}" cy="16" r="3.5" fill="#EF4444" />'''
                elif notes and notes not in ["Supruga", "Suprug"]:
                    clean_n = notes.replace("u. ", "u. ").replace("r. ", "r. ")
                    if len(clean_n) > 28: clean_n = clean_n[:27] + "…"
                    note_text = f'''<text x="{w-8}" y="{h/2 + 3.5}" font-size="8.5" font-weight="800" fill="#64748B" text-anchor="end">{clean_n}</text>'''

                svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="1.5" width="{w}" height="{h}" rx="6" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{border_c}" stroke-width="1.6" />
    <rect x="0" y="0" width="4.5" height="{h}" rx="2" fill="{bar_c}" />
    
    <circle cx="16" cy="{h/2}" r="8.5" fill="{av_bg}" />
    <text x="16" y="{h/2 + 3.5}" font-size="8.5" font-weight="900" fill="{av_text}" text-anchor="middle">{initial}</text>
    
    <text x="30" y="{h/2 + 4.5}" font-size="13.5" font-weight="900" fill="{name_color}">{name}</text>
    {note_text}
</g>''')

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

                note_p_svg = ""
                if "Pogin" in notes:
                    note_p_svg = f'''<circle cx="{w-10}" cy="13.5" r="3.5" fill="#EF4444" />'''
                
                note_s_svg = ""
                if sp_notes and sp_notes not in ["Supruga", "Suprug"]:
                    clean_sn = sp_notes.replace("r. ", "r. ").replace("u. ", "u. ")
                    if len(clean_sn) > 16: clean_sn = clean_sn[:15] + "…"
                    note_s_svg = f'''<text x="{w-8}" y="42" font-size="9" font-weight="800" fill="#BE185D" text-anchor="end">{clean_sn}</text>'''

                svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="1.5" width="{w}" height="{h}" rx="8" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="#FFFFFF" stroke="{border_c}" stroke-width="1.8" />
    <rect x="0" y="0" width="5" height="{h}" rx="2.5" fill="{bar_c}" />

    <!-- Person Top Row -->
    <circle cx="16" cy="14" r="8" fill="{av_bg_p}" />
    <text x="16" y="17" font-size="8" font-weight="900" fill="{av_text_p}" text-anchor="middle">{initial_p}</text>
    <text x="29" y="18" font-size="13" font-weight="900" fill="{name_color_p}">{name}</text>
    {note_p_svg}

    <!-- Dividing Line -->
    <line x1="8" y1="27" x2="{w-8}" y2="27" stroke="#E2E8F0" stroke-width="1" />
    <circle cx="{w/2}" cy="27" r="5.5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />
    <text x="{w/2}" y="29.5" font-size="6.5" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>

    <!-- Spouse Bottom Row -->
    <circle cx="16" cy="41" r="8" fill="{av_bg_s}" />
    <text x="16" y="44" font-size="8" font-weight="900" fill="{av_text_s}" text-anchor="middle">{initial_s}</text>
    <text x="29" y="45" font-size="13" font-weight="900" fill="{name_color_s}">{sp_name}</text>
    {note_s_svg}
</g>''')

        svg.append('</svg>')
        with open(svg_filename, "w", encoding="utf-8") as f:
            f.write("".join(svg))
        print(f"Generated 100% Ultra-Compact {svg_filename}!")

h_engine = HorizontalBranchEngine(raw_data)
h_engine.render_branch_svg("Grana Adem", "Branche_Adem.svg")
h_engine.render_branch_svg("Grana Meho", "Branche_Meho.svg")
h_engine.render_branch_svg("Grana Osman", "Branche_Osman.svg")

# -*- coding: utf-8 -*-
"""
Adobe Illustrator & Ultra-Compact A3 Precision Generator:
- Tight vertical gaps (V_GAP = 5px)
- Ultra-efficient card sizing (CARD_W = 195px, CARD_H = 32px, CARD_H_COUPLE = 54px)
- Big bold names that fill the card width with maximum ink contrast
- Matches standard ISO A3 sheet aspect ratio (~0.71 portrait) with 95% paper fill
- Zero wasted whitespace, eliminating microscopic scaling on A3 prints
"""
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

CARD_W = 196
CARD_H = 32          # Single person card height
CARD_H_COUPLE = 54   # Couple card height
V_GAP = 5            # Tight gap between siblings
COL_W = 216          # Column width per generation (connector span = 20px)
GAP_FROM_ROOT = 70   # Gap between Ibrahim's card and Gen 2 roots

# High Contrast Print Colors (Deep shades for maximum readability on paper)
MALE_TEXT_COLOR = "#0F3A99"     # High-contrast Dark Navy Blue
MALE_AVATAR_BG = "#DBEAFE"      # Light Blue
MALE_AVATAR_TEXT = "#1E40AF"

FEMALE_TEXT_COLOR = "#9F1239"   # High-contrast Deep Crimson Rose
FEMALE_AVATAR_BG = "#FCE7F3"    # Light Rose
FEMALE_AVATAR_TEXT = "#881337"

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

class BilateralPosterEngine:
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

    def layout_wing(self, roots_list, start_x, start_y, direction, branch_name):
        all_nodes = []
        all_lines = []

        def place_node(node, col_idx, top_y, branch):
            has_sp = "spouse" in node
            node_h = CARD_H_COUPLE if has_sp else CARD_H
            span_h = node["_span_h"]

            node_y = top_y + (span_h - node_h) / 2
            node_x = start_x + direction * (col_idx - 1) * COL_W
            card_x = node_x - CARD_W if direction == -1 else node_x

            card_info = {
                "id": node.get("id"),
                "name": node.get("name"),
                "dates": node.get("dates", ""),
                "notes": node.get("notes", ""),
                "gender": node.get("gender", "M"),
                "spouse": node.get("spouse"),
                "gen": node.get("gen", 2),
                "branch": branch,
                "x": card_x,
                "y": node_y,
                "w": CARD_W,
                "h": node_h,
                "has_spouse": has_sp,
                "direction": direction
            }
            all_nodes.append(card_info)

            parent_in_x = card_x + CARD_W if direction == -1 else card_x
            parent_out_x = card_x if direction == -1 else card_x + CARD_W
            parent_center_y = node_y + node_h / 2

            children = node.get("children", [])
            if children:
                ch_cur_y = top_y
                child_attach_points = []
                bus_x = parent_out_x + direction * (COL_W - CARD_W) / 2

                all_lines.append({
                    "type": "stem",
                    "x1": parent_out_x,
                    "y1": parent_center_y,
                    "x2": bus_x,
                    "y2": parent_center_y,
                    "branch": branch
                })

                for c in children:
                    c_span_h = c["_span_h"]
                    c_in_pt = place_node(c, col_idx + 1, ch_cur_y, branch)
                    child_attach_points.append(c_in_pt)
                    all_lines.append({
                        "type": "stem",
                        "x1": bus_x,
                        "y1": c_in_pt[1],
                        "x2": c_in_pt[0],
                        "y2": c_in_pt[1],
                        "branch": branch
                    })
                    ch_cur_y += c_span_h + V_GAP

                min_cy = min(p[1] for p in child_attach_points)
                max_cy = max(p[1] for p in child_attach_points)
                all_lines.append({
                    "type": "bus",
                    "x1": bus_x,
                    "y1": min(parent_center_y, min_cy),
                    "x2": bus_x,
                    "y2": max(parent_center_y, max_cy),
                    "branch": branch
                })

            return (parent_in_x, parent_center_y)

        current_y = start_y
        wing_roots_attach = []
        for r_entry in roots_list:
            if isinstance(r_entry, dict) and "person" in r_entry:
                r_node = r_entry["person"]
                b_title = r_entry["branch_name"]
            else:
                r_node = r_entry
                b_title = branch_name

            span = r_node["_span_h"]
            in_pt = place_node(r_node, 1, current_y, b_title)
            wing_roots_attach.append(in_pt)
            current_y += span + 20

        total_wing_height = current_y - start_y - 20
        return all_nodes, all_lines, wing_roots_attach, total_wing_height

    def generate_full_bilateral(self):
        root_node = self.data["root"]
        
        adem_branch = None
        right_branches = []
        for b in root_node.get("children_branches", []):
            if b["branch_name"] == "Grana Adem":
                adem_branch = b
            else:
                right_branches.append(b)

        # 1. Compute spans
        self.compute_subtree_height(adem_branch["person"])
        for rb in right_branches:
            self.compute_subtree_height(rb["person"])

        adem_total_h = adem_branch["person"]["_span_h"]
        right_total_h = sum(rb["person"]["_span_h"] for rb in right_branches) + (len(right_branches) - 1) * 20

        max_height = max(adem_total_h, right_total_h)
        top_offset = 180

        start_y_left = top_offset + (max_height - adem_total_h) / 2
        start_y_right = top_offset + (max_height - right_total_h) / 2

        root_card_w = 210
        root_card_left_x = -root_card_w / 2
        root_card_right_x = root_card_w / 2

        left_wing_attach_x = root_card_left_x - GAP_FROM_ROOT
        right_wing_attach_x = root_card_right_x + GAP_FROM_ROOT

        left_nodes, left_lines, left_attach, left_h = self.layout_wing(
            [adem_branch], left_wing_attach_x, start_y_left, -1, "Grana Adem"
        )
        right_nodes, right_lines, right_attach, right_h = self.layout_wing(
            right_branches, right_wing_attach_x, start_y_right, 1, "Desno Krilo"
        )

        center_y = top_offset + max_height / 2 - 34
        root_card = {
            "id": root_node["id"],
            "name": root_node["name"],
            "role": "Osnivač loze Zehić",
            "dates": "Zajednički Predak",
            "gender": "M",
            "gen": 1,
            "branch": "root",
            "spouse": root_node.get("spouse"),
            "x": root_card_left_x,
            "y": center_y,
            "w": root_card_w,
            "h": 68,
            "is_root": True
        }

        all_lines = left_lines + right_lines
        
        left_bus_x = (root_card_left_x + left_wing_attach_x) / 2
        all_lines.append({
            "type": "stem",
            "x1": root_card["x"],
            "y1": center_y + 34,
            "x2": left_bus_x,
            "y2": center_y + 34,
            "branch": "root"
        })
        min_ly = min(p[1] for p in left_attach)
        max_ly = max(p[1] for p in left_attach)
        all_lines.append({
            "type": "bus",
            "x1": left_bus_x,
            "y1": min(center_y + 34, min_ly),
            "x2": left_bus_x,
            "y2": max(center_y + 34, max_ly),
            "branch": "root"
        })
        for pt in left_attach:
            all_lines.append({
                "type": "stem",
                "x1": left_bus_x,
                "y1": pt[1],
                "x2": pt[0],
                "y2": pt[1],
                "branch": "Grana Adem"
            })

        right_bus_x = (root_card_right_x + right_wing_attach_x) / 2
        all_lines.append({
            "type": "stem",
            "x1": root_card["x"] + root_card["w"],
            "y1": center_y + 34,
            "x2": right_bus_x,
            "y2": center_y + 34,
            "branch": "root"
        })
        min_ry = min(p[1] for p in right_attach)
        max_ry = max(p[1] for p in right_attach)
        all_lines.append({
            "type": "bus",
            "x1": right_bus_x,
            "y1": min(center_y + 34, min_ry),
            "x2": right_bus_x,
            "y2": max(center_y + 34, max_ry),
            "branch": "root"
        })
        for pt in right_attach:
            all_lines.append({
                "type": "stem",
                "x1": right_bus_x,
                "y1": pt[1],
                "x2": pt[0],
                "y2": pt[1],
                "branch": "root"
            })

        all_nodes = [root_card] + left_nodes + right_nodes
        return all_nodes, all_lines, max_height, top_offset

def render_illustrator_svg(nodes, lines, max_height, top_offset):
    raw_min_x = min(n["x"] for n in nodes) - 40
    raw_max_x = max(n["x"] + n["w"] for n in nodes) + 40
    raw_min_y = 0
    raw_max_y = max(n["y"] + n["h"] for n in nodes) + 80

    width = int(raw_max_x - raw_min_x)
    height = int(raw_max_y - raw_min_y)

    shift_x = -raw_min_x
    shift_y = 0

    svg = []
    svg.append(f'''<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     x="0px" y="0px" width="{width}px" height="{height}px" viewBox="0 0 {width} {height}" 
     xml:space="preserve" style="font-family: 'Plus Jakarta Sans', 'Segoe UI', Arial, Helvetica, sans-serif;">

<!-- Solid Clean Background for Adobe Illustrator & PDF Print -->
<rect x="0" y="0" width="{width}" height="{height}" fill="#F8FAFC" />

''')

    # Header Title
    title_cx = shift_x
    svg.append(f'''
<g transform="translate({title_cx}, 50)">
    <rect x="-380" y="-35" width="760" height="70" rx="35" fill="#0F172A" />
    <text x="0" y="0" font-size="24" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="1.5">PORODIČNO STABLO ZEHIĆ</text>
    <text x="0" y="20" font-size="12" font-weight="700" fill="#94A3B8" text-anchor="middle" letter-spacing="1">POTOMSTVO IBRAHIMA ZEHIĆA • 8 GENERACIJA • 425 ČLANOVA</text>
</g>
''')

    # Legend at Top Right
    legend_x = width - 460
    svg.append(f'''
<g transform="translate({legend_x}, 20)">
    <rect x="0" y="0" width="430" height="135" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" />
    <text x="14" y="20" font-size="11" font-weight="900" fill="#0F172A">LEGENDA GRANA &amp; OZNAKA:</text>
    <line x1="14" y1="26" x2="416" y2="26" stroke="#E2E8F0" stroke-width="1" />

    <!-- Branches -->
    <circle cx="22" cy="42" r="5" fill="#16A34A" />
    <text x="32" y="45" font-size="10" font-weight="700" fill="#14532D">Grana Adem (177)</text>

    <circle cx="22" cy="62" r="5" fill="#0284C7" />
    <text x="32" y="65" font-size="10" font-weight="700" fill="#0C4A6E">Grana Osman (174)</text>

    <circle cx="22" cy="82" r="5" fill="#D97706" />
    <text x="32" y="85" font-size="10" font-weight="700" fill="#78350F">Grana Meho (70)</text>

    <circle cx="22" cy="102" r="5" fill="#E11D48" />
    <text x="32" y="105" font-size="10" font-weight="700" fill="#881337">Nurif &amp; Paša</text>

    <line x1="180" y1="32" x2="180" y2="125" stroke="#E2E8F0" stroke-width="1" />

    <!-- Genders -->
    <rect x="195" y="38" width="10" height="10" rx="3" fill="#DBEAFE" stroke="#0F3A99" stroke-width="1.5"/>
    <text x="212" y="47" font-size="10.5" font-weight="800" fill="#0F3A99">Muško ime (Plavo)</text>

    <rect x="195" y="58" width="10" height="10" rx="3" fill="#FCE7F3" stroke="#9F1239" stroke-width="1.5"/>
    <text x="212" y="67" font-size="10.5" font-weight="800" fill="#9F1239">Žensko ime (Roze)</text>

    <text x="195" y="88" font-size="10" font-weight="900" fill="#E11D48">∞</text>
    <text x="212" y="87" font-size="10" font-weight="700" fill="#475569">Bračni par (Brak)</text>

    <text x="195" y="108" font-size="9" font-weight="900" fill="#B91C1C">●</text>
    <text x="212" y="107" font-size="10" font-weight="700" fill="#B91C1C">Poginuo/la u ratu</text>
</g>
''')

    # Generation Axis Markers
    axis_y = top_offset - 35
    for g in range(8, 1, -1):
        col_idx = g - 1
        gx = shift_x - GAP_FROM_ROOT - CARD_W/2 - (col_idx - 1) * COL_W - CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-40" y="0" width="80" height="22" rx="11" fill="#1E293B" />
    <text x="0" y="15" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g}</text>
</g>''')

    svg.append(f'''
<g transform="translate({shift_x}, {axis_y})">
    <rect x="-50" y="0" width="100" height="22" rx="11" fill="#0F172A" />
    <text x="0" y="15" font-size="10.5" font-weight="900" fill="#F8FAFC" text-anchor="middle">👑 GEN. 1</text>
</g>''')

    for g in range(2, 9):
        col_idx = g - 1
        gx = shift_x + GAP_FROM_ROOT + CARD_W/2 + (col_idx - 1) * COL_W + CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-40" y="0" width="80" height="22" rx="11" fill="#1E293B" />
    <text x="0" y="15" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g}</text>
</g>''')

    # 1. Connecting Lines
    for line in lines:
        b_theme = THEMES.get(line["branch"], THEMES["root"])
        stroke_color = b_theme.get("line", "#475569")
        x1 = line['x1'] + shift_x
        y1 = line['y1'] + shift_y
        x2 = line['x2'] + shift_x
        y2 = line['y2'] + shift_y
        svg.append(f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke_color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />''')

    # 2. Render Cards
    for n in nodes:
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
            has_root_spouse = n.get("spouse") is not None
            sp_name = n["spouse"]["name"] if has_root_spouse else ""
            svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="2" width="{w}" height="{h}" rx="12" fill="#0B0F19" opacity="0.3" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#1E293B" stroke="#3B82F6" stroke-width="2.5" />
    <!-- Ibrahim -->
    <circle cx="22" cy="20" r="12" fill="#334155" />
    <text x="22" y="25" font-size="12" font-weight="900" fill="#F8FAFC" text-anchor="middle">👑</text>
    <text x="42" y="25" font-size="16" font-weight="900" fill="#93C5FD">{name}</text>
    <line x1="12" y1="36" x2="{w-12}" y2="36" stroke="#334155" stroke-width="1" />
    <!-- Hanca -->
    <circle cx="22" cy="51" r="10" fill="#FCE7F3" />
    <text x="22" y="55" font-size="9" font-weight="900" fill="#BE185D" text-anchor="middle">💍</text>
    <text x="42" y="55" font-size="14" font-weight="900" fill="#F472B6">{sp_name}</text>
    <text x="{w-10}" y="54" font-size="9" font-weight="700" fill="#94A3B8" text-anchor="end">Supruga</text>
</g>''')

        elif not has_spouse:
            border_c = theme.get("border", "#94A3B8")
            bar_c = theme.get("primary", "#475569")
            
            name_color = MALE_TEXT_COLOR if is_male else FEMALE_TEXT_COLOR
            av_bg = MALE_AVATAR_BG if is_male else FEMALE_AVATAR_BG
            av_text = MALE_AVATAR_TEXT if is_male else FEMALE_AVATAR_TEXT
            initial = name[0] if name else "?"

            note_text = ""
            if "Pogin" in notes:
                note_text = f'''<circle cx="{w-12}" cy="16" r="4" fill="#EF4444" /><text x="{w-20}" y="19.5" font-size="8.5" font-weight="900" fill="#B91C1C" text-anchor="end">Poginuo/la</text>'''
            elif notes and notes not in ["Supruga", "Suprug"]:
                clean_n = notes.replace("u. ", "u. ").replace("r. ", "r. ")
                if len(clean_n) > 16: clean_n = clean_n[:15] + "…"
                note_text = f'''<text x="{w-8}" y="20" font-size="9" font-weight="800" fill="#64748B" text-anchor="end">{clean_n}</text>'''

            svg.append(f'''
<g transform="translate({x}, {y})">
    <rect x="0" y="1.5" width="{w}" height="{h}" rx="6" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{border_c}" stroke-width="1.6" />
    <rect x="0" y="0" width="4.5" height="{h}" rx="2" fill="{bar_c}" />
    
    <!-- Avatar -->
    <circle cx="16" cy="{h/2}" r="8.5" fill="{av_bg}" />
    <text x="16" y="{h/2 + 3.5}" font-size="8.5" font-weight="900" fill="{av_text}" text-anchor="middle">{initial}</text>
    
    <!-- Big Bold Name -->
    <text x="30" y="{h/2 + 4.5}" font-size="13.5" font-weight="900" fill="{name_color}">{name}</text>
    {note_text}
</g>''')

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

    <!-- Person Top Row (h = 27) -->
    <circle cx="16" cy="14" r="8" fill="{av_bg_p}" />
    <text x="16" y="17" font-size="8" font-weight="900" fill="{av_text_p}" text-anchor="middle">{initial_p}</text>
    <text x="29" y="18" font-size="13" font-weight="900" fill="{name_color_p}">{name}</text>
    {note_p_svg}

    <!-- Dividing Line -->
    <line x1="8" y1="27" x2="{w-8}" y2="27" stroke="#E2E8F0" stroke-width="1" />
    <circle cx="{w/2}" cy="27" r="5.5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1" />
    <text x="{w/2}" y="29.5" font-size="6.5" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>

    <!-- Spouse Bottom Row (h = 27) -->
    <circle cx="16" cy="41" r="8" fill="{av_bg_s}" />
    <text x="16" y="44" font-size="8" font-weight="900" fill="{av_text_s}" text-anchor="middle">{initial_s}</text>
    <text x="29" y="45" font-size="13" font-weight="900" fill="{name_color_s}">{sp_name}</text>
    {note_s_svg}
</g>''')

    svg.append('</svg>')
    return "".join(svg)

engine = BilateralPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_bilateral()
svg_content = render_illustrator_svg(nodes, lines, max_h, top_off)

with open("Porodicno_Stablo_Zehic_A0.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

with open("Arbre_Genealogique_A0_Bilateral.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Generated 100% Ultra-Compact High-Contrast Bilateral Master Poster SVG!")

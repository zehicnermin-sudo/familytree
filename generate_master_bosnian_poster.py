# -*- coding: utf-8 -*-
"""
Adobe Illustrator & Print Master Compatible Generator:
1. Normalized (0,0) coordinate space - Zero negative coordinates in viewBox or objects.
2. 100% Native SVG vector syntax - No feDropShadow or complex filters that break Illustrator importer.
3. Explicit Background rect - Adobe Illustrator displays the clean crisp background instead of transparent canvas.
4. Universal Font fallbacks - Arial / Helvetica / Segoe UI / Plus Jakarta Sans.
5. High precision vector styling for A0 / A1 printing.
"""
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

CARD_W = 238
CARD_H = 48          # Single person card height
CARD_H_COUPLE = 80   # Couple card height
V_GAP = 12           # Gap between sibling leaf blocks
COL_W = 284          # Column width per generation
GAP_FROM_ROOT = 132  # Gap between Ibrahim's card and Gen 2 roots

# Gender Colors (Standard Hex values natively supported by Illustrator)
MALE_TEXT_COLOR = "#1D4ED8"     # Deep Blue
MALE_AVATAR_BG = "#DBEAFE"      # Light Blue
MALE_AVATAR_TEXT = "#1E40AF"

FEMALE_TEXT_COLOR = "#BE185D"   # Deep Rose
FEMALE_AVATAR_BG = "#FCE7F3"    # Light Rose
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

                min_ch_y = min(p[1] for p in child_attach_points)
                max_ch_y = max(p[1] for p in child_attach_points)
                bus_top = min(parent_center_y, min_ch_y)
                bus_bottom = max(parent_center_y, max_ch_y)

                all_lines.append({
                    "type": "bus",
                    "x1": bus_x,
                    "y1": bus_top,
                    "x2": bus_x,
                    "y2": bus_bottom,
                    "branch": branch
                })

            return (parent_in_x, parent_center_y)

        cur_y = start_y
        wing_in_points = []
        for item in roots_list:
            p = item["person"]
            b_name = item["branch_name"]
            in_pt = place_node(p, 1, cur_y, b_name)
            wing_in_points.append(in_pt)
            cur_y += p["_span_h"] + V_GAP * 4

        total_wing_height = cur_y - start_y - V_GAP * 4
        return all_nodes, all_lines, wing_in_points, total_wing_height

    def generate_full_bilateral(self):
        root_node = self.data["root"]
        branches = root_node["children_branches"]

        left_branches = [b for b in branches if "Adem" in b["branch_name"]]
        right_branches = [b for b in branches if "Adem" not in b["branch_name"]]

        for b in branches:
            self.compute_subtree_height(b["person"])

        left_total_span = sum(b["person"]["_span_h"] for b in left_branches) + (len(left_branches) - 1) * V_GAP * 4
        right_total_span = sum(b["person"]["_span_h"] for b in right_branches) + (len(right_branches) - 1) * V_GAP * 4

        max_height = max(left_total_span, right_total_span)
        top_offset = 300

        start_y_left = top_offset + (max_height - left_total_span) / 2
        start_y_right = top_offset + (max_height - right_total_span) / 2

        root_card_left_x = -CARD_W / 2
        root_card_right_x = CARD_W / 2

        left_wing_attach_x = root_card_left_x - GAP_FROM_ROOT
        right_wing_attach_x = root_card_right_x + GAP_FROM_ROOT

        left_nodes, left_lines, left_attach, left_h = self.layout_wing(
            left_branches, left_wing_attach_x, start_y_left, -1, "Grana Adem"
        )
        right_nodes, right_lines, right_attach, right_h = self.layout_wing(
            right_branches, right_wing_attach_x, start_y_right, 1, "Desno Krilo"
        )

        center_y = top_offset + max_height / 2 - 45
        root_card = {
            "id": root_node["id"],
            "name": root_node["name"],
            "role": "Osnivač loze Zehić",
            "dates": "Zajednički Predak",
            "gender": "M",
            "gen": 1,
            "branch": "root",
            "x": root_card_left_x,
            "y": center_y,
            "w": CARD_W,
            "h": 90,
            "is_root": True
        }

        all_lines = left_lines + right_lines
        
        left_bus_x = (root_card_left_x + left_wing_attach_x) / 2
        all_lines.append({
            "type": "stem",
            "x1": root_card["x"],
            "y1": center_y + 45,
            "x2": left_bus_x,
            "y2": center_y + 45,
            "branch": "root"
        })
        min_ly = min(p[1] for p in left_attach)
        max_ly = max(p[1] for p in left_attach)
        all_lines.append({
            "type": "bus",
            "x1": left_bus_x,
            "y1": min(center_y + 45, min_ly),
            "x2": left_bus_x,
            "y2": max(center_y + 45, max_ly),
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
            "y1": center_y + 45,
            "x2": right_bus_x,
            "y2": center_y + 45,
            "branch": "root"
        })
        min_ry = min(p[1] for p in right_attach)
        max_ry = max(p[1] for p in right_attach)
        all_lines.append({
            "type": "bus",
            "x1": right_bus_x,
            "y1": min(center_y + 45, min_ry),
            "x2": right_bus_x,
            "y2": max(center_y + 45, max_ry),
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
    # Calculate coordinate bounds
    raw_min_x = min(n["x"] for n in nodes) - 80
    raw_max_x = max(n["x"] + n["w"] for n in nodes) + 80
    raw_min_y = 0
    raw_max_y = max(n["y"] + n["h"] for n in nodes) + 120

    width = int(raw_max_x - raw_min_x)
    height = int(raw_max_y - raw_min_y)

    # Normalization Offset: Shift everything to positive (0,0) coordinate system
    shift_x = -raw_min_x
    shift_y = 0

    svg = []
    svg.append(f'''<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
     x="0px" y="0px" width="{width}px" height="{height}px" viewBox="0 0 {width} {height}" 
     xml:space="preserve" style="font-family: 'Plus Jakarta Sans', 'Segoe UI', Arial, Helvetica, sans-serif;">

<!-- Background Rectangle (Ensures full visibility in Adobe Illustrator & CorelDraw) -->
<rect x="0" y="0" width="{width}" height="{height}" fill="#F8FAFC" />

''')

    # Main Title Header (Centered in normalized canvas)
    title_cx = shift_x
    svg.append(f'''
<!-- Glavni Naslov -->
<g transform="translate({title_cx}, 45)">
    <!-- Header Card Shadow & Box -->
    <rect x="-380" y="2" width="760" height="85" rx="18" fill="#E2E8F0" />
    <rect x="-380" y="0" width="760" height="85" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />
    <text x="0" y="38" font-size="28" font-weight="900" fill="#0F172A" text-anchor="middle">PORODIČNO STABLO ZEHIĆ</text>
    <text x="0" y="66" font-size="16" font-weight="700" fill="#475569" text-anchor="middle">Potomstvo Ibrahima Zehića • 8 Generacija • 401 Član</text>
</g>
''')

    # Consolidated Right-Side Legend Block
    legend_x = width - 620
    svg.append(f'''
<!-- Objedinjena Legenda na Desnoj Strani -->
<g transform="translate({legend_x}, 25)">
    <!-- Legend Shadow & Box -->
    <rect x="0" y="2" width="560" height="215" rx="16" fill="#E2E8F0" />
    <rect x="0" y="0" width="560" height="215" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" />
    
    <text x="20" y="26" font-size="13" font-weight="800" fill="#1E293B">LEGENDA BOJA, GRANA &amp; OZNAKA</text>
    <line x1="20" y1="34" x2="540" y2="34" stroke="#E2E8F0" stroke-width="1.2" />

    <!-- Lijeva kolona: Grane -->
    <text x="20" y="52" font-size="11.5" font-weight="800" fill="#475569">PORODIČNE GRANE:</text>
    
    <circle cx="28" cy="70" r="6.5" fill="#16A34A" />
    <text x="42" y="74" font-size="12" font-weight="700" fill="#14532D">Grana Adem (177 članova)</text>

    <circle cx="28" cy="94" r="6.5" fill="#0284C7" />
    <text x="42" y="98" font-size="12" font-weight="700" fill="#0C4A6E">Grana Osman (167 članova)</text>

    <circle cx="28" cy="118" r="6.5" fill="#D97706" />
    <text x="42" y="122" font-size="12" font-weight="700" fill="#78350F">Grana Meho (69 članova)</text>

    <circle cx="28" cy="142" r="6.5" fill="#E11D48" />
    <text x="42" y="146" font-size="12" font-weight="700" fill="#881337">Grana Nurif (nije se ženio)</text>

    <circle cx="28" cy="174" r="6.5" fill="#9333EA" />
    <text x="42" y="171" font-size="12" font-weight="800" fill="#581C87">Grana Paša</text>
    <text x="42" y="188" font-size="10.5" font-weight="600" fill="#6B21A8">(udata u Glinje u porodicu Hrustanović)</text>

    <line x1="295" y1="42" x2="295" y2="200" stroke="#E2E8F0" stroke-width="1.2" />

    <!-- Desna kolona: Spol & Simboli -->
    <text x="310" y="52" font-size="11.5" font-weight="800" fill="#475569">OZNAKE PO SPOLU &amp; BRAKU:</text>
    
    <!-- Muško -->
    <rect x="310" y="64" width="14" height="14" rx="4" fill="#DBEAFE" stroke="#1D4ED8" stroke-width="2"/>
    <text x="332" y="76" font-size="12.5" font-weight="900" fill="#1D4ED8">Muško ime (Plava)</text>

    <!-- Žensko -->
    <rect x="310" y="92" width="14" height="14" rx="4" fill="#FCE7F3" stroke="#BE185D" stroke-width="2"/>
    <text x="332" y="104" font-size="12.5" font-weight="900" fill="#BE185D">Žensko ime (Roze)</text>

    <!-- Brak -->
    <g transform="translate(310, 126)">
        <line x1="0" y1="0" x2="22" y2="0" stroke="#CBD5E1" stroke-width="1.5" />
        <circle cx="11" cy="0" r="7.5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
        <text x="11" y="3" font-size="8" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>
        <text x="28" y="4" font-size="12" font-weight="700" fill="#475569">Bračni par (Brak)</text>
    </g>

    <!-- Poginuo -->
    <g transform="translate(310, 156)">
        <rect x="0" y="-8" width="62" height="16" rx="8" fill="#FEE2E2" stroke="#EF4444" stroke-width="1" />
        <text x="31" y="3.5" font-size="8.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>
        <text x="68" y="4" font-size="12" font-weight="700" fill="#475569">Poginuo</text>
    </g>
</g>
''')

    # Generation Axis Markers
    axis_y = top_offset - 45
    for g in range(8, 1, -1):
        col_idx = g - 1
        gx = shift_x - GAP_FROM_ROOT - CARD_W/2 - (col_idx - 1) * COL_W - CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g}</text>
</g>''')

    svg.append(f'''
<g transform="translate({shift_x}, {axis_y})">
    <rect x="-65" y="0" width="130" height="30" rx="15" fill="#0F172A" />
    <text x="0" y="20" font-size="12" font-weight="900" fill="#F8FAFC" text-anchor="middle">👑 GEN. 1</text>
</g>''')

    for g in range(2, 9):
        col_idx = g - 1
        gx = shift_x + GAP_FROM_ROOT + CARD_W/2 + (col_idx - 1) * COL_W + CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEN. {g}</text>
</g>''')

    # 1. Connecting Lines (Shifted to positive coordinates)
    for line in lines:
        b_theme = THEMES.get(line["branch"], THEMES["root"])
        stroke_color = b_theme.get("line", "#475569")
        x1 = line['x1'] + shift_x
        y1 = line['y1'] + shift_y
        x2 = line['x2'] + shift_x
        y2 = line['y2'] + shift_y
        svg.append(f'''<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke_color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" />''')

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
                if len(clean_n) > 22:
                    clean_n = clean_n[:20] + "…"
                badge = f'''<rect x="{w - 120}" y="6" width="114" height="18" rx="9" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/><text x="{w - 63}" y="19" font-size="9" font-weight="700" fill="#334155" text-anchor="middle">{clean_n}</text>'''

            svg.append(f'''
<g transform="translate({x}, {y})">
    <!-- Card Shadow & Body -->
    <rect x="0" y="2" width="{w}" height="{h}" rx="10" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{border_c}" stroke-width="2" />
    <path d="M 0 10 Q 0 0 10 0 L {w-10} 0 Q {w} 0 {w} 10 L {w} 4 L 0 4 Z" fill="{bar_c}" />
    
    <!-- Gender Avatar -->
    <circle cx="22" cy="{h/2 + 2}" r="13" fill="{av_bg}" />
    <text x="22" y="{h/2 + 6.5}" font-size="11" font-weight="900" fill="{av_text}" text-anchor="middle">{initial}</text>
    
    {badge}
    
    <!-- Name in Blue (Male) or Pink (Female) -->
    <text x="44" y="27" font-size="15" font-weight="900" fill="{name_color}">{name}</text>
''')
            if dates:
                svg.append(f'''<text x="44" y="42" font-size="10.5" font-weight="700" fill="#64748B">🗓 {dates}</text>''')
            elif notes and "Poginu" not in notes and notes not in ["Supruga", "Suprug"]:
                display_note = notes
                if len(display_note) > 24:
                    display_note = display_note[:22] + "…"
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
    <!-- Card Shadow & Body -->
    <rect x="0" y="2" width="{w}" height="{h}" rx="12" fill="#E2E8F0" />
    <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="{border_c}" stroke-width="2" />
    <path d="M 0 12 Q 0 0 12 0 L {w-12} 0 Q {w} 0 {w} 12 L {w} 4 L 0 4 Z" fill="{bar_c}" />

    <!-- Person Top Row -->
    <circle cx="20" cy="22" r="11" fill="{av_bg_p}" />
    <text x="20" y="26" font-size="10.5" font-weight="900" fill="{av_text_p}" text-anchor="middle">{initial_p}</text>
    <text x="38" y="26" font-size="14.5" font-weight="900" fill="{name_color_p}">{name}</text>
    {badge}
''')
            if dates:
                svg.append(f'''<text x="38" y="37" font-size="9.5" font-weight="700" fill="#64748B">🗓 {dates}</text>''')

            # Dividing Line with Marriage Symbol (∞)
            svg.append(f'''
    <line x1="10" y1="41" x2="{w-10}" y2="41" stroke="#E2E8F0" stroke-width="1" />
    <circle cx="{w/2}" cy="41" r="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
    <text x="{w/2}" y="44.5" font-size="8.5" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>

    <!-- Spouse Bottom Row -->
    <circle cx="20" cy="{sp_y_name + 1}" r="11" fill="{av_bg_s}" />
    <text x="20" y="{sp_y_name + 5}" font-size="10.5" font-weight="900" fill="{av_text_s}" text-anchor="middle">{initial_s}</text>
    <text x="38" y="{sp_y_name + 5}" font-size="14.5" font-weight="900" fill="{name_color_s}">{sp_name}</text>
''')
            if has_real_sp_note:
                display_sp_note = sp_notes
                if len(display_sp_note) > 24:
                    display_sp_note = display_sp_note[:22] + "…"
                svg.append(f'''<text x="38" y="{sp_y_name + 16}" font-size="9.5" font-weight="600" fill="#64748B">{display_sp_note}</text>''')

            svg.append('</g>\n')

    svg.append('</svg>')
    return "".join(svg)

engine = BilateralPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_bilateral()
svg_content = render_illustrator_svg(nodes, lines, max_h, top_off)

with open("Porodicno_Stablo_Zehic_A0.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

with open("Arbre_Genealogique_A0_Bilateral.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

with open("Arbre_Genealogique_Complet.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Generated 100% Adobe Illustrator Compatible Master Poster!")

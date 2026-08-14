# -*- coding: utf-8 -*-
"""
Bilateral Poster Generator with Unified Vector Icons (Zero broken emojis):
- Marriage indicator: Vector divider with white circle + red infinity '∞' in legend and cards.
- Fallen badge: Red pill badge 'Poginuo' identical in legend and on cards.
- Full consistency across poster and branch views.
"""
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

CARD_W = 236
CARD_H = 48          # Single person card height
CARD_H_COUPLE = 80   # Couple card height
V_GAP = 12           # Gap between sibling leaf blocks
COL_W = 282          # Column width per generation

MALE_TEXT_COLOR = "#1D4ED8"     # Deep Bold Blue
MALE_AVATAR_BG = "#DBEAFE"
MALE_AVATAR_TEXT = "#1E40AF"

FEMALE_TEXT_COLOR = "#BE185D"   # Deep Bold Rose
FEMALE_AVATAR_BG = "#FCE7F3"
FEMALE_AVATAR_TEXT = "#9D174D"

THEMES = {
    "root": {
        "name": "Racine Commune",
        "bg": "#1E293B", "border": "#0F172A", "primary": "#0F172A", "card_bg": "#FFFFFF",
        "text": "#0F172A", "subtext": "#64748B", "line": "#334155", "tag_bg": "#E2E8F0"
    },
    "Branche Adem": {
        "name": "Branche Adem (1855–1938)",
        "bg": "#F0FDF4", "card_bg": "#FFFFFF", "border": "#16A34A", "primary": "#15803D",
        "text": "#14532D", "subtext": "#166534", "line": "#16A34A", "tag_bg": "#DCFCE7"
    },
    "Branche Meho": {
        "name": "Branche Meho (1867–1941)",
        "bg": "#FFFBEB", "card_bg": "#FFFFFF", "border": "#D97706", "primary": "#B45309",
        "text": "#78350F", "subtext": "#92400E", "line": "#D97706", "tag_bg": "#FEF3C7"
    },
    "Branche Osman": {
        "name": "Branche Osman (1860–1937)",
        "bg": "#F0F9FF", "card_bg": "#FFFFFF", "border": "#0284C7", "primary": "#0369A1",
        "text": "#0C4A6E", "subtext": "#075985", "line": "#0284C7", "tag_bg": "#E0F2FE"
    },
    "Branche Nurif": {
        "name": "Branche Nurif",
        "bg": "#FFF1F2", "card_bg": "#FFFFFF", "border": "#E11D48", "primary": "#BE123C",
        "text": "#881337", "subtext": "#9F1239", "line": "#E11D48", "tag_bg": "#FFE4E6"
    },
    "Branche Paša": {
        "name": "Branche Paša",
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

        left_branches = [b for b in branches if b["branch_name"] == "Branche Adem"]
        right_branches = [b for b in branches if b["branch_name"] != "Branche Adem"]

        for b in branches:
            self.compute_subtree_height(b["person"])

        left_total_span = sum(b["person"]["_span_h"] for b in left_branches) + (len(left_branches) - 1) * V_GAP * 4
        right_total_span = sum(b["person"]["_span_h"] for b in right_branches) + (len(right_branches) - 1) * V_GAP * 4

        max_height = max(left_total_span, right_total_span)
        top_offset = 280

        start_y_left = top_offset + (max_height - left_total_span) / 2
        start_y_right = top_offset + (max_height - right_total_span) / 2

        spine_gap = 145

        left_nodes, left_lines, left_attach, left_h = self.layout_wing(left_branches, -spine_gap, start_y_left, -1, "Branche Adem")
        right_nodes, right_lines, right_attach, right_h = self.layout_wing(right_branches, spine_gap, start_y_right, 1, "Right Wing")

        center_y = top_offset + max_height / 2 - 45
        root_card = {
            "id": root_node["id"],
            "name": root_node["name"],
            "role": "Patrijarh / Glava Porodice",
            "dates": "Zajednički Predak",
            "gender": "M",
            "gen": 1,
            "branch": "root",
            "x": -CARD_W / 2,
            "y": center_y,
            "w": CARD_W,
            "h": 90,
            "is_root": True
        }

        all_lines = left_lines + right_lines
        
        # Central Lines to Left Wing
        left_bus_x = -spine_gap / 2
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
                "branch": "Branche Adem"
            })

        # Central Lines to Right Wing
        right_bus_x = spine_gap / 2
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

def render_bilateral_svg(nodes, lines, max_height, top_offset):
    min_x = min(n["x"] for n in nodes) - 80
    max_x = max(n["x"] + n["w"] for n in nodes) + 80
    min_y = 0
    max_y = max(n["y"] + n["h"] for n in nodes) + 120

    width = int(max_x - min_x)
    height = int(max_y - min_y)

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {width} {height}" width="{width}" height="{height}" style="background-color: #F8FAFC; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
<defs>
    <filter id="boxShadow" x="-10%" y="-15%" width="125%" height="135%">
        <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06" flood-color="#0F172A" />
        <feDropShadow dx="0" dy="6" stdDeviation="8" flood-opacity="0.04" flood-color="#0F172A" />
    </filter>
    <filter id="rootShadow" x="-15%" y="-15%" width="130%" height="135%">
        <feDropShadow dx="0" dy="6" stdDeviation="12" flood-opacity="0.25" flood-color="#0F172A" />
    </filter>
    <linearGradient id="rootGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1E293B" />
        <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
</defs>
''')

    # Header
    svg.append(f'''
<!-- Header -->
<g transform="translate(0, 45)" text-anchor="middle">
    <rect x="-440" y="0" width="880" height="110" rx="20" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" filter="url(#boxShadow)"/>
    <text x="0" y="44" font-size="28" font-weight="900" fill="#0F172A" letter-spacing="-0.5">PORODIČNO STABLO (ARBRE GÉNÉALOGIQUE)</text>
    <text x="0" y="74" font-size="16" font-weight="700" fill="#475569">Potomstvo Ibrahima • 8 Generacija • 401 Član</text>
    <text x="0" y="96" font-size="12.5" font-weight="600" fill="#94A3B8">Boje grana (Zelena, Plava, Žuta) • Imena: Plava = Muška, Roze = Ženska</text>
</g>
''')

    # Dual Legend Block (Unified Vector Icons)
    svg.append(f'''
<!-- Legenda Grana (Branches) -->
<g transform="translate({min_x + 80}, 48)">
    <rect x="0" y="0" width="340" height="105" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#boxShadow)"/>
    <text x="18" y="26" font-size="13" font-weight="800" fill="#1E293B" letter-spacing="0.5">BOJE GRANA (BRANCHES)</text>
    
    <circle cx="28" cy="50" r="7" fill="#16A34A" />
    <text x="44" y="55" font-size="12.5" font-weight="700" fill="#14532D">Grana Adem (177 članova)</text>

    <circle cx="28" cy="78" r="7" fill="#0284C7" />
    <text x="44" y="83" font-size="12.5" font-weight="700" fill="#0C4A6E">Grana Osman (152 člana)</text>

    <circle cx="215" cy="50" r="7" fill="#D97706" />
    <text x="230" y="55" font-size="12.5" font-weight="700" fill="#78350F">Meho (69)</text>

    <circle cx="215" cy="78" r="7" fill="#E11D48" />
    <text x="230" y="83" font-size="12" font-weight="700" fill="#881337">Nurif &amp; Paša</text>
</g>

<!-- Legenda Oznaka i Spolova (Identical Icons as in Cards) -->
<g transform="translate({max_x - 440}, 48)">
    <rect x="0" y="0" width="360" height="105" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#boxShadow)"/>
    <text x="18" y="26" font-size="13" font-weight="800" fill="#1E293B" letter-spacing="0.5">LEGENDA OZNAKA &amp; SPOLOVA</text>
    
    <!-- Male -->
    <rect x="18" y="40" width="14" height="14" rx="4" fill="#DBEAFE" stroke="#1D4ED8" stroke-width="2"/>
    <text x="38" y="52" font-size="12.5" font-weight="900" fill="#1D4ED8">Muško ime (Plava)</text>

    <!-- Female -->
    <rect x="18" y="70" width="14" height="14" rx="4" fill="#FCE7F3" stroke="#BE185D" stroke-width="2"/>
    <text x="38" y="82" font-size="12.5" font-weight="900" fill="#BE185D">Žensko ime (Roze)</text>

    <!-- Marriage Vector Icon (Identical to Cards) -->
    <g transform="translate(195, 47)">
        <line x1="0" y1="0" x2="22" y2="0" stroke="#CBD5E1" stroke-width="1.5" />
        <circle cx="11" cy="0" r="7.5" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
        <text x="11" y="3" font-size="8" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>
        <text x="28" y="4" font-size="12" font-weight="700" fill="#475569">Brak (Par)</text>
    </g>

    <!-- Fallen Vector Badge (Identical to Cards) -->
    <g transform="translate(195, 77)">
        <rect x="0" y="-8" width="62" height="16" rx="8" fill="#FEE2E2" stroke="#EF4444" stroke-width="1" />
        <text x="31" y="3.5" font-size="8.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>
        <text x="68" y="4" font-size="11.5" font-weight="600" fill="#64748B">Poginuo</text>
    </g>
</g>
''')

    # Generation Axis Markers (Left Wing & Right Wing)
    axis_y = top_offset - 45
    for g in range(8, 1, -1):
        col_idx = g - 1
        gx = -145 - (col_idx - 1) * COL_W - CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" opacity="0.9" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">GEN. {g}</text>
</g>''')

    svg.append(f'''
<g transform="translate(0, {axis_y})">
    <rect x="-65" y="0" width="130" height="30" rx="15" fill="#0F172A" />
    <text x="0" y="20" font-size="12" font-weight="900" fill="#F8FAFC" text-anchor="middle" letter-spacing="0.5">👑 GEN. 1</text>
</g>''')

    for g in range(2, 9):
        col_idx = g - 1
        gx = 145 + (col_idx - 1) * COL_W + CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" opacity="0.9" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">GEN. {g}</text>
</g>''')

    # Draw Connecting Lines (Branch color-coded)
    for line in lines:
        b_theme = THEMES.get(line["branch"], THEMES["root"])
        stroke_color = b_theme.get("line", "#64748B")
        svg.append(f'''<line x1="{line['x1']}" y1="{line['y1']}" x2="{line['x2']}" y2="{line['y2']}" stroke="{stroke_color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" />''')

    # Draw Cards
    for n in nodes:
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
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
<g transform="translate({x}, {y})" filter="url(#rootShadow)">
    <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="url(#rootGrad)" stroke="#3B82F6" stroke-width="3" />
    <circle cx="36" cy="{h/2}" r="22" fill="#334155" />
    <text x="36" y="{h/2 + 7}" font-size="20" font-weight="900" fill="#F8FAFC" text-anchor="middle">👑</text>
    <text x="70" y="40" font-size="24" font-weight="900" fill="#93C5FD">{name}</text>
    <text x="70" y="66" font-size="13" font-weight="700" fill="#94A3B8">Patrijarh (Osnivač Loze)</text>
</g>''')
        elif not has_spouse:
            # Single Card
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
                if len(clean_n) > 14:
                    clean_n = clean_n[:12] + "…"
                badge = f'''<rect x="{w - 88}" y="6" width="82" height="18" rx="9" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/><text x="{w - 47}" y="19" font-size="9.5" font-weight="700" fill="#334155" text-anchor="middle">{clean_n}</text>'''

            svg.append(f'''
<g transform="translate({x}, {y})" filter="url(#boxShadow)">
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
                svg.append(f'''<text x="44" y="42" font-size="10" font-weight="600" fill="#64748B">{notes}</text>''')
            svg.append('</g>\n')

        else:
            # Couple Card (Cleaned, Identical Marriage Icon)
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
<g transform="translate({x}, {y})" filter="url(#boxShadow)">
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
                svg.append(f'''<text x="38" y="{sp_y_name + 16}" font-size="9.5" font-weight="600" fill="#64748B">{sp_notes}</text>''')

            svg.append('</g>\n')

    svg.append('</svg>')
    return "".join(svg)

engine = BilateralPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_bilateral()
svg_content = render_bilateral_svg(nodes, lines, max_h, top_off)

with open("Arbre_Genealogique_A0_Bilateral.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

with open("Arbre_Genealogique_Complet.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Generated Bilateral Poster with Identical Vector Icons!")

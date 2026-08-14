# -*- coding: utf-8 -*-
"""
Bilateral Genealogical Poster Generator with Explicit Gender Coloring
- Plava boja (Blue) for all Males (Muške osobe)
- Roze boja (Pink/Rose) for all Females (Ženske osobe)
"""
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Layout constants
CARD_W = 236
CARD_H = 48          # Single person card height
CARD_H_COUPLE = 84   # Couple card height
V_GAP = 12           # Vertical gap between sibling leaf blocks
COL_W = 282          # Column width per generation

# Color Tokens
MALE_COLOR = "#2563EB"       # Royal Blue
MALE_BG = "#F0F7FF"          # Light soft blue
MALE_AVATAR_BG = "#DBEAFE"   # Avatar circle bg
MALE_TEXT = "#1E40AF"

FEMALE_COLOR = "#EC4899"     # Elegant Rose / Pink
FEMALE_BG = "#FFF1F6"        # Light soft pink
FEMALE_AVATAR_BG = "#FCE7F3" # Avatar circle bg
FEMALE_TEXT = "#BE185D"

ROOT_COLOR = "#1E293B"       # Slate / Gold Crown for Ibrahim
LINE_COLOR = "#64748B"

class BilateralGenderPosterEngine:
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
            if direction == -1:
                card_x = node_x - CARD_W
            else:
                card_x = node_x

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

            if direction == -1:
                parent_in_x = card_x + CARD_W
                parent_out_x = card_x
            else:
                parent_in_x = card_x
                parent_out_x = card_x + CARD_W

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
                    "gender": node.get("gender", "M")
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
                        "gender": c.get("gender", "M")
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
                    "gender": node.get("gender", "M")
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

    def generate_full_tree(self):
        root_node = self.data["root"]
        branches = root_node["children_branches"]

        # Left Wing: Adem (177 people)
        # Right Wing: Osman (152), Meho (69), Nurif (1), Paša (1) (223 people)
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

        # Central Root Ibrahim
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
            "gender": "M"
        })
        min_ly = min(p[1] for p in left_attach)
        max_ly = max(p[1] for p in left_attach)
        all_lines.append({
            "type": "bus",
            "x1": left_bus_x,
            "y1": min(center_y + 45, min_ly),
            "x2": left_bus_x,
            "y2": max(center_y + 45, max_ly),
            "gender": "M"
        })
        for pt in left_attach:
            all_lines.append({
                "type": "stem",
                "x1": left_bus_x,
                "y1": pt[1],
                "x2": pt[0],
                "y2": pt[1],
                "gender": "M"
            })

        # Central Lines to Right Wing
        right_bus_x = spine_gap / 2
        all_lines.append({
            "type": "stem",
            "x1": root_card["x"] + root_card["w"],
            "y1": center_y + 45,
            "x2": right_bus_x,
            "y2": center_y + 45,
            "gender": "M"
        })
        min_ry = min(p[1] for p in right_attach)
        max_ry = max(p[1] for p in right_attach)
        all_lines.append({
            "type": "bus",
            "x1": right_bus_x,
            "y1": min(center_y + 45, min_ry),
            "x2": right_bus_x,
            "y2": max(center_y + 45, max_ry),
            "gender": "M"
        })
        for pt in right_attach:
            all_lines.append({
                "type": "stem",
                "x1": right_bus_x,
                "y1": pt[1],
                "x2": pt[0],
                "y2": pt[1],
                "gender": "M"
            })

        all_nodes = [root_card] + left_nodes + right_nodes
        return all_nodes, all_lines, max_height, top_offset

def render_svg(nodes, lines, max_height, top_offset):
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
    <linearGradient id="maleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#2563EB" />
        <stop offset="100%" stop-color="#3B82F6" />
    </linearGradient>
    <linearGradient id="femaleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#EC4899" />
        <stop offset="100%" stop-color="#F43F5E" />
    </linearGradient>
</defs>
''')

    # Header Banner
    svg.append(f'''
<!-- Header -->
<g transform="translate(0, 45)" text-anchor="middle">
    <rect x="-440" y="0" width="880" height="110" rx="20" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" filter="url(#boxShadow)"/>
    <text x="0" y="44" font-size="28" font-weight="900" fill="#0F172A" letter-spacing="-0.5">PORODIČNO STABLO (ARBRE GÉNÉALOGIQUE)</text>
    <text x="0" y="74" font-size="16" font-weight="700" fill="#475569">Potomstvo Ibrahima • 8 Generacija • 401 Član</text>
    <text x="0" y="96" font-size="12.5" font-weight="600" fill="#94A3B8">Format Bilateral Poster A0 / A1 • Kodiranje po spolu (Plava = Muški, Roze = Ženski)</text>
</g>
''')

    # Legend Block (Gender Color Code & Wings)
    svg.append(f'''
<!-- Legenda Spolova i Grana (Légende) -->
<g transform="translate({min_x + 80}, 48)">
    <rect x="0" y="0" width="340" height="100" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#boxShadow)"/>
    <text x="18" y="26" font-size="13" font-weight="800" fill="#1E293B" letter-spacing="0.5">LEGENDA OZNAKA (LÉGENDE)</text>
    
    <!-- Male -->
    <rect x="18" y="40" width="14" height="14" rx="4" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" />
    <text x="38" y="52" font-size="12.5" font-weight="800" fill="#1E40AF">Muška osoba (Plava)</text>
    
    <!-- Female -->
    <rect x="18" y="68" width="14" height="14" rx="4" fill="#FCE7F3" stroke="#EC4899" stroke-width="2" />
    <text x="38" y="80" font-size="12.5" font-weight="800" fill="#BE185D">Ženska osoba (Roze)</text>

    <!-- Marriage symbol -->
    <text x="215" y="52" font-size="12" font-weight="700" fill="#64748B">💍 = Bračna veza</text>
    <text x="215" y="80" font-size="12" font-weight="700" fill="#B91C1C">🎖 = Poginuo / Poginula</text>
</g>

<!-- Info Desno Krilo -->
<g transform="translate({max_x - 420}, 48)">
    <rect x="0" y="0" width="340" height="100" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#boxShadow)"/>
    <text x="18" y="26" font-size="13" font-weight="800" fill="#1E293B" letter-spacing="0.5">STRUKTURA KRILA (BRANCHES)</text>
    <text x="18" y="52" font-size="12.5" font-weight="700" fill="#15803D">🌿 Lijevo krilo : Adem (177 članova)</text>
    <text x="18" y="74" font-size="12" font-weight="700" fill="#0369A1">🌊 Desno krilo : Osman (152), Meho (69)</text>
    <text x="18" y="92" font-size="11" font-weight="600" fill="#94A3B8">Nurif &amp; Paša (Drevne loze)</text>
</g>
''')

    # Generation Axis Markers (Left Wing & Right Wing)
    axis_y = top_offset - 45
    # Left wing generation pills
    for g in range(8, 1, -1):
        col_idx = g - 1
        gx = -145 - (col_idx - 1) * COL_W - CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" opacity="0.9" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">GEN. {g}</text>
</g>''')

    # Center Patriarch Header
    svg.append(f'''
<g transform="translate(0, {axis_y})">
    <rect x="-65" y="0" width="130" height="30" rx="15" fill="#0F172A" />
    <text x="0" y="20" font-size="12" font-weight="900" fill="#F8FAFC" text-anchor="middle" letter-spacing="0.5">👑 GEN. 1</text>
</g>''')

    # Right wing generation pills
    for g in range(2, 9):
        col_idx = g - 1
        gx = 145 + (col_idx - 1) * COL_W + CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" opacity="0.9" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">GEN. {g}</text>
</g>''')

    # Draw Connecting Lines (Orthogonal Brackets)
    for line in lines:
        stroke_color = "#64748B"
        svg.append(f'''<line x1="{line['x1']}" y1="{line['y1']}" x2="{line['x2']}" y2="{line['y2']}" stroke="{stroke_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />''')

    # Draw Node Cards with Gender Coloring
    for n in nodes:
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        is_root = n.get("is_root", False)
        name = n["name"]
        dates = n.get("dates", "")
        notes = n.get("notes", "")
        gender = n.get("gender", "M")
        has_spouse = n.get("has_spouse", False)
        spouse = n.get("spouse")

        if is_root:
            # Patriarch Centerpiece
            svg.append(f'''
<g transform="translate({x}, {y})" filter="url(#rootShadow)">
    <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="url(#rootGrad)" stroke="#3B82F6" stroke-width="3" />
    <circle cx="36" cy="{h/2}" r="22" fill="#334155" />
    <text x="36" y="{h/2 + 7}" font-size="20" font-weight="900" fill="#F8FAFC" text-anchor="middle">👑</text>
    <text x="70" y="40" font-size="24" font-weight="900" fill="#FFFFFF">{name}</text>
    <text x="70" y="66" font-size="13" font-weight="700" fill="#93C5FD">Patrijarh (Osnivač Loze)</text>
</g>''')
        elif not has_spouse:
            # Single Person Card (Male or Female)
            is_male = (gender == "M")
            border_color = MALE_COLOR if is_male else FEMALE_COLOR
            bar_color = "url(#maleGrad)" if is_male else "url(#femaleGrad)"
            card_bg = MALE_BG if is_male else FEMALE_BG
            av_bg = MALE_AVATAR_BG if is_male else FEMALE_AVATAR_BG
            av_text = MALE_TEXT if is_male else FEMALE_TEXT
            initial = name[0] if name else "?"

            badge_text = ""
            if "Poginu" in notes:
                badge_text = f'''<rect x="{w - 84}" y="6" width="78" height="18" rx="9" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/><text x="{w - 45}" y="19" font-size="9.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo/la</text>'''
            elif notes:
                clean_n = notes.replace("u. ", "u. ").replace("r. ", "r. ")
                if len(clean_n) > 14:
                    clean_n = clean_n[:12] + "…"
                badge_text = f'''<rect x="{w - 88}" y="6" width="82" height="18" rx="9" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/><text x="{w - 47}" y="19" font-size="9.5" font-weight="700" fill="#334155" text-anchor="middle">{clean_n}</text>'''

            svg.append(f'''
<g transform="translate({x}, {y})" filter="url(#boxShadow)">
    <rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="{card_bg}" stroke="{border_color}" stroke-width="2" />
    <path d="M 0 10 Q 0 0 10 0 L {w-10} 0 Q {w} 0 {w} 10 L {w} 4 L 0 4 Z" fill="{bar_color}" />
    
    <circle cx="22" cy="{h/2 + 2}" r="13" fill="{av_bg}" />
    <text x="22" y="{h/2 + 6.5}" font-size="11" font-weight="900" fill="{av_text}" text-anchor="middle">{initial}</text>
    
    {badge_text}
    
    <text x="44" y="27" font-size="15" font-weight="800" fill="#0F172A">{name}</text>
''')
            if dates:
                svg.append(f'''<text x="44" y="42" font-size="10.5" font-weight="700" fill="#475569">🗓 {dates}</text>''')
            elif notes and "Poginu" not in notes:
                svg.append(f'''<text x="44" y="42" font-size="10" font-weight="600" fill="#64748B">{notes}</text>''')
            svg.append('</g>\n')

        else:
            # Couple Card (Dual Person + Spouse)
            is_male_p = (gender == "M")
            sp_gender = spouse.get("gender", "F" if is_male_p else "M")
            is_male_s = (sp_gender == "M")

            p_color = MALE_COLOR if is_male_p else FEMALE_COLOR
            p_av_bg = MALE_AVATAR_BG if is_male_p else FEMALE_AVATAR_BG
            p_av_text = MALE_TEXT if is_male_p else FEMALE_TEXT

            s_color = MALE_COLOR if is_male_s else FEMALE_COLOR
            s_av_bg = MALE_AVATAR_BG if is_male_s else FEMALE_AVATAR_BG
            s_av_text = MALE_TEXT if is_male_s else FEMALE_TEXT

            initial_p = name[0] if name else "?"
            sp_name = spouse.get("name", "")
            initial_s = sp_name[0] if sp_name else "?"
            sp_notes = spouse.get("notes", "")

            badge_text = ""
            if "Poginu" in notes:
                badge_text = f'''<rect x="{w - 84}" y="6" width="78" height="18" rx="9" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/><text x="{w - 45}" y="19" font-size="9.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo</text>'''

            svg.append(f'''
<g transform="translate({x}, {y})" filter="url(#boxShadow)">
    <!-- Main Card Body -->
    <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.8" />
    
    <!-- Top Row Background Tint (Primary Person) -->
    <path d="M 0 12 Q 0 0 12 0 L {w-12} 0 Q {w} 0 {w} 12 L {w} 42 L 0 42 Z" fill="{MALE_BG if is_male_p else FEMALE_BG}" />
    <!-- Top Accent Stripe -->
    <path d="M 0 12 Q 0 0 12 0 L {w-12} 0 Q {w} 0 {w} 12 L {w} 4 L 0 4 Z" fill="{MALE_COLOR if is_male_p else FEMALE_COLOR}" />

    <!-- Person Top Row -->
    <circle cx="20" cy="23" r="11" fill="{p_av_bg}" />
    <text x="20" y="27" font-size="10.5" font-weight="900" fill="{p_av_text}" text-anchor="middle">{initial_p}</text>
    <text x="38" y="27" font-size="14.5" font-weight="800" fill="#0F172A">{name}</text>
    {badge_text}
''')
            if dates:
                svg.append(f'''<text x="38" y="38" font-size="9.5" font-weight="700" fill="#475569">🗓 {dates}</text>''')

            # Dividing Line with Marriage Rings Symbol
            svg.append(f'''
    <!-- Bottom Row Background Tint (Spouse) -->
    <path d="M 0 43 L {w} 43 L {w} {h-12} Q {w} {h} {w-12} {h} L 12 {h} Q 0 {h} 0 {h-12} Z" fill="{MALE_BG if is_male_s else FEMALE_BG}" />
    
    <line x1="10" y1="43" x2="{w-10}" y2="43" stroke="#CBD5E1" stroke-width="1" />
    <circle cx="{w/2}" cy="43" r="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
    <text x="{w/2}" y="46.5" font-size="8.5" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>

    <!-- Spouse Bottom Row -->
    <circle cx="20" cy="63" r="11" fill="{s_av_bg}" />
    <text x="20" y="67" font-size="10.5" font-weight="900" fill="{s_av_text}" text-anchor="middle">{initial_s}</text>
    <text x="38" y="67" font-size="14" font-weight="800" fill="#1E293B">{sp_name}</text>
''')
            if sp_notes and sp_notes != "Supruga" and sp_notes != "Suprug":
                svg.append(f'''<text x="38" y="78" font-size="9.5" font-weight="600" fill="#64748B">{sp_notes}</text>''')
            else:
                svg.append(f'''<text x="38" y="78" font-size="9" font-weight="600" fill="#94A3B8">Supruga</text>''')

            svg.append('</g>\n')

    svg.append('</svg>')
    return "".join(svg)

engine = BilateralGenderPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_tree()
svg_content = render_svg(nodes, lines, max_h, top_off)

# Write output files
with open("Arbre_Genealogique_A0_Bilateral.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

with open("Arbre_Genealogique_Complet.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print("Generated Gender-Color Coded Bilateral Poster SVG!")

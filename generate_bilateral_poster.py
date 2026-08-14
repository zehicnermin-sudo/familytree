# -*- coding: utf-8 -*-
"""
Bilateral (Center-Out) Genealogical Poster Engine for A0/A1 Printing
Matches the exact dual-wing format requested by the user:
- Root (Ibrahim) in the central column
- Left Wing (Branche Adem) branching out to the left across 7 generations
- Right Wing (Branches Osman, Meho, Nurif, Paša) branching out to the right across 7 generations
- Crystal-clear typography, elegant brackets, branch color palettes, header & legend.
"""
import json

with open("family_tree_structured.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Layout constants
CARD_W = 230
CARD_H = 46          # Height for single person
CARD_H_COUPLE = 82   # Height for person + spouse card
V_GAP = 12           # Gap between sibling subtrees
COL_W = 275          # Column width per generation

THEMES = {
    "root": {
        "name": "Racine Commune",
        "bg": "#1E293B", "border": "#0F172A", "primary": "#0F172A", "text": "#FFFFFF", "subtext": "#94A3B8", "line": "#334155"
    },
    "Branche Adem": {
        "name": "Branche Adem (1855–1938)",
        "bg": "#F0FDF4", "card_bg": "#FFFFFF", "border": "#16A34A", "primary": "#15803D",
        "text": "#0F172A", "subtext": "#166534", "line": "#16A34A", "tag_bg": "#DCFCE7", "tag_text": "#14532D"
    },
    "Branche Meho": {
        "name": "Branche Meho (1867–1941)",
        "bg": "#FFFBEB", "card_bg": "#FFFFFF", "border": "#D97706", "primary": "#B45309",
        "text": "#0F172A", "subtext": "#92400E", "line": "#D97706", "tag_bg": "#FEF3C7", "tag_text": "#78350F"
    },
    "Branche Osman": {
        "name": "Branche Osman (1860–1937)",
        "bg": "#F0F9FF", "card_bg": "#FFFFFF", "border": "#0284C7", "primary": "#0369A1",
        "text": "#0F172A", "subtext": "#075985", "line": "#0284C7", "tag_bg": "#E0F2FE", "tag_text": "#0C4A6E"
    },
    "Branche Nurif": {
        "name": "Branche Nurif",
        "bg": "#FFF1F2", "card_bg": "#FFFFFF", "border": "#E11D48", "primary": "#BE123C",
        "text": "#0F172A", "subtext": "#9F1239", "line": "#E11D48", "tag_bg": "#FFE4E6", "tag_text": "#881337"
    },
    "Branche Paša": {
        "name": "Branche Paša",
        "bg": "#FAF5FF", "card_bg": "#FFFFFF", "border": "#9333EA", "primary": "#7E22CE",
        "text": "#0F172A", "subtext": "#6B21A8", "line": "#9333EA", "tag_bg": "#F3E8FF", "tag_text": "#581C87"
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
            if direction == -1:
                card_x = node_x - CARD_W
            else:
                card_x = node_x

            card_info = {
                "id": node.get("id"),
                "name": node.get("name"),
                "dates": node.get("dates", ""),
                "notes": node.get("notes", ""),
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

        # Left Wing: Adem (177 people)
        # Right Wing: Osman (152), Meho (69), Nurif (1), Paša (1) (223 people)
        left_branches = [b for b in branches if b["branch_name"] == "Branche Adem"]
        right_branches = [b for b in branches if b["branch_name"] != "Branche Adem"]

        for b in branches:
            self.compute_subtree_height(b["person"])

        left_total_span = sum(b["person"]["_span_h"] for b in left_branches) + (len(left_branches) - 1) * V_GAP * 4
        right_total_span = sum(b["person"]["_span_h"] for b in right_branches) + (len(right_branches) - 1) * V_GAP * 4

        max_height = max(left_total_span, right_total_span)
        top_offset = 280 # space for header & generation axis

        start_y_left = top_offset + (max_height - left_total_span) / 2
        start_y_right = top_offset + (max_height - right_total_span) / 2

        # Distance from center spine to Gen 2 columns
        spine_gap = 140

        left_nodes, left_lines, left_attach, left_h = self.layout_wing(left_branches, -spine_gap, start_y_left, -1, "Branche Adem")
        right_nodes, right_lines, right_attach, right_h = self.layout_wing(right_branches, spine_gap, start_y_right, 1, "Right Wing")

        # Patriarch Ibrahim Card in the middle
        center_y = top_offset + max_height / 2 - 45
        root_card = {
            "id": root_node["id"],
            "name": root_node["name"],
            "role": "Patriarche Fondateur",
            "dates": "Ancêtre Commun",
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
        <feDropShadow dx="0" dy="6" stdDeviation="10" flood-opacity="0.25" flood-color="#0F172A" />
    </filter>
    <linearGradient id="rootGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1E293B" />
        <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
</defs>
''')

    # Top Main Header Banner (Symmetrical & Editorial)
    svg.append(f'''
<!-- Header -->
<g transform="translate(0, 45)" text-anchor="middle">
    <rect x="-420" y="0" width="840" height="110" rx="20" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" filter="url(#boxShadow)"/>
    <text x="0" y="44" font-size="28" font-weight="900" fill="#0F172A" letter-spacing="-0.5">ARBRE GÉNÉALOGIQUE DE LA FAMILLE</text>
    <text x="0" y="74" font-size="16" font-weight="700" fill="#475569">Descendance Complète d'Ibrahim • 8 Générations • 401 Membres</text>
    <text x="0" y="96" font-size="12" font-weight="600" fill="#94A3B8">Format Bilatéral A0 / A1 • Haute Résolution &amp; Précision</text>
</g>
''')

    # Left & Right Legends
    svg.append(f'''
<!-- Légende Gauche (Adem) -->
<g transform="translate({min_x + 80}, 50)">
    <rect x="0" y="0" width="310" height="95" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#boxShadow)"/>
    <text x="18" y="28" font-size="13" font-weight="800" fill="#14532D" letter-spacing="0.5">AILE GAUCHE : BRANCHE ADEM</text>
    <circle cx="28" cy="54" r="7" fill="#16A34A" />
    <text x="44" y="59" font-size="13" font-weight="700" fill="#14532D">177 Personnes (1855 – 1938)</text>
    <text x="18" y="82" font-size="11" font-weight="600" fill="#64748B">Sous-branches: Avdo, Mujo, Sajtan, Ibrahim</text>
</g>

<!-- Légende Droite (Osman & Meho) -->
<g transform="translate({max_x - 390}, 50)">
    <rect x="0" y="0" width="310" height="95" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#boxShadow)"/>
    <text x="18" y="28" font-size="13" font-weight="800" fill="#0C4A6E" letter-spacing="0.5">AILE DROITE : OSMAN, MEHO &amp; AUTRES</text>
    <circle cx="28" cy="50" r="6" fill="#0284C7" />
    <text x="42" y="54" font-size="12" font-weight="700" fill="#0C4A6E">Branche Osman (152 p.)</text>
    <circle cx="180" cy="50" r="6" fill="#D97706" />
    <text x="194" y="54" font-size="12" font-weight="700" fill="#78350F">Meho (69 p.)</text>
    <circle cx="28" cy="74" r="6" fill="#E11D48" />
    <text x="42" y="78" font-size="12" font-weight="700" fill="#881337">Nurif &amp; Paša (Lignées ancestrales)</text>
</g>
''')

    # Generation Axis Markers (Left Wing & Right Wing)
    axis_y = top_offset - 45
    # Left wing generation pills
    for g in range(8, 1, -1):
        col_idx = g - 1
        gx = -140 - (col_idx - 1) * COL_W - CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" opacity="0.9" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">GÉN. {g}</text>
</g>''')

    # Center Patriarch Header
    svg.append(f'''
<g transform="translate(0, {axis_y})">
    <rect x="-65" y="0" width="130" height="30" rx="15" fill="#0F172A" />
    <text x="0" y="20" font-size="12" font-weight="900" fill="#F8FAFC" text-anchor="middle" letter-spacing="0.5">👑 GÉN. 1</text>
</g>''')

    # Right wing generation pills
    for g in range(2, 9):
        col_idx = g - 1
        gx = 140 + (col_idx - 1) * COL_W + CARD_W / 2
        svg.append(f'''
<g transform="translate({gx}, {axis_y})">
    <rect x="-55" y="0" width="110" height="30" rx="15" fill="#1E293B" opacity="0.9" />
    <text x="0" y="20" font-size="11.5" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="0.5">GÉN. {g}</text>
</g>''')

    # Draw Connecting Orthogonal Lines (Brackets)
    for line in lines:
        b_theme = THEMES.get(line["branch"], THEMES["root"])
        stroke_color = b_theme.get("line", "#64748B")
        svg.append(f'''<line x1="{line['x1']}" y1="{line['y1']}" x2="{line['x2']}" y2="{line['y2']}" stroke="{stroke_color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />''')

    # Draw Node Cards
    for n in nodes:
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        is_root = n.get("is_root", False)
        branch = n.get("branch", "root")
        theme = THEMES.get(branch, THEMES["root"])
        name = n["name"]
        dates = n.get("dates", "")
        notes = n.get("notes", "")
        has_spouse = n.get("has_spouse", False)
        spouse = n.get("spouse")

        if is_root:
            # Patriarch Centerpiece
            svg.append(f'''
<g transform="translate({x}, {y})" filter="url(#rootShadow)">
    <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="url(#rootGrad)" stroke="#475569" stroke-width="3" />
    <circle cx="36" cy="{h/2}" r="22" fill="#334155" />
    <text x="36" y="{h/2 + 7}" font-size="20" font-weight="900" fill="#F8FAFC" text-anchor="middle">👑</text>
    <text x="70" y="40" font-size="24" font-weight="900" fill="#FFFFFF">{name}</text>
    <text x="70" y="66" font-size="13" font-weight="700" fill="#94A3B8">Patriarche Fondateur</text>
</g>''')
        elif not has_spouse:
            # Single Person Card
            border_color = theme.get("border", "#94A3B8")
            bar_color = theme.get("primary", "#475569")
            initial = name[0] if name else "?"

            badge_text = ""
            if "Poginu" in notes:
                badge_text = f'''<rect x="{w - 82}" y="6" width="76" height="18" rx="9" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/><text x="{w - 44}" y="19" font-size="9.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Mort guerre</text>'''
            elif notes:
                clean_n = notes.replace("u. ", "née ").replace("r. ", "d' ")
                if len(clean_n) > 14:
                    clean_n = clean_n[:12] + "…"
                badge_text = f'''<rect x="{w - 88}" y="6" width="82" height="18" rx="9" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/><text x="{w - 47}" y="19" font-size="9.5" font-weight="700" fill="#334155" text-anchor="middle">{clean_n}</text>'''

            svg.append(f'''
<g transform="translate({x}, {y})" filter="url(#boxShadow)">
    <rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{border_color}" stroke-width="2" />
    <path d="M 0 10 Q 0 0 10 0 L {w-10} 0 Q {w} 0 {w} 10 L {w} 4 L 0 4 Z" fill="{bar_color}" />
    
    <circle cx="22" cy="{h/2 + 2}" r="13" fill="{theme.get('tag_bg', '#E2E8F0')}" />
    <text x="22" y="{h/2 + 6.5}" font-size="11" font-weight="800" fill="{theme.get('primary', '#1E293B')}" text-anchor="middle">{initial}</text>
    
    {badge_text}
    
    <text x="44" y="27" font-size="15" font-weight="800" fill="#0F172A">{name}</text>
''')
            if dates:
                svg.append(f'''<text x="44" y="41" font-size="10.5" font-weight="600" fill="#475569">🗓 {dates}</text>''')
            elif notes and "Poginu" not in notes:
                svg.append(f'''<text x="44" y="41" font-size="10" font-weight="500" fill="#64748B">{notes}</text>''')
            svg.append('</g>\n')

        else:
            # Couple Card (Person + Spouse integrated)
            border_color = theme.get("border", "#94A3B8")
            bar_color = theme.get("primary", "#475569")
            initial_p = name[0] if name else "?"
            sp_name = spouse.get("name", "")
            initial_s = sp_name[0] if sp_name else "?"
            sp_notes = spouse.get("notes", "")

            badge_text = ""
            if "Poginu" in notes:
                badge_text = f'''<rect x="{w - 82}" y="6" width="76" height="18" rx="9" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/><text x="{w - 44}" y="19" font-size="9.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Mort guerre</text>'''

            svg.append(f'''
<g transform="translate({x}, {y})" filter="url(#boxShadow)">
    <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="{border_color}" stroke-width="2" />
    <path d="M 0 12 Q 0 0 12 0 L {w-12} 0 Q {w} 0 {w} 12 L {w} 4 L 0 4 Z" fill="{bar_color}" />
    
    <!-- Person Top Row -->
    <circle cx="20" cy="23" r="11" fill="{theme.get('tag_bg', '#E2E8F0')}" />
    <text x="20" y="27" font-size="10" font-weight="800" fill="{theme.get('primary', '#1E293B')}" text-anchor="middle">{initial_p}</text>
    <text x="38" y="27" font-size="14.5" font-weight="800" fill="#0F172A">{name}</text>
    {badge_text}
''')
            if dates:
                svg.append(f'''<text x="38" y="38" font-size="9.5" font-weight="600" fill="#64748B">🗓 {dates}</text>''')

            # Dividing Line with Marriage Rings Symbol
            svg.append(f'''
    <line x1="12" y1="44" x2="{w-12}" y2="44" stroke="#E2E8F0" stroke-width="1" />
    <circle cx="{w/2}" cy="44" r="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
    <text x="{w/2}" y="47.5" font-size="8" font-weight="800" fill="#E11D48" text-anchor="middle">∞</text>

    <!-- Spouse Bottom Row -->
    <circle cx="20" cy="62" r="11" fill="#F1F5F9" />
    <text x="20" y="66" font-size="10" font-weight="800" fill="#475569" text-anchor="middle">{initial_s}</text>
    <text x="38" y="66" font-size="14" font-weight="700" fill="#1E293B">{sp_name}</text>
''')
            if sp_notes and sp_notes != "Supruga" and sp_notes != "Suprug":
                svg.append(f'''<text x="38" y="76" font-size="9.5" font-weight="500" fill="#64748B">{sp_notes}</text>''')
            else:
                svg.append(f'''<text x="38" y="76" font-size="9.5" font-weight="600" fill="#94A3B8">Conjoint(e)</text>''')

            svg.append('</g>\n')

    svg.append('</svg>')
    return "".join(svg)

engine = BilateralPosterEngine(raw_data)
nodes, lines, max_h, top_off = engine.generate_full_bilateral()
svg_content = render_bilateral_svg(nodes, lines, max_h, top_off)

with open("Arbre_Genealogique_A0_Bilateral.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)
print("Generated Arbre_Genealogique_A0_Bilateral.svg")

# Also update the default Arbre_Genealogique_Complet.svg with this layout
with open("Arbre_Genealogique_Complet.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)
print("Updated Arbre_Genealogique_Complet.svg with Bilateral Layout")

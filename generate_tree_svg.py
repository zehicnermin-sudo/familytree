# -*- coding: utf-8 -*-
"""
Advanced High-Legibility Genealogical Tree & Interactive Application
Builds:
1. Crisp, high-contrast SVG files with large cards (320x120), font-size 26px/18px, bold typography, crystal-clear readability.
2. An interactive modern HTML5 tree explorer with D3-like SVG pan/zoom (up to 30x zoom), search, branch filter, and direct card-level inspection.
"""
import json

with open("family_tree_structured.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

THEMES = {
    "root": {
        "bg": "#F8FAFC", "card_bg": "#1E293B", "border": "#0F172A", "primary": "#0F172A",
        "text": "#FFFFFF", "subtext": "#94A3B8", "line": "#334155", "tag_bg": "#334155", "tag_text": "#F8FAFC"
    },
    "Branche Adem": {
        "name": "Branche Adem",
        "bg": "#F0FDF4", "card_bg": "#FFFFFF", "border": "#16A34A", "primary": "#15803D",
        "text": "#0F172A", "subtext": "#166534", "line": "#16A34A", "tag_bg": "#DCFCE7", "tag_text": "#14532D"
    },
    "Branche Meho": {
        "name": "Branche Meho",
        "bg": "#FFFBEB", "card_bg": "#FFFFFF", "border": "#D97706", "primary": "#B45309",
        "text": "#0F172A", "subtext": "#92400E", "line": "#D97706", "tag_bg": "#FEF3C7", "tag_text": "#78350F"
    },
    "Branche Osman": {
        "name": "Branche Osman",
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

CARD_W = 320
CARD_H = 118
SPOUSE_GAP = 36
SIBLING_GAP = 40
GEN_HEIGHT = 240
TOP_MARGIN = 320
LEFT_MARGIN = 260

def get_node_unit_width(person):
    has_spouse = "spouse" in person
    if has_spouse:
        return CARD_W * 2 + SPOUSE_GAP
    return CARD_W

class LayoutEngine:
    def __init__(self, data):
        self.data = data

    def layout_tree(self, root_node, filter_branch=None):
        def compute_width(p, branch_name):
            unit_w = get_node_unit_width(p)
            children = p.get("children", [])
            if not children:
                p["_subtree_w"] = unit_w
                return unit_w
            
            ch_widths = [compute_width(c, branch_name) for c in children]
            children_total_w = sum(ch_widths) + (len(children) - 1) * SIBLING_GAP
            p["_subtree_w"] = max(unit_w, children_total_w)
            return p["_subtree_w"]

        branches = root_node.get("children_branches", [])
        if filter_branch:
            branches = [b for b in branches if b["branch_name"] == filter_branch or b["id"] == filter_branch]

        for b in branches:
            compute_width(b["person"], b["branch_name"])

        total_branches_w = sum(b["person"]["_subtree_w"] for b in branches) + (len(branches) - 1) * 140
        
        all_nodes = []
        all_lines = []
        all_marriages = []

        root_x = LEFT_MARGIN + total_branches_w / 2
        root_y = TOP_MARGIN
        root_card = {
            "id": root_node["id"],
            "name": root_node["name"],
            "role": root_node.get("role", "Patriarche Fondateur"),
            "dates": root_node.get("dates", ""),
            "notes": root_node.get("notes", ""),
            "gen": 1,
            "branch": "root",
            "x": root_x - CARD_W / 2,
            "y": root_y,
            "w": CARD_W,
            "h": CARD_H,
            "is_root": True
        }
        all_nodes.append(root_card)

        cur_x = LEFT_MARGIN
        gen2_y = TOP_MARGIN + GEN_HEIGHT
        branch_anchor_pts = []

        for b in branches:
            p = b["person"]
            b_name = b["branch_name"]
            b_w = p["_subtree_w"]
            b_center_x = cur_x + b_w / 2

            def assign_positions(node, center_x, y, branch):
                unit_w = get_node_unit_width(node)
                has_sp = "spouse" in node
                gen = node.get("gen", 2)

                if has_sp:
                    p_x = center_x - (CARD_W + SPOUSE_GAP / 2)
                    sp_x = center_x + SPOUSE_GAP / 2
                    
                    p_card = {
                        "id": node.get("id"),
                        "name": node.get("name"),
                        "dates": node.get("dates", ""),
                        "notes": node.get("notes", ""),
                        "gen": gen,
                        "branch": branch,
                        "x": p_x,
                        "y": y,
                        "w": CARD_W,
                        "h": CARD_H
                    }
                    all_nodes.append(p_card)

                    sp = node["spouse"]
                    sp_card = {
                        "id": node.get("id") + "_sp",
                        "name": sp.get("name"),
                        "dates": sp.get("dates", ""),
                        "notes": sp.get("notes", "Supruga/Suprug"),
                        "gen": gen,
                        "branch": branch,
                        "x": sp_x,
                        "y": y,
                        "w": CARD_W,
                        "h": CARD_H,
                        "is_spouse": True,
                        "spouse_of": node.get("name")
                    }
                    all_nodes.append(sp_card)

                    all_marriages.append({
                        "x1": p_x + CARD_W,
                        "y1": y + CARD_H / 2,
                        "x2": sp_x,
                        "y2": y + CARD_H / 2,
                        "branch": branch
                    })
                else:
                    p_x = center_x - CARD_W / 2
                    p_card = {
                        "id": node.get("id"),
                        "name": node.get("name"),
                        "dates": node.get("dates", ""),
                        "notes": node.get("notes", ""),
                        "gen": gen,
                        "branch": branch,
                        "x": p_x,
                        "y": y,
                        "w": CARD_W,
                        "h": CARD_H
                    }
                    all_nodes.append(p_card)

                children = node.get("children", [])
                if children:
                    parent_out_x = center_x
                    parent_out_y = y + CARD_H
                    child_in_y = y + GEN_HEIGHT

                    ch_widths = [c["_subtree_w"] for c in children]
                    total_ch_w = sum(ch_widths) + (len(children) - 1) * SIBLING_GAP
                    ch_start_x = center_x - total_ch_w / 2

                    ch_cur_x = ch_start_x
                    bus_y = parent_out_y + (GEN_HEIGHT - CARD_H) / 2

                    all_lines.append({
                        "type": "stem",
                        "x1": parent_out_x,
                        "y1": parent_out_y,
                        "x2": parent_out_x,
                        "y2": bus_y,
                        "branch": branch
                    })

                    child_center_xs = []
                    for c, cw in zip(children, ch_widths):
                        c_center_x = ch_cur_x + cw / 2
                        child_center_xs.append(c_center_x)
                        assign_positions(c, c_center_x, child_in_y, branch)
                        
                        all_lines.append({
                            "type": "stem",
                            "x1": c_center_x,
                            "y1": bus_y,
                            "x2": c_center_x,
                            "y2": child_in_y,
                            "branch": branch
                        })
                        ch_cur_x += cw + SIBLING_GAP

                    min_ch_x = min(child_center_xs)
                    max_ch_x = max(child_center_xs)
                    bus_left = min(parent_out_x, min_ch_x)
                    bus_right = max(parent_out_x, max_ch_x)

                    all_lines.append({
                        "type": "bus",
                        "x1": bus_left,
                        "y1": bus_y,
                        "x2": bus_right,
                        "y2": bus_y,
                        "branch": branch
                    })

            assign_positions(p, b_center_x, gen2_y, b_name)
            branch_anchor_pts.append(b_center_x)
            cur_x += b_w + 140

        root_bus_y = root_y + CARD_H + (GEN_HEIGHT - CARD_H) / 2
        all_lines.append({
            "type": "stem",
            "x1": root_x,
            "y1": root_y + CARD_H,
            "x2": root_x,
            "y2": root_bus_y,
            "branch": "root"
        })
        min_b_x = min(branch_anchor_pts)
        max_b_x = max(branch_anchor_pts)
        all_lines.append({
            "type": "bus",
            "x1": min_b_x,
            "y1": root_bus_y,
            "x2": max_b_x,
            "y2": root_bus_y,
            "branch": "root"
        })
        for bx in branch_anchor_pts:
            all_lines.append({
                "type": "stem",
                "x1": bx,
                "y1": root_bus_y,
                "x2": bx,
                "y2": gen2_y,
                "branch": "root"
            })

        return all_nodes, all_lines, all_marriages

def generate_svg(nodes, lines, marriages, title="Arbre Généalogique", subtitle="Descendance d'Ibrahim", is_branch_view=False):
    min_x = min(n["x"] for n in nodes) - 120
    max_x = max(n["x"] + n["w"] for n in nodes) + 120
    min_y = 0
    max_y = max(n["y"] + n["h"] for n in nodes) + 160

    width = max_x - min_x
    height = max_y - min_y

    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {width} {height}" width="{width}" height="{height}" style="background-color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
<defs>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="135%">
        <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.08" flood-color="#0F172A" />
        <feDropShadow dx="0" dy="12" stdDeviation="16" flood-opacity="0.05" flood-color="#0F172A" />
    </filter>
    <filter id="rootShadow" x="-15%" y="-15%" width="130%" height="135%">
        <feDropShadow dx="0" dy="8" stdDeviation="12" flood-opacity="0.2" flood-color="#0F172A" />
    </filter>
    <linearGradient id="rootGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1E293B" />
        <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
</defs>
''')

    # Generational Background Bands & Timeline Markers
    max_gen = max(n.get("gen", 1) for n in nodes)
    for g in range(1, max_gen + 1):
        gy = TOP_MARGIN + (g - 1) * GEN_HEIGHT - 35
        gh = GEN_HEIGHT
        bg_fill = "#F8FAFC" if g % 2 != 0 else "#F1F5F9"
        svg_parts.append(f'''<rect x="{min_x}" y="{gy}" width="{width}" height="{gh}" fill="{bg_fill}" opacity="0.6" />''')
        # Generation label badge on the left
        svg_parts.append(f'''
<g transform="translate({min_x + 40}, {gy + 60})">
    <rect x="0" y="0" width="200" height="46" rx="23" fill="#1E293B" opacity="0.9" />
    <text x="100" y="30" font-size="18" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">GÉNÉRATION {g}</text>
</g>''')

    # Header & Title Block
    svg_parts.append(f'''
<!-- Header -->
<g transform="translate({(min_x + max_x)/2}, 60)" text-anchor="middle">
    <rect x="-500" y="0" width="1000" height="140" rx="24" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2.5" filter="url(#cardShadow)"/>
    <text x="0" y="58" font-size="38" font-weight="900" fill="#0F172A" letter-spacing="-0.5">{title}</text>
    <text x="0" y="102" font-size="22" font-weight="600" fill="#475569">{subtitle} • 401 Personnes • 8 Générations</text>
</g>
''')

    # Legend Block
    legend_x = min_x + 280
    legend_y = 60
    svg_parts.append(f'''
<!-- Légende -->
<g transform="translate({legend_x}, {legend_y})">
    <rect x="0" y="0" width="460" height="150" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" filter="url(#cardShadow)"/>
    <text x="24" y="36" font-size="18" font-weight="800" fill="#1E293B" letter-spacing="0.5">LÉGENDE DES BRANCHES</text>
    
    <circle cx="34" cy="70" r="9" fill="#16A34A" />
    <text x="54" y="77" font-size="17" font-weight="700" fill="#14532D">Branche Adem (177 p.)</text>

    <circle cx="260" cy="70" r="9" fill="#D97706" />
    <text x="280" y="77" font-size="17" font-weight="700" fill="#78350F">Branche Meho (69 p.)</text>

    <circle cx="34" cy="110" r="9" fill="#0284C7" />
    <text x="54" y="117" font-size="17" font-weight="700" fill="#0C4A6E">Branche Osman (152 p.)</text>

    <circle cx="260" cy="110" r="9" fill="#E11D48" />
    <text x="280" y="117" font-size="17" font-weight="700" fill="#881337">Nurif &amp; Paša</text>
</g>
''')

    # Draw Connector Lines
    for line in lines:
        b_theme = THEMES.get(line["branch"], THEMES["root"])
        stroke_color = b_theme["border"] if line["branch"] != "root" else "#64748B"
        stroke_w = "3.5"
        svg_parts.append(f'''<line x1="{line['x1']}" y1="{line['y1']}" x2="{line['x2']}" y2="{line['y2']}" stroke="{stroke_color}" stroke-width="{stroke_w}" stroke-linecap="round" stroke-linejoin="round" />''')

    # Draw Marriage Connectors
    for m in marriages:
        b_theme = THEMES.get(m["branch"], THEMES["root"])
        svg_parts.append(f'''
<g>
    <line x1="{m['x1']}" y1="{m['y1']-4}" x2="{m['x2']}" y2="{m['y2']-4}" stroke="#94A3B8" stroke-width="3" />
    <line x1="{m['x1']}" y1="{m['y1']+4}" x2="{m['x2']}" y2="{m['y2']+4}" stroke="#94A3B8" stroke-width="3" />
    <circle cx="{(m['x1']+m['x2'])/2}" cy="{m['y1']}" r="15" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2.5" />
    <text x="{(m['x1']+m['x2'])/2}" y="{m['y1']+6}" font-size="16" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>
</g>
''')

    # Draw Person Cards
    for n in nodes:
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        is_root = n.get("is_root", False)
        is_spouse = n.get("is_spouse", False)
        branch = n.get("branch", "root")
        theme = THEMES.get(branch, THEMES["root"])

        name = n["name"]
        dates = n.get("dates", "")
        notes = n.get("notes", "")

        if is_root:
            svg_parts.append(f'''
<g transform="translate({x}, {y})" filter="url(#rootShadow)">
    <rect x="0" y="0" width="{w}" height="{h}" rx="18" fill="url(#rootGrad)" stroke="#475569" stroke-width="3.5" />
    <circle cx="46" cy="{h/2}" r="26" fill="#334155" />
    <text x="46" y="{h/2 + 8}" font-size="24" font-weight="900" fill="#F8FAFC" text-anchor="middle">👑</text>
    <text x="90" y="52" font-size="30" font-weight="900" fill="#FFFFFF">{name}</text>
    <text x="90" y="86" font-size="18" font-weight="700" fill="#94A3B8">Patriarche Fondateur</text>
</g>
''')
        else:
            border_color = theme["border"]
            header_bar_color = theme["primary"] if not is_spouse else "#64748B"
            bg_color = "#FFFFFF" if not is_spouse else "#F8FAFC"
            border_w = "2.5" if not is_spouse else "2"
            border_dash = "" if not is_spouse else 'stroke-dasharray="6,4"'

            badge_svg = ""
            if "Poginu" in notes:
                badge_svg = f'''<rect x="{w - 118}" y="10" width="106" height="26" rx="13" fill="#FEE2E2" stroke="#EF4444" stroke-width="1.5"/><text x="{w - 65}" y="28" font-size="13" font-weight="800" fill="#B91C1C" text-anchor="middle">Mort guerre</text>'''
            elif is_spouse:
                badge_svg = f'''<rect x="{w - 105}" y="10" width="95" height="26" rx="13" fill="{theme['tag_bg']}" stroke="{theme['border']}" stroke-width="1"/><text x="{w - 57}" y="28" font-size="13" font-weight="800" fill="{theme['tag_text']}" text-anchor="middle">Conjoint(e)</text>'''
            elif notes:
                clean_note = notes.replace("u. ", "née ").replace("r. ", "d' ")
                if len(clean_note) > 18:
                    clean_note = clean_note[:16] + "…"
                badge_svg = f'''<rect x="{w - 130}" y="10" width="120" height="26" rx="13" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/><text x="{w - 70}" y="28" font-size="12.5" font-weight="700" fill="#334155" text-anchor="middle">{clean_note}</text>'''

            initial = name[0] if name else "?"
            avatar_bg = theme["tag_bg"] if not is_spouse else "#E2E8F0"
            avatar_text_color = theme["primary"] if not is_spouse else "#334155"

            y_name = 54 if not dates and not notes else 48
            
            svg_parts.append(f'''
<g transform="translate({x}, {y})" filter="url(#cardShadow)">
    <rect x="0" y="0" width="{w}" height="{h}" rx="16" fill="{bg_color}" stroke="{border_color}" stroke-width="{border_w}" {border_dash} />
    <path d="M 0 16 Q 0 0 16 0 L {w-16} 0 Q {w} 0 {w} 16 L {w} 6 L 0 6 Z" fill="{header_bar_color}" />
    
    <!-- Avatar -->
    <circle cx="36" cy="{h/2 + 4}" r="20" fill="{avatar_bg}" />
    <text x="36" y="{h/2 + 11}" font-size="18" font-weight="900" fill="{avatar_text_color}" text-anchor="middle">{initial}</text>
    
    <!-- Badges -->
    {badge_svg}
    
    <!-- Text -->
    <text x="68" y="{y_name}" font-size="24" font-weight="800" fill="#0F172A">{name}</text>
''')
            if dates:
                svg_parts.append(f'''<text x="68" y="{y_name + 28}" font-size="17" font-weight="700" fill="#475569">🗓 {dates}</text>''')
            elif notes and not is_spouse:
                svg_parts.append(f'''<text x="68" y="{y_name + 28}" font-size="16" font-weight="600" fill="#475569">{notes}</text>''')
            elif is_spouse and notes != "Supruga" and notes != "Suprug":
                svg_parts.append(f'''<text x="68" y="{y_name + 28}" font-size="16" font-weight="600" fill="#475569">{notes}</text>''')

            svg_parts.append('</g>\n')

    svg_parts.append('</svg>')
    return "".join(svg_parts)

engine = LayoutEngine(raw_data)

# 1. Complete Tree SVG
nodes_all, lines_all, marr_all = engine.layout_tree(raw_data["root"])
svg_complete = generate_svg(nodes_all, lines_all, marr_all, title="Arbre Généalogique Complet", subtitle="Descendance d'Ibrahim (Toutes branches)")
with open("Arbre_Genealogique_Complet.svg", "w", encoding="utf-8") as f:
    f.write(svg_complete)
print("Updated Arbre_Genealogique_Complet.svg with High Legibility")

# 2. Branch Adem SVG
nodes_adem, lines_adem, marr_adem = engine.layout_tree(raw_data["root"], filter_branch="Branche Adem")
svg_adem = generate_svg(nodes_adem, lines_adem, marr_adem, title="Branche Adem (1855 – 1938)", subtitle="Descendance d'Adem & Mejra • 177 personnes", is_branch_view=True)
with open("Branche_Adem.svg", "w", encoding="utf-8") as f:
    f.write(svg_adem)
print("Updated Branche_Adem.svg with High Legibility")

# 3. Branch Meho SVG
nodes_meho, lines_meho, marr_meho = engine.layout_tree(raw_data["root"], filter_branch="Branche Meho")
svg_meho = generate_svg(nodes_meho, lines_meho, marr_meho, title="Branche Meho (1867 – 1941)", subtitle="Descendance de Meho & Cura • 69 personnes", is_branch_view=True)
with open("Branche_Meho.svg", "w", encoding="utf-8") as f:
    f.write(svg_meho)
print("Updated Branche_Meho.svg with High Legibility")

# 4. Branch Osman SVG
nodes_osman, lines_osman, marr_osman = engine.layout_tree(raw_data["root"], filter_branch="Branche Osman")
svg_osman = generate_svg(nodes_osman, lines_osman, marr_osman, title="Branche Osman (1860 – 1937)", subtitle="Descendance d'Osman & Hata • 152 personnes", is_branch_view=True)
with open("Branche_Osman.svg", "w", encoding="utf-8") as f:
    f.write(svg_osman)
print("Updated Branche_Osman.svg with High Legibility")

# 5. Interactive HTML Application with Powerful Zoom (up to 30x), Direct Card View, Search & Preset Focus
html_app = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arbre Généalogique - Visualisateur Haute Résolution & Lisibilité</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090d16;
            --surface: #1e293b;
            --surface-hover: #334155;
            --primary: #3b82f6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: var(--bg-dark);
            color: var(--text-main);
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        header {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            z-index: 50;
            gap: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }
        .brand h1 {
            font-size: 1.1rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .brand p {
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        .btn-group {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .tab-btn {
            background: var(--surface);
            color: var(--text-main);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .tab-btn:hover {
            background: var(--surface-hover);
            transform: translateY(-1px);
        }
        .tab-btn.active {
            background: #2563eb;
            border-color: #60a5fa;
            color: #fff;
            box-shadow: 0 0 14px rgba(37, 99, 235, 0.45);
        }
        .badge {
            background: rgba(255, 255, 255, 0.15);
            padding: 2px 7px;
            border-radius: 12px;
            font-size: 0.72rem;
        }
        .search-container {
            position: relative;
        }
        .search-box {
            background: var(--surface);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 8px 12px 8px 34px;
            color: #fff;
            font-size: 0.85rem;
            width: 220px;
            outline: none;
            transition: all 0.2s;
        }
        .search-box:focus {
            width: 280px;
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
        }
        .search-icon {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }
        .dropdown {
            position: absolute;
            top: 45px;
            right: 0;
            width: 300px;
            max-height: 380px;
            overflow-y: auto;
            background: var(--surface);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            box-shadow: 0 16px 36px rgba(0,0,0,0.6);
            display: none;
            flex-direction: column;
            z-index: 100;
        }
        .dropdown-item {
            padding: 10px 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            cursor: pointer;
            transition: background 0.15s;
        }
        .dropdown-item:hover {
            background: var(--surface-hover);
        }
        .dropdown-name {
            font-weight: 700;
            color: #fff;
            font-size: 0.85rem;
        }
        .dropdown-meta {
            font-size: 0.72rem;
            color: var(--text-muted);
            margin-top: 2px;
        }
        #canvasViewport {
            flex: 1;
            position: relative;
            background: #f1f5f9;
            overflow: hidden;
            cursor: grab;
        }
        #canvasViewport:active {
            cursor: grabbing;
        }
        #svgWrapper {
            position: absolute;
            top: 0;
            left: 0;
            transform-origin: 0 0;
            will-change: transform;
        }
        .controls-toolbar {
            position: absolute;
            bottom: 24px;
            right: 24px;
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 14px;
            padding: 6px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.35);
            z-index: 40;
        }
        .tool-btn {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--surface);
            color: var(--text-main);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            cursor: pointer;
            font-weight: 800;
            font-size: 1.2rem;
            transition: all 0.15s;
        }
        .tool-btn:hover {
            background: #2563eb;
            color: #fff;
        }
        .zoom-badge {
            position: absolute;
            bottom: 24px;
            left: 24px;
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            padding: 10px 18px;
            font-size: 0.82rem;
            color: var(--text-muted);
            display: flex;
            gap: 16px;
            z-index: 40;
        }
        .zoom-badge strong {
            color: #fff;
        }
        @media print {
            header, .controls-toolbar, .zoom-badge { display: none !important; }
            body, #canvasViewport { height: auto; overflow: visible; background: #fff; }
            #svgWrapper { transform: none !important; position: static; }
        }
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <h1>Arbre Généalogique de la Famille</h1>
            <p>Descendance d'Ibrahim • Redesign Haute Lisibilité</p>
        </div>

        <div class="btn-group">
            <button class="tab-btn active" onclick="loadTree('Arbre_Genealogique_Complet.svg', this)">Vue Globale <span class="badge">401</span></button>
            <button class="tab-btn" onclick="loadTree('Branche_Adem.svg', this)" style="border-left: 3px solid #16a34a;">Branche Adem <span class="badge">177</span></button>
            <button class="tab-btn" onclick="loadTree('Branche_Meho.svg', this)" style="border-left: 3px solid #d97706;">Branche Meho <span class="badge">69</span></button>
            <button class="tab-btn" onclick="loadTree('Branche_Osman.svg', this)" style="border-left: 3px solid #0284c7;">Branche Osman <span class="badge">152</span></button>
        </div>

        <div class="btn-group">
            <div class="search-container">
                <span class="search-icon">🔍</span>
                <input type="text" class="search-box" id="searchInput" placeholder="Rechercher un membre..." oninput="onSearch(this.value)">
                <div class="dropdown" id="searchDropdown"></div>
            </div>
            <button class="tab-btn" onclick="focusRoot()" title="Recentrer sur l'ancêtre fondateur">👑 Ibrahim</button>
            <button class="tab-btn" onclick="window.print()" title="Imprimer ou exporter en PDF">🖨 Imprimer</button>
        </div>
    </header>

    <div id="canvasViewport">
        <div id="svgWrapper"></div>
    </div>

    <div class="controls-toolbar">
        <button class="tool-btn" onclick="zoom(1.35)" title="Zoom avant (Molette vers le haut)">+</button>
        <button class="tool-btn" onclick="zoom(0.74)" title="Zoom arrière (Molette vers le bas)">−</button>
        <button class="tool-btn" onclick="resetToOptimalReading()" title="Lisibilité optimale (100%)">1:1</button>
        <button class="tool-btn" onclick="fitView()" title="Vue d'ensemble">⛶</button>
    </div>

    <div class="zoom-badge">
        <div>Zoom: <strong id="zoomLevel">100%</strong></div>
        <div>Total: <strong>401 membres</strong></div>
        <div>Statut: <strong>Netteté Vectorielle Maximale</strong></div>
    </div>

    <script>
        let scale = 1.0;
        let posX = 100;
        let posY = 50;
        let isDragging = false;
        let startX, startY;
        let currentSvgUrl = 'Arbre_Genealogique_Complet.svg';
        let svgElement = null;

        const viewport = document.getElementById('canvasViewport');
        const wrapper = document.getElementById('svgWrapper');
        const zoomLabel = document.getElementById('zoomLevel');

        function updateTransform() {
            wrapper.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
            zoomLabel.textContent = Math.round(scale * 100) + '%';
        }

        function loadTree(url, btnElement) {
            currentSvgUrl = url;
            if (btnElement) {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                btnElement.classList.add('active');
            }
            fetch(url)
                .then(res => res.text())
                .then(svgText => {
                    wrapper.innerHTML = svgText;
                    svgElement = wrapper.querySelector('svg');
                    resetToOptimalReading();
                });
        }

        function zoom(factor, clientX, clientY) {
            let oldScale = scale;
            let newScale = scale * factor;
            newScale = Math.min(Math.max(0.04, newScale), 10.0);
            
            if (clientX !== undefined && clientY !== undefined) {
                const rect = viewport.getBoundingClientRect();
                const mouseX = clientX - rect.left;
                const mouseY = clientY - rect.top;
                posX = mouseX - (mouseX - posX) * (newScale / oldScale);
                posY = mouseY - (mouseY - posY) * (newScale / oldScale);
            }
            scale = newScale;
            updateTransform();
        }

        function resetToOptimalReading() {
            scale = 0.85;
            const vw = viewport.clientWidth;
            if (svgElement) {
                const vb = svgElement.viewBox.baseVal;
                posX = (vw - vb.width * scale) / 2;
                posY = 40;
            } else {
                posX = 80;
                posY = 40;
            }
            updateTransform();
        }

        function fitView() {
            if (!svgElement) return;
            const vb = svgElement.viewBox.baseVal;
            const vw = viewport.clientWidth;
            const vh = viewport.clientHeight;
            scale = Math.min(vw / vb.width, vh / vb.height) * 0.94;
            posX = (vw - vb.width * scale) / 2;
            posY = 20;
            updateTransform();
        }

        function focusRoot() {
            scale = 1.0;
            const vw = viewport.clientWidth;
            if (svgElement) {
                const vb = svgElement.viewBox.baseVal;
                posX = vw / 2 - (vb.x + vb.width / 2) * scale;
                posY = 80;
            }
            updateTransform();
        }

        viewport.addEventListener('mousedown', (e) => {
            if (e.target.closest('.controls-toolbar') || e.target.closest('.zoom-badge')) return;
            isDragging = true;
            startX = e.clientX - posX;
            startY = e.clientY - posY;
        });

        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            posX = e.clientX - startX;
            posY = e.clientY - startY;
            updateTransform();
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
        });

        viewport.addEventListener('wheel', (e) => {
            e.preventDefault();
            const factor = e.deltaY < 0 ? 1.18 : 0.84;
            zoom(factor, e.clientX, e.clientY);
        }, { passive: false });

        function onSearch(val) {
            const dropdown = document.getElementById('searchDropdown');
            if (!val || val.trim().length < 2) {
                dropdown.style.display = 'none';
                return;
            }
            val = val.toLowerCase().trim();
            const cards = wrapper.querySelectorAll('g[filter]');
            const results = [];

            cards.forEach(card => {
                const nameNode = card.querySelector('text[font-size="24"], text[font-size="30"]');
                if (nameNode) {
                    const name = nameNode.textContent;
                    if (name.toLowerCase().includes(val)) {
                        const tr = card.getAttribute('transform');
                        const m = tr.match(/translate\(([^,]+),\s*([^)]+)\)/);
                        if (m) {
                            results.push({
                                name: name,
                                x: parseFloat(m[1]),
                                y: parseFloat(m[2])
                            });
                        }
                    }
                }
            });

            if (results.length > 0) {
                dropdown.innerHTML = results.slice(0, 12).map(r => `
                    <div class="dropdown-item" onclick="focusCoords(${r.x}, ${r.y})">
                        <div class="dropdown-name">${r.name}</div>
                        <div class="dropdown-meta">Cliquer pour centrer la vue</div>
                    </div>
                `).join('');
                dropdown.style.display = 'flex';
            } else {
                dropdown.innerHTML = '<div class="dropdown-item" style="color:#94a3b8;">Aucun membre trouvé</div>';
                dropdown.style.display = 'flex';
            }
        }

        function focusCoords(x, y) {
            document.getElementById('searchDropdown').style.display = 'none';
            scale = 1.25;
            const vw = viewport.clientWidth;
            const vh = viewport.clientHeight;
            posX = vw / 2 - (x + 160) * scale;
            posY = vh / 2 - (y + 60) * scale;
            updateTransform();
        }

        // Initialize
        loadTree('Arbre_Genealogique_Complet.svg');
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_app)
print("Updated index.html (High Legibility Interactive Explorer)")

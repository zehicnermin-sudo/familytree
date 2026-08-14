# -*- coding: utf-8 -*-
"""
Update branch SVGs and interactive viewer with Blue/Pink gender styling.
"""
import json

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

MALE_COLOR = "#2563EB"
MALE_BG = "#F0F7FF"
MALE_AVATAR_BG = "#DBEAFE"
MALE_TEXT = "#1E40AF"

FEMALE_COLOR = "#EC4899"
FEMALE_BG = "#FFF1F6"
FEMALE_AVATAR_BG = "#FCE7F3"
FEMALE_TEXT = "#BE185D"

CARD_W = 280
CARD_H = 100
SPOUSE_GAP = 28
SIBLING_GAP = 30
GEN_HEIGHT = 200
TOP_MARGIN = 260
LEFT_MARGIN = 200

def get_node_unit_width(person):
    if "spouse" in person:
        return CARD_W * 2 + SPOUSE_GAP
    return CARD_W

def render_branch_svg(person_node, branch_title, branch_subtitle):
    # Compute recursive widths
    def compute_width(p):
        unit_w = get_node_unit_width(p)
        children = p.get("children", [])
        if not children:
            p["_w"] = unit_w
            return unit_w
        ch_w = [compute_width(c) for c in children]
        total_ch_w = sum(ch_w) + (len(children) - 1) * SIBLING_GAP
        p["_w"] = max(unit_w, total_ch_w)
        return p["_w"]

    compute_width(person_node)
    
    all_nodes = []
    all_lines = []
    all_marriages = []

    def place_node(node, center_x, y):
        has_sp = "spouse" in node
        gen = node.get("gen", 2)
        node_gender = node.get("gender", "M")

        if has_sp:
            p_x = center_x - (CARD_W + SPOUSE_GAP / 2)
            sp_x = center_x + SPOUSE_GAP / 2

            all_nodes.append({
                "name": node.get("name"),
                "dates": node.get("dates", ""),
                "notes": node.get("notes", ""),
                "gender": node_gender,
                "x": p_x, "y": y, "w": CARD_W, "h": CARD_H
            })

            sp = node["spouse"]
            sp_gender = sp.get("gender", "F" if node_gender == "M" else "M")
            all_nodes.append({
                "name": sp.get("name"),
                "dates": sp.get("dates", ""),
                "notes": sp.get("notes", "Supruga/Suprug"),
                "gender": sp_gender,
                "is_spouse": True,
                "x": sp_x, "y": y, "w": CARD_W, "h": CARD_H
            })

            all_marriages.append({
                "x1": p_x + CARD_W, "y1": y + CARD_H / 2,
                "x2": sp_x, "y2": y + CARD_H / 2
            })
        else:
            all_nodes.append({
                "name": node.get("name"),
                "dates": node.get("dates", ""),
                "notes": node.get("notes", ""),
                "gender": node_gender,
                "x": center_x - CARD_W / 2, "y": y, "w": CARD_W, "h": CARD_H
            })

        children = node.get("children", [])
        if children:
            parent_out_x = center_x
            parent_out_y = y + CARD_H
            child_in_y = y + GEN_HEIGHT

            ch_widths = [c["_w"] for c in children]
            total_ch_w = sum(ch_widths) + (len(children) - 1) * SIBLING_GAP
            ch_start_x = center_x - total_ch_w / 2

            bus_y = parent_out_y + (GEN_HEIGHT - CARD_H) / 2
            all_lines.append({"x1": parent_out_x, "y1": parent_out_y, "x2": parent_out_x, "y2": bus_y})

            ch_cur_x = ch_start_x
            child_xs = []
            for c, cw in zip(children, ch_widths):
                c_cx = ch_cur_x + cw / 2
                child_xs.append(c_cx)
                place_node(c, c_cx, child_in_y)
                all_lines.append({"x1": c_cx, "y1": bus_y, "x2": c_cx, "y2": child_in_y})
                ch_cur_x += cw + SIBLING_GAP

            all_lines.append({"x1": min(child_xs), "y1": bus_y, "x2": max(child_xs), "y2": bus_y})

    root_cx = LEFT_MARGIN + person_node["_w"] / 2
    place_node(person_node, root_cx, TOP_MARGIN)

    min_x = min(n["x"] for n in all_nodes) - 80
    max_x = max(n["x"] + n["w"] for n in all_nodes) + 80
    min_y = 0
    max_y = max(n["y"] + n["h"] for n in all_nodes) + 120

    width = int(max_x - min_x)
    height = int(max_y - min_y)

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {width} {height}" width="{width}" height="{height}" style="background-color: #F8FAFC; font-family: 'Plus Jakarta Sans', sans-serif;">
<defs>
    <filter id="shadow" x="-10%" y="-10%" width="125%" height="130%">
        <feDropShadow dx="0" dy="2" stdDeviation="4" flood-opacity="0.08" flood-color="#0F172A" />
    </filter>
    <linearGradient id="maleGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#2563EB" /><stop offset="100%" stop-color="#3B82F6" /></linearGradient>
    <linearGradient id="femaleGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#EC4899" /><stop offset="100%" stop-color="#F43F5E" /></linearGradient>
</defs>
''')

    # Header
    svg.append(f'''
<g transform="translate({(min_x + max_x)/2}, 50)" text-anchor="middle">
    <rect x="-400" y="0" width="800" height="110" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2" filter="url(#shadow)"/>
    <text x="0" y="46" font-size="28" font-weight="900" fill="#0F172A">{branch_title}</text>
    <text x="0" y="78" font-size="16" font-weight="700" fill="#475569">{branch_subtitle}</text>
</g>
<g transform="translate({min_x + 60}, 50)">
    <rect x="0" y="0" width="280" height="90" rx="12" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" filter="url(#shadow)"/>
    <text x="14" y="24" font-size="12" font-weight="800" fill="#1E293B">LEGENDA SPOLOVA</text>
    <rect x="14" y="36" width="12" height="12" rx="3" fill="#DBEAFE" stroke="#2563EB" stroke-width="1.5"/>
    <text x="32" y="46" font-size="11.5" font-weight="800" fill="#1E40AF">Muška osoba (Plava)</text>
    <rect x="14" y="60" width="12" height="12" rx="3" fill="#FCE7F3" stroke="#EC4899" stroke-width="1.5"/>
    <text x="32" y="70" font-size="11.5" font-weight="800" fill="#BE185D">Ženska osoba (Roze)</text>
</g>
''')

    # Lines
    for line in all_lines:
        svg.append(f'''<line x1="{line['x1']}" y1="{line['y1']}" x2="{line['x2']}" y2="{line['y2']}" stroke="#64748B" stroke-width="2.2" stroke-linecap="round" />''')

    for m in all_marriages:
        svg.append(f'''
<g>
    <line x1="{m['x1']}" y1="{m['y1']-3}" x2="{m['x2']}" y2="{m['y2']-3}" stroke="#94A3B8" stroke-width="2.5" />
    <line x1="{m['x1']}" y1="{m['y1']+3}" x2="{m['x2']}" y2="{m['y2']+3}" stroke="#94A3B8" stroke-width="2.5" />
    <circle cx="{(m['x1']+m['x2'])/2}" cy="{m['y1']}" r="11" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" />
    <text x="{(m['x1']+m['x2'])/2}" y="{m['y1']+4}" font-size="11" font-weight="900" fill="#E11D48" text-anchor="middle">∞</text>
</g>''')

    # Cards
    for n in all_nodes:
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        name = n["name"]
        dates = n.get("dates", "")
        notes = n.get("notes", "")
        gender = n.get("gender", "M")
        is_male = (gender == "M")

        border_c = MALE_COLOR if is_male else FEMALE_COLOR
        bar_c = "url(#maleGrad)" if is_male else "url(#femaleGrad)"
        card_bg = MALE_BG if is_male else FEMALE_BG
        av_bg = MALE_AVATAR_BG if is_male else FEMALE_AVATAR_BG
        av_text = MALE_TEXT if is_male else FEMALE_TEXT
        initial = name[0] if name else "?"

        badge = ""
        if "Poginu" in notes:
            badge = f'''<rect x="{w - 95}" y="8" width="85" height="20" rx="10" fill="#FEE2E2" stroke="#EF4444" stroke-width="1"/><text x="{w - 52}" y="22" font-size="10.5" font-weight="800" fill="#B91C1C" text-anchor="middle">Poginuo/la</text>'''
        elif n.get("is_spouse"):
            badge = f'''<rect x="{w - 85}" y="8" width="75" height="20" rx="10" fill="{FEMALE_AVATAR_BG if not is_male else MALE_AVATAR_BG}" stroke="{border_c}" stroke-width="1"/><text x="{w - 47}" y="22" font-size="10" font-weight="800" fill="{av_text}" text-anchor="middle">Supruga/g</text>'''
        elif notes:
            badge = f'''<rect x="{w - 95}" y="8" width="85" height="20" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/><text x="{w - 52}" y="22" font-size="10" font-weight="700" fill="#334155" text-anchor="middle">{notes[:12]}</text>'''

        svg.append(f'''
<g transform="translate({x}, {y})" filter="url(#shadow)">
    <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="{card_bg}" stroke="{border_c}" stroke-width="2" />
    <path d="M 0 12 Q 0 0 12 0 L {w-12} 0 Q {w} 0 {w} 12 L {w} 5 L 0 5 Z" fill="{bar_c}" />
    
    <circle cx="28" cy="{h/2 + 2}" r="16" fill="{av_bg}" />
    <text x="28" y="{h/2 + 8}" font-size="14" font-weight="900" fill="{av_text}" text-anchor="middle">{initial}</text>
    
    {badge}
    
    <text x="56" y="44" font-size="19" font-weight="800" fill="#0F172A">{name}</text>
''')
        if dates:
            svg.append(f'''<text x="56" y="70" font-size="13" font-weight="700" fill="#475569">🗓 {dates}</text>''')
        elif notes and not n.get("is_spouse"):
            svg.append(f'''<text x="56" y="70" font-size="13" font-weight="600" fill="#64748B">{notes}</text>''')
        elif n.get("is_spouse") and notes != "Supruga" and notes != "Suprug":
            svg.append(f'''<text x="56" y="70" font-size="13" font-weight="600" fill="#64748B">{notes}</text>''')

        svg.append('</g>\n')

    svg.append('</svg>')
    return "".join(svg)

# Generate dedicated branch SVGs with gender colors
for b in raw_data["root"]["children_branches"]:
    b_name = b["branch_name"]
    p = b["person"]
    if b_name == "Branche Adem":
        svg_code = render_branch_svg(p, "Branche Adem (1855 – 1938)", "177 Članova • Plava = Muški, Roze = Ženski")
        with open("Branche_Adem.svg", "w", encoding="utf-8") as f:
            f.write(svg_code)
    elif b_name == "Branche Meho":
        svg_code = render_branch_svg(p, "Branche Meho (1867 – 1941)", "69 Članova • Plava = Muški, Roze = Ženski")
        with open("Branche_Meho.svg", "w", encoding="utf-8") as f:
            f.write(svg_code)
    elif b_name == "Branche Osman":
        svg_code = render_branch_svg(p, "Branche Osman (1860 – 1937)", "152 Člana • Plava = Muški, Roze = Ženski")
        with open("Branche_Osman.svg", "w", encoding="utf-8") as f:
            f.write(svg_code)

print("All branch SVGs successfully updated with Blue/Pink gender code!")

# -*- coding: utf-8 -*-
"""
Bilateral (Center-Out) Genealogical Layout Engine
Builds an A0/A1 print-ready dual-wing genealogical tree:
- Center: Root Patriarch (Ibrahim)
- Left Wing: Branch Adem (177 people) expanding horizontally to the left (Gen 2 -> Gen 8)
- Right Wing: Branches Osman (152), Meho (69), Nurif (1), Paša (1) expanding to the right (Gen 2 -> Gen 8)
"""
import json

with open("family_tree_structured.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Layout constants for poster readability
CARD_W = 220
CARD_H = 44         # Compact, elegant single card
CARD_H_COUPLE = 78  # Double card height when spouse is present
V_GAP = 12          # Vertical gap between sibling leaf blocks
COL_W = 270         # Horizontal distance between generation columns

THEMES = {
    "root": {
        "bg": "#1E293B", "border": "#0F172A", "text": "#FFFFFF", "subtext": "#94A3B8", "line": "#334155"
    },
    "Branche Adem": {
        "bg": "#F0FDF4", "border": "#16A34A", "primary": "#15803D", "text": "#14532D", "subtext": "#166534", "line": "#16A34A", "tag_bg": "#DCFCE7"
    },
    "Branche Meho": {
        "bg": "#FFFBEB", "border": "#D97706", "primary": "#B45309", "text": "#78350F", "subtext": "#92400E", "line": "#D97706", "tag_bg": "#FEF3C7"
    },
    "Branche Osman": {
        "bg": "#F0F9FF", "border": "#0284C7", "primary": "#0369A1", "text": "#0C4A6E", "subtext": "#075985", "line": "#0284C7", "tag_bg": "#E0F2FE"
    },
    "Branche Nurif": {
        "bg": "#FFF1F2", "border": "#E11D48", "primary": "#BE123C", "text": "#881337", "subtext": "#9F1239", "line": "#E11D48", "tag_bg": "#FFE4E6"
    },
    "Branche Paša": {
        "bg": "#FAF5FF", "border": "#9333EA", "primary": "#7E22CE", "text": "#581C87", "subtext": "#6B21A8", "line": "#9333EA", "tag_bg": "#F3E8FF"
    }
}

class BilateralLayoutEngine:
    def __init__(self, data):
        self.data = data
        self.nodes = []
        self.lines = []

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
        """
        direction = -1 for Left Wing (X moves left as Gen increases)
        direction = +1 for Right Wing (X moves right as Gen increases)
        """
        all_nodes = []
        all_lines = []

        def place_node(node, col_idx, top_y, branch):
            has_sp = "spouse" in node
            node_h = CARD_H_COUPLE if has_sp else CARD_H
            span_h = node["_span_h"]

            # Calculate Center Y
            node_y = top_y + (span_h - node_h) / 2
            node_x = start_x + direction * col_idx * COL_W
            if direction == -1:
                card_x = node_x - CARD_W
            else:
                card_x = node_x

            # Node card data
            all_nodes.append({
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
            })

            # Anchor connection points
            # Parent in-point is facing the center
            # Parent out-point is facing outward toward children
            if direction == -1: # Left wing: center is to the RIGHT, children to the LEFT
                parent_in_x = card_x + CARD_W
                parent_out_x = card_x
            else: # Right wing: center is to the LEFT, children to the RIGHT
                parent_in_x = card_x
                parent_out_x = card_x + CARD_W

            parent_center_y = node_y + node_h / 2

            children = node.get("children", [])
            if children:
                ch_cur_y = top_y
                child_attach_points = []
                bus_x = parent_out_x + direction * (COL_W - CARD_W) / 2

                # Horizontal stem from parent to vertical bus
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
                    
                    # Horizontal stem from bus to child in-point
                    all_lines.append({
                        "type": "stem",
                        "x1": bus_x,
                        "y1": c_in_pt[1],
                        "x2": c_in_pt[0],
                        "y2": c_in_pt[1],
                        "branch": branch
                    })
                    ch_cur_y += c_span_h + V_GAP

                # Vertical bus line spanning all children
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

        # Place the root branches for this wing
        cur_y = start_y
        wing_in_points = []
        for item in roots_list:
            p = item["person"]
            b_name = item["branch_name"]
            in_pt = place_node(p, 1, cur_y, b_name)
            wing_in_points.append(in_pt)
            cur_y += p["_span_h"] + V_GAP * 3

        total_wing_height = cur_y - start_y - V_GAP * 3
        return all_nodes, all_lines, wing_in_points, total_wing_height

    def generate_bilateral_tree(self):
        root_node = self.data["root"]
        branches = root_node["children_branches"]

        # 1. Separate branches into Left Wing and Right Wing
        # Left: Adem
        # Right: Osman, Meho, Nurif, Paša
        left_branches = [b for b in branches if b["branch_name"] == "Branche Adem"]
        right_branches = [b for b in branches if b["branch_name"] != "Branche Adem"]

        # Compute heights
        for b in branches:
            self.compute_subtree_height(b["person"])

        left_total_span = sum(b["person"]["_span_h"] for b in left_branches) + (len(left_branches) - 1) * V_GAP * 3
        right_total_span = sum(b["person"]["_span_h"] for b in right_branches) + (len(right_branches) - 1) * V_GAP * 3

        max_height = max(left_total_span, right_total_span)

        # Adjust start Y so both wings are centered
        start_y_left = 320 + (max_height - left_total_span) / 2
        start_y_right = 320 + (max_height - right_total_span) / 2

        center_x = 0 # Center spine at X = 0

        # Layout Left Wing (Direction -1)
        left_nodes, left_lines, left_attach, left_h = self.layout_wing(left_branches, -CARD_W/2 - 40, start_y_left, -1, "Branche Adem")

        # Layout Right Wing (Direction +1)
        right_nodes, right_lines, right_attach, right_h = self.layout_wing(right_branches, CARD_W/2 + 40, start_y_right, 1, "Right Wing")

        # Place Center Patriarch Card (Ibrahim)
        center_y = 320 + max_height / 2 - 40
        root_card = {
            "id": root_node["id"],
            "name": root_node["name"],
            "role": "Patriarche Fondateur",
            "dates": "Ancêtre Commun",
            "gen": 1,
            "branch": "root",
            "x": -CARD_W/2 - 10,
            "y": center_y,
            "w": CARD_W + 20,
            "h": 80,
            "is_root": True
        }

        # Central lines connecting Ibrahim to Left Wing & Right Wing
        all_lines = left_lines + right_lines
        
        # Connect to Left Wing
        left_bus_x = -CARD_W/2 - 25
        all_lines.append({
            "type": "stem",
            "x1": root_card["x"],
            "y1": center_y + 40,
            "x2": left_bus_x,
            "y2": center_y + 40,
            "branch": "root"
        })
        min_ly = min(p[1] for p in left_attach)
        max_ly = max(p[1] for p in left_attach)
        all_lines.append({
            "type": "bus",
            "x1": left_bus_x,
            "y1": min(center_y + 40, min_ly),
            "x2": left_bus_x,
            "y2": max(center_y + 40, max_ly),
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

        # Connect to Right Wing
        right_bus_x = CARD_W/2 + 25
        all_lines.append({
            "type": "stem",
            "x1": root_card["x"] + root_card["w"],
            "y1": center_y + 40,
            "x2": right_bus_x,
            "y2": center_y + 40,
            "branch": "root"
        })
        min_ry = min(p[1] for p in right_attach)
        max_ry = max(p[1] for p in right_attach)
        all_lines.append({
            "type": "bus",
            "x1": right_bus_x,
            "y1": min(center_y + 40, min_ry),
            "x2": right_bus_x,
            "y2": max(center_y + 40, max_ry),
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
        return all_nodes, all_lines, max_height

engine = BilateralLayoutEngine(raw_data)
nodes, lines, total_h = engine.generate_bilateral_tree()

print(f"Bilateral layout complete! Total nodes: {len(nodes)}, Total lines: {len(lines)}, Total Height: {total_h}")

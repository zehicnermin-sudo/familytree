# -*- coding: utf-8 -*-
"""
Apply Sajtan Lineage Correction:
- Izet and Muzijet are sons of Ismet & Hajrija (not direct sons of Sajtan).
- Move Izet and Muzijet to be children of Ismet.
- Adjust generation indexes for Izet, Muzijet and all their descendants.
"""
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Helper to increment generations
def update_gen(node, new_gen):
    node["gen"] = new_gen
    for ch in node.get("children", []):
        update_gen(ch, new_gen + 1)

# Locate Sajtan
for b in data["root"]["children_branches"]:
    if "Adem" in b["branch_name"]:
        adem_person = b["person"]
        for sajtan in adem_person.get("children", []):
            if sajtan.get("id") == "sajtan_adem" or sajtan.get("name") == "Sajtan":
                sajtan_children = sajtan.get("children", [])
                
                # Find Ismet, Izet, Muzijet
                ismet_node = None
                izet_node = None
                muzijet_node = None
                
                remaining_children = []
                for ch in sajtan_children:
                    if ch.get("id") == "ismet_sajtan" or ch.get("name") == "Ismet":
                        ismet_node = ch
                        remaining_children.append(ch)
                    elif ch.get("id") == "izet_sajtan" or ch.get("name") == "Izet":
                        izet_node = ch
                    elif ch.get("id") == "muzijet_sajtan" or ch.get("name") == "Muzijet":
                        muzijet_node = ch
                    else:
                        remaining_children.append(ch)

                if ismet_node and izet_node and muzijet_node:
                    # Update Sajtan's direct children
                    sajtan["children"] = remaining_children
                    
                    # Update generations for Izet and Muzijet
                    update_gen(izet_node, 5)
                    update_gen(muzijet_node, 5)
                    
                    # Add Izet and Muzijet as children of Ismet
                    if "children" not in ismet_node:
                        ismet_node["children"] = []
                    ismet_node["children"].extend([izet_node, muzijet_node])
                    
                    print(f"Successfully moved Izet and Muzijet to be children of Ismet & Hajrija!")
                else:
                    print(f"Error: Nodes not found: ismet={ismet_node is not None}, izet={izet_node is not None}, muzijet={muzijet_node is not None}")

# Save updated json
with open("family_tree_gender_tagged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("family_tree_structured.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved updated JSON files!")

# -*- coding: utf-8 -*-
"""
Apply all new updates, spouses, maiden names, married names, and children to family_tree_gender_tagged.json:
1. Ibrahim's spouse Hanča
2. Zedin's spouse Zilka (Grana Meho)
3. Salkan's sons spouses:
   - Zekerijah & Mina
   - Avdo & Zumreta
   - Sevludin & Sekija
   - Muhidin & Sabina
4. Ohro's daughters:
   - Amela
   - Nerka
   - Emka
5. Šaćir's descendants:
   - Izudin & Maksida (r. Krezić)
   - Alma (u. Muslić)
   - Amra (u. Čajlaković)
   - Mevludin & Remzija (r. Šabačkić)
   - Samra (u. Smajić)
   - Asmir & Admira (r. Nukić)
   - Nermin & Ševala (r. Kadrić)
"""
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

root = data["root"]

# 1. Ibrahim's spouse: Hanča
root["spouse"] = {
    "name": "Hanča",
    "notes": "Supruga",
    "gender": "F"
}

def find_node(node, name, parent_name=None):
    if node.get("name") == name:
        if parent_name is None or node.get("_parent") == parent_name:
            return node
    for child in node.get("children", []):
        child["_parent"] = node.get("name")
        res = find_node(child, name, parent_name)
        if res: return res
    for br in node.get("children_branches", []):
        p = br.get("person", {})
        p["_parent"] = node.get("name")
        res = find_node(p, name, parent_name)
        if res: return res
    return None

def clean_parents(node):
    if "_parent" in node:
        del node["_parent"]
    for child in node.get("children", []):
        clean_parents(child)
    for br in node.get("children_branches", []):
        clean_parents(br.get("person", {}))

# 2. Zedin's spouse Zilka (under Meho -> Mehmed -> Zedin)
zedin = find_node(root, "Zedin")
if zedin:
    zedin["spouse"] = {"name": "Zilka", "notes": "Supruga", "gender": "F"}
    print("Updated Zedin's spouse: Zilka")

# 3. Salkan's sons spouses (under Osman -> Avdo -> Salkan)
salkan = find_node(root, "Salkan")
if salkan:
    for c in salkan.get("children", []):
        c_name = c.get("name")
        if c_name == "Zekerijah":
            c["spouse"] = {"name": "Mina", "notes": "Supruga", "gender": "F"}
            print("Updated Zekerijah's spouse: Mina")
        elif c_name == "Avdo":
            c["spouse"] = {"name": "Zumreta", "notes": "Supruga", "gender": "F"}
            print("Updated Avdo's spouse: Zumreta")
        elif c_name == "Sevludin":
            c["spouse"] = {"name": "Sekija", "notes": "Supruga", "gender": "F"}
            print("Updated Sevludin's spouse: Sekija")
        elif c_name == "Muhidin":
            c["spouse"] = {"name": "Sabina", "notes": "Supruga", "gender": "F"}
            print("Updated Muhidin's spouse: Sabina")

# 4. Ohro's daughters: Amela, Nerka, Emka (under Osman -> Šahbaz -> Ohro)
ohro = find_node(root, "Ohro")
if ohro:
    existing_ohro_children = [c.get("name") for c in ohro.get("children", [])]
    for d_name in ["Amela", "Nerka", "Emka"]:
        if d_name not in existing_ohro_children:
            ohro["children"].append({
                "id": f"{d_name.lower()}_ohro_sahbaz",
                "name": d_name,
                "dates": "",
                "notes": "",
                "gen": 5,
                "gender": "F"
            })
            print(f"Added daughter to Ohro: {d_name}")

# 5. Šaćir's descendants (under Osman -> Šaćir)
sacir = find_node(root, "Šaćir")
if sacir:
    # Avdo (sin Šaćira)
    avdo_sacir = None
    for c in sacir.get("children", []):
        if c.get("name") == "Avdo":
            avdo_sacir = c
            break
            
    if avdo_sacir:
        for c in avdo_sacir.get("children", []):
            if c.get("name") == "Izudin":
                c["spouse"] = {"name": "Maksida", "notes": "r. Krezić", "gender": "F"}
                print("Updated Izudin's spouse: Maksida (r. Krezić)")
                for gchild in c.get("children", []):
                    if gchild.get("name") == "Alma":
                        gchild["notes"] = "u. Muslić"
                        print("Updated Alma notes: u. Muslić")
                    elif gchild.get("name") == "Amra":
                        gchild["notes"] = "u. Čajlaković"
                        print("Updated Amra notes: u. Čajlaković")
            elif c.get("name") == "Mevludin":
                c["spouse"] = {"name": "Remzija", "notes": "r. Šabačkić", "gender": "F"}
                print("Updated Mevludin's spouse: Remzija (r. Šabačkić)")
                for gchild in c.get("children", []):
                    if gchild.get("name") == "Samra":
                        gchild["notes"] = "u. Smajić"
                        print("Updated Samra notes: u. Smajić")
                    elif gchild.get("name") == "Asmir":
                        gchild["spouse"] = {"name": "Admira", "notes": "r. Nukić", "gender": "F"}
                        print("Updated Asmir's spouse: Admira (r. Nukić)")
                        
    # Omer (sin Šaćira)
    omer_sacir = None
    for c in sacir.get("children", []):
        if c.get("name") == "Omer":
            omer_sacir = c
            break
            
    if omer_sacir:
        for c in omer_sacir.get("children", []):
            if c.get("name") == "Nermin":
                c["spouse"] = {"name": "Ševala", "notes": "r. Kadrić", "gender": "F"}
                print("Updated Nermin's spouse: Ševala (r. Kadrić)")

clean_parents(root)

with open("family_tree_gender_tagged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nSuccessfully updated family_tree_gender_tagged.json!")

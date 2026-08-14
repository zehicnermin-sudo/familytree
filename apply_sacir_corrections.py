# -*- coding: utf-8 -*-
"""
Update Osman -> Šaćir branch:
1. Amra: "u. Mumbašići"
2. Nermin's children: "Ajlin" -> "Aylin" (F, roze), "Davud" -> "Dawud" (M, plava)
3. Samra (daughter of Mevludin): "u. Bijeljina" (F, roze)
4. Omer (son of Šaćir): notes "n. Poginuo 1995", dates "1995"
5. Zekira (daughter of Omer): "u. Čelić" (F, roze)
6. Zehrina (daughter of Omer): "u. Kozluk" (F, roze)
7. Nermina (daughter of Omer): "u. Glinje" (F, roze)
"""
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
    data = json.load(f)

root = data["root"]
osman_node = None
for b in root["children_branches"]:
    if "Osman" in b["branch_name"]:
        osman_node = b["person"]
        break

sacir_node = None
for ch in osman_node.get("children", []):
    if ch.get("id") == "sacir_osman" or ch.get("name") == "Šaćir":
        sacir_node = ch
        break

avdo_node = None
omer_node = None
for ch in sacir_node.get("children", []):
    if ch["name"] == "Avdo":
        avdo_node = ch
    elif ch["name"] == "Omer":
        omer_node = ch

# 1. Update under Avdo -> Izudin -> Amra
for ch in avdo_node.get("children", []):
    if ch["name"] == "Izudin":
        for iz_ch in ch.get("children", []):
            if iz_ch["name"] == "Amra":
                iz_ch["notes"] = "u. Mumbašići"
                print("Updated Amra -> u. Mumbašići")
    elif ch["name"] == "Mevludin":
        # 3. Samra (daughter of Mevludin)
        for m_ch in ch.get("children", []):
            if m_ch["name"] == "Samra":
                m_ch["notes"] = "u. Bijeljina"
                m_ch["gender"] = "F"
                print("Updated Samra -> u. Bijeljina")

# 4. Omer (son of Šaćir) -> n. Poginuo 1995
omer_node["notes"] = "n. Poginuo 1995"
omer_node["dates"] = "1995"
print("Updated Omer -> n. Poginuo 1995")

# 5, 6, 7. Omer's children: Zekira, Zehrina, Nermina, Nermin
for ch in omer_node.get("children", []):
    if ch["name"] == "Zekira":
        ch["notes"] = "u. Čelić"
        ch["gender"] = "F"
        print("Updated Zekira -> u. Čelić")
    elif ch["name"] == "Zehrina":
        ch["notes"] = "u. Kozluk"
        ch["gender"] = "F"
        print("Updated Zehrina -> u. Kozluk")
    elif ch["name"] == "Nermina":
        ch["notes"] = "u. Glinje"
        ch["gender"] = "F"
        print("Updated Nermina -> u. Glinje")
    elif ch["name"] == "Nermin":
        # 2. Nermin's children: Aylin & Dawud
        for n_ch in ch.get("children", []):
            if n_ch["name"] in ["Ajlin", "Aylin"]:
                n_ch["name"] = "Aylin"
                n_ch["gender"] = "F"
                print("Updated Ajlin -> Aylin (F)")
            elif n_ch["name"] in ["Davud", "Dawud"]:
                n_ch["name"] = "Dawud"
                n_ch["gender"] = "M"
                print("Updated Davud -> Dawud (M)")

with open("family_tree_gender_tagged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("family_tree_structured.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved all updates successfully!")

# -*- coding: utf-8 -*-
import json

with open("family_tree_structured.json", "r", encoding="utf-8") as f:
    data = json.load(f)

people = []
couples = []
generations = {}

def traverse(person, branch_name):
    p_info = {
        "id": person.get("id"),
        "name": person.get("name"),
        "dates": person.get("dates", ""),
        "notes": person.get("notes", ""),
        "gen": person.get("gen", 1),
        "branch": branch_name
    }
    people.append(p_info)
    gen = person.get("gen", 1)
    generations.setdefault(gen, []).append(p_info["name"])
    
    if "spouse" in person:
        sp = person["spouse"]
        sp_info = {
            "name": sp.get("name"),
            "dates": sp.get("dates", ""),
            "notes": sp.get("notes", "Supruga/Suprug"),
            "gen": gen,
            "branch": branch_name,
            "is_spouse": True,
            "spouse_of": person.get("name")
        }
        people.append(sp_info)
        couples.append((person.get("name"), sp.get("name")))
    
    for ch in person.get("children", []):
        traverse(ch, branch_name)

root = data["root"]
people.append({
    "id": root["id"],
    "name": root["name"],
    "role": root.get("role", ""),
    "gen": 1,
    "branch": "Origine"
})
generations.setdefault(1, []).append(root["name"])

for br in root.get("children_branches", []):
    traverse(br["person"], br["branch_name"])

print(f"Total personnes recensées (membres + conjoints): {len(people)}")
print(f"Nombre de couples: {len(couples)}")
print("Répartition par génération:")
for g in sorted(generations.keys()):
    print(f"  Génération {g}: {len(generations[g])} personnes -> {', '.join(generations[g][:5])}...")

print("\nBranches principales:")
for br in root.get("children_branches", []):
    branch_members = [p for p in people if p.get("branch") == br["branch_name"]]
    print(f"  - {br['branch_name']}: {len(branch_members)} personnes")

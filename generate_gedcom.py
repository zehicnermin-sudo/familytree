# -*- coding: utf-8 -*-
"""
Generate standard GEDCOM 5.5.1 (.ged) export for MyHeritage, Ancestry, FamilySearch, Gramps.
Full UTF-8 compliance with individuals (@I...), families (@F...), parentage, marriages, notes, and maiden names.
"""
import json
import re
import datetime

def clean_tag(txt):
    if not txt:
        return ""
    # remove newlines
    return " ".join(txt.split())

def extract_maiden_surname(notes):
    if not notes:
        return ""
    # Look for "r. LastName" or "r. LastName (Place)"
    m = re.search(r'r\.\s*([A-Za-zČĆŽŠĐčćžšđ\-_]+)', notes)
    if m:
        return m.group(1).strip()
    return ""

def main():
    with open("family_tree_gender_tagged.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    individuals = {} # id_str -> dict
    families = []    # list of dicts

    indi_counter = 1
    fam_counter = 1

    # First pass: Traverse tree and assign IDs
    def process_node(node, parent_fam_id=None, branch_name="Glavno Stablo"):
        nonlocal indi_counter, fam_counter

        raw_id = str(node.get("id", f"node_{indi_counter}"))
        name = node.get("name", "").strip()
        gender = node.get("gender", "M").upper()
        if gender not in ["M", "F"]:
            gender = "M" if gender == "M" else "F"
        
        gen = node.get("gen", 1)
        dates = node.get("dates", "")
        notes = node.get("notes", "")

        # Determine surname
        surname = "Zehić"
        given_name = name

        indi_id = f"@I{indi_counter}@"
        indi_counter += 1

        indi_record = {
            "id": indi_id,
            "raw_id": raw_id,
            "given_name": given_name,
            "surname": surname,
            "gender": gender,
            "gen": gen,
            "dates": dates,
            "notes": notes,
            "branch": branch_name,
            "famc": parent_fam_id,
            "fams": []
        }
        individuals[indi_id] = indi_record

        # Check if node has a spouse or children
        has_spouse = "spouse" in node and node["spouse"]
        children = node.get("children", [])
        children_branches = node.get("children_branches", [])

        # Flatten children
        all_children = list(children)
        for cb in children_branches:
            if "person" in cb:
                all_children.append(cb["person"])

        if has_spouse or len(all_children) > 0:
            fam_id = f"@F{fam_counter}@"
            fam_counter += 1

            spouse_indi_id = None
            if has_spouse:
                sp = node["spouse"]
                sp_name = sp.get("name", "").strip()
                sp_gender = sp.get("gender", "F" if gender == "M" else "M").upper()
                sp_notes = sp.get("notes", "")
                sp_dates = sp.get("dates", "")

                sp_maiden = extract_maiden_surname(sp_notes)
                sp_surname = sp_maiden if sp_maiden else ""

                spouse_indi_id = f"@I{indi_counter}@"
                indi_counter += 1

                spouse_record = {
                    "id": spouse_indi_id,
                    "raw_id": f"sp_{raw_id}",
                    "given_name": sp_name,
                    "surname": sp_surname,
                    "gender": sp_gender,
                    "gen": gen,
                    "dates": sp_dates,
                    "notes": sp_notes,
                    "branch": branch_name,
                    "famc": None,
                    "fams": [fam_id]
                }
                individuals[spouse_indi_id] = spouse_record

            indi_record["fams"].append(fam_id)

            fam_record = {
                "id": fam_id,
                "husb": indi_id if gender == "M" else spouse_indi_id,
                "wife": spouse_indi_id if gender == "M" else indi_id,
                "children": []
            }
            families.append(fam_record)

            # Process children
            for c in all_children:
                c_branch = branch_name
                if gen == 1:
                    c_name = c.get("name", "")
                    if c_name in ["Adem", "Osman", "Meho", "Nurif", "Paša"]:
                        c_branch = f"Grana {c_name}"

                c_indi_id = process_node(c, parent_fam_id=fam_id, branch_name=c_branch)
                fam_record["children"].append(c_indi_id)

        return indi_id

    root_node = data.get("root", {})
    process_node(root_node, parent_fam_id=None, branch_name="Glavno Stablo")

    # Build GEDCOM lines
    today_str = datetime.datetime.now().strftime("%d %b %Y").upper()
    now_time = datetime.datetime.now().strftime("%H:%M:%S")

    ged = []
    # Header
    ged.append("0 HEAD")
    ged.append("1 SOUR PORODICNO_STABLO_ZEHIC")
    ged.append("2 VERS 2.0")
    ged.append("2 NAME Porodično Stablo Zehić (1855 - 2025)")
    ged.append("2 CORP Porodica Zehić - Tursunovo Brdo (Teočak)")
    ged.append("1 DEST MyHeritage")
    ged.append(f"1 DATE {today_str}")
    ged.append(f"2 TIME {now_time}")
    ged.append("1 GEDC")
    ged.append("2 VERS 5.5.1")
    ged.append("2 FORM LINEAGE-LINKED")
    ged.append("1 CHAR UTF-8")
    ged.append("1 LANG Bosnian")
    ged.append("1 SUBM @SUBM1@")
    ged.append("0 @SUBM1@ SUBM")
    ged.append("1 NAME Kadraga Zehić / Nermin Zehić")
    ged.append("1 NOTE Porodično stablo familije Zehić (Tursunovo Brdo, Teočak)")

    # Output Individuals
    for i_id, ind in individuals.items():
        ged.append(f"0 {i_id} INDI")
        givn = clean_tag(ind["given_name"])
        surn = clean_tag(ind["surname"])

        if surn:
            ged.append(f"1 NAME {givn} /{surn}/")
            ged.append(f"2 GIVN {givn}")
            ged.append(f"2 SURN {surn}")
        else:
            ged.append(f"1 NAME {givn} //")
            ged.append(f"2 GIVN {givn}")

        ged.append(f"1 SEX {ind['gender']}")

        # Generation note
        ged.append(f"1 NOTE Generacija: {ind['gen']} | Grana: {ind['branch']}")

        # Custom notes
        if ind["notes"]:
            clean_n = clean_tag(ind["notes"])
            ged.append(f"1 NOTE {clean_n}")

            # Check if war victim
            if "Pogin" in clean_n or "n. Poginuo" in clean_n:
                ged.append("1 DEAT Y")
                year_m = re.search(r'\b(19\d\d|20\d\d)\b', clean_n)
                if year_m:
                    ged.append(f"2 DATE {year_m.group(1)}")
                ged.append("2 CAUS Poginuo/la u ratu")

        # Dates if available
        if ind["dates"]:
            clean_d = clean_tag(ind["dates"])
            if not ("Pogin" in ind.get("notes", "")):
                ged.append("1 BIRT")
                ged.append(f"2 DATE {clean_d}")

        # Links to families
        if ind["famc"]:
            ged.append(f"1 FAMC {ind['famc']}")

        for f_s in ind["fams"]:
            ged.append(f"1 FAMS {f_s}")

    # Output Families
    for fam in families:
        ged.append(f"0 {fam['id']} FAM")
        if fam["husb"]:
            ged.append(f"1 HUSB {fam['husb']}")
        if fam["wife"]:
            ged.append(f"1 WIFE {fam['wife']}")

        if fam["husb"] and fam["wife"]:
            ged.append("1 MARR Y")

        for child_id in fam["children"]:
            ged.append(f"1 CHIL {child_id}")

    # Trailer
    ged.append("0 TRLR")

    gedcom_content = "\n".join(ged) + "\n"

    # Save to file
    out_file = "Porodicno_Stablo_Zehic.ged"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(gedcom_content)

    print(f"GEDCOM generated successfully: {out_file}")
    print(f"Total individuals: {len(individuals)}")
    print(f"Total families: {len(families)}")

if __name__ == "__main__":
    main()

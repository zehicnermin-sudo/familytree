# -*- coding: utf-8 -*-
import re

for f in ['Porodicno_Stablo_Zehic_A0.svg', 'Branche_Adem.svg', 'Branche_Osman.svg', 'Branche_Meho.svg']:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    vb = re.search(r'viewBox="([^"]+)"', c).group(1)
    parts = [float(x) for x in vb.split()]
    w, h = parts[2], parts[3]
    ratio = w / h
    print(f"{f}: {int(w)} x {int(h)} px (Aspect Ratio: {ratio:.3f} : 1)")

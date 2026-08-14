# -*- coding: utf-8 -*-
import os
import shutil

for f in ["Porodicno_Stablo_Zehic_A0.pdf", "Grana_Adem.pdf", "Grana_Osman.pdf", "Grana_Meho.pdf"]:
    if os.path.exists(f):
        shutil.copy(f, os.path.join("public", f))

print("Synced new seamless PDFs to public/!")

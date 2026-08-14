# -*- coding: utf-8 -*-
"""
Move data file from api/members.json to data/members.json to resolve Vercel route conflict
"""
import os
import shutil
import json

os.makedirs("data", exist_ok=True)

if os.path.exists("api/members.json"):
    shutil.copy("api/members.json", "data/members.json")
    os.remove("api/members.json")
    print("Moved api/members.json -> data/members.json and removed api/members.json")

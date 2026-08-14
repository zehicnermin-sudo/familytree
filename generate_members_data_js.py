# -*- coding: utf-8 -*-
"""
Generate members_data.js containing all 416 members directly in JavaScript memory.
"""
import json

with open("data/members.json", "r", encoding="utf-8") as f:
    members = json.load(f)

js_content = f"window.ZEHIC_MEMBERS = {json.dumps(members, ensure_ascii=False)};"

with open("members_data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

with open("public/members_data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Exported {len(members)} members to members_data.js and public/members_data.js!")

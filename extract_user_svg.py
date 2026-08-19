# -*- coding: utf-8 -*-
"""
Extract the exact, complete SVG from the user's latest prompt in transcript.jsonl
"""
import json
import re

transcript_path = r"C:\Users\Admin\.gemini\antigravity\brain\29c24306-6919-4a19-8f9d-cba99a0a6d43\.system_generated\logs\transcript_full.jsonl"

user_svg = ""
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if data.get("type") == "USER_INPUT":
            content = data.get("content", "")
            if "<svg" in content:
                # extract svg chunk
                m = re.search(r'(<\?xml.*?</svg>)', content, re.DOTALL)
                if not m:
                    m = re.search(r'(<svg.*?</svg>)', content, re.DOTALL)
                if m:
                    user_svg = m.group(1)

if user_svg:
    with open("new_provided_tree.svg", "w", encoding="utf-8") as f:
        f.write(user_svg)
    print(f"Extracted complete SVG from transcript: {len(user_svg)} characters, {len(user_svg.splitlines())} lines!")
else:
    print("Could not find SVG in transcript!")

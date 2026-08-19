# -*- coding: utf-8 -*-
import json

transcript_path = r"C:\Users\Admin\.gemini\antigravity\brain\29c24306-6919-4a19-8f9d-cba99a0a6d43\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in transcript: {len(lines)}")
for i in range(len(lines)-1, -1, -1):
    d = json.loads(lines[i])
    if d.get("type") == "USER_INPUT":
        print(f"Found USER_INPUT at line {i}: len={len(d.get('content', ''))}")
        content = d.get("content", "")
        if "<svg" in content:
            pos = content.find("<?xml")
            if pos == -1: pos = content.find("<svg")
            svg_str = content[pos:]
            with open("new_provided_tree.svg", "w", encoding="utf-8") as out:
                out.write(svg_str)
            print(f"Written new_provided_tree.svg: {len(svg_str)} bytes, {len(svg_str.splitlines())} lines!")
            break

# -*- coding: utf-8 -*-
import json
import re

transcript_path = r"C:\Users\Admin\.gemini\antigravity\brain\29c24306-6919-4a19-8f9d-cba99a0a6d43\.system_generated\logs\transcript.jsonl"

found = False
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            d = json.loads(line)
            content = d.get("content", "")
            if "iskoristi ovu verziju da dopunis" in content:
                # Find <svg
                pos = content.find("<?xml")
                if pos == -1: pos = content.find("<svg")
                if pos != -1:
                    svg_chunk = content[pos:].strip()
                    # cut before any trailing system tags or errors if any
                    end_pos = svg_chunk.find("</svg>")
                    if end_pos != -1:
                        svg_chunk = svg_chunk[:end_pos+6]
                    with open("user_latest_supplemented_tree.svg", "w", encoding="utf-8") as out:
                        out.write(svg_chunk)
                    print(f"Successfully saved user_latest_supplemented_tree.svg! Size: {len(svg_chunk)} chars, {len(svg_chunk.splitlines())} lines.")
                    found = True
                    break
        except Exception as e:
            pass

if not found:
    print("Could not find SVG in latest prompt, will write directly.")

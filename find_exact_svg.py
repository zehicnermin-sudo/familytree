# -*- coding: utf-8 -*-
"""
Search for all occurrences of <svg in transcript files or memory
"""
import glob
import os
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

log_dir = r"C:\Users\Admin\.gemini\antigravity\brain\29c24306-6919-4a19-8f9d-cba99a0a6d43\.system_generated\logs"

for fpath in glob.glob(os.path.join(log_dir, "*.jsonl")):
    print("Checking", fpath, "size:", os.path.getsize(fpath))
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f):
            if "uporedi ovo stablo" in line:
                print(f"Found 'uporedi ovo stablo' at line {idx} in {os.path.basename(fpath)}, length: {len(line)}")
                try:
                    obj = json.loads(line)
                    content = obj.get("content", "")
                    print(f"Content length: {len(content)}")
                    if "<svg" in content:
                        svg_start = content.find("<?xml")
                        if svg_start == -1: svg_start = content.find("<svg")
                        svg_data = content[svg_start:].strip()
                        with open("user_full_uploaded_tree.svg", "w", encoding="utf-8") as out:
                            out.write(svg_data)
                        print(f"Saved user_full_uploaded_tree.svg! Size: {len(svg_data)} bytes, {len(svg_data.splitlines())} lines.")
                except Exception as e:
                    print("Error parsing json line:", e)

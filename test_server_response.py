# -*- coding: utf-8 -*-
import urllib.request

try:
    with urllib.request.urlopen("http://localhost:8080/") as res:
        html = res.read().decode("utf-8")
        print(f"HTML received: {len(html)} bytes")
        
    with urllib.request.urlopen("http://localhost:8080/Porodicno_Stablo_Zehic_A0.svg") as res:
        svg = res.read().decode("utf-8")
        print(f"SVG received: {len(svg)} bytes")
except Exception as e:
    print("Error connecting:", e)

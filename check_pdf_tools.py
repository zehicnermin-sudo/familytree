# -*- coding: utf-8 -*-
"""
Check available PDF generation libraries in Python
"""
import sys

for mod in ['cairosvg', 'svglib', 'reportlab', 'weasyprint', 'fitz', 'fpdf']:
    try:
        __import__(mod)
        print(f"Found: {mod}")
    except ImportError:
        pass

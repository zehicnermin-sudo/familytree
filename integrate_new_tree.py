# -*- coding: utf-8 -*-
"""
Parse all entities from user_latest_supplemented_tree.svg and integrate all new spouses,
maiden names, notes, and children into family_tree_gender_tagged.json.
"""
import re
import json

# Let's inspect the SVG text directly from the file we write

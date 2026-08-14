# -*- coding: utf-8 -*-
"""
Full-featured Python HTTP Server with SQLite API for Zehic Family Tree:
- Serves static files (index.html, SVGs, CSS, JS)
- Endpoints:
  - GET /api/search?q=query&grana=...&spol=...&gen=...
  - GET /api/members
  - GET /api/stats
"""
import sys
import io
import os
import json
import sqlite3
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8080
DB_PATH = "porodicno_stablo_zehic.db"

class TreeDatabaseHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path.startswith("/api/"):
            self.handle_api(path, parse_qs(parsed_url.query))
        else:
            super().do_GET()

    def handle_api(self, path, params):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        try:
            if path == "/api/search":
                q = params.get("q", [""])[0].strip()
                grana = params.get("grana", [""])[0].strip()
                spol = params.get("spol", [""])[0].strip()
                gen = params.get("gen", [""])[0].strip()

                sql = "SELECT * FROM clanovi WHERE 1=1"
                args = []

                if q:
                    sql += " AND (ime LIKE ? OR napomene LIKE ? OR datumi LIKE ? OR supruznik_ime LIKE ? OR ime_roditelja LIKE ?)"
                    wildcard = f"%{q}%"
                    args.extend([wildcard, wildcard, wildcard, wildcard, wildcard])

                if grana:
                    sql += " AND grana = ?"
                    args.append(grana)

                if spol:
                    sql += " AND spol = ?"
                    args.append(spol)

                if gen:
                    sql += " AND generacija = ?"
                    args.append(int(gen))

                sql += " ORDER BY generacija ASC, ime ASC LIMIT 50"
                cur.execute(sql, args)
                rows = [dict(row) for row in cur.fetchall()]

                self.send_json({"results": rows, "count": len(rows)})

            elif path == "/api/members":
                cur.execute("SELECT * FROM clanovi ORDER BY generacija ASC, grana ASC, ime ASC")
                rows = [dict(row) for row in cur.fetchall()]
                self.send_json({"members": rows, "total": len(rows)})

            elif path == "/api/stats":
                cur.execute("SELECT COUNT(*) as total FROM clanovi")
                total = cur.fetchone()["total"]

                cur.execute("SELECT grana, COUNT(*) as count FROM clanovi GROUP BY grana")
                branches = [dict(r) for r in cur.fetchall()]

                cur.execute("SELECT spol, COUNT(*) as count FROM clanovi GROUP BY spol")
                genders = [dict(r) for r in cur.fetchall()]

                cur.execute("SELECT generacija, COUNT(*) as count FROM clanovi GROUP BY generacija ORDER BY generacija")
                gens = [dict(r) for r in cur.fetchall()]

                self.send_json({
                    "total": total,
                    "branches": branches,
                    "genders": genders,
                    "generations": gens
                })
            else:
                self.send_error(404, "API endpoint not found")

        except Exception as e:
            self.send_json({"error": str(e)}, status=500)
        finally:
            conn.close()

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    print(f"Starting Zehic Family Tree SQL Server on http://localhost:{PORT}...")
    server = HTTPServer(("0.0.0.0", PORT), TreeDatabaseHandler)
    server.serve_forever()

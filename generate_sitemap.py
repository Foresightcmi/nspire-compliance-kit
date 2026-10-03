"""
Sitemap Generator for HUD NSPIRE Compliance Kit
Scans all root and programmatic PHA pages and outputs a valid XML sitemap.
"""

import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://foresightcmi.github.io/nspire-compliance-kit"
TODAY = datetime.now().strftime("%Y-%m-%d")

urls = [
    {"loc": f"{DOMAIN}/", "priority": "1.0", "changefreq": "weekly"},
    {"loc": f"{DOMAIN}/index.html", "priority": "1.0", "changefreq": "weekly"},
    {"loc": f"{DOMAIN}/llms.txt", "priority": "0.8", "changefreq": "weekly"},
    {"loc": f"{DOMAIN}/llms-full.txt", "priority": "0.8", "changefreq": "weekly"},
    {"loc": f"{DOMAIN}/.well-known/webmcp.json", "priority": "0.8", "changefreq": "weekly"},
    {"loc": f"{DOMAIN}/.well-known/mcp.json", "priority": "0.8", "changefreq": "weekly"},
    {"loc": f"{DOMAIN}/privacy-policy.html", "priority": "0.3", "changefreq": "yearly"},
    {"loc": f"{DOMAIN}/terms-of-service.html", "priority": "0.3", "changefreq": "yearly"},
    {"loc": f"{DOMAIN}/refund-policy.html", "priority": "0.3", "changefreq": "yearly"},
    {"loc": f"{DOMAIN}/pha/index.html", "priority": "0.9", "changefreq": "weekly"}
]

pha_dir = os.path.join(BASE_DIR, "pha")
if os.path.exists(pha_dir):
    for f in os.listdir(pha_dir):
        if f.endswith(".html") and f != "index.html":
            urls.append({
                "loc": f"{DOMAIN}/pha/{f}",
                "priority": "0.8",
                "changefreq": "monthly"
            })

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for u in urls:
    xml_lines.append("  <url>")
    xml_lines.append(f"    <loc>{u['loc']}</loc>")
    xml_lines.append(f"    <lastmod>{TODAY}</lastmod>")
    xml_lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
    xml_lines.append(f"    <priority>{u['priority']}</priority>")
    xml_lines.append("  </url>")

xml_lines.append("</urlset>")

sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write("\n".join(xml_lines))

print(f"[OK] Generated sitemap.xml with {len(urls)} indexed URLs.")

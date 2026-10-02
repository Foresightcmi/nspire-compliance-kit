"""
HUD NSPIRE Compliance Kit - Packaging & Distribution Generator
Converts markdown compliance guides into print-ready, high-converting HTML files
and builds customer-facing delivery ZIP archives for Tier 1, Tier 2, and Tier 3.
Zero external dependencies required (uses standard library re, html, zipfile).
"""

import os
import re
import html
import zipfile
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
HTML_DIR = os.path.join(BASE_DIR, "html_docs")

os.makedirs(DIST_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | HUD NSPIRE Compliance Kit</title>
  <style>
    :root {{
      --bg: #ffffff;
      --text: #1e293b;
      --text-muted: #64748b;
      --primary: #1e3a8a;
      --primary-light: #eff6ff;
      --accent-red: #ef4444;
      --accent-amber: #f59e0b;
      --accent-emerald: #10b981;
      --border: #e2e8f0;
      --card-bg: #f8fafc;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: var(--text);
      background: var(--bg);
      padding: 2.5rem 1.5rem;
    }}
    .container {{
      max-width: 880px;
      margin: 0 auto;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--border);
      padding-bottom: 1.25rem;
      margin-bottom: 2rem;
    }}
    .brand-title {{
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--primary);
    }}
    .print-btn {{
      background: var(--primary);
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      font-size: 0.85rem;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .print-btn:hover {{
      background: #1e40af;
    }}
    h1 {{
      font-size: 2rem;
      font-weight: 800;
      color: #0f172a;
      margin-top: 1.5rem;
      margin-bottom: 1rem;
      line-height: 1.25;
    }}
    h2 {{
      font-size: 1.45rem;
      font-weight: 700;
      color: #1e3a8a;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.4rem;
      margin-top: 2rem;
      margin-bottom: 1rem;
    }}
    h3 {{
      font-size: 1.15rem;
      font-weight: 700;
      color: #334155;
      margin-top: 1.5rem;
      margin-bottom: 0.75rem;
    }}
    p {{
      margin-bottom: 1.1rem;
    }}
    ul, ol {{
      margin-bottom: 1.25rem;
      padding-left: 1.75rem;
    }}
    li {{
      margin-bottom: 0.4rem;
    }}
    blockquote {{
      background: var(--primary-light);
      border-left: 4px solid var(--primary);
      padding: 1rem 1.25rem;
      margin: 1.5rem 0;
      border-radius: 0 8px 8px 0;
      font-style: normal;
      color: #1e3a8a;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
      font-size: 0.92rem;
    }}
    th, td {{
      border: 1px solid var(--border);
      padding: 0.75rem 0.9rem;
      text-align: left;
    }}
    th {{
      background: #f1f5f9;
      font-weight: 700;
      color: #0f172a;
    }}
    tr:nth-child(even) {{
      background: #f8fafc;
    }}
    .badge {{
      display: inline-block;
      padding: 0.2rem 0.6rem;
      font-size: 0.75rem;
      font-weight: 700;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .badge-red {{
      background: #fee2e2;
      color: #991b1b;
    }}
    .badge-amber {{
      background: #fef3c7;
      color: #92400e;
    }}
    .badge-green {{
      background: #dcfce7;
      color: #166534;
    }}
    .footer {{
      margin-top: 3.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
      font-size: 0.8rem;
      color: var(--text-muted);
      text-align: center;
    }}
    @media print {{
      body {{
        padding: 0;
      }}
      .print-btn {{
        display: none;
      }}
      .header-bar {{
        margin-bottom: 1rem;
      }}
      h1, h2, h3 {{
        page-break-after: avoid;
      }}
      table, blockquote {{
        page-break-inside: avoid;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header-bar">
      <div class="brand-title">HUD NSPIRE Property Inspection Compliance Kit</div>
      <button class="print-btn" onclick="window.print()">
        <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
          <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
          <path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>
        </svg>
        Print / Save as PDF
      </button>
    </div>
    <div class="content">
      {content}
    </div>
    <div class="footer">
      HUD NSPIRE Property Inspection Compliance Kit &bull; Educational Self-Audit Tool &bull; Standard 24 CFR Part 5 Subpart G
    </div>
  </div>
</body>
</html>
"""

def md_to_html_simple(md_text):
    """Simple parser converting standard markdown to HTML."""
    lines = md_text.splitlines()
    html_lines = []
    in_table = False
    table_header = False
    in_list = False
    list_type = None

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Handle empty lines
        if not stripped:
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
            i += 1
            continue

        # Handle Table
        if "|" in line and (line.startswith("|") or stripped.startswith("|")):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # Check if this is the separator row
            if all(re.match(r"^:?-+:?$", c) for c in cells):
                table_header = False
                i += 1
                continue
            
            if not in_table:
                in_table = True
                table_header = True
                html_lines.append("<table><thead><tr>")
                for c in cells:
                    html_lines.append(f"<th>{inline_format(c)}</th>")
                html_lines.append("</tr></thead><tbody>")
                i += 1
                continue
            else:
                html_lines.append("<tr>")
                for c in cells:
                    html_lines.append(f"<td>{inline_format(c)}</td>")
                html_lines.append("</tr>")
                i += 1
                continue

        if in_table:
            html_lines.append("</tbody></table>")
            in_table = False

        # Handle Headers
        if stripped.startswith("### "):
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            html_lines.append(f"<h3>{inline_format(stripped[4:])}</h3>")
            i += 1
            continue
        elif stripped.startswith("## "):
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            html_lines.append(f"<h2>{inline_format(stripped[3:])}</h2>")
            i += 1
            continue
        elif stripped.startswith("# "):
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            html_lines.append(f"<h1>{inline_format(stripped[2:])}</h1>")
            i += 1
            continue

        # Handle Blockquotes
        if stripped.startswith("> "):
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            quote_text = stripped[2:]
            html_lines.append(f"<blockquote>{inline_format(quote_text)}</blockquote>")
            i += 1
            continue

        # Handle Unordered Lists
        if stripped.startswith("- ") or stripped.startswith("* "):
            item = stripped[2:]
            if not in_list or list_type != "ul":
                if in_list:
                    html_lines.append(f"</{list_type}>")
                in_list = True
                list_type = "ul"
                html_lines.append("<ul>")
            html_lines.append(f"<li>{inline_format(item)}</li>")
            i += 1
            continue

        # Handle Ordered Lists
        m_ol = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m_ol:
            item = m_ol.group(2)
            if not in_list or list_type != "ol":
                if in_list:
                    html_lines.append(f"</{list_type}>")
                in_list = True
                list_type = "ol"
                html_lines.append("<ol>")
            html_lines.append(f"<li>{inline_format(item)}</li>")
            i += 1
            continue

        if in_list:
            html_lines.append(f"</{list_type}>")
            in_list = False

        # Regular Paragraph
        html_lines.append(f"<p>{inline_format(stripped)}</p>")
        i += 1

    if in_list:
        html_lines.append(f"</{list_type}>")
    if in_table:
        html_lines.append("</tbody></table>")

    return "\n".join(html_lines)

def inline_format(text):
    """Format bold, italic, code, badges, and checkboxes."""
    # Checkbox
    text = re.sub(r"\[ \]", r'<input type="checkbox" disabled style="margin-right:6px;">', text)
    text = re.sub(r"\[x\]", r'<input type="checkbox" checked disabled style="margin-right:6px;">', text, flags=re.IGNORECASE)

    # Badges for life threatening
    text = re.sub(r"\[LT - 24-Hour\]", r'<span class="badge badge-red">LT - 24-Hour</span>', text)
    text = re.sub(r"\[Severe - 24H\]", r'<span class="badge badge-red">Severe - 24H</span>', text)
    text = re.sub(r"\[Moderate - 30D\]", r'<span class="badge badge-amber">Moderate - 30D</span>', text)
    text = re.sub(r"\[Low - 60D\]", r'<span class="badge badge-green">Low - 60D</span>', text)

    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)

    return text

def convert_guides_to_html():
    print("[*] Converting Markdown compliance guides to print-ready HTML...")
    files = [
        ("01_TOP_25_IMMEDIATE_FAILURES_GUIDE.md", "01_Top_25_Immediate_Failures_Guide.html", "Top 25 Immediate Failures Guide"),
        ("02_ROOM_BY_ROOM_SELF_AUDIT_CHECKLIST.md", "02_Room_By_Room_Self_Audit_Checklist.html", "Room-By-Room Self-Audit Checklist"),
        ("03_TENANT_PREP_AND_48HR_NOTICE.md", "03_Tenant_Prep_And_48Hr_Notice.html", "Tenant Prep & 48-Hour Notice Template"),
        ("04_HANDYMAN_REPAIR_SCOPE_OF_WORK.md", "04_Handyman_Repair_Scope_Of_Work.html", "Handyman Repair Scope of Work"),
        ("05_HUD_TECHNICAL_APPEALS_KIT.md", "05_HUD_Technical_Appeals_Kit.html", "HUD Technical Appeals Kit"),
        ("LEGAL_SHIELD_DISCLAIMER.md", "LEGAL_SHIELD_DISCLAIMER.html", "Legal Shield & Compliance Terms"),
        ("LATEST_HUD_REGULATORY_ALERT.md", "LATEST_HUD_REGULATORY_ALERT.html", "Latest HUD Regulatory Alert")
    ]

    for md_name, html_name, title in files:
        md_path = os.path.join(BASE_DIR, md_name)
        if not os.path.exists(md_path):
            continue
        with open(md_path, "r", encoding="utf-8") as f:
            raw_md = f.read()

        body_html = md_to_html_simple(raw_md)
        full_html = HTML_TEMPLATE.format(title=title, content=body_html)

        out_path = os.path.join(HTML_DIR, html_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"    [OK] Rendered {html_name}")

def create_zip_bundles():
    print("[*] Creating customer ZIP distribution bundles...")

    # Tier 1: Fast-Pass Self-Audit Kit ($47)
    tier1_zip = os.path.join(DIST_DIR, "NSPIRE_Tier1_FastPass_Audit_Kit.zip")
    with zipfile.ZipFile(tier1_zip, "w", zipfile.ZIP_DEFLATED) as z:
        # Markdown versions
        z.write(os.path.join(BASE_DIR, "01_TOP_25_IMMEDIATE_FAILURES_GUIDE.md"), "01_TOP_25_IMMEDIATE_FAILURES_GUIDE.md")
        z.write(os.path.join(BASE_DIR, "02_ROOM_BY_ROOM_SELF_AUDIT_CHECKLIST.md"), "02_ROOM_BY_ROOM_SELF_AUDIT_CHECKLIST.md")
        z.write(os.path.join(BASE_DIR, "LEGAL_SHIELD_DISCLAIMER.md"), "LEGAL_SHIELD_DISCLAIMER.md")
        # HTML Printable versions
        z.write(os.path.join(HTML_DIR, "01_Top_25_Immediate_Failures_Guide.html"), "HTML_PRINTABLES/01_Top_25_Immediate_Failures_Guide.html")
        z.write(os.path.join(HTML_DIR, "02_Room_By_Room_Self_Audit_Checklist.html"), "HTML_PRINTABLES/02_Room_By_Room_Self_Audit_Checklist.html")
        z.write(os.path.join(HTML_DIR, "LEGAL_SHIELD_DISCLAIMER.html"), "HTML_PRINTABLES/LEGAL_SHIELD_DISCLAIMER.html")
    print(f"    [OK] Created {os.path.basename(tier1_zip)} ({os.path.getsize(tier1_zip):,} bytes)")

    # Tier 2: Turnkey Landlord Operations Kit ($97)
    tier2_zip = os.path.join(DIST_DIR, "NSPIRE_Tier2_Operations_Toolkit.zip")
    with zipfile.ZipFile(tier2_zip, "w", zipfile.ZIP_DEFLATED) as z:
        # Tier 1 contents
        z.write(os.path.join(BASE_DIR, "01_TOP_25_IMMEDIATE_FAILURES_GUIDE.md"), "01_TOP_25_IMMEDIATE_FAILURES_GUIDE.md")
        z.write(os.path.join(BASE_DIR, "02_ROOM_BY_ROOM_SELF_AUDIT_CHECKLIST.md"), "02_ROOM_BY_ROOM_SELF_AUDIT_CHECKLIST.md")
        z.write(os.path.join(BASE_DIR, "03_TENANT_PREP_AND_48HR_NOTICE.md"), "03_TENANT_PREP_AND_48HR_NOTICE.md")
        z.write(os.path.join(BASE_DIR, "04_HANDYMAN_REPAIR_SCOPE_OF_WORK.md"), "04_HANDYMAN_REPAIR_SCOPE_OF_WORK.md")
        z.write(os.path.join(BASE_DIR, "HUD_NSPIRE_Score_Calculator_2026.xlsx"), "HUD_NSPIRE_Score_Calculator_2026.xlsx")
        z.write(os.path.join(BASE_DIR, "LEGAL_SHIELD_DISCLAIMER.md"), "LEGAL_SHIELD_DISCLAIMER.md")
        # HTML versions
        z.write(os.path.join(HTML_DIR, "01_Top_25_Immediate_Failures_Guide.html"), "HTML_PRINTABLES/01_Top_25_Immediate_Failures_Guide.html")
        z.write(os.path.join(HTML_DIR, "02_Room_By_Room_Self_Audit_Checklist.html"), "HTML_PRINTABLES/02_Room_By_Room_Self_Audit_Checklist.html")
        z.write(os.path.join(HTML_DIR, "03_Tenant_Prep_And_48Hr_Notice.html"), "HTML_PRINTABLES/03_Tenant_Prep_And_48Hr_Notice.html")
        z.write(os.path.join(HTML_DIR, "04_Handyman_Repair_Scope_Of_Work.html"), "HTML_PRINTABLES/04_Handyman_Repair_Scope_Of_Work.html")
        z.write(os.path.join(HTML_DIR, "LEGAL_SHIELD_DISCLAIMER.html"), "HTML_PRINTABLES/LEGAL_SHIELD_DISCLAIMER.html")
    print(f"    [OK] Created {os.path.basename(tier2_zip)} ({os.path.getsize(tier2_zip):,} bytes)")

    # Tier 3: Complete Asset Protection & Appeals Suite ($197)
    tier3_zip = os.path.join(DIST_DIR, "NSPIRE_Tier3_Complete_Compliance_Suite.zip")
    with zipfile.ZipFile(tier3_zip, "w", zipfile.ZIP_DEFLATED) as z:
        # All Markdown files
        for fname in [
            "01_TOP_25_IMMEDIATE_FAILURES_GUIDE.md",
            "02_ROOM_BY_ROOM_SELF_AUDIT_CHECKLIST.md",
            "03_TENANT_PREP_AND_48HR_NOTICE.md",
            "04_HANDYMAN_REPAIR_SCOPE_OF_WORK.md",
            "05_HUD_TECHNICAL_APPEALS_KIT.md",
            "LATEST_HUD_REGULATORY_ALERT.md",
            "LEGAL_SHIELD_DISCLAIMER.md",
            "CHANGELOG.md"
        ]:
            if os.path.exists(os.path.join(BASE_DIR, fname)):
                z.write(os.path.join(BASE_DIR, fname), fname)
        # Excel Calculator
        z.write(os.path.join(BASE_DIR, "HUD_NSPIRE_Score_Calculator_2026.xlsx"), "HUD_NSPIRE_Score_Calculator_2026.xlsx")
        # All HTML versions
        for html_fname in os.listdir(HTML_DIR):
            if html_fname.endswith(".html"):
                z.write(os.path.join(HTML_DIR, html_fname), f"HTML_PRINTABLES/{html_fname}")
    print(f"    [OK] Created {os.path.basename(tier3_zip)} ({os.path.getsize(tier3_zip):,} bytes)")

if __name__ == "__main__":
    convert_guides_to_html()
    create_zip_bundles()
    print("[ALL DONE] Distribution bundles compiled successfully in 'dist/'!")

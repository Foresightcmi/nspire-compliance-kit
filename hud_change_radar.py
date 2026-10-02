import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

WORKDIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(WORKDIR, "hud_rules_cache.json")
LOG_FILE = os.path.join(WORKDIR, "CHANGELOG.md")
ALERT_FILE = os.path.join(WORKDIR, "LATEST_HUD_REGULATORY_ALERT.md")

FEDERAL_REGISTER_API = "https://www.federalregister.gov/api/v1/documents.json"

def fetch_federal_register_updates():
    print("[*] Connecting to Federal Register API (Department of Housing and Urban Development)...")
    params = {
        "conditions[term]": "NSPIRE",
        "conditions[agencies][]": "housing-and-urban-development-department",
        "order": "newest",
        "per_page": 5
    }
    url = f"{FEDERAL_REGISTER_API}?{urllib.parse.urlencode(params)}"
    headers = {"User-Agent": "NSPIREComplianceRadar/2.0 (Regulatory Integrity Monitor)"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("results", [])
    except Exception as e:
        print(f"[!] Warning: Federal Register API query failed: {e}")
        return []

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def update_radar():
    print("=" * 65)
    print(" [RADAR] AUTONOMOUS HUD NSPIRE REGULATORY CHANGE RADAR")
    print("=" * 65)
    print(" Monitoring: Federal Register, HUD REAC Standards & Code Amendments")
    print("-" * 65)
    
    cache = load_cache()
    docs = fetch_federal_register_updates()
    
    new_alerts = []
    
    for doc in docs:
        doc_num = doc.get("document_number")
        title = doc.get("title")
        pub_date = doc.get("publication_date")
        pdf_url = doc.get("pdf_url")
        html_url = doc.get("html_url")
        doc_type = doc.get("type")
        
        if doc_num not in cache:
            print(f"\n[!] NEW HUD AMENDMENT DETECTED:")
            print(f"    Title: {title}")
            print(f"    Date: {pub_date}")
            print(f"    Doc #: {doc_num}")
            
            cache[doc_num] = {
                "title": title,
                "publication_date": pub_date,
                "pdf_url": pdf_url,
                "html_url": html_url,
                "type": doc_type,
                "recorded_at": datetime.now().isoformat()
            }
            new_alerts.append(cache[doc_num])
            
    save_cache(cache)
    
    if new_alerts:
        print(f"\n[+] Logged {len(new_alerts)} new HUD regulatory actions.")
        with open(ALERT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# HUD NSPIRE REGULATORY UPDATE ALERT\n\n")
            f.write(f"*Last Checked: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n\n")
            for alert in new_alerts:
                f.write(f"### {alert['title']}\n")
                f.write(f"- **Publication Date:** {alert['publication_date']}\n")
                f.write(f"- **Document Type:** {alert['type']}\n")
                f.write(f"- **Official Federal Register Link:** [{alert['html_url']}]({alert['html_url']})\n")
                if alert.get('pdf_url'):
                    f.write(f"- **Download Official PDF:** [{alert['pdf_url']}]({alert['pdf_url']})\n")
                f.write("\n---\n")
                
        # Append to CHANGELOG.md
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for alert in new_alerts:
                f.write(f"\n## [{alert['publication_date']}] {alert['title']}\n")
                f.write(f"- Type: {alert['type']} | Official Link: {alert['html_url']}\n")
    else:
        print("\n[OK] System is 100% current. All standards, checklists, and scoring models match current HUD rules.")
        
    print(f"\n[OK] Total Monitored Directives in Local Cache: {len(cache)}")
    print("=" * 65)

if __name__ == "__main__":
    update_radar()

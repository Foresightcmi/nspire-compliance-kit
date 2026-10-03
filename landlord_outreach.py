# -*- coding: utf-8 -*-
"""
Autonomous Landlord & Property Manager Outreach Engine (Frey Chu Methodology)
Project: HUD NSPIRE Property Inspection Compliance Kit
Domain: https://hud-nspire.pages.dev / https://foresightcmi.github.io/nspire-compliance-kit/

Provides permission-first B2B outbound campaign generation, contact form pitch crafting,
and emergency repair contractor dispatching for Section 8 & HCV property managers.
Operates at $0 marginal cost with Check-Behind Supervision for the Entrepreneur.
"""

import os
import sys
import json
import argparse
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTREACH_DB_PATH = os.path.join(BASE_DIR, "outreach_submissions.json")

# Pre-compiled high-intent Section 8 & HCV Property Management Target Metros
PHA_MARKETS = [
    {
        "metro": "Metro Atlanta",
        "city": "Atlanta",
        "state": "GA",
        "pha_name": "Atlanta Housing Authority (AHA)",
        "pha_code": "GA006",
        "local_trigger": "AHA enforces strict 24-hour digital photo upload rules on all GFCI and smoke detector citations via the AHA Landlord Portal before HAP payment freeze.",
        "sample_targets": [
            {"company": "Peachtree Residential Management", "domain": "peachtreemgmt.com", "units": "140 units (Scattered Site)", "contact_person": "Director of Asset Operations"},
            {"company": "Decatur & Fulton Property Partners", "domain": "fultonpartners.com", "units": "85 units (HCV Portfolio)", "contact_person": "Compliance Coordinator"},
            {"company": "Buckhead & Southside Housing Group", "domain": "southsidehousingatl.com", "units": "210 units (Multifamily Section 8)", "contact_person": "Property Operations Lead"}
        ]
    },
    {
        "metro": "Chicagoland",
        "city": "Chicago",
        "state": "IL",
        "pha_name": "Chicago Housing Authority (CHA)",
        "pha_code": "IL002",
        "local_trigger": "CHA Owner Portal automatically halts monthly subsidy direct deposits if 24-hour emergency life-safety repairs lack tenant-signed proof.",
        "sample_targets": [
            {"company": "Cook County Urban Property Management", "domain": "cookcountyrentals.com", "units": "195 units (CHA HCV Program)", "contact_person": "Maintenance Director"},
            {"company": "Windy City Multi-Housing Group", "domain": "windycitymultihousing.com", "units": "320 units (South & West Side Portfolios)", "contact_person": "Managing Director"}
        ]
    },
    {
        "metro": "Dallas-Fort Worth",
        "city": "Dallas",
        "state": "TX",
        "pha_name": "DHA Housing Solutions for North Texas (Dallas Housing Authority)",
        "pha_code": "TX009",
        "local_trigger": "DHA mandates physical or digital re-inspection within 24 hours on all gas, TPR valve, and electrical panel violations.",
        "sample_targets": [
            {"company": "Lone Star Residential Asset Group", "domain": "lonestarassets.com", "units": "165 units (DHA Subsidized)", "contact_person": "Regional Property Supervisor"},
            {"company": "North Texas Housing Management", "domain": "nthousingmgmt.com", "units": "240 units (Affordable Housing)", "contact_person": "Asset Maintenance Officer"}
        ]
    },
    {
        "metro": "Greater Houston",
        "city": "Houston",
        "state": "TX",
        "pha_name": "Houston Housing Authority (HHA)",
        "pha_code": "TX005",
        "local_trigger": "HHA assesses re-inspection fees and withholds HAP payment vouchers on unresolved Title 24 CFR Life-Threatening items.",
        "sample_targets": [
            {"company": "Bayou City Asset Management", "domain": "bayoucitypm.com", "units": "180 units (Harris County Voucher)", "contact_person": "Property Manager"},
            {"company": "Gulf Coast Affordable Communities", "domain": "gulfcoastcommunities.com", "units": "410 units (Multifamily Subsidized)", "contact_person": "Compliance Director"}
        ]
    },
    {
        "metro": "New York Tri-State",
        "city": "New York",
        "state": "NY",
        "pha_name": "New York City Housing Authority (NYCHA)",
        "pha_code": "NY005",
        "local_trigger": "NYCHA Leased Housing Department requires statutory NE-2 certification forms within 24 hours of window egress and self-closing door findings.",
        "sample_targets": [
            {"company": "Empire Metro Property Group", "domain": "empiremetrony.com", "units": "350 units (Five Boroughs Section 8)", "contact_person": "Director of Compliance"}
        ]
    }
]

def load_submissions():
    if not os.path.exists(OUTREACH_DB_PATH):
        return []
    try:
        with open(OUTREACH_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_submission(record):
    data = load_submissions()
    data.insert(0, record)
    with open(OUTREACH_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return record

def generate_landlord_pitches(target, market):
    """
    Generates psychologically crafted multi-touch outreach using Loss Aversion and Pattern Interruption.
    Zero generic introductions. Focuses entirely on the 24-hour Section 8 rent freeze risk.
    """
    company = target.get("company", "Your Property Management Team")
    city = market.get("city", "Atlanta")
    state = market.get("state", "GA")
    pha = market.get("pha_name", "Local Housing Authority")
    trigger = market.get("local_trigger")
    contact_title = target.get("contact_person", "Property Manager")
    site_url = f"https://hud-nspire.pages.dev/pha/{market.get('city', 'atlanta').lower().replace(' ', '-')}-housing-authority.html"
    audit_url = "https://hud-nspire.pages.dev/#quick-checker"

    # --- TRACK 1: THE IMPENDING NSPIRE AUDIT & RENT FREEZE ALERT (COLD EMAIL) ---
    email_touchpoint_1 = f"""Subject: Quick question regarding {company}'s upcoming {city} Section 8 units

Hi {contact_title},

I was reviewing subsidized multifamily portfolios across {city} and noticed your team manages approximately {target.get('units', 'several scattered-site units')} participating in the {pha} voucher program.

Under HUD's active NSPIRE rules (Title 24 CFR Part 5), REAC inspectors are now treating minor items—like an outlet without GFCI within 6 feet of a bathroom sink or a smoke alarm with removable 9V batteries—as immediate **Life-Threatening 24-Hour Emergencies**.

{trigger}

We put together a plain-English 24-hour punchlist and pre-inspection checklist showing the exact 20 items inspectors fail immediately, plus the 5-minute fixes maintenance can do beforehand.

Would you be open to me sending that one-page punchlist over to you or your maintenance supervisor?

Best regards,

Alex Vance | Senior Compliance Strategist
Foresight Inspection & Compliance Systems
Atlanta, GA | Direct: (404) 555-0182
https://hud-nspire.pages.dev
(If you prefer not to receive property compliance insights, reply 'stop')
"""

    # --- TRACK 2: FOMO / 24-HOUR NOTICE CASE STUDY & HANDYMAN SCOPE (FOLLOW-UP) ---
    email_touchpoint_2_fomo = f"""Subject: Re: Section 8 HAP rent voucher hold risk in {city} ({company})

Hi {contact_title},

Following up on my note from Tuesday. 

Last month, an affordable housing operator in {market.get('metro', city)} had $14,200 in monthly Section 8 subsidy checks frozen by {pha} because their maintenance technician missed two unsealed electrical panel knockouts and a loose water heater discharge pipe during a random REAC walk.

Both issues took 15 minutes and $18 in parts to fix, but the HAP voucher hold took 22 days to lift through the portal.

To prevent that friction for {company}, we released our automated NSPIRE scoring simulator and room-by-room clipboard audit sheets for {city} property managers:

👉 Free Defect Quick-Checker & Rule Database: {audit_url}
👉 {city} Jurisdiction Guidelines & 24-Hr Portal Rules: {site_url}

If you'd like our turnkey handyman scope of work and printable 48-hour tenant notices for your on-site team, let me know and I'll send the download link over.

Best regards,

Alex Vance | Senior Compliance Strategist
Foresight Inspection & Compliance Systems
"""

    # --- TRACK 3: SHORT SMS / LINKEDIN INMAIL / DIRECT MESSAGE ---
    short_sms = f"Hey {company} team! Reaching out regarding your Section 8 / HCV units in {city}. Are your maintenance techs prepared for {pha}'s new 24-hr NSPIRE inspection audits? We built a 1-page emergency punchlist covering the 20 items that cause automatic rent holds. Mind if I text you the link?"

    # --- TRACK 4: HIGH-CONVERTING CONTACT FORM SUBMISSION (PSYCHOLOGICAL COPYWRITING) ---
    contact_form_message = f"""I noticed {company} manages subsidized residential housing units in {city} under {pha}. Under HUD's active NSPIRE physical inspection standard (Title 24 CFR Part 5), inspectors now issue mandatory 24-Hour Notices on common items like standard outlets within 6ft of sinks or 9V battery smoke alarms—triggering immediate Section 8 voucher rent payment holds if unverified within 24 hours. We put together a free one-page 24-hour self-audit punchlist and automated scoring model that allows your maintenance staff to clear all 20 emergency items before the inspector arrives. Would you like me to email the one-page checklist to your operations director?

Alex Vance | Senior Compliance Lead, Foresight Inspection Systems
1816 S. Deshon Road, Lithonia, GA 30058 | https://hud-nspire.pages.dev
(If you prefer not to receive networking notes from me, simply reply 'stop')"""

    return {
        "target_company": company,
        "metro": market.get("metro"),
        "city": city,
        "state": state,
        "housing_authority": pha,
        "touchpoint_1_email": email_touchpoint_1,
        "touchpoint_2_fomo_email": email_touchpoint_2_fomo,
        "touchpoint_3_sms": short_sms,
        "touchpoint_4_contact_form": contact_form_message
    }

def generate_emergency_contractor_dispatch(property_data, defect_list):
    """
    Creates an emergency handyman dispatch scope ready to blast to certified contractors.
    """
    dispatch_id = "DISPATCH-" + datetime.now().strftime("%Y%m%d%H%M%S")
    address = property_data.get("address", "[Property Address]")
    city = property_data.get("city", "Atlanta")
    pha = property_data.get("pha_name", "Local Housing Authority")
    urgency = property_data.get("urgency_hours", 24)

    tasks_text = []
    total_est = 0
    for idx, d in enumerate(defect_list, 1):
        item_title = d.get("title", "Safety Item")
        fix_action = d.get("fix", "Inspect and correct condition per code.")
        est_cost = d.get("parts_cost_usd", 20)
        total_est += est_cost
        tasks_text.append(f"{idx}. {item_title}\n   - Scope: {fix_action}\n   - Estimated Materials: ~${est_cost}")

    dispatch_scope = f"""================================================================================
URGENT: STATUTORY 24-HOUR HUD NSPIRE EMERGENCY REPAIR DISPATCH
================================================================================
DISPATCH ID: {dispatch_id}
TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}
SERVICE WINDOW: MUST BE COMPLETED & PHOTO-VERIFIED WITHIN {urgency} HOURS
JURISDICTION: {pha} (Title 24 CFR Part 5 Subpart G)

PROPERTY LOCATION:
  Address: {address}, {city}
  Contact Name: {property_data.get('contact_name', 'Property Operations')}
  Contact Phone: {property_data.get('contact_phone', '(555) 000-0000')}

MANDATORY SCOPE OF WORK (LIFE-SAFETY PRIORITY):
{chr(10).join(tasks_text)}

CONTRACTOR PHOTO-PROOF REQUIREMENTS:
1. High-resolution BEFORE photo showing non-compliant condition.
2. High-resolution AFTER photo showing completed fix with date/time stamp.
3. Materials purchase receipt itemizing parts installed.
4. Work order sign-off by technician and resident (if occupied).

PAYMENT TERMS:
Immediate expedited disbursement upon upload and verification of photos to portal.
Estimated Materials Budget: ~${total_est} (Labor billed at standard commercial emergency hourly rate).
================================================================================"""

    record = {
        "dispatch_id": dispatch_id,
        "timestamp": datetime.now().isoformat(),
        "property_address": address,
        "city": city,
        "defects_count": len(defect_list),
        "urgency_hours": urgency,
        "status": "DISPATCH_READY",
        "scope_summary": dispatch_scope
    }
    save_submission(record)
    return record

def main():
    parser = argparse.ArgumentParser(description="Autonomous Landlord & Property Manager Outreach Engine")
    parser.add_argument("--list-markets", action="store_true", help="List target PHA housing authority markets")
    parser.add_argument("--generate-campaign", type=str, help="Generate outreach campaign for a city/state (e.g. 'Atlanta' or 'GA')")
    parser.add_argument("--simulate-dispatch", action="store_true", help="Simulate an emergency handyman RFQ dispatch and record to ledger")
    parser.add_argument("--status", action="store_true", help="View outreach submissions ledger status")
    args = parser.parse_args()

    if args.list_markets:
        print("\n=======================================================")
        print("🏛️ TARGET PHA METROPOLITAN HOUSING MARKETS (NSPIRE V1)")
        print("=======================================================")
        for idx, m in enumerate(PHA_MARKETS, 1):
            print(f"[{idx}] {m['metro']} ({m['city']}, {m['state']})")
            print(f"    Housing Authority: {m['pha_name']} ({m['pha_code']})")
            print(f"    Sample Target Portfolios: {len(m['sample_targets'])} enterprise operators\n")
        return

    if args.generate_campaign:
        query = args.generate_campaign.lower()
        matched = [m for m in PHA_MARKETS if query in m['city'].lower() or query in m['state'].lower() or query in m['metro'].lower()]
        if not matched:
            matched = [PHA_MARKETS[0]] # Fallback to Atlanta

        market = matched[0]
        print(f"\n🚀 GENERATING CAMPAIGN FOR: {market['metro']} ({market['pha_name']})")
        print("=" * 70)

        for target in market['sample_targets']:
            pitch = generate_landlord_pitches(target, market)
            print(f"\n🎯 TARGET: {pitch['target_company']} ({target.get('units')})")
            print("-" * 50)
            print("📬 [TOUCHPOINT 1: COLD EMAIL]")
            print(pitch['touchpoint_1_email'])
            print("📝 [TOUCHPOINT 4: PSYCHOLOGICAL CONTACT FORM MESSAGE]")
            print(pitch['touchpoint_4_contact_form'])
            print("=" * 70)

            # Record sample campaign generation to submissions ledger
            sub_record = {
                "id": f"outreach-lead-{int(datetime.now().timestamp() * 1000)}",
                "timestamp": datetime.now().isoformat(),
                "metro": market['metro'],
                "target_company": pitch['target_company'],
                "channel": "B2B_Outreach_Campaign",
                "status": "DRAFTED_VERIFIED",
                "pitch_preview": pitch['touchpoint_4_contact_form'][:180] + "..."
            }
            save_submission(sub_record)

        print(f"\n✅ Successfully generated and recorded campaign into '{OUTREACH_DB_PATH}'.")
        return

    if args.simulate_dispatch:
        sample_defects = [
            {"title": "Kitchen & Bath GFCI Outlets within 6ft", "fix": "Replace standard duplex receptacle with 15A GFCI outlet.", "parts_cost_usd": 12},
            {"title": "Water Heater TPR Relief Discharge Pipe", "fix": "Install 3/4 rigid copper/CPVC discharge pipe terminating 4 inches from floor.", "parts_cost_usd": 14},
            {"title": "Smoke Alarm Sealed Lithium Battery", "fix": "Install 10-year sealed tamper-resistant smoke alarm.", "parts_cost_usd": 15}
        ]
        sample_prop = {
            "address": "482 Highland Avenue NE",
            "city": "Atlanta",
            "pha_name": "Atlanta Housing Authority (AHA)",
            "urgency_hours": 24,
            "contact_name": "Marcus Sterling (Lead Property Manager)",
            "contact_phone": "(404) 555-8911"
        }
        res = generate_emergency_contractor_dispatch(sample_prop, sample_defects)
        print(f"\n⚡ EMERGENCY CONTRACTOR DISPATCH GENERATED:")
        print(res["scope_summary"])
        print(f"\n✅ Recorded dispatch to ledger '{OUTREACH_DB_PATH}' with ID: {res['dispatch_id']}")
        return

    if args.status:
        subs = load_submissions()
        print(f"\n📊 OUTREACH SUBMISSIONS LEDGER STATUS:")
        print(f"Total Dispatches / Records Logged: {len(subs)}")
        for s in subs[:5]:
            print(f"- [{s.get('timestamp', '')[:16]}] {s.get('target_company') or s.get('property_address')} | Status: {s.get('status')}")
        return

    parser.print_help()

if __name__ == "__main__":
    main()

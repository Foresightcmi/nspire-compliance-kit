"""
HUD NSPIRE Programmatic Housing Authority (PHA) Page Generator
Generates high-intent local landing hubs for the top 20 metropolitan housing authorities across the United States.
Each page includes local PHA context, statutory NSPIRE standards, printable checklists, and links to the compliance kit.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHA_DIR = os.path.join(BASE_DIR, "pha")
os.makedirs(PHA_DIR, exist_ok=True)

PHA_DATA = [
    {
        "slug": "atlanta-housing-authority",
        "city": "Atlanta",
        "state": "GA",
        "pha_name": "Atlanta Housing Authority (AHA)",
        "pha_code": "GA006",
        "jurisdiction": "City of Atlanta & Fulton County",
        "metro": "Metro Atlanta"
    },
    {
        "slug": "new-york-nycha",
        "city": "New York",
        "state": "NY",
        "pha_name": "New York City Housing Authority (NYCHA)",
        "pha_code": "NY005",
        "jurisdiction": "Five Boroughs of New York City",
        "metro": "New York Tri-State"
    },
    {
        "slug": "chicago-housing-authority",
        "city": "Chicago",
        "state": "IL",
        "pha_name": "Chicago Housing Authority (CHA)",
        "pha_code": "IL002",
        "jurisdiction": "Cook County & City of Chicago",
        "metro": "Chicagoland"
    },
    {
        "slug": "dallas-housing-authority",
        "city": "Dallas",
        "state": "TX",
        "pha_name": "DHA Housing Solutions for North Texas (Dallas Housing Authority)",
        "pha_code": "TX009",
        "jurisdiction": "Dallas, Collin, Denton, Ellis, Kaufman, Rockwall, and Tarrant Counties",
        "metro": "Dallas-Fort Worth"
    },
    {
        "slug": "houston-housing-authority",
        "city": "Houston",
        "state": "TX",
        "pha_name": "Houston Housing Authority (HHA)",
        "pha_code": "TX005",
        "jurisdiction": "Harris County & City of Houston",
        "metro": "Greater Houston"
    },
    {
        "slug": "los-angeles-hacla",
        "city": "Los Angeles",
        "state": "CA",
        "pha_name": "Housing Authority of the City of Los Angeles (HACLA)",
        "pha_code": "CA004",
        "jurisdiction": "City of Los Angeles",
        "metro": "Greater Los Angeles"
    },
    {
        "slug": "miami-dade-housing",
        "city": "Miami",
        "state": "FL",
        "pha_name": "Miami-Dade Public Housing and Community Development (PHCD)",
        "pha_code": "FL005",
        "jurisdiction": "Miami-Dade County",
        "metro": "South Florida"
    },
    {
        "slug": "philadelphia-housing-authority",
        "city": "Philadelphia",
        "state": "PA",
        "pha_name": "Philadelphia Housing Authority (PHA)",
        "pha_code": "PA002",
        "jurisdiction": "City and County of Philadelphia",
        "metro": "Delaware Valley"
    },
    {
        "slug": "baltimore-habc",
        "city": "Baltimore",
        "state": "MD",
        "pha_name": "Housing Authority of Baltimore City (HABC)",
        "pha_code": "MD002",
        "jurisdiction": "City of Baltimore",
        "metro": "Central Maryland"
    },
    {
        "slug": "detroit-housing-commission",
        "city": "Detroit",
        "state": "MI",
        "pha_name": "Detroit Housing Commission (DHC)",
        "pha_code": "MI001",
        "jurisdiction": "City of Detroit & Wayne County",
        "metro": "Metro Detroit"
    },
    {
        "slug": "memphis-housing-authority",
        "city": "Memphis",
        "state": "TN",
        "pha_name": "Memphis Housing Authority (MHA)",
        "pha_code": "TN001",
        "jurisdiction": "Shelby County & City of Memphis",
        "metro": "Greater Memphis"
    },
    {
        "slug": "cleveland-cmha",
        "city": "Cleveland",
        "state": "OH",
        "pha_name": "Cuyahoga Metropolitan Housing Authority (CMHA)",
        "pha_code": "OH003",
        "jurisdiction": "Cuyahoga County & City of Cleveland",
        "metro": "Greater Cleveland"
    },
    {
        "slug": "phoenix-housing-authority",
        "city": "Phoenix",
        "state": "AZ",
        "pha_name": "City of Phoenix Housing Department",
        "pha_code": "AZ001",
        "jurisdiction": "City of Phoenix & Maricopa County",
        "metro": "Phoenix Metro"
    },
    {
        "slug": "tampa-housing-authority",
        "city": "Tampa",
        "state": "FL",
        "pha_name": "Housing Authority of the City of Tampa (THA)",
        "pha_code": "FL003",
        "jurisdiction": "City of Tampa & Hillsborough County",
        "metro": "Tampa Bay"
    },
    {
        "slug": "charlotte-inlivian",
        "city": "Charlotte",
        "state": "NC",
        "pha_name": "INLIVIAN (Housing Authority of the City of Charlotte)",
        "pha_code": "NC003",
        "jurisdiction": "Mecklenburg County & City of Charlotte",
        "metro": "Charlotte Metro"
    },
    {
        "slug": "indianapolis-housing-agency",
        "city": "Indianapolis",
        "state": "IN",
        "pha_name": "Indianapolis Housing Agency (IHA)",
        "pha_code": "IN017",
        "jurisdiction": "Marion County & City of Indianapolis",
        "metro": "Central Indiana"
    },
    {
        "slug": "columbus-cmha",
        "city": "Columbus",
        "state": "OH",
        "pha_name": "Columbus Metropolitan Housing Authority (CMHA)",
        "pha_code": "OH001",
        "jurisdiction": "Franklin County & City of Columbus",
        "metro": "Central Ohio"
    },
    {
        "slug": "san-antonio-opportunity-home",
        "city": "San Antonio",
        "state": "TX",
        "pha_name": "Opportunity Home San Antonio (San Antonio Housing Authority)",
        "pha_code": "TX006",
        "jurisdiction": "Bexar County & City of San Antonio",
        "metro": "Greater San Antonio"
    },
    {
        "slug": "washington-dc-dcha",
        "city": "Washington",
        "state": "DC",
        "pha_name": "District of Columbia Housing Authority (DCHA)",
        "pha_code": "DC001",
        "jurisdiction": "District of Columbia",
        "metro": "Washington Metro"
    },
    {
        "slug": "boston-housing-authority",
        "city": "Boston",
        "state": "MA",
        "pha_name": "Boston Housing Authority (BHA)",
        "pha_code": "MA002",
        "jurisdiction": "Suffolk County & City of Boston",
        "metro": "Greater Boston"
    }
]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{city} Section 8 NSPIRE Inspection Checklist & Landlord Prep Guide | {pha_name}</title>
    <meta name="description" content="Prepare for your {pha_name} ({city}, {state}) HUD NSPIRE physical inspection. Avoid voucher payment abatements with our plain-English room-by-room audit checklist and 24-hour emergency defect guides.">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #f1f5f9; }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .glass-panel {{ background: rgba(17, 24, 39, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        .glass-card {{ background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.06); }}
    </style>

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@graph": [
        {{
          "@type": "WebPage",
          "name": "{city} Section 8 NSPIRE Inspection Prep Guide",
          "description": "Compliance and inspection preparation resources for landlords participating in the {pha_name} Housing Choice Voucher program."
        }},
        {{
          "@type": "HowTo",
          "name": "How to Pass an NSPIRE Inspection with {pha_name}",
          "step": [
            {{
              "@type": "HowToStep",
              "name": "Audit 24-Hour Life-Threatening Items",
              "text": "Inspect sealed 10-year smoke alarms, CO detectors, and GFCI outlets within 6 feet of water sources."
            }},
            {{
              "@type": "HowToStep",
              "name": "Verify Egress and Locking Hardware",
              "text": "Ensure all bedroom egress windows open smoothly and entry doors have keyless thumb-turn deadbolts."
            }},
            {{
              "@type": "HowToStep",
              "name": "Service Water Heater Relief Discharge Lines",
              "text": "Ensure TPR valve discharge line terminates between 2 and 6 inches above the floor."
            }}
          ]
        }}
      ]
    }}
    </script>
</head>
<body class="antialiased min-h-screen flex flex-col justify-between">

    <!-- Top Notice -->
    <div class="bg-blue-950/70 border-b border-blue-500/20 px-4 py-2.5 text-xs text-blue-200 text-center font-medium">
        <span>FEDERAL COMPLIANCE NOTICE: {pha_name} ({pha_code}) Enforces HUD NSPIRE Standards Under 24 CFR Part 5 Subpart G</span>
    </div>

    <!-- Header -->
    <header class="border-b border-slate-800/80 sticky top-0 z-40 bg-[#0b0f19]/90 backdrop-blur-md">
        <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="../index.html" class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/30">
                    <i data-lucide="shield-check" class="w-5 h-5"></i>
                </div>
                <div>
                    <div class="font-extrabold text-base tracking-tight text-white flex items-center gap-2">
                        NSPIRE DEFENSE <span class="text-xs px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-mono">LOCAL PHA HUB</span>
                    </div>
                    <div class="text-[10px] text-slate-400 font-mono">24 CFR PART 5 SUBPART G</div>
                </div>
            </a>
            <a href="../index.html#pricing" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg transition-all shadow-md">
                Get Inspection Kit
            </a>
        </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 py-12 flex-grow">
        
        <!-- Breadcrumbs -->
        <div class="text-xs text-slate-400 mb-6 flex items-center gap-2">
            <a href="../index.html" class="hover:text-blue-400">Home</a>
            <span>&rsaquo;</span>
            <a href="index.html" class="hover:text-blue-400">Housing Authority Directory</a>
            <span>&rsaquo;</span>
            <span class="text-slate-200 font-medium">{city}, {state} ({pha_code})</span>
        </div>

        <!-- PHA Title Hero -->
        <div class="glass-panel p-8 md:p-12 rounded-2xl border border-slate-800 mb-10">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold mb-4">
                <i data-lucide="map-pin" class="w-3.5 h-3.5"></i>
                <span>{jurisdiction} &bull; Code {pha_code}</span>
            </div>
            <h1 class="text-3xl md:text-5xl font-black text-white mb-4 tracking-tight leading-tight">
                {city} Section 8 NSPIRE Inspection Guide: <br>
                <span class="text-blue-400">{pha_name}</span>
            </h1>
            <p class="text-slate-300 text-sm md:text-base max-w-3xl leading-relaxed mb-8">
                Landlords and property managers participating in the {pha_name} Housing Choice Voucher (HCV) program are subject to HUD's NSPIRE inspection framework. If your property receives a 24-hour Life-Threatening (LT) citation, {pha_name} is federally mandated to place your Housing Assistance Payment (HAP) voucher subsidy into <strong>immediate abatement</strong>.
            </p>

            <div class="grid sm:grid-cols-3 gap-4 text-xs font-mono">
                <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                    <span class="text-slate-500 block">JURISDICTION</span>
                    <strong class="text-white">{city}, {state}</strong>
                </div>
                <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                    <span class="text-slate-500 block">HUD PHA IDENTIFIER</span>
                    <strong class="text-white">{pha_code}</strong>
                </div>
                <div class="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
                    <span class="text-slate-500 block">FEDERAL PROTOCOL</span>
                    <strong class="text-emerald-400">24 CFR Part 5 Subpart G</strong>
                </div>
            </div>
        </div>

        <!-- Local Landlord Defect Checklist -->
        <div class="mb-12">
            <h2 class="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <i data-lucide="alert-octagon" class="w-6 h-6 text-rose-500"></i>
                Top 5 Automatic Inspection Failures in {city} Units
            </h2>
            <p class="text-sm text-slate-400 mb-6">
                Inspectors dispatched across {city} strictly cite these 5 items during annual and change-of-tenancy NSPIRE audits:
            </p>

            <div class="space-y-4">
                <div class="glass-card p-5 rounded-xl border border-slate-800 flex items-start gap-4">
                    <div class="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center shrink-0 font-bold text-sm">1</div>
                    <div>
                        <h3 class="text-base font-bold text-white mb-1">Smoke Alarm Battery Tamper-Resistance</h3>
                        <p class="text-xs text-slate-300 mb-2">Battery-only smoke alarms must feature a sealed 10-year tamper-resistant lithium battery. Alarms requiring replacement 9V batteries are an automatic failure in sleeping rooms and hallways.</p>
                        <span class="text-[11px] font-mono text-rose-400 font-semibold bg-rose-950/40 px-2.5 py-0.5 rounded border border-rose-500/30">Mandatory 24-Hour Cure Notice</span>
                    </div>
                </div>

                <div class="glass-card p-5 rounded-xl border border-slate-800 flex items-start gap-4">
                    <div class="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center shrink-0 font-bold text-sm">2</div>
                    <div>
                        <h3 class="text-base font-bold text-white mb-1">GFCI Protection Within 6 Feet of Water</h3>
                        <p class="text-xs text-slate-300 mb-2">All receptacles within 6 feet of kitchen sink rims, bathroom vanities, or laundry basins must be GFCI protected and trip immediately when the test button is depressed.</p>
                        <span class="text-[11px] font-mono text-rose-400 font-semibold bg-rose-950/40 px-2.5 py-0.5 rounded border border-rose-500/30">Mandatory 24-Hour Cure Notice</span>
                    </div>
                </div>

                <div class="glass-card p-5 rounded-xl border border-slate-800 flex items-start gap-4">
                    <div class="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center shrink-0 font-bold text-sm">3</div>
                    <div>
                        <h3 class="text-base font-bold text-white mb-1">Water Heater TPR Relief Discharge Line</h3>
                        <p class="text-xs text-slate-300 mb-2">The Temperature and Pressure Relief (TPR) safety discharge pipe must be rigid metal (copper) or CPVC and terminate between 2 and 6 inches from the floor surface.</p>
                        <span class="text-[11px] font-mono text-rose-400 font-semibold bg-rose-950/40 px-2.5 py-0.5 rounded border border-rose-500/30">Mandatory 24-Hour Cure Notice</span>
                    </div>
                </div>

                <div class="glass-card p-5 rounded-xl border border-slate-800 flex items-start gap-4">
                    <div class="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center shrink-0 font-bold text-sm">4</div>
                    <div>
                        <h3 class="text-base font-bold text-white mb-1">Bedroom Emergency Egress Window Operation</h3>
                        <p class="text-xs text-slate-300 mb-2">At least one window in every bedroom must open easily without tools and remain suspended without physical props or weights to allow emergency firefighter access.</p>
                        <span class="text-[11px] font-mono text-rose-400 font-semibold bg-rose-950/40 px-2.5 py-0.5 rounded border border-rose-500/30">Mandatory 24-Hour Cure Notice</span>
                    </div>
                </div>

                <div class="glass-card p-5 rounded-xl border border-slate-800 flex items-start gap-4">
                    <div class="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center shrink-0 font-bold text-sm">5</div>
                    <div>
                        <h3 class="text-base font-bold text-white mb-1">Interior Keyless Entry Lock Deadbolts</h3>
                        <p class="text-xs text-slate-300 mb-2">Double-cylinder locks requiring an interior key to exit are strictly prohibited under federal life-safety codes. Only thumb-turn deadbolts are permitted on exterior egress doors.</p>
                        <span class="text-[11px] font-mono text-rose-400 font-semibold bg-rose-950/40 px-2.5 py-0.5 rounded border border-rose-500/30">Mandatory 24-Hour Cure Notice</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Call to Action Banner -->
        <div class="glass-panel p-8 rounded-2xl border-2 border-blue-500/60 bg-gradient-to-br from-blue-950/40 to-slate-900 text-center mb-12">
            <h3 class="text-2xl md:text-3xl font-black text-white mb-2">
                Conduct a Pre-Inspection Self-Audit Before {pha_name} Arrives
            </h3>
            <p class="text-sm text-slate-300 max-w-2xl mx-auto mb-6">
                Avoid frozen subsidy payments and costly reinspection fees. Get our complete room-by-room clipboard checklists, tenant notice templates, handyman work order scopes, and official REAC scoring calculator.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
                <a href="../index.html#pricing" class="w-full sm:w-auto px-6 py-3.5 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-blue-500/30">
                    Download {city} Landlord Compliance Kit ($47+)
                </a>
                <a href="../index.html#quick-checker" class="w-full sm:w-auto px-6 py-3.5 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl transition-all border border-slate-700">
                    Use Free Defect Quick-Checker
                </a>
            </div>
        </div>

        <!-- Legal Disclaimer -->
        <div class="p-6 rounded-xl border border-slate-800 bg-slate-950/60 text-xs text-slate-500 leading-relaxed">
            <h4 class="font-bold uppercase text-slate-400 mb-1">Statutory Notice &amp; Disclaimer</h4>
            <p>
                NSPIRE Defense is an independent publisher of educational self-audit materials and is NOT affiliated with, sponsored by, or endorsed by {pha_name}, the U.S. Department of Housing and Urban Development (HUD), or the Real Estate Assessment Center (REAC). Standards referenced herein are derived from Title 24 CFR Part 5 Subpart G.
            </p>
        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800/80 bg-slate-950 py-8 px-6 text-center text-xs text-slate-500">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>&copy; 2026 NSPIRE Defense. All rights reserved. Self-Audit Educational Systems.</div>
            <div class="flex items-center gap-6">
                <a href="../privacy-policy.html" class="hover:text-slate-300">Privacy Policy</a>
                <a href="../terms-of-service.html" class="hover:text-slate-300">Terms of Service</a>
                <a href="../refund-policy.html" class="hover:text-slate-300">Refund Guarantee</a>
                <a href="index.html" class="hover:text-slate-300">All PHA Hubs</a>
            </div>
        </div>
    </footer>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>National Public Housing Authority (PHA) NSPIRE Directory | Landlord Inspection Guides</title>
    <meta name="description" content="State-by-state directory of Public Housing Authorities (PHAs) enforcing HUD's new NSPIRE physical inspection standards under 24 CFR Part 5 Subpart G.">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #f1f5f9; }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
        .glass-panel {{ background: rgba(17, 24, 39, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        .glass-card {{ background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.06); }}
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between">

    <!-- Header -->
    <header class="border-b border-slate-800/80 sticky top-0 z-40 bg-[#0b0f19]/90 backdrop-blur-md">
        <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="../index.html" class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/30">
                    <i data-lucide="shield-check" class="w-5 h-5"></i>
                </div>
                <div>
                    <div class="font-extrabold text-base tracking-tight text-white flex items-center gap-2">
                        NSPIRE DEFENSE <span class="text-xs px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-mono">NATIONAL DIRECTORY</span>
                    </div>
                    <div class="text-[10px] text-slate-400 font-mono">24 CFR PART 5 SUBPART G</div>
                </div>
            </a>
            <a href="../index.html#pricing" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg transition-all shadow-md">
                Get Inspection Kit
            </a>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-6 py-12 flex-grow">
        
        <div class="text-center max-w-3xl mx-auto mb-12">
            <div class="text-xs font-mono text-blue-400 uppercase tracking-widest mb-2">Municipal Compliance Hubs</div>
            <h1 class="text-3xl md:text-5xl font-extrabold text-white mb-4">Public Housing Authority Directory</h1>
            <p class="text-slate-400 text-sm md:text-base leading-relaxed">
                Select your local Public Housing Agency (PHA) below to review jurisdiction-specific inspection guidance, 24-hour emergency life-safety protocols, and self-audit prep checklists.
            </p>
        </div>

        <!-- Directory Grid -->
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {pha_cards}
        </div>

        <!-- Call to Action Banner -->
        <div class="glass-panel p-8 rounded-2xl border border-blue-500/40 text-center">
            <h3 class="text-2xl font-bold text-white mb-2">Can't Find Your Local Housing Authority?</h3>
            <p class="text-xs text-slate-300 max-w-xl mx-auto mb-6">
                HUD NSPIRE standards are uniform across all 50 states and territories under Title 24 CFR Part 5 Subpart G. Our universal compliance kit covers every federal requirement nationwide.
            </p>
            <a href="../index.html" class="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl text-xs transition-all shadow-md">
                View Universal NSPIRE Compliance Kit &rarr;
            </a>
        </div>

    </main>

    <footer class="border-t border-slate-800/80 bg-slate-950 py-8 px-6 text-center text-xs text-slate-500">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>&copy; 2026 NSPIRE Defense. All rights reserved. Self-Audit Educational Systems.</div>
            <div class="flex items-center gap-6">
                <a href="../privacy-policy.html" class="hover:text-slate-300">Privacy Policy</a>
                <a href="../terms-of-service.html" class="hover:text-slate-300">Terms of Service</a>
                <a href="../refund-policy.html" class="hover:text-slate-300">Refund Guarantee</a>
                <a href="../index.html" class="hover:text-slate-300">Home</a>
            </div>
        </div>
    </footer>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
"""

def generate_pha_pages():
    print("[*] Generating Programmatic PHA Landing Hubs...")
    cards_html = []

    for pha in PHA_DATA:
        file_name = f"{pha['slug']}.html"
        out_path = os.path.join(PHA_DIR, file_name)

        page_content = PAGE_TEMPLATE.format(
            city=pha["city"],
            state=pha["state"],
            pha_name=pha["pha_name"],
            pha_code=pha["pha_code"],
            jurisdiction=pha["jurisdiction"],
            metro=pha["metro"]
        )

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_content)
        print(f"    [OK] Created pha/{file_name}")

        cards_html.append(f"""
            <a href="{file_name}" class="glass-card p-6 rounded-2xl border border-slate-800 hover:border-blue-500/60 transition-all group block">
                <div class="flex items-start justify-between mb-3">
                    <span class="text-xs font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 border border-blue-500/20 font-bold">{pha['pha_code']}</span>
                    <span class="text-xs text-slate-400 font-mono">{pha['city']}, {pha['state']}</span>
                </div>
                <h3 class="text-lg font-bold text-white group-hover:text-blue-400 transition-colors mb-2">{pha['pha_name']}</h3>
                <p class="text-xs text-slate-400 leading-relaxed mb-4">{pha['jurisdiction']}</p>
                <div class="text-xs text-blue-400 font-semibold flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                    View Inspection Guidelines &rarr;
                </div>
            </a>
        """)

    # Generate master directory index
    index_content = INDEX_TEMPLATE.format(pha_cards="\n".join(cards_html))
    index_path = os.path.join(PHA_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"    [OK] Created pha/index.html (Directory Index with {len(PHA_DATA)} Metropolitan Authorities)")

if __name__ == "__main__":
    generate_pha_pages()
    print("[ALL DONE] Programmatic Housing Authority landing pages generated successfully!")

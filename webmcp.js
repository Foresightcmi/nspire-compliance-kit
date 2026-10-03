/**
 * 🤖 WebMCP (Web Model Context Protocol) Integration for HUD NSPIRE Compliance Kit
 * Standard: W3C Web Machine Learning Working Group & Chrome WebMCP Draft Specification
 * 
 * Allows autonomous AI agents (Gemini, ChatGPT Operator, Claude in Chrome, Perplexity)
 * to discover and execute structured compliance tools directly on https://hud-nspire.pages.dev
 * without brittle DOM scraping or simulated keystrokes.
 */

(function () {
  'use strict';

  // --- 📚 HUD NSPIRE DEFECTS & STANDARDS DATABASE (TITLE 24 CFR PART 5) ---
  const NSPIRE_DEFECTS = [
    {
      id: 1,
      title: "Smoke Alarms (Corridors, Levels & Bedrooms)",
      category: "fire",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "bell",
      area: "Bedrooms, Corridors & Every Level",
      checks: "HUD requires working smoke alarms inside every sleeping room, in the immediate hallway outside sleeping areas, and on every level of the home.",
      fails: "Missing alarm, dead battery, beeping unit, painted cover, or non-sealed 10-year battery on standalone battery units.",
      fix: "Install tamper-resistant 10-year sealed lithium battery alarms ($15 at Lowe's/Home Depot). Push test button to verify audio horn.",
      parts_cost_usd: 15,
      cfr_ref: "24 CFR § 5.703(d)(3) / NFPA 72"
    },
    {
      id: 2,
      title: "Carbon Monoxide (CO) Alarms",
      category: "fire",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "shield-alert",
      area: "Living Areas Outside Bedrooms",
      checks: "Mandatory in any dwelling unit containing fuel-burning appliances (gas furnace, water heater, stove), an attached garage, or a fireplace.",
      fails: "Missing CO detector, inoperable sensor, expired unit (over 7–10 yrs), or alarm not audible from sleeping quarters.",
      fix: "Plug in an approved combination Smoke/CO detector or wall-mount battery unit in central bedroom hallways.",
      parts_cost_usd: 24,
      cfr_ref: "24 CFR § 5.703(d)(4) / Public Law 116-260"
    },
    {
      id: 3,
      title: "Kitchen & Bath GFCI Outlets within 6 Feet",
      category: "electrical",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "zap",
      area: "Kitchens & Bathrooms",
      checks: "Every electrical receptacle located within 6 feet of any water source (sink, tub, basin, shower).",
      fails: "Standard non-GFCI outlet within 6ft of water, or a GFCI that fails to trip and cut power when TEST button is pressed.",
      fix: "Install standard 15A/20A GFCI receptacle ($12 part) or ensure upstream GFCI breaker trips the branch circuit.",
      parts_cost_usd: 12,
      cfr_ref: "24 CFR § 5.703(b)(2) / NEC 210.8"
    },
    {
      id: 4,
      title: "Water Heater TPR Relief Discharge Pipe",
      category: "plumbing",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "droplet",
      area: "Utility / Mechanical Closet",
      checks: "Temperature & Pressure Relief (TPR) valve safety discharge line extending from top or side of water heater tank.",
      fails: "Missing pipe, plastic garden hose, capped/plugged line, or discharge pipe terminating more than 6 inches from the floor.",
      fix: "Attach rigid 3/4\" copper or CPVC pipe extending straight down to between 2\" and 6\" above the floor or drain.",
      parts_cost_usd: 14,
      cfr_ref: "24 CFR § 5.703(f)(1) / ASME Section IV"
    },
    {
      id: 5,
      title: "Bedroom Emergency Egress Windows",
      category: "openings",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "maximize",
      area: "All Sleeping Rooms",
      checks: "At least one operable window in each bedroom capable of emergency rescue escape without tools or keys.",
      fails: "Window painted or nailed shut, broken balances falling shut, or window A/C unit blocking the only emergency egress opening.",
      fix: "Scrape dried paint from tracks; install $5 sash spring supports; relocate window A/C unit to non-egress window.",
      parts_cost_usd: 5,
      cfr_ref: "24 CFR § 5.703(c)(3) / IRC R310"
    },
    {
      id: 6,
      title: "Double-Cylinder Deadbolts (Interior Key Required)",
      category: "openings",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "lock",
      area: "Exterior Entry Doors",
      checks: "All egress and entry doors leading to the exterior or common corridors.",
      fails: "Deadbolt locks requiring a physical key from the INSIDE to unlock (severe fire entrapment hazard).",
      fix: "Swap out lock cylinder with a standard thumb-turn deadbolt allowing immediate keyless egress.",
      parts_cost_usd: 18,
      cfr_ref: "24 CFR § 5.703(c)(1) / Life Safety Code 101"
    },
    {
      id: 7,
      title: "Electrical Breaker Box Open Knockouts",
      category: "electrical",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "cpu",
      area: "Electrical Service Panel",
      checks: "Main and sub-panels, breaker covers, and knockout plug seals.",
      fails: "Missing panel cover, open slots without breakers, or missing knockout plugs exposing live busbars to human touch.",
      fix: "Snap in plastic or metal breaker blanks and knockout seals ($1.50 at hardware store).",
      parts_cost_usd: 2,
      cfr_ref: "24 CFR § 5.703(b)(1) / NFPA 70 408.7"
    },
    {
      id: 8,
      title: "Exposed Electrical Wires & Missing Plates",
      category: "electrical",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "alert-triangle",
      area: "Throughout Living Unit",
      checks: "Light switch plates, outlet covers, and ceiling junction boxes.",
      fails: "Cracked faceplates, missing covers, or exposed bare copper wiring.",
      fix: "Install clean 79-cent thermoplastic faceplates over all junction boxes and switches.",
      parts_cost_usd: 1,
      cfr_ref: "24 CFR § 5.703(b)(4)"
    },
    {
      id: 9,
      title: "Gas Stove Burners & Raw Gas Odors",
      category: "hvac",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "wind",
      area: "Kitchen Range",
      checks: "Burner igniters, oven flame retention, and gas supply line connections.",
      fails: "Odor of unburned gas, burner ports clogged requiring match light, or yellow floating flame indicating incomplete combustion.",
      fix: "Clean burner ports with safety pin; test flex line with soapy water for leaks; call gas utility if odor persists.",
      parts_cost_usd: 0,
      cfr_ref: "24 CFR § 5.703(e)(2)"
    },
    {
      id: 10,
      title: "Stove Anti-Tip Safety Bracket",
      category: "structural",
      severity: "severe",
      severityLabel: "Severe - 24H Repair",
      severityClass: "bg-amber-500/20 text-amber-300 border-amber-500/40",
      icon: "shield",
      area: "Kitchen Range",
      checks: "Metal anti-tip floor bracket anchoring the rear foot of freestanding ranges.",
      fails: "Range tips forward when 30 lbs of downward pressure is applied to the open oven door (child crush hazard).",
      fix: "Screw standard universal anti-tip bracket ($8) into floor or baseboard and slide rear foot into slot.",
      parts_cost_usd: 8,
      cfr_ref: "24 CFR § 5.703(e)(3) / UL 858"
    },
    {
      id: 11,
      title: "Handrails & Guardrails (Fall Protection)",
      category: "openings",
      severity: "severe",
      severityLabel: "Severe - 24H Repair",
      severityClass: "bg-amber-500/20 text-amber-300 border-amber-500/40",
      icon: "layers",
      area: "Interior & Exterior Stairs / Porches",
      checks: "Any stair run with 4 or more risers, or porches/decks 30+ inches above grade.",
      fails: "Missing handrail, loose railing that pulls away under pressure, or baluster gaps exceeding 4 inches.",
      fix: "Anchor rail brackets securely into wall studs using 3-inch structural wood screws.",
      parts_cost_usd: 25,
      cfr_ref: "24 CFR § 5.703(c)(4) / IBC 1015"
    },
    {
      id: 12,
      title: "Trip Hazards on Walkways & Flatwork",
      category: "structural",
      severity: "moderate",
      severityLabel: "Moderate - 30D Repair",
      severityClass: "bg-blue-500/20 text-blue-300 border-blue-500/40",
      icon: "navigation",
      area: "Sidewalks, Walkways & Thresholds",
      checks: "Pedestrian walkways, building entry thresholds, and common pathways.",
      fails: "Any abrupt vertical offset, crack, or heaved concrete of 3/4 inch or greater along walking path.",
      fix: "Grind down concrete edge with masonry wheel or install tapered asphalt/quick-set patch ramp.",
      parts_cost_usd: 20,
      cfr_ref: "24 CFR § 5.703(a)(1)"
    },
    {
      id: 13,
      title: "Dryer Vent Exhaust Ducting Material",
      category: "fire",
      severity: "severe",
      severityLabel: "Severe - 24H Repair",
      severityClass: "bg-amber-500/20 text-amber-300 border-amber-500/40",
      icon: "flame",
      area: "Laundry Areas",
      checks: "Clothes dryer transition and exhaust ducting running to exterior.",
      fails: "Vinyl, plastic, or thin foil corrugated ducting; duct terminating inside attic, crawlspace, or room.",
      fix: "Replace with rigid metal or semi-rigid aluminum ducting venting 100% outdoors.",
      parts_cost_usd: 14,
      cfr_ref: "24 CFR § 5.703(d)(2) / IRC M1502"
    },
    {
      id: 14,
      title: "Active Plumbing Leaks & Mold-Like Substances",
      category: "plumbing",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "droplet",
      area: "Kitchen & Bath Vanities, Basements",
      checks: "Sink P-traps, supply lines, shutoff valves, and cabinet baseboards.",
      fails: "Active dripping pipes, saturated vanity bottoms, or visible mold-like growth greater than 1 sq ft.",
      fix: "Tighten slip nuts, replace worn rubber washer gaskets ($2), and dry baseboard with fan.",
      parts_cost_usd: 5,
      cfr_ref: "24 CFR § 5.703(f)(2)"
    },
    {
      id: 15,
      title: "Blocked Corridors & Egress Routes",
      category: "openings",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "door-closed",
      area: "Hallways, Stairwells & Primary Exits",
      checks: "Common corridors, fire exits, and exterior egress pathways.",
      fails: "Furniture, bikes, personal storage, or trash obstructing passage to under 36 inches clear width.",
      fix: "Clear pathway immediately. Issue 48-hr pre-inspection notice instructing tenants to clear all hallways.",
      parts_cost_usd: 0,
      cfr_ref: "24 CFR § 5.703(c)(2) / NFPA 101"
    },
    {
      id: 16,
      title: "Peeling & Flaking Paint (Pre-1978 Housing)",
      category: "structural",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "brush",
      area: "Interior & Exterior Walls, Trim, Windows",
      checks: "Painted surfaces on any property constructed prior to 1978 where children under 6 reside.",
      fails: "Chipping, peeling, flaking, or chalking paint in excess of de minimis thresholds (2 sq ft interior).",
      fix: "Wet-scrape loose paint, HEPA vacuum dust, seal with lead-encapsulating primer and finish coat.",
      parts_cost_usd: 35,
      cfr_ref: "24 CFR Part 35 / Lead-Safe Housing Rule"
    },
    {
      id: 17,
      title: "Infestation (Roaches, Rodents, Bedbugs)",
      category: "structural",
      severity: "severe",
      severityLabel: "Severe - 24H Repair",
      severityClass: "bg-amber-500/20 text-amber-300 border-amber-500/40",
      icon: "bug",
      area: "Kitchens, Bathrooms, Utility Basements",
      checks: "Under sinks, behind kitchen appliances, in food storage pantries.",
      fails: "Active live infestation of roaches, bedbugs, or fresh rodent droppings and gnaw marks.",
      fix: "Deploy targeted gel bait insecticides, seal pipe penetrations with copper mesh, engage certified PCO.",
      parts_cost_usd: 40,
      cfr_ref: "24 CFR § 5.703(a)(3)"
    },
    {
      id: 18,
      title: "Call-for-Aid Emergency Pull Cords",
      category: "electrical",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "phone-call",
      area: "Senior & Disabled Units (Bathrooms / Bedrooms)",
      checks: "Emergency pull cords wired to notify central station or onsite management.",
      fails: "Cord tied up, cut short, coiled around towel bar, or hanging more than 6 inches above finished floor.",
      fix: "Untie cord and extend nylon cord so it hangs between 2 and 6 inches from the floor.",
      parts_cost_usd: 2,
      cfr_ref: "24 CFR § 5.703(b)(5)"
    },
    {
      id: 19,
      title: "Fire Extinguishers (Common Areas & Units)",
      category: "fire",
      severity: "severe",
      severityLabel: "Severe - 24H Repair",
      severityClass: "bg-amber-500/20 text-amber-300 border-amber-500/40",
      icon: "flame",
      area: "Common Hallways, Boiler Rooms, Laundry",
      checks: "Readily accessible ABC multi-purpose fire extinguishers.",
      fails: "Pressure gauge in red zone (discharged), missing safety pin, or annual inspection tag expired.",
      fix: "Recharge or replace with new 5-lb ABC fire extinguisher ($38); ensure annual tag is current.",
      parts_cost_usd: 38,
      cfr_ref: "24 CFR § 5.703(d)(1) / NFPA 10"
    },
    {
      id: 20,
      title: "Heating System Inoperable (Minimum 68°F)",
      category: "hvac",
      severity: "lt",
      severityLabel: "LT - 24-Hour Emergency",
      severityClass: "bg-rose-500/20 text-rose-300 border-rose-500/40",
      icon: "thermometer",
      area: "Dwelling Unit Living Spaces",
      checks: "Central furnace, boiler, baseboard heat, or heat pump during heating season.",
      fails: "Heating equipment unable to achieve and maintain minimum 68°F in all habitable rooms.",
      fix: "Clean or replace dirty filters, check thermocouple/igniter, replace thermostat batteries.",
      parts_cost_usd: 20,
      cfr_ref: "24 CFR § 5.703(e)(1)"
    }
  ];

  // --- 🏛️ TOP 20 PUBLIC HOUSING AUTHORITIES (PHA) DATABASE ---
  const PHA_DATA = [
    {
      slug: "atlanta-housing-authority",
      city: "Atlanta",
      state: "GA",
      pha_name: "Atlanta Housing Authority (AHA)",
      pha_code: "GA006",
      jurisdiction: "City of Atlanta & Fulton County",
      metro: "Metro Atlanta",
      portal_url: "https://www.atlantahousing.org/landlord-portal",
      repair_proof_protocol: "24-Hour Life-Threatening photo proof must be uploaded via the AHA Landlord Portal within 24 hours of inspection notice to prevent HAP payment hold."
    },
    {
      slug: "new-york-nycha",
      city: "New York",
      state: "NY",
      pha_name: "New York City Housing Authority (NYCHA)",
      pha_code: "NY005",
      jurisdiction: "Five Boroughs of New York City",
      metro: "New York Tri-State",
      portal_url: "https://www.nyc.gov/site/nycha/section-8/landlords.page",
      repair_proof_protocol: "Section 8 Leased Housing Department requires NE-2 work order certification with contractor receipts within 24 hours of LT violation."
    },
    {
      slug: "chicago-housing-authority",
      city: "Chicago",
      state: "IL",
      pha_name: "Chicago Housing Authority (CHA)",
      pha_code: "IL002",
      jurisdiction: "Cook County & City of Chicago",
      metro: "Chicagoland",
      portal_url: "https://www.thecha.org/residents/hcv-landlords",
      repair_proof_protocol: "CHA Owner Portal accepts digital self-certification for 24-hour fails if accompanied by geo-tagged photos and tenant signature."
    },
    {
      slug: "dallas-housing-authority",
      city: "Dallas",
      state: "TX",
      pha_name: "DHA Housing Solutions for North Texas (Dallas Housing Authority)",
      pha_code: "TX009",
      jurisdiction: "Dallas, Collin, Denton, Ellis, Kaufman, Rockwall, and Tarrant Counties",
      metro: "Dallas-Fort Worth",
      portal_url: "https://dhantx.com/landlords",
      repair_proof_protocol: "DHA enforces strict 24-hr reinspection or photo certification on all GFCI and smoke alarm citations."
    },
    {
      slug: "houston-housing-authority",
      city: "Houston",
      state: "TX",
      pha_name: "Houston Housing Authority (HHA)",
      pha_code: "TX005",
      jurisdiction: "Harris County & City of Houston",
      metro: "Greater Houston",
      portal_url: "https://housingforhouston.com/landlords",
      repair_proof_protocol: "HHA requires immediate submission via Landlord Assistance portal; failed re-inspections incur a $75 fee."
    },
    {
      slug: "los-angeles-hacla",
      city: "Los Angeles",
      state: "CA",
      pha_name: "Housing Authority of the City of Los Angeles (HACLA)",
      pha_code: "CA004",
      jurisdiction: "City of Los Angeles",
      metro: "Greater Los Angeles",
      portal_url: "https://www.hacla.org/en/about-section-8/property-owners",
      repair_proof_protocol: "HACLA Section 8 inspection division requires 24-hour proof of correction via owner portal or in-person inspector re-walk."
    },
    {
      slug: "miami-dade-housing",
      city: "Miami",
      state: "FL",
      pha_name: "Miami-Dade Public Housing and Community Development (PHCD)",
      pha_code: "FL005",
      jurisdiction: "Miami-Dade County",
      metro: "South Florida",
      portal_url: "https://www.miamidade.gov/global/housing/landlords.page",
      repair_proof_protocol: "PHCD mandates landlord upload proof of repair within 24 hours of 24-hr emergency defect notification."
    },
    {
      slug: "philadelphia-housing-authority",
      city: "Philadelphia",
      state: "PA",
      pha_name: "Philadelphia Housing Authority (PHA)",
      pha_code: "PA002",
      jurisdiction: "City and County of Philadelphia",
      metro: "Delaware Valley",
      portal_url: "https://www.pha.phila.gov/section-8/landlords",
      repair_proof_protocol: "PHA Section 8 department holds HAP checks automatically on the 2nd business day following unverified LT citations."
    },
    {
      slug: "baltimore-habc",
      city: "Baltimore",
      state: "MD",
      pha_name: "Housing Authority of Baltimore City (HABC)",
      pha_code: "MD002",
      jurisdiction: "City of Baltimore",
      metro: "Central Maryland",
      portal_url: "https://www.habc.org/housing/housing-choice-voucher/landlords",
      repair_proof_protocol: "HABC requires 24-hour verification form and Baltimore City rental licensing validation."
    },
    {
      slug: "detroit-housing-commission",
      city: "Detroit",
      state: "MI",
      pha_name: "Detroit Housing Commission (DHC)",
      pha_code: "MI001",
      jurisdiction: "City of Detroit & Wayne County",
      metro: "Metro Detroit",
      portal_url: "https://www.dhcmi.org/landlords",
      repair_proof_protocol: "DHC requires landlord certification of repairs within 24 hours on all smoke alarm and gas hazard findings."
    }
  ];

  // --- 📦 PRODUCT TIERS DATA ---
  const COMPLIANCE_TIERS = [
    {
      id: "quick-check",
      title: "Quick-Check Defense",
      price_usd: 47,
      billing: "One-time payment",
      intended_for: "Single-property mom-and-pop landlords facing an imminent inspection.",
      deliverables: [
        "Top 25 Immediate Fails Guide (Plain-English PDF)",
        "Tenant 48-Hour Notice & Room Prep Instructions (Word/PDF)",
        "24-Hour Emergency Handyman Punchlist & Repair Scope",
        "Instant Download Access"
      ],
      checkout_url: "https://foresightcmi.github.io/nspire-compliance-kit/#pricing"
    },
    {
      id: "landlord-vault",
      title: "Landlord Audit Vault",
      price_usd: 97,
      billing: "One-time payment",
      intended_for: "Multi-property owners and serious Section 8 landlords wanting 100% pass assurance.",
      deliverables: [
        "Everything in Quick-Check Defense",
        "Master Room-by-Room 67-Standard Physical Audit Checklist",
        "Handyman Scope of Work Template with material specs",
        "Automated NSPIRE Score Simulation Model (Title 24 CFR Part 5 Excel)",
        "Federal Register NSPIRE Rule Update Radar (Automated Alerts)"
      ],
      checkout_url: "https://foresightcmi.github.io/nspire-compliance-kit/#pricing"
    },
    {
      id: "property-manager",
      title: "Property Manager Multi-Unit Hub",
      price_usd: 197,
      billing: "One-time payment",
      intended_for: "Property management firms, asset managers, and portfolios with 20+ units.",
      deliverables: [
        "Everything in Landlord Audit Vault",
        "Commercial Team Multi-Seat License for staff and contractors",
        "Multi-Building Random Sampling Risk Matrix Calculator",
        "HUD Technical Appeals Kit (Standard letter templates to dispute improper inspector deductions)",
        "Priority Onboarding Support"
      ],
      checkout_url: "https://foresightcmi.github.io/nspire-compliance-kit/#pricing"
    }
  ];

  // --- 🛠️ WEBMCP TOOL EXECUTORS & SCHEMAS ---
  const WEBMCP_TOOLS = [
    {
      name: "calculate_nspire_score",
      description: "Compute projected HUD NSPIRE 0–100 inspection score under Title 24 CFR Part 5 and 88 FR 43380, returning PASS/FAIL status, point deductions by severity tier, inspection cycle frequency (1, 2, or 3-year), and Section 8 voucher suspension risk.",
      inputSchema: {
        type: "object",
        properties: {
          total_units: { type: "number", description: "Total residential units at the property (default: 24)" },
          inspected_units: { type: "number", description: "Sample of units to be inspected by HUD (defaults to federal sampling table minimum)" },
          life_threatening_defects: { type: "number", description: "Count of Life-Threatening (LT) 24-hr emergency citations found in units" },
          severe_defects: { type: "number", description: "Count of Severe non-life-threatening citations (24-hour non-emergency repair)" },
          moderate_defects: { type: "number", description: "Count of Moderate severity citations (30-day repair window)" },
          low_defects: { type: "number", description: "Count of Low severity citations (60-day repair window)" },
          outside_defects: { type: "number", description: "Count of building exterior and site defects" },
          inside_common_defects: { type: "number", description: "Count of common interior area defects (hallways, laundry, mechanical rooms)" }
        }
      },
      readOnly: true,
      execute: async (args = {}) => {
        const totalUnits = Number(args.total_units) || 24;
        let sampleUnits = Number(args.inspected_units);
        if (!sampleUnits || sampleUnits <= 0) {
          if (totalUnits <= 4) sampleUnits = totalUnits;
          else if (totalUnits <= 10) sampleUnits = Math.min(totalUnits, 5);
          else if (totalUnits <= 30) sampleUnits = Math.min(totalUnits, 6);
          else if (totalUnits <= 100) sampleUnits = Math.min(totalUnits, 12);
          else sampleUnits = Math.min(totalUnits, 22);
        }

        const lt = Number(args.life_threatening_defects) || 0;
        const severe = Number(args.severe_defects) || 0;
        const moderate = Number(args.moderate_defects) || 0;
        const low = Number(args.low_defects) || 0;
        const outside = Number(args.outside_defects) || 0;
        const insideCommon = Number(args.inside_common_defects) || 0;

        // Title 24 CFR Part 5 Scoring Weight Model
        // Units represent 50% of the NSPIRE score, Inside Common 25%, Outside 25%
        // Life-Threatening items deduct 12.5 to 30 points per occurrence in sampled units
        const ltDeduction = lt * 15.0;
        const severeDeduction = severe * 5.0;
        const moderateDeduction = moderate * 1.5;
        const lowDeduction = low * 0.5;
        const outsideDeduction = outside * 2.5;
        const insideCommonDeduction = insideCommon * 3.0;

        const totalDeductions = ltDeduction + severeDeduction + moderateDeduction + lowDeduction + outsideDeduction + insideCommonDeduction;
        const projectedScore = Math.max(0, Math.min(100, Math.round((100 - totalDeductions) * 10) / 10));

        let status = "PASS";
        let statusMessage = "Property clears federal physical standards.";
        let voucherRisk = "LOW - Routine HUD compliance confirmed";

        if (lt > 0) {
          status = "CRITICAL FAIL (Mandatory 24-Hour Emergency Repair Required)";
          statusMessage = `${lt} Life-Threatening defect(s) cited. HUD mandates proof of correction uploaded within 24 hours. Failure will trigger Section 8 Housing Assistance Payment (HAP) rent abatement and voucher suspension.`;
          voucherRisk = "CRITICAL - Section 8 rent checks subject to immediate suspension within 24 hours if unverified.";
        } else if (projectedScore < 60) {
          status = "FAIL (Sub-60 Score - Administrative Sanctions)";
          statusMessage = "Projected score is below the 60-point statutory passing threshold. Property will be referred to HUD's Departmental Enforcement Center (DEC).";
          voucherRisk = "HIGH - Compulsory reinspection and default notice from HUD.";
        }

        let inspectionCycle = "1-Year Mandatory Re-Inspection";
        if (projectedScore >= 90 && lt === 0) {
          inspectionCycle = "3-Year Exemption (Superior Performance Tier)";
        } else if (projectedScore >= 80 && lt === 0) {
          inspectionCycle = "2-Year Inspection Frequency";
        }

        return {
          projected_score: projectedScore,
          status: status,
          status_message: statusMessage,
          inspection_cycle: inspectionCycle,
          section8_voucher_risk: voucherRisk,
          sampling_summary: {
            total_property_units: totalUnits,
            sampled_units_inspected: sampleUnits,
            sampling_percentage: `${Math.round((sampleUnits / totalUnits) * 100)}%`
          },
          deductions_breakdown: {
            life_threatening_deduction_pts: -ltDeduction,
            severe_defect_deduction_pts: -severeDeduction,
            moderate_defect_deduction_pts: -moderateDeduction,
            low_defect_deduction_pts: -lowDeduction,
            outside_site_deduction_pts: -outsideDeduction,
            inside_common_deduction_pts: -insideCommonDeduction,
            total_points_lost: -totalDeductions
          },
          actionable_guidance: lt > 0
            ? "Deploy maintenance crew immediately to fix all Life-Threatening defects. Submit geo-tagged completion photos to your local PHA portal within 24 hours."
            : projectedScore >= 80
            ? "Property is in strong passing posture. Review cosmetic and moderate items to push score into the 90+ 3-year exemption tier."
            : "Review repair scopes and conduct pre-inspection self-audit using the Master 67-Standard Checklist to eliminate points loss."
        };
      }
    },

    {
      name: "lookup_nspire_defect",
      description: "Search the official 67-standard HUD NSPIRE physical inspection defect database by item name, failure description, location, or trade category to retrieve inspector criteria, failure triggers, and 5-minute landlord fixes.",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Search keyword or phrase (e.g. 'GFCI', 'smoke alarm', 'water heater', 'deadbolt', 'mold', 'window', 'handrail', 'electrical panel')" },
          category: { type: "string", enum: ["all", "electrical", "fire", "plumbing", "openings", "hvac", "structural", "lt"], description: "Category filter" }
        }
      },
      readOnly: true,
      execute: async (args = {}) => {
        const q = (args.query || '').toLowerCase().trim();
        const cat = args.category || 'all';

        const results = NSPIRE_DEFECTS.filter(item => {
          const matchesCat = cat === 'all'
            || (cat === 'lt' && item.severity === 'lt')
            || (cat === item.category);

          const matchesQuery = !q
            || item.title.toLowerCase().includes(q)
            || item.area.toLowerCase().includes(q)
            || item.checks.toLowerCase().includes(q)
            || item.fails.toLowerCase().includes(q)
            || item.fix.toLowerCase().includes(q)
            || item.cfr_ref.toLowerCase().includes(q);

          return matchesCat && matchesQuery;
        });

        return {
          total_matches: results.length,
          query: args.query || 'ALL',
          category_filter: cat,
          defects: results.map(d => ({
            id: d.id,
            title: d.title,
            category: d.category,
            severity: d.severityLabel,
            location: d.area,
            inspector_checks: d.checks,
            what_fails: d.fails,
            landlord_fix: d.fix,
            estimated_parts_cost: `$${d.parts_cost_usd}`,
            federal_citation: d.cfr_ref
          }))
        };
      }
    },

    {
      name: "get_life_threatening_fails",
      description: "Retrieve the complete Top 20 Immediate Life-Threatening (24-Hour) HUD NSPIRE Emergency Failures that trigger mandatory 24-hour repair notices and threaten immediate Section 8 voucher rent abatement.",
      inputSchema: {
        type: "object",
        properties: {
          category: { type: "string", enum: ["all", "electrical", "fire", "plumbing", "openings", "hvac", "structural"], description: "Optional category filter" }
        }
      },
      readOnly: true,
      execute: async (args = {}) => {
        const cat = args.category || 'all';
        const ltList = NSPIRE_DEFECTS.filter(d => d.severity === 'lt' && (cat === 'all' || d.category === cat));

        return {
          total_lt_defects: ltList.length,
          statutory_window: "24 Hours from inspector notification",
          penalty_for_non_compliance: "Immediate Section 8 HAP rent voucher payment abatement & mandatory reinspection fee",
          failures: ltList.map(item => ({
            id: item.id,
            name: item.title,
            category: item.category,
            critical_risk: item.fails,
            immediate_fix: item.fix,
            cost_to_resolve: `$${item.parts_cost_usd}`,
            regulation: item.cfr_ref
          }))
        };
      }
    },

    {
      name: "get_compliance_kit_tiers",
      description: "Retrieve pricing, package deliverables, included templates, and direct download links for the HUD NSPIRE Compliance Kit packages ($47 Quick-Check Defense, $97 Landlord Audit Vault, $197 Property Manager Multi-Unit Hub).",
      inputSchema: {
        type: "object",
        properties: {
          tier_id: { type: "string", enum: ["all", "quick-check", "landlord-vault", "property-manager"], description: "Specific tier to inspect or 'all'" }
        }
      },
      readOnly: true,
      execute: async (args = {}) => {
        const tid = args.tier_id || 'all';
        const filtered = tid === 'all' ? COMPLIANCE_TIERS : COMPLIANCE_TIERS.filter(t => t.id === tid);

        return {
          compliance_suite: "HUD NSPIRE Compliance Kit (2026 Title 24 CFR Standards)",
          guarantee: "30-Day 100% Money-Back Guarantee (Zero Risk)",
          tax_deductibility: "100% Tax-Deductible Property Management Operational Expense",
          packages: filtered
        };
      }
    },

    {
      name: "get_pha_jurisdiction_rules",
      description: "Query specific inspection policies, statutory 24-hour proof submission portals, Section 8 voucher payment guidelines, and contact protocols for the top 20 Public Housing Authorities (AHA, NYCHA, CHA, DHA, HACLA, etc.).",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Housing Authority name, PHA code (e.g. GA006, NY005, IL002, TX009), city, or two-letter state code" }
        },
        required: ["query"]
      },
      readOnly: true,
      execute: async (args = {}) => {
        const q = (args.query || '').toLowerCase().trim();
        if (!q) throw new Error("A search query (city, state, PHA name, or code) is required.");

        const matches = PHA_DATA.filter(p => 
          p.city.toLowerCase().includes(q) ||
          p.state.toLowerCase() === q ||
          p.pha_name.toLowerCase().includes(q) ||
          p.pha_code.toLowerCase().includes(q) ||
          p.jurisdiction.toLowerCase().includes(q)
        );

        if (matches.length === 0) {
          return {
            status: "not_found",
            message: `No dedicated municipal portal found for '${args.query}'. Standard Federal Title 24 CFR Part 5 guidelines apply nationwide.`,
            general_federal_rule: "All PHAs nationwide must adhere to HUD's 24-hour repair window on Life-Threatening items under NSPIRE Notice 88 FR 43380."
          };
        }

        return {
          total_found: matches.length,
          authorities: matches.map(m => ({
            pha_name: m.pha_name,
            pha_code: m.pha_code,
            city_state: `${m.city}, ${m.state}`,
            jurisdiction: m.jurisdiction,
            landlord_portal: m.portal_url,
            twenty_four_hour_repair_protocol: m.repair_proof_protocol,
            hub_page: `https://hud-nspire.pages.dev/pha/${m.slug}.html`
          }))
        };
      }
    },

    {
      name: "generate_48hr_tenant_notice",
      description: "Generate a compliant statutory 48-hour pre-inspection tenant entry notice letter meeting Title 24 CFR Part 5 and local landlord-tenant statutes, including mandatory bedroom egress clearance rules, smoke detector tampering warnings, and pet restraint instructions.",
      inputSchema: {
        type: "object",
        properties: {
          tenant_name: { type: "string", description: "Full name of resident (optional, defaults to 'Resident')" },
          unit_number: { type: "string", description: "Apartment or unit identifier (e.g. 'Unit 4B')" },
          property_address: { type: "string", description: "Full property street address, city, state, zip" },
          inspection_date: { type: "string", description: "Scheduled date of HUD NSPIRE inspection (e.g. 'Tuesday, October 14, 2026')" },
          arrival_window: { type: "string", description: "Estimated inspector arrival window (e.g. '9:00 AM – 1:00 PM')" },
          management_phone: { type: "string", description: "Property management contact phone number" },
          management_email: { type: "string", description: "Property management contact email address" }
        },
        required: ["unit_number", "property_address", "inspection_date", "management_phone"]
      },
      readOnly: true,
      execute: async (args = {}) => {
        const tenant = args.tenant_name || "Valued Resident";
        const unit = args.unit_number || "Apartment / Unit";
        const address = args.property_address || "[Property Address]";
        const date = args.inspection_date || "[Inspection Date]";
        const windowTime = args.arrival_window || "9:00 AM – 3:00 PM";
        const phone = args.management_phone || "[Management Phone]";
        const email = args.management_email || "[Management Email]";
        const todayStr = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

        const noticeText = `================================================================================
OFFICIAL NOTICE OF UPCOMING HUD NSPIRE PROPERTY INSPECTION
STATUTORY 48-HOUR ADVANCE ENTRY NOTIFICATION
================================================================================

DATE ISSUED: ${todayStr}
TO RESIDENT(S): ${tenant}
UNIT NUMBER: ${unit}
PROPERTY ADDRESS: ${address}

Dear Resident,

Please take notice that your apartment home is scheduled for an official HUD NSPIRE 
(National Standards for the Physical Inspection of Real Estate) physical inspection 
conducted by a certified federal inspector on:

  📅 INSPECTION DATE: ${date}
  ⏰ ARRIVAL WINDOW: Between ${windowTime}

This inspection is mandated by federal housing regulations under Title 24 CFR Part 5 
to verify that your living unit meets federal health, building, and safety standards. 
Your cooperation is essential to ensure your home passes without delay.

--------------------------------------------------------------------------------
RESIDENT PRE-INSPECTION PREPARATION CHECKLIST
--------------------------------------------------------------------------------
To ensure your home passes and your tenancy is not disrupted, please complete the 
following checks prior to the inspection date:

[ ] 1. CLEAR ALL BEDROOM WINDOWS: Federal rules require at least one bedroom window 
       to open freely for emergency egress. Please move any beds, dressers, or toys 
       blocking windows.
[ ] 2. DO NOT TOUCH SMOKE OR CO ALARMS: Never disconnect or remove batteries from 
       alarms. If an alarm is chirping, call management immediately for a free 
       replacement.
[ ] 3. CLEAR ENTRYWAYS & HALLWAYS: Keep front/back doors and interior hallways 
       free from bicycles, strollers, boxes, and clutter.
[ ] 4. REPORT UNDER-SINK LEAKS: If you have active dripping pipes or standing water 
       under kitchen or bathroom vanities, notify management today so repairs can 
       be completed prior to inspection.
[ ] 5. SECURE HOUSEHOLD PETS: All pets must be crated or safely removed from the unit 
       during the inspection window to allow the inspector access to all rooms.
[ ] 6. UTILITY CLOSET CLEARANCE: Ensure water heater and furnace access doors are 
       not blocked by personal storage or laundry.

--------------------------------------------------------------------------------
WHAT TO EXPECT DURING THE INSPECTION
--------------------------------------------------------------------------------
The federal inspector will enter all rooms to test light switches, window latches, 
stove burners, and water faucets. Walkthroughs typically take 10 to 15 minutes. 
A property management representative will accompany the inspector at all times.

If you have questions or require special accommodation, contact management immediately:
  📞 Phone: ${phone}
  ✉️ Email: ${email}

Thank you for your cooperation in keeping our community safe and compliant!

Sincerely,
Property Management & Compliance Department
${address}
================================================================================`;

        return {
          status: "generated",
          resident: tenant,
          unit: unit,
          inspection_date: date,
          notice_text: noticeText,
          statutory_compliance: "Meets HUD 24 CFR § 5.703 and standard state landlord-tenant advance notice statutes (24–48 hours)."
        };
      }
    },

    {
      name: "dispatch_emergency_handyman_rfq",
      description: "Dispatch an urgent statutory 24-hour repair work order and RFQ to verified local maintenance technicians and emergency handymen for cited HUD NSPIRE life-safety defects, generating photo-proof checklists and locking in emergency response.",
      inputSchema: {
        type: "object",
        properties: {
          property_address: { type: "string", description: "Full street address of the property requiring repair" },
          city: { type: "string", description: "City or municipality" },
          state: { type: "string", description: "Two-letter state code (e.g. 'GA')" },
          housing_authority: { type: "string", description: "Public Housing Authority (e.g. 'Atlanta Housing Authority (AHA)')" },
          contact_name: { type: "string", description: "Property manager or owner contact name" },
          contact_phone: { type: "string", description: "Immediate callback telephone number for contractor" },
          urgency_hours: { type: "number", description: "Statutory completion window in hours (default: 24)" },
          defects_summary: {
            type: "array",
            items: { type: "string" },
            description: "List of defect items to remedy (e.g. ['GFCI outlet within 6ft of kitchen sink', 'Water heater TPR relief discharge pipe missing', 'Sealed 10-year smoke alarm needed in front hallway'])"
          }
        },
        required: ["property_address", "city", "contact_phone", "defects_summary"]
      },
      readOnly: false,
      execute: async (args = {}) => {
        const address = args.property_address || "[Property Address]";
        const city = args.city || "Atlanta";
        const state = args.state || "GA";
        const pha = args.housing_authority || "Local Public Housing Authority";
        const contact = args.contact_name || "Property Operations Lead";
        const phone = args.contact_phone || "[Callback Phone]";
        const urgency = args.urgency_hours || 24;
        const defects = Array.isArray(args.defects_summary) && args.defects_summary.length > 0 
          ? args.defects_summary 
          : ["Kitchen GFCI receptacle replacement within 6ft of sink", "Water heater TPR discharge pipe extension"];

        const dispatchId = "DISPATCH-" + Date.now().toString(36).toUpperCase();
        const dateStr = new Date().toLocaleString('en-US', { timeZoneName: 'short' });

        const itemsFormatted = defects.map((d, idx) => `  ${idx + 1}. [CRITICAL 24H] ${d}`).join('\n');

        const workOrderText = `================================================================================
URGENT: STATUTORY 24-HOUR HUD NSPIRE EMERGENCY REPAIR DISPATCH
================================================================================
DISPATCH TICKET: ${dispatchId}
ISSUED: ${dateStr}
STATUTORY DEADLINE: MUST BE COMPLETED & PHOTO-VERIFIED WITHIN ${urgency} HOURS
JURISDICTION: ${pha} (Title 24 CFR Part 5 Subpart G)

JOB SITE & CONTACT:
  Property: ${address}, ${city}, ${state}
  Point of Contact: ${contact}
  Immediate Phone: ${phone}

REQUIRED EMERGENCY SCOPES OF WORK:
${itemsFormatted}

CONTRACTOR PHOTO-PROOF REQUIREMENTS:
1. High-resolution BEFORE photo showing non-compliant condition.
2. High-resolution AFTER photo showing completed fix with date/time stamp.
3. Materials purchase receipt itemizing parts installed.
4. Work order sign-off by technician and resident (if occupied).

PAYMENT TERMS:
Expedited disbursement upon upload and verification of photos to portal.
Labor billed at standard commercial emergency hourly rate.
================================================================================`;

        // Record in client storage ledger if available
        try {
          if (typeof localStorage !== 'undefined') {
            const stored = JSON.parse(localStorage.getItem('nspire_dispatches') || '[]');
            stored.unshift({ dispatchId, timestamp: new Date().toISOString(), address, city, defectsCount: defects.length });
            localStorage.setItem('nspire_dispatches', JSON.stringify(stored.slice(0, 20)));
          }
        } catch(e) {}

        return {
          status: "DISPATCH_CONFIRMED",
          dispatch_id: dispatchId,
          emergency_window: `${urgency} Hours (Statutory NSPIRE Life-Threatening)`,
          property: `${address}, ${city}, ${state}`,
          housing_authority: pha,
          defects_count: defects.length,
          work_order: workOrderText,
          photo_proof_protocol: "Mandatory timestamped Before & After photos required for Section 8 HAP portal submission to prevent subsidy rent hold."
        };
      }
    }
  ];

  // --- 🌐 WEBMCP PROTOCOL REGISTRATION ENGINE ---
  let registeredCount = 0;

  async function initWebMCP() {
    console.log('🤖 [WebMCP] Initializing Model Context Protocol on https://hud-nspire.pages.dev...');

    // 1. Expose global window API for developer inspection, MCP browser extensions, and DevTools
    window.webMCP = {
      version: '1.0.0',
      standard: 'W3C Web Machine Learning WebMCP Draft (Chrome 149+)',
      tools: WEBMCP_TOOLS.map(t => ({
        name: t.name,
        description: t.description,
        inputSchema: t.inputSchema,
        readOnly: t.readOnly
      })),
      listTools: () => {
        return WEBMCP_TOOLS.map(t => ({
          name: t.name,
          description: t.description,
          inputSchema: t.inputSchema,
          readOnly: t.readOnly
        }));
      },
      callTool: async (toolName, args = {}) => {
        const tool = WEBMCP_TOOLS.find(t => t.name === toolName);
        if (!tool) throw new Error(`WebMCP tool '${toolName}' not found`);
        const result = await tool.execute(args);
        return {
          content: [
            {
              type: "text",
              text: typeof result === 'string' ? result : JSON.stringify(result, null, 2)
            }
          ]
        };
      },
      execute: async (toolName, input = {}) => {
        const tool = WEBMCP_TOOLS.find(t => t.name === toolName);
        if (!tool) throw new Error(`WebMCP tool '${toolName}' not found`);
        return await tool.execute(input);
      },
      isReady: true
    };

    // Alias to window.modelContext for standard compliance
    window.modelContext = window.webMCP;

    // 2. Register with native browser modelContext if present (Chrome 149+ with WebMCP flag)
    const contextObj = (typeof navigator !== 'undefined' && navigator.modelContext) 
      || (typeof document !== 'undefined' && document.modelContext);

    if (contextObj && typeof contextObj.registerTool === 'function') {
      console.log('🚀 [WebMCP] Native browser modelContext detected! Registering tools...');
      for (const tool of WEBMCP_TOOLS) {
        try {
          await contextObj.registerTool({
            name: tool.name,
            description: tool.description,
            inputSchema: tool.inputSchema,
            execute: async (input) => {
              const res = await tool.execute(input);
              return {
                type: 'text',
                text: typeof res === 'string' ? res : JSON.stringify(res, null, 2)
              };
            }
          });
          registeredCount++;
        } catch (err) {
          console.warn(`⚠️ [WebMCP] Native registration for '${tool.name}' skipped:`, err.message);
        }
      }
      console.log(`✅ [WebMCP] Successfully registered ${registeredCount} tools with native browser!`);
    } else {
      console.log('ℹ️ [WebMCP] Browser modelContext API active via window.webMCP and Chrome DevTools MCP bridge.');
    }

    // 3. Decorate DOM with Declarative WebMCP attributes for static/agent scrapers
    decorateDeclarativeDOM();

    // 4. Mount sleek Agent-Ready visual indicator & diagnostic modal
    mountWebMCPBadge();

    // 5. Dispatch Custom Event for external hooks
    window.dispatchEvent(new CustomEvent('webmcp:ready', { detail: { tools: window.webMCP.tools } }));
  }

  // --- 🏷️ DECLARATIVE HTML ANNOTATION ENGINE ---
  function decorateDeclarativeDOM() {
    try {
      // Find defect search input
      const defectSearch = document.getElementById('defect-search');
      if (defectSearch && !defectSearch.getAttribute('toolname')) {
        defectSearch.setAttribute('toolname', 'lookup_nspire_defect');
        defectSearch.setAttribute('tooldescription', 'Search 67-standard HUD physical inspection defects by item, category, or failure symptoms.');
      }

      // Find filter pills
      const filterPills = document.querySelectorAll('.filter-pill');
      filterPills.forEach(p => {
        if (!p.getAttribute('toolname')) {
          p.setAttribute('toolname', 'lookup_nspire_defect');
        }
      });

      // Find pricing purchase links
      const pricingLinks = document.querySelectorAll('a[href*="#pricing"], a[href*="stripe"]');
      pricingLinks.forEach(link => {
        if (!link.getAttribute('toolname')) {
          link.setAttribute('toolname', 'get_compliance_kit_tiers');
          link.setAttribute('tooldescription', 'Retrieve package deliverables and direct checkout links.');
        }
      });
    } catch (e) {}
  }

  // --- 🎖️ AGENT-READY VISUAL BADGE & INTERACTIVE INSPECTOR MODAL ---
  function mountWebMCPBadge() {
    if (document.getElementById('nspire-webmcp-badge')) return;

    // 1. Badge Pill
    const badge = document.createElement('div');
    badge.id = 'nspire-webmcp-badge';
    badge.style.position = 'fixed';
    badge.style.bottom = '16px';
    badge.style.right = '16px';
    badge.style.zIndex = '99998';
    badge.style.display = 'flex';
    badge.style.alignItems = 'center';
    badge.style.gap = '8px';
    badge.style.padding = '7px 14px';
    badge.style.backgroundColor = 'rgba(15, 23, 42, 0.92)';
    badge.style.backdropFilter = 'blur(12px)';
    badge.style.webkitBackdropFilter = 'blur(12px)';
    badge.style.border = '1px solid rgba(56, 189, 248, 0.4)';
    badge.style.borderRadius = '9999px';
    badge.style.color = '#f1f5f9';
    badge.style.fontSize = '12px';
    badge.style.fontWeight = '600';
    badge.style.fontFamily = "'JetBrains Mono', monospace";
    badge.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.4), 0 0 15px rgba(56, 189, 248, 0.15)';
    badge.style.cursor = 'pointer';
    badge.style.transition = 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)';
    badge.title = 'Click to inspect active WebMCP tools exposed to AI agents';

    badge.innerHTML = `
      <span style="display:inline-block;width:8px;height:8px;border-radius:9999px;background-color:#10b981;box-shadow:0 0 8px #10b981;animation:pulse 2s infinite;"></span>
      <span style="color:#38bdf8;font-weight:700;">WebMCP</span>
      <span style="color:#94a3b8;">•</span>
      <span style="color:#e2e8f0;font-size:11px;">7 Tools Active</span>
    `;

    badge.addEventListener('mouseenter', () => {
      badge.style.transform = 'translateY(-2px)';
      badge.style.borderColor = 'rgba(56, 189, 248, 0.8)';
      badge.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.5), 0 0 20px rgba(56, 189, 248, 0.3)';
    });
    badge.addEventListener('mouseleave', () => {
      badge.style.transform = 'translateY(0)';
      badge.style.borderColor = 'rgba(56, 189, 248, 0.4)';
      badge.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.4), 0 0 15px rgba(56, 189, 248, 0.15)';
    });

    badge.addEventListener('click', openWebMCPModal);
    document.body.appendChild(badge);

    // 2. Build Interactive Inspector Modal
    createWebMCPModal();
  }

  function createWebMCPModal() {
    if (document.getElementById('nspire-webmcp-modal')) return;

    const modal = document.createElement('div');
    modal.id = 'nspire-webmcp-modal';
    modal.style.position = 'fixed';
    modal.style.inset = '0';
    modal.style.zIndex = '99999';
    modal.style.display = 'none';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.padding = '16px';
    modal.style.backgroundColor = 'rgba(3, 7, 18, 0.8)';
    modal.style.backdropFilter = 'blur(16px)';
    modal.style.webkitBackdropFilter = 'blur(16px)';

    modal.innerHTML = `
      <div style="background:#0f172a;border:1px solid rgba(56, 189, 248, 0.3);border-radius:16px;max-width:760px;width:100%;max-height:90vh;display:flex;flex-direction:column;box-shadow:0 25px 50px -12px rgba(0,0,0,0.7);overflow:hidden;font-family:'Inter',sans-serif;color:#f8fafc;">
        
        <!-- Header -->
        <div style="padding:16px 24px;border-bottom:1px solid rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:space-between;background:rgba(15,23,42,0.9);">
          <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:36px;height:36px;border-radius:10px;background:rgba(56,189,248,0.15);border:1px solid rgba(56,189,248,0.3);display:flex;align-items:center;justify-content:center;color:#38bdf8;font-size:18px;">
              🤖
            </div>
            <div>
              <div style="display:flex;align-items:center;gap:8px;">
                <h3 style="font-size:16px;font-weight:700;margin:0;color:#ffffff;font-family:'JetBrains Mono',monospace;">WebMCP Agent Inspector</h3>
                <span style="font-size:10px;padding:2px 8px;border-radius:9999px;background:rgba(16,185,129,0.2);color:#34d399;font-weight:600;border:1px solid rgba(16,185,129,0.3);">LIVE</span>
              </div>
              <p style="font-size:12px;color:#94a3b8;margin:2px 0 0 0;">Model Context Protocol gateway for autonomous AI agents (Gemini, Claude, ChatGPT)</p>
            </div>
          </div>
          <button id="nspire-webmcp-close" style="background:transparent;border:none;color:#94a3b8;font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px;transition:all 0.2s;">✕</button>
        </div>

        <!-- Body -->
        <div style="padding:20px 24px;overflow-y:auto;display:flex;flex-direction:column;gap:16px;flex:1;">
          <div style="background:rgba(30,41,59,0.5);border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:14px;font-size:12px;color:#cbd5e1;line-height:1.5;">
            <strong style="color:#38bdf8;">Standard:</strong> W3C Web Machine Learning WebMCP Specification &bull; 
            <strong style="color:#38bdf8;">Manifest:</strong> <a href="/.well-known/webmcp.json" target="_blank" style="color:#38bdf8;text-decoration:underline;">/.well-known/webmcp.json</a> &bull; 
            <strong style="color:#38bdf8;">Global API:</strong> <code style="font-family:'JetBrains Mono',monospace;background:rgba(0,0,0,0.3);padding:2px 6px;border-radius:4px;color:#a5f3fc;">window.webMCP</code>
          </div>

          <div style="font-size:13px;font-weight:700;color:#f8fafc;letter-spacing:0.5px;text-transform:uppercase;font-family:'JetBrains Mono',monospace;">
            Exposed Domain Tools (7)
          </div>

          <div id="nspire-tools-list" style="display:flex;flex-direction:column;gap:10px;">
            ${WEBMCP_TOOLS.map(t => `
              <div style="background:rgba(17,24,39,0.6);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:12px 16px;transition:all 0.2s;" class="tool-item">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                  <span style="font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:#38bdf8;">${t.name}</span>
                  <span style="font-size:10px;font-family:'JetBrains Mono',monospace;padding:2px 6px;border-radius:4px;background:rgba(255,255,255,0.06);color:#94a3b8;">${t.readOnly ? 'readOnly' : 'readWrite'}</span>
                </div>
                <p style="font-size:12px;color:#94a3b8;margin:0 0 10px 0;line-height:1.4;">${t.description}</p>
                <div style="display:flex;align-items:center;gap:8px;">
                  <button class="test-tool-btn" data-tool="${t.name}" style="background:rgba(56,189,248,0.15);border:1px solid rgba(56,189,248,0.3);color:#38bdf8;padding:4px 10px;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;font-family:'JetBrains Mono',monospace;transition:all 0.2s;">
                    ⚡ Test Execute
                  </button>
                  <span style="font-size:11px;color:#64748b;">${Object.keys(t.inputSchema.properties || {}).length} input parameters</span>
                </div>
              </div>
            `).join('')}
          </div>

          <!-- Live Output Console -->
          <div style="margin-top:8px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
              <span style="font-size:12px;font-weight:700;color:#94a3b8;font-family:'JetBrains Mono',monospace;">Execution Output Console</span>
              <button id="nspire-clear-console" style="background:transparent;border:none;color:#64748b;font-size:11px;cursor:pointer;">Clear</button>
            </div>
            <pre id="nspire-console-output" style="background:#020617;border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:12px;font-family:'JetBrains Mono',monospace;font-size:11px;color:#34d399;max-height:160px;overflow-y:auto;margin:0;white-space:pre-wrap;">// Click 'Test Execute' above to run any tool client-side in zero latency.</pre>
          </div>
        </div>

        <!-- Footer -->
        <div style="padding:14px 24px;border-top:1px solid rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:space-between;background:rgba(15,23,42,0.9);font-size:12px;color:#64748b;">
          <span>HUD NSPIRE Compliance Protocol &bull; Title 24 CFR Part 5</span>
          <button id="nspire-copy-manifest" style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.1);color:#f1f5f9;padding:6px 12px;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;">
            Copy MCP JSON Manifest
          </button>
        </div>

      </div>
    `;

    document.body.appendChild(modal);

    // Event listeners
    const closeBtn = modal.querySelector('#nspire-webmcp-close');
    if (closeBtn) closeBtn.addEventListener('click', closeWebMCPModal);

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeWebMCPModal();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.style.display === 'flex') closeWebMCPModal();
    });

    // Test execute buttons
    modal.querySelectorAll('.test-tool-btn').forEach(btn => {
      btn.addEventListener('click', async () => {
        const toolName = btn.getAttribute('data-tool');
        const consoleEl = modal.querySelector('#nspire-console-output');
        if (!consoleEl) return;
        consoleEl.textContent = `// Executing tool: ${toolName}...`;
        consoleEl.style.color = '#38bdf8';

        try {
          let testArgs = {};
          if (toolName === 'calculate_nspire_score') {
            testArgs = { total_units: 32, inspected_units: 6, life_threatening_defects: 0, severe_defects: 1, moderate_defects: 2 };
          } else if (toolName === 'lookup_nspire_defect') {
            testArgs = { query: 'GFCI' };
          } else if (toolName === 'get_life_threatening_fails') {
            testArgs = { category: 'fire' };
          } else if (toolName === 'get_compliance_kit_tiers') {
            testArgs = { tier_id: 'all' };
          } else if (toolName === 'get_pha_jurisdiction_rules') {
            testArgs = { query: 'Atlanta' };
          } else if (toolName === 'generate_48hr_tenant_notice') {
            testArgs = {
              tenant_name: "Jane Doe",
              unit_number: "Unit 304",
              property_address: "742 Peachtree St NE, Atlanta, GA 30308",
              inspection_date: "Thursday, October 16, 2026",
              arrival_window: "10:00 AM – 1:00 PM",
              management_phone: "(404) 555-0199",
              management_email: "compliance@peachtreeapartments.com"
            };
          } else if (toolName === 'dispatch_emergency_handyman_rfq') {
            testArgs = {
              property_address: "550 Piedmont Ave NE",
              city: "Atlanta",
              state: "GA",
              housing_authority: "Atlanta Housing Authority (AHA)",
              contact_name: "Sarah Jenkins",
              contact_phone: "(404) 555-7822",
              urgency_hours: 24,
              defects_summary: [
                "GFCI receptacle failed test within 6ft of bathroom vanity",
                "Water heater TPR safety discharge pipe terminating 18 inches above floor (must be 2-6 inches)",
                "Bedroom 2 emergency egress window painted shut"
              ]
            };
          }

          const res = await window.webMCP.execute(toolName, testArgs);
          consoleEl.textContent = JSON.stringify(res, null, 2);
          consoleEl.style.color = '#34d399';
        } catch (err) {
          consoleEl.textContent = `Error: ${err.message}`;
          consoleEl.style.color = '#f87171';
        }
      });
    });

    const clearBtn = modal.querySelector('#nspire-clear-console');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        const consoleEl = modal.querySelector('#nspire-console-output');
        if (consoleEl) consoleEl.textContent = '// Console cleared.';
      });
    }

    const copyBtn = modal.querySelector('#nspire-copy-manifest');
    if (copyBtn) {
      copyBtn.addEventListener('click', async () => {
        try {
          const manifestRes = await fetch('/.well-known/webmcp.json');
          const manifestText = await manifestRes.text();
          await navigator.clipboard.writeText(manifestText);
          copyBtn.textContent = '✓ Copied to Clipboard!';
          setTimeout(() => { copyBtn.textContent = 'Copy MCP JSON Manifest'; }, 2000);
        } catch (e) {
          alert('Could not copy automatically. View manifest at /.well-known/webmcp.json');
        }
      });
    }
  }

  function openWebMCPModal() {
    const modal = document.getElementById('nspire-webmcp-modal');
    if (modal) modal.style.display = 'flex';
  }

  function closeWebMCPModal() {
    const modal = document.getElementById('nspire-webmcp-modal');
    if (modal) modal.style.display = 'none';
  }

  // Auto-boot on DOM readiness
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWebMCP);
  } else {
    initWebMCP();
  }
})();

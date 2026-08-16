#!/usr/bin/env python3
"""
Static site generator for the San Antonio handyman lead-gen site.

Why this exists: this business model (per the Website Landlord playbook)
is "pick a niche + city, build a site, rank it, forward leads." This script
is reusable — swap CONFIG and SERVICES below for the next niche/city and
run it again to spin up a new site in minutes. Keep it if you (or Taylor)
want to clone this pattern for city #2.

Usage: python3 generate.py
Output: writes .html files into the current directory (alongside css/, js/).
"""
import os
import json
import re

# ============================================================
# CONFIG — swap these for a new niche/city clone
# ============================================================
BUSINESS_NAME = "San Antonio Handyman Pros"
CITY = "San Antonio"
STATE = "TX"
STATE_FULL = "Texas"
DOMAIN = "sanantoniohandymanpros.com"          # PLACEHOLDER — pick your real domain
PHONE_DISPLAY = "(210) 555-0142"                # PLACEHOLDER — forwarding number
PHONE_TEL = "+12105550142"                      # PLACEHOLDER — E.164 for tel: links
EMAIL = "leads@sanantoniohandymanpros.com"      # PLACEHOLDER — forwarding inbox
ADDRESS_LOCALITY = "San Antonio"
ADDRESS_REGION = "TX"
LATITUDE = "29.4241"
LONGITUDE = "-98.4936"
YEAR = "2026"

# Analytics placeholders — fill these in before launch, see README.
GA4_ID = "G-XXXXXXXXXX"                # Google Analytics 4 measurement ID
AHREFS_KEY = "YOUR_AHREFS_ANALYTICS_KEY"  # Ahrefs Web Analytics key
AHREFS_SITE_VERIFICATION = "YOUR_AHREFS_VERIFICATION_TOKEN"  # ahrefs-site-verification meta

NEIGHBORHOODS = [
    "Alamo Heights", "Stone Oak", "Terrell Hills", "Olmos Park",
    "Hollywood Park", "Castle Hills", "Leon Valley", "Universal City",
    "Schertz", "Converse", "Live Oak", "Windcrest", "Helotes",
    "Cibolo", "Shavano Park", "Downtown San Antonio", "The Dominion",
    "Alamo Ranch", "Northwest San Antonio", "Southtown",
]

SITE_ROOT = "https://www." + DOMAIN

# ============================================================
# SERVICES — each is its own bottom-of-funnel landing page
# ============================================================
SERVICES = [
    {
        "slug": "emergency-handyman-san-antonio",
        "name": "Emergency & Same-Day Handyman",
        "kw": "emergency handyman San Antonio",
        "title": "Emergency Handyman San Antonio, TX | Same-Day Repairs",
        "meta": "Need a handyman today? San Antonio's same-day emergency handyman service handles urgent repairs fast. Call now for a free estimate — no job too small.",
        "h1": "Emergency Handyman Service in San Antonio, TX",
        "intro": "A broken door lock, a leaking pipe under the sink, or a fence panel down after a storm doesn't wait for a convenient time. Our San Antonio emergency handyman network takes same-day and next-day calls across the metro, including nights and weekends for urgent situations. Tell us what's wrong, get a straightforward estimate, and we'll get someone out to fix it — not just patch it.",
        "included": [
            "Same-day and next-day scheduling for urgent repairs",
            "Weekend availability across the San Antonio metro",
            "Storm-damage triage: fencing, doors, gutters, minor roof leaks",
            "Lockouts, broken hinges, and door/window security fixes",
            "Burst-pipe shutoff and minor plumbing emergencies",
            "Upfront, no-surprise estimate before any work begins",
        ],
        "why": "Emergencies get expensive fast when a small problem is left to sit — a slow leak becomes water damage, a loose fence becomes a liability. Getting a licensed, insured pro out quickly usually costs far less than waiting.",
        "faqs": [
            ("How fast can someone come out?", "Most San Antonio emergency requests are scheduled same-day or next-day, depending on the time of your call and the nature of the repair. Call the number above and we'll give you a real-time estimate on arrival."),
            ("Do you charge extra for emergency calls?", "Urgent same-day scheduling may carry a service fee depending on timing. You'll always get a clear quote before any work starts — no surprise charges."),
            ("What counts as an emergency repair?", "Anything that risks further damage or safety if it waits: active leaks, broken exterior locks, storm damage, downed fencing near a street or pool, and similar issues."),
        ],
    },
    {
        "slug": "drywall-repair-san-antonio",
        "name": "Drywall Repair",
        "kw": "drywall repair San Antonio",
        "title": "Drywall Repair San Antonio, TX | Patch, Texture & Paint-Ready",
        "meta": "Holes, cracks, water stains, or nail pops in your drywall? San Antonio drywall repair pros patch, texture-match, and leave walls paint-ready. Free estimates.",
        "h1": "Drywall Repair in San Antonio, TX",
        "intro": "Doorknob holes, hairline cracks from foundation settling, water stains from an old roof leak — San Antonio homes see all of it. Our drywall repair techs match your existing texture (knockdown, orange peel, smooth) so the patch disappears instead of standing out, and leave the wall ready for your painter or ours.",
        "included": [
            "Small hole and doorknob-dent patching",
            "Crack repair, including recurring cracks from foundation movement",
            "Water-stain drywall replacement and moisture check",
            "Texture matching: knockdown, orange peel, smooth",
            "Popped nail and screw repair",
            "Ceiling drywall repair and patching",
        ],
        "why": "A DIY patch that doesn't match texture or gets the mud ratio wrong is obvious under any light and often needs to be redone anyway. A pro gets it flat, matched, and paint-ready in one visit for most jobs.",
        "faqs": [
            ("Can you match my wall's texture?", "Yes — knockdown, orange peel, and smooth finishes are all matched on-site so the repair blends in rather than standing out."),
            ("Is a cracked wall a sign of a bigger problem?", "Sometimes. Hairline cracks are common with normal home settling in San Antonio's clay soil, but recurring or widening cracks are worth a second look — we'll flag it if we see something that needs more than a patch."),
            ("Do you also paint after the repair?", "We can leave the area paint-ready or handle the touch-up paint too — just ask when you request your estimate."),
        ],
    },
    {
        "slug": "tv-mounting-san-antonio",
        "name": "TV Mounting",
        "kw": "TV mounting San Antonio",
        "title": "TV Mounting Service San Antonio, TX | Wall Mount Installation",
        "meta": "Professional TV wall mounting in San Antonio — studs found, cables hidden, level every time. Any size TV, any wall type. Get a free quote today.",
        "h1": "TV Mounting Service in San Antonio, TX",
        "intro": "A crooked TV or cables hanging down the wall isn't the look you paid for. Our San Antonio TV mounting techs find the studs (or use the right anchors for brick, stucco, and tile), hide the cable run, and make sure it's level and secure — done right the first time, whatever size TV or wall you've got.",
        "included": [
            "Stud-mounted or heavy-duty anchor installation for any wall type",
            "In-wall cable concealment (no dangling cords)",
            "Full-motion, tilt, or fixed mount installation — your mount or ours",
            "Soundbar and shelf mounting alongside the TV",
            "Fireplace and brick/stucco mounting",
            "Old mount removal and TV re-hang",
        ],
        "why": "TVs are heavy, walls in San Antonio homes vary from drywall to brick veneer to stucco, and a mount that's not anchored into real structure is a safety risk to kids, pets, and the TV itself.",
        "faqs": [
            ("Do you supply the mount, or do I?", "Either — bring your own mount or we can recommend and supply one that fits your TV and wall type."),
            ("Can you mount over brick or stucco?", "Yes, we use the correct masonry anchors for brick, stone, and stucco walls, common in a lot of San Antonio homes."),
            ("Can you hide the cables inside the wall?", "In most cases, yes — an in-wall cable kit routes power and HDMI so nothing hangs down. We'll confirm it's feasible for your wall during the estimate."),
        ],
    },
    {
        "slug": "furniture-assembly-san-antonio",
        "name": "Furniture Assembly",
        "kw": "furniture assembly San Antonio",
        "title": "Furniture Assembly San Antonio, TX | IKEA, Wayfair & More",
        "meta": "Skip the instructions. San Antonio furniture assembly for IKEA, Wayfair, Amazon, and flat-pack furniture of any kind — fast, careful, and guaranteed level.",
        "h1": "Furniture Assembly in San Antonio, TX",
        "intro": "New furniture in the box is progress; furniture actually built and in place is the win. We assemble flat-pack furniture from any retailer — IKEA, Wayfair, Amazon, Target, you name it — beds, dressers, desks, shelving, and office furniture, done right and hauled-away boxes on request.",
        "included": [
            "Bedroom sets: beds, dressers, nightstands, wardrobes",
            "Office furniture: desks, chairs, shelving, filing cabinets",
            "Flat-pack from IKEA, Wayfair, Amazon, Target, and others",
            "Outdoor and patio furniture assembly",
            "Multi-piece and whole-room assembly for movers and new-home setup",
            "Packaging removal and haul-away on request",
        ],
        "why": "Missing hardware, stripped screws, and misread diagrams turn a 45-minute job into a weekend. Our techs assemble this furniture regularly and know the common trouble spots before they cause a problem.",
        "faqs": [
            ("Do you assemble furniture from any store?", "Yes — IKEA, Wayfair, Amazon, Target, Costco, and most other flat-pack furniture brands."),
            ("What if a part is missing or damaged?", "We'll flag it immediately so you can get a replacement part from the manufacturer, and finish whatever we can in the meantime."),
            ("Can you take the boxes and packaging away?", "Just ask when booking — haul-away can be added to most furniture assembly visits."),
        ],
    },
    {
        "slug": "door-repair-installation-san-antonio",
        "name": "Door Repair & Installation",
        "kw": "door repair San Antonio",
        "title": "Door Repair & Installation San Antonio, TX | Interior & Exterior",
        "meta": "Sticking, sagging, or broken doors fixed fast in San Antonio. Interior and exterior door repair, hinge and lock fixes, and full door installation.",
        "h1": "Door Repair & Installation in San Antonio, TX",
        "intro": "A door that sticks, won't latch, or has a broken lock is more than annoying — it's a security gap. San Antonio's humidity and shifting soil both take a toll on door frames over time. We fix sagging doors, replace worn hinges and hardware, and install new interior or exterior doors, storm doors, and screen doors.",
        "included": [
            "Sticking, sagging, and misaligned door repair",
            "Hinge, handle, and deadbolt replacement",
            "Interior and exterior door installation",
            "Storm door and screen door installation and repair",
            "Weatherstripping and threshold replacement",
            "Sliding and closet door track repair",
        ],
        "why": "A door that doesn't close and latch properly is a real security and energy-efficiency issue, not just a cosmetic one. Most fixes are quick for a pro who knows whether the problem is the hinge, the frame, or the foundation shift behind it.",
        "faqs": [
            ("My door sticks only in summer — is that normal?", "Very common in San Antonio due to humidity and temperature swings. Sometimes it's a quick hinge adjustment; sometimes the door needs to be planed. We'll diagnose it on-site."),
            ("Can you replace just the lock, not the whole door?", "Yes, hardware-only replacement (locks, handles, deadbolts) is one of our most common calls."),
            ("Do you install exterior doors, not just repair them?", "Yes — full exterior and interior door installation, including storm and screen doors."),
        ],
    },
    {
        "slug": "fence-repair-san-antonio",
        "name": "Fence Repair",
        "kw": "fence repair San Antonio",
        "title": "Fence Repair San Antonio, TX | Wood, Chain-Link & Gate Fixes",
        "meta": "Leaning, broken, or storm-damaged fence? San Antonio fence repair for wood, chain-link, and gates. Fast estimates, quality repairs that last.",
        "h1": "Fence Repair in San Antonio, TX",
        "intro": "Texas storms and wind take a real toll on fences — leaning posts, snapped panels, gates that won't latch. We repair wood, chain-link, and iron fencing across San Antonio, replacing individual posts and panels instead of pushing a full rebuild when it isn't needed.",
        "included": [
            "Leaning and rotted fence post replacement",
            "Broken panel and picket repair (wood and composite)",
            "Chain-link fence patching and post repair",
            "Gate realignment, hinge, and latch repair",
            "Storm-damage fence assessment and repair",
            "Concrete post reset and re-set",
        ],
        "why": "A fence that's failing at the post usually doesn't need full replacement — resetting or replacing individual posts is faster and considerably cheaper, and it's often all that's needed.",
        "faqs": [
            ("Do I need a whole new fence or can it be repaired?", "Most fence problems are localized — a few posts, a panel, or a gate. We'll tell you honestly if repair makes sense or if replacement is the better value."),
            ("Can you match my existing wood fence style?", "Yes, we match board style, height, and spacing so repaired sections blend with the rest of the fence."),
            ("Do you fix gates that won't latch?", "Yes — gate sag and latch misalignment is one of the most common fence calls we get."),
        ],
    },
    {
        "slug": "deck-patio-repair-san-antonio",
        "name": "Deck & Patio Repair",
        "kw": "deck repair San Antonio",
        "title": "Deck & Patio Repair San Antonio, TX | Boards, Rails & Stairs",
        "meta": "Wobbly rails, warped boards, or unsafe steps? San Antonio deck and patio repair — board replacement, railing fixes, and structural checks.",
        "h1": "Deck & Patio Repair in San Antonio, TX",
        "intro": "Texas sun and humidity are hard on outdoor wood — warped boards, loose railings, and stairs that have gotten a little too bouncy are the usual culprits. We repair and reinforce decks and patio structures across San Antonio, replacing what's failing and checking what's structural before you have guests over it.",
        "included": [
            "Warped, cracked, and splintered board replacement",
            "Railing and baluster repair and reinforcement",
            "Stair and step repair for safety",
            "Deck fastener and ledger board inspection",
            "Re-staining and sealing after repair",
            "Screened porch and patio cover repair",
        ],
        "why": "Deck failures are one of the more dangerous things to put off — a soft board or loose railing that seems minor can give way under weight. A quick structural check and targeted repair usually costs far less than people expect.",
        "faqs": [
            ("How do I know if my deck is actually unsafe?", "Soft or spongy boards, wobbly railings, and rust on fasteners are the big warning signs. If you're unsure, we'll do a quick structural check as part of the estimate."),
            ("Can you match new boards to weathered ones?", "We can stain or seal repaired sections to blend with the existing deck, though some color variation with older wood is normal until it weathers evenly."),
            ("Do you work on patio covers too?", "Yes, we handle patio cover and screened porch structural repair in addition to decks."),
        ],
    },
    {
        "slug": "gutter-cleaning-repair-san-antonio",
        "name": "Gutter Cleaning & Repair",
        "kw": "gutter repair San Antonio",
        "title": "Gutter Cleaning & Repair San Antonio, TX | Leaks, Sagging & Clogs",
        "meta": "Clogged, sagging, or leaking gutters in San Antonio? Cleaning, resealing, and repair to protect your foundation and roofline. Free estimates.",
        "h1": "Gutter Cleaning & Repair in San Antonio, TX",
        "intro": "Clogged gutters send water straight down your foundation instead of away from it — a real problem in San Antonio's clay soil. We clean out debris, reseal and reattach sagging sections, and fix leaks at the seams and downspouts so water actually goes where it's supposed to.",
        "included": [
            "Full gutter debris clean-out",
            "Sagging gutter re-hanging and bracket replacement",
            "Seam and joint resealing for leaks",
            "Downspout repair and extension/redirection",
            "Gutter guard installation",
            "Minor fascia board check where gutters attach",
        ],
        "why": "Water pooling near your foundation from a clogged or misdirected gutter is one of the more expensive problems to ignore in San Antonio's shifting clay soil — a cleaning and reseal now is cheap insurance against foundation repair later.",
        "faqs": [
            ("How often should gutters be cleaned in San Antonio?", "Twice a year is typical (spring and fall), more often if you've got a lot of oak or pecan trees overhead."),
            ("Can a sagging gutter be fixed, or does it need replacing?", "Most sagging is a bracket or fastener issue that can be repaired in place — full replacement is rarely needed."),
            ("Do you install gutter guards?", "Yes, we install guards to cut down on future clogging, especially useful under tree cover."),
        ],
    },
    {
        "slug": "minor-plumbing-repair-san-antonio",
        "name": "Minor Plumbing Repair",
        "kw": "minor plumbing repair San Antonio",
        "title": "Minor Plumbing Repair San Antonio, TX | Leaks, Faucets & Fixtures",
        "meta": "Leaky faucet, running toilet, or dripping pipe in San Antonio? Fast minor plumbing repairs and fixture installs — no job too small.",
        "h1": "Minor Plumbing Repair in San Antonio, TX",
        "intro": "Not every plumbing issue needs an emergency plumber — a lot of the day-to-day stuff (a leaky faucet, a running toilet, a garbage disposal that won't turn on) is exactly what our San Antonio handyman team handles quickly and affordably, without the emergency-plumber price tag.",
        "included": [
            "Leaky faucet and showerhead repair",
            "Running or clogged toilet repair",
            "Garbage disposal replacement and repair",
            "Sink and fixture installation",
            "Minor pipe leak repair (under sinks, exposed lines)",
            "Water heater component checks and minor fixes",
        ],
        "why": "Small leaks waste real money over months and can lead to water damage if ignored. Most of these fixes take under an hour for a handyman and cost a fraction of an emergency plumbing call-out.",
        "faqs": [
            ("Is this a licensed plumber or a handyman?", "Our team handles minor, non-permit plumbing repairs and fixture installs. For major re-pipes or code-required work, we'll tell you upfront and can point you toward a licensed plumber."),
            ("Can you install a new faucet I bought?", "Yes — bring your own fixture or we can source one, either way."),
            ("What if the leak turns out to be bigger than expected?", "We'll always tell you honestly if a job is outside minor-repair scope before continuing, so there are no surprise costs."),
        ],
    },
    {
        "slug": "minor-electrical-repair-san-antonio",
        "name": "Minor Electrical Repair",
        "kw": "minor electrical repair San Antonio",
        "title": "Minor Electrical Repair San Antonio, TX | Outlets, Fixtures & Fans",
        "meta": "Outlet not working, flickering light, or need a ceiling fan installed in San Antonio? Minor electrical repairs and fixture installs, done safely.",
        "h1": "Minor Electrical Repair in San Antonio, TX",
        "intro": "Dead outlets, flickering lights, and fans that need mounting are some of the most requested handyman jobs in San Antonio. Our techs handle everyday electrical fixes and fixture installs safely and up to code for non-permit work — and tell you straight if something needs a licensed electrician instead.",
        "included": [
            "Outlet and switch replacement (including GFCI)",
            "Light fixture installation and repair",
            "Ceiling fan installation and mounting",
            "Dimmer switch installation",
            "Flickering light and minor circuit troubleshooting",
            "Doorbell and exterior fixture wiring",
        ],
        "why": "Flickering lights or a dead outlet are often a quick fix, but electrical work is one area where 'quick DIY fix' can go wrong fast. Getting it done right the first time protects your home and your breaker panel.",
        "faqs": [
            ("Can you install a ceiling fan where a light used to be?", "In most cases yes — we'll check that the existing electrical box is fan-rated (or replace it) before mounting."),
            ("Is this licensed electrician work?", "We handle minor, non-permit electrical repairs and fixture swaps. For panel work or new circuits, we'll let you know it needs a licensed electrician."),
            ("Why does my outlet keep tripping?", "Could be an overloaded circuit, a worn GFCI, or a wiring issue — we'll diagnose it on-site rather than guess over the phone."),
        ],
    },
    {
        "slug": "interior-exterior-painting-san-antonio",
        "name": "Interior & Exterior Painting",
        "kw": "handyman painting San Antonio",
        "title": "Interior & Exterior Painting San Antonio, TX | Touch-Ups & Rooms",
        "meta": "Room repaints, trim touch-ups, and exterior touch-up painting in San Antonio. Clean lines, proper prep, no drips. Get a free painting estimate.",
        "h1": "Interior & Exterior Painting in San Antonio, TX",
        "intro": "Scuffed walls before a move-out, a single room that needs a refresh, or exterior trim that's peeling in the Texas sun — our painting jobs are sized for handyman-scale work, not whole-house repaints. Clean cut lines, proper surface prep, and no drips left behind.",
        "included": [
            "Single-room and accent-wall painting",
            "Trim, baseboard, and door painting",
            "Drywall patch touch-up blending after repairs",
            "Exterior trim and fascia touch-up painting",
            "Move-out and move-in scuff and wall repainting",
            "Cabinet and shelving touch-up painting",
        ],
        "why": "A rushed paint job shows in the cut lines and roller marks within a week. Proper taping, prep, and two coats where needed is the difference between a wall that looks refreshed and one that looks patched.",
        "faqs": [
            ("Do you supply the paint or do I?", "Either — we can pick up a color you've chosen, or bring recommendations based on the space."),
            ("Can you paint after a drywall repair so it blends in?", "Yes, blending a patch into the surrounding wall is exactly the kind of job we handle regularly."),
            ("Do you do full exterior house painting?", "We focus on trim, touch-ups, and smaller exterior sections rather than full house repaints — ask and we'll tell you honestly if your job fits."),
        ],
    },
]

NAV_LINKS = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("service-area.html", "Service Area"),
    ("contact.html", "Free Quote"),
]

# ============================================================
# Shared JSON-LD
# ============================================================
def local_business_schema():
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": SITE_ROOT + "/#business",
        "name": BUSINESS_NAME,
        "image": SITE_ROOT + "/og-image.jpg",
        "url": SITE_ROOT + "/",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": ADDRESS_LOCALITY,
            "addressRegion": ADDRESS_REGION,
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": LATITUDE, "longitude": LONGITUDE},
        "areaServed": {"@type": "City", "name": "San Antonio, TX"},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "07:00",
            "closes": "19:00",
        }],
        "sameAs": [],
    }


def breadcrumb_schema(items):
    # items: list of (name, url)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(items)
        ],
    }


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def service_schema(svc):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": svc["name"],
        "provider": {"@type": "LocalBusiness", "name": BUSINESS_NAME, "telephone": PHONE_TEL},
        "areaServed": {"@type": "City", "name": "San Antonio, TX"},
        "url": f"{SITE_ROOT}/{svc['slug']}.html",
    }


def ld(*schemas):
    if len(schemas) == 1:
        payload = schemas[0]
    else:
        payload = list(schemas)
    return f'<script type="application/ld+json">{json.dumps(payload, indent=None)}</script>'


# ============================================================
# Shared page chrome
# ============================================================
def head(title, description, path, extra_schema_html=""):
    canonical = f"{SITE_ROOT}/{path}"
    return f"""<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="ahrefs-site-verification" content="{AHREFS_SITE_VERIFICATION}">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BUSINESS_NAME}">

<link rel="stylesheet" href="/css/style.css">
<link rel="icon" href="data:,">

<!-- ====== ANALYTICS PLACEHOLDERS — fill in before launch, see README ====== -->
<!-- Google Analytics 4 (GA4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA4_ID}');
</script>
<!-- Ahrefs Web Analytics -->
<script src="https://analytics.ahrefs.com/analytics.js" data-key="{AHREFS_KEY}" async></script>
<!-- ====== END ANALYTICS PLACEHOLDERS ====== -->

{ld(local_business_schema())}
{extra_schema_html}
"""


def header_nav():
    links = "\n      ".join(f'<li><a href="{href}">{label}</a></li>' for href, label in NAV_LINKS)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/index.html">{BUSINESS_NAME}<span>Licensed &amp; Insured &middot; {CITY}, {STATE}</span></a>
    <nav class="main-nav" aria-label="Primary">
      <ul>
      {links}
      </ul>
    </nav>
    <div class="header-cta">
      <a class="header-phone" href="tel:{PHONE_TEL}"><small>Call Now</small>{PHONE_DISPLAY}</a>
      <a class="btn btn-primary" href="/contact.html">Free Quote</a>
    </div>
  </div>
</header>
"""


def mobile_call_bar():
    return f"""<div class="mobile-call-bar">
  <a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
  <a class="secondary" href="/contact.html">Get Free Quote</a>
</div>
"""


def footer():
    svc_links = "\n        ".join(
        f'<li><a href="/{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES
    )
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="grid grid-4">
      <div>
        <h4>{BUSINESS_NAME}</h4>
        <p>Local handyman services across {CITY}, {STATE} and the surrounding metro. Licensed &amp; insured. Free estimates.</p>
        <p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h4>Services</h4>
        <ul style="list-style:none;padding:0;">
        {svc_links}
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul style="list-style:none;padding:0;">
          <li><a href="/index.html">Home</a></li>
          <li><a href="/services.html">All Services</a></li>
          <li><a href="/service-area.html">Service Area</a></li>
          <li><a href="/contact.html">Free Quote</a></li>
        </ul>
      </div>
      <div>
        <h4>Hours</h4>
        <p>Mon&ndash;Sat: 7:00 AM &ndash; 7:00 PM<br>Emergency calls: by request</p>
      </div>
    </div>
    <div class="legal">
      <p>&copy; {YEAR} {BUSINESS_NAME}. Serving {CITY}, {STATE} and surrounding communities. &middot; <a href="/privacy-policy.html">Privacy Policy</a> &middot; <a href="/terms.html">Terms of Service</a></p>
    </div>
  </div>
</footer>
<script src="/js/script.js"></script>
"""


def page(title, description, path, body, extra_schema_html=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(title, description, path, extra_schema_html)}
</head>
<body>
{header_nav()}
{body}
{footer()}
{mobile_call_bar()}
</body>
</html>
"""


def breadcrumb_html(items):
    # items: list of (label, href) — last item has no href
    parts = []
    for i, (label, href) in enumerate(items):
        if href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span>{label}</span>')
    return f'<div class="wrap"><p class="breadcrumb">{" &rsaquo; ".join(parts)}</p></div>'


def icon(name):
    icons = {
        "check": '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-6"/></svg>',
        "wrench": '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 1 1-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 0 1 5.4-5.4z"/></svg>',
        "clock": '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
        "shield": '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6z"/></svg>',
    }
    return icons.get(name, icons["wrench"])


# ============================================================
# Reusable section blocks
# ============================================================
def quote_form_card(heading="Get a Free Estimate", sub="Tell us what you need fixed — we'll text or call back, usually within the hour during business hours."):
    return f"""<div class="quote-card">
  <h3>{heading}</h3>
  <p class="sub">{sub}</p>
  <form id="quote-form" name="quote-request" method="POST" data-netlify="true" netlify-honeypot="company" action="/thank-you.html">
    <input type="hidden" name="form-name" value="quote-request">
    <div class="honeypot">
      <label for="company">Company</label>
      <input type="text" id="company" name="company" tabindex="-1" autocomplete="off">
    </div>
    <div class="form-field">
      <label for="name">Full Name</label>
      <input type="text" id="name" name="name" required>
    </div>
    <div class="form-field">
      <label for="phone">Phone Number</label>
      <input type="tel" id="phone" name="phone" required>
    </div>
    <div class="form-field">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required>
    </div>
    <div class="form-field">
      <label for="zip">Property ZIP Code</label>
      <input type="text" id="zip" name="zip" required>
    </div>
    <div class="form-field">
      <label for="service">What do you need done?</label>
      <select id="service" name="service" required>
        <option value="">Select a service</option>
        {"".join(f'<option value="{s["name"]}">{s["name"]}</option>' for s in SERVICES)}
        <option value="Something else">Something else</option>
      </select>
    </div>
    <div class="form-field">
      <label for="message">Details (optional)</label>
      <textarea id="message" name="message" rows="3"></textarea>
    </div>
    <button type="submit" class="btn btn-primary btn-block btn-lg">Request My Free Estimate</button>
    <p class="form-note">No obligation. We'll never sell your info. Prefer to talk? Call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
  </form>
</div>"""


def services_grid(exclude_slug=None, limit=None):
    items = [s for s in SERVICES if s["slug"] != exclude_slug]
    if limit:
        items = items[:limit]
    cards = []
    for s in items:
        cards.append(f"""<div class="card service-card">
      <div class="icon">{icon('wrench')}</div>
      <h3><a href="/{s['slug']}.html">{s['name']}</a></h3>
      <p>{s['intro'][:110].rsplit(' ', 1)[0]}&hellip;</p>
      <a class="more" href="/{s['slug']}.html">See details &rarr;</a>
    </div>""")
    return f'<div class="grid grid-3">\n    {"".join(cards)}\n    </div>'


def neighborhoods_chip_list():
    chips = "\n      ".join(f"<li>{n}</li>" for n in NEIGHBORHOODS)
    return f'<ul class="chip-list">\n      {chips}\n      </ul>'


def faq_block(faqs):
    items = "\n    ".join(
        f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs
    )
    return f'<div>\n    {items}\n    </div>'


def cta_band(heading="Ready to Get It Fixed?", sub="Free estimates. Licensed &amp; insured. Most calls answered same day."):
    return f"""<section class="cta-band">
  <div class="wrap">
    <h2>{heading}</h2>
    <p>{sub}</p>
    <div class="cta-row center" style="justify-content:center;">
      <a class="btn btn-navy btn-lg" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
      <a class="btn btn-outline btn-lg" href="/contact.html">Request Free Estimate</a>
    </div>
  </div>
</section>"""


# ============================================================
# Page builders
# ============================================================
def build_home():
    hero = f"""<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow">San Antonio, TX &middot; Licensed &amp; Insured</span>
      <h1>Handyman Services in San Antonio, TX &mdash; Same-Day Estimates</h1>
      <p class="lead">From drywall patches to fence repair, TV mounting to minor plumbing &mdash; one call gets it fixed. Serving San Antonio and the surrounding metro with upfront pricing and no wasted trips.</p>
      <ul class="badges">
        <li>{icon('shield')} Licensed &amp; Insured</li>
        <li>{icon('clock')} Same-Day Estimates</li>
        <li>{icon('check')} No Job Too Small</li>
      </ul>
      <div class="cta-row">
        <a class="btn btn-primary btn-lg" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
        <a class="btn btn-outline btn-lg" href="/contact.html">Get a Free Estimate</a>
      </div>
    </div>
    {quote_form_card()}
  </div>
</section>"""

    stats = f"""<section class="section section-tight">
  <div class="wrap">
    <div class="grid grid-4">
      <div class="stat"><div class="num">10+</div><div class="label">Handyman Specialties</div></div>
      <div class="stat"><div class="num">San Antonio</div><div class="label">Metro-Wide Coverage</div></div>
      <div class="stat"><div class="num">Same-Day</div><div class="label">Estimates Available</div></div>
      <div class="stat"><div class="num">100%</div><div class="label">Free, No-Obligation Quotes</div></div>
    </div>
  </div>
</section>"""

    services_section = f"""<section class="section bg-gray" id="services">
  <div class="wrap">
    <span class="eyebrow center" style="display:block;text-align:center;">What We Fix</span>
    <h2 class="center">San Antonio Handyman Services</h2>
    <p class="center text-muted" style="max-width:640px;margin:0 auto 30px;">Pick a service below for details and pricing guidance, or just call &mdash; if it's a repair around the house, chances are we handle it.</p>
    {services_grid()}
  </div>
</section>"""

    why = f"""<section class="section">
  <div class="wrap two-col">
    <div>
      <span class="eyebrow">Why San Antonio Homeowners Call Us</span>
      <h2>A Handyman You Can Actually Rely On</h2>
      <p>Most people don't call a handyman until something's already broken and it's already inconvenient. We keep the process simple: tell us what's wrong, get a clear estimate, get it fixed &mdash; without a week of phone tag or a stranger showing up with no idea what they're walking into.</p>
      <ul class="check-list">
        <li>Upfront estimates before any work starts &mdash; no surprise invoices</li>
        <li>Licensed and insured for your protection</li>
        <li>Same-day and next-day scheduling for urgent repairs</li>
        <li>One call for multiple repairs &mdash; no need to hire five different specialists</li>
        <li>Serving San Antonio proper plus the surrounding suburbs and metro</li>
      </ul>
    </div>
    <div class="card">
      <h3>Get a Fast, Free Estimate</h3>
      <p class="text-muted">Call, text, or fill out the quote form &mdash; most requests get a response the same business day.</p>
      <a class="btn btn-primary btn-block btn-lg" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a>
      <div style="height:10px;"></div>
      <a class="btn btn-navy btn-block btn-lg" href="/contact.html">Request Free Estimate</a>
    </div>
  </div>
</section>"""

    area = f"""<section class="section bg-gray">
  <div class="wrap">
    <span class="eyebrow">Service Area</span>
    <h2>Serving San Antonio &amp; the Surrounding Metro</h2>
    <p class="text-muted" style="max-width:680px;">From downtown San Antonio out to Stone Oak, Alamo Heights, Helotes, Schertz, and beyond &mdash; see the full list on our <a href="/service-area.html">service area page</a>.</p>
    {neighborhoods_chip_list()}
  </div>
</section>"""

    faqs = [
        ("How much does a handyman cost in San Antonio?", "Cost depends on the job &mdash; a simple fixture install is a lot less than a multi-hour repair. We give a clear, upfront estimate before starting any work so you know the cost with no surprises."),
        ("Do you offer same-day handyman service?", "Yes, same-day and next-day appointments are available depending on your location and the nature of the job. Call for real-time availability."),
        ("Are you licensed and insured?", "Yes. We carry insurance and hold the appropriate licensing for the work we perform."),
        ("What areas of San Antonio do you serve?", "The full San Antonio metro, including Stone Oak, Alamo Heights, Helotes, Schertz, Converse, and surrounding communities. See our full service area list for details."),
    ]
    faq_section = f"""<section class="section" id="faq">
  <div class="wrap" style="max-width:820px;">
    <h2 class="center">Frequently Asked Questions</h2>
    {faq_block(faqs)}
  </div>
</section>"""

    body = hero + stats + services_section + why + area + faq_section + cta_band()
    schema = ld(faq_schema(faqs), breadcrumb_schema([("Home", SITE_ROOT + "/")]))
    return page(
        f"Handyman San Antonio, TX | {BUSINESS_NAME} &mdash; Same-Day Estimates",
        "Licensed & insured handyman services in San Antonio, TX. Drywall, fencing, TV mounting, minor plumbing & electrical, and more. Free same-day estimates.",
        "index.html",
        body,
        schema,
    )


def build_services_index():
    body = f"""{breadcrumb_html([("Home", "/index.html"), ("Services", None)])}
<section class="section">
  <div class="wrap">
    <span class="eyebrow">Full Service List</span>
    <h1>Handyman Services in San Antonio, TX</h1>
    <p class="text-muted" style="max-width:680px;">Every service below is available across the San Antonio metro with free, no-obligation estimates. Click any service for full details, or call if you don't see exactly what you need &mdash; if it's a repair around the house, we probably handle it.</p>
    {services_grid()}
  </div>
</section>
{cta_band()}
"""
    schema = ld(breadcrumb_schema([("Home", SITE_ROOT + "/"), ("Services", SITE_ROOT + "/services.html")]))
    return page(
        "All Handyman Services | San Antonio, TX",
        "Browse every handyman service offered across San Antonio, TX — drywall, fencing, TV mounting, plumbing, electrical, painting, and more.",
        "services.html",
        body,
        schema,
    )


def build_service_page(svc):
    others = [s for s in SERVICES if s["slug"] != svc["slug"]]
    related = others[:3]
    related_html = "\n      ".join(
        f'<li><a href="/{r["slug"]}.html">{r["name"]}</a></li>' for r in related
    )
    included = "\n      ".join(f"<li>{item}</li>" for item in svc["included"])

    body = f"""{breadcrumb_html([("Home", "/index.html"), ("Services", "/services.html"), (svc["name"], None)])}
<section class="section">
  <div class="wrap two-col">
    <div>
      <span class="eyebrow">{svc['kw'].title()}</span>
      <h1>{svc['h1']}</h1>
      <p>{svc['intro']}</p>

      <h2>What's Included</h2>
      <ul class="check-list">
      {included}
      </ul>

      <h2>Why Hire a Pro</h2>
      <p>{svc['why']}</p>

      <h2>Frequently Asked Questions</h2>
      {faq_block(svc['faqs'])}

      <hr class="divider">
      <h3>Related Services</h3>
      <ul>
      {related_html}
      </ul>
    </div>
    {quote_form_card(heading=f"Get a Free {svc['name']} Estimate", sub="Tell us a bit about the job — we'll follow up same day during business hours.")}
  </div>
</section>
{cta_band(heading=f"Need {svc['name']} in San Antonio?", sub="Free estimates. Licensed &amp; insured. Most calls answered same day.")}
"""
    schema = ld(
        service_schema(svc),
        faq_schema(svc["faqs"]),
        breadcrumb_schema([
            ("Home", SITE_ROOT + "/"),
            ("Services", SITE_ROOT + "/services.html"),
            (svc["name"], f"{SITE_ROOT}/{svc['slug']}.html"),
        ]),
    )
    return page(svc["title"], svc["meta"], f"{svc['slug']}.html", body, schema)


def build_service_area():
    chips = neighborhoods_chip_list()
    body = f"""{breadcrumb_html([("Home", "/index.html"), ("Service Area", None)])}
<section class="section">
  <div class="wrap">
    <span class="eyebrow">Where We Work</span>
    <h1>Handyman Service Area: San Antonio, TX &amp; Surrounding Communities</h1>
    <p style="max-width:700px;">We cover the full San Antonio metro &mdash; from the urban core out through the northside suburbs and neighboring cities. If you're not sure whether your address is in range, just call; most of the metro is covered.</p>
    {chips}
  </div>
</section>
<section class="section bg-gray">
  <div class="wrap two-col">
    <div>
      <h2>Local Knowledge, Not a Call Center</h2>
      <p>San Antonio's older neighborhoods, newer northside developments, and everything from historic homes near Southtown to new builds out toward Helotes all come with their own quirks &mdash; clay-soil foundation settling, older electrical panels, HOA fencing rules. We work across all of it and know what to expect walking in.</p>
      <p>Don't see your neighborhood listed? We likely still cover it &mdash; give us a call and we'll confirm.</p>
    </div>
    {quote_form_card()}
  </div>
</section>
{cta_band()}
"""
    schema = ld(breadcrumb_schema([("Home", SITE_ROOT + "/"), ("Service Area", SITE_ROOT + "/service-area.html")]))
    return page(
        "Service Area | Handyman San Antonio, TX & Surrounding Suburbs",
        "See the full San Antonio, TX handyman service area — Stone Oak, Alamo Heights, Helotes, Schertz, Converse, and more.",
        "service-area.html",
        body,
        schema,
    )


def build_contact():
    body = f"""{breadcrumb_html([("Home", "/index.html"), ("Free Quote", None)])}
<section class="section">
  <div class="wrap two-col">
    <div>
      <span class="eyebrow">Get a Free Estimate</span>
      <h1>Request Your Free Handyman Estimate</h1>
      <p>Fill out the form, call, or text &mdash; whatever's easiest. Most requests get a response the same business day, and there's never any obligation to book.</p>
      <ul class="check-list">
        <li>Free, no-obligation estimates</li>
        <li>Same-day response during business hours</li>
        <li>Licensed &amp; insured</li>
        <li>Straightforward pricing before any work starts</li>
      </ul>
      <p><strong>Call:</strong> <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br>
      <strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a><br>
      <strong>Hours:</strong> Mon&ndash;Sat, 7:00 AM &ndash; 7:00 PM</p>
    </div>
    {quote_form_card()}
  </div>
</section>
"""
    schema = ld(breadcrumb_schema([("Home", SITE_ROOT + "/"), ("Contact", SITE_ROOT + "/contact.html")]))
    return page(
        "Free Handyman Estimate | San Antonio, TX",
        "Request a free, no-obligation handyman estimate in San Antonio, TX. Call, text, or send your project details — same-day response.",
        "contact.html",
        body,
        schema,
    )


def build_thank_you():
    body = f"""<section class="section" style="min-height:50vh;">
  <div class="wrap center" style="max-width:600px;">
    <h1>Thanks — We Got Your Request</h1>
    <p>A team member will follow up shortly, usually within the same business day. If it's urgent, don't wait on us &mdash; call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> directly.</p>
    <a class="btn btn-primary btn-lg" href="/index.html">Back to Home</a>
  </div>
</section>
"""
    return page(
        "Request Received | " + BUSINESS_NAME,
        "Your free handyman estimate request has been received.",
        "thank-you.html",
        body,
    )


def build_legal(title, path, heading, body_text):
    body = f"""{breadcrumb_html([("Home", "/index.html"), (heading, None)])}
<section class="section">
  <div class="wrap" style="max-width:760px;">
    <h1>{heading}</h1>
    {body_text}
  </div>
</section>
"""
    return page(title, f"{heading} for {BUSINESS_NAME}.", path, body)


def build_privacy():
    text = f"""<p><em>Last updated: {YEAR}</em></p>
<p>{BUSINESS_NAME} ("we," "us") respects your privacy. This page explains what information we collect through this website and how it's used.</p>
<h2>Information We Collect</h2>
<p>When you submit a quote request or contact form, we collect the information you provide: name, phone number, email address, property ZIP code, and any project details you share.</p>
<h2>How We Use It</h2>
<p>We use this information solely to respond to your service request, provide an estimate, and, if you choose to proceed, schedule and complete the requested work. We do not sell your personal information to third parties.</p>
<h2>Analytics</h2>
<p>This site uses analytics tools (including Google Analytics and Ahrefs Web Analytics) to understand site traffic and improve our content. These tools may use cookies or similar technologies.</p>
<h2>Contact Us</h2>
<p>Questions about this policy can be directed to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p><strong>Note:</strong> This is a template privacy policy. Have it reviewed by an attorney before relying on it, especially if you collect payment information or serve customers outside Texas.</p>
"""
    return build_legal("Privacy Policy | " + BUSINESS_NAME, "privacy-policy.html", "Privacy Policy", text)


def build_terms():
    text = f"""<p><em>Last updated: {YEAR}</em></p>
<p>These terms govern your use of this website. By using this site or submitting a request through it, you agree to these terms.</p>
<h2>Estimates</h2>
<p>Estimates provided through this site or by phone are free and non-binding until confirmed in writing or in person at the time of service.</p>
<h2>Service Availability</h2>
<p>Same-day and next-day availability is offered on a best-effort basis and is not guaranteed for every request.</p>
<h2>Website Use</h2>
<p>Content on this site is for general informational purposes and does not constitute a guarantee of pricing, availability, or outcome for any specific project.</p>
<h2>Contact</h2>
<p>Questions about these terms can be directed to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p><strong>Note:</strong> This is a template terms page. Have it reviewed by an attorney before relying on it.</p>
"""
    return build_legal("Terms of Service | " + BUSINESS_NAME, "terms.html", "Terms of Service", text)


def build_404():
    body = f"""<section class="section center" style="min-height:50vh;">
  <div class="wrap">
    <h1>Page Not Found</h1>
    <p>The page you're looking for moved or doesn't exist. Try the homepage, or call us directly at <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.</p>
    <a class="btn btn-primary btn-lg" href="/index.html">Back to Home</a>
  </div>
</section>
"""
    return page("Page Not Found | " + BUSINESS_NAME, "Page not found.", "404.html", body)


# ============================================================
# Sitemap + robots
# ============================================================
def build_sitemap():
    urls = ["index.html", "services.html", "service-area.html", "contact.html"] + [
        f"{s['slug']}.html" for s in SERVICES
    ]
    items = "\n  ".join(
        f"<url><loc>{SITE_ROOT}/{u}</loc></url>" for u in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  {items}
</urlset>
"""


def build_robots():
    return f"""User-agent: *
Allow: /

Sitemap: {SITE_ROOT}/sitemap.xml
"""


# ============================================================
# Main
# ============================================================
def main():
    out = {}
    out["index.html"] = build_home()
    out["services.html"] = build_services_index()
    out["service-area.html"] = build_service_area()
    out["contact.html"] = build_contact()
    out["thank-you.html"] = build_thank_you()
    out["privacy-policy.html"] = build_privacy()
    out["terms.html"] = build_terms()
    out["404.html"] = build_404()
    for svc in SERVICES:
        out[f"{svc['slug']}.html"] = build_service_page(svc)

    for fname, content in out.items():
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(build_sitemap())
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(build_robots())

    print(f"Generated {len(out)} HTML pages + sitemap.xml + robots.txt")


if __name__ == "__main__":
    main()


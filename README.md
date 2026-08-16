# San Antonio Handyman Lead-Gen Site

A standalone, unbranded (from Creative Factorial) static website built to rank for **bottom-of-funnel handyman search terms in San Antonio, TX** and capture leads you can forward to a partner business. No build tools, no framework — plain HTML/CSS/JS, so it's cheap to host and fast to load (which Google rewards).

## What's in here

- `index.html` — homepage targeting the money keyword: "handyman San Antonio TX"
- 11 service pages, each targeting a specific bottom-funnel search (e.g. `drywall-repair-san-antonio.html`, `emergency-handyman-san-antonio.html`, `tv-mounting-san-antonio.html`) — these convert better than the homepage because the searcher already knows exactly what they need
- `services.html` — hub page linking to all services (internal linking helps every page rank)
- `service-area.html` — lists San Antonio-metro neighborhoods/suburbs for local relevance
- `contact.html` — lead capture form
- `thank-you.html` — form confirmation page (also your Google Ads/GA4 conversion goal page)
- `privacy-policy.html`, `terms.html` — generic templates; **have an attorney review before relying on them**
- `404.html`
- `sitemap.xml`, `robots.txt`
- `css/style.css`, `js/script.js`
- `generate.py` — the Python script that built every page. Keep it — see "Reusing this for the next city/niche" below.

## Before you launch — required edits

Open `generate.py` and edit the `CONFIG` block at the top (search for `PLACEHOLDER`):

| Variable | What to change |
|---|---|
| `PHONE_DISPLAY` / `PHONE_TEL` | The number leads should call — this is what gets forwarded to your partner business |
| `EMAIL` | The inbox leads should land in |
| `DOMAIN` | Your real domain once you buy one |
| `GA4_ID` | Your Google Analytics 4 measurement ID |
| `AHREFS_KEY` | Your Ahrefs Web Analytics key (Ahrefs dashboard → Web Analytics → Add website) |
| `AHREFS_SITE_VERIFICATION` | The token Ahrefs gives you to verify site ownership |

Then re-run `python3 generate.py` — it rewrites every HTML file with your values baked in everywhere (header, footer, schema markup, forms, meta tags).

**Why edit the script instead of the HTML directly:** the phone number, email, and analytics IDs appear on all 19 pages. Editing 4 lines in `generate.py` and re-running it is much safer than hand-editing 19 files and missing one.

## Deploying it

Easiest path — **Netlify** (free tier is plenty for this):
1. Drag the whole `handyman-site` folder onto [app.netlify.com/drop](https://app.netlify.com/drop), or connect it via GitHub.
2. Netlify auto-detects the `data-netlify="true"` attribute already on the contact/quote forms — submissions show up in Netlify's dashboard and can be forwarded to email with zero extra setup (Site settings → Forms → Form notifications).
3. Point your new domain at Netlify (Domain settings), separate from Creative Factorial's domain as requested.

Alternatives: Vercel, GitHub Pages, or any $5/mo static host — just note that Netlify Forms is what currently powers the lead form with **no backend code required**. If you host elsewhere, swap the form's `action`/`data-netlify` setup for something like [Formspree](https://formspree.io) (also free tier, also zero backend).

## Ahrefs setup

1. **Site Verification**: Ahrefs Webmaster Tools → Add site → choose "Meta tag" verification → copy the token into `AHREFS_SITE_VERIFICATION` in `generate.py` → regenerate → deploy → click verify in Ahrefs. This gets you free Site Audit + backlink data for the domain.
2. **Web Analytics** (optional, separate from Webmaster Tools): Ahrefs → Web Analytics → Add website → copy the `data-key` value into `AHREFS_KEY` → regenerate → deploy. This is a lighter-weight, privacy-friendlier alternative/companion to GA4 for traffic data.
3. Also set up **Google Search Console** and a **Google Business Profile** for San Antonio (not included here since neither requires code) — those two matter as much as the site itself for local rankings.

## Why it's unbranded

There's no "Creative Factorial" anywhere in the code, footer, meta tags, or schema markup — the business identity is a generic, keyword-relevant placeholder name ("San Antonio Handyman Experts") so leads can be forwarded to whichever partner business you land without any connection back to your agency. Swap `BUSINESS_NAME` in `generate.py` any time — e.g. once you sign a partner, you may want to rename it to match their actual business for trust/consistency, or keep it generic. Either works; regenerate after changing it.

## SEO decisions baked in

- **Bottom-of-funnel focus**: every service page targets a "ready to hire" search (e.g. "drywall repair San Antonio"), not informational/DIY searches ("how to patch drywall") — those visitors aren't ready to pay.
- **LocalBusiness, Service, FAQPage, and BreadcrumbList schema** (JSON-LD) on every relevant page — helps Google understand the business and can earn FAQ rich results in search.
- **Unique content per page** — no duplicated boilerplate paragraphs between service pages; thin/duplicate content is a real ranking penalty.
- **Internal linking** — every service page links to 3 related services + the hub page; the hub and homepage link to every service. This spreads ranking authority across the site.
- **Mobile-first, no page-bloat** — no JS frameworks, no web fonts, no external images. Page speed is a ranking factor and most local "near me" searches are on mobile.
- **Sticky mobile call bar** — the #1 conversion lever for local service sites is making "call now" impossible to miss on a phone screen.
- **Netlify-native lead form** with a honeypot field for basic spam protection.

## Next steps to actually rank (not code — you or Taylor)

1. Buy the domain, deploy, verify in Google Search Console + Ahrefs Webmaster Tools, submit `sitemap.xml`.
2. Set up a Google Business Profile for the San Antonio service area — this matters as much as the website for local map-pack rankings.
3. Get a handful of local citations (Yelp, Angi, Nextdoor, BBB) with matching name/phone/address (NAP consistency).
4. Once it's ranking and generating leads, this is the point in your playbook where you forward free leads to a real handyman business, then convert them to a paying client.

## Reusing this for the next city/niche

This is built as a generator, not a one-off. To spin up "fence repair Charleston SC" or "handyman Austin TX" next:
1. Copy this whole folder.
2. Edit `CONFIG` (business name, city, phone, domain) and the `SERVICES` list (swap service copy, or keep it and just change the city references) in `generate.py`.
3. Run `python3 generate.py`.
4. New site, same SEO structure, in minutes instead of hours.

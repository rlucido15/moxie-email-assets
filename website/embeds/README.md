# Moxie core pages: Lofty install guide

Five paste-in blocks: one per page plus a shared footer. Each is self-contained (HTML + CSS + schema + a small script). Images load from your `moxie-email-assets` repo through jsDelivr, so nothing needs uploading to Lofty. A copy of every block also lives in the repo under `website/embeds/`.

| File | Page | Size |
|---|---|---|
| `moxie-buy-embed.html` | /buy | ~37 KB |
| `moxie-refinance-embed.html` | /refinance | ~29 KB |
| `moxie-products-embed.html` | /products | ~38 KB |
| `moxie-faqs-embed.html` | /faqs | ~101 KB (all 100 Q&As + FAQ schema) |
| `moxie-footer-embed.html` | bottom of every page | ~4 KB |

## Before you start
1. In Lofty, **save a website version** first (your restore point).
2. Work on one page at a time and preview before publishing.

## Install, page by page

### /buy
1. Remove or hide the old Buy page blocks (hero, guarantees, "How soon", reviews, calculators, CTA, disclaimer).
2. Directly under the Lofty header, add a **Custom Code / Embed** block and paste all of `moxie-buy-embed.html`.
3. Add a second Embed block at the bottom and paste `moxie-footer-embed.html`.

### /refinance
1. **Keep your existing "How much could you be saving" widget block.** Don't delete it. The new page moves it into the hero automatically and hides its old spot. I tested this on your live page, and the widget still works after the move.
2. Remove the other old blocks (cash out / lower payment / shorten term, HELOC, "Questions about refinancing?").
3. Add an Embed block directly under the header, *above* the widget block, and paste `moxie-refinance-embed.html`.
4. Add the footer embed at the bottom.
   - If the widget block is ever missing, the hero shows a matching "Show me my numbers" card that links to the application instead.

### /products
1. Remove the old product list and "Questions? Ask us" blocks.
2. Paste `moxie-products-embed.html` under the header, then the footer embed.
   - Every product has a link anchor, e.g. `/products#fha`, `#va`, `#dscr`, `#heloc`, `#bridge-loan`.

### /faqs
1. Remove the old FAQ widget block. It's a third-party widget that search engines can't read, and the new block replaces it with the same 100 Q&As in plain HTML.
2. Paste `moxie-faqs-embed.html` under the header.
3. **Optional:** keep your Lofty "Still have questions? Submit question" form block below it, so questions still flow into Lofty.
4. Footer embed at the bottom.
   - Search also works from a link: `/faqs?q=dscr`.

## SEO fields (Lofty › page settings › SEO)
| Page | Title tag | Meta description |
|---|---|---|
| /buy | Get Preapproved to Buy a Home \| Same-Day Approval \| Moxie | Buy with Moxie's Ultimate Buyer Advantage: same-day preapproval, lock your rate up to 360 days, and clear to close in 21 days or less. Apply in 10 minutes. |
| /refinance | Mortgage Refinance: Lower Your Payment or Cash Out \| Moxie | See your new payment in 60 seconds, with no credit check. Refinance at wholesale pricing to lower your rate, shorten your term, or take cash out. |
| /products | Home Loan Options: FHA, VA, Jumbo, DSCR & Non-QM \| Moxie | Compare 18 home loan options, from 3% down conventional and 0% down VA and USDA to bank statement, DSCR, HELOC and bridge loans. |
| /faqs | Mortgage FAQs: Preapproval, Rates, Credit & Refinance \| Moxie | Search 100 answers about preapproval, down payments, credit scores, closing costs, Non-QM and DSCR loans, appraisals and refinancing. |

Structured data is already inside each block. Check each page after publishing with Google's Rich Results Test (search.google.com/test/rich-results) and the Schema validator (validator.schema.org).

## Dynamic hero (Buy and Refinance)
These pages follow the same rules and storage as your homepage hero, so visitors see consistent copy from page to page.
- **Returning visitor:** "Welcome back / Ready to pick up where you left off?" with the "Continue my approval" button.
- **Hawaii visitor:** detected by device timezone first, then IP lookup (geojs, with ipapi.co as backup). They get the Hawaii copy, the Hawaiian homebuyers photo, and "Call 808.818.5618" buttons.
- **Everyone else:** the default copy, which is also what Google indexes.

**Test links** (add to the page URL):
`?hero=hawaii` · `?hero=returning` · `?hero=default` · `?geo=HI` · `?hero=reset` (clears your visit count)

**Analytics:** if GA4 or GTM is on the site, these events are sent: `hero_view`, `hero_cta_click`, `products_filter`, `faq_search`, `faq_open`. Every apply button adds `?src=` (for example `buy_hero_hi`) so you can see which button drove each application.

## Google reviews
- The Buy page ships with three real reviews.
- **To switch to a live feed:** once a daily Business Profile sync is set up, publish a JSON file and add this line in an Embed block placed *above* the Buy block:
  `<script>window.MX_REVIEWS_URL = 'https://…/reviews.json';</script>`
- **JSON format:** `{ "rating": 4.9, "count": 123, "url": "https://g.page/r/…", "reviews": [{ "author": "Name", "rating": 5, "text": "…" }] }`
- **What changes:** the rating and count appear automatically, and the three newest 4–5 star reviews replace the static ones.
- **Google logo:** the block loads `google_logo.png` from the root of the repo. Until that file is pushed, it shows the word "Google" instead.

## Speed notes
- No extra font downloads; it uses the Barlow your site already loads.
- The hero photo is served at 800px or 1400px wide (WebP) depending on screen size, and other images lazy-load.
- Each block's script is about 3–4 KB, with no libraries.
- Motion is subtle and switches off for visitors who've turned on reduced motion.

## Confirm before launch
- **Compliance review** of the guarantees, "save $1,000s", "tax-free" cash-out, and down-payment percentages. Reg Z can require extra disclosures when ads mention down payments.
- **Closing speed:** it's still quoted as 21 days (guarantee), under 12 days and 10 days (FAQs). Pick one claim.
- **HELOC figures:** confirm 5 minutes, 5 days and $400K are still current.
- **Phone format:** the general line is (480) 660-2518 and Hawaii is 808.818.5618. Say if you want both in the same format.

## Homepage (/) — moxie-home-embed.html
1. In Lofty, edit the homepage. Remove the old dynamic-hero code block and every old content block between the header and the footer.
2. Add ONE Custom Code block and paste moxie-home-embed.html. Add the footer embed in a second block below it.
3. SEO title: "Moxie Mortgage | Wholesale Mortgage Broker, 51 States"
   Meta description: "Moxie Mortgage is a wholesale mortgage broker serving 51 states and territories. Skip the retail markup on home purchase, refinance, and HELOC loans."
4. Hero logic (same storage keys as the other pages): ?hero= override > UTM intent (refi / heloc|equity, kept for the session) > returning visitor > sticky A/B arm (mx_ab). Hawaii visitors get the Hawaii photo and a Call 808.818.5618 button on every version, plus Hawaii copy on the purchase and returning versions.
   Test URLs: ?hero=refi | heloc | returning | hawaii | default | reset, ?ab=A | B, ?geo=HI
5. GA4 / dataLayer events: hero_view (hero_variant, hero_ab, hero_geo, hero_label), hero_cta_click, hero_call_click, savings_calc_use, savings_cta_click, reviews_view. Apply links carry ?src=hero_<label> plus any utm_ parameters.

## About (/about) — moxie-about-embed.html
1. Edit the About page in Lofty. Delete every block between the header and the footer (definition banner, map banner, "Our mission" text, both testimonial blocks).
2. Add ONE Custom Code block, paste moxie-about-embed.html, and add the footer embed below it.
3. Keep the SEO title "About Moxie Mortgage | Wholesale Lending by NEXA" and the current meta description.
4. Founder headshot: once the photo is in the repo, set HEADSHOT in about.py and rebuild (initials show until then).
5. Hawaii visitors see "Call 808.818.5618" instead of "Talk to a loan expert", and Hawaii-tagged reviews.

## Calculators hub (/calculators) — moxie-calculators-embed.html
Replace the page's three blocks (heading text, 3-column cards, closing text) with this one embed + the footer embed.

## Calculator pages — moxie-calc-mortgage-embed.html (/mortgage-calculator), moxie-calc-affordability-embed.html (/affordabilitycalculator), moxie-calc-rentvsbuy-embed.html (/rentvsbuy)
1. On each page, delete the title banner, the old Custom Code block holding the iframe, the definitions text block, and the legal-disclosure text block.
2. Add ONE Custom Code block with the matching embed, then the footer embed.
3. The calculators still run from github.io (rlucido15/mortgage-calculator, affordability-calculator, rent-vs-buy-calculator), so lead capture, email and PDF reports are unchanged. The embed sizes the calculator to its content automatically.
4. Optional SEO title tweaks: keep the current titles; they already match the new H1s.

## Client success (/client-success) — moxie-client-success-embed.html
1. In Lofty, create a new page with URL /client-success. SEO title: "Client Success Stories | Moxie Mortgage". Meta description: "Real-world homeownership case studies from Moxie Mortgage clients: first-time buyers, VA loans, self-employed borrowers, refinances, investors, Hawaii buyers, and tough files."
2. Add ONE Custom Code block with this embed, then the footer embed.
3. Point the nav/footer "Client Success" links (and the "READ CLIENT STORIES" button on /blog) to /client-success.
4. Keep publishing stories in the Lofty blog under the Client Success category. New ones appear on the page automatically ("New story"); fold them in with the "Client Stories Update" routine so they get a summary, tags, and crawlable HTML.

## /loanofficer (new page)
File: `moxie-loan-officer-embed.html` (~111 KB)

1. In Lofty, create a page at **/loanofficer**. Add a Custom Code / Embed block directly under the header and paste the whole file. Add the footer embed at the bottom.
2. No Lofty form block is needed. The page's own application form (inline card plus a popup that every "Apply" button opens) posts to the existing "Lofty API" intake Apps Script. Leads are tagged **CTA: LO Application** plus one tag per licensed state (e.g. `AZ`). NMLS #, years, units, volume, states, company and consent text go in the pinned note.
3. Add /loanofficer to the site nav or footer so it gets crawled, and submit it in Google Search Console.

SEO (page settings › SEO):
- Title: `Loan Officer Careers | Join Moxie Mortgage`
- Meta description: `Join Moxie Mortgage as a loan officer: 300+ wholesale investors, thousands of loan programs, referrals from agent partners, everyday payday, benefits, and hands-on support.`

## /area-director (live at /areadirector)
File: `moxie-area-director-embed.html` (~74 KB)

1. In Lofty, on the /areadirector page, add a Custom Code / Embed block directly under the header and paste the whole file.
2. No Lofty form block is needed. The page has its own application form (an inline card plus a popup that every "Apply" button opens). It posts to the existing "Lofty API" intake Apps Script (the same deployment the rent-vs-buy calculator uses), which creates or updates the Lofty lead tagged **CTA: AD Application**. Units, volume, states, message and consent text go into the lead's pinned note.
3. Add the footer embed at the bottom.
4. Point /bdm to /areadirector so old links keep working.
   - The Lofty API key stays in the Apps Script. The page only carries that script's spam-gate secret, same as the calculators.
   - To change the endpoint, rebuild with `AD_ENDPOINT=... python3 build/ad.py`.

SEO (page settings › SEO):
- Title: `Area Director | Earn Mortgage Income in Your Area | Moxie Mortgage`
- Meta description: `Join Moxie Mortgage as an Area Director: a W-2 business development role paid 0.25% of the loan amount on closed Moxie loans in your area. No mortgage license or loan work required.`

## Spanish (EN / ES toggle)
Every page embed, the header, the footer and the three calculators switch to Spanish when a visitor clicks **ES** in the header.

- **Install:** paste the latest version of each embed (header first on every page, then the page embed, then the footer). No other setup. Pages that still carry an older embed upgrade themselves when a newer one is on the page.
- **How it works:** the header's toggle sets `?lang=es` and remembers the choice; every internal link carries it. Each page fetches its Spanish dictionary from this repo (`website/es/<page>.json`) only when Spanish is on, so English visitors download nothing extra. Text is swapped in place, so forms, sliders, filters, the FAQ search and lead posting work unchanged.
- **Calculators:** the calculator pages pass the language to the calculator apps (GitHub Pages) and keep them in sync when the toggle changes.
- **Stays English:** customer reviews (left in the reviewer's own words), Lofty blog posts and city pages, apply.moxiemortgage.com, the PDF reports and the emails Moxie receives.
- **Editing Spanish:** strings live in `build/es/*.py`. Run `build/publish_es.sh` (rebuilds dictionaries, publishes them, rebuilds embeds) and `build/app_i18n.py` for the calculators, then commit the three calculator repos.
- **New client stories:** add the new story's title and summary to `build/es/mx-stories.py` when running Client Stories Update, or they show in English on the Spanish page.

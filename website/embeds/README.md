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

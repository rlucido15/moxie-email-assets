import re
from common import *

A = APPLY
GROUPS = [
 ("Conventional and jumbo loans", "The most widely used mortgages, with fixed or adjustable rates.", [
  ("Conventional 30 Year Fixed", "As low as 3% down", "buy low", "Most buyers and refinancers", "The most popular loan for buying or refinancing a home, offering a fixed rate for 30 years, down payments as low as 3%, and options with no mortgage insurance.", "MortgageLoan"),
  ("Conventional 15 Year Fixed", "As low as 5% down", "buy", "Paying less interest overall", "A shorter term means higher monthly payments, but lower interest paid overall. Buy with as little as 5% down or choose options with no mortgage insurance.", "MortgageLoan"),
  ("Conventional Adjustable Rate (ARM)", "5, 7 or 10-year fixed start", "buy", "Buyers planning to move or refinance", "Start with a fixed rate for 5, 7, or 10 years, which adjusts every 6 months thereafter. This could offer a lower interest rate and savings compared with a fixed-rate option.", "MortgageLoan"),
  ("Jumbo", "Above $832,750", "buy", "Higher-priced homes", "Buy or refinance beyond conventional loan limits ($832,750 for a single-family home in most areas in 2026) with many options not requiring mortgage insurance.", "MortgageLoan")]),
 ("Government-backed loans", "Low or no down payment programs backed by FHA, VA and USDA.", [
  ("FHA", "3.5% down", "buy low", "First-time buyers and lower credit", "Buy or refinance with as little as 3.5% down. FHA offers lower credit requirements and allows for higher debt limits than other products.", "MortgageLoan"),
  ("VA", "0% down", "buy low", "Veterans and service members", "Those with military service benefits can buy or streamline refinance with as little as 0% down and often with a lower interest rate than other options.", "MortgageLoan"),
  ("USDA", "0% down", "buy low", "Rural and suburban buyers", "Eligible individuals can buy or refinance in a USDA-designated rural area with as little as 0% down and often a lower interest rate than other options.", "MortgageLoan"),
  ("Down Payment Assistance", "Grants and forgivable loans", "buy low", "Buyers short on cash to close", "Designed to make homeownership more affordable by reducing or eliminating the need for a down payment.", "LoanOrCredit")]),
 ("Self-employed and alternative income loans", "Non-QM options that qualify you without W-2s or tax returns.", [
  ("Bank Statement Loan", "12–24 months of deposits", "self", "Self-employed with tax write-offs", "Qualify using 12–24 months of bank deposit statements instead of W-2s or tax returns. Ideal for self-employed individuals who claimed tax write-offs in prior years.", "MortgageLoan"),
  ("P&amp;L Loan", "No tax returns", "self", "Business owners with variable income", "Qualify using profit and loss statements rather than tax returns or W-2s, offering self-employed borrowers flexibility for fluctuating income and potentially higher loan amounts.", "MortgageLoan"),
  ("Asset Utilization", "Assets as income", "self", "Retirees and high-net-worth buyers", "Qualify using liquid assets (like savings or investments) as income, rather than traditional employment or W-2 income. Ideal for retirees and high-net-worth individuals.", "MortgageLoan"),
  ("No Ratio Loan", "No income documentation", "self", "Strong credit and assets", "Qualify for a mortgage without income or employment documentation, relying instead on factors like your credit score, assets, and down payment.", "MortgageLoan")]),
 ("Investor and specialty loans", "Financing for rentals, fixer-uppers, land, and buying before you sell.", [
  ("Debt Service Coverage Ratio (DSCR)", "No tax returns or W-2s", "inv", "Real estate investors", "Invest in real estate based on the property's cash flow rather than your personal income, meaning no tax returns or W-2s are required.", "MortgageLoan"),
  ("Purchase + Renovation Loan", "One loan, one closing", "buy inv", "Fixer-uppers", "Finance both the purchase and renovation of a property with a single mortgage. Ideal for buying fixer-uppers.", "MortgageLoan"),
  ("Land Loan", "Up to 100% construction financing", "buy inv", "Building your own home", "Buy raw land with the option to also include up to 100% financing for the construction of a home.", "LoanOrCredit"),
  ("Bridge Loan", "Make non-contingent offers", "buy equity", "Buying before you sell", "Buy before you sell your current home with a short-term loan that enables you to make a non-contingent offer.", "LoanOrCredit")]),
 ("Home equity loans", "Tap your equity without refinancing your first mortgage.", [
  ("Home Equity Line of Credit (HELOC)", "Pay interest only on what you use", "equity", "Flexible, ongoing access to cash", "Use your home equity to get access to cash, pay interest only on the amount used, typically at interest rates lower than credit cards or personal loans.", "LoanOrCredit"),
  ("Home Equity Loan (HELOAN)", "Fixed rate, lump sum", "equity", "Renovations or debt consolidation", "Use your equity to get a lump-sum amount with a fixed interest rate and predictable monthly payments, ideal for financing renovations or debt consolidation.", "LoanOrCredit")]),
]
ID = {"Conventional 30 Year Fixed": "conventional-30", "Conventional 15 Year Fixed": "conventional-15", "Conventional Adjustable Rate (ARM)": "arm",
      "Jumbo": "jumbo", "FHA": "fha", "VA": "va", "USDA": "usda", "Down Payment Assistance": "down-payment-assistance",
      "Bank Statement Loan": "bank-statement-loan", "P&amp;L Loan": "pl-loan", "Asset Utilization": "asset-utilization", "No Ratio Loan": "no-ratio-loan",
      "Debt Service Coverage Ratio (DSCR)": "dscr", "Purchase + Renovation Loan": "renovation-loan", "Land Loan": "land-loan", "Bridge Loan": "bridge-loan",
      "Home Equity Line of Credit (HELOC)": "heloc", "Home Equity Loan (HELOAN)": "heloan"}

EXTRA_CSS = r"""
.mx-help{flex:0 1 300px;background:var(--navy);color:#fff;border-radius:20px;padding:26px}
.mx-help p{color:#C9D6DF;font-size:15px;margin:4px 0 18px !important}
.mx-tbl-box{overflow-x:auto;border:1px solid var(--line);border-radius:18px;-webkit-overflow-scrolling:touch}
.mxp table{width:100%;border-collapse:collapse;min-width:760px;font-size:16px;margin:0}
.mxp th,.mxp td{padding:14px 16px;text-align:left;border:0;border-bottom:1px solid var(--line);vertical-align:top;background:none;color:var(--navy)}
.mxp thead th{font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:13px;color:var(--muted);background:var(--soft)}
.mxp tbody tr:last-child th,.mxp tbody tr:last-child td{border-bottom:0}
.mx-chips{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:40px}
.mxp .mx-chip{min-height:44px;padding:9px 18px;border-radius:999px;font-family:inherit;font-weight:600;font-size:15px;line-height:1.2;cursor:pointer;background:#fff;color:var(--navy);border:1px solid #B9C8D2}
.mxp .mx-chip:hover{border-color:var(--navy)}
.mxp .mx-chip[aria-pressed="true"]{background:var(--navy);color:#fff;border-color:var(--navy)}
.mx-group{margin-bottom:52px}
.mx-group-h{display:flex;flex-wrap:wrap;gap:8px 24px;align-items:baseline;justify-content:space-between;margin-bottom:18px;border-bottom:2px solid var(--navy);padding-bottom:12px}
.mx-group-h h2{font-size:28px;line-height:1.15;font-weight:800}
.mx-group-h p{color:var(--muted);font-size:16px;max-width:520px}
.mx-prods{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}
@media (max-width:1100px){.mx-prods{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.mx-prods{grid-template-columns:minmax(0,1fr)}}
.mx-prods .mx-card{padding:24px}.mx-prods .mx-card h3{font-size:20px}
.mx-prod{scroll-margin-top:120px}
.mx-fact{align-self:flex-start;background:#E3F5F9;color:#0F5F6E;font-weight:700;font-size:13px;padding:4px 10px;border-radius:999px}
.mx-prod .mx-ideal{font-size:14px;color:var(--navy)}
.mx-links{margin-top:auto !important;padding-top:8px;display:flex;gap:18px;flex-wrap:wrap}
.mx-links a{font-weight:700}
.mx-links a+a{color:var(--muted);font-weight:600}

"""

def card(name, fact, tags, ideal, desc):
    pid = ID[name]
    return (f'<article class="mx-card mx-prod" id="{pid}" data-tags="{tags}"><span class="mx-fact">{fact}</span><h3>{name}</h3>'
            f'<p>{desc}</p><p class="mx-ideal"><strong>Ideal for:</strong> {ideal}</p>'
            f'<div class="mx-links"><a href="{A}?src=products_{pid}">Get started →</a><a href="/contact">Ask a loan expert</a></div></article>')

groups_html = ''.join(
    f'<div class="mx-group"><div class="mx-group-h"><h2>{g}</h2><p>{intro}</p></div><div class="mx-prods">'
    + ''.join(card(*p[:5]) for p in prods) + '</div></div>' for g, intro, prods in GROUPS)

CHIPS = [("all", "All loans"), ("buy", "Buying a home"), ("low", "Low or no down payment"), ("self", "Self-employed"), ("inv", "Investors"), ("equity", "Home equity")]
chips_html = ''.join(f'<button type="button" class="mx-chip" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>' for k, l in CHIPS)

body = f"""
<style>{EXTRA_CSS.strip()}</style>
<section class="mx-hero" aria-labelledby="mxp-h1" style="padding-bottom:56px">
  <div class="mx-wrap" style="align-items:flex-end;justify-content:space-between">
    <div class="mx-hero-copy" style="flex:1 1 560px">
      <p class="mx-eyebrow mx-rise">18 home loan options · 1,000s of products</p>
      <h1 id="mxp-h1" class="mx-h1 mx-rise">Home loan options to fit your future</h1>
      <p class="mx-lede mx-rise mx-d2" style="max-width:640px">From first-time homebuyer programs to self-employed bank statement loans, we provide the expert guidance and diverse loan options you need to secure your home with confidence.</p>
    </div>
    <div class="mx-help mx-fade">
      <p style="color:#fff;font-weight:700;font-size:19px;margin:0 !important">Not sure which loan fits?</p>
      <p>Answer a few questions and a loan expert will match you in one call.</p>
      <a class="mx-btn mx-btn-p" href="{A}?src=products_match">Match me to a loan</a>
    </div>
  </div>
</section>

<section aria-labelledby="mxp-glance" style="padding:0 0 72px">
  <div class="mx-wrap">
    <h2 id="mxp-glance" class="mx-h2" style="font-size:clamp(28px,3vw,36px)">Popular home loans at a glance</h2>
    <p class="mx-muted" style="margin:8px 0 22px">Typical minimums. Your Moxie loan officer will confirm what you qualify for.</p>
    <div class="mx-tbl-box" role="region" aria-labelledby="mxp-glance" tabindex="0">
      <table>
        <caption style="position:absolute;left:-9999px">Comparison of popular Moxie Mortgage home loan types</caption>
        <thead><tr><th scope="col">Loan type</th><th scope="col">Best for</th><th scope="col">Down payment</th><th scope="col">Credit score</th></tr></thead>
        <tbody>
          <tr><th scope="row"><a href="#conventional-30">Conventional</a></th><td>Buyers with steady credit and income</td><td>As low as 3%</td><td>620+</td></tr>
          <tr><th scope="row"><a href="#fha">FHA</a></th><td>First-time buyers, lower credit or savings</td><td>3.5%</td><td>580+ (as low as 500 with Moxie)</td></tr>
          <tr><th scope="row"><a href="#va">VA</a></th><td>Eligible veterans and service members</td><td>0%</td><td>Set by lender</td></tr>
          <tr><th scope="row"><a href="#usda">USDA</a></th><td>Buyers in USDA-designated rural areas</td><td>0%</td><td>640+</td></tr>
          <tr><th scope="row"><a href="#jumbo">Jumbo</a></th><td>Loans above $832,750 (2026 limit, most areas)</td><td>Often 10%–20%</td><td>Varies by program</td></tr>
          <tr><th scope="row"><a href="#bank-statement-loan">Non-QM</a></th><td>Self-employed and investors</td><td>10%–25%</td><td>620+</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="mx-sec mx-soft" aria-labelledby="mxp-all" style="padding-top:72px">
  <div class="mx-wrap">
    <h2 id="mxp-all" class="mx-h2" style="margin-bottom:18px">Explore every loan option</h2>
    <div class="mx-chips" role="group" aria-label="Filter loans by goal">{chips_html}</div>
    <p class="mx-muted" aria-live="polite" id="mxp-count" style="position:absolute;left:-9999px"></p>
    {groups_html}
    <p style="font-size:22px;font-weight:700;text-align:center">No matter your current situation or future goals, Moxie has you covered.</p>
  </div>
</section>

<section class="mx-sec" aria-labelledby="mxp-help">
  <div class="mx-wrap">
    <h2 id="mxp-help" class="mx-h2" style="margin-bottom:28px">Questions? Ask us.</h2>
    <div class="mx-grid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
      <a class="mx-card" href="/faqs" style="color:var(--navy)"><h3 style="font-size:24px">Search 100 mortgage FAQs</h3><p>Get instant answers on loan types, down payments, credit, rates, and refinancing.</p><span class="mx-more">Browse FAQs →</span></a>
      <div class="mx-card" style="background:var(--navy);border-color:var(--navy);color:#fff"><h3 style="font-size:24px">Talk to a loan expert</h3><p style="color:#C9D6DF">Our team is standing by to help you choose the best product for your goals.</p>
        <a class="mx-btn mx-btn-w" data-mx-phone href="tel:{PHONE_TEL}" style="align-self:flex-start;margin-top:6px">Call {PHONE}</a></div>
    </div>
  </div>
</section>
"""

script = f"""
var chips = [].slice.call(root.querySelectorAll('.mx-chip'));
var cards = [].slice.call(root.querySelectorAll('.mx-prod'));
var groups = [].slice.call(root.querySelectorAll('.mx-group'));
chips.forEach(function (c) {{
  c.addEventListener('click', function () {{
    var f = c.getAttribute('data-f'), n = 0;
    chips.forEach(function (x) {{ x.setAttribute('aria-pressed', x === c); }});
    cards.forEach(function (k) {{ var on = f === 'all' || (' ' + k.getAttribute('data-tags') + ' ').indexOf(' ' + f + ' ') > -1; k.hidden = !on; if (on) n++; }});
    groups.forEach(function (g) {{ g.hidden = !g.querySelector('.mx-prod:not([hidden])'); }});
    root.querySelector('#mxp-count').textContent = n + ' loan options shown';
    MX.track('products_filter', {{ filter: f }});
  }});
}});
// Hawaii visitors get the Hawaii line on the call button
var V = MX.visitor();
MX.region(V.qs, V.override, function (hi) {{
  if (hi) root.querySelectorAll('[data-mx-phone]').forEach(function (a) {{ a.textContent = 'Call {HI_PHONE}'; a.href = 'tel:{HI_TEL}'; }});
}});
"""

def plain(s): return re.sub('<[^>]+>', '', s).replace('&amp;', '&')

items = []
pos = 0
for g, intro, prods in GROUPS:
    for name, fact, tags, ideal, desc, typ in prods:
        pos += 1
        it = {"@type": typ, "name": plain(name), "description": plain(desc), "url": SITE + "/products#" + ID[name],
              "provider": {"@id": SITE + "/#org"}, "category": g}
        items.append({"@type": "ListItem", "position": pos, "item": it})

DESC = "Compare 18 home loan options, from 3% down conventional and 0% down VA and USDA to bank statement, DSCR, HELOC and bridge loans."
graph = [ORG] + webpage("/products", "Home Loan Options: FHA, VA, Jumbo, DSCR & Non-QM | Moxie Mortgage", DESC, "Loan options",
                        {"@type": "CollectionPage", "mainEntity": {"@id": SITE + "/products#loans"}}) + [
  {"@type": "ItemList", "@id": SITE + "/products#loans", "name": "Moxie Mortgage home loan options", "numberOfItems": pos, "itemListElement": items}]

open('/home/claude/build/out/moxie-products-embed.html', 'w', encoding='utf-8').write(
    wrap('mx-products', body, script, jsonld(graph), 'LOAN OPTIONS PAGE (/products)'))
print('products ok', pos)

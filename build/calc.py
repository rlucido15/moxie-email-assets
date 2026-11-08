"""Calculator hub (/calculators) + the three calculator pages, built from Calculators.dc.html and CalcPage.dc.html."""
import sys, json
sys.path.insert(0, '/home/claude/work')
from common import *
from optimize import optimize
from calc_copy import HUB, MORTGAGE, AFFORD, RENTBUY

A = APPLY
ORIGIN = "https://rlucido15.github.io"

ICONS = {
 'mortgage': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h2M14 11h2M8 15h2M14 15h2M8 19h2M14 19h2"/></svg>',
 'afford': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M12 12v5M10 14.5h4"/></svg>',
 'rentbuy': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 4L3 8l4 4"/><path d="M3 8h13"/><path d="M17 12l4 4-4 4"/><path d="M21 16H8"/></svg>',
}
RVB_LEGAL = ("This calculator is for estimation purposes only and not intended to offer mortgage, tax, or other financial advice. "
             "Results are not a commitment to lend. Consult a tax advisor about potential deductions. "
             "Contact Moxie Mortgage for current rates and more information.")

PAGES = {
 'mortgage': dict(path='/mortgage-calculator', src=MORTGAGE, out='moxie-calc-mortgage-embed.html',
   eyebrow='Free mortgage calculator', h1='Mortgage payment calculator', name='Mortgage Payment Calculator',
   sub='Estimate your full monthly payment, including taxes, insurance, and HOA fees.',
   card=('Mortgage calculator', 'Thinking of buying a house?', 'Estimate your monthly payment including taxes, insurance, and association fees.', 'Determine your budget'),
   iframe=dict(id='moxie-calc', title='Moxie Mortgage payment calculator', attrs=''),
   minh=(1050, 1710), legal=MORTGAGE['legal'],
   about='Estimates a full monthly mortgage payment, including principal, interest, property taxes, homeowners insurance, mortgage insurance, and HOA fees, across conventional, FHA, VA, USDA, jumbo, and non-QM loans.'),
 'afford': dict(path='/affordabilitycalculator', src=AFFORD, out='moxie-calc-affordability-embed.html',
   eyebrow='Free affordability calculator', h1='How much house can I afford?', name='Home Affordability Calculator',
   sub='Estimate your home budget from your income, debts, and down payment, and see how much you could get preapproved for.',
   card=('Affordability calculator', 'Curious what you can afford?', 'Estimate how much you could get preapproved for.', 'See your buying power'),
   iframe=dict(id='moxie-afford-frame', title='Home affordability calculator',
               attrs=' sandbox="allow-scripts allow-same-origin allow-popups allow-top-navigation-by-user-activation"'),
   minh=(785, 1355), legal=AFFORD['legal'],
   about='Estimates how much home you can afford from yearly income, cash to buy, monthly debts, credit score, and interest rate, with a comfortable-to-stretching price range.'),
 'rentbuy': dict(path='/rentvsbuy', src=RENTBUY, out='moxie-calc-rentvsbuy-embed.html',
   eyebrow='Free rent vs. buy calculator', h1='Should I rent or buy?', name='Rent vs. Buy Calculator',
   sub='Compare the cost of renting with the potential value of owning, from monthly costs to long-term equity.',
   card=('Rent vs. buy calculator', 'Deciding whether to rent or buy?', 'Weigh your options side by side and guide your decision.', 'Plan your future'),
   iframe=dict(id='moxieCalc', title='Rent vs. buy calculator', attrs=' scrolling="no"'),
   minh=(1100, 1650), legal=RVB_LEGAL,
   about='Compares the cost of renting with buying a home over time, including monthly costs, equity, appreciation, closing costs, and break-even years.'),
}

PAGE_CSS = r"""
.mxc-head{padding:48px 0 8px}
.mxc-head .mx-h1{font-size:clamp(36px,4.4vw,54px)}
.mxc-head .mx-lede{font-size:19px;max-width:700px;margin-top:14px !important}
.mxc-frame{padding:16px 0 64px}
.mxc-frame iframe{display:block;width:100%;border:0;min-height:var(--mxc-h,1100px);background:transparent}
@media (max-width:760px){.mxc-frame iframe{min-height:var(--mxc-hm,1600px)}}
.mxc-qa{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:12px;align-items:start}
.mxc-qa .mx-faq summary h3{font-size:17px}
.mxc-qa .mx-faq summary{padding:14px 0;min-height:56px}
.mxc-more{padding:80px 0 40px}
.mxc-more .mx-h2{font-size:clamp(26px,2.6vw,32px);margin-bottom:24px !important}
.mxc-more .mx-card-dark{background:var(--navy);border-color:var(--navy);color:#fff}
.mxc-more .mx-card-dark p{color:#C9D6DF}
.mxc-more .mx-card-dark .mx-more{color:var(--orange)}
.mxc-legal{margin-top:48px !important}
.mxc-hub{padding:72px 0 40px}
.mxc-hub .mx-h1{max-width:860px}
.mxc-hub .mx-lede{max-width:720px}
.mxc-hub .mxc-note{margin-top:16px !important;font-size:15px;font-weight:600;color:var(--muted)}
.mxc-cards{padding:16px 0 88px}
.mxc-cards .mx-grid{grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}
.mxc-cards .mx-card{border-radius:24px;padding:32px;gap:12px;color:var(--navy)}
.mxc-cards .mx-ico{width:60px;height:60px;border-radius:16px}
.mxc-cards .mx-ico svg{width:30px;height:30px}
.mxc-cards .mxc-q{margin-top:8px !important;font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:13px;color:var(--bt)}
.mxc-cards h2{font-size:26px;line-height:1.15;font-weight:800}
.mxc-cards .mx-more{padding-top:12px}
.mxc-cta{padding:0 0 72px}
"""

ORG_REF = {"@id": SITE + "/#org"}


def app_schema(k):
    p = PAGES[k]
    return {"@type": "WebApplication", "@id": SITE + p['path'] + "#app", "name": p['name'], "url": SITE + p['path'],
            "description": p['about'], "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": ORG_REF, "inLanguage": "en-US"}


def plain(a):
    return a.replace('||', ' ')


DEFER = """// Start the calculator once the page itself has loaded, so it doesn't compete with the first paint.
var go = function () { if (!fr.getAttribute('src')) fr.src = fr.dataset.src; };
if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
"""


def build_page(k):
    p = PAGES[k]; src = p['src']
    qs = [(q, ''.join(f'<p class="mx-speak">{para}</p>' for para in a.split('||'))) for q, a in src['faq']]
    half = (len(qs) + 1) // 2
    others = [o for o in ('mortgage', 'afford', 'rentbuy') if o != k]
    ocards = ''.join(f'<a class="mx-card" href="{PAGES[o]["path"]}"><h3>{PAGES[o]["card"][0]}</h3><p>{PAGES[o]["card"][2]}</p><span class="mx-more">{PAGES[o]["card"][3]} →</span></a>' for o in others)
    f = p['iframe']
    body = f"""
<style>{PAGE_CSS.strip()}</style>
<section class="mxc-head" aria-labelledby="mxc-h1">
  <div class="mx-wrap">
    <p class="mx-eyebrow">{p['eyebrow']}</p>
    <h1 id="mxc-h1" class="mx-h1">{p['h1']}</h1>
    <p class="mx-lede mx-speak">{p['sub']}</p>
  </div>
</section>
<section class="mxc-frame" aria-label="{p['name']}">
  <div class="mx-wrap" style="--mxc-h:{p['minh'][0]}px;--mxc-hm:{p['minh'][1]}px">
    <iframe id="{f['id']}" {'data-src' if k == 'mortgage' else 'src'}="{src['iframe']}" title="{f['title']}"{f['attrs']}></iframe>
    <noscript><p><a href="{src['iframe']}">Open the {p['card'][0].lower()}</a></p></noscript>
  </div>
</section>
<section class="mx-sec mx-soft" aria-labelledby="mxc-faq">
  <div class="mx-wrap">
    <h2 id="mxc-faq" class="mx-h2" style="font-size:clamp(30px,3.2vw,40px);margin-bottom:28px">{src['faq_h']}</h2>
    <div class="mxc-qa">
      {faq_details(qs[:half], open_first=False)}
      {faq_details(qs[half:], open_first=False)}
    </div>
  </div>
</section>
<section class="mxc-more" aria-labelledby="mxc-more">
  <div class="mx-wrap">
    <h2 id="mxc-more" class="mx-h2">Try another calculator</h2>
    <div class="mx-grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">
      {ocards}
      <a class="mx-card mx-card-dark" href="{A}?src=calc_{k}"><h3>Ready for real numbers?</h3><p>Turn your estimate into a pre-approval you can shop with.</p><span class="mx-more">Get pre-approved →</span></a>
    </div>
    <p class="mx-fine mxc-legal"><strong>Legal disclosures.</strong> {p['legal']}</p>
  </div>
</section>
"""
    script = f"""
// Size the calculator to its content. The calculator reports its height; only messages from {ORIGIN} are trusted.
var fr = root.querySelector('iframe');
{DEFER if k == 'mortgage' else ''}window.addEventListener('message', function (e) {{
  if (e.origin !== '{ORIGIN}' || e.source !== fr.contentWindow) return;
  var d = e.data || {{}}, h = d.height || d.moxieCalcHeight;
  if (typeof h === 'number' && h > 200 && h < 20000) {{ fr.style.height = Math.ceil(h) + 'px'; fr.style.minHeight = '0'; }}
}});
root.querySelectorAll('a[href^="{A}"]').forEach(function (a) {{
  a.addEventListener('click', function () {{ MX.track('calc_cta_click', {{ calc: '{k}' }}); }});
}});
"""
    page, crumbs = webpage(p['path'], src['title'], src['desc'], p['card'][0][0].upper() + p['card'][0][1:], {"mainEntity": {"@id": SITE + p['path'] + "#app"}})
    crumbs["itemListElement"].insert(1, {"@type": "ListItem", "position": 2, "name": "Calculators", "item": SITE + "/calculators"})
    crumbs["itemListElement"][2]["position"] = 3
    graph = [ORG, page, crumbs, app_schema(k), faq_schema([(q, plain(a)) for q, a in src['faq']])]
    html = wrap('mx-calc-' + k, body, script, jsonld(graph), p['name'].upper() + ' (' + p['path'] + ')')
    # the calculator is the main content: open the connection to it right away
    html = html.replace('<link rel="preload"', f'<link rel="preconnect" href="{ORIGIN}">\n<link rel="preload"', 1)
    html = optimize(html)
    open('/home/claude/build/out/' + p['out'], 'w', encoding='utf-8').write(html)
    print(k, 'ok')


def build_hub():
    cards = ''.join(f"""<a class="mx-card" href="{PAGES[k]['path']}"><span class="mx-ico">{ICONS[k]}</span><p class="mxc-q">{PAGES[k]['card'][1]}</p><h2>{PAGES[k]['card'][0]}</h2><p>{PAGES[k]['card'][2]}</p><span class="mx-more">{PAGES[k]['card'][3]} →</span></a>""" for k in ('mortgage', 'afford', 'rentbuy'))
    body = f"""
<style>{PAGE_CSS.strip()}</style>
<section class="mxc-hub" aria-labelledby="mxc-h1">
  <div class="mx-wrap">
    <p class="mx-eyebrow">Free mortgage calculators</p>
    <h1 id="mxc-h1" class="mx-h1">{HUB['h1']}</h1>
    <p class="mx-lede mx-speak">{HUB['closer']}</p>
    <p class="mxc-note">No sign-up · No credit check · Free</p>
  </div>
</section>
<section class="mxc-cards" aria-label="Calculators">
  <div class="mx-wrap"><div class="mx-grid">{cards}</div></div>
</section>
<section class="mxc-cta" aria-labelledby="mxc-cta">
  <div class="mx-wrap">
    <div class="mx-cta">
      <div style="max-width:640px"><h2 id="mxc-cta" class="mx-h2" style="font-size:clamp(30px,3.2vw,42px)">{HUB['closer_h']}</h2>
        <p>Calculators give you a great estimate. A pre-approval turns it into real numbers you can shop with.</p></div>
      <div class="mx-btns"><a class="mx-btn mx-btn-p" href="{A}?src=calc_hub">Get pre-approved</a><a class="mx-btn mx-btn-w" href="/contact">Get expert guidance</a></div>
    </div>
  </div>
</section>
"""
    script = f"""
root.querySelectorAll('a[href^="{A}"]').forEach(function (a) {{
  a.addEventListener('click', function () {{ MX.track('calc_cta_click', {{ calc: 'hub' }}); }});
}});
"""
    page, crumbs = webpage('/calculators', HUB['title'], HUB['desc'], 'Calculators', {
        "@type": "CollectionPage", "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": app_schema(k)} for i, k in enumerate(('mortgage', 'afford', 'rentbuy'))]}})
    graph = [ORG, page, crumbs]
    html = optimize(wrap('mx-calc-hub', body, script, jsonld(graph), 'CALCULATORS HUB (/calculators)'))
    open('/home/claude/build/out/moxie-calculators-embed.html', 'w', encoding='utf-8').write(html)
    print('hub ok')


build_hub()
for k in PAGES:
    build_page(k)

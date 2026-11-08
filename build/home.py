"""Homepage embed (/) built from the approved Home.dc.html design."""
import buy
from common import *

A = APPLY
GLOGO = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@39110a3/google_logo.png"
BADGE = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@8ea82e8/website/scotsman-top-originators-320"
STEPS = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@c5abc25/website/home-step-"
def step_img(i, alt):
    return (f'<img class="mxh-step-img" src="{STEPS}{i}-800.webp" srcset="{STEPS}{i}-480.webp 480w, {STEPS}{i}-800.webp 800w" '
            f'sizes="(max-width: 640px) 92vw, (max-width: 1024px) 45vw, 370px" width="800" height="600" alt="{alt}" loading="lazy" decoding="async">')
SCOTSMAN_URL = "https://www.scotsmanguide.com/rankings/top-originators/"

def badge(px, cls='', eager=False):
    return (f'<picture><source type="image/webp" srcset="{BADGE}.webp"><img{cls} src="{BADGE}.png" '
            f'alt="Scotsman Guide Top Originators badge" width="{px}" height="{px}" loading="{'eager' if eager else 'lazy'}" decoding="async" '
            f'style="width:{px}px;height:{px}px"></picture>')

WS_FAQ = [
 ("How much can you save with a wholesale lender?", "You can save on both closing costs and your monthly payment. Retail lenders often charge 4.5% to 6% for your loan, and Moxie charges a fraction of that. On a $500,000 mortgage, a 3% difference in margin could mean $15,000 in closing costs, or a lower rate that saves $10,000s over the life of the loan."),
 ("Is it faster to get a mortgage through a wholesale lender?", "Yes. Wholesale lenders like Moxie skip the red tape and long turn times of large retail banks."),
 ("Do wholesale lenders have more loan options than big banks?", "Yes. A retail bank limits you to its own products and pricing. Moxie borrowers get access to 300+ lenders that compete for your business, so you get the best product at the best market price."),
 ("What is a correspondent lender?", "A correspondent lender funds its own mortgage loans and partners with large wholesale investors who assume the loan after closing. It gives Moxie clients the full range of loan options under one roof, with a streamlined approval process."),
]

REVIEWS = [
 ("Pomaika`ilani Tolentino", "Robert and his team provided a speedy and FLAWLESS execution in our loan process. We cannot be more grateful for being referred to Robert and look forward to working with the Moxie team again in the future! Mahalo!"),
 ("Arpit P", "Working with Calvin and the team at Moxie Mortgage was an absolute pleasure from start to finish. Calvin made what is usually a stressful process completely seamless."),
 ("Julia Santini", "We recently closed on a HELOC with Moxie Mortgage and could not have been happier with the entire experience!! Our loan officer, Alex, went above and beyond to ensure a smooth and seamless process from start to finish."),
]

ICO_HOME = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>'
ICO_REFI = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 4v5h-5"/></svg>'
ICO_CASH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/></svg>'
SEC = '<span class="mx-dag">§</span>'
X = '<span class="mx-x" aria-hidden="true">✕</span>'
CK = '<span class="mx-ok" aria-hidden="true">✓</span>'

HOME_CSS = r"""
.mx-sr{position:absolute !important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.mxh-hero{padding:56px 0 40px}
.mxh-hero .mx-rise{animation-name:mxRiseT}
@keyframes mxRiseT{from{transform:translateY(8px)}to{transform:none}}
.mxh-cv{content-visibility:auto;contain-intrinsic-size:auto 900px}
.mxh-hero .mx-h1{font-size:clamp(40px,5vw,62px);line-height:1.04}
.mxh-paths{padding:24px 0 88px}
.mxp a.mxh-path{background:var(--soft);border:1px solid var(--line);border-radius:20px;padding:28px;color:var(--navy);display:flex;gap:18px;align-items:center;transition:transform .15s,border-color .15s}
.mxp a.mxh-path:hover{border-color:var(--blue);transform:translateY(-2px);color:var(--navy)}
.mxh-path .mx-ico{width:56px;height:56px;border-radius:16px;margin:0;flex:none}
.mxh-path .mx-ico svg{width:28px;height:28px}
.mxh-path strong{display:block;font-size:21px;line-height:1.25}
.mxh-path span span{font-size:15px;color:var(--muted)}
.mxh-ws{display:flex;flex-wrap:wrap;gap:56px;align-items:flex-start}
.mxh-ws>div{flex:1 1 460px;min-width:0}
.mxh-ws .mx-intro{margin-top:18px !important;font-size:19px}
.mxh-cmp{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-top:32px}
.mxh-cmp>div{background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px 18px;display:grid;grid-row:span 4;grid-template-rows:subgrid;row-gap:8px;align-items:start}
.mxh-cmp ul{display:contents}
.mxh-cmp>div.mxh-us{background:var(--navy);border-color:var(--navy);color:#fff}
.mxh-cmp .mxh-cmp-h{font-weight:700;color:var(--muted);margin-bottom:4px !important}
.mxh-cmp .mxh-us .mxh-cmp-h{color:#7FDCEC}
.mxh-cmp li{display:flex;gap:8px;align-items:baseline;font-size:16px}
.mx-x{color:#D93025;font-weight:700}
.mx-ok{font-weight:700}
.mxh-ws .mx-faq summary h3{font-size:18px}
.mxh-steps ol{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:28px}
.mxp.mxp .mxh-steps li{display:flex !important;flex-direction:column;gap:10px}
.mxh-step-media{position:relative;margin-bottom:8px}
.mxh-step-img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:20px;background:var(--soft)}
.mxh-num{position:absolute;left:16px;top:16px;width:56px;height:56px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:28px;line-height:1;box-shadow:0 0 0 4px rgba(255,255,255,.9),0 8px 20px rgba(14,42,71,.3)}
.mxh-steps h3{font-size:22px;line-height:1.25;font-weight:700}
.mxh-steps p{color:var(--muted);font-size:16px}
.mxh-steps .mx-dag{font-size:.6em}
.mxh-proof{display:flex;align-items:center;gap:20px;flex-wrap:nowrap;max-width:100%}
@media (max-width:480px){.mxp .mxh-proof{gap:14px;padding:12px 14px !important}.mxh-proof-g{column-gap:8px}.mxh-proof-g img{width:26px;height:26px}.mxh-proof-g .mx-rating-n{font-size:30px}.mxh-proof-g .mx-stars{font-size:13px;letter-spacing:1px}.mxp a.mxh-proof-s{gap:8px;font-size:12px}.mxh-proof-s strong{font-size:14px}.mxh-proof-s img{width:40px !important;height:40px !important}}
.mxh-proof-g{display:grid;grid-template-columns:auto auto;grid-template-rows:auto auto;column-gap:12px;align-items:center}
.mxh-proof-g img{grid-row:1/3;width:32px;height:32px}
.mxh-proof-g .mx-rating-n{font-size:36px}
.mxh-proof-g .mx-stars{font-size:16px;letter-spacing:2px;margin-top:2px}
.mxh-proof-div{width:1px;align-self:stretch;background:var(--line)}
.mxp a.mxh-proof-s{display:flex;align-items:center;gap:12px;color:var(--navy);font-size:14px;line-height:1.3}
.mxp a.mxh-proof-s:hover{color:var(--bt)}
.mxh-proof-s strong{font-size:16px}
.mxh-proof-s>span{white-space:nowrap}
@media (max-width:380px){.mxh-proof-g .mx-rating-n{font-size:26px !important}.mxh-proof-s img{width:32px !important;height:32px !important}.mxh-proof-s strong{font-size:13px !important}.mxp a.mxh-proof-s{font-size:11px !important}.mxp .mxh-proof{gap:12px !important}}
.mxp .mxh-grad{border:3px solid transparent;border-radius:18px;padding:12px 20px;background:linear-gradient(#fff,#fff) padding-box,linear-gradient(135deg,#1C97AE 0%,#0E2A47 100%) border-box}
.mxh-tools{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}
.mxh-tools .mx-card{padding:26px;gap:8px}
.mxh-tools .mx-card h3{font-size:21px}
.mxh-tools .mx-card-dark img{margin-bottom:6px}
.mxh-tools .mx-card-dark h3{color:#fff}
.mxh-final{padding:0 0 72px}
.mxh-notes{margin-top:40px}
.mxp.mxp .mxh-notes p+p{margin-top:10px !important}
"""

body = f"""
<style>{buy.EXTRA_CSS.strip()}{HOME_CSS.strip()}</style>
<section class="mx-hero mxh-hero" aria-labelledby="mxh-h1">
  <div class="mx-wrap">
    <div class="mx-hero-copy">
      <p class="mx-eyebrow mx-rise" data-mx="eyebrow" hidden></p>
      <h1 id="mxh-h1" class="mx-h1 mx-rise"><span data-mx="h1">Buy your dream home and save $1,000s on your mortgage.</span><span data-mx="dag">{DAG}</span></h1>
      <p class="mx-lede mx-rise mx-d2" data-mx="sub">Skip the retail markup. Keep more of your money and reach your home goals faster.</p>
      <div class="mx-btns mx-rise mx-d2">
        <a class="mx-btn mx-btn-p" data-mx="cta" href="{A}?src=hero_purchase">Save on my home loan</a>
        <a class="mx-btn mx-btn-o" data-mx="cta2" href="tel:{HI_TEL}" hidden>Call {HI_PHONE}</a>
      </div>
    </div>
    <div class="mx-hero-media">
      <div class="mx-photo"><img data-mx="img" src="{CDN}buy-hero-1400.webp" srcset="{CDN}buy-hero-800.webp 800w, {CDN}buy-hero-1400.webp 1400w" sizes="(max-width: 900px) 92vw, 560px" width="1400" height="900" alt="Homebuyers shaking hands with their Moxie loan officer after approval" fetchpriority="high" decoding="async"></div>
      <div class="mx-badge"><span class="mx-badge-i">{ICON['trend'].replace('<svg ', '<svg width="22" height="22" ')}</span><span><strong style="display:block;font-size:16px">Wholesale pricing</strong><span style="font-size:13px;color:var(--muted)">No retail markup</span></span></div>
    </div>
  </div>
</section>

<section class="mxh-paths" aria-labelledby="mxh-paths">
  <div class="mx-wrap">
    <h2 id="mxh-paths" class="mx-sr">What would you like to do?</h2>
    <div class="mx-grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">
      <a class="mxh-path" href="/buy"><span class="mx-ico">{ICO_HOME}</span><span><strong>Buy a home</strong><span>Same-day approval, close in 21 days or less†</span></span></a>
      <a class="mxh-path" href="/refinance"><span class="mx-ico">{ICO_REFI}</span><span><strong>Refinance</strong><span>Lower your payment or take cash out</span></span></a>
      <a class="mxh-path" href="/heloc"><span class="mx-ico">{ICO_CASH}</span><span><strong>Tap your equity</strong><span>HELOC funding in as little as 5 days</span></span></a>
    </div>
  </div>
</section>

<section class="mx-sec mx-soft mxh-cv" aria-labelledby="mxh-ws">
  <div class="mx-wrap mxh-ws">
    <div>
      <p class="mx-eyebrow">The Costco of home loans</p>
      <h2 id="mxh-ws" class="mx-h2">What is a wholesale mortgage?</h2>
      <p class="mx-intro mx-speak"><strong>A wholesale mortgage is like an insider price for your home loan.</strong> Big banks and retail lenders add markups to pay for offices, managers, and ads. Moxie skips the retail markup, finds the best deal for you, and puts those savings back in your pocket.</p>
      <div class="mxh-cmp">
        <div><p class="mxh-cmp-h">Retail lender</p><ul><li>{X}<span>Branch and office overhead</span></li><li>{X}<span>Advertising markups</span></li><li>{X}<span>Only their own products</span></li></ul></div>
        <div class="mxh-us"><p class="mxh-cmp-h">Moxie</p><ul><li>{CK}<span>No retail markup</span></li><li>{CK}<span>300+ lender options</span></li><li>{CK}<span>Savings go back to you</span></li></ul></div>
      </div>
    </div>
    <div>{faq_details([(q, f'<p class="mx-speak">{a}</p>') for q, a in WS_FAQ])}</div>
  </div>
</section>

<section class="mx-sec mx-dark" aria-labelledby="mxh-sav" id="mxh-savings">
  <div class="mx-wrap mx-sav">
    <div class="mx-sav-in">
      <p class="mx-eyebrow" style="margin:0 !important">Savings estimator</p>
      <h2 id="mxh-sav" class="mx-h2">Watch your savings add up</h2>
      <p class="mx-speak" style="font-size:19px">Our rates have averaged 0.559% lower than the nation's largest retail lender.<span class="mx-dag">‡</span> Here's what that's worth on your loan.</p>
      <div>
        <div class="mx-sav-row"><label for="mxh-amt">Loan amount</label><output id="mxh-amt-out" for="mxh-amt">$600,000</output></div>
        <input class="mx-range" id="mxh-amt" type="range" min="100000" max="1500000" step="10000" value="600000" aria-valuetext="$600,000">
        <div class="mx-sav-ends"><span>$100K</span><span>$1.5M</span></div>
      </div>
      <div class="mx-sav-act">
        <a class="mx-btn mx-btn-p" id="mxh-sav-cta" href="{A}?src=home_savings&amp;loan_amount=600000">See how much I can save</a>
        <span style="color:#D3E3EC"><strong style="color:#fff" id="mxh-sav-m">{buy.SAV_M}</strong> a month</span>
      </div>
    </div>
    <div class="mx-sav-chart" aria-live="polite">
      <p style="font-weight:700;font-size:17px">Your estimated savings with Moxie</p>
      <div class="mx-bars">
        <div><strong data-y="1">{buy.SAV_1}</strong><i data-yb="1" style="height:4%"></i></div>
        <div><strong data-y="5">{buy.SAV_5}</strong><i data-yb="5" style="height:16.7%"></i></div>
        <div><strong data-y="10">{buy.SAV_10}</strong><i data-yb="10" style="height:33.3%"></i></div>
        <div><strong data-y="30">{buy.SAV_L}</strong><i data-yb="30" style="height:100%"></i></div>
      </div>
      <div class="mx-bar-l" aria-hidden="true"><span>Year 1</span><span>Year 5</span><span>Year 10</span><span>Year 30</span></div>
      <p class="mx-sav-note">Estimate only, not a commitment to lend or a promise of savings. Principal and interest on a 30-year fixed loan. Rate and savings vary and depend on borrower's qualification, property specifics, and market conditions.</p>
    </div>
  </div>
</section>

<section class="mx-sec mxh-steps mxh-cv" aria-labelledby="mxh-steps">
  <div class="mx-wrap">
    <div class="mx-head">
      <div><p class="mx-eyebrow">How it works</p><h2 id="mxh-steps" class="mx-h2">Your 3 steps to homeownership</h2></div>
      <p class="mx-muted">A simpler path from application to keys in hand.</p>
    </div>
    <ol>
      <li><div class="mxh-step-media">{step_img(1, "Couple reviewing their mortgage pre-approval on a laptop at the kitchen table")}<span class="mxh-num" aria-hidden="true">1</span></div><h3>Get pre-approved<br>in minutes{SEC}</h3><p>Answer a few questions online and know exactly what you can afford, with no office visit required.</p></li>
      <li><div class="mxh-step-media">{step_img(2, "Moxie loan officer helping a couple compare mortgage options")}<span class="mxh-num" aria-hidden="true">2</span></div><h3>Get matched with the best product and rate</h3><p>We shop 300+ investors to pair you with the right loan at the right price, not a one-size-fits-all box.</p></li>
      <li><div class="mxh-step-media">{step_img(3, "Family celebrating moving into their new home")}<span class="mxh-num" aria-hidden="true">3</span></div><h3>Close fast and<br>move in sooner</h3><p>Clear to close in 21 days or less from your executed purchase contract,† so you start your next chapter sooner.</p></li>
    </ol>
    <div class="mx-btns" style="margin-top:36px"><a class="mx-btn mx-btn-p" href="{A}?src=home_steps">Get pre-approved today</a></div>
  </div>
</section>

<section class="mx-sec mx-soft mxh-cv" aria-labelledby="mxh-rev" id="mxh-reviews">
  <div class="mx-wrap">
    <div class="mx-head" style="margin-bottom:0">
      <h2 id="mxh-rev" class="mx-h2" style="max-width:640px;font-size:clamp(30px,3.2vw,40px)">Buying a home can be stressful. We're with you every step.</h2>
      <div class="mxh-proof mxh-grad">
        <div class="mxh-proof-g"><img src="{GLOGO}" alt="Google" width="32" height="32" loading="lazy"><span class="mx-rating-n" data-rv="rating">5.0</span><span class="mx-stars" role="img" aria-label="Rated 5 out of 5 stars on Google">★★★★★</span></div>
        <span class="mxh-proof-div" aria-hidden="true"></span>
        <a class="mxh-proof-s" href="{SCOTSMAN_URL}" target="_blank" rel="noopener">{badge(48)}<span>Scotsman Guide<br><strong>Top Originator</strong></span></a>
      </div>
    </div>
    <div class="mx-revs" data-rv="list">
      {''.join(buy.review(n, t) for n, t in REVIEWS)}
    </div>
    <p style="margin-top:24px;text-align:center"><a data-rv="link" href="https://www.google.com/search?q=Moxie+Mortgage+reviews" rel="noopener" style="font-weight:700">Read all reviews on Google →</a></p>
  </div>
</section>

<section class="mx-sec mxh-cv" aria-labelledby="mxh-res">
  <div class="mx-wrap">
    <p class="mx-eyebrow">Moxie comes with knowledge</p>
    <h2 id="mxh-res" class="mx-h2" style="margin-bottom:32px !important;font-size:clamp(30px,3.2vw,40px)">Tools to plan your next move</h2>
    <div class="mxh-tools">
      <a class="mx-card" href="/calculators"><h3>Calculators</h3><p>Discover what's possible based on your numbers.</p><span class="mx-more">Try our calculators →</span></a>
      <a class="mx-card" href="/faqs"><h3>Mortgage FAQs</h3><p>Instant answers to the 100 questions we hear most.</p><span class="mx-more">Browse FAQs →</span></a>
      <a class="mx-card" href="/products"><h3>Loan options</h3><p>Whatever your scenario, we have a product for you.</p><span class="mx-more">Explore our products →</span></a>
      <a class="mx-card mx-card-dark" href="{SCOTSMAN_URL}" target="_blank" rel="noopener">{badge(88)}<span class="mx-tag">Recognition</span><h3>Scotsman Guide names Moxie a Top Originator</h3><span class="mx-more">Read more →</span></a>
    </div>
  </div>
</section>

<section class="mxh-final" aria-labelledby="mxh-cta">
  <div class="mx-wrap">
    <div class="mx-cta">
      <div style="max-width:640px"><p class="mx-eyebrow" style="color:#7FDCEC">Serving 51 states and territories</p>
        <h2 id="mxh-cta" class="mx-h2" style="font-size:clamp(30px,3.2vw,42px)">Buy with Moxie. Own with confidence.</h2>
        <p>Licensed experts across the country are ready to guide you through the process and secure a great rate.</p></div>
      <div class="mx-btns"><a class="mx-btn mx-btn-p" href="{A}?src=home_cta">Get approved now</a><a class="mx-btn mx-btn-w" href="/contact">Get expert guidance</a></div>
    </div>
    <div class="mxh-notes mx-fine">
      <p>† Offers made by Moxie Mortgage are available only to clients who are purchasing a home and financing with Moxie Mortgage. This is not a commitment to lend and is contingent on qualification per full underwriting guidelines. Conditions and exclusions apply.</p>
      <p>§ “In minutes” refers to the time it takes to submit an application. Time will vary based on the parameters of the applicant’s situation. A preapproval decision will be provided within 24 hours of a completed application.</p>
      <p>‡ Based on Moxie Mortgage’s apples-to-apples comparison of weekly rates against Rocket Mortgage from November 2025 to November 2026; average difference 0.559%. Savings estimates compare principal and interest on a 30-year fixed loan at a {buy.SAV_BASE}% example rate with a rate {buy.SAV_GAP}% lower. Individual results vary.</p>
    </div>
  </div>
</section>
"""

# ---- reuse the Buy page's estimator + review library JS, re-pointed at this page's ids
s = buy.script
est = s[s.index('// ---- savings estimator'):s.index('// ---- tabs')].replace('mxb-', 'mxh-').replace('buy_savings', 'home_savings')
rev = s[s.index('// ---- Review library'):].replace('#mxb-reviews', '#mxh-reviews')
rev = rev.replace("if (d.count) sec.querySelector('[data-rv=\"count\"]').textContent = d.count + ' reviews on Google';", "")
rev = rev.replace("if (d.rating) { var n = sec.querySelector('[data-rv=\"rating\"]'); n.textContent = Number(d.rating).toFixed(1); n.hidden = false; }",
  "if (d.rating) root.querySelectorAll('[data-rv=\"rating\"]').forEach(function (n) { n.textContent = Number(d.rating).toFixed(1); });")
assert 'reviews on Google' not in rev and "querySelectorAll('[data-rv=\"rating\"]')" in rev, 'review patch failed'

hero_js = f"""
// ---- Dynamic hero. The HTML above is version A (what search engines index).
// Order: ?hero= override > UTM intent (refi / heloc) > returning visitor > A/B arm. Hawaii overlays on top.
// Test: ?hero=refi|heloc|returning|hawaii|default|reset  ?ab=A|B  ?geo=HI
var V = MX.visitor(), qs = V.qs, S = MX.store;
var SUB = 'Skip the retail markup. Keep more of your money and reach your home goals faster.';
var VARS = {{
  a: {{ eyebrow: '', h1: 'Buy your dream home and save $1,000s on your mortgage.', sub: SUB, cta: 'Save on my home loan', dag: true, src: 'purchase' }},
  b: {{ eyebrow: '', h1: 'Same home. Lower mortgage. Keep the $1,000s you\\u2019d pay a retail lender.', sub: SUB, cta: 'Save on my home loan', dag: true, src: 'purchase' }},
  returning: {{ eyebrow: 'Welcome back', h1: 'Ready to pick up where you left off?', sub: 'Your savings are still waiting. Getting pre-approved takes just a few minutes.', cta: 'Continue my approval', dag: false, src: 'returning' }},
  refi: {{ eyebrow: 'Refinance', h1: 'Lower your payment without the retail markup.', sub: 'See what you could save by refinancing with Moxie. It takes a few minutes and won\\u2019t affect your credit to start.', cta: 'See my refi savings', dag: false, src: 'refi' }},
  heloc: {{ eyebrow: 'Home equity', h1: 'Put your home\\u2019s equity to work.', sub: 'Tap your equity for renovations, debt payoff, or what\\u2019s next, and skip the retail markup.', cta: 'Check my HELOC options', dag: false, src: 'heloc' }},
  hawaii: {{ eyebrow: 'Serving Hawaii homebuyers', h1: 'Buy your Hawaii home and save $1,000s on your mortgage.', sub: 'Island prices are high enough. Skip the retail markup and keep more of your money with a loan expert who knows the market.', cta: 'Save on my Hawaii home loan', dag: true, src: 'purchase_hi' }},
  hawaiiReturning: {{ eyebrow: 'Aloha, welcome back', h1: 'Ready to pick up where you left off?', sub: 'Your savings are still waiting. Getting pre-approved takes just a few minutes.', cta: 'Continue my approval', dag: false, src: 'returning_hi' }}
}};
var IMG_HI = {{ src: '{CDN}hawaii-hero-1400.webp', srcset: '{CDN}hawaii-hero-800.webp 800w, {CDN}hawaii-hero-1400.webp 1400w', alt: 'Hawaii family reviewing paperwork with their agent outside their new home' }};

// intent from UTMs, kept for the session
var utm = ['utm_campaign', 'utm_content', 'utm_term', 'utm_source', 'utm_medium'].map(function (k) {{ return qs.get(k) || ''; }}).join(' ').toLowerCase();
var intent = /heloc|equity/.test(utm) ? 'heloc' : /refi/.test(utm) ? 'refi' : '';
if (intent) S.sset('mx_intent', intent); else intent = S.sget('mx_intent') || '';

// sticky A/B arm
var ab = (qs.get('ab') || '').toUpperCase();
if (ab === 'A' || ab === 'B') S.set('mx_ab', ab);
ab = S.get('mx_ab');
if (ab !== 'A' && ab !== 'B') {{ ab = Math.random() < 0.5 ? 'A' : 'B'; S.set('mx_ab', ab); }}

var ov = V.override, variant;
if (ov === 'refi' || ov === 'heloc') variant = ov;
else if (ov === 'returning') variant = 'returning';
else if (ov === 'default' || ov === 'hawaii') variant = ab === 'B' ? 'b' : 'a';
else if (intent) variant = intent;
else if (V.returning) variant = 'returning';
else variant = ab === 'B' ? 'b' : 'a';

// carry UTMs to the application
var pass = '';
qs.forEach(function (val, k) {{ if (/^utm_/.test(k)) pass += '&' + encodeURIComponent(k) + '=' + encodeURIComponent(val); }});

var heroLabel = '', heroGeo = '';
function decide(hi) {{
  var key = variant;
  if (hi && (variant === 'a' || variant === 'b')) key = 'hawaii';
  if (hi && variant === 'returning') key = 'hawaiiReturning';
  var v = VARS[key];
  var ey = root.querySelector('[data-mx="eyebrow"]'); ey.textContent = v.eyebrow; ey.hidden = !v.eyebrow;
  MX.applyHero(root, {{ h1: v.h1, sub: v.sub, dag: v.dag, cta: {{ text: v.cta, href: '{A}?src=hero_' + v.src + pass }} }});
  var c2 = root.querySelector('[data-mx="cta2"]');
  if (hi) {{ MX.applyHero(root, {{ img: IMG_HI }}); c2.hidden = false; }}
  heroLabel = v.src; heroGeo = hi ? 'HI' : '';
  MX.track('hero_view', {{ hero_page: 'home', hero_variant: key, hero_ab: ab, hero_geo: heroGeo, hero_label: heroLabel }});
  MX.hi = hi; if (MX.loadReviews) MX.loadReviews(hi);
}}
MX.region(qs, ov, decide);
root.querySelector('[data-mx="cta"]').addEventListener('click', function () {{ MX.track('hero_cta_click', {{ hero_page: 'home', hero_label: heroLabel, hero_ab: ab, hero_geo: heroGeo }}); }});
root.querySelector('[data-mx="cta2"]').addEventListener('click', function () {{ MX.track('hero_call_click', {{ hero_page: 'home', hero_label: heroLabel, hero_geo: heroGeo }}); }});
"""
script = est + rev + "\nMX.loadReviews = loadReviews; if (MX.hi !== undefined) loadReviews(MX.hi);\n"


DESC = "Moxie Mortgage is a wholesale mortgage broker serving 51 states and territories. Skip the retail markup on home purchase, refinance, and HELOC loans."
graph = [ORG,
  {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Moxie Mortgage", "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-US"},
  {"@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/", "name": "Moxie Mortgage | Wholesale Mortgage Broker, 51 States", "description": DESC,
   "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#org"}, "inLanguage": "en-US",
   "primaryImageOfPage": {"@type": "ImageObject", "url": CDN + "buy-hero-1400.webp", "width": 1400, "height": 900},
   "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".mx-h1", ".mx-lede", ".mx-speak"]}},
  {"@type": "HowTo", "name": "Your 3 steps to homeownership with Moxie Mortgage", "step": [
    {"@type": "HowToStep", "position": 1, "image": STEPS + "1-800.webp", "name": "Get pre-approved in minutes", "text": "Answer a few questions online and know exactly what you can afford, with no office visit required. A preapproval decision is provided within 24 hours of a completed application."},
    {"@type": "HowToStep", "position": 2, "image": STEPS + "2-800.webp", "name": "Get matched with the best product and rate", "text": "Moxie shops 300+ investors to pair you with the right loan at the right price."},
    {"@type": "HowToStep", "position": 3, "image": STEPS + "3-800.webp", "name": "Close fast and move in sooner", "text": "Clear to close in 21 days or less from your executed purchase contract."}]},
  faq_schema([("What is a wholesale mortgage?", "A wholesale mortgage is like an insider price for your home loan. Big banks and retail lenders add markups to pay for offices, managers, and ads. A wholesale mortgage broker like Moxie Mortgage skips the retail markup, shops 300+ lenders for the best deal, and passes the savings to the borrower.")] + WS_FAQ)]

html = wrap('mx-home', body, script, jsonld(graph), 'HOMEPAGE (/)')
# hero runs right after its own markup, before first paint, so a returning / refi / B-arm swap never shifts the layout
early = "<script>\n(function () {\n" + ENGINE.strip() + "\nvar root = document.getElementById('mx-home');\n" + hero_js.strip() + "\n})();\n</script>"
i = html.index('</section>') + len('</section>')
html = html[:i] + '\n' + early + html[i:]
from optimize import optimize
html = optimize(html, hero_img=(CDN + 'buy-hero-800.webp 800w, ' + CDN + 'buy-hero-1400.webp 1400w', '(max-width: 900px) 92vw, 560px'))
open('/home/claude/build/out/moxie-home-embed.html', 'w', encoding='utf-8').write(html)
print('home ok')

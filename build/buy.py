from common import *
CDN_MAIN = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@main/website/"

A = APPLY
img = lambda name, alt, eager=True: (
    f'<img data-mx="img" src="{CDN}{name}-1400.webp" srcset="{CDN_M}{name}-480.webp 480w, {CDN_M}{name}-640.webp 640w, {CDN}{name}-800.webp 800w, {CDN}{name}-1400.webp 1400w" '
    f'sizes="(max-width: 900px) calc(92vw - 28px), 532px" width="1400" height="900" alt="{alt}"'
    + (' fetchpriority="high" decoding="async"' if eager else ' loading="lazy" decoding="async"') + '>')

FAQ = [
 ("How long does it take to close a mortgage?", "Most lenders typically require 30–45 days to close a mortgage; however, Moxie can close in as little as 10 days, making our buyers' offers more attractive to sellers."),
 ("What is a rate lock and should I use one?", "A rate lock guarantees your interest rate for a set period, protecting you from rate increases. A standard rate lock is 30 days; however, Moxie has the ability to lock your rate for up to 360 days."),
 ("How much do I need for a down payment?", "It depends on the loan type: conventional as low as 3%–5%, FHA 3.5%, VA and USDA 0% down for qualified borrowers, and jumbo often 10%–20%."),
 ("What's the difference between prequalification and preapproval?", "Pre-qualification is an estimate of what you could afford that is missing one or more criteria for a full preapproval, such as proof of funds, verification of employment and income, or a satisfactory review of credit."),
]

REVIEWS = [
 ("Alejandro Navia", "They held our hand every step of the way, explaining every detail with patience and clarity. Thank you, Moxie Mortgage, for making our dream of homeownership a reality!"),
 ("Arpit P", "Calvin made what is usually a stressful process completely seamless. His professionalism, transparency, and attention to detail gave me complete confidence that I was in the best hands."),
 ("S Peterson", "Alex Salomons of Moxie Mortgage was great to work with. She was very patient and helpful, guided us through the entire process, provided options, and answered all our questions."),
]

def guar(icon, title, text):
    return f'<article class="mx-card"><span class="mx-ico">{ICON[icon]}</span><h3><span class="mx-line1">{title.replace(" Guarantee", "")}</span><br>Guarantee{DAG}</h3><p>{text}</p></article>'

def review(name, text):
    return (f'<figure class="mx-rev"><div class="mx-rev-top"><span class="mx-stars" role="img" aria-label="5 out of 5 stars">★★★★★</span>'
            f'<span class="mx-rev-src" data-glogo>Google</span></div><blockquote>“{text}”</blockquote>'
            f'<figcaption><span class="mx-av" aria-hidden="true">{name[0]}</span><span>{name}</span></figcaption></figure>')


def _pay(L, r):
    i = r / 1200
    return L * i / (1 - (1 + i) ** -360)
SAV_BASE, SAV_GAP, SAV_DEF = 6.75, 0.559, 600000
_sv = _pay(SAV_DEF, SAV_BASE) - _pay(SAV_DEF, SAV_BASE - SAV_GAP)
usd = lambda n: '${:,.0f}'.format(n)
SAV_M, SAV_L, SAV_5, SAV_1, SAV_10 = usd(_sv), usd(_sv * 360), usd(_sv * 60), usd(_sv * 12), usd(_sv * 120)

EXTRA_CSS = r"""
.mx-uba h3{font-size:20px !important;letter-spacing:-.005em !important}
.mx-uba h3 .mx-line1{white-space:nowrap}
.mx-time ol{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;margin-top:24px !important}
.mxp.mxp .mx-time li{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:28px 28px 30px !important;display:flex;flex-direction:column;gap:10px}
.mx-time h3{margin:0 !important}
.mxp.mxp .mx-time li.mx-last{background:#fff;color:var(--navy);border-color:#fff}
.mx-time li.mx-last p{color:var(--muted)}
.mx-step{font-weight:700;font-size:14px;letter-spacing:.12em !important;color:#7FDCEC;text-transform:uppercase !important}
.mx-time li.mx-last .mx-step{color:var(--bt)}
.mx-time h3{font-size:24px;line-height:1.2;font-weight:700}
.mx-track{height:3px;border-radius:3px;background:rgba(255,255,255,.14);overflow:hidden;margin-top:44px}
.mx-track span{display:block;height:100%;background:var(--blue);transform-origin:left;transform:scaleX(0);transition:transform 1.6s ease-out}
.mx-track.is-in span{transform:scaleX(1)}
.mx-soon{display:flex;flex-wrap:wrap;gap:48px;align-items:flex-start}
.mx-tabs{display:flex;flex-wrap:wrap;gap:8px;background:var(--soft);padding:6px;border-radius:14px}
.mxp .mx-tab{flex:1 1 160px;min-height:46px;border:0;border-radius:10px;background:transparent;color:var(--navy);font-family:inherit;font-weight:700;font-size:16px;line-height:1.2;cursor:pointer;padding:10px 16px}
.mxp .mx-tab[aria-selected="true"]{background:var(--navy);color:#fff}
.mx-panel{margin-top:18px;border:1px solid var(--line);border-radius:20px;padding:32px}
.mx-panel h3{font-size:26px;font-weight:700;margin-bottom:8px !important}
.mx-panel p{color:var(--muted);margin-bottom:22px !important}
.mx-card-dark{background:var(--navy);border-color:var(--navy);color:#fff}
.mx-card-dark p{color:#C9D6DF}
.mx-card-dark .mx-tag,.mx-card-dark .mx-more{color:#7FDCEC}
.mx-tag{font-weight:700;font-size:13px;letter-spacing:.12em !important;color:var(--bt);text-transform:uppercase !important}
a.mx-card{color:var(--navy)}
a.mx-card.mx-card-dark{color:#fff}
.mx-rating{display:flex;gap:16px;align-items:center;border:1px solid var(--line);border-radius:16px;padding:14px 20px}
.mx-rating img{height:32px;width:32px}
.mx-rating-n{font-size:40px;font-weight:800;line-height:1}
.mx-revs{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-top:28px}
.mxp.mxp .mx-rev{border:1px solid var(--line);border-radius:20px;padding:32px 32px 28px !important;margin:0 !important;background:#fff;display:flex;flex-direction:column;gap:14px}
.mx-rev-top{display:flex;justify-content:space-between;align-items:center}
.mx-stars{color:var(--orange);letter-spacing:3px;font-size:18px}
.mx-rev-src{font-size:13px;color:var(--muted);display:inline-flex;align-items:center}
.mx-rev-src img{height:20px;width:20px;display:block}
.mxp.mxp .mx-rev blockquote{margin:0 !important;padding:0 !important;border:0 !important;font-style:normal !important;quotes:none}
.mx-rev blockquote{font-size:18px;line-height:1.5}
.mx-rev figcaption{margin-top:auto;display:flex;gap:12px;align-items:center;font-weight:700}
.mx-sav{display:flex;flex-wrap:wrap;gap:48px 96px;align-items:stretch}
.mx-sav-in{flex:1 1 380px;min-width:0;display:flex;flex-direction:column;justify-content:center;gap:16px}
.mx-sav-row{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-top:16px}
.mx-sav-row label{font-weight:700;font-size:17px}
.mx-sav-row output{font-size:30px;font-weight:800;font-variant-numeric:tabular-nums;color:#fff}
.mxp .mx-range{-webkit-appearance:none;appearance:none;width:100%;height:8px;border-radius:8px;background:linear-gradient(90deg,var(--blue) var(--p,35.7%),rgba(255,255,255,.25) var(--p,35.7%));cursor:pointer;margin:12px 0 6px}
.mx-range::-webkit-slider-thumb{-webkit-appearance:none;width:28px;height:28px;border-radius:50%;background:#fff;border:3px solid var(--blue);box-shadow:0 2px 8px rgba(14,42,71,.25)}
.mx-range::-moz-range-thumb{width:24px;height:24px;border-radius:50%;background:#fff;border:3px solid var(--blue);box-shadow:0 2px 8px rgba(14,42,71,.25)}
.mx-sav-ends{display:flex;justify-content:space-between;font-size:14px;color:#C9D6DF}
.mx-sav-act{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:8px}
.mx-sav-chart{flex:1 1 500px;min-width:0;background:#fff;color:var(--navy);border-radius:24px;padding:32px 36px 24px;box-shadow:0 30px 60px rgba(2,10,30,.3);display:flex;flex-direction:column;gap:18px}
.mx-sav-chart p{color:var(--navy)}
.mx-bars{height:260px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;align-items:end;border-bottom:2px solid var(--line)}
.mx-bars>div{height:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:10px}
.mx-bars strong{font-size:20px;font-variant-numeric:tabular-nums}
.mx-bars i{display:block;width:70%;border-radius:10px 10px 0 0;background:linear-gradient(180deg,#1C97AE,#0E2A47);transition:height .25s ease-out}
.mx-bar-l{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;text-align:center;font-size:15px;color:var(--muted);font-weight:600}
.mx-sav-chart .mx-sav-note{font-size:12px;line-height:1.5;color:var(--muted)}
@media (max-width:640px){.mx-sav-chart{padding:24px 18px 18px}.mx-bars{height:200px;gap:10px}.mx-bars strong{font-size:15px}.mx-bar-l{gap:10px;font-size:13px}}
.mx-av{width:40px;height:40px;border-radius:50%;background:var(--navy);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:700;flex:none;overflow:hidden}
.mx-av.has-photo{background:#E3F5F9}
.mx-av img{width:100%;height:100%;object-fit:cover;display:block}
"""

body = f"""
<style>{EXTRA_CSS.strip()}</style>
<section class="mx-hero" aria-labelledby="mxb-h1">
  <div class="mx-wrap">
    <div class="mx-hero-copy">
      <p class="mx-eyebrow mx-rise" data-mx="eyebrow">Home purchase loans</p>
      <h1 id="mxb-h1" class="mx-h1 mx-rise"><span data-mx="h1">Buy your dream home and save $1,000s on your mortgage.</span><span data-mx="dag">{DAG}</span></h1>
      <p class="mx-lede mx-rise mx-d2" data-mx="sub">Moxie is direct to wholesale, so you skip the retail overhead. Get approved the same day and close in 21 days or less.</p>
      <div class="mx-btns mx-rise mx-d2">
        <a class="mx-btn mx-btn-p" data-mx="cta" href="{A}?src=buy_hero">Get approved today</a>
        <a class="mx-btn mx-btn-o" data-mx="cta2" href="/products">Explore loan options</a>
      </div>
      <ul class="mx-stats mx-rise mx-d2">
        <li><strong>24 hrs</strong><span>Preapproval decision{DAG}</span></li>
        <li><strong>360 days</strong><span>Lock and shop{DAG}</span></li>
        <li><strong>≤ 21 days</strong><span>Clear to close{DAG}</span></li>
      </ul>
    </div>
    <div class="mx-hero-media mx-fade">
      <div class="mx-photo">{img('buy-hero', 'Homebuyers shaking hands with their Moxie loan officer after approval')}</div>
      <div class="mx-badge"><span class="mx-badge-i">{ICON['check22']}</span><span><strong style="display:block;font-size:16px">You're preapproved</strong><span style="font-size:13px;color:var(--muted)">Same-day decision{DAG}</span></span></div>
    </div>
  </div>
</section>

<section class="mx-sec mx-soft mx-uba" aria-labelledby="mxb-uba">
  <div class="mx-wrap">
    <div class="mx-head">
      <div><p class="mx-eyebrow">Four guarantees</p><h2 id="mxb-uba" class="mx-h2">The Ultimate Buyer Advantage</h2></div>
      <p class="mx-muted">Every Moxie purchase loan comes with protections most lenders don't offer, before and after you close.</p>
    </div>
    <div class="mx-grid">
      {guar('trend', 'Low Rates Guarantee', "Don't pay for a lender's office and overhead. Moxie is direct to wholesale and passes the savings on to you.")}
      {guar('shield', 'Buyer Rate Protection Guarantee', "If you aren't happy with your mortgage, we'll cover your lender fees on any refinance to help.")}
      {guar('grid', 'Best Product Guarantee', "With access to 1,000s of products, we'll help you find the best product for your needs.")}
      {guar('pct', 'Rate Buydown Guarantee', "We'll knock 1% off your rate for the first year, so your payment starts lower while you settle in.")}
    </div>
  </div>
</section>

<section class="mx-sec mx-dark mx-time" aria-labelledby="mxb-time">
  <div class="mx-wrap">
    <p class="mx-eyebrow">Speed wins offers</p>
    <h2 id="mxb-time" class="mx-h2">Because time is of the essence</h2>
    <p style="margin-top:16px;max-width:620px;font-size:19px">Sellers pick offers they trust to close. Here's how fast Moxie moves, from first application to keys.</p>
    <div class="mx-track" aria-hidden="true"><span></span></div>
    <ol>
      <li><span class="mx-step">Step 1 · Day one</span><h3>Same Day Mortgage Approval{DAG}</h3><p>We'll deliver your preapproval decision within 24 hours of completed application.</p></li>
      <li><span class="mx-step">Step 2 · While you shop</span><h3>Lock and Shop<br>Option{DAG}</h3><p>You can lock your rate for up to 360 days while you shop for your dream home.</p></li>
      <li class="mx-last"><span class="mx-step">Step 3 · Under contract</span><h3>Clear to Close in 21 Days or Less{DAG}</h3><p>Close in 21 days or less from receipt of your executed purchase contract.</p></li>
    </ol>
  </div>
</section>

<section class="mx-sec" aria-labelledby="mxb-soon">
  <div class="mx-wrap mx-soon">
    <div style="flex:1 1 340px;min-width:0">
      <p class="mx-eyebrow">Your next step</p>
      <h2 id="mxb-soon" class="mx-h2">How soon do you want to buy your home?</h2>
      <p class="mx-muted" style="margin-top:16px">Pick where you are today. We'll point you to the fastest path.</p>
    </div>
    <div style="flex:2 1 560px;min-width:0">
      <div class="mx-tabs" role="tablist" aria-label="Buying timeline">
        <button type="button" class="mx-tab" role="tab" id="mxb-t1" aria-controls="mxb-p1" aria-selected="true">I'm ready now</button>
        <button type="button" class="mx-tab" role="tab" id="mxb-t2" aria-controls="mxb-p2" aria-selected="false" tabindex="-1">Beginning my search</button>
        <button type="button" class="mx-tab" role="tab" id="mxb-t3" aria-controls="mxb-p3" aria-selected="false" tabindex="-1">Just researching</button>
      </div>
      <div class="mx-panel" role="tabpanel" id="mxb-p1" aria-labelledby="mxb-t1">
        <h3>Apply now and get approved same day</h3><p>We'll help you find the perfect mortgage for the perfect home. The application takes about 10 minutes.</p>
        <a class="mx-btn mx-btn-p" href="{A}?src=buy_ready">Get approved today</a>
      </div>
      <div class="mx-panel" role="tabpanel" id="mxb-p2" aria-labelledby="mxb-t2" hidden>
        <h3>Lock your rate for up to 360 days</h3><p>Avoid paying a higher rate and missing out on that dream home. It's easy to do online and you can be approved same day.</p>
        <a class="mx-btn mx-btn-p" href="{A}?src=buy_lockshop">Get Lock and Shop protection</a>
      </div>
      <div class="mx-panel" role="tabpanel" id="mxb-p3" aria-labelledby="mxb-t3" hidden>
        <h3>Talk it through with a loan expert</h3><p>Learn about the homebuying process and how to take advantage of Moxie's buyer benefits. No obligation.</p>
        <a class="mx-btn mx-btn-o" href="/contact">Chat with a loan expert</a>
      </div>
    </div>
  </div>
</section>

<section class="mx-sec mx-dark" aria-labelledby="mxb-sav" id="mxb-savings">
  <div class="mx-wrap mx-sav">
    <div class="mx-sav-in">
      <p class="mx-eyebrow" style="margin:0 !important">Savings estimator</p>
      <h2 id="mxb-sav" class="mx-h2">Watch your savings add up</h2>
      <p class="mx-speak" style="font-size:19px">Our rates have averaged 0.559% lower than the nation's largest retail lender.<span class="mx-dag">‡</span> Here's what that's worth on your loan.</p>
      <div>
        <div class="mx-sav-row"><label for="mxb-amt">Loan amount</label><output id="mxb-amt-out" for="mxb-amt">$600,000</output></div>
        <input class="mx-range" id="mxb-amt" type="range" min="100000" max="1500000" step="10000" value="600000" aria-valuetext="$600,000">
        <div class="mx-sav-ends"><span>$100K</span><span>$1.5M</span></div>
      </div>
      <div class="mx-sav-act">
        <a class="mx-btn mx-btn-p" id="mxb-sav-cta" href="{A}?src=buy_savings&amp;loan_amount=600000">See how much I can save</a>
        <span style="color:#D3E3EC"><strong style="color:#fff" id="mxb-sav-m">{SAV_M}</strong> a month</span>
      </div>
    </div>
    <div class="mx-sav-chart" aria-live="polite">
      <p style="font-weight:700;font-size:17px">Your estimated savings with Moxie</p>
      <div class="mx-bars">
        <div><strong data-y="1">{SAV_1}</strong><i data-yb="1" style="height:4%"></i></div>
        <div><strong data-y="5">{SAV_5}</strong><i data-yb="5" style="height:16.7%"></i></div>
        <div><strong data-y="10">{SAV_10}</strong><i data-yb="10" style="height:33.3%"></i></div>
        <div><strong data-y="30">{SAV_L}</strong><i data-yb="30" style="height:100%"></i></div>
      </div>
      <div class="mx-bar-l" aria-hidden="true"><span>Year 1</span><span>Year 5</span><span>Year 10</span><span>Year 30</span></div>
      <p class="mx-sav-note">Estimate only, not a commitment to lend or a promise of savings. Principal and interest on a 30-year fixed loan. Rate and savings vary and depend on borrower's qualification, property specifics, and market conditions.</p>
    </div>
  </div>
</section>

<section class="mx-sec mx-soft" aria-labelledby="mxb-prog">
  <div class="mx-wrap">
    <h2 id="mxb-prog" class="mx-h2" style="margin-bottom:32px">Ways to make your purchase easier</h2>
    <div class="mx-grid">
      <a class="mx-card" href="/products#va"><span class="mx-tag">0% down options</span><h3>Get the home and keep your savings</h3><p>VA and USDA loans let eligible buyers put 0% down. Down payment assistance can cover the rest.</p><span class="mx-more">Explore 0% down →</span></a>
      <a class="mx-card" href="/products#bridge-loan"><span class="mx-tag">Bridge loans</span><h3>Buy your next home before selling</h3><p>A short-term bridge loan lets you make a non-contingent offer while your current home is still listed.</p><span class="mx-more">Learn about bridge loans →</span></a>
      <a class="mx-card mx-card-dark" href="/calculators"><span class="mx-tag">Calculators</span><h3>See what you can afford</h3><p>Run the numbers on payment, affordability, and rent vs. buy in under a minute.</p><span class="mx-more">Get my instant analysis →</span></a>
    </div>
  </div>
</section>

<section class="mx-sec" aria-labelledby="mxb-rev" id="mxb-reviews">
  <div class="mx-wrap">
    <div class="mx-head" style="margin-bottom:0">
      <h2 id="mxb-rev" class="mx-h2" style="max-width:640px">Buying a home can be stressful. We're with you every step.</h2>
      <div class="mx-rating">
        <img src="https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@39110a3/google_logo.png" alt="Google" width="32" height="32" loading="lazy" onerror="this.outerHTML='&lt;strong style=&quot;font-size:20px&quot;&gt;Google&lt;/strong&gt;'">
        <span class="mx-rating-n" data-rv="rating" hidden></span>
        <span><span class="mx-stars" role="img" aria-label="Rated 5 stars on Google">★★★★★</span><span style="display:block;font-size:14px;color:var(--muted)" data-rv="count">Reviews from Google</span></span>
      </div>
    </div>
    <div class="mx-revs" data-rv="list">
      {''.join(review(n, t) for n, t in REVIEWS)}
    </div>
    <p style="margin-top:24px;text-align:center"><a data-rv="link" href="https://www.google.com/search?q=Moxie+Mortgage+reviews" rel="noopener" style="font-weight:700;display:inline-flex;align-items:center;min-height:48px;padding:0 16px">Read all reviews on Google →</a></p>
  </div>
</section>

<section class="mx-sec mx-soft" aria-labelledby="mxb-faq">
  <div class="mx-wrap" style="max-width:928px">
    <h2 id="mxb-faq" class="mx-h2">Home buying questions, answered</h2>
    <p class="mx-muted" style="margin:8px 0 28px">Straight answers to what buyers ask us most. <a href="/faqs" style="text-decoration:underline;text-underline-offset:3px">See all 100 mortgage FAQs</a></p>
    {faq_details([(q, f'<p class="mx-speak">{a}</p>') for q, a in FAQ])}
  </div>
</section>

<section class="mx-sec" aria-labelledby="mxb-cta">
  <div class="mx-wrap">
    <div class="mx-cta">
      <div style="max-width:640px"><h2 id="mxb-cta" class="mx-h2">Get expert guidance now. No obligation.</h2>
      <p>Our financing consultants will match you with the best product for your needs at the best price available.</p></div>
      <div class="mx-btns"><a class="mx-btn mx-btn-p" href="{A}?src=buy_cta">Get approved today</a><a class="mx-btn mx-btn-w" data-mx-phone href="tel:{PHONE_TEL}">Call {PHONE}</a></div>
    </div>
    <p class="mx-fine" style="margin-top:40px">† Offers made by Moxie Mortgage are available only to clients who are purchasing a home and financing with Moxie Mortgage. Certain offers require a minimum purchase price of $300,000 including, but not limited to, $1,000 lender credit for closing costs. This is not a commitment to lend and is contingent on qualification per full underwriting guidelines. Offers made by Moxie Mortgage may not be redeemed for cash and are non-transferable. Offers cannot be retroactively applied to loans where the rate has been locked. Conditions and exclusions apply.</p>
    <p class="mx-fine" style="margin-top:10px">‡ Based on Moxie Mortgage’s apples-to-apples comparison of weekly rates against Rocket Mortgage from November 2025 to November 2026; average difference 0.559%. Savings estimates compare principal and interest on a 30-year fixed loan at a {SAV_BASE}% example rate with a rate {SAV_GAP}% lower. Individual results vary.</p>
  </div>
</section>
"""

script = f"""
// ---- dynamic hero: default is in the HTML (what search engines index); swaps for returning + Hawaii visitors
var V = MX.visitor();
var IMG_DEF = {{ src: '{CDN}buy-hero-1400.webp', srcset: '{CDN_M}buy-hero-480.webp 480w, {CDN_M}buy-hero-640.webp 640w, {CDN}buy-hero-800.webp 800w, {CDN}buy-hero-1400.webp 1400w', alt: 'Homebuyers shaking hands with their Moxie loan officer after approval' }};
var IMG_HI = {{ src: '{CDN}hawaii-hero-1400.webp', srcset: '{CDN_M}hawaii-hero-480.webp 480w, {CDN_M}hawaii-hero-640.webp 640w, {CDN}hawaii-hero-800.webp 800w, {CDN}hawaii-hero-1400.webp 1400w', alt: 'Hawaii family reviewing paperwork with their agent outside their new home' }};
function decide(hi) {{
  var v, label;
  if (V.returning) {{
    v = {{ eyebrow: hi ? 'Aloha, welcome back' : 'Welcome back', h1: 'Ready to pick up where you left off?', dag: false,
          sub: 'Your savings are still waiting. Getting pre-approved takes just a few minutes.',
          cta: {{ text: 'Continue my approval', href: '{A}?src=buy_hero_returning' + (hi ? '_hi' : '') }} }};
    label = 'returning';
  }} else if (hi) {{
    v = {{ eyebrow: 'Serving Hawaii homebuyers', h1: 'Buy your Hawaii home and save $1,000s on your mortgage.', dag: true,
          sub: 'Island prices are high enough. Skip the retail markup and keep more of your money with a loan expert who knows the market.',
          cta: {{ text: 'Save on my Hawaii home loan', href: '{A}?src=buy_hero_hi' }} }};
    label = 'purchase';
  }} else {{ label = 'purchase'; v = {{}}; }}
  if (hi) {{ v.img = IMG_HI; v.cta2 = {{ text: 'Call {HI_PHONE}', href: 'tel:{HI_TEL}' }}; label += '_hi';
    root.querySelectorAll('[data-mx-phone]').forEach(function (a) {{ a.textContent = 'Call {HI_PHONE}'; a.href = 'tel:{HI_TEL}'; }}); }}
  MX.applyHero(root, v);
  MX.track('hero_view', {{ hero_page: 'buy', hero_label: label }});
  loadReviews(hi);
}}
MX.region(V.qs, V.override, decide);
root.querySelectorAll('.mx-hero a').forEach(function (a) {{ a.addEventListener('click', function () {{ MX.track('hero_cta_click', {{ hero_page: 'buy', cta: a.textContent.trim() }}); }}); }});

// ---- savings estimator (edit RATE_GAP when the 12-month comparison is refreshed)
var RATE_GAP = {SAV_GAP}, BASE_RATE = {SAV_BASE};
var amt = root.querySelector('#mxb-amt'), money = function (n) {{ return '$' + Math.round(n).toLocaleString('en-US'); }};
function pay(L, r) {{ var i = r / 1200; return L * i / (1 - Math.pow(1 + i, -360)); }}
function calc() {{
  var L = Number(amt.value), sv = pay(L, BASE_RATE) - pay(L, BASE_RATE - RATE_GAP);
  root.querySelector('#mxb-amt-out').textContent = money(L); amt.setAttribute('aria-valuetext', money(L));
  amt.style.setProperty('--p', ((L - amt.min) / (amt.max - amt.min) * 100) + '%');
  root.querySelector('#mxb-sav-m').textContent = money(sv);
  [1, 5, 10, 30].forEach(function (y) {{
    root.querySelector('[data-y="' + y + '"]').textContent = money(sv * 12 * y);
    root.querySelector('[data-yb="' + y + '"]').style.height = Math.max(4, y / 30 * 100) + '%';
  }});
  root.querySelector('#mxb-sav-cta').href = '{A}?src=buy_savings&loan_amount=' + L;
}}
amt.addEventListener('input', calc); calc();
var savTracked = false;
amt.addEventListener('change', function () {{ if (!savTracked) {{ savTracked = true; MX.track('savings_calc_use', {{ loan_amount: Number(amt.value) }}); }} }});
root.querySelector('#mxb-sav-cta').addEventListener('click', function () {{ MX.track('savings_cta_click', {{ loan_amount: Number(amt.value) }}); }});

// ---- tabs
var tabs = [].slice.call(root.querySelectorAll('.mx-tab'));
function sel(t) {{ tabs.forEach(function (x) {{ var on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
  document.getElementById(x.getAttribute('aria-controls')).hidden = !on; }}); }}
tabs.forEach(function (t, i) {{
  t.addEventListener('click', function () {{ sel(t); }});
  t.addEventListener('keydown', function (e) {{ var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
    if (d) {{ var n = tabs[(i + d + tabs.length) % tabs.length]; sel(n); n.focus(); e.preventDefault(); }} }});
}});

// ---- timeline line fills when scrolled into view
var tr = root.querySelector('.mx-track');
if ('IntersectionObserver' in window) {{ var io = new IntersectionObserver(function (es) {{ es.forEach(function (e) {{ if (e.isIntersecting) {{ tr.classList.add('is-in'); io.disconnect(); }} }}); }}, {{ threshold: .4 }}); io.observe(tr); }}
else tr.classList.add('is-in');

// ---- Review library: rotates which reviews show on each visit, filtered by location.
// Library lives in the repo (website/reviews.json); edit it there, no Lofty change needed.
// Hawaii visitors see only reviews tagged "HI" (falls back to everyone's reviews if none exist yet).
var GLOGO = 'https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@39110a3/google_logo.png', glogoOk = null;
function swapLogos() {{
  var go = function () {{ root.querySelectorAll('[data-glogo]').forEach(function (el) {{
    if (el.querySelector('img')) return; var im = new Image(); im.src = GLOGO; im.alt = 'Google'; im.width = 20; im.height = 20; el.textContent = ''; el.appendChild(im); }}); }};
  if (glogoOk === true) return go();
  if (glogoOk === false) return;
  var t = new Image(); t.onload = function () {{ glogoOk = true; go(); }}; t.onerror = function () {{ glogoOk = false; }}; t.src = GLOGO;
}}
swapLogos();
function loadReviews(hi) {{
  fetch(window.MX_REVIEWS_URL || '{CDN_MAIN}reviews.json').then(function (r) {{ return r.json(); }}).then(function (d) {{
    var sec = root.querySelector('#mxb-reviews');
    if (d.rating) {{ var n = sec.querySelector('[data-rv="rating"]'); n.textContent = Number(d.rating).toFixed(1); n.hidden = false; }}
    if (d.count) sec.querySelector('[data-rv="count"]').textContent = d.count + ' reviews on Google';
    if (d.url) sec.querySelector('[data-rv="link"]').href = d.url;
    var all = (d.reviews || []).filter(function (x) {{ return x.active !== false && (x.rating || 5) >= 4 && x.text; }});
    var isHI = function (x) {{ return String(x.location || '').toUpperCase() === 'HI'; }};
    var pool = all.filter(function (x) {{ return hi ? isHI(x) : !isHI(x); }});
    if (!pool.length) pool = all.filter(function (x) {{ return !isHI(x); }});
    if (!pool.length) return;
    // shuffle, then prefer reviews this visitor hasn't just seen
    for (var i = pool.length - 1; i > 0; i--) {{ var j = Math.floor(Math.random() * (i + 1)), t = pool[i]; pool[i] = pool[j]; pool[j] = t; }}
    var seen = (MX.store.get('mx_rev_seen') || '').split('|');
    pool.sort(function (a, b) {{ return (seen.indexOf(a.author) > -1) - (seen.indexOf(b.author) > -1); }});
    var list = pool.slice(0, 3);
    MX.store.set('mx_rev_seen', list.map(function (x) {{ return x.author; }}).join('|'));
    var box = sec.querySelector('[data-rv="list"]'); box.textContent = '';
    list.forEach(function (x) {{
      var f = document.createElement('figure'); f.className = 'mx-rev';
      f.innerHTML = '<div class="mx-rev-top"><span class="mx-stars" role="img"></span><span class="mx-rev-src"></span></div><blockquote></blockquote><figcaption><span class="mx-av" aria-hidden="true"></span><span></span></figcaption>';
      var r = Math.max(1, Math.min(5, Math.round(x.rating || 5)));
      f.querySelector('.mx-stars').textContent = '★★★★★'.slice(0, r); f.querySelector('.mx-stars').setAttribute('aria-label', r + ' out of 5 stars');
      f.querySelector('.mx-rev-src').textContent = x.source || 'Google'; f.querySelector('.mx-rev-src').setAttribute('data-glogo', '');
      var t = String(x.text); f.querySelector('blockquote').textContent = '“' + (t.length > 260 ? t.slice(0, 257).replace(/\\s+\\S*$/, '') + '…' : t) + '”';
      var a = String(x.author || 'Google user'), av = f.querySelector('.mx-av'); av.textContent = a.charAt(0); f.querySelector('figcaption span:last-child').textContent = a;
      if (x.photo && /^https:\\/\\/lh3\\.googleusercontent\\.com\\//.test(x.photo)) {{
        var im = new Image(); im.alt = ''; im.width = 40; im.height = 40; im.decoding = 'async'; im.referrerPolicy = 'no-referrer';
        im.onload = function () {{ av.textContent = ''; av.appendChild(im); av.classList.add('has-photo'); }};
        im.src = x.photo;
      }}
      box.appendChild(f);
    }});
    swapLogos();
    MX.track('reviews_view', {{ review_pool: hi ? 'HI' : 'general', reviews_shown: list.length }});
  }}).catch(function () {{}});
}}
"""

DESC = "Buy with Moxie's Ultimate Buyer Advantage: same-day preapproval, lock your rate up to 360 days, and clear to close in 21 days or less."
graph = [ORG] + webpage("/buy", "Get Preapproved to Buy a Home | Moxie Mortgage", DESC, "Buy a home") + [
  {"@type": "Service", "@id": SITE + "/buy#service", "name": "Home purchase mortgage", "serviceType": "Mortgage loan",
   "provider": {"@id": SITE + "/#org"}, "areaServed": {"@type": "Country", "name": "United States"},
   "description": "Wholesale-priced home purchase loans with same-day preapproval, rate locks up to 360 days, and clear to close in 21 days or less."},
  {"@type": "HowTo", "name": "How to buy a home with Moxie Mortgage", "step": [
    {"@type": "HowToStep", "position": 1, "name": "Get approved the same day", "text": "Apply online in about 10 minutes and receive a preapproval decision within 24 hours."},
    {"@type": "HowToStep", "position": 2, "name": "Lock your rate and shop", "text": "Lock your rate for up to 360 days while you shop for your home."},
    {"@type": "HowToStep", "position": 3, "name": "Clear to close", "text": "Close in 21 days or less from receipt of your executed purchase contract."}]},
  faq_schema(FAQ)]

open('/home/claude/build/out/moxie-buy-embed.html', 'w', encoding='utf-8').write(
    wrap('mx-buy', body, script, jsonld(graph), 'BUY PAGE (/buy)'))
print('buy ok')

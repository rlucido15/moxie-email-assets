"""About page embed (/about), built from the approved About.dc.html design."""
import sys, re
sys.path.insert(0, '/home/claude/work')
import buy, home
from common import *
from optimize import optimize
from calc_copy import ABOUT as C

A = APPLY
MAP = "https://cdn.lofty.com/image/fs/304384915757294/website/78760/cmsbuild/"
MAP_SRCSET = f"{MAP}w480_202578_d17e8ff5c0ff4356-png.webp 480w, {MAP}w800_202578_d17e8ff5c0ff4356-png.webp 800w, {MAP}202578_d17e8ff5c0ff4356.png 1870w"
# Founder headshot: set HEADSHOT to an image URL once the photo is in the repo; initials show until then.
HEADSHOT = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@25d214c/website/robert-lucido-headshot-400.jpg"
HS = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@25d214c/website/robert-lucido-headshot-"

FAQ = [
 ("Who owns Moxie Mortgage?", "Moxie Mortgage is a full-service lending division of NEXA Lending, NMLS #1660690."),
 ("Who founded Moxie Mortgage?", "Robert Lucido Jr founded Moxie Mortgage after spending over seven years helping lead one of the largest real estate teams in the country."),
 ("Where does Moxie Mortgage lend?", "Moxie serves clients across 51 states and U.S. territories."),
 ("What kind of lender is Moxie Mortgage?", "Moxie is a nationwide correspondent lender. It combines the control and organization of a direct lender with the flexibility and product depth of the broker channel, with access to over 300 investors at wholesale pricing."),
]
REVIEWS = [
 ("Morgan West", "Robert and team did amazing! As a first-time homebuyer, each step of the way I was met with knowledge, quick responses, questions answered and an accurate timeline to make sure I would close in a timely manner."),
 ("Stefanie Olson", "Robert at Moxie Mortgage was incredible! He went above and beyond, pulling out all the stops to make sure our deal got done. He was responsive, solution-oriented, and truly fought for us every step of the way."),
 ("Arpit P", "Working with Calvin and the team at Moxie Mortgage was an absolute pleasure from start to finish. Calvin made what is usually a stressful process completely seamless."),
]
LOANS = ["Conventional", "FHA", "VA", "USDA", "Non-traditional programs"]

avatar = (f'<img class="mxa-av" src="{HS}128.webp" srcset="{HS}128.webp 128w, {HS}256.webp 256w" sizes="64px" alt="Robert Lucido Jr, founder of Moxie Mortgage" width="64" height="64" loading="lazy" decoding="async">'
          if HEADSHOT else '<span class="mxa-av" aria-hidden="true">RL</span>')

ABOUT_CSS = r"""
.mxa-hero{padding:88px 0 96px}
.mxa-hero .mx-wrap{display:flex;flex-wrap:wrap;gap:56px;align-items:center}
.mxa-hero-copy{flex:1 1 520px;min-width:0}
.mxa-hero .mx-h1{font-size:clamp(42px,5.4vw,66px);line-height:1.02;color:#fff}
.mxa-wm{display:inline-block;white-space:nowrap;padding-bottom:.16em;background:linear-gradient(var(--orange),var(--orange)) left bottom/100% 5px no-repeat}
.mxa-wm picture{display:inline}
.mxp .mxa-wm img{display:inline-block;height:.58em;width:auto;vertical-align:baseline;margin-right:.03em}
.mx-sr{position:absolute !important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.mxa-hero .mx-lede{color:#D3E3EC;max-width:600px;margin-top:24px !important}
.mxa-hero .mx-btns{margin-top:32px}
.mxa-def{flex:1 1 380px;min-width:0;margin:0;background:#fff;color:var(--navy);border-radius:24px;padding:36px 36px 32px;box-shadow:0 30px 60px rgba(2,2,21,.35)}
.mxa-def dt{font-size:44px;font-weight:800;letter-spacing:-.02em;line-height:1}
.mxa-def dd{margin:10px 0 0;color:var(--muted)}
.mxa-def .mxa-traits{margin-top:22px;padding-top:22px;border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.mxa-traits span{background:#E3F5F9;color:var(--navy);border-radius:12px;padding:12px 14px;font-weight:700}
.mxa-split{display:flex;flex-wrap:wrap;gap:56px;align-items:center}
.mxa-split>div{flex:1 1 440px;min-width:0}
.mxa-split .mxa-map{flex-basis:520px}
.mxa-split p.mx-speak{font-size:19px;margin-top:18px !important}
.mxa-stats{margin-top:32px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.mxa-stats>div{border:1px solid var(--line);border-radius:18px;padding:20px 22px}
.mxa-stats dt{font-size:15px;color:var(--muted)}
.mxa-stats dd{margin:4px 0 0;font-size:38px;font-weight:800;line-height:1.1}
.mxa-map img{width:100%;aspect-ratio:1870/1445;height:auto}
.mxa-mission{display:flex;flex-wrap:wrap;gap:64px;align-items:flex-start}
.mxa-mission-l{flex:1 1 360px;min-width:0}
@media (min-width:1000px){.mxa-mission-l{position:sticky;top:96px}}
.mxa-mission-r{flex:1 1 560px;min-width:0;font-size:18px;line-height:1.65}
.mxa-mission-r p+p{margin-top:18px !important}
.mxa-mission-r h3{margin-top:40px !important;font-size:24px;line-height:1.25}
.mxa-mission-r h3+p{margin-top:12px !important}
.mxp .mxa-quote{margin-top:32px !important;padding:30px !important;background:var(--navy);color:#fff;border-radius:22px;padding:30px}
.mxa-quote blockquote{font-size:22px;line-height:1.4;font-weight:600}
.mxa-quote figcaption{margin-top:22px;display:flex;align-items:center;gap:14px}
.mxa-av{flex:none;width:64px;height:64px;border-radius:50%;object-fit:cover;background:linear-gradient(135deg,#1C97AE,#0D4E66);box-shadow:0 0 0 3px #fff;color:#fff;font-weight:800;font-size:22px;display:inline-flex;align-items:center;justify-content:center}
.mxa-quote strong{display:block;font-size:17px}
.mxa-quote figcaption span span{color:#7FDCEC;font-weight:600;font-size:15px}
.mxa-loans{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px !important}
.mxp.mxp .mxa-loans li{background:#fff;border:1px solid var(--line);border-radius:999px !important;padding:8px 16px !important;font-weight:700;font-size:16px}
.mxa-mission-r .mxa-strong{font-weight:700}
.mxa-faq{display:flex;flex-wrap:wrap;gap:56px;align-items:flex-start}
.mxa-faq>div:first-child{flex:1 1 340px;min-width:0}
.mxa-faq>div:last-child{flex:1 1 600px;min-width:0}
.mxa-faq .mx-faq details{border-color:var(--line)}
.mxa-faq .mx-faq summary h3{font-size:18px}
.mxa-cta{padding:0 0 72px}
"""

PROOF_CSS = "\n".join(l for l in home.HOME_CSS.splitlines() if 'mxh-proof' in l or 'mxh-grad' in l or '.mxh-proof-s>span' in l)

stats = [("States and territories", "51"), ("Investors competing for your loan", "300+"), ("Loan products", "100s"), ("Average to final approval", "12 days")]

body = f"""
<style>{buy.EXTRA_CSS.strip()}{PROOF_CSS}{ABOUT_CSS.strip()}</style>
<section class="mx-dark mxa-hero" aria-labelledby="mxa-h1">
  <div class="mx-wrap">
    <div class="mxa-hero-copy">
      <p class="mx-eyebrow">About Moxie Mortgage</p>
      <h1 id="mxa-h1" class="mx-h1">Own a home <br>with <span class="mxa-wm"><span class="mx-sr">moxie</span><picture><source type="image/webp" srcset="https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@1938a7a/website/moxie-wordmark-white-160h.webp"><img src="https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@1938a7a/website/moxie-wordmark-white-160h.png" alt="" width="736" height="160" fetchpriority="high" decoding="async"></picture>.</span></h1>
      <p class="mx-lede mx-speak">Moxie Mortgage is a full-service lending division of NEXA Lending. We proudly serve clients across 51 states and U.S. territories, helping property owners save $1,000s over the life of their loan.</p>
      <div class="mx-btns">
        <a class="mx-btn mx-btn-p" href="{A}?src=about_hero">Get approved now</a>
        <a class="mx-btn mx-btn-w" data-mx="call" href="/contact">Talk to a loan expert</a>
      </div>
    </div>
    <dl class="mxa-def" aria-label="Definition of moxie">
      <dt>mox·ie</dt>
      <dd><em>noun</em> &nbsp;·&nbsp; /ˈmäk-sē/</dd>
      <dd class="mxa-traits"><span>Energy</span><span>Confidence</span><span>Determination</span><span>Know-how</span></dd>
    </dl>
  </div>
</section>

<section class="mx-sec" aria-labelledby="mxa-cov">
  <div class="mx-wrap mxa-split">
    <div>
      <p class="mx-eyebrow">Nationwide, wholesale pricing</p>
      <h2 id="mxa-cov" class="mx-h2">No middlemen. The savings go to you.</h2>
      <p class="mx-speak">With access to 100s of loan products at wholesale pricing, we eliminate unnecessary middlemen and pass the savings directly to you.</p>
      <dl class="mxa-stats">{''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in stats)}</dl>
    </div>
    <div class="mxa-map">
      <img src="{MAP}w800_202578_d17e8ff5c0ff4356-png.webp" srcset="{MAP_SRCSET}" sizes="(max-width: 900px) 92vw, 560px" width="1870" height="1445" alt="Map of the United States showing Moxie Mortgage's nationwide lending coverage" loading="lazy" decoding="async">
    </div>
  </div>
</section>

<section class="mx-sec mx-soft" aria-labelledby="mxa-mission">
  <div class="mx-wrap mxa-mission">
    <div class="mxa-mission-l">
      <p class="mx-eyebrow">Our mission</p>
      <h2 id="mxa-mission" class="mx-h2">Home financing that fits how people actually earn and live</h2>
      <figure class="mxa-quote">
        <blockquote>“Make home financing more accessible, more efficient, and more aligned with how people actually earn and live today.”</blockquote>
        <figcaption>{avatar}<span><strong>Robert Lucido Jr</strong><span>Founder, Moxie Mortgage</span></span></figcaption>
      </figure>
    </div>
    <div class="mxa-mission-r">
      <p>{C['mission'][0]}</p>
      <p>{C['mission'][1]}</p>
      <p class="mx-speak">{C['mission'][2]}</p>
      <h3>The best of a direct lender and a broker</h3>
      <p class="mx-speak">As a nationwide correspondent lender, Moxie combines the control and organization of a direct lender with the flexibility and product depth typically found in the broker channel. That means clients have access to the full spectrum of loan options (conventional, FHA, VA, USDA, and specialized non-traditional programs) all under one roof.</p>
      <p>Whether a borrower has straightforward W-2 income or multiple complex tax returns, Moxie delivers competitive solutions without forcing clients into a one-size-fits-all box.</p>
      <p>{C['mission'][4]}</p>
      <p class="mxa-strong">{C['mission'][5]}</p>
    </div>
  </div>
</section>

<section class="mx-sec" aria-labelledby="mxa-faq">
  <div class="mx-wrap mxa-faq">
    <div>
      <p class="mx-eyebrow">Quick facts</p>
      <h2 id="mxa-faq" class="mx-h2" style="font-size:clamp(30px,3.2vw,40px)">Moxie Mortgage at a glance</h2>
      <p class="mx-muted" style="margin-top:16px">NMLS #1660690 · AZMB 0944059<br>5559 S Sossaman Rd, Mesa, AZ 85212</p>
    </div>
    <div>{faq_details([(q, f'<p class="mx-speak">{a}</p>') for q, a in FAQ])}</div>
  </div>
</section>

<section class="mx-sec mx-soft" aria-labelledby="mxa-rev" id="mxa-reviews">
  <div class="mx-wrap">
    <div class="mx-head" style="margin-bottom:0">
      <h2 id="mxa-rev" class="mx-h2" style="max-width:640px;font-size:clamp(30px,3.2vw,40px)">What our clients say about Moxie</h2>
      <div class="mxh-proof mxh-grad">
        <div class="mxh-proof-g"><img src="{home.GLOGO}" alt="Google" width="32" height="32" loading="lazy"><span class="mx-rating-n" data-rv="rating">5.0</span><span class="mx-stars" role="img" aria-label="Rated 5 out of 5 stars on Google">★★★★★</span></div>
        <span class="mxh-proof-div" aria-hidden="true"></span>
        <a class="mxh-proof-s" href="{home.SCOTSMAN_URL}" target="_blank" rel="noopener">{home.badge(48)}<span>Scotsman Guide<br><strong>Top Originator</strong></span></a>
      </div>
    </div>
    <div class="mx-revs" data-rv="list">{''.join(buy.review(n, t) for n, t in REVIEWS)}</div>
    <p style="margin-top:24px;text-align:center"><a data-rv="link" href="https://www.google.com/search?q=Moxie+Mortgage+reviews" rel="noopener" style="font-weight:700;display:inline-flex;align-items:center;min-height:48px;padding:0 16px">Read all reviews on Google →</a></p>
  </div>
</section>

<section class="mxa-cta" aria-labelledby="mxa-cta">
  <div class="mx-wrap">
    <div class="mx-cta">
      <div style="max-width:640px"><p class="mx-eyebrow" style="color:#7FDCEC">Helping you unlock doors</p>
        <h2 id="mxa-cta" class="mx-h2" style="font-size:clamp(30px,3.2vw,42px)">One property at a time.</h2>
        <p>Licensed experts across the country are ready to guide you through the process and secure a great rate.</p></div>
      <div class="mx-btns"><a class="mx-btn mx-btn-p" href="{A}?src=about_cta">Get approved now</a><a class="mx-btn mx-btn-w" href="/contact">Get expert guidance</a></div>
    </div>
  </div>
</section>
"""

s = buy.script
rev = s[s.index('// ---- Review library'):].replace('#mxb-reviews', '#mxa-reviews')
rev = rev.replace("if (d.count) sec.querySelector('[data-rv=\"count\"]').textContent = d.count + ' reviews on Google';", "")
rev = rev.replace("if (d.rating) { var n = sec.querySelector('[data-rv=\"rating\"]'); n.textContent = Number(d.rating).toFixed(1); n.hidden = false; }",
  "if (d.rating) root.querySelectorAll('[data-rv=\"rating\"]').forEach(function (n) { n.textContent = Number(d.rating).toFixed(1); });")
assert 'reviews on Google' not in rev and "querySelectorAll('[data-rv=\"rating\"]')" in rev

script = f"""
var V = MX.visitor();
MX.region(V.qs, V.override, function (hi) {{
  if (hi) {{ var c = root.querySelector('[data-mx="call"]'); c.textContent = 'Call {HI_PHONE}'; c.href = 'tel:{HI_TEL}'; }}
  MX.track('page_view_region', {{ page: 'about', geo: hi ? 'HI' : '' }});
  loadReviews(hi);
}});
{rev}
"""

DESC = C['desc']
org = dict(ORG)
org["founder"] = {"@id": SITE + "/about#founder"}
person = {"@type": "Person", "@id": SITE + "/about#founder", "name": "Robert Lucido Jr", "jobTitle": "Founder",
          "worksFor": {"@id": SITE + "/#org"}, "description": "Founded Moxie Mortgage after over seven years helping lead one of the largest real estate teams in the country."}
if HEADSHOT:
    person["image"] = HEADSHOT
page, crumbs = webpage('/about', C['title'], DESC, 'About', {
    "@type": "AboutPage", "mainEntity": {"@id": SITE + "/#org"},
    "primaryImageOfPage": {"@type": "ImageObject", "url": MAP + "w800_202578_d17e8ff5c0ff4356-png.webp", "width": 800, "height": 618}})
graph = [org, person, page, crumbs, faq_schema(FAQ)]

html = wrap('mx-about', body, script, jsonld(graph), 'ABOUT (/about)')
html = optimize(html)
open('/home/claude/build/out/moxie-about-embed.html', 'w', encoding='utf-8').write(html)
print('about ok')

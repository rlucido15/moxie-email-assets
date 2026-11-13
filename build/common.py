import os
"""Shared pieces for the Moxie Lofty embeds."""
import json

CDN = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@7c56298/website/"
CDN_M = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@f1af2af/website/"  # 480/640 mobile hero sizes
SITE = "https://moxiemortgage.com"
APPLY = "https://apply.moxiemortgage.com/"
PHONE = "480.660.2518"
PHONE_TEL = "+14806602518"
HI_PHONE = "808.818.5618"
HI_TEL = "+18088185618"

FONTBASE = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@326b42d/website/fonts/"
FONT_CSS = (
  "@font-face{font-family:MoxieBarlow;font-style:normal;font-weight:400;font-display:swap;src:url(" + FONTBASE + "barlow-latin-400-normal.woff2) format('woff2')}"
  "@font-face{font-family:MoxieBarlow;font-style:normal;font-weight:500;font-display:swap;src:url(https://cdn.chime.me/doc/fs/upload/2024124/14/c202c01f-272d-4423-9fd7-72c91e452881/Barlow-Medium.ttf) format('truetype'),url(" + FONTBASE + "barlow-latin-600-normal.woff2) format('woff2')}"
  "@font-face{font-family:MoxieBarlow;font-style:normal;font-weight:600;font-display:swap;src:url(" + FONTBASE + "barlow-latin-600-normal.woff2) format('woff2')}"
  "@font-face{font-family:MoxieBarlow;font-style:normal;font-weight:700;font-display:swap;src:url(https://cdn.chime.me/doc/fs/upload/2024124/14/05cdcc97-1e84-4a7f-ad8a-f81dbe379c1e/Barlow-Bold.ttf) format('truetype'),url(" + FONTBASE + "barlow-latin-700-normal.woff2) format('woff2')}"
  "@font-face{font-family:MoxieBarlow;font-style:normal;font-weight:800;font-display:swap;src:url(" + FONTBASE + "barlow-latin-800-normal.woff2) format('woff2')}"
)

# ---------------------------------------------------------------- CSS
CSS = r"""
.mxp{--navy:#0E2A47;--blue:#1C97AE;--bt:#127C8F;--orange:#F46744;--muted:#4A5868;--line:#DCE6EB;--soft:#F4F8FA;
  font-family:MoxieBarlow,Barlow,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--navy);font-size:17px;line-height:1.55;
  -webkit-font-smoothing:antialiased;text-align:left;box-sizing:border-box;width:100%}
.mxp *,.mxp *::before,.mxp *::after{box-sizing:border-box}
.mxp h1,.mxp h2,.mxp h3,.mxp p,.mxp ul,.mxp ol,.mxp figure,.mxp blockquote{margin:0;padding:0;font-family:inherit;text-transform:none;letter-spacing:normal}
.mxp h1,.mxp h2,.mxp h3{color:inherit;text-wrap:balance}
.mxp p{text-wrap:pretty}
.mxp ul,.mxp ol{list-style:none !important;padding:0 !important;margin:0}
.mxp.mxp li{list-style:none !important;margin:0 !important;padding:0 !important;background-image:none !important;text-indent:0 !important}
.mxp li::before{content:none !important;display:none !important}
.mxp.mxp .mx-ans li{list-style:disc !important;margin:0 0 4px 22px !important}
.mxp.mxp .mx-ans ol li,.mxp.mxp .mx-box ol li{list-style:decimal !important;margin-left:22px !important}
.mxp [hidden]{display:none !important}
.mxp img{max-width:100%;height:auto;display:block}
.mxp a{color:var(--bt);text-decoration:none}
.mxp a:hover{color:#0F5F6E}
.mxp a:focus-visible,.mxp button:focus-visible,.mxp summary:focus-visible,.mxp input:focus-visible{outline:3px solid var(--blue);outline-offset:2px}
.mx-wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.mx-sec{padding:88px 0}
.mx-soft{background:var(--soft)}
.mx-eyebrow{font-weight:700;letter-spacing:.14em !important;text-transform:uppercase !important;font-size:14px;color:var(--bt);margin-bottom:12px !important}
.mx-h1{font-size:clamp(38px,5vw,60px);line-height:1.05;font-weight:800;letter-spacing:-.02em !important}
.mx-h2{font-size:clamp(30px,3.4vw,44px);line-height:1.1;font-weight:800;letter-spacing:-.015em !important}
.mx-lede{font-size:20px;color:var(--muted);max-width:580px;margin-top:20px !important}
.mx-muted{color:var(--muted)}
.mx-dag{font-weight:400;font-size:.5em;vertical-align:super;line-height:0;margin-left:1px}
.mx-h1 .mx-dag{font-size:16px;vertical-align:top;position:relative;top:.5em;margin-left:2px}
.mx-btns{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.mxp .mx-btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:13px 24px;border-radius:12px;font-weight:700;font-size:17px;line-height:1.2;transition:background .15s,color .15s;border:2px solid transparent;cursor:pointer;text-align:center}
.mxp .mx-btn-p{background:var(--orange);color:var(--navy)}
.mxp .mx-btn-p:hover{background:#ff7a59;color:var(--navy)}
.mxp .mx-btn-o{border-color:var(--navy);color:var(--navy)}
.mxp .mx-btn-o:hover{background:var(--navy);color:#fff}
.mxp .mx-btn-w{border-color:#fff;color:#fff}
.mxp .mx-btn-w:hover{background:#fff;color:var(--navy)}
.mx-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.mx-card{background:#fff;border:1px solid var(--line);border-radius:20px;padding:28px;transition:transform .15s,border-color .15s;display:flex;flex-direction:column;gap:10px}
.mx-card:hover{border-color:var(--blue);transform:translateY(-2px)}
.mx-card h3{font-size:22px;line-height:1.2;font-weight:700}
.mx-card p{color:var(--muted);font-size:16px}
.mx-ico{width:52px;height:52px;border-radius:14px;background:var(--navy);color:var(--blue);display:inline-flex;align-items:center;justify-content:center;margin-bottom:8px}
.mx-ico svg{width:26px;height:26px}
.mx-more{margin-top:auto !important;font-weight:700}
.mx-head{display:flex;flex-wrap:wrap;gap:20px 40px;justify-content:space-between;align-items:flex-end;margin-bottom:36px}
.mx-head>p{max-width:440px}
.mx-dark{background:linear-gradient(315deg,#1C97AE 0%,#0D4E66 42%,#0E2A47 100%);color:#fff}
.mx-dark .mx-eyebrow{color:#7FDCEC}
.mx-dark p{color:#D3E3EC}
.mx-hero{padding:56px 0 64px}
.mx-hero .mx-wrap{display:flex;flex-wrap:wrap;gap:48px;align-items:center}
.mx-hero-copy{flex:1 1 470px;min-width:0}
.mx-hero-media{flex:1 1 420px;min-width:0;position:relative}
.mx-photo{border-radius:28px;padding:14px;background:linear-gradient(135deg,#1C97AE 0%,#0E2A47 100%)}
.mx-photo img{width:100%;aspect-ratio:14/9;object-fit:cover;border-radius:18px}
.mx-badge{position:absolute;left:-18px;bottom:34px;background:#fff;border-radius:16px;padding:14px 18px;box-shadow:0 18px 40px rgba(14,42,71,.18);display:flex;gap:12px;align-items:center}
.mx-badge-i{width:40px;height:40px;border-radius:50%;background:#E3F5F9;color:var(--bt);display:inline-flex;align-items:center;justify-content:center;flex:none}
.mx-stats{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:16px 48px;margin-top:36px !important}
@media (max-width:520px){.mx-stats{grid-template-columns:repeat(2,auto);gap:16px 32px}}

.mx-stats strong{display:block;font-size:28px;line-height:1.1;font-weight:800}
.mx-stats li>span{display:block;margin-top:4px;font-size:14px;color:var(--muted);white-space:nowrap}
.mx-checks{display:flex;flex-direction:column;gap:12px;margin-top:28px !important}
.mx-checks li{display:flex;gap:12px;align-items:center}
.mx-ck{width:28px;height:28px;border-radius:50%;background:#E3F5F9;color:var(--bt);display:inline-flex;align-items:center;justify-content:center;flex:none}
.mx-faq{display:flex;flex-direction:column;gap:12px}
.mx-faq details{background:#fff;border:1px solid var(--line);border-radius:16px;padding:0 24px}
.mx-faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:16px;align-items:center;padding:18px 0;min-height:60px}
.mx-faq summary::-webkit-details-marker{display:none}
.mx-faq summary h3{font-size:19px;line-height:1.35;font-weight:700}
.mx-pm{flex:none;width:32px;height:32px;border-radius:50%;background:#E3F5F9;color:var(--bt);display:inline-flex;align-items:center;justify-content:center;font-size:22px;line-height:1;transition:transform .15s}
.mx-faq details[open] .mx-pm{transform:rotate(45deg);background:var(--navy);color:#fff}
.mx-ans{padding:0 0 20px;color:#344455;font-size:16px;display:flex;flex-direction:column;gap:8px}
.mx-ans ul,.mx-ans ol{padding-left:22px !important;display:flex;flex-direction:column;gap:4px}
.mx-ans ul{list-style:disc}.mx-ans ol{list-style:decimal}
.mx-cta{background:var(--navy);color:#fff;border-radius:28px;padding:56px;display:flex;flex-wrap:wrap;gap:32px;align-items:center;justify-content:space-between}
.mx-cta p{color:#C9D6DF;margin-top:14px !important}
.mx-cta .mx-btns{margin-top:0}
.mx-fine{font-size:13px;line-height:1.6;color:var(--muted)}
.mx-rise{animation:mxRise .5s ease-out both}
.mx-d2{animation-delay:.12s}
.mx-fade{animation:mxFade .6s .1s ease-out both}
@keyframes mxRise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes mxFade{from{opacity:0}to{opacity:1}}
@media (max-width:640px){.mx-sec{padding:64px 0}.mx-cta{padding:36px 24px}.mx-badge{left:8px;bottom:16px}.mx-hero{padding:32px 0 48px}}
@media (prefers-reduced-motion:reduce){.mxp *,.mxp *::before,.mxp *::after{animation:none !important;transition:none !important}}
"""

# ---------------------------------------------------------------- JS
# Shared engine: full-bleed inside Lofty's container, visit + region detection
# (same storage keys as the homepage hero, so a visitor gets one consistent story),
# analytics events.
ENGINE = r"""
var MX = window.MX || (window.MX = {});
MX.store = {
  get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
  del: function (k) { try { localStorage.removeItem(k); } catch (e) {} },
  sget: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
  sset: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
};
MX.track = function (name, data) {
  var p = Object.assign({ event: name }, data || {});
  window.dataLayer = window.dataLayer || []; window.dataLayer.push(p);
  if (typeof window.gtag === 'function') window.gtag('event', name, data || {});
};
MX.fullBleed = function (root) {
  function fit() {
    for (var el = root.parentElement; el && el !== document.body; el = el.parentElement) {
      var cs = getComputedStyle(el);
      if (/(hidden|clip)/.test(cs.overflowX + cs.overflow)) { el.style.overflow = 'visible'; el.style.overflowX = 'visible'; }
    }
    root.style.marginLeft = '0px'; root.style.width = 'auto'; root.style.maxWidth = 'none';
    var left = root.getBoundingClientRect().left;
    root.style.width = document.documentElement.clientWidth + 'px';
    root.style.marginLeft = (-left) + 'px';
  }
  fit(); window.addEventListener('resize', fit); window.addEventListener('load', fit);
  document.documentElement.style.overflowX = 'hidden';
};
MX.visitor = function () {
  var qs = new URLSearchParams(location.search), S = MX.store;
  var override = (qs.get('hero') || '').toLowerCase();
  if (override === 'reset') { S.del('mx_visits'); S.del('mx_ab'); override = ''; }
  var visits = parseInt(S.get('mx_visits') || '0', 10);
  if (!S.sget('mx_counted')) { visits += 1; S.set('mx_visits', String(visits)); S.sset('mx_counted', '1'); }
  return { qs: qs, override: override, returning: override === 'returning' || (override !== 'default' && override !== 'hawaii' && visits > 1) };
};
MX.region = function (qs, override, cb) {
  if (override === 'hawaii' || (qs.get('geo') || '').toUpperCase() === 'HI') return cb(true);
  if (override === 'default') return cb(false);
  try { if (Intl.DateTimeFormat().resolvedOptions().timeZone === 'Pacific/Honolulu') return cb(true); } catch (e) {}
  var cached = MX.store.sget('mx_region');
  if (cached !== null) return cb(/^hawaii$/i.test(cached));
  var done = false;
  var finish = function (r) { if (done) return; done = true; MX.store.sset('mx_region', r || ''); cb(/^hawaii$/i.test(r || '')); };
  setTimeout(function () { finish(''); }, 2500);
  fetch('https://get.geojs.io/v1/ip/geo.json').then(function (r) { return r.json(); })
    .then(function (d) { finish(d && d.region); })
    .catch(function () {
      fetch('https://ipapi.co/json/').then(function (r) { return r.json(); })
        .then(function (d) { finish(d && d.region); }).catch(function () { finish(''); });
    });
};
MX.applyHero = function (root, v) {
  Object.keys(v).forEach(function (k) {
    var el = root.querySelector('[data-mx="' + k + '"]');
    if (!el) return;
    if (k === 'img') { el.srcset = v.img.srcset; el.src = v.img.src; el.alt = v.img.alt; }
    else if (k === 'cta2') { el.textContent = v.cta2.text; el.href = v.cta2.href; }
    else if (k === 'cta') { el.textContent = v.cta.text; el.href = v.cta.href; }
    else if (k === 'dag') { el.hidden = !v.dag; }
    else el.textContent = v[k];
  });
};
"""

ICON = {
 'check': '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
 'check22': '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
 'trend': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg>',
 'down': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 7l6 6 4-4 8 8"/><path d="M14 17h7v-7"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
 'grid': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M17.5 14v7M14 17.5h7"/></svg>',
 'pct': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 5 5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/></svg>',
 'cash': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 10v4M18 10v4"/></svg>',
 'clock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5"/><path d="M9 2h6"/></svg>',
}

DAG = '<span class="mx-dag">†</span>'

ORG = {
  "@type": ["FinancialService", "Organization"],
  "@id": SITE + "/#org",
  "name": "Moxie Mortgage",
  "url": SITE + "/",
  "logo": CDN + "moxie-wordmark-white-640.png",
  "telephone": "+1-480-660-2518",
  "email": "hello@moxiemortgage.com",
  "address": {"@type": "PostalAddress", "streetAddress": "5559 S Sossaman Rd, Bldg 1 Ste 101",
              "addressLocality": "Mesa", "addressRegion": "AZ", "postalCode": "85212", "addressCountry": "US"},
  "areaServed": {"@type": "Country", "name": "United States"},
  "slogan": "Wholesale mortgage pricing without the retail markup",
  "award": "Scotsman Guide Top Originator",
  "knowsAbout": ["Wholesale mortgages", "Home purchase loans", "Mortgage refinancing", "Home equity lines of credit (HELOC)",
                 "FHA loans", "VA loans", "Jumbo loans", "Non-QM loans", "Mortgage rate locks"],
  "identifier": {"@type": "PropertyValue", "propertyID": "NMLS", "value": "1660690"},
  "parentOrganization": {"@type": "Organization", "name": "NEXA Lending"},
  "contactPoint": [
    {"@type": "ContactPoint", "telephone": "+1-480-660-2518", "contactType": "customer service", "areaServed": "US"},
    {"@type": "ContactPoint", "telephone": "+1-808-818-5618", "contactType": "customer service", "areaServed": "US-HI", "email": "aloha@moxiemortgage.com"}
  ]
}


def jsonld(graph):
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'


def webpage(path, name, desc, crumb, extra=None):
    url = SITE + path
    page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": name, "description": desc,
            "isPartOf": {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Moxie Mortgage", "publisher": {"@id": SITE + "/#org"}},
            "about": {"@id": SITE + "/#org"}, "inLanguage": "en-US",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".mx-h1", ".mx-lede", ".mx-speak"]}}
    if extra:
        page.update(extra)
    bc = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": crumb, "item": url}]}
    return [page, bc]


def faq_schema(items):
    """items: list of (q, plain_answer)."""
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def faq_details(items, open_first=True):
    """items: list of (q, answer_html)."""
    out = []
    for i, (q, a) in enumerate(items):
        o = ' open' if (open_first and i == 0) else ''
        out.append(f'<details{o}><summary><h3>{q}</h3><span class="mx-pm" aria-hidden="true">+</span></summary><div class="mx-ans">{a}</div></details>')
    return '<div class="mx-faq">' + ''.join(out) + '</div>'


def es_url(root_id):
    """CDN URL of this page's Spanish dictionary (es/build.py writes them; publish_es.sh pins the commit), or None."""
    here = os.path.dirname(os.path.abspath(__file__))
    pin = os.path.join(here, 'es', '_cdn.txt')
    if not (os.path.exists(os.path.join(here, 'es', root_id + '.json')) and os.path.exists(pin)): return None
    return f"https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@{open(pin).read().strip()}/website/es/{root_id}.json"


def wrap(root_id, body, script, schema, title_comment):
    from i18n import I18N_JS
    es = es_url(root_id)
    es_js = (I18N_JS.strip() + '\n') if es else ''
    es_reg = f"MX.i18n.load(root, '{es}');\n" if es else ''
    script = es_reg + script
    return f"""<!--
  MOXIE MORTGAGE · {title_comment}
  Paste this whole file into ONE Lofty "Custom Code / Embed" block. See README.md for setup.
  Images load from github.com/rlucido15/moxie-email-assets via jsDelivr (pinned commit 7c56298).
-->
<link rel="preload" href="{FONTBASE}barlow-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{FONTBASE}barlow-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{FONT_CSS}{CSS.strip()}.mx-es-wait{{visibility:hidden}}</style>
<div class="mxp" id="{root_id}">
{body}
</div>
{schema}
<script>
{es_js}(function () {{
{ENGINE.strip()}
var root = document.getElementById('{root_id}');
MX.fullBleed(root);
{script.strip()}
}})();
</script>
"""

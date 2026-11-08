"""Client success hub (/client-success), built from the approved Stories.dc.html design.

Stories live in work/stories.py. To add a story: append a tuple to STORIES (newest first is fine;
the page orders by list position), rebuild with `python3 cs.py`, and paste the output into Lofty.
Stories published in Lofty after the last rebuild are picked up automatically in the browser
(auto-add), but only rebuilt ones are in the HTML that AI crawlers read.
"""
import sys, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'work'))
sys.path.insert(0, '/home/claude/work')
import home, buy
from common import *
from optimize import optimize
from stories import TAGS, STORIES, FEATURED

A = APPLY
CAT_URL = '/blog?categoryId=60326'

CS_CSS = r"""
.mxs-hero{padding:72px 0 32px}
.mxs-hero .mx-wrap{display:flex;flex-wrap:wrap;gap:32px 48px;align-items:flex-end;justify-content:space-between}
.mxs-hero-copy{flex:1 1 560px;min-width:0}
.mxs-hero .mx-lede{max-width:640px}
.mxs-feat{padding:16px 0 40px}
.mxp a.mxs-feat-card{display:flex;flex-wrap:wrap;gap:32px 48px;align-items:center;color:#fff;border-radius:28px;padding:44px 48px;background:linear-gradient(315deg,#1C97AE 0%,#0D4E66 42%,#0E2A47 100%);border:1px solid #0E2A47;transition:transform .15s}
.mxp a.mxs-feat-card:hover{transform:translateY(-2px);color:#fff}
.mxs-feat-stat{flex:none;text-align:center}
.mxs-feat-stat strong{display:block;font-size:88px;line-height:1;font-weight:800;letter-spacing:-.03em}
.mxs-feat-stat span{color:#7FDCEC;font-weight:700}
.mxs-feat-body{flex:1 1 420px;min-width:0}
.mxs-feat-body .mx-eyebrow{color:#7FDCEC;font-size:13px;margin-bottom:10px !important}
.mxs-feat-body h2{font-size:clamp(28px,3vw,38px);line-height:1.1;font-weight:800}
.mxs-feat-body p{margin-top:12px !important;color:#D3E3EC;font-size:18px}
.mxs-feat-body .mxs-go{display:inline-block;margin-top:18px;font-weight:700;color:var(--orange)}
@media (max-width:640px){.mxp a.mxs-feat-card{padding:32px 24px}.mxs-feat-stat strong{font-size:64px}}
.mxs-list{padding:24px 0 88px}
.mxs-list>.mx-wrap>h2{font-size:clamp(26px,2.6vw,32px);line-height:1.15;font-weight:800;margin-bottom:18px !important}
.mxs-chips{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:28px}
.mxp .mxs-chip{min-height:44px;padding:9px 18px;border-radius:999px;font-weight:600;font-size:15px;line-height:1.2;font-family:inherit;cursor:pointer;background:#fff;color:var(--navy);border:1px solid #B9C8D2}
.mxp .mxs-chip:hover{border-color:var(--navy)}
.mxp .mxs-chip[aria-pressed="true"]{background:var(--navy);color:#fff;border-color:var(--navy)}
.mxs-count{color:var(--muted);font-size:15px;font-weight:600;margin-bottom:18px !important}
.mxs-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:20px}
.mxp.mxp .mxs-grid>li{display:flex !important}
.mxp a.mxs-card{flex:1;border:1px solid var(--line);border-radius:22px;padding:26px;color:var(--navy);display:flex;flex-direction:column;gap:12px;background:#fff;transition:transform .15s,border-color .15s}
.mxp a.mxs-card:hover{border-color:var(--blue);transform:translateY(-2px);color:var(--navy)}
.mxs-top{display:flex;align-items:center;justify-content:space-between;gap:12px}
.mxs-who{display:flex;align-items:center;gap:10px;font-weight:700}
.mxs-av{width:40px;height:40px;border-radius:50%;background:var(--navy);color:#fff;display:inline-flex;align-items:center;justify-content:center;flex:none}
.mxs-out{background:#E3F5F9;color:#0F5F6E;font-weight:700;font-size:13px;padding:5px 11px;border-radius:999px;white-space:nowrap}
.mxs-out.mxs-new{background:#FDE6DF;color:#9A3412}
.mxs-card h3{margin-top:4px !important;font-size:21px;line-height:1.25;font-weight:700}
.mxs-card p{color:var(--muted);font-size:16px}
.mxs-meta{margin-top:auto !important;padding-top:6px;display:flex;justify-content:space-between;align-items:center;gap:12px;font-size:14px}
.mxs-meta span:first-child{color:var(--muted)}
.mxs-meta span:last-child{font-weight:700;color:var(--bt);white-space:nowrap}
.mxs-you .mx-wrap{display:flex;flex-wrap:wrap;gap:32px 56px;align-items:center}
.mxs-you .mx-wrap>div:first-child{flex:1 1 480px;min-width:0}
.mxs-you p{margin-top:14px !important;font-size:19px;color:var(--muted)}
.mxs-you .mx-btns{margin-top:0}
.mxs-cta{padding:80px 0 72px}
"""

PROOF_CSS = "\n".join(l for l in home.HOME_CSS.splitlines() if 'mxh-proof' in l or 'mxh-grad' in l)


def card(s, extra=''):
    slug, title, who, where, summ, tags, out = s
    return (f'<li data-tags="{" ".join(tags)}"{extra}><a class="mxs-card" href="/blog/{slug}">'
            f'<div class="mxs-top"><span class="mxs-who"><span class="mxs-av" aria-hidden="true">{who[0]}</span>{who}</span><span class="mxs-out">{out}</span></div>'
            f'<h3>{title}</h3><p>{summ}</p>'
            f'<div class="mxs-meta"><span>{where}</span><span>Read the story →</span></div></a></li>')


def build():
    feat = next(s for s in STORIES if s[0] == FEATURED['slug'])
    counts = {t: (len(STORIES) if t == 'all' else sum(1 for s in STORIES if t in s[5])) for t, _ in TAGS}
    chips = ''.join(f'<button type="button" class="mxs-chip" data-f="{t}" aria-pressed="{"true" if t == "all" else "false"}">{label} (<span data-n="{t}">{counts[t]}</span>)</button>' for t, label in TAGS)
    body = f"""
<style>{buy.EXTRA_CSS.strip()}{PROOF_CSS}{CS_CSS.strip()}</style>
<section class="mxs-hero" aria-labelledby="mxs-h1">
  <div class="mx-wrap">
    <div class="mxs-hero-copy">
      <p class="mx-eyebrow">Real-world case studies of homeownership</p>
      <h1 id="mxs-h1" class="mx-h1">Client success stories</h1>
      <p class="mx-lede mx-speak">From “un-approvable” to “closed,” these stories offer the roadmap for your own journey.</p>
    </div>
    <div class="mxh-proof mxh-grad">
      <div class="mxh-proof-g"><img src="{home.GLOGO}" alt="Google" width="32" height="32"><span class="mx-rating-n">5.0</span><span class="mx-stars" role="img" aria-label="Rated 5 out of 5 stars on Google">★★★★★</span></div>
      <span class="mxh-proof-div" aria-hidden="true"></span>
      <a class="mxh-proof-s" href="{home.SCOTSMAN_URL}" target="_blank" rel="noopener">{home.badge(48, eager=True)}<span>Scotsman Guide<br><strong>Top Originator</strong></span></a>
    </div>
  </div>
</section>
<section class="mxs-feat" aria-label="Featured story">
  <div class="mx-wrap">
    <a class="mxs-feat-card" href="/blog/{feat[0]}">
      <div class="mxs-feat-stat"><strong>{FEATURED['stat']}</strong><span>{FEATURED['stat_label']}</span></div>
      <div class="mxs-feat-body">
        <p class="mx-eyebrow">Featured story{' · ' + feat[3] if feat[3] else ''}</p>
        <h2>{feat[1]}</h2>
        <p>{feat[4]}</p>
        <span class="mxs-go">Read {feat[2]}’s story →</span>
      </div>
    </a>
  </div>
</section>
<section class="mxs-list" aria-labelledby="mxs-all">
  <div class="mx-wrap">
    <h2 id="mxs-all">Find a story like yours</h2>
    <div class="mxs-chips" role="group" aria-label="Filter stories by situation">{chips}</div>
    <p class="mxs-count" aria-live="polite"><span data-count>{len(STORIES)}</span> stories</p>
    <ul class="mxs-grid">{''.join(card(s) for s in STORIES)}</ul>
  </div>
</section>
<section class="mx-sec mx-soft mxs-you" aria-labelledby="mxs-you">
  <div class="mx-wrap">
    <div>
      <h2 id="mxs-you" class="mx-h2" style="font-size:clamp(30px,3.2vw,40px)">Don’t see your situation?</h2>
      <p>Self-employed, buying before you sell, rebuilding credit, or moving across the country: with 300+ investors, there’s a good chance we’ve solved it before.</p>
    </div>
    <div class="mx-btns"><a class="mx-btn mx-btn-o" href="/products">Explore loan options</a><a class="mx-btn mx-btn-p" data-mx="call" href="/contact">Talk to a loan expert</a></div>
  </div>
</section>
<section class="mxs-cta" aria-labelledby="mxs-cta">
  <div class="mx-wrap">
    <div class="mx-cta">
      <div style="max-width:640px"><p class="mx-eyebrow" style="color:#7FDCEC">Your story could be next</p>
        <h2 id="mxs-cta" class="mx-h2" style="font-size:clamp(30px,3.2vw,42px)">Let’s write your success story.</h2>
        <p>Licensed experts across the country are ready to guide you through the process and secure a great rate.</p></div>
      <div class="mx-btns"><a class="mx-btn mx-btn-p" href="{A}?src=stories_cta">Get approved now</a><a class="mx-btn mx-btn-w" href="/contact">Get expert guidance</a></div>
    </div>
  </div>
</section>
"""
    known = json.dumps([s[0].lower() for s in STORIES])
    script = f"""
var grid = root.querySelector('.mxs-grid'), cnt = root.querySelector('[data-count]'), cur = 'all';
function apply() {{
  var n = 0;
  grid.querySelectorAll('li').forEach(function (li) {{
    var on = cur === 'all' || (' ' + li.getAttribute('data-tags') + ' ').indexOf(' ' + cur + ' ') > -1;
    li.hidden = !on; if (on) n++;
  }});
  cnt.textContent = n;
}}
root.querySelectorAll('.mxs-chip').forEach(function (b) {{
  b.addEventListener('click', function () {{
    cur = b.getAttribute('data-f');
    root.querySelectorAll('.mxs-chip').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
    apply(); MX.track('stories_filter', {{ filter: cur }});
  }});
}});

// Auto-add: stories published in Lofty after the last rebuild appear at the top until they're folded in.
var KNOWN = {known};
function esc(s) {{ var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }}
fetch('{CAT_URL}', {{ credentials: 'same-origin' }}).then(function (r) {{ return r.text(); }}).then(function (html) {{
  var doc = new DOMParser().parseFromString(html, 'text/html'), added = 0;
  var items = doc.querySelectorAll('ul.blog-list li.item');
  for (var i = items.length - 1; i >= 0; i--) {{
    var a = items[i].querySelector('a[href*="/blog/"]'); if (!a) continue;
    var slug = (a.getAttribute('href').split('/blog/')[1] || '').split(/[?#]/)[0];
    if (!slug || /moxie-minute/i.test(slug) || KNOWN.indexOf(slug.toLowerCase()) > -1) continue;
    var t = items[i].querySelector('.blog-title'), c = items[i].querySelector('.content');
    var title = (t ? t.textContent : a.getAttribute('aria-label') || '').trim(); if (!title) continue;
    var ex = (c ? c.textContent : '').replace(/\\s+/g, ' ').split('★')[0].trim();
    if (ex.length > 170) ex = ex.slice(0, 167).replace(/\\s+\\S*$/, '') + '…';
    var li = document.createElement('li'); li.setAttribute('data-tags', 'new');
    li.innerHTML = '<a class="mxs-card" href="/blog/' + encodeURIComponent(slug) + '"><div class="mxs-top"><span class="mxs-who"><span class="mxs-av" aria-hidden="true">' + esc(title.charAt(0)) + '</span>Moxie client</span><span class="mxs-out mxs-new">New story</span></div><h3>' + esc(title) + '</h3><p>' + esc(ex) + '</p><div class="mxs-meta"><span></span><span>Read the story →</span></div></a>';
    grid.insertBefore(li, grid.firstChild); KNOWN.push(slug.toLowerCase()); added++;
  }}
  if (added) {{ var all = root.querySelector('[data-n="all"]'); all.textContent = +all.textContent + added; apply(); }}
}}).catch(function () {{}});

var V = MX.visitor();
MX.region(V.qs, V.override, function (hi) {{
  if (hi) {{ var c = root.querySelector('[data-mx="call"]'); c.textContent = 'Call {HI_PHONE}'; c.href = 'tel:{HI_TEL}'; }}
}});
"""
    items = [{"@type": "ListItem", "position": i + 1, "item": {
        "@type": "Article", "headline": s[1], "url": SITE + "/blog/" + s[0], "description": s[4],
        "author": {"@type": "Organization", "@id": SITE + "/#org", "name": "Moxie Mortgage"},
        "publisher": {"@id": SITE + "/#org"}, "about": [dict(TAGS)[t] for t in s[5]]}} for i, s in enumerate(STORIES)]
    page, crumbs = webpage('/client-success', 'Client Success Stories | Moxie Mortgage',
        'Real-world homeownership case studies from Moxie Mortgage clients: first-time buyers, VA loans, self-employed borrowers, refinances, investors, Hawaii buyers, and tough files.',
        'Client success stories', {"@type": "CollectionPage", "mainEntity": {"@type": "ItemList", "numberOfItems": len(STORIES), "itemListElement": items}})
    graph = [ORG, page, crumbs]
    html = optimize(wrap('mx-stories', body, script, jsonld(graph), 'CLIENT SUCCESS (/client-success)'))
    open(os.path.join(HERE, 'out', 'moxie-client-success-embed.html'), 'w', encoding='utf-8').write(html)
    print('client success ok:', len(STORIES), 'stories')


build()

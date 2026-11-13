import json, re, html
from common import *

data = json.load(open('/home/claude/work/faq.json', encoding='utf-8'))
esc = lambda s: html.escape(s, quote=False)

def ans_html(blocks):
    out, cur, kind = [], [], None
    def flush():
        nonlocal cur, kind
        if cur: out.append(f'<{kind}>' + ''.join(f'<li>{esc(x)}</li>' for x in cur) + f'</{kind}>')
        cur, kind = [], None
    for b in blocks:
        if b['k'] == 'p':
            flush(); out.append(f'<p>{esc(b["t"])}</p>')
        else:
            if kind and kind != b['k']: flush()
            kind = b['k']; cur.append(b['t'])
    flush()
    return ''.join(out)

def ans_text(blocks):
    parts = []
    for b in blocks:
        parts.append(b['t'] if b['k'] == 'p' else '• ' + b['t'])
    return ' '.join(parts)

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

EXTRA_CSS = r"""
.mx-fhero{padding:64px 0}
@media (min-width:1024px){.mx-oneline{white-space:nowrap}}
.mx-search{position:relative;margin-top:28px;max-width:820px}
.mx-search svg{position:absolute;left:20px;top:50%;transform:translateY(-50%);pointer-events:none}
.mxp .mx-search input{width:100%;height:64px;border:0;border-radius:16px;padding:0 20px 0 56px;font-family:inherit;font-weight:500;font-size:19px;line-height:1.2;color:var(--navy);background:#fff;box-shadow:0 20px 40px rgba(14,42,71,.25);margin:0}
.mx-pop{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:18px}
.mx-pop span{font-size:14px;color:#C9D6DF;margin-right:4px}
.mxp .mx-pop button{min-height:36px;border:1px solid rgba(255,255,255,.35);background:rgba(255,255,255,.08);color:#fff;border-radius:999px;padding:6px 14px;font-family:inherit;font-weight:600;font-size:14px;line-height:1.2;cursor:pointer}
.mxp .mx-pop button:hover{background:rgba(255,255,255,.18)}
.mx-browse{display:flex;flex-wrap:wrap;gap:40px;align-items:flex-start;padding:48px 0 72px}
.mx-cats{flex:1 1 240px;max-width:300px;min-width:0}
.mx-cats-l{font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:13px;color:var(--muted);margin-bottom:12px !important}
.mx-cats ul{display:flex;flex-direction:column;gap:4px}
.mxp .mx-cat{width:100%;min-height:44px;display:flex;justify-content:space-between;align-items:center;gap:12px;border:0;border-radius:10px;padding:10px 14px;font-family:inherit;font-weight:600;font-size:16px;line-height:1.3;text-align:left;cursor:pointer;background:transparent;color:var(--navy)}
.mxp .mx-cat:hover{background:#E3F5F9}
.mxp .mx-cat[aria-pressed="true"]{background:var(--navy);color:#fff}
.mx-cat small{font-size:13px;font-weight:600;opacity:.75}
.mx-results{flex:999 1 560px;min-width:0}
.mx-bar{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;align-items:center;margin-bottom:20px}
.mx-bar p{font-weight:600;color:var(--muted)}
.mxp .mx-clear{min-height:40px;border:0;background:none;color:var(--bt);font-family:inherit;font-weight:700;font-size:15px;cursor:pointer;text-decoration:underline}
.mx-cgroup{margin-bottom:40px;scroll-margin-top:120px}
.mx-cgroup>h2{font-size:26px;line-height:1.2;font-weight:800;margin-bottom:14px !important}
.mx-cgroup .mx-faq details{border-radius:14px}
.mx-cgroup .mx-faq summary h3{font-size:18px}
.mx-empty{border:1px dashed #B9C8D2;border-radius:18px;padding:40px;text-align:center}
.mx-empty strong{display:block;font-size:22px;margin-bottom:6px}
mark.mx-hl{background:#FFE3D9;color:inherit;padding:0 2px;border-radius:3px}
"""

POP = ["Down payment", "Credit score", "Closing costs", "DSCR", "Refinance", "Rate lock"]
total = sum(len(c['items']) for c in data)

cats_html = f'<li><button type="button" class="mx-cat" data-c="all" aria-pressed="true"><span>All topics</span><small>{total}</small></button></li>' + ''.join(
    f'<li><button type="button" class="mx-cat" data-c="{slug(c["name"])}" aria-pressed="false"><span>{esc(c["name"])}</span><small>{len(c["items"])}</small></button></li>' for c in data)

groups = []
for ci, c in enumerate(data):
    det = []
    for ii, it in enumerate(c['items']):
        o = ' open' if (ci == 0 and ii == 0) else ''
        det.append(f'<details{o} id="{slug(it["q"])[:60]}"><summary><h3>{esc(it["q"])}</h3><span class="mx-pm" aria-hidden="true">+</span></summary><div class="mx-ans">{ans_html(it["blocks"])}</div></details>')
    groups.append(f'<div class="mx-cgroup" id="topic-{slug(c["name"])}" data-c="{slug(c["name"])}"><h2>{esc(c["name"])}</h2><div class="mx-faq">{"".join(det)}</div></div>')

body = f"""
<style>{EXTRA_CSS.strip()}</style>
<section class="mx-dark mx-fhero" aria-labelledby="mxf-h1">
  <div class="mx-wrap">
    <div>
      <p class="mx-eyebrow mx-rise">Own with confidence</p>
      <h1 id="mxf-h1" class="mx-h1 mx-rise">Mortgage FAQs</h1>
      <p class="mx-lede mx-rise mx-d2 mx-oneline" style="color:#D3E3EC;font-size:19px;max-width:none">Answers to common questions about getting preapproved, rates, credit, closing, and loan options.</p>
    </div>
    <form class="mx-search" role="search" onsubmit="return false">
      <label for="mxf-q" style="position:absolute;left:-9999px">Search mortgage FAQs</label>
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4A5868" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
      <input id="mxf-q" type="search" autocomplete="off" placeholder="Search {total} questions, e.g. “down payment” or “DSCR”">
    </form>
    <div class="mx-pop"><span>Popular:</span>{''.join(f'<button type="button" data-q="{p.lower()}">{p}</button>' for p in POP)}</div>
  </div>
</section>

<div class="mx-wrap mx-browse">
  <nav class="mx-cats" aria-label="FAQ topics"><p class="mx-cats-l">Topics</p><ul>{cats_html}</ul></nav>
  <div class="mx-results">
    <div class="mx-bar"><p id="mxf-sum" aria-live="polite">{total} questions across {len(data)} topics</p><button type="button" class="mx-clear" id="mxf-clear" hidden>Clear search</button></div>
    {''.join(groups)}
    <div class="mx-empty" id="mxf-empty" hidden><strong>No answers match that search yet</strong><p class="mx-muted">Ask a Moxie loan expert and we'll get back to you. <a href="/contact">Contact us</a> or call <a data-mx-phone href="tel:{PHONE_TEL}">{PHONE}</a>.</p></div>
  </div>
</div>
"""

script = f"""
var q = root.querySelector('#mxf-q'), sum = root.querySelector('#mxf-sum'), clr = root.querySelector('#mxf-clear'), empty = root.querySelector('#mxf-empty');
var groups = [].slice.call(root.querySelectorAll('.mx-cgroup'));
var cats = [].slice.call(root.querySelectorAll('.mx-cat'));
var items = [].slice.call(root.querySelectorAll('.mx-cgroup details')).map(function (d) {{
  return {{ d: d, h3: d.querySelector('h3'), q: (window.MX.i18n ? MX.i18n.en(d.querySelector('h3').textContent) : d.querySelector('h3').textContent), text: d.textContent.toLowerCase(), wasOpen: d.open }};
}});
var cat = 'all', TOTAL = {total}, NCAT = {len(data)}, timer;
function escRe(s) {{ return s.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&'); }}
function run(track) {{
  var raw = q.value.trim(), terms = raw.toLowerCase().split(/\\s+/).filter(Boolean), searching = raw.length >= 2, n = 0;
  var re = searching ? new RegExp('(' + terms.map(escRe).join('|') + ')', 'gi') : null;
  items.forEach(function (it) {{
    var inCat = cat === 'all' || it.d.parentElement.parentElement.getAttribute('data-c') === cat;
    var hit = !searching || terms.every(function (t) {{ return it.text.indexOf(t) > -1; }});
    var on = inCat && hit; it.d.hidden = !on; if (on) n++;
    it.h3.textContent = window.MX.i18n ? MX.i18n.text(it.q) : it.q;
    if (searching && on) {{ it.h3.innerHTML = it.h3.innerHTML.replace(re, '<mark class="mx-hl">$1</mark>'); it.d.open = true; }}
    else if (!searching) it.d.open = it.wasOpen;
  }});
  groups.forEach(function (g) {{ g.hidden = !g.querySelector('details:not([hidden])'); }});
  empty.hidden = n > 0; clr.hidden = !(searching || cat !== 'all');
  sum.textContent = searching ? (n + (n === 1 ? ' answer' : ' answers') + ' for “' + raw + '”')
    : (cat === 'all' ? TOTAL + ' questions across ' + NCAT + ' topics' : n + ' questions in ' + root.querySelector('.mx-cat[data-c="' + cat + '"] span').textContent);
  if (track && searching) {{ clearTimeout(timer); timer = setTimeout(function () {{ MX.track('faq_search', {{ search_term: raw, results: n }}); }}, 1200); }}
}}
q.addEventListener('input', function () {{ run(true); }});
root.querySelectorAll('.mx-pop button').forEach(function (b) {{ b.addEventListener('click', function () {{ q.value = (window.MX.i18n && MX.i18n.lang === 'es') ? b.textContent.trim().toLowerCase() : b.getAttribute('data-q'); setCat('all'); run(true); }}); }});
function setCat(c) {{ cat = c; cats.forEach(function (x) {{ x.setAttribute('aria-pressed', x.getAttribute('data-c') === c); }}); }}
cats.forEach(function (b) {{ b.addEventListener('click', function () {{ setCat(b.getAttribute('data-c')); run(false); }}); }});
clr.addEventListener('click', function () {{ q.value = ''; setCat('all'); run(false); q.focus(); }});
items.forEach(function (it) {{ it.d.addEventListener('toggle', function () {{ if (it.d.open) MX.track('faq_open', {{ question: it.q }}); }}); }});
// Spanish: the page text is swapped in place, so re-read the search index from the page when the language changes
document.addEventListener('mx:lang', function () {{ setTimeout(function () {{ items.forEach(function (it) {{ it.text = it.d.textContent.toLowerCase(); }}); run(false); }}, 0); }});
var pre = new URLSearchParams(location.search).get('q'); if (pre) {{ q.value = pre; run(false); }}
var V = MX.visitor();
MX.region(V.qs, V.override, function (hi) {{
  if (hi) root.querySelectorAll('[data-mx-phone]').forEach(function (a) {{ a.textContent = '{HI_PHONE}'; a.href = 'tel:{HI_TEL}'; }});
}});
"""

qa = [(it['q'], ans_text(it['blocks'])) for c in data for it in c['items']]
DESC = "Search 100 answers about preapproval, down payments, credit scores, closing costs, Non-QM and DSCR loans, appraisals and refinancing."
wp = webpage("/faqs", "Mortgage FAQs: Preapproval, Rates, Credit & Refinance | Moxie Mortgage", DESC, "Mortgage FAQs")
wp[0]["isPartOf"]["potentialAction"] = {"@type": "SearchAction", "target": {"@type": "EntryPoint", "urlTemplate": SITE + "/faqs?q={search_term_string}"},
                                        "query-input": "required name=search_term_string"}
fq = faq_schema(qa); fq["@id"] = SITE + "/faqs#faq"
graph = [ORG] + wp + [fq]

open('/home/claude/build/out/moxie-faqs-embed.html', 'w', encoding='utf-8').write(
    wrap('mx-faqs', body, script, jsonld(graph), 'FAQS PAGE (/faqs)'))
print('faqs ok', len(qa))

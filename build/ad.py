"""Area Director recruiting page (/area-director, replaces /bdm), built from the approved AreaDirector.dc.html design.

Source of truth: the design file on the canvas (copied to /home/claude/canvas/project/AreaDirector.dc.html).
This script lifts its <main> markup, swaps the design-tool template holes for plain JS, points images at
jsDelivr, and leaves a slot where Moxie's existing Lofty form block (the /bdm application form) is moved in,
so applications keep flowing into Lofty exactly as they do today.
"""
import re, os, html as H
from common import *
from optimize import optimize

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = '/home/claude/canvas/project/AreaDirector.dc.html'
CDN_AD = "https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@c5224bc/website/"
IMG = {
    '/_blob/2184183c16f63209083b1f848369886d': ('ad-listing-flyer.webp', 560, 684),
    '/_blob/096b0531d3c6db98ee8b90e1f2ebf9e5': ('ad-social-post.webp', 560, 560),
    '/_blob/3b018aaca4d50896a0c8bfd7904ad87c': ('ad-agent-portal.webp', 800, 451),
    '/_blob/0e04ccd625696ebe9a11ec059e3a1b14': ('ad-moxie-minute.webp', 800, 660),
}

src = open(SRC, encoding='utf-8').read()
design_css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
main = re.search(r'<main>(.*?)</main>', src, re.S).group(1)

# ---------- design CSS: keep the page-specific rules, drop globals the shared reset already covers
drop = ('body{', 'h1,h2,h3{', 'p{text-wrap', 'a{color', '@keyframes mxRise', '.mx-rise{', '@media (prefers-reduced-motion')
keep = [ln for ln in design_css.strip().split('\n') if not ln.startswith(drop)]
page_css = '\n'.join(keep)
page_css = page_css.replace('.mx-card', '.mxa-card').replace('.mx-pill', '.mxa-pill')
page_css = page_css.replace('.mx-btn-p:hover', '.mxp .mxa-btn-p:hover').replace('.mx-btn-w:hover', '.mxp .mxa-btn-w:hover')

AD_CSS = page_css + r"""
.mxp.mxp .ad-tl>li{padding:22px 24px !important}
.mxp.mxp .ad-steps>li{display:flex !important;gap:18px}
.mxp a.mxa-btn-p{color:#0E2A47}
.mxp a.mxa-btn-w{color:#fff}
.mxp .mxa-pill{font-family:inherit}
.mxp dl,.mxp dd{margin:0}
.mxp table{border-collapse:collapse}
.mxp th,.mxp td{border:0}
.mxp blockquote{border:0;quotes:none;font-style:normal}
.mxp blockquote::before,.mxp blockquote::after{content:none}
.mxp input.ad-range{border:0;padding:0;background-color:transparent}
/* the Lofty application form, moved into the apply card */
.mxa-form{flex:1 1 480px;min-width:0;background:#fff;color:#0E2A47;border-radius:24px;padding:32px;box-shadow:0 30px 60px rgba(2,2,21,.35)}
.mxa-form>h3{font-size:24px;line-height:1.2;font-weight:800}
.mxa-form>p{margin:6px 0 18px !important;color:#4A5868;font-size:15px}
.mxa-slot .md-form{padding:0 !important;margin:0 !important;background:none !important;min-height:0 !important;width:auto !important}
.mxa-slot .md-form .mask,.mxa-slot .md-form .site-title{display:none !important}
.mxa-slot .md-form-container{padding:0 !important;margin:0 !important;max-width:none !important;width:auto !important;background:none !important;box-shadow:none !important}
.mxa-slot .basic-info{display:grid !important;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 16px}
.mxa-slot .basic-info>.fullname{grid-column:1/-1}
.mxa-slot .basic-info>.singleLineTextH2jVGbA4p{grid-column:1/-1}
.mxa-slot .v-input{margin:0 !important;width:auto !important;max-width:none !important;padding:0 !important}
.mxa-slot .v-input.message{margin-top:14px !important}
.mxa-slot .label-top{display:block !important;position:static !important;transform:none !important;font:600 15px MoxieBarlow,Barlow,system-ui,sans-serif !important;color:#0E2A47 !important;margin:0 0 6px !important;opacity:1 !important;background:none !important;padding:0 !important;letter-spacing:0 !important;text-transform:none !important}
.mxa-slot input[type=text],.mxa-slot input[type=tel],.mxa-slot input[type=email],.mxa-slot textarea{width:100% !important;box-sizing:border-box !important;min-height:46px !important;border:1px solid #C9D8DF !important;border-radius:10px !important;padding:10px 12px !important;font:500 16px MoxieBarlow,Barlow,system-ui,sans-serif !important;color:#0E2A47 !important;background:#fff !important;box-shadow:none !important}
.mxa-slot textarea{min-height:92px !important;resize:vertical}
.mxa-slot input:focus,.mxa-slot textarea:focus{outline:2px solid #1C97AE !important;border-color:#1C97AE !important}
.mxa-slot .mg-error{font-size:13px !important;margin:4px 0 0 !important}
.mxa-slot .disclaimer-wrap{margin-top:16px !important}
.mxa-slot .disclaimer-content,.mxa-slot .disclaimer-content p{font-size:12.5px !important;line-height:1.45 !important;color:#4A5868 !important}
.mxa-slot .submit-content{margin-top:18px !important;padding:0 !important}
.mxa-slot .submit-box{width:100% !important;max-width:none !important}
.mxa-slot button.submit{width:100% !important;min-height:52px !important;border:0 !important;border-radius:12px !important;background:#F46744 !important;color:#0E2A47 !important;font:700 17px MoxieBarlow,Barlow,system-ui,sans-serif !important;text-transform:none !important;letter-spacing:0 !important;cursor:pointer}
.mxa-slot button.submit:hover{background:#ff7a59 !important}
.mxa-slot button.submit.submit-disabled{opacity:.6}
.mxa-fallback{display:flex;flex-direction:column;gap:12px}
.mxa-slot.has-form .mxa-fallback{display:none}
@media (max-width:560px){.mxa-slot .basic-info{grid-template-columns:1fr}.mxa-form{padding:24px}}
"""

body = main.strip()

# ---------- class renames that would otherwise collide with the shared stylesheet
body = body.replace('class="mx-card"', 'class="mxa-card"').replace('class="mx-pill"', 'class="mxa-pill"')
body = body.replace('class="mx-btn-p"', 'class="mxa-btn-p"').replace('class="mx-btn-w"', 'class="mxa-btn-w"')

# ---------- images -> jsDelivr with intrinsic size
for blob, (fn, w, h) in IMG.items():
    body = body.replace(f'src="{blob}"', f'src="{CDN_AD}{fn}" width="{w}" height="{h}" decoding="async"')
assert '/_blob/' not in body

# ---------- estimator: template holes -> static first render + data hooks
L0, A0 = 40, 500000
def short(n):
    return ('$' + (f'{n/1e6:.2f}'.rstrip('0').rstrip('.')) + 'M') if n >= 1e6 else '$' + str(round(n / 1000)) + 'K'
def usd(n): return '$' + f'{round(n):,}'
def track(v, lo, hi):
    p = f'{(v - lo) / (hi - lo) * 100:.1f}'
    return f'background:linear-gradient(90deg,#1C97AE {p}%,#DCE6EB {p}%)'
annual = L0 * A0 * 0.0025
pill_on = 'min-height:44px;border-radius:999px;padding:8px 16px;font:700 15px MoxieBarlow,Barlow,system-ui,sans-serif;cursor:pointer;border:1.5px solid #0E2A47;background:#0E2A47;color:#ffffff'
pill_off = 'min-height:44px;border-radius:999px;padding:8px 16px;font:700 15px MoxieBarlow,Barlow,system-ui,sans-serif;cursor:pointer;border:1.5px solid #C9D8DF;background:#ffffff;color:#0E2A47'
R = {
    'onClick="{{pickExample}}" aria-pressed="{{exPressed}}" style="{{exStyle}}"': f'data-ad-preset="40" aria-pressed="true" style="{pill_on}"',
    'onClick="{{pickLarge}}" aria-pressed="{{lgPressed}}" style="{{lgStyle}}"': f'data-ad-preset="80" aria-pressed="false" style="{pill_off}"',
    'value="{{loans}}" onInput="{{onLoans}}" style="{{loansTrack}}"': f'value="{L0}" style="{track(L0, 1, 250)}"',
    'value="{{loan}}" onInput="{{onLoan}}" style="{{loanTrack}}"': f'value="{A0}" style="{track(A0, 150000, 1500000)}"',
    'onClick="{{revPrev}}"': 'data-ad-rev="-1"',
    'onClick="{{revNext}}"': 'data-ad-rev="1"',
}
for a, b in R.items():
    assert body.count(a) == 1, a
    body = body.replace(a, b)
body = body.replace('>{{loans}}</output>', f' data-ad="loans">{L0}</output>')
body = body.replace('>{{loanLabel}}</output>', f' data-ad="loanLabel">{short(A0)}</output>')
body = body.replace('>{{annual}}</p>', f' data-ad="annual">{usd(annual)}</p>')
body = body.replace('>{{monthly}}</dd>', f' data-ad="monthly">{usd(annual / 12)}</dd>')
body = body.replace('>{{volume}}</dd>', f' data-ad="volume">{short(L0 * A0)}</dd>')
body = body.replace('>{{loans}} loans × {{loanLabel}} average × 0.25%</p>',
                    f'><span data-ad="loans">{L0}</span> loans × <span data-ad="loanLabel">{short(A0)}</span> average × 0.25%</p>')
assert '{{' not in body, re.findall(r'\{\{\w+\}\}', body)

# ---------- apply steps list gets a hook for the li reset
body = body.replace('<ol style="list-style: none; padding: 0; margin: 32px 0 0;', '<ol class="ad-steps" style="list-style: none; padding: 0; margin: 32px 0 0;', 1)

# ---------- the design's static form -> slot for Moxie's Lofty form block
form = re.search(r'\s*<form aria-labelledby="ad-form-h".*?</form>', body, re.S)
assert form
body = body.replace(form.group(0), f'''
      <div class="mxa-form" id="mxa-apply-card">
        <h3 id="ad-form-h">Apply to become an Area Director</h3>
        <p>We’ll review and reach out to book your onboarding call.</p>
        <div class="mxa-slot" id="mxa-form-slot">
          <div class="mxa-fallback">
            <p style="margin:0;color:#4A5868">Call us and we’ll get your application started.</p>
            <a class="mx-btn mx-btn-p" href="tel:{PHONE_TEL}">Call {PHONE}</a>
          </div>
        </div>
      </div>''', 1)

# ---------- shared footer is its own embed block
body = re.sub(r'\s*<dc-import[^>]*></dc-import>', '', body)

script = r"""
// ---- compensation estimator (0.25% of the loan amount on closed volume)
var st = { loans: 40, loan: 500000 };
var rL = root.querySelector('#ad-loans'), rA = root.querySelector('#ad-loan');
var usd = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
var short = function (n) { return n >= 1e6 ? '$' + (n / 1e6).toFixed(2).replace(/\.?0+$/, '') + 'M' : '$' + Math.round(n / 1000) + 'K'; };
var track = function (v, lo, hi) { var p = ((v - lo) / (hi - lo) * 100).toFixed(1); return 'linear-gradient(90deg,#1C97AE ' + p + '%,#DCE6EB ' + p + '%)'; };
var PON = '__PON__', POFF = '__POFF__';
function paint() {
  var annual = st.loans * st.loan * 0.0025;
  var set = function (k, v) { root.querySelectorAll('[data-ad="' + k + '"]').forEach(function (el) { el.textContent = v; }); };
  set('loans', st.loans); set('loanLabel', short(st.loan)); set('annual', usd(annual)); set('monthly', usd(annual / 12)); set('volume', short(st.loans * st.loan));
  rL.value = st.loans; rA.value = st.loan;
  rL.style.background = track(st.loans, 1, 250); rA.style.background = track(st.loan, 150000, 1500000);
  root.querySelectorAll('[data-ad-preset]').forEach(function (b) {
    var on = st.loan === 500000 && st.loans === +b.getAttribute('data-ad-preset');
    b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.style.cssText = on ? PON : POFF;
  });
}
var tracked = false;
function used(src) { if (!tracked) { tracked = true; MX.track('ad_estimator_use', { src: src }); } }
rL.addEventListener('input', function () { st.loans = +rL.value; paint(); used('slider'); });
rA.addEventListener('input', function () { st.loan = +rA.value; paint(); used('slider'); });
root.querySelectorAll('[data-ad-preset]').forEach(function (b) {
  b.addEventListener('click', function () { st.loans = +b.getAttribute('data-ad-preset'); st.loan = 500000; paint(); used('preset'); });
});

// ---- reviews: arrow buttons page the scrolling track
var trackEl = root.querySelector('.ad-rev-track');
root.querySelectorAll('[data-ad-rev]').forEach(function (b) {
  b.addEventListener('click', function () { trackEl.scrollBy({ left: +b.getAttribute('data-ad-rev') * trackEl.clientWidth, behavior: 'smooth' }); });
});

// ---- move Moxie's Lofty application form (its own block on this page) into the apply card.
// Leads keep going to Lofty exactly as before. If the form block isn't on the page, a call button shows instead.
var RELABEL = [[/buyer sales/i, 'Buyer sales, last 12 months (units)*'], [/sales \(volume\)/i, 'Sales volume, last 12 months*']];
function mountForm() {
  var slot = root.querySelector('#mxa-form-slot'); if (!slot || slot.classList.contains('has-form')) return true;
  var blocks = document.querySelectorAll('.md-form');
  for (var i = 0; i < blocks.length; i++) {
    var b = blocks[i];
    if (root.contains(b) || !b.querySelector('form')) continue;
    slot.appendChild(b); slot.classList.add('has-form');
    b.querySelectorAll('.v-input').forEach(function (v) {
      var lab = v.querySelector('.label-top'), inp = v.querySelector('input,textarea'); if (!lab || !inp) return;
      RELABEL.forEach(function (r) { if (r[0].test(lab.textContent)) { lab.textContent = r[1]; inp.placeholder = ''; } });
      if (inp.placeholder) inp.placeholder = '';
    });
    b.addEventListener('submit', function () { MX.track('ad_apply_submit', {}); }, true);
    return true;
  }
  return false;
}
if (!mountForm()) document.addEventListener('DOMContentLoaded', function () { if (!mountForm()) window.addEventListener('load', mountForm); });
root.querySelectorAll('a[href="#apply"]').forEach(function (a) { a.addEventListener('click', function () { MX.track('ad_apply_click', { src: a.textContent.trim() }); }); });
""".replace('__PON__', pill_on).replace('__POFF__', pill_off)

DESC = "Join Moxie Mortgage as an Area Director: a W-2 business development role paid 0.25% of the loan amount on closed Moxie loans in your area. No mortgage license or loan work required."
page, crumbs = webpage('/area-director', 'Area Director | Earn Mortgage Income in Your Area | Moxie Mortgage', DESC, 'Area Director')
schema = jsonld([ORG, page, crumbs])

LOFTY_KEEP = '<!-- styles the moved Lofty form: md-form mask site-title md-form-container basic-info fullname singleLineTextH2jVGbA4p v-input message label-top mg-error disclaimer-wrap disclaimer-content submit-content submit-box submit submit-disabled -->'
full = wrap('mx-ad', LOFTY_KEEP + f'\n<style>{AD_CSS}</style>\n<div class="mxa-main">\n{body}\n</div>', script, schema, 'AREA DIRECTOR (/area-director, replaces /bdm)')
# the design font is Barlow; the shared embeds self-host it as MoxieBarlow
full = full.replace('font-family: Barlow, system-ui, sans-serif', 'font-family: MoxieBarlow, Barlow, system-ui, sans-serif')
full = full.replace('font:700 26px/1 Barlow,system-ui', 'font:700 26px/1 MoxieBarlow,Barlow,system-ui').replace('font:800 16px/1 Barlow,system-ui', 'font:800 16px/1 MoxieBarlow,Barlow,system-ui')
full = full.replace('font:500 16px Barlow,system-ui', 'font:500 16px MoxieBarlow,Barlow,system-ui').replace('font:700 14px Barlow,system-ui', 'font:700 14px MoxieBarlow,Barlow,system-ui')
html_out = optimize(full)
out = os.path.join(HERE, 'out', 'moxie-area-director-embed.html')
open(out, 'w', encoding='utf-8').write(html_out)
print('area director ok', len(html_out), 'bytes')

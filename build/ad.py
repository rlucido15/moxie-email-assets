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
# Google Apps Script web app that holds the Lofty API key and creates the lead (see ad-relay.gs). Paste its /exec URL here.
# Existing shared "Lofty API" intake Apps Script (same deployment the rent-vs-buy calculator uses).
# The secret is only that script's light spam gate; the Lofty API key stays server-side in the script.
AD_ENDPOINT = os.environ.get('AD_ENDPOINT', 'https://script.google.com/macros/s/AKfycby2DNAgTJREXdoEPWPobju74TheeTS5ne4LdXR16cVG9jW7HfcwCJchxGgthsM47Ndj/exec')
AD_SECRET = os.environ.get('AD_SECRET', 'joasidfjoaiewlkejwlkessddfsqwe')
SRC = '/home/claude/canvas/project/AreaDirector.dc.html'
if not os.path.exists(SRC):
    SRC = '/home/claude/work/AreaDirector.dc.html'  # snapshot kept in build/work/
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
# stat tiles: one-line labels, values on one line and level across the two tiles
_tile_old = '<div style="background: #E3F5F9; border-radius: 14px; padding: 16px 18px"><dt style="font-size: 14px; color: #4A5868">'
_tile_new = '<div style="background: #E3F5F9; border-radius: 14px; padding: 16px 18px; display: flex; flex-direction: column; justify-content: space-between; gap: 4px"><dt style="font-size: 14px; color: #4A5868">'
assert main.count(_tile_old) == 2
main = main.replace(_tile_old, _tile_new).replace('>Onboarding call</dt>', '>Onboarding</dt>')
main = main.replace('font-size: 30px; font-weight: 800; line-height: 1.1">$0</dd>', 'font-size: 30px; font-weight: 800; line-height: 1.1; white-space: nowrap">$0</dd>')
main = main.replace('font-size: 30px; font-weight: 800; line-height: 1.1">20 min</dd>', 'font-size: 30px; font-weight: 800; line-height: 1.1; white-space: nowrap">20 min</dd>')

# ---------- design CSS: keep the page-specific rules, drop globals the shared reset already covers
drop = ('body{', 'h1,h2,h3{', 'p{text-wrap', 'a{color', '@keyframes mxRise', '.mx-rise{', '@media (prefers-reduced-motion')
keep = [ln for ln in design_css.strip().split('\n') if not ln.startswith(drop)]
page_css = '\n'.join(keep)
page_css = page_css.replace('.mx-card', '.mxa-card').replace('.mx-pill', '.mxa-pill')
page_css = page_css.replace('.mx-btn-p:hover', '.mxp .mxa-btn-p:hover').replace('.mx-btn-w:hover', '.mxp .mxa-btn-w:hover')

AD_CSS = page_css + r"""
.mxp.mxp .ad-tl>li{padding:22px 24px !important}
.mxp .mxa-main h3,.mxa-dlg h3{font-weight:700}
.mxp .mxa-main section[id]{scroll-margin-top:120px}
@media (prefers-reduced-motion:reduce){.mxp .ad-tl>li{opacity:1 !important;transform:none !important}}
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
/* application form (inline card + popup) */
.mxa-form{flex:1 1 480px;min-width:0;max-width:560px;margin:0 auto;align-self:center;background:#fff;color:#0E2A47;border-radius:24px;padding:32px;box-shadow:0 30px 60px rgba(2,2,21,.35)}
.mxa-form>h3,.mxa-dlg h3{font-size:24px;line-height:1.2;font-weight:800}
.mxa-form>p,.mxa-dlg .mxa-sub{margin:6px 0 18px !important;color:#4A5868;font-size:15px}
.mxa-f{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px 16px}
.mxa-f .full{grid-column:1/-1}
.mxa-f label{display:block;font-weight:600;font-size:15px;margin:0 0 6px;color:#0E2A47}
.mxa-f input[type=text],.mxa-f input[type=tel],.mxa-f input[type=email],.mxa-f textarea{width:100%;box-sizing:border-box;min-height:46px;border:1px solid #C9D8DF !important;border-radius:10px !important;padding:10px 12px !important;font:500 16px MoxieBarlow,Barlow,system-ui,sans-serif !important;color:#0E2A47 !important;background:#fff !important;box-shadow:none !important;margin:0 !important}
.mxa-f textarea{min-height:84px;resize:vertical}
.mxa-f .mxa-lbl{display:block;font-weight:600;font-size:15px;margin:0 0 6px;color:#0E2A47}
.mxa-st{position:relative}
.mxa-st summary{list-style:none;cursor:pointer;min-height:46px;box-sizing:border-box;border:1px solid #C9D8DF;border-radius:10px;padding:11px 40px 11px 12px;font:500 16px MoxieBarlow,Barlow,system-ui,sans-serif;color:#0E2A47;background:#fff;position:relative}
.mxa-st summary::-webkit-details-marker{display:none}
.mxa-st summary::after{content:"";position:absolute;right:16px;top:50%;width:8px;height:8px;border-right:2px solid #127C8F;border-bottom:2px solid #127C8F;transform:translateY(-70%) rotate(45deg);transition:transform .2s}
.mxa-st[open] summary::after{transform:translateY(-30%) rotate(-135deg)}
.mxa-st summary:focus-visible{outline:2px solid #1C97AE}
.mxa-st.mxa-bad summary{border-color:#C2362B}
.mxa-st .mxa-st-v.mxa-ph{color:#6B7F8E}
.mxa-st-p{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:6px;margin-top:6px;padding:10px;border:1px solid #C9D8DF;border-radius:10px;background:#fff;max-height:228px;overflow:auto}
.mxa-st-p label{display:flex !important;align-items:center;justify-content:center;gap:0;margin:0 !important;padding:7px 0;border:1px solid #DCE7EC;border-radius:8px;font:600 14px MoxieBarlow,Barlow,system-ui,sans-serif !important;color:#0E2A47;cursor:pointer;user-select:none}
.mxa-st-p input{position:absolute;opacity:0;width:1px;height:1px}
.mxa-st-p label:has(input:checked){background:#127C8F;border-color:#127C8F;color:#fff}
.mxa-st-p label:has(input:focus-visible){outline:2px solid #1C97AE}
.mxa-f input:focus,.mxa-f textarea:focus{outline:2px solid #1C97AE !important;border-color:#1C97AE !important}
.mxa-f [aria-invalid=true]{border-color:#C2362B !important}
.mxa-f .mxa-hp{position:absolute !important;left:-9999px !important;width:1px;height:1px;opacity:0}
.mxa-f .mxa-consent{display:flex;gap:10px;align-items:flex-start}
.mxa-f .mxa-consent input{margin:4px 0 0;width:18px;height:18px;accent-color:#127C8F;flex:none}
.mxa-f .mxa-consent label{font-weight:400;font-size:12.5px;line-height:1.45;color:#4A5868;margin:0}
.mxa-f button[type=submit]{width:100%;min-height:52px;border:0;border-radius:12px;background:#F46744;color:#0E2A47;font:700 17px MoxieBarlow,Barlow,system-ui,sans-serif;cursor:pointer}
.mxa-f button[type=submit]:hover{background:#ff7a59}
.mxa-f button[disabled]{opacity:.6;cursor:wait}
.mxa-err{color:#C2362B;font-size:14px;margin:0}
.mxa-done{text-align:center;padding:20px 0}
.mxa-done b{display:block;font-size:22px;margin-bottom:6px}
.mxa-dlg{border:0;padding:0;border-radius:24px;max-width:560px;width:calc(100% - 32px);max-height:calc(100% - 32px);box-shadow:0 30px 80px rgba(2,2,21,.45);color:#0E2A47;font-family:MoxieBarlow,Barlow,system-ui,sans-serif}
.mxa-dlg::backdrop{background:rgba(14,42,71,.6)}
.mxa-dlg>div{padding:32px;position:relative}
.mxa-x{position:absolute;top:14px;right:14px;width:40px;height:40px;border-radius:50%;border:0;background:#F4F8FA;color:#0E2A47;font-size:22px;line-height:1;cursor:pointer}
@media (max-width:560px){.mxa-f{grid-template-columns:1fr}.mxa-form,.mxa-dlg>div{padding:24px}}
/* below-the-fold sections skip rendering work until they are near the viewport */
.mxa-main>section:nth-of-type(n+3){content-visibility:auto;contain-intrinsic-size:auto 900px}
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
    'value="{{loans}}" onInput="{{onLoans}}" style="{{loansTrack}}"': f'value="{L0}" style="{track(L0, 1, 100)}"',
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

# ---------- page speed + answer engines: H1 paints immediately (it is the LCP element); speakable hooks
body = body.replace('<h1 id="ad-h1" class="mx-rise"', '<h1 id="ad-h1" class="mx-speak"', 1)
body = body.replace('<p style="margin: 0 0 8px">Area Directors are part of the Moxie team', '<p class="mx-speak" style="margin: 0 0 8px">Area Directors are part of the Moxie team', 1)
assert body.count('class="mx-speak"') == 2

# ---------- grids: fit 4 marketing cards and 5 timeline steps on laptop widths too
body = body.replace('grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 36px', 'grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 36px', 1)
body = body.replace('grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 28px', 'grid-template-columns: repeat(auto-fit, minmax(165px, 1fr)); gap: 28px', 1)

body = body.replace('<ol class="ad-tl ad-go"', '<ol class="ad-tl"', 1)

# ---------- apply steps list gets a hook for the li reset
body = body.replace('<ol style="list-style: none; padding: 0; margin: 32px 0 0;', '<ol class="ad-steps" style="list-style: none; padding: 0; margin: 32px 0 0;', 1)

# ---------- the design's static form -> slot for Moxie's Lofty form block
form = re.search(r'\s*<form aria-labelledby="ad-form-h".*?</form>', body, re.S)
assert form
CONSENT = ('I agree to the <a href="/site/electronic-disclosure-consent" target="_blank" rel="noopener">Electronic Disclosure Consent Agreement</a> '
           'and to receive recurring marketing communications from Moxie Mortgage, including auto-dialed calls, texts, and prerecorded or artificial '
           'voice messages. Frequency varies; message and data rates may apply. Reply STOP to opt out or HELP for help. I agree to the '
           '<a href="/site/privacy-terms#terms-of-service" target="_blank" rel="noopener">Terms of Service</a> and '
           '<a href="/site/privacy-terms#privacy-policy" target="_blank" rel="noopener">Privacy Policy</a>. Consent is not required to make a purchase; '
           f'call {PHONE} for direct assistance.')
US_STATES = 'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split()
ST_BOXES = ''.join(f'<label><input type="checkbox" value="{a}">{a}</label>' for a in US_STATES)

def appform(k):
    f = lambda n: f'mxa-{k}-{n}'
    return f'''<form class="mxa-f" data-mxa-form novalidate>
          <div class="full"><label for="{f('name')}">Name *</label><input id="{f('name')}" name="name" type="text" autocomplete="name" required maxlength="60"></div>
          <div><label for="{f('phone')}">Phone *</label><input id="{f('phone')}" name="phone" type="tel" autocomplete="tel" required maxlength="20"></div>
          <div><label for="{f('email')}">Email *</label><input id="{f('email')}" name="email" type="email" autocomplete="email" required maxlength="80"></div>
          <div><label for="{f('units')}">Buyer sales, last 12 months (units) *</label><input id="{f('units')}" name="units" type="text" inputmode="numeric" required maxlength="20"></div>
          <div><label for="{f('volume')}">Sales volume, last 12 months *</label><input id="{f('volume')}" name="volume" type="text" inputmode="decimal" required maxlength="30"></div>
          <div class="full"><span class="mxa-lbl" id="{f('states')}-l">States you operate in *</span><details class="mxa-st"><summary aria-labelledby="{f('states')}-l {f('states')}-v"><span id="{f('states')}-v" class="mxa-st-v">Select states</span></summary><div class="mxa-st-p" role="group" aria-labelledby="{f('states')}-l">{ST_BOXES}</div></details><input type="hidden" name="states" value=""></div>
          <div class="full"><label for="{f('msg')}">Message</label><textarea id="{f('msg')}" name="message" rows="3" maxlength="1000"></textarea></div>
          <div class="mxa-hp" aria-hidden="true"><label for="{f('web')}">Website</label><input id="{f('web')}" name="website" type="text" tabindex="-1" autocomplete="off"></div>
          <div class="full mxa-consent"><input id="{f('ok')}" name="consent" type="checkbox" required><label for="{f('ok')}">{CONSENT}</label></div>
          <p class="full mxa-err" role="alert" hidden></p>
          <div class="full"><button type="submit">Submit application</button></div>
        </form>'''
body = body.replace(form.group(0), f'''
      <div class="mxa-form" id="mxa-apply-card">
        <h3 id="ad-form-h">Apply to become an Area Director</h3>
        <p>We’ll review and reach out to book your onboarding call.</p>
        {appform('card')}
      </div>''', 1)
body += f'''
<dialog class="mxa-dlg" id="mxa-dlg" aria-labelledby="mxa-dlg-h"><div>
  <button type="button" class="mxa-x" data-mxa-close aria-label="Close">×</button>
  <h3 id="mxa-dlg-h">Apply to become an Area Director</h3>
  <p class="mxa-sub">Takes about a minute. We’ll reach out to book your 20-minute onboarding call.</p>
  {appform('pop')}
</div></dialog>'''

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
  rL.style.background = track(st.loans, 1, 100); rA.style.background = track(st.loan, 150000, 1500000);
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

// ---- first view: nudge the loans slider right and back to 40 so visitors see it moves the estimate
var touched = false;
rL.addEventListener('pointerdown', function () { touched = true; });
rL.addEventListener('keydown', function () { touched = true; });
function nudge() {
  if (touched || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
  var start = null, from = st.loans, peak = 72, dur = 1800;
  var ease = function (t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; };
  function step(ts) {
    if (touched) return;
    if (start === null) start = ts;
    var t = Math.min(1, (ts - start) / dur), k = t < .5 ? ease(t * 2) : ease((1 - t) * 2);
    st.loans = Math.round(from + (peak - from) * k); paint();
    if (t < 1) requestAnimationFrame(step); else { st.loans = from; paint(); }
  }
  requestAnimationFrame(step);
}
if ('IntersectionObserver' in window) {
  var nio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { nio.disconnect(); setTimeout(nudge, 350); } }); }, { threshold: 0.6 });
  nio.observe(rL.closest('div'));
}

// ---- timeline: cards appear one after the next when the section scrolls into view
var tl = root.querySelector('.ad-tl');
if (tl) {
  if (!('IntersectionObserver' in window)) tl.classList.add('ad-go');
  else { var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { tl.classList.add('ad-go'); io.disconnect(); } }); }, { threshold: 0.25 }); io.observe(tl); }
}

// ---- reviews: arrow buttons page the scrolling track
var trackEl = root.querySelector('.ad-rev-track');
root.querySelectorAll('[data-ad-rev]').forEach(function (b) {
  b.addEventListener('click', function () { trackEl.scrollBy({ left: +b.getAttribute('data-ad-rev') * trackEl.clientWidth, behavior: 'smooth' }); });
});

// ---- application: our own form, posted to Moxie's existing Lofty intake script, which tags the lead "CTA: AD Application"
var ENDPOINT = '__ENDPOINT__', SECRET = '__SECRET__';
var started = Date.now();
var dlg = root.querySelector('#mxa-dlg');
function openApply(src) {
  MX.track('ad_apply_open', { src: src });
  if (dlg && typeof dlg.showModal === 'function') { dlg.showModal(); var f = dlg.querySelector('input[name=name]'); if (f) f.focus(); }
  else { var c = root.querySelector('#mxa-apply-card'); if (c) c.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
}
root.querySelectorAll('a[href="#apply"]').forEach(function (a) {
  a.addEventListener('click', function (e) { e.preventDefault(); openApply(a.textContent.trim()); });
});
if (dlg) {
  dlg.querySelector('[data-mxa-close]').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
}
root.querySelectorAll('.mxa-st').forEach(function (d) {
  var form = d.closest('form'), hid = form.elements.states, val = d.querySelector('.mxa-st-v');
  function sync() {
    var on = [].map.call(d.querySelectorAll('input:checked'), function (c) { return c.value; });
    hid.value = on.join(', '); d.classList.remove('mxa-bad');
    val.textContent = on.length ? on.join(', ') : 'Select states'; val.classList.toggle('mxa-ph', !on.length);
  }
  d.addEventListener('change', sync); sync();
  document.addEventListener('click', function (e) { if (d.open && !d.contains(e.target)) d.open = false; });
});
var digits = function (v) { return String(v || '').replace(/\D/g, ''); };
root.querySelectorAll('[data-mxa-form]').forEach(function (form) {
  var err = form.querySelector('.mxa-err'), btn = form.querySelector('button[type=submit]');
  function fail(msg, el) { err.textContent = msg; err.hidden = false; if (el) { el.setAttribute('aria-invalid', 'true'); el.focus(); } }
  form.addEventListener('submit', function (e) {
    e.preventDefault(); err.hidden = true;
    form.querySelectorAll('[aria-invalid]').forEach(function (el) { el.removeAttribute('aria-invalid'); });
    var v = function (n) { return (form.elements[n].value || '').trim(); };
    var req = ['name', 'phone', 'email', 'units', 'volume', 'states'];
    for (var i = 0; i < req.length; i++) {
      if (v(req[i])) continue;
      if (req[i] === 'states') { var st = form.querySelector('.mxa-st'); st.classList.add('mxa-bad'); st.open = true; return fail('Please select the states you operate in.', st.querySelector('summary')); }
      return fail('Please fill in all required fields.', form.elements[req[i]]);
    }
    if (digits(v('phone')).length < 10) return fail('Please enter a 10-digit phone number.', form.elements.phone);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('email'))) return fail('Please enter a valid email address.', form.elements.email);
    if (!form.elements.consent.checked) return fail('Please check the consent box to continue.', form.elements.consent);
    if (v('website') || Date.now() - started < 3000) { done(form); return; } // bots: pretend success, send nothing
    if (!ENDPOINT || ENDPOINT.indexOf('__') === 0) return fail('Applications aren’t connected yet. Please call ' + '__PHONE__' + '.');
    var consentText = form.querySelector('.mxa-consent label').textContent.replace(/\s+/g, ' ').trim();
    var payload = { name: v('name'), phone: v('phone'), email: v('email'), cta: 'AD Application', tags: v('states').split(', ').filter(Boolean), source: 'MoxieMortgage.com — Area Director page',
      consent: true, secret: SECRET, message: v('message'), pageUrl: location.href.split('#')[0], submittedAt: new Date().toISOString(),
      fields: { 'Application': 'Area Director', 'Buyer sales, last 12 months (units)': v('units'), 'Sales volume, last 12 months': v('volume'),
        'States': v('states'), 'Consent text': consentText } };
    btn.disabled = true; btn.textContent = 'Sending…';
    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j || !j.ok) throw new Error((j && j.error) || 'failed');
        MX.track('ad_apply_submit', { src: form.closest('dialog') ? 'popup' : 'card' }); done(form);
      })
      .catch(function () { btn.disabled = false; btn.textContent = 'Submit application'; fail('Something went wrong sending your application. Please try again or call ' + '__PHONE__' + '.'); });
  });
});
function done(form) {
  root.querySelectorAll('[data-mxa-form]').forEach(function (f) {
    f.innerHTML = '<div class="full mxa-done" role="status"><b>Application received.</b>Thanks! We’ll review it and reach out to book your onboarding call.</div>';
  });
}
""".replace('__PON__', pill_on).replace('__POFF__', pill_off).replace('__ENDPOINT__', AD_ENDPOINT).replace('__SECRET__', AD_SECRET).replace('__PHONE__', PHONE)

DESC = "Join Moxie Mortgage as an Area Director: a W-2 business development role paid 0.25% of the loan amount on closed Moxie loans in your area. No mortgage license or loan work required."
import datetime
page, crumbs = webpage('/area-director', 'Area Director | Earn Mortgage Income in Your Area | Moxie Mortgage', DESC, 'Area Director', {
    "dateModified": datetime.date.today().isoformat(),
    "keywords": "Moxie Mortgage Area Director, mortgage business development role, earn mortgage income without a license, alternative to a mortgage joint venture",
    "mentions": [{"@type": "Thing", "name": "Real Estate Settlement Procedures Act (RESPA)"}, {"@type": "Thing", "name": "Mortgage joint venture"}]})
schema = jsonld([ORG, page, crumbs])

LOFTY_KEEP = '<!-- dialog showModal close data-mxa-close data-mxa-form mxa-done aria-invalid mxa-bad mxa-ph open -->'
full = wrap('mx-ad', LOFTY_KEEP + f'\n<style>{AD_CSS}</style>\n<div class="mxa-main">\n{body}\n</div>', script, schema, 'AREA DIRECTOR (/area-director, replaces /bdm)')
# the design font is Barlow; the shared embeds self-host it as MoxieBarlow
full = full.replace('font-family: Barlow, system-ui, sans-serif', 'font-family: MoxieBarlow, Barlow, system-ui, sans-serif')
full = full.replace('font:700 26px/1 Barlow,system-ui', 'font:700 26px/1 MoxieBarlow,Barlow,system-ui').replace('font:800 16px/1 Barlow,system-ui', 'font:800 16px/1 MoxieBarlow,Barlow,system-ui')
full = full.replace('font:500 16px Barlow,system-ui', 'font:500 16px MoxieBarlow,Barlow,system-ui').replace('font:700 14px Barlow,system-ui', 'font:700 14px MoxieBarlow,Barlow,system-ui')
html_out = optimize(full)
out = os.path.join(HERE, 'out', 'moxie-area-director-embed.html')
open(out, 'w', encoding='utf-8').write(html_out)
print('area director ok', len(html_out), 'bytes')

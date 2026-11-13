"""Moxie site header with an English / Español toggle. Replaces Lofty's built-in header.

Paste into a Lofty Custom Code / Embed block as the FIRST block on each page. It hides Lofty's own header
(header.md-header) on that page, keeps the same nav, and drives the shared MX.i18n language switch that the
footer and page embeds read.
"""
import os
from common import FONT_CSS, PHONE, PHONE_TEL
from i18n import I18N_JS
from optimize import optimize

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = 'https://cdn.lofty.com/image/fs/844775624682466/website/78760/cmsbuild/h200_2026117_2a0da67830f846bb-png.webp'
APPLY = 'https://apply.moxiemortgage.com'


def a(href, en, es, cls='', extra=''):
    c = f' class="{cls}"' if cls else ''
    return f'<a href="{href}"{c}{extra}><span data-es="{es}">{en}</span></a>'


NAV = [
    ('/buy', 'Buy', 'Comprar'),
    ('/refinance', 'Refinance', 'Refinanciar'),
    ('/heloc', 'HELOC', 'HELOC'),
    ('/loanoptions', 'Loan Options', 'Préstamos'),
]
RES = [
    ('/about', 'About Moxie', 'Sobre Moxie'),
    ('/faqs', 'FAQs', 'Preguntas frecuentes'),
    ('/clientsuccess', 'Client Success', 'Historias de clientes'),
]
CALC = [
    ('/calculators', 'All Calculators', 'Todas las calculadoras'),
    ('/affordabilitycalculator', 'Affordability Calculator', 'Calculadora de asequibilidad'),
    ('/mortgage-calculator', 'Mortgage Calculator', 'Calculadora de hipoteca'),
    ('/rentvsbuy', 'Rent vs. Buy Calculator', 'Calculadora de rentar vs. comprar'),
]

CSS = r"""
header.md-header,.md-header{display:none !important}
.mxh{--navy:#0E2A47;--teal:#127C8F;--sky:#1C97AE;--line:#DCE6EB;font-family:MoxieBarlow,Barlow,system-ui,sans-serif;color:var(--navy);background:#fff;box-sizing:border-box;width:100%;position:relative;z-index:1000;text-align:left;line-height:1.4;border-bottom:1px solid var(--line)}
.mxh *{box-sizing:border-box}
.mxh a{text-decoration:none;color:inherit}
.mxh ul{list-style:none !important;margin:0 !important;padding:0 !important}
.mxh.mxh li{list-style:none !important;margin:0 !important;padding:0 !important}
.mxh li::before{content:none !important}
.mxh a:focus-visible,.mxh button:focus-visible{outline:3px solid var(--sky);outline-offset:2px;border-radius:6px}
.mxh-top{background:#F4F8FA;font-size:14px}
.mxh-top>div{max-width:1440px;margin:0 auto;padding:7px 32px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.mxh-contact{display:flex;gap:28px;flex-wrap:wrap}
.mxh-contact a{display:inline-flex;align-items:center;gap:10px;font-weight:600;letter-spacing:.04em;color:var(--navy)}
.mxh-contact a:hover{color:var(--teal)}
.mxh-ic{width:30px;height:30px;border-radius:50%;background:#DFE8ED;color:var(--navy);display:inline-flex;align-items:center;justify-content:center;flex:none;transition:background .15s,color .15s}
.mxh-contact a:hover .mxh-ic{background:var(--teal);color:#fff}
.mxh-ic svg{width:14px;height:14px}
.mxh-lang{display:inline-flex;border:1.5px solid #C9D8DF;border-radius:999px;padding:2px;background:#fff}
.mxh-lang button{appearance:none;border:0;background:transparent;font:700 13px/1 MoxieBarlow,Barlow,system-ui,sans-serif;letter-spacing:.08em;color:#4A5868;padding:7px 12px;border-radius:999px;cursor:pointer;min-height:30px}
.mxh-lang button[aria-pressed=true]{background:var(--navy);color:#fff}
.mxh-main{max-width:1440px;margin:0 auto;padding:14px 32px;display:flex;align-items:center;gap:52px;min-height:88px}
.mxh-logo{flex:none;display:block}
.mxh-logo img{display:block;width:208px;height:auto}
.mxh-nav{flex:1;display:flex;justify-content:flex-start}
.mxh-nav>ul{display:flex;align-items:center;gap:6px}
.mxh-nav>ul>li>a,.mxh-dd>button{position:relative;display:inline-flex;align-items:center;gap:7px;padding:12px 13px;font-weight:700;font-size:17px;letter-spacing:.09em;text-transform:uppercase;color:var(--navy);background:none;border:0;cursor:pointer;font-family:inherit;white-space:nowrap;line-height:1.2}
.mxh-nav>ul>li>a::after,.mxh-dd>button::after{content:"";position:absolute;left:13px;right:13px;bottom:4px;height:2.5px;border-radius:2px;background:var(--sky);transform:scaleX(0);transform-origin:left;transition:transform .2s ease}
.mxh-nav>ul>li>a:hover::after,.mxh-dd>button:hover::after,.mxh-dd.open>button::after,.mxh-nav a[aria-current=page]::after,.mxh-dd>button[aria-current=page]::after{transform:scaleX(1)}
.mxh-nav>ul>li>a:hover,.mxh-dd>button:hover,.mxh-dd.open>button,.mxh-nav a[aria-current=page],.mxh-dd>button[aria-current=page]{color:var(--teal)}
.mxh-nav>ul>li>a.mxh-start{color:var(--sky)}
.mxh-dd{position:relative}
.mxh-dd>button svg{width:12px;height:12px;transition:transform .2s}
.mxh-dd.open>button svg{transform:rotate(180deg)}
.mxh-menu{position:absolute;left:0;top:calc(100% + 10px);min-width:480px;background:#fff;border:1px solid var(--line);border-radius:20px;box-shadow:0 24px 60px rgba(14,42,71,.18);padding:18px;display:none;grid-template-columns:1fr 1.25fr;gap:4px 20px}
.mxh-dd.open .mxh-menu{display:grid}
.mxh-menu h3{margin:4px 12px 8px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);font-weight:700}
.mxh-menu a{display:block;padding:10px 12px;border-radius:10px;font-weight:600;font-size:16px;white-space:nowrap}
.mxh-menu a:hover,.mxh-menu a[aria-current=page]{background:#E3F5F9;color:var(--teal)}
.mxh-cta{flex:none;display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:12px 22px;border-radius:12px;border:2px solid var(--navy);background:#fff;color:var(--navy) !important;font-weight:800;font-size:15px;letter-spacing:.09em;text-transform:uppercase;white-space:nowrap;transition:background .15s,color .15s}
.mxh-cta:hover{background:var(--navy);color:#fff !important}
.mxh-main>.mxh-cta{margin-left:auto}
.mxh-burger{display:none;margin-left:auto;width:46px;height:46px;border-radius:12px;border:1.5px solid #C9D8DF;background:#fff;cursor:pointer;align-items:center;justify-content:center;color:var(--navy)}
.mxh-burger svg{width:22px;height:22px}
.mxh-panel{display:none}
@media (max-width:1380px){.mxh-main{gap:28px;padding:14px 24px}.mxh-top>div{padding:7px 24px}.mxh-nav>ul{gap:0}.mxh-nav>ul>li>a,.mxh-dd>button{padding:12px 10px;font-size:15px;letter-spacing:.06em}.mxh-nav>ul>li>a::after,.mxh-dd>button::after{left:10px;right:10px}.mxh-logo img{width:184px}.mxh-cta{padding:12px 16px;font-size:14px;letter-spacing:.06em}}
@media (max-width:1100px){
  .mxh-nav,.mxh-main>.mxh-cta{display:none}
  .mxh-burger{display:inline-flex}
  .mxh-main{min-height:72px;gap:12px}
  .mxh-logo img{width:170px}
  .mxh.open .mxh-panel{display:block;border-top:1px solid var(--line);padding:8px 24px 24px;max-height:calc(100vh - 110px);overflow:auto}
  .mxh-panel a{display:block;padding:13px 4px;font-weight:700;font-size:17px;border-bottom:1px solid #EEF3F6}
  .mxh-panel a.mxh-start{color:var(--sky)}
  .mxh-panel a[aria-current=page]{color:var(--teal)}
  .mxh-panel h3{margin:18px 4px 4px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal)}
  .mxh-panel .mxh-cta{display:flex;margin-top:18px}
}
/* trust line */
.mxh-trust{flex:1;display:flex;justify-content:center;align-items:center;gap:10px;font-weight:600;color:#33475B;font-size:14px;letter-spacing:.02em;white-space:nowrap;overflow:hidden}
.mxh-trust .mxh-stars{color:#F46744;letter-spacing:2px}
.mxh-trust i{font-style:normal;color:#9FB3C2}
.mxh-right{display:flex;align-items:center;gap:12px;position:relative}
/* language suggestion */
.mxh-tip{position:absolute;right:0;top:calc(100% + 10px);z-index:1002;background:var(--navy);color:#fff;border-radius:14px;padding:12px 14px;box-shadow:0 16px 40px rgba(14,42,71,.3);display:none;align-items:center;gap:10px;white-space:nowrap;font-size:14px;font-weight:600}
.mxh-tip.show{display:flex;animation:mxhPop .25s ease-out}
.mxh-tip::before{content:"";position:absolute;right:22px;top:-6px;width:12px;height:12px;background:var(--navy);transform:rotate(45deg)}
.mxh-tip button{appearance:none;border:0;cursor:pointer;font:700 14px MoxieBarlow,Barlow,system-ui,sans-serif;border-radius:999px}
.mxh-tip .mxh-tip-yes{background:#F46744;color:#0E2A47;padding:7px 12px}
.mxh-tip .mxh-tip-x{background:transparent;color:#C9D6DF;font-size:18px;line-height:1;padding:4px 6px}
@keyframes mxhPop{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}
/* follow-on-scroll (condensed, glass) */
.mxh-wrap{position:relative;z-index:1000}
.mxh.mxh-stuck{position:fixed !important;top:0;left:0 !important;right:0;margin-left:0 !important;width:100% !important;background:rgba(255,255,255,.86);-webkit-backdrop-filter:saturate(1.6) blur(14px);backdrop-filter:saturate(1.6) blur(14px);box-shadow:0 8px 30px rgba(14,42,71,.12);border-bottom-color:rgba(220,230,235,.7);animation:mxhDrop .28s ease-out}
.mxh.mxh-stuck .mxh-top{display:none}
.mxh.mxh-stuck .mxh-main{min-height:66px;padding-top:8px;padding-bottom:8px}
.mxh.mxh-stuck .mxh-logo img{width:164px}
.mxh-logo img,.mxh-main{transition:width .2s ease,min-height .2s ease,padding .2s ease}
@keyframes mxhDrop{from{transform:translateY(-100%)}to{transform:none}}
/* phone action bar */
.mxh-bar{display:none}
@media (max-width:760px){
  .mxh-bar{position:fixed;left:0;right:0;bottom:0;z-index:1001;display:flex;gap:10px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.9);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-top:1px solid var(--line);box-shadow:0 -8px 24px rgba(14,42,71,.1);transform:translateY(110%);transition:transform .25s ease;font-family:MoxieBarlow,Barlow,system-ui,sans-serif}
  .mxh-bar.show{transform:none}
  .mxh-bar a{flex:1;display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;border-radius:12px;font-weight:800;font-size:16px;text-decoration:none;letter-spacing:.02em}
  .mxh-bar .mxh-call{border:2px solid var(--navy);color:var(--navy);background:#fff}
  .mxh-bar .mxh-go{background:#F46744;color:#0E2A47;flex:1.4}
  .mxh-bar svg{width:18px;height:18px}
}
@media (max-width:1100px){.mxh-trust{display:none}}
@media (prefers-reduced-motion:reduce){.mxh.mxh-stuck,.mxh-tip.show{animation:none}.mxh-bar{transition:none}}
@media (max-width:560px){.mxh-contact .mxh-hide{display:none}.mxh-contact{gap:12px}.mxh-top>div{padding:6px 16px}.mxh-main{padding:10px 16px}}
"""

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'
CHEV = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M2 4l4 4 4-4"/></svg>'
BURGER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'

apply_cta = f'<a href="{APPLY}" class="mxh-cta" data-mx-nolang><span data-es="Obtén tu aprobación">Get approved now</span></a>'
nav_items = f'<li>{a(APPLY, "Start Approval", "Aprobación", cls="mxh-start", extra=" data-mx-nolang")}</li>' + ''.join(f'<li>{a(h, en, es)}</li>' for h, en, es in NAV)
menu = ('<div><h3 data-es="Recursos">Resources</h3>' + ''.join(a(h, en, es) for h, en, es in RES) + '</div>'
        '<div><h3 data-es="Calculadoras">Calculators</h3>' + ''.join(a(h, en, es) for h, en, es in CALC) + '</div>')
panel = (f'{a(APPLY, "Start Approval", "Solicitar aprobación", cls="mxh-start", extra=" data-mx-nolang")}' + ''.join(a(h, en, es) for h, en, es in NAV)
         + '<h3 data-es="Recursos">Resources</h3>' + ''.join(a(h, en, es) for h, en, es in RES)
         + '<h3 data-es="Calculadoras">Calculators</h3>' + ''.join(a(h, en, es) for h, en, es in CALC) + apply_cta)

html = f"""<!--
  MOXIE MORTGAGE · SITE HEADER (English / Español)
  Paste into a Lofty "Custom Code / Embed" block as the FIRST block on each page. It hides Lofty's built-in
  header (md-header) on that page and adds the language toggle that the footer and page embeds follow.
-->
<link rel="preload" href="{LOGO}" as="image">
<style>{FONT_CSS}{CSS.strip()}</style>
<div class="mxh-wrap" id="mx-header-wrap"><header class="mxh" id="mx-header">
  <div class="mxh-top"><div>
    <div class="mxh-contact">
      <a href="tel:{PHONE_TEL}"><span class="mxh-ic">{ICON_PHONE}</span><span>480.660.2518</span></a>
      <a href="mailto:hello@moxiemortgage.com" aria-label="Email hello@moxiemortgage.com"><span class="mxh-ic">{ICON_MAIL}</span><span class="mxh-hide">hello@moxiemortgage.com</span></a>
    </div>
    <p class="mxh-trust" style="margin:0"><span class="mxh-stars" aria-hidden="true">★★★★★</span><span data-es="5.0 en Google">5.0 on Google</span><i aria-hidden="true">·</i><span data-es="Préstamos en 51 estados y territorios">Lending in 51 states &amp; territories</span><i aria-hidden="true">·</i><span>NMLS #1660690</span></p>
    <div class="mxh-right">
      <div class="mxh-lang" role="group" aria-label="Language" data-es-aria="Idioma">
      <button type="button" data-mx-lang="en" aria-pressed="true" lang="en" title="English">EN</button>
      <button type="button" data-mx-lang="es" aria-pressed="false" lang="es" title="Español">ES</button>
    </div>
      <div class="mxh-tip" role="dialog" aria-live="polite" lang="es"><span>¿Prefieres español?</span><button type="button" class="mxh-tip-yes">Ver en español</button><button type="button" class="mxh-tip-x" aria-label="Cerrar">×</button></div>
    </div>
  </div></div>
  <div class="mxh-main">
    <a href="/" class="mxh-logo" aria-label="Moxie Mortgage home" data-es-aria="Moxie Mortgage, inicio"><img src="{LOGO}" alt="Moxie Mortgage" width="212" height="59" fetchpriority="high"></a>
    <nav class="mxh-nav" aria-label="Main" data-es-aria="Principal"><ul>
      {nav_items}
      <li class="mxh-dd"><button type="button" aria-expanded="false" aria-controls="mxh-res"><span data-es="Recursos">Resources</span>{CHEV}</button>
        <div class="mxh-menu" id="mxh-res">{menu}</div></li>
    </ul></nav>
    {apply_cta}
    <button type="button" class="mxh-burger" aria-expanded="false" aria-controls="mxh-panel" aria-label="Menu" data-es-aria="Menú">{BURGER}</button>
  </div>
  <nav class="mxh-panel" id="mxh-panel" aria-label="Mobile" data-es-aria="Móvil">{panel}</nav>
</header></div>
<div class="mxh-bar" id="mx-actionbar" aria-label="Quick actions" data-es-aria="Acciones rápidas"><a href="tel:{PHONE_TEL}" class="mxh-call">{ICON_PHONE}<span data-es="Llamar">Call</span></a><a href="{APPLY}" class="mxh-go" data-mx-nolang><span data-es="Obtén tu aprobación">Get approved</span></a></div>
<script>
{I18N_JS.strip()}
(function () {{
  var h = document.getElementById('mx-header');
  // full width inside Lofty's container (same approach as the footer)
  function fit() {{
    for (var el = h.parentElement; el && el !== document.body; el = el.parentElement) {{
      var cs = getComputedStyle(el); if (/(hidden|clip)/.test(cs.overflowX + cs.overflow)) el.style.overflow = 'visible';
    }}
    h.style.marginLeft = '0px'; h.style.width = 'auto';
    var left = h.getBoundingClientRect().left;
    h.style.width = document.documentElement.clientWidth + 'px'; h.style.marginLeft = (-left) + 'px';
  }}
  fit(); window.addEventListener('resize', fit); window.addEventListener('load', fit);
  // highlight the current page
  var here = location.pathname.replace(/[/]+$/, '') || '/';
  h.querySelectorAll('.mxh-nav a, .mxh-panel a').forEach(function (l) {{
    try {{ var p = new URL(l.href, location.href); if (p.origin === location.origin && (p.pathname.replace(/[/]+$/, '') || '/') === here && here !== '/') l.setAttribute('aria-current', 'page'); }} catch (e) {{}}
  }});
  if (h.querySelector('.mxh-menu a[aria-current]')) h.querySelector('.mxh-dd>button').setAttribute('aria-current', 'page');
  // language toggle
  var btns = h.querySelectorAll('[data-mx-lang]');
  function paint() {{ btns.forEach(function (b) {{ b.setAttribute('aria-pressed', b.getAttribute('data-mx-lang') === MX.i18n.lang ? 'true' : 'false'); }}); }}
  btns.forEach(function (b) {{ b.addEventListener('click', function () {{ MX.i18n.set(b.getAttribute('data-mx-lang')); }}); }});
  document.addEventListener('mx:lang', paint); paint();
  // resources dropdown: click/tap to open, hover on desktop, Esc / outside click to close
  var dd = h.querySelector('.mxh-dd'), ddb = dd.querySelector('button'), t;
  function setDD(o) {{ dd.classList.toggle('open', o); ddb.setAttribute('aria-expanded', o ? 'true' : 'false'); }}
  ddb.addEventListener('click', function () {{ setDD(!dd.classList.contains('open')); }});
  if (window.matchMedia('(hover: hover)').matches) {{
    dd.addEventListener('mouseenter', function () {{ clearTimeout(t); setDD(true); }});
    dd.addEventListener('mouseleave', function () {{ t = setTimeout(function () {{ setDD(false); }}, 180); }});
  }}
  document.addEventListener('click', function (e) {{ if (!dd.contains(e.target)) setDD(false); }});
  document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape') {{ setDD(false); setPanel(false); }} }});
  var wrap = document.getElementById('mx-header-wrap');
  // follow on scroll: once the visitor scrolls past the full header, pin a slim glass version to the top
  var stuck = false, ticking = false;
  function onScroll() {{
    ticking = false;
    var full = wrap.offsetHeight, y = window.pageYOffset || document.documentElement.scrollTop;
    var want = y > full + 40;
    if (want === stuck) return;
    stuck = want;
    if (stuck) {{ wrap.style.height = full + 'px'; h.classList.add('mxh-stuck'); setDD(false); }}
    else {{ h.classList.remove('mxh-stuck'); wrap.style.height = ''; fit(); }}
  }}
  window.addEventListener('scroll', function () {{ if (!ticking) {{ ticking = true; requestAnimationFrame(onScroll); }} }}, {{ passive: true }});
  onScroll();
  // phone action bar: slides up after the first screen, hides near the footer so it never covers it
  var bar = document.getElementById('mx-actionbar');
  if (bar) {{
    document.body.appendChild(bar);
    var barOn = false;
    function onBar() {{
      var y = window.pageYOffset, max = document.documentElement.scrollHeight - innerHeight;
      var show = y > 320 && y < max - 160;
      if (show !== barOn) {{ barOn = show; bar.classList.toggle('show', show); }}
    }}
    window.addEventListener('scroll', onBar, {{ passive: true }}); onBar();
    bar.querySelectorAll('a').forEach(function (l) {{ l.addEventListener('click', function () {{ MX.track && MX.track('actionbar_click', {{ action: l.className }}); }}); }});
  }}
  // returning applicants: anyone who clicked an apply link before sees "Continue my approval"
  var APPLY_RE = /apply\.moxiemortgage\.com/;
  document.addEventListener('click', function (e) {{
    var l = e.target.closest && e.target.closest('a[href]');
    if (l && APPLY_RE.test(l.href)) {{ try {{ localStorage.setItem('mx_applied', String(Date.now())); }} catch (x) {{}} }}
  }}, true);
  var applied = null; try {{ applied = localStorage.getItem('mx_applied'); }} catch (x) {{}}
  if (applied && Date.now() - (+applied) < 1000 * 60 * 60 * 24 * 90) {{
    document.querySelectorAll('#mx-header .mxh-cta > span, #mx-actionbar .mxh-go > span').forEach(function (sp) {{
      sp.setAttribute('data-en', 'Continue my approval'); sp.setAttribute('data-es', 'Continúa tu aprobación');
    }});
    MX.i18n.apply(h); MX.i18n.apply(bar);
  }}
  // Spanish suggestion: once, for visitors whose browser prefers Spanish and who haven't picked a language
  var tip = h.querySelector('.mxh-tip');
  var picked = null, seen = null; try {{ picked = localStorage.getItem('mx_lang'); seen = localStorage.getItem('mx_lang_tip'); }} catch (x) {{}}
  var prefersEs = (navigator.languages || [navigator.language || '']).slice(0, 2).some(function (l) {{ return /^es(-|_|$)/i.test(l || ''); }});
  function hideTip() {{ tip.classList.remove('show'); try {{ localStorage.setItem('mx_lang_tip', '1'); }} catch (x) {{}} }}
  if (prefersEs && !picked && !seen && MX.i18n.lang === 'en') {{
    setTimeout(function () {{ if (!stuck) {{ tip.classList.add('show'); MX.track && MX.track('language_tip_shown', {{}}); }} }}, 1200);
  }}
  tip.querySelector('.mxh-tip-yes').addEventListener('click', function () {{ hideTip(); MX.i18n.set('es'); }});
  tip.querySelector('.mxh-tip-x').addEventListener('click', hideTip);
  document.addEventListener('mx:lang', hideTip);
  // mobile panel
  var bg = h.querySelector('.mxh-burger');
  function setPanel(o) {{ h.classList.toggle('open', o); bg.setAttribute('aria-expanded', o ? 'true' : 'false'); }}
  bg.addEventListener('click', function () {{ setPanel(!h.classList.contains('open')); }});
}})();
</script>
"""

out = os.path.join(HERE, 'out', 'moxie-header-embed.html')
open(out, 'w', encoding='utf-8').write(optimize(html))
print('header ok', os.path.getsize(out), 'bytes')

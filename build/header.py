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
.mxh{--navy:#0E2A47;--teal:#127C8F;--line:#DCE6EB;font-family:MoxieBarlow,Barlow,system-ui,sans-serif;color:var(--navy);background:#fff;box-sizing:border-box;width:100%;position:relative;z-index:1000;text-align:left;line-height:1.4}
.mxh *{box-sizing:border-box}
.mxh a{text-decoration:none;color:inherit}
.mxh ul{list-style:none !important;margin:0 !important;padding:0 !important}
.mxh.mxh li{list-style:none !important;margin:0 !important;padding:0 !important}
.mxh li::before{content:none !important}
.mxh a:focus-visible,.mxh button:focus-visible{outline:3px solid #1C97AE;outline-offset:2px;border-radius:6px}
.mxh-top{background:#F4F8FA;font-size:14px}
.mxh-top>div{max-width:1280px;margin:0 auto;padding:6px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.mxh-contact{display:flex;gap:22px;flex-wrap:wrap}
.mxh-contact a{display:inline-flex;align-items:center;gap:7px;font-weight:600;color:#33475B}
.mxh-contact a:hover{color:var(--teal)}
.mxh-contact svg{width:15px;height:15px;color:var(--teal)}
.mxh-lang{display:inline-flex;border:1.5px solid #C9D8DF;border-radius:999px;padding:2px;background:#fff}
.mxh-lang button{appearance:none;border:0;background:transparent;font:700 13px/1 MoxieBarlow,Barlow,system-ui,sans-serif;letter-spacing:.06em;color:#4A5868;padding:7px 12px;border-radius:999px;cursor:pointer;min-height:30px}
.mxh-lang button[aria-pressed=true]{background:var(--navy);color:#fff}
.mxh-main{max-width:1280px;margin:0 auto;padding:12px 24px;display:flex;align-items:center;gap:28px;min-height:84px}
.mxh-logo{flex:none;display:block}
.mxh-logo img{display:block;width:200px;height:auto}
.mxh-nav{flex:1;display:flex;justify-content:flex-end}
.mxh-nav>ul{display:flex;align-items:center;gap:4px}
.mxh-nav>ul>li>a,.mxh-dd>button{display:inline-flex;align-items:center;gap:6px;padding:10px 12px;border-radius:8px;font-weight:700;font-size:16px;letter-spacing:.04em;text-transform:uppercase;color:var(--navy);background:none;border:0;cursor:pointer;font-family:inherit;white-space:nowrap}
.mxh-nav>ul>li>a:hover,.mxh-dd>button:hover,.mxh-dd.open>button{color:var(--teal);background:#F4F8FA}
.mxh-dd{position:relative}
.mxh-dd>button svg{width:12px;height:12px;transition:transform .2s}
.mxh-dd.open>button svg{transform:rotate(180deg)}
.mxh-menu{position:absolute;right:0;top:calc(100% + 8px);min-width:300px;background:#fff;border:1px solid var(--line);border-radius:16px;box-shadow:0 20px 50px rgba(14,42,71,.18);padding:14px;display:none;grid-template-columns:1fr 1fr;gap:4px 18px}
.mxh-dd.open .mxh-menu{display:grid}
.mxh-menu h3{margin:4px 10px 6px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#6B7F8E;font-weight:700}
.mxh-menu a{display:block;padding:9px 10px;border-radius:8px;font-weight:600;font-size:15px;white-space:nowrap}
.mxh-menu a:hover{background:#E3F5F9;color:var(--teal)}
.mxh-cta{flex:none;display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:12px 20px;border-radius:12px;background:#F46744;color:#0E2A47 !important;font-weight:800;font-size:15px;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap}
.mxh-cta:hover{background:#ff7a59}
.mxh-burger{display:none;margin-left:auto;width:46px;height:46px;border-radius:10px;border:1.5px solid #C9D8DF;background:#fff;cursor:pointer;align-items:center;justify-content:center;color:var(--navy)}
.mxh-burger svg{width:22px;height:22px}
.mxh-panel{display:none}
@media (max-width:1320px){.mxh-nav>ul>li>a,.mxh-dd>button{padding:10px 8px;font-size:15px;letter-spacing:.02em}.mxh-main{gap:18px}.mxh-cta{padding:12px 16px;font-size:14px}}
@media (max-width:1100px){
  .mxh-nav,.mxh-main>.mxh-cta{display:none}
  .mxh-burger{display:inline-flex}
  .mxh-main{min-height:72px;gap:12px}
  .mxh-logo img{width:170px}
  .mxh.open .mxh-panel{display:block;border-top:1px solid var(--line);padding:8px 24px 24px;max-height:calc(100vh - 110px);overflow:auto}
  .mxh-panel a{display:block;padding:13px 4px;font-weight:700;font-size:17px;border-bottom:1px solid #EEF3F6}
  .mxh-panel h3{margin:18px 4px 4px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#6B7F8E}
  .mxh-panel .mxh-cta{display:flex;margin-top:18px;border-bottom:0}
}
@media (max-width:560px){.mxh-contact a span.mxh-hide{display:none}.mxh-contact{gap:14px}.mxh-top>div{padding:6px 16px}.mxh-main{padding:10px 16px}}
"""

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>'
CHEV = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M2 4l4 4 4-4"/></svg>'
BURGER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'

apply_cta = f'<a href="{APPLY}" class="mxh-cta" data-mx-nolang><span data-es="Obtén tu aprobación">Get approved now</span></a>'
nav_items = f'<li>{a(APPLY, "Start Approval", "Aprobación", extra=" data-mx-nolang")}</li>' + ''.join(f'<li>{a(h, en, es)}</li>' for h, en, es in NAV)
menu = ('<div><h3 data-es="Recursos">Resources</h3>' + ''.join(a(h, en, es) for h, en, es in RES) + '</div>'
        '<div><h3 data-es="Calculadoras">Calculators</h3>' + ''.join(a(h, en, es) for h, en, es in CALC) + '</div>')
panel = (f'{a(APPLY, "Start Approval", "Solicitar aprobación", extra=" data-mx-nolang")}' + ''.join(a(h, en, es) for h, en, es in NAV)
         + '<h3 data-es="Recursos">Resources</h3>' + ''.join(a(h, en, es) for h, en, es in RES)
         + '<h3 data-es="Calculadoras">Calculators</h3>' + ''.join(a(h, en, es) for h, en, es in CALC) + apply_cta)

html = f"""<!--
  MOXIE MORTGAGE · SITE HEADER (English / Español)
  Paste into a Lofty "Custom Code / Embed" block as the FIRST block on each page. It hides Lofty's built-in
  header (md-header) on that page and adds the language toggle that the footer and page embeds follow.
-->
<link rel="preload" href="{LOGO}" as="image">
<style>{FONT_CSS}{CSS.strip()}</style>
<header class="mxh" id="mx-header">
  <div class="mxh-top"><div>
    <div class="mxh-contact">
      <a href="tel:{PHONE_TEL}">{ICON_PHONE}<span>480.660.2518</span></a>
      <a href="mailto:hello@moxiemortgage.com">{ICON_MAIL}<span class="mxh-hide">hello@moxiemortgage.com</span></a>
    </div>
    <div class="mxh-lang" role="group" aria-label="Language" data-es-aria="Idioma">
      <button type="button" data-mx-lang="en" aria-pressed="true" lang="en" title="English">EN</button>
      <button type="button" data-mx-lang="es" aria-pressed="false" lang="es" title="Español">ES</button>
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
</header>
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

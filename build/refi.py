from common import *

A = APPLY
FAQ = [
 ("Will I need another appraisal when refinancing?", "In most cases, lenders require an appraisal to confirm the current market value of the property; however, FHA Streamline and VA IRRRL refinances generally do not require an appraisal."),
 ("Can I roll refinance closing costs into my loan?", "Yes, often closing costs can be financed into the new loan, reducing your upfront out-of-pocket expenses."),
 ("What is a streamline refinance?", "A streamline refinance is a simplified process available for current FHA or VA loan holders, which does not require an appraisal."),
 ("Does Moxie offer no-cost refinance?", "Yes, for qualifying borrowers we offer a no-cost refinances for life program, which can save clients $1,000s in origination fees and unlock financing strategies that otherwise would not be feasible."),
]

EXTRA_CSS = r"""
.mx-slot{min-height:520px;display:flex;flex-direction:column;justify-content:center}
.mx-slot.has-widget{display:block;min-height:0}
.mx-facade{background:radial-gradient(120% 90% at 85% 0%,#145A75 0%,#0E2A47 55%,#0B2340 100%);border-radius:24px;padding:40px;color:#fff;box-shadow:0 30px 60px rgba(14,42,71,.28)}
.mx-facade .mx-eyebrow{color:#1C97AE}
.mx-facade h2{font-size:38px;line-height:1.1;font-weight:800}
.mx-facade p{color:#B8C7D3;margin:18px 0 28px !important}
.mxp .mx-facade .mx-btn{width:100%;background:#1C97AE;color:var(--navy);font-size:19px;min-height:56px;animation:mxGlow 2s 1s ease-out 2}
.mx-pills{display:flex;gap:10px;justify-content:center;margin-top:18px;flex-wrap:wrap}
.mx-pills span{border:1px solid rgba(28,151,174,.45);border-radius:999px;padding:5px 14px;font-size:14px;color:#CDEFF6}
@keyframes mxGlow{0%,100%{box-shadow:0 0 0 0 rgba(28,151,174,.35)}50%{box-shadow:0 0 0 8px rgba(28,151,174,0)}}
.mx-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:28px}
.mx-steps li{display:flex;flex-direction:column;gap:10px}
.mx-num{font-weight:700;font-size:56px;line-height:1;color:var(--blue)}
.mx-steps h3{font-size:22px;font-weight:700}
.mx-steps p{color:var(--muted);font-size:16px}
.mx-band{border-radius:28px;padding:56px;display:flex;flex-wrap:wrap;gap:40px;align-items:center}
.mx-kpis{flex:1 1 320px;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}
.mxp.mxp .mx-kpis li{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:16px;padding:18px 20px !important}
.mx-kpis strong{display:block;font-size:24px;color:#fff}
.mx-kpis span{color:#D3E3EC;font-size:15px}
.mx-worth{display:flex;flex-wrap:wrap;gap:48px}
.mx-box{flex:1 1 380px;min-width:0;background:#fff;border:1px solid var(--line);border-radius:20px;padding:30px}
.mx-box h3{font-size:22px;font-weight:700;margin-bottom:16px !important}
.mx-box ol{list-style:decimal;padding-left:22px !important;display:flex;flex-direction:column;gap:10px}
@media (max-width:640px){.mx-band{padding:36px 24px}.mx-facade{padding:28px}.mx-facade h2{font-size:30px}}
"""

def goal(icon, title, text, kind, link, href):
    return (f'<article class="mx-card"><span class="mx-ico">{ICON[icon]}</span><h3 style="font-size:24px">{title}</h3><p>{text}</p>'
            f'<p style="font-size:14px;color:var(--navy)"><strong>{kind}</strong></p><a class="mx-more" href="{href}">{link} →</a></article>')

CK = lambda t: f'<li><span class="mx-ck">{ICON["check"]}</span>{t}</li>'

body = f"""
<style>{EXTRA_CSS.strip()}</style>
<section class="mx-hero" aria-labelledby="mxr-h1">
  <div class="mx-wrap">
    <div class="mx-hero-copy">
      <p class="mx-eyebrow mx-rise" data-mx="eyebrow">It's your equity. Use it.</p>
      <h1 id="mxr-h1" class="mx-h1 mx-rise"><span data-mx="h1">Refinance your mortgage at wholesale pricing</span></h1>
      <p class="mx-lede mx-rise mx-d2" data-mx="sub">Lower your payment without the retail markup. See what you could save in a few minutes, and it won’t affect your credit to start.</p>
      <ul class="mx-checks mx-rise mx-d2">
        {CK('No junk fees or unnecessary lender fees')}
        {CK('No-cost refinance for qualifying Moxie purchase clients')}
        {CK('FHA Streamline and VA IRRRL, usually no appraisal')}
      </ul>
    </div>
    <div class="mx-hero-media mx-fade">
      <div class="mx-slot" id="mx-refi-slot">
        <div class="mx-facade" id="mx-refi-facade">
          <p class="mx-eyebrow">Your new payment in 60 seconds</p>
          <h2>How much could you be saving on your mortgage?</h2>
          <p>Answer a few quick questions and we'll show you, in plain numbers, what your payment could look like. No guesswork and no credit check.</p>
          <a class="mx-btn" href="{A}?src=refi_hero">Show me my numbers</a>
          <div class="mx-pills"><span>✓ 60 seconds</span><span>✓ No credit check</span></div>
        </div>
      </div>
      <p class="mx-fine" style="margin-top:14px;text-align:center">Estimates are illustrative and not a loan offer, commitment, or underwriting decision. Actual rates, costs, and terms depend on credit, property, and market conditions.</p>
    </div>
  </div>
</section>

<section class="mx-sec mx-soft" aria-labelledby="mxr-goal">
  <div class="mx-wrap">
    <p class="mx-eyebrow">Pick your goal</p>
    <h2 id="mxr-goal" class="mx-h2" style="margin-bottom:36px;max-width:720px">Find the right refinance for you</h2>
    <div class="mx-grid">
      {goal('down', 'Lower my payment', 'Rates change over time. Refinance to a lower rate or longer term to lower your monthly payment and free up savings.', 'Rate-and-term refinance', 'Lower my payment', A + '?src=refi_lower')}
      {goal('cash', 'Take cash out', "You've been building equity with every payment. You may qualify to take cash out tax-free for renovations, debt payoff, or investing.", 'Cash-out refinance', 'Cash out my equity', A + '?src=refi_cashout')}
      {goal('clock', 'Shorten my term', "Life changes, and so can your mortgage. Move from a 30-year to a 15-year term and reduce the interest you'll pay.", 'Term-reduction refinance', 'Shorten my mortgage', A + '?src=refi_term')}
    </div>
  </div>
</section>

<section class="mx-sec" aria-labelledby="mxr-how">
  <div class="mx-wrap">
    <h2 id="mxr-how" class="mx-h2" style="margin-bottom:36px">How refinancing with Moxie works</h2>
    <ol class="mx-steps">
      <li><span class="mx-num">1</span><h3>See your numbers</h3><p>Use the savings tool above or talk to a loan expert. No credit check to see your estimate.</p></li>
      <li><span class="mx-num">2</span><h3>Apply in about 10 minutes</h3><p>Apply securely online. We compare wholesale lenders and lay out your best options side by side.</p></li>
      <li><span class="mx-num">3</span><h3>Lock and close</h3><p>Lock your rate, sign your disclosures, and close. Closing costs can often be rolled into the new loan.</p></li>
    </ol>
  </div>
</section>

<section aria-labelledby="mxr-heloc" style="padding:0 0 88px">
  <div class="mx-wrap">
    <div class="mx-band mx-dark">
      <div style="flex:1 1 420px;min-width:0">
        <p class="mx-eyebrow">Keep your current rate</p>
        <h2 id="mxr-heloc" class="mx-h2">Home Equity Line of Credit: cash in minutes, not weeks</h2>
        <p style="margin:16px 0 26px">Love your first-mortgage rate? A HELOC lets you tap equity without touching it, and you only pay interest on what you use.</p>
        <a class="mx-btn mx-btn-p" href="/heloc">Get my money now</a>
      </div>
      <ul class="mx-kpis">
        <li><strong>5 min</strong><span>Apply 100% online</span></li>
        <li><strong>Minutes</strong><span>To an approval decision</span></li>
        <li><strong>5 days</strong><span>Funding in as little as</span></li>
        <li><strong>$400K</strong><span>Borrow up to, no in-person appraisal</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="mx-sec mx-soft" aria-labelledby="mxr-worth">
  <div class="mx-wrap mx-worth">
    <div style="flex:1 1 420px;min-width:0">
      <h2 id="mxr-worth" class="mx-h2">Is refinancing worth it?</h2>
      <p class="mx-speak" style="margin-top:18px;font-size:20px;line-height:1.5"><strong>Usually, if your current rate is 0.5%–1% or more above today's rates.</strong> Refinancing can also make sense to switch from an ARM to a fixed rate, drop mortgage insurance, consolidate high-interest debt, or pull cash from your equity.</p>
      <p class="mx-muted" style="margin-top:16px">Refinance closing costs typically run 2%–5% of the loan amount and can often be rolled into the new loan. Qualifying borrowers who bought their home with Moxie can refinance at no cost.</p>
    </div>
    <div class="mx-box">
      <h3>What you need to refinance</h3>
      <ol><li>Sufficient home equity</li><li>A solid credit score (620+ for most lenders)</li><li>Stable income and a low debt-to-income ratio</li><li>On-time payment history</li></ol>
    </div>
  </div>
</section>

<section class="mx-sec" aria-labelledby="mxr-faq">
  <div class="mx-wrap" style="max-width:928px">
    <h2 id="mxr-faq" class="mx-h2">Refinance questions, answered</h2>
    <p class="mx-muted" style="margin:8px 0 28px"><a href="/faqs">Browse every mortgage FAQ</a></p>
    {faq_details([(q, f'<p class="mx-speak">{a}</p>') for q, a in FAQ])}
  </div>
</section>

<section aria-labelledby="mxr-cta" style="padding:0 0 88px">
  <div class="mx-wrap">
    <div class="mx-cta">
      <div style="max-width:640px"><h2 id="mxr-cta" class="mx-h2">Questions about refinancing?</h2>
      <p>Whether you're just exploring or ready to apply, Moxie advisors will match you with the best product at the best price available.</p></div>
      <div class="mx-btns"><a class="mx-btn mx-btn-p" href="{A}?src=refi_cta">Start my refinance</a><a class="mx-btn mx-btn-w" data-mx-phone href="tel:{PHONE_TEL}">Talk to an advisor</a></div>
    </div>
  </div>
</section>
"""

script = f"""
// ---- move Moxie's existing "How much could you be saving" widget (its own Lofty block) into the hero.
// If it isn't on the page, the facade stays and its button links to the application.
function mountWidget() {{
  var slot = document.getElementById('mx-refi-slot'); if (!slot || slot.classList.contains('has-widget')) return true;
  var blocks = document.querySelectorAll('.custom-code-html-content');
  for (var i = 0; i < blocks.length; i++) {{
    var b = blocks[i];
    if (root.contains(b) || b.contains(root)) continue;
    if (/How much could you be saving/i.test(b.textContent || '')) {{
      var block = b.closest('.md-custom-code') || b.parentElement;
      slot.textContent = ''; slot.appendChild(b); slot.classList.add('has-widget');
      if (block && !block.contains(root)) block.style.display = 'none';
      return true;
    }}
  }}
  return false;
}}
if (!mountWidget()) document.addEventListener('DOMContentLoaded', function () {{ if (!mountWidget()) window.addEventListener('load', mountWidget); }});

// ---- dynamic hero (returning + Hawaii), same rules and storage as the homepage hero
var V = MX.visitor();
MX.region(V.qs, V.override, function (hi) {{
  var v = {{}}, label = 'default';
  if (V.returning) {{
    v = {{ eyebrow: hi ? 'Aloha, welcome back' : 'Welcome back', h1: 'Ready to pick up where you left off?',
          sub: 'Your savings are still waiting. See your new payment in 60 seconds, then lock it in with a Moxie loan expert.' + (hi ? ' Call our Hawaii team at {HI_PHONE}.' : '') }};
    label = 'returning';
  }} else if (hi) {{
    v = {{ eyebrow: 'Serving Hawaii homeowners', h1: 'Refinance your Hawaii home at wholesale pricing',
          sub: 'Lower your payment without the retail markup. See what you could save in a few minutes. Questions? Call our Hawaii team at {HI_PHONE}.' }};
  }}
  if (hi) {{ label += '_hi'; root.querySelectorAll('[data-mx-phone]').forEach(function (a) {{ a.textContent = 'Call {HI_PHONE}'; a.href = 'tel:{HI_TEL}'; }}); }}
  MX.applyHero(root, v);
  MX.track('hero_view', {{ hero_page: 'refinance', hero_label: label }});
}});
"""

DESC = "See your new payment in 60 seconds, with no credit check. Refinance at wholesale pricing to lower your rate, shorten your term, or take cash out."
graph = [ORG] + webpage("/refinance", "Mortgage Refinance: Lower Your Payment or Cash Out | Moxie Mortgage", DESC, "Refinance") + [
  {"@type": "Service", "@id": SITE + "/refinance#service", "name": "Mortgage refinance", "serviceType": "Mortgage refinancing",
   "provider": {"@id": SITE + "/#org"}, "areaServed": {"@type": "Country", "name": "United States"},
   "description": "Rate-and-term, cash-out, and term-reduction refinances at wholesale pricing, including FHA Streamline and VA IRRRL."},
  {"@type": "LoanOrCredit", "name": "Home Equity Line of Credit (HELOC)", "loanType": "HELOC", "provider": {"@id": SITE + "/#org"},
   "url": SITE + "/heloc", "description": "Apply online in about 5 minutes, get a decision in minutes, and fund in as little as 5 days. Borrow up to $400,000 with no in-person appraisal."},
  {"@type": "HowTo", "name": "How to refinance with Moxie Mortgage", "step": [
    {"@type": "HowToStep", "position": 1, "name": "See your numbers", "text": "Use the savings tool or talk to a loan expert. No credit check to see your estimate."},
    {"@type": "HowToStep", "position": 2, "name": "Apply in about 10 minutes", "text": "Apply securely online and compare your best wholesale options side by side."},
    {"@type": "HowToStep", "position": 3, "name": "Lock and close", "text": "Lock your rate, sign your disclosures, and close."}]},
  faq_schema(FAQ)]

open('/home/claude/build/out/moxie-refinance-embed.html', 'w', encoding='utf-8').write(
    wrap('mx-refi', body, script, jsonld(graph), 'REFINANCE PAGE (/refinance)'))
print('refi ok')

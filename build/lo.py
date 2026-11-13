"""Loan officer recruiting page (/loanofficer). Same look and building blocks as the Area Director page
(ad.py): hero glance card, animated referral flow, retail-vs-Moxie table, marketing cards, agent reviews,
FAQ (FAQPage schema for answer engines), and the in-page application form + popup that posts to the
existing "Lofty API" intake Apps Script, tagged "CTA: LO Application" plus each licensed-state abbreviation.
Compensation is intentionally kept general (no bps on the page).
"""
import re, os, io, contextlib, datetime
from common import *
from optimize import optimize
with contextlib.redirect_stdout(io.StringIO()):
    import ad  # rebuilds the AD embed (deterministic) and exposes its CSS, form pieces and sections

HERE = os.path.dirname(os.path.abspath(__file__))
CDN_AD = ad.CDN_AD

EYEBROW = 'margin: 0 0 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; font-size: 14px; color: #127C8F'
EYEBROW_L = EYEBROW.replace('#127C8F', '#7FDCEC')
H2 = 'margin: 0; font-size: clamp(32px, 3.6vw, 46px); line-height: 1.08; font-weight: 800; letter-spacing: -0.015em'
BTN_P = 'background: #F46744; color: #0E2A47; font-weight: 700; padding: 15px 26px; border-radius: 12px; text-decoration: none; display: inline-flex; min-height: 48px; box-sizing: border-box; align-items: center'
BTN_W = 'border: 2px solid #ffffff; color: #ffffff; font-weight: 700; padding: 13px 24px; border-radius: 12px; text-decoration: none; display: inline-flex; min-height: 48px; box-sizing: border-box; align-items: center'
GRAD = 'linear-gradient(315deg, #1C97AE 0%, #0D4E66 42%, #0E2A47 100%)'
CARD = 'background: #ffffff; border: 1px solid #DCE6EB; border-radius: 20px; padding: 26px 26px 24px'


def section(sid, eyebrow, h2, inner, bg=None, lede=None, sec_id=None, dark=False):
    wrap_style = f'background: {bg}; padding: 92px 24px' + ('; color: #ffffff' if dark else '') if bg else 'max-width: 1200px; margin: 0 auto; padding: 92px 24px'
    open_inner = '<div style="max-width: 1200px; margin: 0 auto">' if bg else '<div>'
    lede_html = f'<p style="margin: 16px 0 0; font-size: 19px; color: {"#D3E3EC" if dark else "#4A5868"}">{lede}</p>' if lede else ''
    sec_id = sec_id or sid.replace('lo-', '')
    idattr = f' id="{sec_id}"'
    return f'''
  <section{idattr} aria-labelledby="{sid}" style="{wrap_style}">
    {open_inner}
      <div style="max-width: 780px">
        <p style="{EYEBROW_L if dark else EYEBROW}">{eyebrow}</p>
        <h2 id="{sid}" style="{H2}">{h2}</h2>{lede_html}
      </div>
      {inner}
    </div>
  </section>'''


# ---------------- HERO
hero = f'''
  <section aria-labelledby="lo-h1" style="background: {GRAD}; color: #ffffff; padding: 88px 24px 96px">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 56px; align-items: center">
      <div style="flex: 1 1 560px; min-width: 0">
        <p style="margin: 0 0 14px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; font-size: 14px; color: #7FDCEC">Loan officer careers</p>
        <h1 id="lo-h1" class="mx-speak" style="margin: 0; font-size: clamp(40px, 5.2vw, 64px); line-height: 1.03; font-weight: 800; letter-spacing: -0.02em; text-wrap: balance">Close more loans, faster and easier.</h1>
        <p class="mx-speak" style="margin: 22px 0 0; font-size: 19px; line-height: 1.5; color: #D3E3EC; max-width: 600px; text-wrap: pretty">Warm purchase deals, wholesale pricing, in-house operations and a team that has your back. Moxie Mortgage, a division of NEXA Mortgage, is hiring experienced, licensed loan officers who want to excel.</p>
        <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px">
          <a href="#apply" class="mxa-btn-p" style="{BTN_P}">Apply to join Moxie</a>
          <a href="#founder" class="mxa-btn-w" style="{BTN_W}">Talk with our founder</a>
        </div>
      </div>
      <div style="flex: 1 1 380px; min-width: 0">
        <dl aria-label="Moxie at a glance" style="margin: 0; background: #ffffff; color: #0E2A47; border-radius: 24px; padding: 24px; box-shadow: 0 30px 60px rgba(2,2,21,.35); display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); grid-auto-rows: 1fr; gap: 12px">
          <div style="background: #0E2A47; border-radius: 16px; padding: 18px 20px; display: flex; flex-direction: column; justify-content: space-between; gap: 6px; min-height: 132px; box-sizing: border-box; color: #ffffff"><dt style="font-size: 14px; color: #4A5868; font-weight: 600; line-height: 1.3; color: #7FDCEC">Company-generated business since day one<sup>3</sup></dt><dd style="margin: 0; font-size: clamp(32px, 3vw, 40px); font-weight: 800; line-height: 1; letter-spacing: -0.02em">82%</dd></div>
          <div style="background: #E3F5F9; border-radius: 16px; padding: 18px 20px; display: flex; flex-direction: column; justify-content: space-between; gap: 6px; min-height: 132px; box-sizing: border-box"><dt style="font-size: 14px; color: #4A5868; font-weight: 600; line-height: 1.3">Purchase business<sup>3</sup></dt><dd style="margin: 0; font-size: clamp(32px, 3vw, 40px); font-weight: 800; line-height: 1; letter-spacing: -0.02em">86%</dd></div>
          <div style="background: #E3F5F9; border-radius: 16px; padding: 18px 20px; display: flex; flex-direction: column; justify-content: space-between; gap: 6px; min-height: 132px; box-sizing: border-box"><dt style="font-size: 14px; color: #4A5868; font-weight: 600; line-height: 1.3">Avg. clear to close<sup>2</sup></dt><dd style="margin: 0; font-size: clamp(32px, 3vw, 40px); font-weight: 800; line-height: 1; letter-spacing: -0.02em">14 days</dd></div>
          <div style="background: #E3F5F9; border-radius: 16px; padding: 18px 20px; display: flex; flex-direction: column; justify-content: space-between; gap: 6px; min-height: 132px; box-sizing: border-box"><dt style="font-size: 14px; color: #4A5868; font-weight: 600; line-height: 1.3">Rating on Google</dt><dd style="margin: 0; font-size: clamp(32px, 3vw, 40px); font-weight: 800; line-height: 1; letter-spacing: -0.02em; display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap">5.0<span aria-label="5 out of 5 stars" style="color: #F46744; font-size: 18px; letter-spacing: 2px; line-height: 1">★★★★★</span></dd></div>
        </dl>
      </div>
    </div>
  </section>'''


# ---------------- STOP SAYING NO (from the recruiting deck)
STOPS = [
    ('Losing deals on rate', 'Price every file across 300+ wholesale investors instead of one rate sheet.'),
    ('Turning away self-employed borrowers', 'Bank statement, P&amp;L and asset depletion loans when tax returns don’t tell the story.'),
    ('Saying no to lower credit scores', 'Non-QM options for borrowers other lenders turned down.'),
    ('Sending investors elsewhere', 'DSCR, fix and flip, bridge and portfolio loans for real estate investors.'),
    ('Fighting slow, unresponsive operations', 'In-house processing and priority underwriting with key investors.'),
    ('Waiting weeks to get paid', 'Everyday payday: commission is paid as your loans close.'),
]
stop_cards = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article style="background: rgba(255,255,255,.06); border: 1px solid rgba(127,220,236,.25); border-radius: 20px; padding: 24px 26px">'
    f'<h3 style="margin: 0; font-size: 20px; color: #ffffff; display: flex; gap: 10px; align-items: center"><span aria-hidden="true" style="flex: none; width: 28px; height: 28px; border-radius: 50%; background: #F46744; color: #0E2A47; font-weight: 800; display: inline-flex; align-items: center; justify-content: center; font-size: 16px">×</span>Stop {t[0].lower() + t[1:]}</h3>'
    f'<p style="margin: 8px 0 0 38px; color: #D3E3EC; font-size: 16px">{d}</p></article>' for t, d in STOPS) + '</div>'
stop_sec = section('lo-stop', 'Sound familiar?', 'Stop saying no to good borrowers.', stop_cards, bg='#0E2A47', dark=True)

# ---------------- FOUR PILLARS
PILLARS = [
    ('trend', 'Company-generated deals', '82% of Moxie’s business since day one has been company-generated by Area Directors, agent partners and Moxie marketing, and 86% is purchase.<sup>3</sup>'),
    ('pct', 'Lender access and pricing', 'Shop 300+ wholesale investors through NEXA instead of one rate sheet. Moxie rates averaged 0.559% lower than the largest retail lender.<sup>1</sup>'),
    ('grid', 'Tools that sell for you', 'Arive for origination, Lofty CRM, and client-ready worksheets and calculators that make the numbers easy to explain.'),
    ('shield', 'In-house operations', 'In-house processing, priority underwriting and account support with key investors, and live support 6 AM–6 PM AZT for payroll, marketing, IT, compliance, licensing, training and HR.'),
]
pillars = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article class="mxa-card" style="{CARD}; display: flex; flex-direction: column; gap: 10px">'
    f'<span style="width: 48px; height: 48px; border-radius: 14px; background: #E3F5F9; color: #127C8F; display: inline-flex; align-items: center; justify-content: center"><span style="width: 24px; height: 24px; display: block">{ICON[ic]}</span></span>'
    f'<h3 style="margin: 6px 0 0; font-size: 21px">{t}</h3><p style="margin: 0; color: #4A5868; font-size: 16px">{d}</p></article>'
    for ic, t, d in PILLARS) + '</div>'
why = section('lo-why', 'Why loan officers move to Moxie', 'Everything you need to close more loans, under one roof.', pillars, sec_id='why')

# ---------------- PRICING + SPEED (dark stat band)
def stat(label, val):
    return (f'<div style="background: rgba(255,255,255,.06); border: 1px solid rgba(127,220,236,.25); border-radius: 20px; padding: 26px 24px 22px; display: flex; flex-direction: column-reverse; justify-content: flex-end; gap: 10px">'
            f'<dt style="font-size: 16px; line-height: 1.4; color: #C9D6DF">{label}</dt><dd style="margin: 0; font-size: clamp(44px, 4.4vw, 58px); line-height: 1; font-weight: 800; letter-spacing: -0.02em; color: #7FDCEC; font-variant-numeric: tabular-nums">{val}</dd></div>')
stats = ('<dl style="margin: 44px 0 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px">'
         + stat('Lower rates than the largest retail lender, on average<sup>1</sup>', '0.559%')
         + stat('Average clear to close<sup>2</sup>', '14 days')
         + stat('Wholesale investors', '300+')
         + stat('States and territories', '51') + '</dl>')
pricing = section('lo-price', 'Win on price and speed', 'Quote with confidence when buyers compare offers.', stats, bg='#0E2A47', dark=True,
                  lede='Wholesale pricing means your borrowers skip the retail overhead, and fast closings help their offers win. You see the full pricing and the investor purchase advice on every loan.')

# ---------------- OPERATIONS EDGE
OPS = [
    ('In-house processing', 'Moxie’s own processors work your files, so you aren’t waiting in a shared third-party queue.'),
    ('Priority underwriting and account support', 'Priority underwriting and account support with key investors across product types: conventional, government, jumbo, non-QM and HELOC.'),
    ('Full transparency', 'See the pricing and the investor purchase advice on every loan, so you always know how your deal was priced and paid.'),
]
ops_cards = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article class="mxa-card" style="{CARD}"><h3 style="margin: 0; font-size: 21px; display: flex; gap: 10px; align-items: flex-start"><span style="color: #127C8F; flex: none; display: inline-flex; margin-top: 2px">{ICON["check22"]}</span>{t}</h3>'
    f'<p style="margin: 8px 0 0; color: #4A5868; font-size: 16px">{d}</p></article>' for t, d in OPS) + '</div>'
ops_sec = section('lo-ops', 'Built to close', 'Operations that keep your files moving.', ops_cards,
                  lede='The deals only count if they close. Moxie keeps processing in-house and has priority lines into the investors you use most.')

# ---------------- REFERRAL FLOW (animated timeline, same as AD "Income builds over time")
STACK = [
    ('Key enterprise accounts', 'Relationships Moxie builds with key enterprise accounts in its markets, which send warm opportunities to Moxie loan officers.'),
    ('Area Directors in your market', 'Local Area Directors build and maintain agent relationships so buyers get introduced to you.'),
    ('Agent partner introductions', 'Agents introduce their buyers to you by group text or a quick call.'),
    ('Moxie marketing, done for you', 'Listing flyers, social posts and the Moxie Minute market report, designed and sent with your name on them.'),
    ('The Moxie Realtor Portal', 'Agents track every loan in the portal, so they keep sending the next buyer.'),
    ('Follow-up and client retention systems', 'Automated follow-up keeps every lead and past client close for referrals, equity options and refinances when the numbers work.'),
]
stack_rows = ''.join(
    f'<li style="display: flex; gap: 16px; align-items: flex-start; padding: 20px 24px; border-top: 1px solid #DCE6EB">'
    f'<span aria-hidden="true" style="flex: none; width: 32px; height: 32px; border-radius: 50%; background: #E3F5F9; color: #127C8F; display: inline-flex; align-items: center; justify-content: center"><span style="width: 18px; height: 18px; display: block">{ICON["check22"]}</span></span>'
    f'<div style="min-width: 0"><h4 style="margin: 0; font-size: 19px; line-height: 1.3">{t}</h4><p style="margin: 4px 0 0; color: #4A5868; font-size: 16px">{d}</p></div></li>' for t, d in STACK)
value_stack = (f'<div style="margin-top: 56px; border: 1px solid #DCE6EB; border-radius: 24px; overflow: hidden; background: #ffffff">'
               f'<h3 style="margin: 0; padding: 22px 24px; font-size: 22px">Everything working to send you deals</h3>'
               f'<ul class="lo-stack" style="list-style: none; padding: 0; margin: 0">{stack_rows}</ul>'
               f'<p style="margin: 0; padding: 20px 24px; background: #0E2A47; color: #ffffff; font-size: 19px; font-weight: 700">= A purchase pipeline that doesn’t depend on cold calls</p></div>')

def bigstat(val, label, note):
    return (f'<div style="background: {GRAD}; color: #ffffff; border-radius: 24px; padding: 30px 30px 28px; display: flex; flex-direction: column; gap: 8px">'
            f'<span style="font-size: clamp(64px, 7vw, 92px); line-height: .95; font-weight: 800; letter-spacing: -0.03em">{val}</span>'
            f'<span style="font-size: 21px; font-weight: 700; line-height: 1.25">{label}</span><span style="font-size: 16px; color: #D3E3EC">{note}</span></div>')
dealstats = ('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 40px">'
             + bigstat('82%', 'Company-generated business<sup>3</sup>', 'Since day one, most Moxie loans have started with a warm introduction from our key enterprise accounts, Area Directors, agent partners or Moxie marketing, not a loan officer’s own prospecting.')
             + bigstat('86%', 'Purchase business<sup>3</sup>', 'Buyers keep buying when refinances dry up. A purchase-heavy pipeline keeps your production steady when rates don’t cooperate.')
             + '</div>')
flow = section('lo-flow', 'Where your deals come from', 'Most of the business comes to you.',
               dealstats + value_stack +
               '',
               lede='Moxie builds the enterprise accounts and relationships that send buyers your way, so more of your week goes to structuring and closing loans.', sec_id='deals')


# ---------------- PRODUCTS (chip cloud; doubles as long-tail keywords)
PROGRAM_GROUPS = [
    ('home', 'Agency and government', 'Up to 100% LTV', ['Conventional', 'FHA', 'VA', 'USDA', 'Down payment assistance', 'Doctor loans']),
    ('gem', 'Jumbo', 'Up to $30M', ['Jumbo', 'Jumbo max ($5M)', 'Super jumbo ($30M)', 'Non-QM jumbo']),
    ('brief', 'Self-employed and non-QM', 'No tax returns needed', ['Bank statement', 'P&amp;L only', 'Asset depletion', 'Non-QM', 'No doc', 'Foreign national']),
    ('trend', 'Real estate investors', 'DSCR up to 25 units', ['DSCR', 'Bridge loans', 'Up to 25 units', 'Mixed use', 'Close in an LLC', 'Cross-collateralized loans']),
    ('cash', 'Home equity', 'Keep the low first rate', ['HELOC', 'HELOAN', 'Second mortgages', 'Reverse mortgages']),
    ('tool', 'Construction and renovation', 'Build, renovate, rehab', ['203(k)', 'Construction', 'One-time close', 'Fix and flip']),
    ('grid', 'Unique properties', 'Hard-to-finance properties', ['Non-warrantable condos', 'Condotels', 'Short-term rentals']),
    ('pct', 'Rate and payment options', 'Payments that fit', ['ARMs', 'Interest-only', 'Temporary buydowns']),
]
prog_cards = '<div class="lo-pg">' + ''.join(
    f'<article class="lo-pc" style="--i: {n}">'
    f'<div class="lo-pc-top"><span class="lo-pc-ic" aria-hidden="true"><span>{ICON[ic]}</span></span>'
    f'<div style="min-width: 0"><h3>{title}</h3><p class="lo-pc-hi">{hi}</p></div>'
    f'<span class="lo-pc-n">{len(items)}</span></div>'
    '<div class="lo-pl-wrap"><ul class="lo-plist">' + ''.join(f'<li style="--j: {k}"><span class="lo-ck" aria-hidden="true"></span><span>{x}</span></li>' for k, x in enumerate(items)) + '</ul></div></article>'
    for n, (ic, title, hi, items) in enumerate(PROGRAM_GROUPS)) + '</div>'
PROG_CSS = r"""
.mxp .lo-pg{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-rows:1fr;gap:20px;margin-top:44px}
.mxp .lo-pg>.lo-pc{display:flex;flex-direction:column}
@media (max-width:1100px){.mxp .lo-pg{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:600px){.mxp .lo-pg{grid-template-columns:1fr;grid-auto-rows:auto}}
.mxp .lo-pc{position:relative;background:#fff;border-radius:24px;overflow:hidden;box-shadow:0 1px 0 #DCE6EB,0 12px 32px rgba(14,42,71,.08);transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s}
.mxp .lo-pc::after{content:"";position:absolute;inset:0;border-radius:24px;border:1.5px solid transparent;pointer-events:none;transition:border-color .3s}
.mxp .lo-pc:hover{transform:translateY(-6px);box-shadow:0 1px 0 #DCE6EB,0 22px 44px rgba(14,42,71,.16)}
.mxp .lo-pc:hover::after{border-color:#1C97AE}
.mxp .lo-pc-top{position:relative;display:grid;grid-template-columns:1fr auto;grid-template-areas:"ic n" "txt txt";align-content:start;row-gap:16px;height:196px;box-sizing:border-box;padding:22px 22px 20px;background:radial-gradient(120% 140% at 100% 0%,#1C97AE 0%,#145A75 38%,#0E2A47 78%);color:#fff;overflow:hidden}
.mxp .lo-pc-top::before{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.22),transparent);transform:skewX(-18deg);pointer-events:none}
.mxp .lo-pc-ic{flex:none;width:52px;height:52px;border-radius:16px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);color:#7FDCEC;display:inline-flex;align-items:center;justify-content:center;transition:transform .45s cubic-bezier(.2,.8,.2,1)}
.mxp .lo-pc-ic>span{width:26px;height:26px;display:block}
.mxp .lo-pc:hover .lo-pc-ic{transform:rotate(-8deg) scale(1.08)}
.mxp .lo-pc-top h3{margin:0;font-size:14px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#B8E6EF}
.mxp .lo-pc-hi{margin:4px 0 0;font-size:clamp(20px,1.75vw,24px);font-weight:800;line-height:1.15;letter-spacing:-.01em;color:#fff}
.mxp .lo-pc-ic{grid-area:ic}
.mxp .lo-pc-top>div{grid-area:txt}
.mxp .lo-pc-n{grid-area:n;align-self:start;flex:none;min-width:34px;height:34px;padding:0 10px;border-radius:999px;background:#F46744;color:#0E2A47;font-weight:800;font-size:15px;display:inline-flex;align-items:center;justify-content:center}
.mxp .lo-pl-wrap{padding:22px 24px 26px}
.mxp .lo-plist{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr;gap:10px}
.mxp.mxp .lo-plist>li{display:flex !important;gap:10px;margin:0 !important;padding:0 !important;font-size:15.5px;line-height:1.4;color:#0E2A47;font-weight:500;list-style:none}
.mxp .lo-ck{flex:none;width:6px;height:11px;border:solid #1C97AE;border-width:0 2.5px 2.5px 0;transform:rotate(45deg);margin:3px 3px 0 2px}
@media (max-width:600px){.mxp .lo-pc-top{height:auto;padding:20px}.mxp .lo-pl-wrap{padding:18px 20px 22px}}
/* reveal: only when JS has armed it, so content never stays hidden */
.mxp .lo-pg.arm .lo-pc{opacity:0;transform:translateY(28px) scale(.98)}
.mxp .lo-pg.arm .lo-plist>li{opacity:0;transform:translateX(-8px)}
.mxp .lo-pg.arm.in .lo-pc{opacity:1;transform:none;transition:opacity .6s ease calc(var(--i) * 90ms),transform .7s cubic-bezier(.2,.8,.2,1) calc(var(--i) * 90ms),box-shadow .35s}
.mxp .lo-pg.arm.in .lo-plist>li{opacity:1;transform:none;transition:opacity .4s ease calc(var(--i) * 90ms + 250ms + var(--j) * 45ms),transform .4s ease calc(var(--i) * 90ms + 250ms + var(--j) * 45ms)}
.mxp .lo-pg.arm.in .lo-pc-top::before{animation:lo-shine 1.1s ease calc(var(--i) * 90ms + 200ms) 1}
.mxp .lo-pg.arm.in .lo-pc:hover{transform:translateY(-6px)}
@keyframes lo-shine{from{left:-60%}to{left:130%}}
@media (prefers-reduced-motion:reduce){.mxp .lo-pg.arm .lo-pc,.mxp .lo-pg.arm .lo-plist>li{opacity:1 !important;transform:none !important;transition:none !important}.mxp .lo-pc-top::before{display:none}}
"""
products_sec = section('lo-products', 'Loan programs', 'Thousands of programs, so you can say yes more often.',
    prog_cards + '',
    lede='Through NEXA’s wholesale investors, Moxie loan officers can match nearly any borrower to a program, from first-time buyers to self-employed borrowers and investors.')

# ---------------- YOUR DATABASE IS YOUR PIPELINE
DB = [
    ('HELOCs and second mortgages', 'Help past clients tap their equity for renovations or big expenses while they keep their low first-mortgage rate.'),
    ('Debt consolidation', 'Show exactly what a cash-out refinance pays off and saves with Moxie’s debt consolidation worksheet.'),
    ('Move-up and investor purchases', 'Past buyers become move-up buyers and investors, with DSCR and non-QM options when they need them.'),
    ('Refinances when the numbers work', 'Lofty CRM keeps every past client in follow-up, so you’re first in line when a refinance makes sense.'),
]
db_cards = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article class="mxa-card" style="{CARD}"><h3 style="margin: 0; font-size: 20px; display: flex; gap: 10px; align-items: flex-start"><span style="color: #127C8F; flex: none; display: inline-flex; margin-top: 2px">{ICON["check22"]}</span>{t}</h3>'
    f'<p style="margin: 8px 0 0; color: #4A5868; font-size: 16px">{d}</p></article>' for t, d in DB) + '</div>'
db_sec = section('lo-db', 'Your past clients', 'Your database is your next pipeline.', db_cards,
                 lede='Most homeowners won’t give up a low first-mortgage rate. You’ll have the products and tools to help them anyway, without waiting for rates to fall.')


# ================= STREAMLINED LAYOUT =================
# ---------------- SOUND FAMILIAR? (what the LO is thinking -> what Moxie does about it)
PAIN = [
    ('You’re chasing your own leads.', '82% of our business is company-generated', 'Warm introductions from key enterprise accounts, Area Directors and agent partners, and 86% of it is purchase.<sup>3</sup>'),
    ('You’re losing deals on rate.', 'Wholesale pricing that wins', 'Moxie rates averaged 0.559% lower than the largest retail lender.<sup>1</sup>'),
    ('You wait weeks to get paid.', 'Everyday payday', 'Generous compensation paid as your loans close, with full health insurance and a 401(k) for eligible employees.'),
    ('You’re turning away opportunities.', 'Huge product selection', 'Credit scores as low as 500, self-employed loans, DSCR up to 25 units, no doc loans, HELOCs and much more.'),
    ('Your files sit in a slow queue.', '14-day average clear to close<sup>2</sup>', 'In-house processing, plus priority underwriting and account support with key investors.'),
    ('You can’t see how your loans are priced.', 'Full transparency', 'See the pricing and the investor purchase advice on every loan.'),
]
FL_STATS = ['82%', '0.559%', 'Daily', '300+', '14 days', 'Every loan']
OK_IC = '<span aria-hidden="true" class="lo-fl-ok"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" style="display: block"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>'
flip_cards = ''.join(
    f'<button type="button" class="lo-fl" aria-pressed="false" style="--i: {n}">'
    f'<span class="lo-fl-in">'
    f'<span class="lo-fl-face lo-fl-front"><span class="lo-fl-qm" aria-hidden="true">“</span><span class="lo-fl-q">{a}</span><span class="lo-fl-hint">Tap if that’s you<span class="lo-fl-arrow" aria-hidden="true">→</span></span></span>'
    f'<span class="lo-fl-face lo-fl-back"><span class="lo-fl-stat">{FL_STATS[n]}</span><span class="lo-fl-t">{b}</span><span class="lo-fl-d">{c}</span></span>'
    f'</span></button>' for n, (a, b, c) in enumerate(PAIN))
pain_sec = section('lo-pain', 'Sound familiar?', 'Great loan officers, held back by the wrong company.',
    f'<div class="lo-fl-grid">{flip_cards}</div>'
    '<div class="lo-fl-sum" aria-live="polite">'
    '<p class="lo-fl-msg lo-fl-msg0">Pick the ones that sound like you.</p>'
    '<p class="lo-fl-msg lo-fl-msg1"><span>You picked</span> <span class="lo-fl-n">0</span> <span>of 6, and every one is fixed at Moxie.</span></p>'
    f'<div class="lo-fl-cta"><a href="#founder" class="mxa-btn-p" data-jump-link="founder" style="{BTN_P}">Talk with our founder</a><a href="#apply" class="lo-fl-apply">Apply to join Moxie</a></div></div>',
    lede='Tap everything that sounds like your week, and see what changes at Moxie.')
FLIP_CSS = r"""
.mxp .lo-fl-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:40px;perspective:1600px}
.mxp.mxp button.lo-fl{all:unset;box-sizing:border-box;display:grid;cursor:pointer;border-radius:20px;-webkit-tap-highlight-color:transparent;transform-style:preserve-3d;transform:perspective(1000px) translateY(var(--lift,0px)) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .35s cubic-bezier(.2,.8,.2,1)}
.mxp.mxp button.lo-fl.tilt{transition:transform .08s linear}
.mxp .lo-fl:hover{--lift:-6px}
.mxp .lo-fl:focus-visible{outline:3px solid #0E2A47;outline-offset:4px}
.mxp .lo-fl-in{display:grid;transition:transform .7s cubic-bezier(.2,.8,.2,1);transform-style:preserve-3d}
.mxp .lo-fl[aria-pressed="true"] .lo-fl-in{transform:rotateY(180deg)}
.mxp .lo-fl-face{grid-area:1/1;position:relative;display:flex;flex-direction:column;gap:14px;min-height:220px;padding:28px 28px 24px;border-radius:20px;-webkit-backface-visibility:hidden;backface-visibility:hidden;box-sizing:border-box;text-align:left;font-family:Barlow,system-ui,sans-serif;overflow:hidden}
.mxp .lo-fl-front{background:linear-gradient(160deg,#fff 55%,#F3F8FA);color:#0E2A47;border:1px solid #DCE6EB;box-shadow:0 1px 0 #E9F0F3,0 5px 0 #D5E1E7,0 20px 34px -10px rgba(14,42,71,.26);transition:box-shadow .3s}
.mxp .lo-fl-front::after{content:"";position:absolute;inset:0;border-radius:inherit;background:radial-gradient(circle at var(--mx,30%) var(--my,0%),rgba(255,255,255,.9),rgba(255,255,255,0) 55%);opacity:0;transition:opacity .3s;pointer-events:none;mix-blend-mode:soft-light}
.mxp .lo-fl:hover .lo-fl-front::after{opacity:1}
.mxp .lo-fl-front::before{content:"";position:absolute;left:0;top:0;bottom:0;width:6px;background:#0E2A47}
.mxp .lo-fl:hover .lo-fl-front{box-shadow:0 1px 0 #E9F0F3,0 7px 0 #D5E1E7,0 30px 46px -12px rgba(14,42,71,.32)}
.mxp .lo-fl-qm{display:block;height:26px;font-family:Georgia,"Times New Roman",serif;font-size:72px;line-height:.9;font-weight:700;color:#1C97AE;margin-bottom:-4px}
.mxp .lo-fl-q{font-size:clamp(22px,1.9vw,26px);font-weight:800;line-height:1.18;letter-spacing:-.015em;color:#0E2A47}
.mxp .lo-fl-hint{margin-top:auto;display:inline-flex;align-items:center;gap:10px;font-size:13px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#127C8F}
.mxp .lo-fl-arrow{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;border:2px solid #1C97AE;font-size:15px;letter-spacing:0;transition:transform .25s,background .25s,color .25s}
.mxp .lo-fl:hover .lo-fl-arrow{transform:translateX(4px);background:#1C97AE;color:#fff}
.mxp .lo-fl-back{transform:rotateY(180deg);background:linear-gradient(160deg,#123657,#0E2A47 60%);color:#fff;box-shadow:0 1px 0 #1A3E60,0 5px 0 #071A2E,0 20px 34px -10px rgba(14,42,71,.4)}
.mxp .lo-fl-stat{font-size:clamp(40px,3.4vw,50px);font-weight:800;line-height:1;letter-spacing:-.025em;color:#7FDCEC;margin-bottom:-4px}
.mxp .lo-fl-back::before{content:"";position:absolute;left:0;top:0;bottom:0;width:6px;background:#1C97AE}
.mxp .lo-fl-ok{width:34px;height:34px;border-radius:10px;background:#1C97AE;color:#fff;display:inline-flex;align-items:center;justify-content:center}
.mxp .lo-fl-t{font-size:clamp(21px,1.8vw,24px);font-weight:800;line-height:1.2;letter-spacing:-.01em}
.mxp .lo-fl-d{font-size:15.5px;line-height:1.45;color:#D3E3EC}
.mxp .lo-fl-back sup{color:#D3E3EC}
.mxp .lo-fl-grid:not(.picked) .lo-fl-arrow{animation:lo-glow 2.2s ease-in-out infinite}
@keyframes lo-glow{0%,100%{box-shadow:0 0 0 0 rgba(28,151,174,0)}50%{box-shadow:0 0 0 6px rgba(28,151,174,.2)}}
.mxp .lo-fl-grid.nudge .lo-fl:not([aria-pressed="true"]) .lo-fl-in{animation:lo-nudge 1.1s ease calc(var(--i) * .12s) 1}
@keyframes lo-nudge{0%,100%{transform:none}35%{transform:rotateY(-22deg)}70%{transform:rotateY(6deg)}}
.mxp .lo-fl-sum{margin-top:20px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px 24px;padding:22px 28px;border-radius:20px;background:#F4F8FA;border:1px solid #DCE6EB;color:#0E2A47}
.mxp .lo-fl-msg{margin:0;font-size:20px;font-weight:800}
.mxp .lo-fl-msg1{display:none}
.mxp .lo-fl-sum.on .lo-fl-msg0{display:none}
.mxp .lo-fl-sum.on .lo-fl-msg1{display:block}
.mxp.mxp .lo-fl-n{display:inline-block !important;min-width:1.4em;padding:0 .3em;border-radius:8px;background:#F46744;color:#0E2A47;text-align:center}
.mxp .lo-fl-n.lo-bump{animation:lo-pop .35s ease}
@keyframes lo-pop{50%{transform:scale(1.35)}}
.mxp .lo-fl-cta{display:flex;flex-wrap:wrap;align-items:center;gap:10px 20px}
.mxp.mxp .lo-fl-apply{color:#127C8F;font-weight:700;text-decoration:underline;text-underline-offset:3px}
.mxp .lo-fl-sum:not(.on) .lo-fl-cta{opacity:.55}
@media (max-width:980px){.mxp .lo-fl-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:600px){.mxp .lo-fl-grid{grid-template-columns:1fr;gap:16px}.mxp .lo-fl-stat{font-size:40px}.mxp .lo-fl-face{min-height:0;padding:22px 22px 20px 26px}.mxp .lo-fl-q,.mxp .lo-fl-t{font-size:21px}.mxp .lo-fl-sum{padding:20px}.mxp .lo-fl-msg{font-size:18px}}
@media (prefers-reduced-motion:reduce){.mxp .lo-fl-grid .lo-fl-arrow,.mxp .lo-fl-grid.nudge .lo-fl .lo-fl-in{animation:none !important}.mxp .lo-fl-in,.mxp.mxp button.lo-fl{transition:none}.mxp.mxp button.lo-fl{transform:none}.mxp .lo-fl-n.lo-bump{animation:none}}
"""

# ---------------- WHERE YOUR DEALS COME FROM (value stack, dark)
STACK = [
    ('Key enterprise accounts', 'Relationships Moxie builds with key enterprise accounts in its markets, which send warm opportunities to Moxie loan officers.'),
    ('Area Directors in your market', 'Local Area Directors build and maintain agent relationships so buyers get introduced to you.'),
    ('Follow-up and client retention systems', 'Automated follow-up keeps every lead and past client close for referrals, equity options and refinances when the numbers work.'),
]
stack_rows = ''.join(
    f'<li><div class="lo-st-row"><span aria-hidden="true" class="lo-st-n">{i}</span><div style="min-width: 0"><h3>{t}</h3><p>{d}</p></div></div></li>' for i, (t, d) in enumerate(STACK, 1))
deals_sec = section('lo-deals', 'Where your deals come from', 'We create the business opportunities that drive your growth.',
    f'<div class="lo-st"><ul style="list-style: none; padding: 0; margin: 0">{stack_rows}</ul>'
    '<p class="lo-st-sum"><b>82% company-generated, 86% purchase.</b><span>A pipeline that doesn’t depend on cold calls or waiting for rates to drop.<sup>3</sup></span></p></div>'
    '',
    bg='#F4F8FA', sec_id='deals',
    lede='Moxie builds the enterprise accounts and relationships that send buyers your way, so more of your week goes to structuring and closing loans.')

# ---------------- PAY + SUPPORT (dark)
PAY = [
    ('pct', 'Generous compensation', 'Packages built to reward production, set out in a written agreement.'),
    ('cash', 'Everyday payday', 'Commission is paid as your loans close, not on a monthly cycle.'),
    ('shield', 'Full health insurance', 'Medical, dental and vision coverage for eligible employees.'),
    ('trend', '401(k) and HSA', 'Retirement savings and pre-tax health dollars for eligible employees.'),
]
SUPPORT = [
    ('Live support, 6 AM–6 PM AZT', 'Payroll, marketing, IT, compliance, licensing, training and HR.'),
    ('A mentor on your deals', 'Deal strategy, accountability and direction when a file gets complicated.'),
    ('Monday and Friday huddles', 'Live team calls at noon ET for market updates, new tools and deal reviews.'),
    ('Annual conference', 'A yearly event with top producers and lenders.'),
]
pay_cards = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article style="background: #ffffff; color: #0E2A47; border-radius: 20px; padding: 24px; display: flex; flex-direction: column; gap: 8px">'
    f'<span style="width: 44px; height: 44px; border-radius: 12px; background: #FDE7E1; color: #C2482A; display: inline-flex; align-items: center; justify-content: center"><span style="width: 22px; height: 22px; display: block">{ICON[ic]}</span></span>'
    f'<h3 style="margin: 6px 0 0; font-size: clamp(16px, 1.55vw, 20px); white-space: nowrap">{t}</h3><p style="margin: 0; color: #4A5868; font-size: 16px">{d}</p></article>' for ic, t, d in PAY) + '</div>'
sup_list = ('<h3 style="margin: 56px 0 0; font-size: 24px; color: #ffffff">Support behind every file</h3>'
            '<ul class="lo-sup" style="list-style: none; padding: 0; margin: 20px 0 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px 32px">'
            + ''.join(f'<li><div class="lo-sup-i"><h4>{t}</h4><p>{d}</p></div></li>' for t, d in SUPPORT) + '</ul>')
pay_sec = section('lo-pay', 'Pay, benefits and support', 'Get paid well. Work anywhere, but never work alone.',
    pay_cards + sup_list + '',
    bg='#0E2A47', dark=True)

STREAM_CSS = r"""
.mxp sup{font-size:.45em !important;line-height:0;vertical-align:super;font-weight:600;opacity:.75;margin-left:1px}
.mxp .lo-pf-head{display:grid;grid-template-columns:1fr 1.35fr;gap:16px;margin:40px 0 12px;padding:0 24px;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#4A5868}
.mxp .lo-pf-head span+span{color:#127C8F}
.mxp.mxp .lo-pf>li{list-style:none;margin:0 0 12px !important;padding:0 !important}
.mxp.mxp .lo-pf>li::before,.mxp.mxp .lo-st li::before,.mxp.mxp .lo-tl>li::before,.mxp.mxp .lo-sup>li::before{content:none !important}
.mxp .lo-pf-row{display:grid;grid-template-columns:1fr 1.35fr;gap:16px;align-items:stretch}
.mxp .lo-pf-was{display:flex;gap:14px;align-items:center;background:#F4F8FA;border-radius:18px;padding:20px 24px}
.mxp .lo-pf-was p{margin:0;font-size:18px;color:#4A5868;font-weight:600}
.mxp .lo-pf-x{flex:none;width:28px;height:28px;border-radius:50%;background:#FDE7E1;color:#C2482A;font-weight:800;display:inline-flex;align-items:center;justify-content:center;font-size:17px;line-height:1}
.mxp .lo-pf-now{display:flex;gap:14px;align-items:flex-start;background:#fff;border:1.5px solid #1C97AE;border-radius:18px;padding:18px 24px;box-shadow:0 10px 24px rgba(14,42,71,.06)}
.mxp .lo-pf-now h3{margin:0;font-size:20px;line-height:1.25;color:#0E2A47}
.mxp .lo-pf-now p{margin:4px 0 0;font-size:16px;color:#4A5868}
.mxp .lo-pf-ok{flex:none;width:28px;height:28px;border-radius:50%;background:#1C97AE;color:#fff;display:inline-flex;align-items:center;justify-content:center;margin-top:1px}
@media (max-width:760px){.mxp .lo-pf-head{display:none}.mxp .lo-pf-row{grid-template-columns:1fr;gap:0}.mxp .lo-pf-was{border-radius:18px 18px 0 0;padding:16px 20px}.mxp .lo-pf-was p{font-size:16px}.mxp .lo-pf-now{border-radius:0 0 18px 18px;padding:16px 20px}.mxp.mxp .lo-pf>li{margin-bottom:16px !important}}
.mxp .lo-st{margin-top:40px;background:#fff;color:#0E2A47;border-radius:24px;overflow:hidden;border:1px solid #DCE6EB;box-shadow:0 12px 32px rgba(14,42,71,.06)}
.mxp.mxp .lo-st li{list-style:none;margin:0 !important}
.mxp .lo-st-row{display:flex;gap:18px;align-items:flex-start;padding:22px 28px;border-bottom:1px solid #DCE6EB}
.mxp .lo-st-n{flex:none;width:36px;height:36px;border-radius:50%;background:#E3F5F9;color:#127C8F;font-weight:800;display:inline-flex;align-items:center;justify-content:center}
.mxp .lo-st-row h3{margin:0;font-size:20px;line-height:1.3}
.mxp .lo-st-row p{margin:4px 0 0;font-size:16px;color:#4A5868}
.mxp .lo-st-sum{margin:0;padding:24px 28px;background:linear-gradient(315deg,#1C97AE 0%,#0D4E66 60%,#0E2A47 100%);color:#fff;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px}
.mxp .lo-st-sum b{font-size:clamp(22px,2.4vw,28px);font-weight:800;letter-spacing:-.01em}
.mxp .lo-st-sum span{font-size:16px;color:#D3E3EC}
@media (max-width:600px){.mxp .lo-st-row{padding:18px 20px;gap:14px}.mxp .lo-st-sum{padding:20px}}
.mxp .lo-tl-i{padding:16px 0 0;margin-top:16px;border-top:1px solid #DCE6EB}
.mxp .lo-tl>li:first-child .lo-tl-i{border-top:0;margin-top:0;padding-top:8px}
.mxp .lo-tl h4{margin:0;font-size:18px;color:#0E2A47}
.mxp .lo-tl p{margin:4px 0 0;font-size:16px;color:#4A5868}
.mxp .lo-sup-i{padding:2px 0 2px 18px;border-left:3px solid #1C97AE}
.mxp .lo-sup h4{margin:0;font-size:18px;color:#fff}
.mxp .lo-sup p{margin:4px 0 0;font-size:15px;color:#D3E3EC}
"""

# ---------------- QUICK-JUMP TABS
JUMP = [('pain', 'Why Moxie'), ('deals', 'Deal flow'), ('pay', 'Pay and support'), ('products', 'Loan programs'), ('tools', 'Tools'),
        ('partners', 'Partners'), ('marketing', 'Marketing'), ('faq', 'FAQ'), ('apply', 'Apply')]
jump_nav = ('\n  <nav class="lo-jump" aria-label="Page sections"><div class="lo-jump-in">'
            + ''.join(f'<a href="#{i}" data-jump="{i}">{t}</a>' for i, t in JUMP) + '</div>'
            '<label class="lo-jump-m"><span>Jump to a section</span><select data-jump-select>'
            + ''.join(f'<option value="{i}">{t}</option>' for i, t in JUMP) + '</select></label></nav>')
JUMP_CSS = r"""
.mxp .lo-jump{position:relative;z-index:40;background:rgba(255,255,255,.92);-webkit-backdrop-filter:saturate(1.4) blur(12px);backdrop-filter:saturate(1.4) blur(12px);border-bottom:1px solid #DCE6EB;transition:box-shadow .2s}
.mxp .lo-jump.pinned{position:fixed;left:0;right:0;top:var(--lo-jt,0px);transition:top .25s ease,box-shadow .2s;box-shadow:0 8px 24px rgba(14,42,71,.08)}
.mxp .lo-jump-in{max-width:1200px;margin:0 auto;padding:12px 24px;display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
.mxp.mxp .lo-jump a{display:inline-flex;align-items:center;min-height:38px;padding:0 16px;border-radius:999px;font-size:15px;font-weight:600;color:#0E2A47;text-decoration:none;white-space:nowrap;border:1px solid transparent;transition:background .15s,color .15s,border-color .15s}
.mxp.mxp .lo-jump a:hover{background:#E3F5F9;color:#127C8F}
.mxp.mxp .lo-jump a[aria-current="true"]{background:#0E2A47;color:#fff}
.mxp.mxp .lo-jump a[href="#apply"]{background:#F46744;color:#0E2A47;font-weight:700}
.mxp .lo-jump a:focus-visible{outline:3px solid #1C97AE;outline-offset:2px}
.mxp section[id]{scroll-margin-top:140px}
.mxp .lo-jump-m{display:none}
@media (max-width:900px){.mxp .lo-jump{background:#fff;-webkit-backdrop-filter:none;backdrop-filter:none;padding:14px 20px}.mxp .lo-jump-in{display:none}.mxp .lo-jump-m{display:flex;align-items:center;gap:12px;max-width:600px;margin:0 auto}.mxp .lo-jump-m span{flex:none;font-size:14px;font-weight:700;color:#0E2A47}.mxp .lo-jump-m select{flex:1;min-width:0;font:600 16px Barlow,sans-serif;color:#0E2A47;padding:10px 36px 10px 14px;border:1.5px solid #DCE6EB;border-radius:12px;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' fill='none' stroke='%230E2A47' stroke-width='2'/%3E%3C/svg%3E") no-repeat right 14px center;-webkit-appearance:none;appearance:none}.mxp section[id]{scroll-margin-top:90px}}
"""

# ---------------- ABOUT MOXIE (small band, opens /about in a new tab)
about_band = '''
  <section aria-label="About Moxie Mortgage" style="max-width: 1200px; margin: 0 auto; padding: 56px 24px 0">
    <div class="lo-about">
      <div style="min-width: 0"><p class="lo-about-k">New to Moxie?</p>
        <p class="lo-about-t">Get the full story: who we are, how we started and what we stand for.</p></div>
      <a href="/about" target="_blank" rel="noopener" class="lo-about-btn">Learn more about Moxie<span aria-hidden="true">↗</span><span class="lo-sr"> (opens in a new tab)</span></a>
    </div>
  </section>'''
ABOUT_CSS = r"""
.mxp .lo-about{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px 32px;padding:26px 32px;border-radius:22px;background:#E3F5F9;border:1px solid #C9E8EF}
.mxp .lo-about-k{margin:0;font-size:13px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#127C8F}
.mxp .lo-about-t{margin:4px 0 0;font-size:19px;font-weight:600;color:#0E2A47;max-width:560px}
.mxp.mxp .lo-about-btn{display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 22px;border-radius:12px;background:#0E2A47;color:#fff;font-weight:700;text-decoration:none;transition:background .15s,transform .15s}
.mxp.mxp .lo-about-btn:hover{background:#1C97AE;transform:translateY(-1px)}
.mxp .lo-about-btn span[aria-hidden]{font-size:18px;line-height:1}
.mxp .lo-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media (max-width:600px){.mxp .lo-about{padding:22px 20px}.mxp.mxp .lo-about-btn{width:100%;justify-content:center}}
"""

# ---------------- FOUNDER (a direct line, not a recruiter)
HS = 'https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@25d214c/website/robert-lucido-headshot-'
founder_sec = f'''
  <section id="founder" aria-labelledby="lo-founder" style="max-width: 1200px; margin: 0 auto; padding: 92px 24px">
    <div style="background: #ffffff; border: 1px solid #DCE6EB; border-radius: 28px; padding: 40px; display: flex; flex-wrap: wrap; gap: 32px; align-items: center">
      <img src="{HS}256.webp" srcset="{HS}128.webp 128w, {HS}256.webp 256w, {HS}400.webp 400w" sizes="140px" alt="Robert Lucido Jr, founder of Moxie Mortgage" width="140" height="140" loading="lazy" decoding="async" style="flex: none; width: 140px; height: 140px; border-radius: 50%; object-fit: cover; border: 4px solid #E3F5F9">
      <div style="flex: 1 1 420px; min-width: 0">
        <p style="{EYEBROW}">A direct line</p>
        <h2 id="lo-founder" style="{H2}; text-wrap: balance">Talk with the founder, not a recruiter.</h2>
        <p style="margin: 14px 0 0; font-size: 18px; color: #4A5868; max-width: 640px">Your intro call is with Robert Lucido Jr, Moxie’s founder. Ask him anything: compensation, where the deals come from, and what your first 90 days look like. The conversation is confidential.</p>
        <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 24px"><a href="#apply" class="mxa-btn-p" style="{BTN_P}">Book a confidential call</a></div>
      </div>
      <figure class="lo-sg" style="flex: none; margin: 0; display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center">
        <img src="https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@8ea82e8/website/scotsman-top-originators-320.webp" alt="Scotsman Guide Top Originators badge" width="120" height="120" loading="lazy" decoding="async" style="width: 120px; height: 120px">
        <figcaption style="font-size: 13px; font-weight: 700; color: #0E2A47; line-height: 1.3; max-width: 150px">Scotsman Guide Top Originator</figcaption>
      </figure>
    </div>
  </section>'''

# ---------------- RETAIL VS MOXIE TABLE
ROWS = [
    ('Loan options', 'One lender’s product shelf', '300+ wholesale investors: conventional, FHA, VA, jumbo, non-QM and HELOC'),
    ('Pricing', 'Retail pricing that carries branch overhead', 'Wholesale pricing; rates averaged 0.559% lower than the largest retail lender<sup>1</sup>'),
    ('Speed', '38-day industry average to close<sup>2</sup>', '14-day average clear to close<sup>2</sup>'),
    ('Referrals', 'Mostly yours to find', '82% of business company-generated, 86% purchase<sup>3</sup>'),
    ('When you’re paid', 'On the next payroll cycle, often weeks after closing', 'Everyday payday: as your loans close'),
    ('Operations', 'Shared processing queue', 'In-house processing, plus priority underwriting and account support with key investors'),
    ('Transparency', 'You see your split, not the pricing', 'Full transparency on pricing and the investor purchase advice'),
    ('Technology', 'Whatever the company licenses', 'Proprietary Moxie tools, integrated, automated and powered by AI'),
    ('Support', 'Varies by branch', 'A mentor on your deals and twice-weekly team huddles'),
]
trs = ''.join(f'<tr style="border-top: 1px solid #DCE6EB"><th scope="row" style="text-align: left; padding: 18px 24px; font-weight: 700">{a}</th><td style="padding: 18px 24px; color: #4A5868">{b}</td><td style="padding: 18px 24px; background: #F4F8FA; font-weight: 700">{c}</td></tr>' for a, b, c in ROWS)
SR = 'position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0)'
table = f'''<div style="margin-top: 36px; overflow-x: auto; border: 1px solid #DCE6EB; border-radius: 24px">
      <table style="width: 100%; min-width: 720px; border-collapse: collapse; font-size: 16px">
        <caption style="{SR}">A typical retail lender compared with originating at Moxie Mortgage</caption>
        <thead><tr><th scope="col" style="text-align: left; padding: 20px 24px; width: 22%"><span style="{SR}">Item</span></th>
          <th scope="col" style="text-align: left; padding: 20px 24px; color: #4A5868; font-size: 15px; letter-spacing: .08em; text-transform: uppercase">Typical retail lender</th>
          <th scope="col" style="text-align: left; padding: 20px 24px; background: #0E2A47; color: #ffffff; font-size: 15px; letter-spacing: .08em; text-transform: uppercase">Moxie loan officer</th></tr></thead>
        <tbody>{trs}</tbody>
      </table>
    </div>'''
compare = section('lo-compare', 'Retail vs. Moxie', 'More ways to say yes, at a price your borrower can feel.', table)

# ---------------- TOOLS
TOOLS = [
    ('Proprietary client tools', 'Proven tools that help you win more deals and get them to the closing table easier.'),
    ('Arive and Lofty CRM', 'Originate in Arive and keep every lead and past client moving forward and coming back in Lofty.'),
    ('Moxie University', 'On-demand courses plus short how-to videos for Moxie’s client tools.'),
    ('Automated client experience', 'Automated tools that elevate and streamline every step for your clients, from application to closing and beyond.'),
]
T = dict(TOOLS)
CHK = '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8.5l3.2 3L13 4.5"/></svg>'
ROV_STEPS = ['Appraisal uploaded', 'Comparable sales pulled', 'Value gaps flagged', 'ROV letter drafted']
DONE = lambda t: f'<div class="lo-rov-done"><span>✓</span>{t}</div>'
rov_slide = ('<div class="lo-sl lo-sl-rov on">'
             '<div class="lo-rov-top"><span class="lo-rov-logo"><b>ROV</b>ai</span></div>'
             '<div class="lo-rov-bar"><i></i></div>'
             '<ul class="lo-rov-steps">' + ''.join(f'<li><span class="lo-rov-ic"></span>{t}</li>' for t in ROV_STEPS) + '</ul>'
             + DONE('ROV ready to submit in minutes') + '</div>')
BELL = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/></svg>'
RF_ALERTS = [('Phoenix, AZ', 'Save $384/mo'), ('Tampa, FL', 'Save $291/mo')]
refi_slide = ('<div class="lo-sl lo-sl-rf">'
              '<div class="lo-rov-top"><span class="lo-rov-logo"><b>Refi alert engine</b></span></div>'
              '<div class="lo-rf-chart"><svg viewBox="0 0 300 100" preserveAspectRatio="none">'
              '<line class="lo-rf-tg" x1="0" y1="62" x2="300" y2="62"/>'
              '<path class="lo-rf-ln" pathLength="1" d="M0,22 C30,16 45,32 70,28 S110,42 135,36 S170,52 195,58 S240,76 300,84"/></svg>'
              '<span class="lo-rf-lbl">Client’s target rate</span><span class="lo-rf-dot"></span></div>'
              '<div class="lo-rf-al">' + ''.join(f'<div class="lo-rf-a"><span class="lo-rf-bell">{BELL}</span><b><small>Past client</small>{a}</b><em>{b}</em></div>' for a, b in RF_ALERTS) + '</div>'
              + DONE('Clients alerted the moment rates drop') + '</div>')
WH_DOCS = ['Local attractions', 'Parks and trails', 'Restaurants', 'Hospitals and urgent care']
home_slide = ('<div class="lo-sl lo-sl-wh">'
              '<div class="lo-rov-top"><span class="lo-rov-logo"><b>Welcome home packet</b></span></div>'
              '<div class="lo-wh-stage"><div class="lo-wh-house"><svg viewBox="0 0 64 64" fill="none" stroke-linecap="round" stroke-linejoin="round">'
              '<path class="lo-wh-roof" d="M10 30 L32 11 L54 30 Z"/>'
              '<path class="lo-wh-draw" pathLength="1" d="M8 31 L32 10 L56 31 M15 26 V54 H49 V26"/>'
              '<rect class="lo-wh-door" x="27" y="39" width="10" height="15" rx="1.5"/></svg></div>'
              '<div class="lo-wh-docs">' + ''.join(f'<div class="lo-wh-doc"><i></i>{t}</div>' for t in WH_DOCS) + '</div></div>'
              + DONE('Their new neighborhood, all in one guide') + '</div>')
DEMOS = ['ROVai', 'Refi alerts', 'Welcome home']
viz_tools = ('<div class="lo-rov" aria-hidden="true"><div class="lo-dtabs">'
             + ''.join(f'<span data-i="{k}"{" class=\"on\"" if k == 0 else ""}>{t}<i></i></span>' for k, t in enumerate(DEMOS))
             + '</div><div class="lo-demo">' + rov_slide + refi_slide + home_slide + '</div></div>'
             )
viz_loop = ('<div class="lo-viz-loop" aria-hidden="true"><span>Lead</span><b>→</b><span>App</span>'
            '<b class="v">↑</b><i></i><b class="v">↓</b>'
            '<span class="lo-loop-back">Coming back</span><b>←</b><span>Funded</span></div>')
viz_uni = '<div class="lo-viz-play" aria-hidden="true"><span class="lo-play"></span><span>On demand, 24/7</span></div>'
viz_auto = ('<div class="lo-viz-toasts" aria-hidden="true">'
            + ''.join(f'<div class="lo-toast" style="--k: {k}"><span class="lo-toast-ic">{CHK}</span>{t}</div>' for k, t in enumerate(['Title work received', 'Appraisal ordered', 'Clear to close']))
            + '</div>')
def bcard(cls, title, viz):
    return f'<article class="lo-b {cls}"><h3>{title}</h3><p>{T[title]}</p>{viz}</article>'
tools = ('<div class="lo-bento">'
         + bcard('lo-b-big', 'Proprietary client tools', viz_tools)
         + bcard('lo-b-crm', 'Arive and Lofty CRM', viz_loop)
         + bcard('lo-b-uni', 'Moxie University', viz_uni)
         + bcard('lo-b-auto', 'Automated client experience', viz_auto)
         + '</div>')
BENTO_CSS = r"""
.mxp .lo-bento{display:grid;grid-template-columns:1.25fr 1fr 1fr;grid-template-areas:"big crm uni" "big aut aut";gap:18px;margin-top:44px}
.mxp .lo-b-big{grid-area:big}.mxp .lo-b-crm{grid-area:crm}.mxp .lo-b-uni{grid-area:uni}.mxp .lo-b-auto{grid-area:aut}
.mxp .lo-b{position:relative;overflow:hidden;border-radius:24px;padding:28px;background:linear-gradient(160deg,rgba(255,255,255,.09),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.14);color:#fff;display:flex;flex-direction:column;gap:8px;transition:transform .35s cubic-bezier(.2,.8,.2,1),border-color .3s,box-shadow .35s}
.mxp .lo-b::before{content:"";position:absolute;width:260px;height:260px;right:-90px;top:-110px;border-radius:50%;background:radial-gradient(circle,rgba(28,151,174,.45),transparent 70%);pointer-events:none;transition:transform .5s}
.mxp .lo-b:hover{transform:translateY(-5px);border-color:rgba(127,220,236,.55);box-shadow:0 24px 48px rgba(0,0,0,.25)}
.mxp .lo-b:hover::before{transform:scale(1.25)}
.mxp .lo-b h3{position:relative;margin:0;font-size:22px;line-height:1.2;color:#fff}
.mxp .lo-b-big h3{font-size:clamp(26px,2.6vw,32px)}
.mxp .lo-b p{position:relative;margin:0;font-size:16px;color:#C9D7E2;max-width:44ch}
.mxp .lo-viz-bars{margin-top:auto;padding-top:20px;display:grid;gap:14px}
.mxp .lo-rov{position:relative;flex:1 1 auto;margin-top:22px;border-radius:18px;background:rgba(2,2,21,.35);border:1px solid rgba(255,255,255,.12);padding:18px 18px 16px;display:flex;flex-direction:column;gap:12px;overflow:hidden}
.mxp .lo-rov::after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(127,220,236,.10) 50%,transparent 70%);transform:translateX(-100%);animation:lo-scan 6s ease-in-out infinite;pointer-events:none}
.mxp .lo-rov-top{display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 10px}
.mxp .lo-rov-logo{font-size:20px;font-weight:800;letter-spacing:-.01em;color:#7FDCEC}
.mxp .lo-rov-logo b{color:#fff;font-weight:800}
.mxp .lo-dtabs{position:relative;z-index:1;display:flex;flex-wrap:wrap;gap:6px}
.mxp .lo-dtabs span{position:relative;overflow:hidden;cursor:pointer;font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#B8C7D3;padding:6px 11px;border-radius:999px;border:1px solid rgba(255,255,255,.14);transition:background .25s,color .25s}
.mxp .lo-dtabs span:hover{color:#fff}
.mxp .lo-dtabs span.on{background:rgba(127,220,236,.16);border-color:rgba(127,220,236,.5);color:#fff}
.mxp .lo-dtabs span i{position:absolute;left:0;bottom:0;height:2px;width:100%;background:#7FDCEC;transform:scaleX(0);transform-origin:left}
.mxp .lo-dtabs span.on i{animation:lo-dt 6.5s linear forwards}
@keyframes lo-dt{to{transform:scaleX(1)}}
.mxp .lo-demo{display:grid;flex:1 1 auto}
.mxp .lo-sl{grid-area:1/1;display:flex;flex-direction:column;gap:12px;opacity:0;visibility:hidden;transition:opacity .45s,visibility 0s .45s}
.mxp .lo-sl.on{opacity:1;visibility:visible;transition:opacity .45s}
.mxp .lo-sl:not(.on) *,.mxp .lo-sl:not(.on) *::after{animation:none !important}
.mxp .lo-rf-chart{position:relative;height:104px;border-radius:12px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08)}
.mxp .lo-rf-chart svg{position:absolute;inset:8px 0;width:100%;height:calc(100% - 16px);overflow:visible}
.mxp .lo-rf-tg{stroke:#F46744;stroke-width:2;stroke-dasharray:6 6;vector-effect:non-scaling-stroke}
.mxp .lo-rf-ln{fill:none;stroke:#7FDCEC;stroke-width:3;stroke-linecap:round;vector-effect:non-scaling-stroke;stroke-dasharray:1;stroke-dashoffset:1;animation:lo-rf-draw 6s cubic-bezier(.45,0,.3,1) infinite}
.mxp .lo-rf-lbl{position:absolute;left:10px;top:calc(8px + 62% * .846 - 22px);font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#F7A389}
.mxp .lo-rf-dot{position:absolute;left:68%;top:calc(8px + 62% * .846);width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:#F46744;box-shadow:0 0 0 0 rgba(244,103,68,.6);opacity:0;animation:lo-rf-dot 6s ease infinite}
.mxp .lo-rf-al{display:grid;gap:8px}
.mxp .lo-rf-a{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:12px;background:#fff;color:#0E2A47;font-size:14px;opacity:0;transform:translateX(24px);animation:6s cubic-bezier(.2,.8,.2,1) infinite}
.mxp .lo-rf-a:nth-child(1){animation-name:lo-rf-a1}.mxp .lo-rf-a:nth-child(2){animation-name:lo-rf-a2}
.mxp .lo-rf-bell{flex:none;width:26px;height:26px;border-radius:8px;background:#0E2A47;color:#7FDCEC;display:inline-flex;align-items:center;justify-content:center}
.mxp .lo-rf-a b{font-weight:700;min-width:0;display:flex;flex-direction:column;line-height:1.2}
.mxp .lo-rf-a small{font-size:10.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#5E7A8C}
.mxp .lo-rf-a em{margin-left:auto;font-style:normal;font-weight:800;color:#127C8F;white-space:nowrap}
@keyframes lo-rf-draw{0%{stroke-dashoffset:1}55%,95%{stroke-dashoffset:0}100%{stroke-dashoffset:0;opacity:.4}}
@keyframes lo-rf-dot{0%,40%{opacity:0;transform:scale(.3)}45%{opacity:1;transform:scale(1.25);box-shadow:0 0 0 0 rgba(244,103,68,.6)}60%{transform:scale(1);box-shadow:0 0 0 14px rgba(244,103,68,0)}95%{opacity:1}100%{opacity:0}}
@keyframes lo-rf-a1{0%,50%{opacity:0;transform:translateX(24px)}57%,95%{opacity:1;transform:none}100%{opacity:0}}
@keyframes lo-rf-a2{0%,60%{opacity:0;transform:translateX(24px)}67%,95%{opacity:1;transform:none}100%{opacity:0}}
.mxp .lo-wh-stage{display:flex;align-items:center;gap:16px;flex:1 1 auto}
.mxp .lo-wh-house{flex:none;width:92px;height:92px;border-radius:22px;background:rgba(127,220,236,.08);border:1px solid rgba(127,220,236,.25);display:flex;align-items:center;justify-content:center}
.mxp .lo-wh-house svg{width:64px;height:64px}
.mxp .lo-wh-draw{stroke:#7FDCEC;stroke-width:3.2;stroke-dasharray:1;stroke-dashoffset:1;animation:lo-wh-draw 6s ease infinite}
.mxp .lo-wh-roof{fill:#1C97AE;opacity:0;animation:lo-wh-fill 6s ease infinite}
.mxp .lo-wh-door{fill:#F46744;opacity:0;transform-origin:32px 54px;animation:lo-wh-door 6s ease infinite}
.mxp .lo-wh-docs{position:relative;flex:1 1 auto;min-width:0;display:grid;gap:6px}
.mxp .lo-wh-doc{display:flex;align-items:center;gap:9px;padding:8px 12px;border-radius:10px;background:#fff;color:#0E2A47;font-size:14px;font-weight:700;box-shadow:0 8px 18px rgba(2,2,21,.3);opacity:0;animation:6s cubic-bezier(.2,.9,.25,1.15) infinite}
.mxp .lo-wh-doc i{flex:none;width:12px;height:15px;border-radius:2px;border:2px solid #1C97AE;box-sizing:border-box;position:relative}
.mxp .lo-wh-doc:nth-child(1){animation-name:lo-wh-d1;--r:-2deg}.mxp .lo-wh-doc:nth-child(2){animation-name:lo-wh-d2;--r:1.5deg}.mxp .lo-wh-doc:nth-child(3){animation-name:lo-wh-d3;--r:-1deg}.mxp .lo-wh-doc:nth-child(4){animation-name:lo-wh-d4;--r:2deg}
@keyframes lo-wh-draw{0%{stroke-dashoffset:1}25%,95%{stroke-dashoffset:0}100%{stroke-dashoffset:0;opacity:.4}}
@keyframes lo-wh-fill{0%,22%{opacity:0}32%,95%{opacity:.55}100%{opacity:0}}
@keyframes lo-wh-door{0%,26%{opacity:0;transform:scaleY(0)}34%,95%{opacity:1;transform:none}100%{opacity:0}}
@keyframes lo-wh-d1{0%,30%{opacity:0;transform:translate(-40px,30px) rotate(-14deg) scale(.8)}38%,95%{opacity:1;transform:rotate(var(--r))}100%{opacity:0}}
@keyframes lo-wh-d2{0%,38%{opacity:0;transform:translate(-40px,30px) rotate(-14deg) scale(.8)}46%,95%{opacity:1;transform:rotate(var(--r))}100%{opacity:0}}
@keyframes lo-wh-d3{0%,46%{opacity:0;transform:translate(-40px,30px) rotate(-14deg) scale(.8)}54%,95%{opacity:1;transform:rotate(var(--r))}100%{opacity:0}}
@keyframes lo-wh-d4{0%,54%{opacity:0;transform:translate(-40px,30px) rotate(-14deg) scale(.8)}62%,95%{opacity:1;transform:rotate(var(--r))}100%{opacity:0}}
@media (max-width:420px){.mxp .lo-wh-house{width:52px;height:52px;border-radius:14px}.mxp .lo-wh-house svg{width:38px;height:38px}.mxp .lo-wh-stage{gap:10px}.mxp .lo-wh-doc{font-size:13px;padding:7px 10px;gap:8px}.mxp .lo-rf-a{font-size:13px;gap:2px 8px;padding:8px 12px;flex-wrap:wrap}.mxp .lo-rf-bell{display:none}.mxp .lo-rf-a b{white-space:nowrap}.mxp .lo-rf-a small{letter-spacing:.06em}.mxp .lo-rov-done{font-size:13px;padding:8px 12px}}
.mxp .lo-rov-done,.mxp .lo-wh-doc,.mxp .lo-rf-a b{text-wrap:balance}
.mxp .lo-rov-bar{height:6px;border-radius:999px;background:rgba(255,255,255,.12);overflow:hidden}
.mxp .lo-rov-bar i{display:block;height:100%;width:100%;border-radius:999px;background:linear-gradient(90deg,#1C97AE,#7FDCEC);transform-origin:left;animation:lo-rov-fill 6s cubic-bezier(.4,0,.2,1) infinite}
.mxp .lo-rov-steps{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.mxp.mxp .lo-rov-steps>li{display:flex !important;align-items:center;gap:10px;margin:0 !important;padding:0 !important;font-size:14.5px;font-weight:600;color:#E3F5F9;opacity:.35;animation:6s ease infinite}
.mxp.mxp .lo-rov-steps>li::before{content:none !important}
.mxp .lo-rov-ic{position:relative;flex:none;width:18px;height:18px;border-radius:50%;border:2px solid rgba(127,220,236,.5);box-sizing:border-box;animation:6s ease infinite}
.mxp .lo-rov-ic::after{content:"";position:absolute;left:4px;top:1px;width:4px;height:8px;border:solid #0E2A47;border-width:0 2px 2px 0;transform:rotate(45deg);opacity:0;animation:6s ease infinite}
.mxp.mxp .lo-rov-steps>li:nth-child(1){animation-name:lo-rov-s1}.mxp.mxp .lo-rov-steps>li:nth-child(2){animation-name:lo-rov-s2}.mxp.mxp .lo-rov-steps>li:nth-child(3){animation-name:lo-rov-s3}.mxp.mxp .lo-rov-steps>li:nth-child(4){animation-name:lo-rov-s4}
.mxp .lo-rov-steps>li:nth-child(1) .lo-rov-ic{animation-name:lo-rov-i1}.mxp .lo-rov-steps>li:nth-child(2) .lo-rov-ic{animation-name:lo-rov-i2}.mxp .lo-rov-steps>li:nth-child(3) .lo-rov-ic{animation-name:lo-rov-i3}.mxp .lo-rov-steps>li:nth-child(4) .lo-rov-ic{animation-name:lo-rov-i4}
.mxp .lo-rov-steps>li:nth-child(1) .lo-rov-ic::after{animation-name:lo-rov-c1}.mxp .lo-rov-steps>li:nth-child(2) .lo-rov-ic::after{animation-name:lo-rov-c2}.mxp .lo-rov-steps>li:nth-child(3) .lo-rov-ic::after{animation-name:lo-rov-c3}.mxp .lo-rov-steps>li:nth-child(4) .lo-rov-ic::after{animation-name:lo-rov-c4}
.mxp .lo-rov-done{display:inline-flex;align-self:flex-start;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;background:#F46744;color:#0E2A47;font-size:14px;font-weight:800;opacity:0;transform:translateY(8px);animation:lo-rov-done 6s ease infinite}
.mxp .lo-rov-done span{width:18px;height:18px;border-radius:50%;background:#0E2A47;color:#fff;font-size:11px;display:inline-flex;align-items:center;justify-content:center}
@keyframes lo-scan{0%,20%{transform:translateX(-100%)}60%,100%{transform:translateX(100%)}}
@keyframes lo-rov-fill{0%{transform:scaleX(0)}70%,95%{transform:scaleX(1)}100%{transform:scaleX(1);opacity:.4}}
@keyframes lo-rov-s1{0%,5%{opacity:.35}12%,95%{opacity:1}100%{opacity:.35}}
@keyframes lo-rov-s2{0%,22%{opacity:.35}29%,95%{opacity:1}100%{opacity:.35}}
@keyframes lo-rov-s3{0%,39%{opacity:.35}46%,95%{opacity:1}100%{opacity:.35}}
@keyframes lo-rov-s4{0%,56%{opacity:.35}63%,95%{opacity:1}100%{opacity:.35}}
@keyframes lo-rov-i1{0%,8%{background:transparent;border-color:rgba(127,220,236,.5)}14%,95%{background:#7FDCEC;border-color:#7FDCEC}100%{background:transparent}}
@keyframes lo-rov-i2{0%,25%{background:transparent;border-color:rgba(127,220,236,.5)}31%,95%{background:#7FDCEC;border-color:#7FDCEC}100%{background:transparent}}
@keyframes lo-rov-i3{0%,42%{background:transparent;border-color:rgba(127,220,236,.5)}48%,95%{background:#7FDCEC;border-color:#7FDCEC}100%{background:transparent}}
@keyframes lo-rov-i4{0%,59%{background:transparent;border-color:rgba(127,220,236,.5)}65%,95%{background:#7FDCEC;border-color:#7FDCEC}100%{background:transparent}}
@keyframes lo-rov-c1{0%,10%{opacity:0}14%,95%{opacity:1}100%{opacity:0}}
@keyframes lo-rov-c2{0%,27%{opacity:0}31%,95%{opacity:1}100%{opacity:0}}
@keyframes lo-rov-c3{0%,44%{opacity:0}48%,95%{opacity:1}100%{opacity:0}}
@keyframes lo-rov-c4{0%,61%{opacity:0}65%,95%{opacity:1}100%{opacity:0}}
@keyframes lo-rov-done{0%,70%{opacity:0;transform:translateY(8px)}76%,95%{opacity:1;transform:none}100%{opacity:0}}
@media (prefers-reduced-motion:reduce){.mxp .lo-rov *,.mxp .lo-rov::after,.mxp .lo-rov *::after{animation:none !important}.mxp.mxp .lo-rov-steps>li,.mxp .lo-rov-done,.mxp .lo-rf-a,.mxp .lo-rf-dot,.mxp .lo-wh-doc,.mxp .lo-wh-door{opacity:1;transform:none}.mxp .lo-wh-roof{opacity:.55}.mxp .lo-rf-ln,.mxp .lo-wh-draw{stroke-dashoffset:0}.mxp .lo-rov-ic{background:#7FDCEC}.mxp .lo-rov-ic::after{opacity:1}}

.mxp .lo-bar-row{display:grid;grid-template-columns:96px 1fr;align-items:center;gap:12px;font-size:14px;font-weight:600;color:#B8C7D3}
.mxp .lo-bar-row i{display:block;height:14px;border-radius:999px;background:rgba(255,255,255,.22);width:var(--w);transform-origin:left;transition:transform 1s cubic-bezier(.2,.8,.2,1) .2s}
.mxp .lo-bar-new{color:#7FDCEC}
.mxp .lo-bar-new i{background:linear-gradient(90deg,#1C97AE,#7FDCEC);box-shadow:0 0 18px rgba(127,220,236,.45)}
.mxp .lo-tchips{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.mxp .lo-tchips span{font-size:13px;font-weight:600;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);color:#E3F5F9}
.mxp .lo-viz-loop{margin-top:auto;padding-top:20px;display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:center;gap:4px 8px;font-size:13px;font-weight:600;max-width:340px}
.mxp .lo-viz-loop span{padding:7px 10px;border-radius:10px;background:rgba(255,255,255,.08);color:#E3F5F9;text-align:center;white-space:nowrap}
.mxp .lo-viz-loop b.v{justify-self:center;line-height:1}
.mxp .lo-viz-loop b{color:#7FDCEC;font-weight:700}
.mxp .lo-viz-loop .lo-loop-back{background:#F46744;color:#0E2A47}
.mxp .lo-viz-play{margin-top:auto;padding-top:20px;display:flex;align-items:center;gap:12px;font-size:14px;font-weight:600;color:#7FDCEC}
.mxp .lo-play{position:relative;flex:none;width:48px;height:48px;border-radius:50%;background:#F46744;box-shadow:0 0 0 0 rgba(244,103,68,.5);animation:lo-pulse 2.4s ease-out infinite}
.mxp .lo-play::after{content:"";position:absolute;left:19px;top:15px;border-left:14px solid #0E2A47;border-top:9px solid transparent;border-bottom:9px solid transparent}
@keyframes lo-pulse{0%{box-shadow:0 0 0 0 rgba(244,103,68,.5)}70%{box-shadow:0 0 0 16px rgba(244,103,68,0)}100%{box-shadow:0 0 0 0 rgba(244,103,68,0)}}
.mxp .lo-viz-toasts{margin-top:auto;padding-top:18px;display:flex;flex-wrap:wrap;gap:10px}
.mxp .lo-toast{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:14px;background:#fff;color:#0E2A47;font-size:14px;font-weight:700;box-shadow:0 10px 24px rgba(0,0,0,.2);transition:opacity .5s ease calc(.3s + var(--k) * .35s),transform .5s cubic-bezier(.2,.8,.2,1) calc(.3s + var(--k) * .35s)}
.mxp .lo-toast-ic{width:22px;height:22px;border-radius:50%;background:#1C97AE;color:#fff;display:inline-flex;align-items:center;justify-content:center}
/* reveal (armed only by JS) */
.mxp .lo-bento.arm .lo-bar-row i{transform:scaleX(0)}
.mxp .lo-bento.arm .lo-toast{opacity:0;transform:translateY(12px)}
.mxp .lo-bento.arm.in .lo-bar-row i{transform:none}
.mxp .lo-bento.arm.in .lo-toast{opacity:1;transform:none}
@media (max-width:980px){.mxp .lo-bento{grid-template-columns:1fr 1fr;grid-template-areas:"big big" "crm uni" "aut aut"}}
@media (max-width:640px){.mxp .lo-bento{grid-template-columns:1fr;grid-template-areas:"big" "crm" "uni" "aut"}.mxp .lo-b{padding:24px}.mxp .lo-bar-row{grid-template-columns:84px 1fr}}
@media (prefers-reduced-motion:reduce){.mxp .lo-play{animation:none}.mxp .lo-bento.arm .lo-bar-row i,.mxp .lo-bento.arm .lo-toast{opacity:1 !important;transform:none !important;transition:none !important}}
"""
tools_sec = section('lo-tools', 'Tools and technology', 'Tools that close business and build repeat business.', tools, bg='radial-gradient(120% 90% at 85% 0%, #145A75 0%, #0E2A47 55%, #0B2340 100%)', dark=True,
                    lede='Moxie has invested significantly to give its team cutting-edge technology, including proprietary tools available only to Moxie team members. Our systems are integrated, automated and powered by AI, maximizing your effectiveness and minimizing wasted time.')

# ---------------- PARTNER RELATIONSHIPS
PARTNERS = [
    ('shield', 'Insurance network', 'Faster clear to close',
     'Our insurance network helps clients get the best price on homeowners insurance, so they’re fully protected while keeping their monthly payment as low as possible, with no work required from them.'),
    ('clock', 'AMC relationships', 'Faster appraisals',
     'Appraisal management relationships with local market experts speed up appraisal turnaround times.'),
    ('home', 'Home services', 'No cost to the borrower',
     'Help with the move and getting the new home set up, at no cost to the borrower, so there’s less stress and the house feels like home sooner.'),
]
partner_cards = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 44px">' + ''.join(
    f'<article class="lo-pr"><div style="display: flex; align-items: center; justify-content: space-between; gap: 12px">'
    f'<span class="lo-pr-ic" aria-hidden="true"><span>{ICON[ic]}</span></span><span class="lo-pr-tag">{tag}</span></div>'
    f'<h3>{t}</h3><p>{d}</p></article>' for ic, t, tag, d in PARTNERS) + '</div>'
partners_sec = section('lo-partners', 'Partner relationships', 'Relationships that close loans faster and make clients happier.', partner_cards,
    lede='Moxie’s partner network takes work off your plate and your clients’ plates, from insurance to appraisal to moving day.')
PARTNER_CSS = r"""
.mxp .lo-pr{background:#fff;border:1px solid #DCE6EB;border-radius:24px;padding:28px;display:flex;flex-direction:column;gap:10px;transition:transform .3s cubic-bezier(.2,.8,.2,1),box-shadow .3s,border-color .3s}
.mxp .lo-pr:hover{transform:translateY(-4px);border-color:#1C97AE;box-shadow:0 18px 40px rgba(14,42,71,.12)}
.mxp .lo-pr-ic{width:52px;height:52px;border-radius:16px;background:#0E2A47;color:#7FDCEC;display:inline-flex;align-items:center;justify-content:center}
.mxp .lo-pr-ic>span{width:26px;height:26px;display:block}
.mxp .lo-pr-tag{font-size:13px;font-weight:700;letter-spacing:.04em;color:#127C8F;background:#E3F5F9;border-radius:999px;padding:6px 12px;white-space:nowrap}
@media (max-width:420px){.mxp .lo-pr-tag{white-space:normal;text-align:center;text-wrap:balance;font-size:12px;min-width:0}}
.mxp .lo-pr h3{margin:8px 0 0;font-size:22px;line-height:1.2}
.mxp .lo-pr p{margin:0;font-size:16px;color:#4A5868}
"""

# ---------------- MARKETING (reuse AD cards and images)
mk = re.search(r'\s*<!-- WHAT AGENTS GET -->.*?</section>', ad.body, re.S)
assert mk, 'AD marketing section not found'
mk = mk.group(0).replace('<!-- WHAT AGENTS GET -->', '<!-- CO-MARKETING -->')
mk = re.sub(r'aria-labelledby="ad-tools"', 'aria-labelledby="lo-mkt"', mk).replace('id="ad-tools"', 'id="lo-mkt"')
mk = re.sub(r'<section(?![^>]*\bid=)', '<section id="marketing"', mk, count=1)
mk = mk.replace('>Marketing support<', '>Co-marketing<').replace('Ready-to-use Moxie marketing for your area, every month.', 'Marketing your agent partners will actually use.')
mk = re.sub(r'\s*<p[^>]*>Plus approval pages and a direct line to a licensed Moxie loan officer, live within 24 hours\.</p>', '', mk)
mk = mk.replace('Marketing your agent partners will actually use.</h2>', 'Marketing your agent partners will actually use.</h2>\n        <p style="margin: 14px 0 0; font-size: 19px; color: #4A5868">Created by Moxie, personalized to you.</p>', 1)
mk = mk.replace('>Listing flyers</h3>', '>Flyers, guides and special offers</h3>').replace('Show buyers the payment with a seller-paid buydown.', 'Listing and buydown flyers, buyer guides and special offers that show buyers the savings.')
assert 'lo-mkt' in mk and 'Co-marketing' in mk and 'personalized to you' in mk and 'Flyers, guides' in mk

# ---------------- TRAINING
TRAIN = [
    ('Processing and consultants', 'Dedicated loan processors plus mortgage consultants to help structure tough scenarios.'),
    ('Live back-office support', 'Live support 6 AM–6 PM AZT for payroll, marketing, IT, compliance, licensing, training and HR, plus legal and accounting handled for you.'),
    ('A mentor on your deals', 'Training and deal strategy, an accountability partner, and direction when a file gets complicated.'),
    ('Moxie University', 'Courses on products, pricing strategy and Moxie’s tools, available whenever you need them.'),
    ('Monday and Friday huddles', 'Live team calls at noon ET for market updates, new tools and deal reviews.'),
    ('Annual mortgage conference', 'Learn from top producers and lenders, and meet the rest of the team.'),
]
train = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article style="background: rgba(255,255,255,.06); border: 1px solid rgba(127,220,236,.25); border-radius: 20px; padding: 26px"><h3 style="margin: 0; font-size: 21px; color: #ffffff">{t}</h3><p style="margin: 8px 0 0; color: #D3E3EC; font-size: 16px">{d}</p></article>'
    for t, d in TRAIN) + '</div>'
train_sec = section('lo-train', 'Support and training', 'You’re never on your own with a tough file.', train, bg='#0E2A47', dark=True)


# ---------------- PAY + BENEFITS
BENEFITS = [
    ('pct', 'Generous compensation', 'Compensation packages built to reward production, set out in a written agreement.'),
    ('cash', 'Everyday payday', 'Commission is paid as your loans close, not on a monthly cycle.'),
    ('shield', 'Full health insurance', 'Medical, dental and vision coverage for eligible employees.'),
    ('trend', '401(k) and HSA', 'Plan for retirement and set aside pre-tax dollars for health costs, for eligible employees.'),
    ('grid', 'W-2 or 1099', 'Choose the employment structure that fits your business.'),
]
ben_cards = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article class="mxa-card" style="{CARD}; display: flex; flex-direction: column; gap: 10px">'
    f'<span style="width: 48px; height: 48px; border-radius: 14px; background: #FDE7E1; color: #C2482A; display: inline-flex; align-items: center; justify-content: center"><span style="width: 24px; height: 24px; display: block">{ICON[ic]}</span></span>'
    f'<h3 style="margin: 6px 0 0; font-size: 21px">{t}</h3><p style="margin: 0; color: #4A5868; font-size: 16px">{d}</p></article>' for ic, t, d in BENEFITS) + '</div>'
ben_sec = section('lo-pay', 'Pay and benefits', 'Generous compensation, with full benefits.', lede='Packages built to reward production, paid as your loans close, with full health insurance and a 401(k) for eligible employees.', inner=
    ben_cards + '')

# ---------------- REVIEWS (reuse AD track)
rv = re.search(r'\s*<!-- AGENT REVIEWS -->.*?</section>', ad.body, re.S)
assert rv
rv = rv.group(0).replace('aria-labelledby="ad-reviews"', 'aria-labelledby="lo-reviews"').replace('id="ad-reviews"', 'id="lo-reviews"')
rv = rv.replace('Top agents say their clients are in great hands.', 'Agents trust Moxie loan officers with their buyers.')
rv = rv.replace('style="background: #F4F8FA; padding: 92px 24px"', 'style="background: #F4F8FA; padding: 92px 24px"', 1)
assert 'lo-reviews' in rv

# ---------------- FAQ (visible + FAQPage schema)
FAQ = [
    ('Does Moxie provide leads or referrals?',
     'Yes. Moxie builds relationships with key enterprise accounts in its markets, which generate warm opportunities for Moxie loan officers, alongside introductions from Moxie Area Directors and agent partners. Since Moxie’s inception, 82% of its business has been company-generated and 86% has been purchase business. Referral volume varies by market and isn’t guaranteed, so you’ll still grow your own network, with Moxie co-marketing to help.'),
    ('What is it like to be a loan officer at Moxie Mortgage?',
     'Moxie Mortgage is a wholesale mortgage brokerage and a division of NEXA Mortgage. Moxie loan officers price loans across 300+ wholesale investors, get introductions from Moxie Area Directors and agent partners, use Moxie’s client tools and CRM, and work with a mentor and a team that meets twice a week.'),
    ('How are Moxie loan officers paid?',
     'Moxie offers generous compensation packages, paid on closed loans under a written agreement, and commission is paid as each loan closes. W-2 and 1099 options are available, and eligible employees get full health insurance (medical, dental and vision), a 401(k) and an HSA. We walk through the full plan, including splits and any costs you’re responsible for, on your intro call. As federal rules require, loan officer pay is never based on a loan’s rate or terms.'),
    ('Which lenders and loan programs can I offer?',
     'Moxie loan officers have access to more than 300 wholesale investors and thousands of programs: conventional, FHA, VA, USDA and jumbo loans, HELOCs and second mortgages, bank statement and other non-QM loans, DSCR and fix-and-flip loans for investors, construction, renovation and reverse mortgages, and cross-collateralized options.'),
    ('Who processes and underwrites my loans?',
     'Moxie processes loans in-house, and Moxie loan officers get priority underwriting and account support with key investors across product types. You also get full transparency on pricing and the investor purchase advice on every loan.'),
    ('What technology do Moxie loan officers use?',
     'Moxie has invested significantly to give its team cutting-edge technology, including proprietary tools available only to Moxie team members. Our systems are integrated, automated and powered by AI, maximizing your effectiveness and minimizing wasted time. That includes Arive for loan origination, Lofty for CRM and follow-up, and Moxie’s proprietary client tools, including a debt consolidation worksheet with MISMO 3.4 credit import, ARM vs. fixed and buydown comparisons, and an effective rate calculator.'),
    ('What do I need to join, and which states can I originate in?',
     'You need an active NMLS license in good standing. Moxie loan officers are sponsored through NEXA Mortgage in the states where they’re licensed. NEXA isn’t licensed in New York or Massachusetts yet, so we can’t sponsor originators there today.'),
    ('What training and support will I get?',
     'Dedicated loan processors and mortgage consultants, a back office that handles HR, legal, compliance, marketing, accounting, payroll and licensing, Moxie University for on-demand training, Monday and Friday team huddles at noon ET, an annual mortgage conference, and a mentor for deal strategy and accountability.'),
    ('How do I apply?',
     'Fill out the short application on this page. We’ll reach out to book a 20-minute intro call with Robert Lucido Jr, Moxie’s founder, to review compensation, the referral pipeline and next steps.'),
]
faq_sec = section('lo-faq', 'Questions', 'Loan officer FAQs.', '<div style="margin-top: 36px; max-width: 900px">' + faq_details(FAQ) + '</div>')

# ---------------- APPLY (steps + form + popup)
CONSENT = ad.CONSENT
def appform(k):
    f = lambda n: f'mxa-{k}-{n}'
    return f'''<form class="mxa-f" data-mxa-form novalidate>
          <div class="full"><label for="{f('name')}">Name *</label><input id="{f('name')}" name="name" type="text" autocomplete="name" required maxlength="60"></div>
          <div><label for="{f('phone')}">Phone *</label><input id="{f('phone')}" name="phone" type="tel" autocomplete="tel" required maxlength="20"></div>
          <div><label for="{f('email')}">Email *</label><input id="{f('email')}" name="email" type="email" autocomplete="email" required maxlength="80"></div>
          <div><label for="{f('nmls')}">NMLS # *</label><input id="{f('nmls')}" name="nmls" type="text" inputmode="numeric" required maxlength="12"></div>
          <div><label for="{f('years')}">Years originating *</label><input id="{f('years')}" name="years" type="text" inputmode="numeric" required maxlength="10"></div>
          <div><label for="{f('units')}">Loans closed, last 12 months *</label><input id="{f('units')}" name="units" type="text" inputmode="numeric" required maxlength="20"></div>
          <div><label for="{f('volume')}">Volume, last 12 months *</label><input id="{f('volume')}" name="volume" type="text" inputmode="decimal" required maxlength="30"></div>
          <div class="full"><span class="mxa-lbl" id="{f('states')}-l">States you’re licensed in *</span><details class="mxa-st"><summary aria-labelledby="{f('states')}-l {f('states')}-v"><span id="{f('states')}-v" class="mxa-st-v">Select states</span></summary><div class="mxa-st-p" role="group" aria-labelledby="{f('states')}-l">{ad.ST_BOXES}</div></details><input type="hidden" name="states" value=""></div>
          <div class="full"><label for="{f('co')}">Current company</label><input id="{f('co')}" name="company" type="text" autocomplete="organization" maxlength="80"></div>
          <div class="full"><label for="{f('msg')}">Anything else we should know?</label><textarea id="{f('msg')}" name="message" rows="3" maxlength="1000"></textarea></div>
          <div class="mxa-hp" aria-hidden="true"><label for="{f('web')}">Website</label><input id="{f('web')}" name="website" type="text" tabindex="-1" autocomplete="off"></div>
          <div class="full mxa-consent"><input id="{f('ok')}" name="consent" type="checkbox" required><label for="{f('ok')}">{CONSENT}</label></div>
          <p class="full mxa-err" role="alert" hidden></p>
          <div class="full"><button type="submit">Submit application</button></div>
        </form>'''

STEPS = [
    ('#ffffff', '20-minute call with our founder', 'Robert walks you through compensation, the referral pipeline and how Moxie fits your business.'),
    ('rgba(252, 200, 184, 0.92)', 'Sponsorship and setup', 'Move your NMLS sponsorship to NEXA and get set up in Arive, Lofty and pricing.'),
    ('#F9A48D', 'White-glove onboarding', 'Get fully trained on everything, including your lender relationships and every tool at your disposal.'),
    ('#F46744', 'Start originating', 'Work your first files with your mentor and join the Monday and Friday huddles.'),
]
steps = ''.join(
    f'<li style="display: flex; gap: 18px"><span aria-hidden="true" style="flex: none; width: 44px; height: 44px; border-radius: 50%; background: {c}; color: #0E2A47; font-weight: 800; font-size: 20px; display: inline-flex; align-items: center; justify-content: center">{i}</span>'
    f'<div><h3 style="margin: 0; font-size: 20px">{t}</h3><p style="margin: 4px 0 0; color: #D3E3EC">{d}</p></div></li>' for i, (c, t, d) in enumerate(STEPS, 1))
apply_sec = f'''
  <section id="apply" aria-labelledby="lo-apply" style="background: {GRAD}; color: #ffffff; padding: 92px 24px">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 56px; align-items: flex-start">
      <div style="flex: 1 1 440px; min-width: 0">
        <p style="{EYEBROW_L}">Get started</p>
        <h2 id="lo-apply" style="{H2}">Four steps to joining Moxie.</h2>
        <ol class="ad-steps" style="list-style: none; padding: 0; margin: 32px 0 0; display: flex; flex-direction: column; gap: 22px">{steps}</ol>
      </div>
      <div class="mxa-form" id="mxa-apply-card">
        <h3 id="lo-form-h">Apply to join Moxie as a loan officer</h3>
        <p>We’ll review your application and reach out to book your intro call.</p>
        {appform('card')}
      </div>
    </div>
  </section>'''

disclosures = '''
  <section aria-label="Disclosures" style="max-width: 1200px; margin: 0 auto; padding: 40px 24px 56px; font-size: 13px; line-height: 1.55; color: #4A5868">
    <p style="margin: 0 0 8px">Loan officers are compensated on closed loans under a written agreement that complies with federal loan originator compensation rules and state law; compensation is never based on a loan’s rate or terms. Referral volume varies by market and is not guaranteed. Consumers are always free to choose their lender and settlement service providers.</p>
    <p style="margin: 0 0 8px"><sup>1</sup> Based on Moxie Mortgage’s apples-to-apples comparison of weekly rates against Rocket Mortgage from November 2025 to November 2026; average difference 0.559%. Rate and savings vary and depend on borrower’s qualification, property specifics, and market conditions. <sup>2</sup> Moxie average clear-to-close time; the industry average was 38 days (ICE Mortgage Technology, May 2026). Not a commitment to lend; all loans are subject to credit approval. <sup>3</sup> Share of Moxie Mortgage’s business from inception through November 2026: company-generated versus loan officer–sourced, and purchase versus refinance. Past results don’t guarantee future referral volume.</p>
    <p style="margin: 0 0 8px">Compensation and benefit eligibility depend on employment type and are set out in your written agreement. W-2 and 1099 options are available. We walk through the full plan on your intro call.</p>
    <p style="margin: 0 0 8px">Program availability varies by state, investor and borrower qualification.</p>
    <p style="margin: 0">Moxie Mortgage, a division of NEXA Mortgage, LLC · NMLS #1660690 · AZMB 0944059 · Equal Housing Lender</p>
  </section>'''

body = hero + jump_nav + pain_sec + deals_sec + pay_sec + products_sec + tools_sec + partners_sec + mk + about_band + founder_sec + rv + faq_sec + apply_sec + disclosures
body += f'''
<dialog class="mxa-dlg" id="mxa-dlg" aria-labelledby="mxa-dlg-h"><div>
  <button type="button" class="mxa-x" data-mxa-close aria-label="Close">×</button>
  <h3 id="mxa-dlg-h">Apply to join Moxie as a loan officer</h3>
  <p class="mxa-sub">Takes about a minute. We’ll reach out to book your 20-minute intro call.</p>
  {appform('pop')}
</div></dialog>'''
assert '{{' not in body

# ---------------- SCRIPT: timeline, reviews, application (from the AD page script, re-pointed)
s = ad.script
s = s[s.index('// ---- timeline'):]
s = s.replace("MX.track('ad_apply_open'", "MX.track('lo_apply_open'").replace("MX.track('ad_apply_submit'", "MX.track('lo_apply_submit'")
s = s.replace("var req = ['name', 'phone', 'email', 'units', 'volume', 'states'];", "var req = ['name', 'phone', 'email', 'nmls', 'years', 'units', 'volume', 'states'];")
s = s.replace("Please select the states you operate in.", "Please select the states you’re licensed in.")
old_payload = s[s.index('    var payload = {'):s.index('    btn.disabled = true;')]
new_payload = """    var payload = { name: v('name'), phone: v('phone'), email: v('email'), cta: 'LO Applicant', leadTypes: [7], tags: v('states').split(', ').filter(Boolean), source: 'MoxieMortgage.com — Loan Officer page',
      consent: true, secret: SECRET, message: v('message'), pageUrl: location.href.split('#')[0], submittedAt: new Date().toISOString(),
      fields: { 'Application': 'Loan Officer', 'NMLS #': v('nmls'), 'Years originating': v('years'), 'Loans closed, last 12 months': v('units'),
        'Volume, last 12 months': v('volume'), 'Licensed states': v('states'), 'Current company': v('company'), 'Consent text': consentText },
      sheet: 'lo-applications',
      sheetRow: { 'Timestamp': '', 'Name': v('name'), 'Email': v('email'), 'Phone Number': v('phone'),
        'What was your total loan volume over the previous 12 months?': v('volume'),
        'What was your total loan units over the previous 12 months?': v('units'),
        'NMLS #': v('nmls'), 'Years originating': v('years'), 'Licensed states': v('states'), 'Current company': v('company'),
        'Anything else we should know?': v('message'), 'Application source': 'Website: moxiemortgage.com/loanofficer' } };
"""
s = s.replace(old_payload, new_payload).replace('tags the lead "CTA: AD Application"', 'tags the lead "CTA: LO Applicant" (Agent lead type) and logs the application to the Loan Officer Application (Responses) sheet')
assert "cta: 'LO Applicant'" in s and 'AD Application' not in s
s = s.replace('Thanks! We’ll review it and reach out to book your onboarding call.', 'Thanks! We’ll review it and reach out to book your intro call.')
s = s.replace('// ---- timeline:', '// ---- referral flow:')
s += '''
// ---- quick-jump tabs: pin under the site header while scrolling (JS, since Lofty's body overflow breaks CSS sticky), highlight the section in view
(function () {
  var nav = root.querySelector('.lo-jump'); if (!nav) return;
  var main = root.querySelector('.mxa-main') || root;
  var ph = document.createElement('div'); ph.className = 'lo-jump-ph'; nav.parentNode.insertBefore(ph, nav);
  var hdrBottom = function () {
    var h = document.getElementById('mx-header');
    if (!h) return 0;
    var cs = getComputedStyle(h); if (cs.position !== 'fixed' && cs.position !== 'sticky') return 0;
    return Math.max(0, h.getBoundingClientRect().bottom);
  };
  var desktop = function () { return window.matchMedia ? matchMedia('(min-width: 901px)').matches : true; };
  var pinned = false;
  var update = function () {
    var t = hdrBottom();
    nav.style.setProperty('--lo-jt', t + 'px');
    var pr = ph.getBoundingClientRect(), mr = main.getBoundingClientRect();
    var want = desktop() && pr.top <= t && mr.bottom > t + nav.offsetHeight + 40;
    if (want !== pinned) {
      pinned = want;
      ph.style.height = want ? nav.offsetHeight + 'px' : '0px';
      nav.classList.toggle('pinned', want);
    }
  };
  var raf = 0; var onScroll = function () { if (!raf) raf = requestAnimationFrame(function () { raf = 0; update(); }); };
  window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); update();
  // the site header switches to fixed on its own scroll handler; re-measure whenever it changes
  var hdrEl = document.getElementById('mx-header');
  if (hdrEl && 'MutationObserver' in window) new MutationObserver(function () { onScroll(); setTimeout(onScroll, 180); setTimeout(onScroll, 400); }).observe(hdrEl, { attributes: true, attributeFilter: ['class', 'style'] });
  if (hdrEl) { hdrEl.addEventListener('transitionend', onScroll); hdrEl.addEventListener('animationend', onScroll); }
  var hw = document.getElementById('mx-header-wrap');
  if (hw && hw !== hdrEl && 'MutationObserver' in window) new MutationObserver(onScroll).observe(hw, { attributes: true, attributeFilter: ['class', 'style'] });
  var links = [].slice.call(nav.querySelectorAll('a[data-jump]'));
  var go = function (id) {
    var el = root.querySelector('#' + id); if (!el) return;
    var off = hdrBottom() + (desktop() ? nav.offsetHeight : 0) + 8;
    window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - off, behavior: 'smooth' });
  };
  var sel = nav.querySelector('[data-jump-select]');
  if (sel) { sel.selectedIndex = -1; sel.addEventListener('change', function () { go(sel.value); }); }
  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      var el = root.querySelector('#' + a.getAttribute('data-jump')); if (!el) return;
      e.preventDefault();
      var off = hdrBottom() + (desktop() ? nav.offsetHeight : 0) + 8;
      window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - off, behavior: 'smooth' });
      if (history.replaceState) history.replaceState(null, '', '#' + a.getAttribute('data-jump'));
    });
  });
  if (!('IntersectionObserver' in window)) return;
  var cur = null;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) cur = e.target.id; });
    links.forEach(function (a) { a.setAttribute('aria-current', a.getAttribute('data-jump') === cur ? 'true' : 'false'); });
  }, { rootMargin: '-35% 0px -60% 0px' });
  links.forEach(function (a) { var el = root.querySelector('#' + a.getAttribute('data-jump')); if (el) io.observe(el); });
})();

// ---- "Sound familiar?" pick-your-frustrations cards
(function () {
  var cards = [].slice.call(root.querySelectorAll('.lo-fl')); if (!cards.length) return;
  var sum = root.querySelector('.lo-fl-sum'), n = root.querySelector('.lo-fl-n'), grid = root.querySelector('.lo-fl-grid');
  // a quick "flip me" nudge the first time the cards scroll into view
  if (grid && 'IntersectionObserver' in window && !(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    var nio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { setTimeout(function () { if (!grid.classList.contains('picked')) grid.classList.add('nudge'); }, 500); nio.disconnect(); } }); }, { threshold: 0.4 });
    nio.observe(grid);
  }
  var fine = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (fine) cards.forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      var flip = c.getAttribute('aria-pressed') === 'true' ? -1 : 1;
      c.classList.add('tilt');
      c.style.setProperty('--ry', ((x - 0.5) * 12 * flip).toFixed(2) + 'deg');
      c.style.setProperty('--rx', ((0.5 - y) * 10).toFixed(2) + 'deg');
      c.style.setProperty('--mx', (x * 100).toFixed(0) + '%'); c.style.setProperty('--my', (y * 100).toFixed(0) + '%');
    });
    c.addEventListener('pointerleave', function () { c.classList.remove('tilt'); c.style.removeProperty('--rx'); c.style.removeProperty('--ry'); });
  });
  cards.forEach(function (c) {
    c.addEventListener('click', function () {
      c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      var k = cards.filter(function (x) { return x.getAttribute('aria-pressed') === 'true'; }).length;
      if (n) { n.textContent = k; n.classList.remove('lo-bump'); void n.offsetWidth; n.classList.add('lo-bump'); }
      if (sum) sum.classList.toggle('on', k > 0);
      if (grid) grid.classList.add('picked');
      if (window.MX && MX.track && k === 1) MX.track('lo_pain_pick');
    });
  });
  var f = root.querySelector('.lo-fl-cta a[data-jump-link]');
  if (f) f.addEventListener('click', function (e) {
    var t = root.querySelector('a[data-jump="founder"]') ; var el = root.querySelector('#founder');
    if (!el) return; e.preventDefault();
    var h = document.getElementById('mx-header'); var off = (h && getComputedStyle(h).position === 'fixed' ? h.getBoundingClientRect().bottom : 0) + 80;
    window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - off, behavior: 'smooth' });
  });
})();

// ---- tools bento: rotate the client-tool demos (ROVai, refi alerts, welcome home)
(function () {
  var box = root.querySelector('.lo-rov'); if (!box) return;
  var tabs = [].slice.call(box.querySelectorAll('.lo-dtabs span')), sl = [].slice.call(box.querySelectorAll('.lo-sl')); if (sl.length < 2) return;
  var cur = 0, timer = null, still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(i) {
    cur = (i + sl.length) % sl.length;
    sl.forEach(function (s, k) { s.classList.remove('on'); if (tabs[k]) tabs[k].classList.remove('on'); });
    void box.offsetWidth;
    sl[cur].classList.add('on'); if (tabs[cur]) tabs[cur].classList.add('on');
  }
  function play() { clearInterval(timer); if (!still) timer = setInterval(function () { show(cur + 1); }, 6500); }
  tabs.forEach(function (t, k) { t.addEventListener('click', function () { show(k); play(); }); });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { show(cur); play(); } else clearInterval(timer); }); }, { threshold: 0.3 });
    io.observe(box);
  } else play();
})();

// ---- tools bento: grow the bars and drop in the client updates when visible
(function () {
  var bt = root.querySelector('.lo-bento'); if (!bt) return;
  if (!('IntersectionObserver' in window) || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
  if (bt.getBoundingClientRect().top < innerHeight * 0.85) return;
  bt.classList.add('arm');
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { bt.classList.add('in'); io.disconnect(); } }); }, { threshold: 0.2 });
  io.observe(bt);
  setTimeout(function () { bt.classList.add('in'); }, 8000);
})();

// ---- loan program cards: staggered reveal when they scroll into view
(function () {
  var pg = root.querySelector('.lo-pg'); if (!pg) return;
  if (!('IntersectionObserver' in window) || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
  var r = pg.getBoundingClientRect(); if (r.top < innerHeight * 0.9) return;
  pg.classList.add('arm');
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { pg.classList.add('in'); io.disconnect(); } }); }, { threshold: 0.12 });
  io.observe(pg);
  setTimeout(function () { pg.classList.add('in'); }, 8000);
})();
'''
# FAQ: one open at a time is not needed; leave native <details>

DESC = ("Join Moxie Mortgage as a loan officer: 82% of our business is company-generated and 86% is purchase. 300+ wholesale investors, "
        "everyday payday, benefits, and a direct line to our founder. For experienced, licensed LOs.")
page, crumbs = webpage('/loanofficer', 'Loan Officer Careers | Join Moxie Mortgage', DESC, 'Loan Officer Careers', {
    "dateModified": datetime.date.today().isoformat(),
    "keywords": "mortgage loan officer jobs, non-QM loan officer, W-2 loan officer with benefits, loan officer careers, mortgage broker loan officer, wholesale mortgage loan officer, join a mortgage brokerage, NEXA Mortgage loan officer",
    "audience": {"@type": "Audience", "audienceType": "Licensed mortgage loan originators"},
    "mentions": [{"@type": "Organization", "name": "NEXA Mortgage"}, {"@type": "Thing", "name": "NMLS license sponsorship"}]})
schema = jsonld([ORG, page, crumbs, faq_schema(FAQ)])

LOFTY_KEEP = '<!-- dialog showModal close data-mxa-close data-mxa-form mxa-done aria-invalid mxa-bad mxa-ph open ad-go -->'
LO_CSS = ad.AD_CSS + STREAM_CSS + PROG_CSS + PARTNER_CSS + JUMP_CSS + BENTO_CSS + FLIP_CSS + ABOUT_CSS + r"""
.mxp .mxa-main section[id]{scroll-margin-top:120px}
.mxp.mxp .lo-chips>li{padding:9px 16px !important;margin:0 !important;border:1px solid #DCE6EB !important;border-radius:999px !important;background:#fff !important;color:#0E2A47;line-height:1.2;list-style:none}
.mxp.mxp .lo-chips>li::before{content:none !important}
.mxp.mxp .lo-stack>li{margin:0 !important;list-style:none}
.mxp.mxp .lo-stack>li::before{content:none !important}
.mxp .mxa-main .mx-faq details{border-bottom:1px solid #DCE6EB}
.mxp .mxa-main .mx-faq summary h3{font-size:19px;font-weight:700;margin:0}
"""
full = wrap('mx-lo', LOFTY_KEEP + f'\n<style>{LO_CSS}</style>\n<div class="mxa-main">\n{body}\n</div>', s, schema, 'LOAN OFFICER CAREERS (/loanofficer)')
full = full.replace('font-family: Barlow, system-ui, sans-serif', 'font-family: MoxieBarlow, Barlow, system-ui, sans-serif')
for a in ('font:700 26px/1 ', 'font:800 16px/1 ', 'font:500 16px ', 'font:700 14px '):
    full = full.replace(a + 'Barlow,system-ui', a + 'MoxieBarlow,Barlow,system-ui')
html_out = optimize(full)
out = os.path.join(HERE, 'out', 'moxie-loan-officer-embed.html')
open(out, 'w', encoding='utf-8').write(html_out)
print('loan officer ok', len(html_out), 'bytes')

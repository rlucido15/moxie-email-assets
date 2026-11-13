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
    idattr = f' id="{sec_id}"' if sec_id else ''
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
        <dl aria-label="Moxie at a glance" style="margin: 0; background: #ffffff; color: #0E2A47; border-radius: 24px; padding: 32px; box-shadow: 0 30px 60px rgba(2,2,21,.35); display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px">
          <div style="grid-column: 1 / -1; background: #0E2A47; color: #ffffff; border-radius: 16px; padding: 20px 22px">
            <dt style="font-size: 15px; color: #7FDCEC; font-weight: 600">Company-generated business since day one<sup>3</sup></dt>
            <dd style="margin: 2px 0 0; font-size: 52px; font-weight: 800; line-height: 1.05; letter-spacing: -0.02em">82%</dd>
          </div>
          <div style="background: #E3F5F9; border-radius: 14px; padding: 16px 18px; display: flex; flex-direction: column; justify-content: space-between; gap: 4px"><dt style="font-size: 14px; color: #4A5868">Purchase business<sup>3</sup></dt><dd style="margin: 2px 0 0; font-size: 30px; font-weight: 800; line-height: 1.1">86%</dd></div>
          <div style="background: #E3F5F9; border-radius: 14px; padding: 16px 18px; display: flex; flex-direction: column; justify-content: space-between; gap: 4px"><dt style="font-size: 14px; color: #4A5868">Avg. clear to close<sup>2</sup></dt><dd style="margin: 2px 0 0; font-size: 30px; font-weight: 800; line-height: 1.1">14 days</dd></div>
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
               '<p style="margin: 16px 0 0; font-size: 13px; color: #4A5868">Referral volume varies by market and is not guaranteed. Buyers always choose their own lender.</p>',
               lede='Moxie builds the enterprise accounts and relationships that send buyers your way, so more of your week goes to structuring and closing loans.', sec_id='deals')


# ---------------- PRODUCTS (chip cloud; doubles as long-tail keywords)
PROGRAM_GROUPS = [
    ('home', 'Agency and government', 'FICO from 500', ['Conventional', 'FHA', 'VA', 'USDA', 'Down payment assistance', 'Doctor loans']),
    ('gem', 'Jumbo', 'Up to $30M', ['Jumbo', 'Jumbo max ($5M)', 'Super jumbo ($30M)']),
    ('brief', 'Self-employed and non-QM', 'No tax returns needed', ['Bank statement', 'P&amp;L only', 'Asset depletion', 'Non-QM', 'No doc', 'Foreign national']),
    ('trend', 'Real estate investors', 'DSCR up to 25 units', ['DSCR', 'Bridge loans', 'Up to 25 units', 'Mixed use', 'Close in an LLC', 'Cross-collateralized loans']),
    ('cash', 'Home equity', 'Keep the low first rate', ['HELOC', 'HELOAN', 'Second mortgages', 'Reverse mortgages']),
    ('tool', 'Construction and renovation', 'Build, renovate, rehab', ['203(k) and renovation', 'Construction', 'One-time close', 'Fix and flip']),
    ('grid', 'Unique properties', 'Hard-to-finance properties', ['Non-warrantable condos', 'Condotels', 'Manufactured homes']),
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
.mxp .lo-pg{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:20px;margin-top:44px}
.mxp .lo-pg>.lo-pc{grid-column:span 2}
.mxp .lo-pg>.lo-pc:nth-last-child(-n+2){grid-column:span 3}
@media (max-width:1000px){.mxp .lo-pg>.lo-pc,.mxp .lo-pg>.lo-pc:nth-last-child(-n+2){grid-column:span 3}}
@media (max-width:640px){.mxp .lo-pg>.lo-pc,.mxp .lo-pg>.lo-pc:nth-last-child(-n+2){grid-column:1/-1}}
.mxp .lo-pc{position:relative;background:#fff;border-radius:24px;overflow:hidden;box-shadow:0 1px 0 #DCE6EB,0 12px 32px rgba(14,42,71,.08);transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s}
.mxp .lo-pc::after{content:"";position:absolute;inset:0;border-radius:24px;border:1.5px solid transparent;pointer-events:none;transition:border-color .3s}
.mxp .lo-pc:hover{transform:translateY(-6px);box-shadow:0 1px 0 #DCE6EB,0 22px 44px rgba(14,42,71,.16)}
.mxp .lo-pc:hover::after{border-color:#1C97AE}
.mxp .lo-pc-top{position:relative;display:flex;gap:14px;align-items:center;padding:24px 24px 22px;background:radial-gradient(120% 140% at 100% 0%,#1C97AE 0%,#145A75 38%,#0E2A47 78%);color:#fff;overflow:hidden}
.mxp .lo-pc-top::before{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.22),transparent);transform:skewX(-18deg);pointer-events:none}
.mxp .lo-pc-ic{flex:none;width:52px;height:52px;border-radius:16px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);color:#7FDCEC;display:inline-flex;align-items:center;justify-content:center;transition:transform .45s cubic-bezier(.2,.8,.2,1)}
.mxp .lo-pc-ic>span{width:26px;height:26px;display:block}
.mxp .lo-pc:hover .lo-pc-ic{transform:rotate(-8deg) scale(1.08)}
.mxp .lo-pc-top h3{margin:0;font-size:14px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#B8E6EF}
.mxp .lo-pc-hi{margin:2px 0 0;font-size:clamp(22px,2.2vw,26px);font-weight:800;line-height:1.15;letter-spacing:-.01em;color:#fff}
.mxp .lo-pc-n{margin-left:auto;flex:none;min-width:34px;height:34px;padding:0 10px;border-radius:999px;background:#F46744;color:#0E2A47;font-weight:800;font-size:15px;display:inline-flex;align-items:center;justify-content:center}
.mxp .lo-pl-wrap{padding:22px 24px 26px}
.mxp .lo-plist{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 16px}
.mxp.mxp .lo-plist>li{display:flex !important;gap:10px;margin:0 !important;padding:0 !important;font-size:15.5px;line-height:1.4;color:#0E2A47;font-weight:500;list-style:none}
.mxp .lo-ck{flex:none;width:6px;height:11px;border:solid #1C97AE;border-width:0 2.5px 2.5px 0;transform:rotate(45deg);margin:3px 3px 0 2px}
@media (max-width:420px){.mxp .lo-plist{grid-template-columns:1fr}.mxp .lo-pc-top{padding:20px}.mxp .lo-pl-wrap{padding:18px 20px 22px}}
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
    prog_cards + '<p style="margin: 16px 0 0; font-size: 13px; color: #4A5868">Program availability varies by state, investor and borrower qualification.</p>',
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
    ('You’re turning away good borrowers.', 'Huge loan selection', 'Credit scores as low as 500, self-employed loans, DSCR up to 25 units, no doc loans, HELOCs and much more.'),
    ('Your files sit in a slow queue.', '14-day average clear to close<sup>2</sup>', 'In-house processing, plus priority underwriting and account support with key investors across product types.'),
    ('You can’t see how your loans are priced.', 'Full transparency', 'See the pricing and the investor purchase advice on every loan.'),
    ('You wait weeks to get paid.', 'Everyday payday', 'Generous compensation paid as your loans close, with full health insurance and a 401(k) for eligible employees.'),
]
X_IC = '<span aria-hidden="true" class="lo-pf-x">×</span>'
OK_IC = f'<span aria-hidden="true" class="lo-pf-ok"><span style="width: 16px; height: 16px; display: block">{ICON["check22"]}</span></span>'
pain_rows = ''.join(
    f'<li class="lo-pf-row"><div class="lo-pf-was">{X_IC}<p>{a}</p></div>'
    f'<div class="lo-pf-now">{OK_IC}<div><h3>{b}</h3><p>{c}</p></div></div></li>' for a, b, c in PAIN)
pain_sec = section('lo-pain', 'Sound familiar?', 'Great loan officers, held back by the wrong company.',
    '<div class="lo-pf-head" aria-hidden="true"><span>What you’re dealing with now</span><span>What you get at Moxie</span></div>'
    f'<ul class="lo-pf" style="list-style: none; padding: 0; margin: 0">{pain_rows}</ul>')

# ---------------- WHERE YOUR DEALS COME FROM (value stack, dark)
STACK = [
    ('Key enterprise accounts', 'Relationships Moxie builds with key enterprise accounts in its markets, which send warm opportunities to Moxie loan officers.'),
    ('Area Directors in your market', 'Local Area Directors build and maintain agent relationships so buyers get introduced to you.'),
    ('Follow-up and client retention systems', 'Automated follow-up keeps every lead and past client close for referrals, equity options and refinances when the numbers work.'),
]
stack_rows = ''.join(
    f'<li><div class="lo-st-row"><span aria-hidden="true" class="lo-st-n">{i}</span><div style="min-width: 0"><h3>{t}</h3><p>{d}</p></div></div></li>' for i, (t, d) in enumerate(STACK, 1))
deals_sec = section('lo-deals', 'Where your deals come from', 'We drive the business opportunities that fuel your growth.',
    f'<div class="lo-st"><ul style="list-style: none; padding: 0; margin: 0">{stack_rows}</ul>'
    '<p class="lo-st-sum"><b>= 82% company-generated, 86% purchase.</b><span>A pipeline that doesn’t depend on cold calls or waiting for rates to drop.<sup>3</sup></span></p></div>'
    '<p style="margin: 16px 0 0; font-size: 13px; color: #B8C7D3">Referral volume varies by market and is not guaranteed. Buyers always choose their own lender.</p>',
    bg='#0E2A47', dark=True, sec_id='deals',
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
    f'<h3 style="margin: 6px 0 0; font-size: 21px">{t}</h3><p style="margin: 0; color: #4A5868; font-size: 16px">{d}</p></article>' for ic, t, d in PAY) + '</div>'
sup_list = ('<h3 style="margin: 56px 0 0; font-size: 24px; color: #ffffff">Support behind every file</h3>'
            '<ul class="lo-sup" style="list-style: none; padding: 0; margin: 20px 0 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px 32px">'
            + ''.join(f'<li><div class="lo-sup-i"><h4>{t}</h4><p>{d}</p></div></li>' for t, d in SUPPORT) + '</ul>')
pay_sec = section('lo-pay', 'Pay, benefits and support', 'Get paid well. Work anywhere, but never work alone.',
    pay_cards + sup_list + '<p style="margin: 28px 0 0; font-size: 13px; color: #B8C7D3">Compensation and benefit eligibility depend on employment type and are set out in your written agreement. W-2 and 1099 options are available. We walk through the full plan on your intro call.</p>',
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
.mxp .lo-st{margin-top:40px;background:#fff;color:#0E2A47;border-radius:24px;overflow:hidden}
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
    ('Proprietary client tools', 'Proven tools that turn your complex details into a clear understanding in minutes.'),
    ('Arive and Lofty CRM', 'Originate in Arive and keep every lead and past client moving forward and coming back in Lofty.'),
    ('Moxie University', 'On-demand courses plus short how-to videos for Moxie’s client tools.'),
    ('Automated client experience', 'Automated tools that elevate and streamline every step for your clients, from application to closing and beyond.'),
]
tools = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article class="mxa-card" style="{CARD}"><h3 style="margin: 0; font-size: 20px; display: flex; gap: 10px; align-items: center"><span style="color: #127C8F; flex: none; display: inline-flex">{ICON["check22"]}</span>{t}</h3>'
    f'<p style="margin: 8px 0 0; color: #4A5868; font-size: 16px">{d}</p></article>' for t, d in TOOLS) + '</div>'
tools_sec = section('lo-tools', 'Tools and technology', 'Tools that close business and build repeat business.', tools, bg='#F4F8FA',
                    lede='Moxie has invested significantly to give its team cutting-edge technology, including proprietary tools available only to Moxie team members. Our systems are integrated, automated and powered by AI, maximizing your effectiveness and minimizing wasted time.')

# ---------------- PARTNER RELATIONSHIPS
PARTNERS = [
    ('shield', 'Insurance network', 'Faster clear to close',
     'Our insurance network finds clients the best price on homeowners insurance, so they’re fully protected while keeping their monthly payment as low as possible, with no work required from them.'),
    ('home', 'Home services', 'No cost to the borrower',
     'Help with the move and getting the new home set up, at no cost to the borrower, so there’s less stress and the house feels like home sooner.'),
    ('clock', 'AMC relationships', 'Faster appraisals',
     'Appraisal management relationships with local market experts speed up appraisal turnaround times.'),
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
.mxp .lo-pr h3{margin:8px 0 0;font-size:22px;line-height:1.2}
.mxp .lo-pr p{margin:0;font-size:16px;color:#4A5868}
"""

# ---------------- MARKETING (reuse AD cards and images)
mk = re.search(r'\s*<!-- WHAT AGENTS GET -->.*?</section>', ad.body, re.S)
assert mk, 'AD marketing section not found'
mk = mk.group(0).replace('<!-- WHAT AGENTS GET -->', '<!-- CO-MARKETING -->')
mk = re.sub(r'aria-labelledby="ad-tools"', 'aria-labelledby="lo-mkt"', mk).replace('id="ad-tools"', 'id="lo-mkt"')
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
    ben_cards + '<p style="margin: 16px 0 0; font-size: 13px; color: #4A5868">Compensation and benefit eligibility depend on employment type and are set out in your written agreement. We walk through the full plan on your intro call.</p>')

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
    <p style="margin: 0">Moxie Mortgage, a division of NEXA Mortgage, LLC · NMLS #1660690 · AZMB 0944059 · Equal Housing Lender</p>
  </section>'''

body = hero + pain_sec + deals_sec + mk + products_sec + tools_sec + partners_sec + pay_sec + founder_sec + rv + faq_sec + apply_sec + disclosures
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
new_payload = """    var payload = { name: v('name'), phone: v('phone'), email: v('email'), cta: 'LO Application', tags: v('states').split(', ').filter(Boolean), source: 'MoxieMortgage.com — Loan Officer page',
      consent: true, secret: SECRET, message: v('message'), pageUrl: location.href.split('#')[0], submittedAt: new Date().toISOString(),
      fields: { 'Application': 'Loan Officer', 'NMLS #': v('nmls'), 'Years originating': v('years'), 'Loans closed, last 12 months': v('units'),
        'Volume, last 12 months': v('volume'), 'Licensed states': v('states'), 'Current company': v('company'), 'Consent text': consentText } };
"""
s = s.replace(old_payload, new_payload).replace('tags the lead "CTA: AD Application"', 'tags the lead "CTA: LO Application"')
assert "cta: 'LO Application'" in s and 'AD Application' not in s
s = s.replace('Thanks! We’ll review it and reach out to book your onboarding call.', 'Thanks! We’ll review it and reach out to book your intro call.')
s = s.replace('// ---- timeline:', '// ---- referral flow:')
s += '''
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
LO_CSS = ad.AD_CSS + STREAM_CSS + PROG_CSS + PARTNER_CSS + r"""
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

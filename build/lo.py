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
        <h1 id="lo-h1" class="mx-speak" style="margin: 0; font-size: clamp(40px, 5.2vw, 64px); line-height: 1.03; font-weight: 800; letter-spacing: -0.02em">Win more loans with wholesale pricing and a referral pipeline.</h1>
        <p class="mx-speak" style="margin: 22px 0 0; font-size: 19px; line-height: 1.5; color: #D3E3EC; max-width: 600px">Moxie Mortgage, a division of NEXA Mortgage, is hiring experienced, licensed loan officers. You get 300+ wholesale investors, introductions from our Area Directors and agent partners, purpose-built sales tools, and a mentor on your deals.</p>
        <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px">
          <a href="#apply" class="mxa-btn-p" style="{BTN_P}">Apply to join Moxie</a>
          <a href="#why" class="mxa-btn-w" style="{BTN_W}">See what you get</a>
        </div>
      </div>
      <div style="flex: 1 1 380px; min-width: 0">
        <dl aria-label="Moxie at a glance" style="margin: 0; background: #ffffff; color: #0E2A47; border-radius: 24px; padding: 32px; box-shadow: 0 30px 60px rgba(2,2,21,.35); display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px">
          <div style="grid-column: 1 / -1; background: #0E2A47; color: #ffffff; border-radius: 16px; padding: 20px 22px">
            <dt style="font-size: 15px; color: #7FDCEC; font-weight: 600">Wholesale investors to price every file</dt>
            <dd style="margin: 2px 0 0; font-size: 52px; font-weight: 800; line-height: 1.05; letter-spacing: -0.02em">300+</dd>
          </div>
          <div style="background: #E3F5F9; border-radius: 14px; padding: 16px 18px"><dt style="font-size: 14px; color: #4A5868">Avg. clear to close<sup>2</sup></dt><dd style="margin: 2px 0 0; font-size: 30px; font-weight: 800; line-height: 1.1">14 days</dd></div>
          <div style="background: #E3F5F9; border-radius: 14px; padding: 16px 18px"><dt style="font-size: 14px; color: #4A5868">States and territories</dt><dd style="margin: 2px 0 0; font-size: 30px; font-weight: 800; line-height: 1.1">51</dd></div>
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
    ('Fighting slow, unresponsive operations', 'Dedicated processors and mortgage consultants on your files.'),
    ('Waiting weeks to get paid', 'Everyday payday: commission is paid as your loans close.'),
]
stop_cards = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article style="background: rgba(255,255,255,.06); border: 1px solid rgba(127,220,236,.25); border-radius: 20px; padding: 24px 26px">'
    f'<h3 style="margin: 0; font-size: 20px; color: #ffffff; display: flex; gap: 10px; align-items: center"><span aria-hidden="true" style="flex: none; width: 28px; height: 28px; border-radius: 50%; background: #F46744; color: #0E2A47; font-weight: 800; display: inline-flex; align-items: center; justify-content: center; font-size: 16px">×</span>Stop {t[0].lower() + t[1:]}</h3>'
    f'<p style="margin: 8px 0 0 38px; color: #D3E3EC; font-size: 16px">{d}</p></article>' for t, d in STOPS) + '</div>'
stop_sec = section('lo-stop', 'Sound familiar?', 'Stop saying no to good borrowers.', stop_cards, bg='#0E2A47', dark=True)

# ---------------- FOUR PILLARS
PILLARS = [
    ('pct', 'Lender access and pricing', 'Shop 300+ wholesale investors through NEXA instead of one rate sheet. Moxie rates averaged 0.559% lower than the largest retail lender.<sup>1</sup>'),
    ('trend', 'A referral pipeline', 'Moxie Area Directors build agent relationships in their markets, and agent partners introduce their buyers to Moxie loan officers.'),
    ('grid', 'Tools that sell for you', 'Arive for origination, Lofty CRM, and client-ready worksheets and calculators that make the numbers easy to explain.'),
    ('shield', 'Support and mentorship', 'Dedicated processors, a full back office, Moxie University, and a mentor for deal strategy.'),
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
                  lede='Wholesale pricing means your borrowers skip the retail overhead, and fast closings help their offers win.')

# ---------------- REFERRAL FLOW (animated timeline, same as AD "Income builds over time")
FLOW = [
    ('Step 1', 'Agent relationships', 'Area Directors and Moxie marketing keep agents in your market engaged.'),
    ('Step 2', 'Buyer introduction', 'The agent introduces the buyer by group text or a quick call.'),
    ('Step 3', 'You run the file', 'Preapproval or a plan of action, priced across wholesale investors.'),
    ('Step 4', 'Agent stays in the loop', 'The agent tracks the loan in the Moxie Realtor Portal.'),
]
flow_items = ''.join(
    f'<li class="ad-step" style="{CARD.replace("26px 26px 24px", "22px 24px")}"><span style="display: inline-block; background: #E3F5F9; color: #127C8F; font-weight: 700; font-size: 14px; border-radius: 999px; padding: 4px 12px">{n}</span>'
    f'<h3 style="margin: 12px 0 0; font-size: 20px">{t}</h3><p style="margin: 6px 0 0; color: #4A5868; font-size: 15px">{d}</p></li>' for n, t, d in FLOW)
flow_items += ('<li style="background: #0E2A47; color: #ffffff; border-radius: 20px; padding: 22px 24px"><span style="display: inline-block; background: #F46744; color: #0E2A47; font-weight: 700; font-size: 14px; border-radius: 999px; padding: 4px 12px">Then</span>'
               '<h3 style="margin: 12px 0 0; font-size: 20px">Repeat business</h3><p style="margin: 6px 0 0; color: #C9D6DF; font-size: 15px">Happy agents send the next buyer, and past clients come back to refinance.</p></li>')
flow = section('lo-flow', 'How referrals reach you', 'A pipeline that doesn’t depend on cold calls.',
               f'<ol class="ad-tl" style="list-style: none; padding: 0; margin: 40px 0 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(165px, 1fr)); gap: 28px">{flow_items}</ol>'
               '<p style="margin: 16px 0 0; font-size: 13px; color: #4A5868">Referral volume varies by market and is not guaranteed. Buyers always choose their own lender.</p>',
               lede='Moxie invests in the agent relationships that send buyers your way, so more of your week goes to structuring and closing loans.')


# ---------------- PRODUCTS (chip cloud; doubles as long-tail keywords)
PRODUCTS = ['Conventional', 'FHA', 'VA', 'USDA', 'Jumbo and super jumbo', 'HELOC', 'Home equity loans', 'Second mortgages', 'Bank statement',
            'P&amp;L only', 'Asset depletion', 'DSCR', 'Non-QM', 'ITIN', 'Foreign national', 'DACA', 'Doctor loans', 'Down payment assistance',
            '203(k) and renovation', 'Construction and one-time close', 'Fix and flip', 'Bridge loans', 'Interest-only', 'Manufactured homes',
            'Non-warrantable condos', 'Condotels', 'Up to 8 units', 'Mixed use', 'Close in an LLC', 'Reverse mortgages', 'Temporary buydowns', 'ARMs']
chips = '<ul class="lo-chips" style="list-style: none; padding: 0; margin: 36px 0 0; display: flex; flex-wrap: wrap; gap: 10px">' + ''.join(
    f'<li style="background: #ffffff; border: 1px solid #DCE6EB; border-radius: 999px; padding: 9px 16px; font-weight: 600; font-size: 15px">{x}</li>' for x in PRODUCTS) + '</ul>'
products_sec = section('lo-products', 'Loan programs', 'Thousands of programs, so you can say yes more often.',
    chips + '<p style="margin: 16px 0 0; font-size: 13px; color: #4A5868">Program availability varies by state, investor and borrower qualification.</p>',
    bg='#F4F8FA', lede='Through NEXA’s wholesale investors, Moxie loan officers can match nearly any borrower to a program, from first-time buyers to self-employed borrowers and investors.')

# ---------------- RETAIL VS MOXIE TABLE
ROWS = [
    ('Loan options', 'One lender’s product shelf', '300+ wholesale investors: conventional, FHA, VA, jumbo, non-QM and HELOC'),
    ('Pricing', 'Retail pricing that carries branch overhead', 'Wholesale pricing; rates averaged 0.559% lower than the largest retail lender<sup>1</sup>'),
    ('Speed', '38-day industry average to close<sup>2</sup>', '14-day average clear to close<sup>2</sup>'),
    ('Referrals', 'Mostly yours to find', 'Area Directors and agent partners introduce buyers'),
    ('When you’re paid', 'On the next payroll cycle, often weeks after closing', 'Everyday payday: as your loans close'),
    ('Operations', 'Shared processing queue', 'Dedicated processors and mortgage consultants'),
    ('Technology', 'Whatever the company licenses', 'Arive, Lofty CRM and Moxie client tools'),
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
    ('Debt consolidation worksheet', 'Import a MISMO 3.4 credit file and show clients exactly what a cash-out refinance pays off and saves. Nothing is saved after the session.'),
    ('ARM vs. fixed comparison', 'Side-by-side payments and break-even so clients can pick a loan with confidence.'),
    ('Buydown calculator', 'Turn seller credits into a lower payment and show it on the listing flyer.'),
    ('Effective rate calculator', 'Show the after-tax cost of mortgage interest for clients who itemize.'),
    ('Arive and Lofty CRM', 'Originate in Arive and keep every lead and past client moving in Lofty.'),
    ('Moxie University', 'On-demand courses plus short how-to videos for Moxie’s client tools.'),
]
tools = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article class="mxa-card" style="{CARD}"><h3 style="margin: 0; font-size: 20px; display: flex; gap: 10px; align-items: center"><span style="color: #127C8F; flex: none; display: inline-flex">{ICON["check22"]}</span>{t}</h3>'
    f'<p style="margin: 8px 0 0; color: #4A5868; font-size: 16px">{d}</p></article>' for t, d in TOOLS) + '</div>'
tools_sec = section('lo-tools', 'Tools and technology', 'Client-ready tools that make your numbers easy to say yes to.', tools)

# ---------------- MARKETING (reuse AD cards and images)
mk = re.search(r'\s*<!-- WHAT AGENTS GET -->.*?</section>', ad.body, re.S)
assert mk, 'AD marketing section not found'
mk = mk.group(0).replace('<!-- WHAT AGENTS GET -->', '<!-- CO-MARKETING -->')
mk = re.sub(r'aria-labelledby="ad-tools"', 'aria-labelledby="lo-mkt"', mk).replace('id="ad-tools"', 'id="lo-mkt"')
mk = mk.replace('>Marketing support<', '>Co-marketing<').replace('Ready-to-use Moxie marketing for your area, every month.', 'Marketing your agent partners will actually use.')
mk = re.sub(r'Plus approval pages and a direct line to a licensed Moxie loan officer, live within 24 hours\.', 'Designed and sent by Moxie, with your name and number on it.', mk)
assert 'lo-mkt' in mk and 'Co-marketing' in mk and 'your name and number' in mk

# ---------------- TRAINING
TRAIN = [
    ('Processing and consultants', 'Dedicated loan processors plus mortgage consultants to help structure tough scenarios.'),
    ('A full back office', 'HR, legal, compliance, marketing, accounting, payroll and licensing, handled for you.'),
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
    ('cash', 'Everyday payday', 'Commission is paid as your loans close, not on a monthly cycle.'),
    ('shield', 'Medical, dental and vision', 'Health coverage options for eligible loan officers.'),
    ('trend', '401(k) and HSA', 'Plan for retirement and set aside pre-tax dollars for health costs.'),
    ('grid', 'W-2 or 1099', 'Choose the employment structure that fits your business.'),
]
ben_cards = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 40px">' + ''.join(
    f'<article class="mxa-card" style="{CARD}; display: flex; flex-direction: column; gap: 10px">'
    f'<span style="width: 48px; height: 48px; border-radius: 14px; background: #FDE7E1; color: #C2482A; display: inline-flex; align-items: center; justify-content: center"><span style="width: 24px; height: 24px; display: block">{ICON[ic]}</span></span>'
    f'<h3 style="margin: 6px 0 0; font-size: 21px">{t}</h3><p style="margin: 0; color: #4A5868; font-size: 16px">{d}</p></article>' for ic, t, d in BENEFITS) + '</div>'
ben_sec = section('lo-pay', 'Pay and benefits', 'Get paid faster, with benefits that come with a real company.',
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
    ('What is it like to be a loan officer at Moxie Mortgage?',
     'Moxie Mortgage is a wholesale mortgage brokerage and a division of NEXA Mortgage. Moxie loan officers price loans across 300+ wholesale investors, get introductions from Moxie Area Directors and agent partners, use Moxie’s client tools and CRM, and work with a mentor and a team that meets twice a week.'),
    ('How are Moxie loan officers paid?',
     'Loan officers are paid on closed loans under a written compensation agreement, and commission is paid as each loan closes. W-2 and 1099 options are available, and eligible loan officers can access medical, dental and vision coverage, a 401(k) and an HSA. We walk through the full plan, including splits and any costs you’re responsible for, on your intro call. As federal rules require, loan officer pay is never based on a loan’s rate or terms.'),
    ('Does Moxie provide leads or referrals?',
     'Moxie Area Directors build relationships with real estate agents in their markets, and agent partners introduce their buyers to Moxie loan officers. Referral volume varies by market and isn’t guaranteed, so you’ll still grow your own network, with Moxie co-marketing to help.'),
    ('Which lenders and loan programs can I offer?',
     'Through NEXA, Moxie loan officers can shop more than 300 wholesale investors and thousands of programs: conventional, FHA, VA, USDA and jumbo loans, HELOCs and second mortgages, bank statement and other non-QM loans, DSCR and fix-and-flip loans for investors, ITIN and foreign national loans, construction, renovation and reverse mortgages.'),
    ('What technology do Moxie loan officers use?',
     'Arive for loan origination, Lofty for CRM and follow-up, and Moxie’s client tools, including a debt consolidation worksheet with MISMO 3.4 credit import, ARM vs. fixed and buydown comparisons, and an effective rate calculator.'),
    ('What do I need to join, and which states can I originate in?',
     'You need an active NMLS license in good standing. Moxie loan officers are sponsored through NEXA Mortgage in the states where they’re licensed. NEXA isn’t licensed in New York or Massachusetts yet, so we can’t sponsor originators there today.'),
    ('What training and support will I get?',
     'Dedicated loan processors and mortgage consultants, a back office that handles HR, legal, compliance, marketing, accounting, payroll and licensing, Moxie University for on-demand training, Monday and Friday team huddles at noon ET, an annual mortgage conference, and a mentor for deal strategy and accountability.'),
    ('How do I apply?',
     'Fill out the short application on this page. We’ll reach out to book a 20-minute intro call to review compensation, the referral pipeline and next steps.'),
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
    ('#ffffff', '20-minute intro call', 'We review compensation, the referral pipeline and how Moxie fits your business.'),
    ('rgba(252, 200, 184, 0.92)', 'Sponsorship and setup', 'Move your NMLS sponsorship to NEXA and get set up in Arive, Lofty and pricing.'),
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
        <h2 id="lo-apply" style="{H2}">Three steps to joining Moxie.</h2>
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
    <p style="margin: 0 0 8px"><sup>1</sup> Based on Moxie Mortgage’s apples-to-apples comparison of weekly rates against Rocket Mortgage from November 2025 to November 2026; average difference 0.559%. Rate and savings vary and depend on borrower’s qualification, property specifics, and market conditions. <sup>2</sup> Moxie average clear-to-close time; the industry average was 38 days (ICE Mortgage Technology, May 2026). Not a commitment to lend; all loans are subject to credit approval.</p>
    <p style="margin: 0">Moxie Mortgage, a division of NEXA Mortgage, LLC · NMLS #1660690 · AZMB 0944059 · Equal Housing Lender</p>
  </section>'''

body = hero + stop_sec + why + pricing + products_sec + flow + compare + tools_sec + mk + ben_sec + train_sec + rv + faq_sec + apply_sec + disclosures
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
# FAQ: one open at a time is not needed; leave native <details>

DESC = ("Join Moxie Mortgage as a loan officer: 300+ wholesale investors, thousands of loan programs, referrals from agent partners, "
        "everyday payday, benefits, and hands-on support. For experienced, licensed LOs.")
page, crumbs = webpage('/loanofficer', 'Loan Officer Careers | Join Moxie Mortgage', DESC, 'Loan Officer Careers', {
    "dateModified": datetime.date.today().isoformat(),
    "keywords": "mortgage loan officer jobs, non-QM loan officer, W-2 loan officer with benefits, loan officer careers, mortgage broker loan officer, wholesale mortgage loan officer, join a mortgage brokerage, NEXA Mortgage loan officer",
    "audience": {"@type": "Audience", "audienceType": "Licensed mortgage loan originators"},
    "mentions": [{"@type": "Organization", "name": "NEXA Mortgage"}, {"@type": "Thing", "name": "NMLS license sponsorship"}]})
schema = jsonld([ORG, page, crumbs, faq_schema(FAQ)])

LOFTY_KEEP = '<!-- dialog showModal close data-mxa-close data-mxa-form mxa-done aria-invalid mxa-bad mxa-ph open ad-go -->'
LO_CSS = ad.AD_CSS + r"""
.mxp .mxa-main section[id]{scroll-margin-top:120px}
.mxp.mxp .lo-chips>li{padding:9px 16px !important;margin:0 !important;border:1px solid #DCE6EB !important;border-radius:999px !important;background:#fff !important;color:#0E2A47;line-height:1.2;list-style:none}
.mxp.mxp .lo-chips>li::before{content:none !important}
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

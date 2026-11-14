import re
logo = open('/home/claude/moxie-email-assets/website/moxie-logo-color.svg').read()
logo = re.sub(r'\s(width|height)="\d+"', '', logo, count=2)
logo = re.sub(r'(\d+)\.\d+', r'\1', logo)
logo_c = logo.replace('<svg ', '<svg class="logo" width="112" height="30" role="img" aria-label="Moxie Mortgage" ', 1)
logo_w = re.sub(r'fill="#[0-9A-Fa-f]{3,6}"', 'fill="#FFFFFF"', logo).replace('<svg ', '<svg class="logo logo-w" role="img" aria-label="Moxie Mortgage" ', 1)
logo_w = logo_w.replace('<title>Moxie Mortgage</title>', '')

CK = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 8.4l2.9 2.9 6.1-6.6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
EHO = '<svg class="eho" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3 2 14h4v15h20V14h4z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><path d="M11 17h10M11 22h10" stroke="currentColor" stroke-width="2.6"/></svg>'

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moxie Client Benefit: No Lender Fees When You Refinance | Moxie Mortgage</title>
<meta name="description" content="Moxie Mortgage clients pay no Moxie lender fees to refinance, every time rates drop, after 6 on-time payments. See a hypothetical example and get personalized options within one business day.">
<link rel="canonical" href="https://www.moxiemortgage.com/refinance-benefit">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0E2A47">
<meta property="og:type" content="website"><meta property="og:site_name" content="Moxie Mortgage">
<meta property="og:title" content="Your payment should drop when rates do">
<meta property="og:description" content="Moxie clients pay no Moxie lender fees to refinance, every time rates drop. Terms apply.">
<meta property="og:url" content="https://www.moxiemortgage.com/refinance-benefit">
<meta property="og:image" content="https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@13fa019/website/og-refinance-benefit.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800;900&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800;900&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800;900&display=swap"></noscript>
<style>
@font-face{{font-family:'Barlow Fallback';src:local('Arial');size-adjust:92%;ascent-override:100%;descent-override:20%}}
:root{{--navy:#0E2A47;--ink:#020215;--teal:#1C97AE;--teal-d:#127C8F;--aqua:#7FDCEC;--orange:#F46744;--slate:#4A5868;--mist:#D3E3EC;--line:#DCE6EB;--wash:#F4F8FA;
  --grad:linear-gradient(135deg,#1C97AE 0%,#0D4E66 55%,#0E2A47 100%)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Barlow,'Barlow Fallback',Arial,sans-serif;color:var(--navy);background:#E6EDF1;-webkit-font-smoothing:antialiased;padding:40px 16px}}
.page{{width:8.5in;min-height:11in;margin:0 auto;background:#fff;position:relative;overflow:hidden;border-radius:18px;box-shadow:0 18px 50px rgba(14,42,71,.14);display:flex;flex-direction:column}}
.wrap{{padding:0 .55in}}

/* top bar */
.top{{display:flex;align-items:center;justify-content:space-between;padding:.3in .55in 0}}
.logo{{height:30px;width:auto;display:block}}
.tag{{font-size:10.5px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--teal-d);border:1.5px solid var(--teal);border-radius:999px;padding:5px 12px}}

/* headline */
.head{{padding-top:18px}}
h1{{font-size:35px;font-weight:900;line-height:1.02;letter-spacing:-.025em;color:var(--navy);text-wrap:balance}}
h1 .hl{{background:linear-gradient(transparent 62%,rgba(127,220,236,.55) 62%);padding:0 2px}}
h1 sup,.sup{{font-size:.38em;font-weight:800;color:var(--teal);vertical-align:super;line-height:0}}
.lede{{margin-top:8px;font-size:15px;line-height:1.42;color:var(--slate);max-width:6.1in}}

/* hero */
.hero{{margin-top:16px;border-radius:20px;background:var(--grad);color:#fff;position:relative;overflow:hidden;display:grid;grid-template-columns:1fr auto;gap:22px;align-items:center;padding:18px 24px}}
.hero::after{{content:"";position:absolute;right:-60px;top:-80px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(127,220,236,.35),rgba(127,220,236,0) 70%)}}
.eyebrow{{display:inline-block;font-size:10.5px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--navy);background:var(--aqua);border-radius:999px;padding:5px 11px}}
.hero h2{{margin-top:10px;font-size:23px;font-weight:800;line-height:1.15;letter-spacing:-.01em;text-wrap:balance}}
.hero p{{margin-top:8px;font-size:13.5px;line-height:1.45;color:#D3E3EC;max-width:4.6in}}
.badge{{position:relative;z-index:1;width:124px;height:124px;border-radius:50%;background:#fff;color:var(--navy);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-shadow:0 0 0 8px rgba(255,255,255,.14),0 14px 30px rgba(2,2,21,.35)}}
.badge b{{font-size:44px;font-weight:900;line-height:.9;letter-spacing:-.03em;color:var(--orange)}}
.badge span{{margin-top:4px;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;line-height:1.15}}

/* repeat strip */
.repeat{{margin-top:12px;display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.repeat div{{padding:12px 14px;display:flex;gap:10px;align-items:flex-start}}
.repeat div+div{{border-left:1px solid var(--line)}}
.repeat i{{flex:none;width:26px;height:26px;border-radius:8px;background:#E3F5F9;color:var(--teal-d);display:flex;align-items:center;justify-content:center}}
.repeat i svg{{width:15px;height:15px}}
.repeat b{{display:block;font-size:13.5px;font-weight:800;line-height:1.2}}
.repeat small{{display:block;margin-top:2px;font-size:11.5px;line-height:1.35;color:var(--slate)}}

/* example */
.ex{{margin-top:14px}}
.exhead{{display:flex;align-items:baseline;justify-content:space-between;gap:12px}}
.exhead h3{{font-size:19px;font-weight:800;letter-spacing:-.01em}}
.exhead h3 em{{font-style:normal;color:var(--orange)}}
.exhead span{{font-size:10.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#7A8A99}}
.exgrid{{margin-top:8px;display:grid;grid-template-columns:1.35fr 1fr;gap:14px}}
.chart{{background:var(--wash);border-radius:16px;padding:12px 14px 8px;position:relative;display:flex;align-items:center}}
.chart svg{{display:block;width:100%;height:auto;overflow:visible}}
.chart text{{font-family:Barlow,'Barlow Fallback',Arial,sans-serif}}
.sum{{background:var(--navy);color:#fff;border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
.sum ul{{list-style:none;padding:8px 16px 2px;flex:1}}
.sum li{{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:4px 0;border-bottom:1px solid rgba(255,255,255,.1)}}
.sum li:last-child{{border-bottom:0}}
.sum li span{{font-size:12px;line-height:1.3;color:#B8C7D3}}
.sum li span b{{display:block;color:#fff;font-size:13px;font-weight:700}}
.sum li strong{{font-size:18px;font-weight:800;letter-spacing:-.01em;font-variant-numeric:tabular-nums;white-space:nowrap}}
.sum .tot{{background:var(--teal);padding:9px 16px;display:flex;justify-content:space-between;align-items:center;gap:10px}}
.sum .tot span{{font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;line-height:1.25}}
.sum .tot strong{{font-size:30px;font-weight:900;letter-spacing:-.02em;font-variant-numeric:tabular-nums}}

/* proof */
.proof{{margin-top:12px;display:grid;grid-template-columns:1fr auto;gap:14px;align-items:stretch}}
.quote{{border:1px solid var(--line);border-left:4px solid var(--teal);border-radius:0 14px 14px 0;padding:10px 16px}}
.stars{{color:var(--orange);font-size:13px;letter-spacing:3px}}
.quote p{{margin-top:3px;font-size:13px;line-height:1.4;font-style:italic}}
.quote .by{{margin-top:6px;font-size:11.5px;color:var(--slate)}}
.quote .by b{{color:var(--navy)}}
.stat{{min-width:1.7in;border-radius:14px;background:#E3F5F9;padding:12px 16px;display:flex;flex-direction:column;justify-content:center;text-align:center}}
.stat b{{font-size:34px;font-weight:900;line-height:1;letter-spacing:-.02em;color:var(--teal-d)}}
.stat b small{{font-size:15px;font-weight:800}}
.stat span{{margin-top:5px;font-size:11.5px;line-height:1.35;color:var(--slate)}}

/* CTA */
.cta{{margin-top:auto;background:var(--grad);color:#fff;padding:15px .55in;display:grid;grid-template-columns:1fr auto;gap:22px;align-items:center;position:relative}}
.cta h4{{font-size:21px;font-weight:800;line-height:1.15;letter-spacing:-.01em;text-wrap:balance}}
.cta p{{margin-top:5px;font-size:13px;line-height:1.4;color:#D3E3EC}}
.chips{{margin-top:9px;display:flex;flex-wrap:wrap;gap:6px 14px}}
.chips span{{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:600}}
.chips i{{width:15px;height:15px;border-radius:50%;background:var(--aqua);color:var(--navy);display:inline-flex;align-items:center;justify-content:center}}
.chips i svg{{width:10px;height:10px}}
.acts{{display:flex;flex-direction:column;gap:7px;min-width:2.15in}}
.btn{{display:flex;align-items:center;justify-content:center;gap:8px;border-radius:12px;padding:10px 16px;font-weight:800;font-size:17px;text-decoration:none;white-space:nowrap}}
.btn.p{{background:var(--orange);color:var(--navy);box-shadow:0 8px 18px rgba(244,103,68,.35)}}
.btn.s{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.45);color:#fff;font-size:13px;font-weight:700;padding:8px 14px}}
.btn svg{{width:16px;height:16px}}
.cta .logo-w{{position:absolute;right:.55in;top:-9999px}}

/* disclosures */
.disc{{background:#fff;padding:10px .55in .24in;font-size:8px;line-height:1.38;color:#5E6B78}}
.disc ol{{padding-left:11px}}
.disc li{{margin-bottom:3px}}
.disc .legal{{margin-top:6px;padding-top:6px;border-top:1px solid var(--line);display:flex;gap:10px;align-items:flex-start}}
.disc .eho{{flex:none;width:20px;height:20px;color:var(--navy)}}
.disc b{{color:var(--navy)}}

/* faq (screen only) */
.faq{{padding:22px .55in 6px}}
.faq h2{{font-size:20px;font-weight:800;letter-spacing:-.01em}}
.faq dl{{margin-top:10px;display:grid;grid-template-columns:1fr 1fr;gap:12px 24px}}
.faq dt{{font-size:14px;font-weight:800;line-height:1.3}}
.faq dd{{margin-top:3px;font-size:13px;line-height:1.45;color:var(--slate)}}
/* motion (screen only) */
@media screen and (prefers-reduced-motion:no-preference){{
  .badge{{animation:pop .7s cubic-bezier(.2,.9,.3,1.3) .2s both}}
  .step{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.6s ease .5s forwards}}
  .area{{opacity:0;animation:fade .8s ease 1.6s forwards}}
  .mark{{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.2,.9,.3,1.3) forwards}}
  .mark.m1{{animation-delay:.7s}}.mark.m2{{animation-delay:1.4s}}
  .btn.p{{animation:pulse 2.6s ease-in-out 2.4s infinite}}
}}
@keyframes pop{{from{{opacity:0;transform:scale(.6)}}to{{opacity:1;transform:none}}}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes fade{{to{{opacity:1}}}}
@keyframes pulse{{0%,100%{{box-shadow:0 8px 18px rgba(244,103,68,.35),0 0 0 0 rgba(244,103,68,.45)}}50%{{box-shadow:0 8px 18px rgba(244,103,68,.35),0 0 0 10px rgba(244,103,68,0)}}}}

@media screen and (max-width:860px){{
  body{{padding:0}} .page{{width:100%;min-height:0;border-radius:0}}
  .wrap,.top,.cta,.disc{{padding-left:20px;padding-right:20px}}
  h1{{font-size:31px}} .hero,.exgrid,.proof,.cta{{grid-template-columns:1fr}} .badge{{margin:0 auto}}
  .repeat{{grid-template-columns:1fr}} .repeat div+div{{border-left:0;border-top:1px solid var(--line)}}
  .acts{{min-width:0}} .faq{{padding-left:20px;padding-right:20px}} .faq dl{{grid-template-columns:1fr}}
}}
@page{{size:letter;margin:0}}
@media print{{.faq{{display:none}} body{{background:#fff;padding:0}} .page{{border-radius:0;box-shadow:none;width:8.5in;height:11in}} *{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}}}
</style>
<script type="application/ld+json">{{"@context": "https://schema.org", "@graph": [{{"@type": "Organization", "@id": "https://www.moxiemortgage.com/#org", "name": "Moxie Mortgage", "url": "https://www.moxiemortgage.com/", "telephone": "+1-480-660-2518", "email": "hello@moxiemortgage.com", "parentOrganization": {{"@type": "Organization", "name": "NEXA Mortgage, LLC", "identifier": "NMLS 1660690"}}}}, {{"@type": "WebPage", "@id": "https://www.moxiemortgage.com/refinance-benefit#webpage", "url": "https://www.moxiemortgage.com/refinance-benefit", "name": "Moxie Client Benefit: No Lender Fees When You Refinance", "inLanguage": "en-US", "description": "Moxie Mortgage clients pay no Moxie lender fees to refinance, every time rates drop, after 6 on-time payments.", "publisher": {{"@id": "https://www.moxiemortgage.com/#org"}}, "about": {{"@id": "https://www.moxiemortgage.com/refinance-benefit#benefit"}}}}, {{"@type": "LoanOrCredit", "@id": "https://www.moxiemortgage.com/refinance-benefit#benefit", "name": "Moxie Client Benefit refinance", "loanType": "Mortgage refinance", "provider": {{"@id": "https://www.moxiemortgage.com/#org"}}, "description": "Moxie covers its origination, processing and underwriting fees each time an eligible client refinances with Moxie after at least 6 consecutive on-time payments. Subject to credit approval and terms.", "areaServed": {{"@type": "Country", "name": "US"}}}}, {{"@type": "FAQPage", "@id": "https://www.moxiemortgage.com/refinance-benefit#faq", "mainEntity": [{{"@type": "Question", "name": "What is the Moxie Client Benefit?", "acceptedAnswer": {{"@type": "Answer", "text": "Clients whose current mortgage closed with Moxie Mortgage pay no Moxie lender fees (origination, processing and underwriting) when they refinance that home with Moxie. Terms apply; see disclosure 1."}}}}, {{"@type": "Question", "name": "Which fees does Moxie cover?", "acceptedAnswer": {{"@type": "Answer", "text": "Moxie covers its own origination, processing and underwriting fees. Third-party and government fees, such as appraisal, credit report, title, settlement, recording fees and transfer taxes, plus prepaid interest, escrow deposits and any discount points you choose, are not covered."}}}}, {{"@type": "Question", "name": "How often can I use the benefit?", "acceptedAnswer": {{"@type": "Answer", "text": "You can use it every time rates drop, after making at least 6 consecutive on-time payments on your current Moxie loan, for as long as you own the home. The benefit may change or end at any time, but changes won't affect a loan already locked."}}}}, {{"@type": "Question", "name": "Does refinancing always save money?", "acceptedAnswer": {{"@type": "Answer", "text": "Not always. Refinancing can restart or extend your loan term, which can increase the total interest you pay over the life of the loan. Moxie will show you the full cost and savings before you decide."}}}}, {{"@type": "Question", "name": "How do I see if I can lower my payment?", "acceptedAnswer": {{"@type": "Answer", "text": "Call 480.660.2518 or email hello@moxiemortgage.com. Because Moxie already has your file, we'll review your options within one business day, at no cost and with no obligation."}}}}]}}]}}</script>
</head>
<body>
<main class="page">

  <header class="top"><a href="https://www.moxiemortgage.com/" aria-label="Moxie Mortgage home">{logo_c}</a></header>

  <section class="wrap head">
    <h1>Your payment should drop <span class="hl">when rates do.</span><sup>1</sup></h1>
    <p class="lede">As a Moxie client, you never pay our lender fees to refinance with us. When rates fall, we'll help you lock in the savings, again and again.</p>

    <div class="hero">
      <div>
        <span class="eyebrow">Your benefit</span>
        <h2>We cover our lender fees every time you refinance with Moxie.<span class="sup">1</span></h2>
        <p>Use it every time rates drop, after every 6 on-time payments, for as long as you own your home. Rates fall five times? Use your benefit five times.</p>
      </div>
      <div class="badge" aria-label="Zero dollars in lender fees"><b>$0</b><span>Lender<br>fees<span class="sup">1</span></span></div>
    </div>

    <div class="ex">
      <div class="exhead"><h3>Rates drop twice? You save <em>twice.</em></h3><span>Hypothetical example<span class="sup">2</span></span></div>
      <div class="exgrid">
        <div class="chart">
          <svg viewBox="0 0 420 172" role="img" aria-label="Chart: monthly payment steps down 300 dollars at the first refinance and another 300 dollars at the second refinance two years later.">
            <line x1="40" y1="40" x2="410" y2="40" stroke="#9FB3C2" stroke-width="2" stroke-dasharray="5 5"/>
            <text x="410" y="30" text-anchor="end" font-size="11" font-weight="700" fill="#7A8A99">Payment without refinancing</text>
            <path class="area" d="M40 40 H410 V124 H190 V82 H40 Z" fill="rgba(28,151,174,.16)"/>
            <path class="step" pathLength="1" d="M40 82 H190 V124 H410" fill="none" stroke="#1C97AE" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
            <g class="mark m1"><circle cx="40" cy="60" r="13" fill="#F46744"/><text x="40" y="64.5" text-anchor="middle" font-size="12" font-weight="900" fill="#0E2A47">1</text></g>
            <g class="mark m2"><circle cx="190" cy="103" r="13" fill="#F46744"/><text x="190" y="107.5" text-anchor="middle" font-size="12" font-weight="900" fill="#0E2A47">2</text></g>
            <text x="115" y="72" text-anchor="middle" font-size="15" font-weight="800" fill="#0E2A47">−$300/mo</text>
            <text x="300" y="114" text-anchor="middle" font-size="15" font-weight="800" fill="#0E2A47">−$600/mo</text>
            <line x1="40" y1="146" x2="410" y2="146" stroke="#C6D3DB" stroke-width="1.5"/>
            <g font-size="11" font-weight="700" fill="#4A5868">
              <text x="40" y="164" text-anchor="middle">Refi #1</text>
              <text x="190" y="164" text-anchor="middle">Refi #2 · Year 2</text>
              <text x="410" y="164" text-anchor="end">Year 5</text>
            </g>
          </svg>
        </div>
        <div class="sum">
          <ul>
            <li><span><b>First payment drop</b>$300 × 60 months</span><strong>$18,000</strong></li>
            <li><span><b>Second payment drop</b>$300 × 36 months</span><strong>$10,800</strong></li>
            <li><span><b>Lender fees covered</b>$2,300 × 2 refinances</span><strong>$4,600</strong></li>
          </ul>
          <div class="tot"><span>Total over<br>5 years<span class="sup" style="color:#fff">2</span></span><strong>$33,400</strong></div>
        </div>
      </div>
    </div>

    <div class="proof">
      <figure class="quote">
        <div class="stars" aria-label="5 out of 5 stars">★★★★★</div>
        <p>“I refinanced two properties at the same time with Moxie, and the whole experience was outstanding from start to finish. If you want a team that truly knows what they’re doing and makes the process as seamless as possible, they are the people to call.”</p>
        <figcaption class="by"><b>Justin</b> · New Jersey · Google review</figcaption>
      </figure>
      <div class="stat"><b>$911<small>/mo</small></b><span>Justin’s combined monthly<br>savings on two refinances<span class="sup">3</span></span></div>
    </div>
  </section>

  <section class="cta" style="margin-top:14px">
    <div>
      <h4>See if you can lower your payment.</h4>
      <p>We’ll review your options within one business day, at no cost and with no obligation.</p>
      <div class="chips"><span><i>{CK}</i>We already have your file</span><span><i>{CK}</i>Personalized options</span><span><i>{CK}</i>No cost to review</span></div>
    </div>
    <div class="acts">
      <a class="btn p" href="tel:+14806602518"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/></svg>480.660.2518</a>
      <a class="btn s" href="mailto:hello@moxiemortgage.com">hello@moxiemortgage.com</a>
    </div>
  </section>

  <section class="faq" aria-labelledby="faq-h">
    <h2 id="faq-h">Questions about your refinance benefit</h2>
    <dl>
      <div><dt>What is the Moxie Client Benefit?</dt><dd>Clients whose current mortgage closed with Moxie Mortgage pay no Moxie lender fees (origination, processing and underwriting) when they refinance that home with Moxie. Terms apply; see disclosure 1.</dd></div>
      <div><dt>Which fees does Moxie cover?</dt><dd>Moxie covers its own origination, processing and underwriting fees. Third-party and government fees, such as appraisal, credit report, title, settlement, recording fees and transfer taxes, plus prepaid interest, escrow deposits and any discount points you choose, are not covered.</dd></div>
      <div><dt>How often can I use the benefit?</dt><dd>You can use it every time rates drop, after making at least 6 consecutive on-time payments on your current Moxie loan, for as long as you own the home. The benefit may change or end at any time, but changes won't affect a loan already locked.</dd></div>
      <div><dt>Does refinancing always save money?</dt><dd>Not always. Refinancing can restart or extend your loan term, which can increase the total interest you pay over the life of the loan. Moxie will show you the full cost and savings before you decide.</dd></div>
      <div><dt>How do I see if I can lower my payment?</dt><dd>Call 480.660.2518 or email hello@moxiemortgage.com. Because Moxie already has your file, we'll review your options within one business day, at no cost and with no obligation.</dd></div>
    </dl>
  </section>

  <footer class="disc">
    <ol>
      <li><b>Moxie Client Benefit.</b> Available to borrowers whose current mortgage closed with Moxie Mortgage who refinance that home with Moxie Mortgage after making at least 6 consecutive on-time monthly payments on the current loan. Covered “lender fees” are Moxie’s origination, processing and underwriting fees only. Not included: third-party and government fees (such as appraisal, credit report, title, settlement, recording fees and transfer taxes), prepaid interest, escrow or impound deposits, and any discount points you choose to pay. Covered fees may be provided as a lender credit. All loans are subject to credit approval, underwriting guidelines, property eligibility and program requirements; not all applicants will qualify, and a refinance must provide a benefit to you. The benefit has no cash value, is not transferable and may be changed or discontinued at any time; changes will not affect a loan already locked.</li>
      <li><b>Hypothetical example</b> for illustration only. It is not a loan offer, rate quote or commitment to lend. Assumes the monthly principal and interest payment decreases by $300 after each refinance, a second refinance 2 years after the first, and $2,300 in Moxie lender fees per refinance. The total adds payment reductions and covered lender fees over the 5 years after the first refinance and does not subtract third-party closing costs. Refinancing may restart or extend your loan term, which can increase the total interest and finance charges you pay over the life of the loan. Your results will depend on your rate, loan amount, term, credit, property and other factors.</li>
      <li>Client review posted on Google. Savings reflect this client’s combined monthly payment reduction across two refinances and are not typical or guaranteed; individual results vary.</li>
    </ol>
    <div class="legal">{EHO}<p>Moxie Mortgage is a division of NEXA Mortgage, LLC · NMLS #1660690 (nmlsconsumeraccess.org) · AZMB 0944059. Equal Housing Opportunity. This is not a commitment to lend or an offer to extend credit. Rates, terms, programs and availability are subject to change without notice and are not available in all states. Moxie Mortgage is not affiliated with or acting on behalf of any government agency. © 2026 Moxie Mortgage.</p></div>
  </footer>
</main>
</body>
</html>'''
def mincss(m):
    c=m.group(1)
    c=re.sub(r'/\*.*?\*/','',c,flags=re.S); c=re.sub(r'\s+',' ',c); c=re.sub(r'\s*([{{}};:,>])\s*',r'\1',c); c=c.replace(';}','}')
    return '<style>'+c+'</style>'
html=re.sub(r'<style>(.*?)</style>',mincss,html,flags=re.S)
open('moxie-lower-your-payment.html','w').write(html)
print(len(html))

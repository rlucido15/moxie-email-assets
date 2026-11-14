import re, json
src = open('moxie-lower-your-payment.html').read()
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
body = re.search(r'<body>(.*?)</body>', src, re.S).group(1)
ld = re.search(r'(<script type="application/ld\+json">.*?</script>)', src, re.S).group(1)

# ---- markup: avoid tags Lofty restyles
body = re.sub(r'<b>', '<strong>', body); body = body.replace('</b>', '</strong>')
body = re.sub(r'<i>', '<span class="ico">', body); body = body.replace('</i>', '</span>')
body = re.sub(r'<header class="top">.*?</header>', '', body, flags=re.S)
body = body.replace('You save <em>twice.</em>', 'You save <em>four times.</em>')
body = re.sub(r'<div class="legal">.*?</div>', '', body, flags=re.S)
body = body.replace('<footer class="disc">', '<footer class="disc"><h2 class="disc-h">Disclosures</h2>')
body = body.replace('<main class="page">', '<div class="page">').replace('</main>', '</div>')

# ---- css: drop page-shell / print rules, then scope everything under .mxrb
css = css.replace("@page{size:letter;margin:0}", "")
css = re.sub(r'@media print\{.*?\}\}', '', css)
css = re.sub(r'body\{[^}]*\}', '', css)
css = css.replace('.page{width:8.5in;min-height:11in;', '.page{width:100%;max-width:1040px;')
css = re.sub(r'\*\{margin:0;padding:0;box-sizing:border-box\}', '', css)

def scope_rules(block):
    out = []
    i = 0
    while i < len(block):
        if block.startswith('@media', i) or block.startswith('@supports', i):
            j = block.index('{', i); depth = 1; k = j + 1
            while depth:
                depth += {'{': 1, '}': -1}.get(block[k], 0); k += 1
            out.append(block[i:j+1] + scope_rules(block[j+1:k-1]) + '}'); i = k; continue
        if block.startswith('@keyframes', i) or block.startswith('@font-face', i):
            j = block.index('{', i); depth = 1; k = j + 1
            while depth:
                depth += {'{': 1, '}': -1}.get(block[k], 0); k += 1
            out.append(block[i:k]); i = k; continue
        j = block.find('{', i)
        if j < 0: break
        k = block.index('}', j)
        sel = block[i:j].strip(); decl = block[j+1:k]
        sels = []
        for s in sel.split(','):
            s = s.strip()
            if s == ':root': sels.append('.mxrb')
            elif s.startswith('.mxrb'): sels.append(s)
            else: sels.append('.mxrb ' + s)
        out.append(','.join(sels) + '{' + decl + '}'); i = k + 1
    return ''.join(out)
css = re.sub(r'(?<=[ >])b(?=[{,: >])', 'strong', css)
css = re.sub(r'(?<=[ >])i(?=[{,: >])', '.ico', css)
css = scope_rules(css)
base = (".mxrb{background:#F4F8FA;padding:48px 16px;font-family:Barlow,'Barlow Fallback',Arial,sans-serif;color:#0E2A47;-webkit-font-smoothing:antialiased}"
        ".mxrb *,.mxrb *::before,.mxrb *::after{box-sizing:border-box}"
        ".mxrb h1,.mxrb h2,.mxrb h3,.mxrb h4,.mxrb p,.mxrb ul,.mxrb ol,.mxrb li,.mxrb dl,.mxrb dt,.mxrb dd,.mxrb figure{margin:0;padding:0}"
        ".mxrb.mxrb p{padding:0 !important}"
        ".mxrb.mxrb ol{padding-left:12px !important}.mxrb.mxrb ol>li{list-style:decimal;padding:0 !important}"
        ".mxrb.mxrb .sum ul>li{list-style:none;padding:4px 0 !important}"
        ".mxrb strong{display:inline}.mxrb .sum li span strong{display:block}"
        ".mxrb a{text-decoration:none}"
        ".mxrb.mxrb figure.quote{padding:12px 16px !important;margin:0 !important}"
        ".mxrb .ico{display:inline-flex}"
        ".mxrb .page{margin:0 auto}"
        ".mxrb .page>.head{padding-top:40px}"
        "@media (max-width:860px){.mxrb{padding:0}.mxrb .page>.head{padding-top:28px}.mxrb .exhead{flex-direction:column;align-items:flex-start;gap:2px}.mxrb .exhead h3{text-wrap:balance}}")
web = (".mxrb{padding:64px 20px}"
       ".mxrb .page>.head{padding-top:56px}"
       ".mxrb .wrap{padding-left:64px;padding-right:64px}"
       ".mxrb .lede{margin-top:14px;font-size:17px;line-height:1.55}"
       ".mxrb .hero{margin-top:32px;padding:36px 40px;gap:32px}"
       ".mxrb .hero h2{margin-top:14px}.mxrb .hero p{margin-top:12px;font-size:15px;line-height:1.55;max-width:620px}.mxrb .lede{max-width:680px}"
       ".mxrb .ex{margin-top:48px}.mxrb .exgrid{margin-top:16px;gap:20px}"
       ".mxrb .chart{padding:24px 22px 18px}"
       ".mxrb .sum ul{padding:16px 22px 8px}.mxrb.mxrb .sum ul>li{padding:10px 0 !important}"
       ".mxrb .sum .tot{padding:16px 22px}"
       ".mxrb .proof{margin-top:28px;gap:20px}"
       ".mxrb.mxrb figure.quote{padding:20px 24px !important}.mxrb .quote p{margin-top:8px;font-size:14px;line-height:1.55}.mxrb .quote .by{margin-top:10px}"
       ".mxrb .stat{padding:20px 24px}"
       ".mxrb.mxrb .cta{margin-top:56px !important;padding:36px 64px}"
       ".mxrb .cta p{margin-top:8px}.mxrb .chips{margin-top:14px;gap:8px 18px}.mxrb .acts{gap:10px}"
       ".mxrb .faq{padding:48px 64px 16px}.mxrb .faq dl{margin-top:18px;gap:22px 40px}.mxrb .faq dd{margin-top:6px}"
       ".mxrb .disc{padding:24px 64px 40px;font-size:11px;line-height:1.5}.mxrb .disc li{margin-bottom:6px}.mxrb .disc .legal{margin-top:12px;padding-top:12px}"
       ".mxrb .exhead h3{font-size:clamp(26px,3vw,32px);line-height:1.1;letter-spacing:-.02em}"
       ".mxrb .proof{margin-top:56px;margin-bottom:24px}"
       ".mxrb .faq{background:#F4F8FA;margin:0;padding:56px 64px 48px;border-top:1px solid #DCE6EB}"
       ".mxrb .faq h2{font-size:clamp(24px,2.6vw,28px)}"
       ".mxrb .faq dl>div{background:#fff;border:1px solid #DCE6EB;border-radius:14px;padding:18px 20px}"
       ".mxrb .disc{border-top:1px solid #DCE6EB;padding-top:28px}"
       ".mxrb .disc-h{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#7A8A99;margin:0 0 12px}"
       "@media (max-width:860px){.mxrb{padding:0}.mxrb .page>.head{padding-top:32px}.mxrb .wrap,.mxrb .faq,.mxrb .disc{padding-left:22px;padding-right:22px}"
       ".mxrb .hero{padding:28px 22px;gap:24px}.mxrb .ex{margin-top:36px}.mxrb .exgrid{gap:16px}.mxrb .proof{gap:16px}"
       ".mxrb.mxrb .cta{margin-top:36px !important;padding:30px 22px}.mxrb .faq{padding:36px 22px 32px}.mxrb .proof{margin-top:40px;margin-bottom:8px}.mxrb .disc{padding-bottom:32px}}")
css = base + css + web
html = ('<!-- Moxie Client Benefit: refinance page block. Paste into a Lofty custom HTML block. -->\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800;900&display=swap">\n'
        '<style>' + css + '</style>\n'
        '<section class="mxrb" aria-label="Moxie Client Benefit">' + body.strip() + '</section>\n' + ld + '\n')
open('moxie-refinance-benefit-embed.html', 'w').write(html)
print(len(html))

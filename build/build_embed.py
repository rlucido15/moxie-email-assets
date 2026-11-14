import re, json
src = open('moxie-lower-your-payment.html').read()
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
body = re.search(r'<body>(.*?)</body>', src, re.S).group(1)
ld = re.search(r'(<script type="application/ld\+json">.*?</script>)', src, re.S).group(1)

# ---- markup: avoid tags Lofty restyles
body = re.sub(r'<b>', '<strong>', body); body = body.replace('</b>', '</strong>')
body = re.sub(r'<i>', '<span class="ico">', body); body = body.replace('</i>', '</span>')
body = re.sub(r'<header class="top">.*?</header>', '', body, flags=re.S)
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
        ".mxrb .ico{display:inline-flex}"
        ".mxrb .page{margin:0 auto}"
        ".mxrb .page>.head{padding-top:40px}"
        "@media (max-width:860px){.mxrb{padding:0}.mxrb .page>.head{padding-top:28px}.mxrb .exhead{flex-direction:column;align-items:flex-start;gap:2px}.mxrb .exhead h3{text-wrap:balance}}")
css = base + css
html = ('<!-- Moxie Client Benefit: refinance page block. Paste into a Lofty custom HTML block. -->\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800;900&display=swap">\n'
        '<style>' + css + '</style>\n'
        '<section class="mxrb" aria-label="Moxie Client Benefit">' + body.strip() + '</section>\n' + ld + '\n')
open('moxie-refinance-benefit-embed.html', 'w').write(html)
print(len(html))

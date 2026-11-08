"""Post-build optimizer: drops unused CSS, compacts CSS, minifies JS, adds connection hints."""
import re, subprocess

TERSER = '/tmp/jsmin/node_modules/.bin/terser'


def _blocks(css):
    """Split CSS into top-level blocks: (prelude, inner)."""
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0:
            break
        depth, k = 1, j + 1
        while depth:
            depth += {'{': 1, '}': -1}.get(css[k], 0); k += 1
        out.append((css[i:j].strip(), css[j + 1:k - 1]))
        i = k
    return out


def _purge(css, used):
    keep = []
    for pre, inner in _blocks(css):
        if pre.startswith('@media') or pre.startswith('@supports'):
            sub = _purge(inner, used)
            if sub:
                keep.append(pre + '{' + sub + '}')
        elif pre.startswith('@'):
            keep.append(pre + '{' + inner + '}')
        else:
            sels = [s for s in pre.split(',') if all(c in used for c in re.findall(r'\.([A-Za-z][\w-]*)', s))]
            if sels:
                keep.append(','.join(x.strip() for x in sels) + '{' + inner.strip() + '}')
    return ''.join(keep)


def _compact(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};,>])\s*', r'\1', css)
    css = re.sub(r':\s+', ':', css)
    return css.replace(';}', '}').strip()


def optimize(html, hero_img=None):
    # every word that appears outside <style> blocks counts as a possibly-used class
    no_style = re.sub(r'<style>.*?</style>', '', html, flags=re.S)
    used = set(re.findall(r'[A-Za-z][\w-]*', no_style))
    before = sum(len(m) for m in re.findall(r'<style>(.*?)</style>', html, flags=re.S))
    html = re.sub(r'<style>(.*?)</style>', lambda m: '<style>' + _compact(_purge(m.group(1), used)) + '</style>', html, flags=re.S)
    after = sum(len(m) for m in re.findall(r'<style>(.*?)</style>', html, flags=re.S))

    # minify the inline script (JSON-LD untouched)
    def mini(m):
        js = subprocess.run([TERSER, '--compress', 'passes=2', '--mangle'], input=m.group(1), capture_output=True, text=True, check=True).stdout
        return '<script>' + js.strip() + '</script>'
    html = re.sub(r'<script>(.*?)</script>', mini, html, flags=re.S)

    # images come from jsDelivr without CORS; fonts preload with CORS: open both connections early
    hint = '<link rel="preconnect" href="https://cdn.jsdelivr.net">\n<link rel="dns-prefetch" href="https://lh3.googleusercontent.com">\n'
    html = html.replace('<link rel="preload"', hint + '<link rel="preload"', 1)
    print(f'css {before} -> {after} bytes')
    return html

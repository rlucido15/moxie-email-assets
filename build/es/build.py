"""Merge the Spanish string files and write one small dictionary per page root (only the strings that page uses)."""
import json, re, glob, os
HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = {  # page root id -> (extracted source json, page file whose keys are always included)
    'mx-home': ('moxie-home-embed', 'mx-home'), 'mx-buy': ('moxie-buy-embed', 'mx-buy'), 'mx-refi': ('moxie-refinance-embed', 'mx-refi'),
    'mx-products': ('moxie-products-embed', 'mx-products'), 'mx-faqs': ('moxie-faqs-embed', 'mx-faqs'), 'mx-about': ('moxie-about-embed', 'mx-about'),
    'mx-stories': ('moxie-client-success-embed', 'mx-stories'), 'mx-calc-hub': ('moxie-calculators-embed', 'calc-pages'),
    'mx-calc-mortgage': ('moxie-calc-mortgage-embed', 'calc-pages'), 'mx-calc-afford': ('moxie-calc-affordability-embed', 'calc-pages'),
    'mx-calc-rentbuy': ('moxie-calc-rentvsbuy-embed', 'calc-pages'), 'mx-ad': ('moxie-area-director-embed', 'mx-ad'), 'mx-lo': ('moxie-loan-officer-embed', 'mx-lo'),
    # calculator apps (inside the calculator pages' frames): their own file is used whole
    'app-afford': ('app-afford', 'app-afford'), 'app-rentbuy': ('app-rentbuy', 'app-rentbuy'), 'app-mortgage': (None, 'app-mortgage'), 'heloc': (None, 'heloc'),
}
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
def load(name):
    ns = {}; exec(open(os.path.join(HERE, name + '.py'), encoding='utf-8').read(), ns); return {norm(k): v for k, v in ns['T'].items()}, ns.get('R', [])
FILES = {os.path.basename(f)[:-3]: load(os.path.basename(f)[:-3]) for f in glob.glob(os.path.join(HERE, '*.py')) if not os.path.basename(f).startswith(('build', '_'))}
GT, GR = {}, []
for k in ['common'] + sorted(x for x in FILES if x != 'common'):
    GT.update(FILES[k][0]); GR += [r for r in FILES[k][1] if r not in GR]
def page_dict(root):
    src, own = PAGES[root]
    strings = [norm(s) for s in json.load(open(os.path.join(HERE, f'_src_{src}.json'), encoding='utf-8'))] if src else []
    t = {} if (root.startswith('app-') or root == 'heloc') else {s: GT[s] for s in strings if s in GT}
    for k, v in FILES['common'][0].items():
        if k in strings: t[k] = v
    t.update(FILES[own][0])   # the page's own wording wins
    rx = FILES['common'][1] + [r for r in FILES[own][1] if r not in FILES['common'][1]]
    missing = [s for s in strings if s not in t and not any(re.search(p, s) for p, _ in GR)]
    return {'t': t, 'r': rx}, missing
if __name__ == '__main__':
    import sys
    for root in PAGES:
        d, miss = page_dict(root)
        json.dump(d, open(os.path.join(HERE, root + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        if root.startswith('app-'): miss = [m for m in miss if m not in GT]
        print(f'{root}: {len(d["t"])} strings, {len(json.dumps(d, ensure_ascii=False))//1024} KB')
        if '-v' in sys.argv:
            for s in miss: print('   MISSING |', s[:160])

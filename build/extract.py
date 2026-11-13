"""List every string a page shows (static text, attributes, UI strings inside its scripts) for translation."""
import re, sys, json, html
from html.parser import HTMLParser
SKIP = {'script', 'style', 'template', 'noscript', 'textarea'}
ATTRS = {'placeholder', 'aria-label', 'title', 'alt'}
class P(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.stack=[]; s.out=[]; s.scripts=[]; s.cur=None
    def handle_starttag(s, t, a):
        s.stack.append(t); d=dict(a)
        if t=='script' and d.get('type') not in ('application/ld+json',): s.cur=[]
        for k,v in a:
            if k in ATTRS and v and re.search('[A-Za-z]', v): s.out.append(v.strip())
            if k=='value' and t=='input' and d.get('type') in ('submit','button') and v: s.out.append(v)
    def handle_startendtag(s,t,a):
        s.handle_starttag(t,a); s.stack.pop()
    def handle_endtag(s, t):
        if t=='script' and s.cur is not None: s.scripts.append(''.join(s.cur)); s.cur=None
        while s.stack:
            x=s.stack.pop()
            if x==t: break
    def handle_data(s, d):
        if s.cur is not None: s.cur.append(d); return
        if any(x in SKIP for x in s.stack): return
        t=re.sub(r'\s+',' ',d).strip()
        if t and re.search('[A-Za-z]', t): s.out.append(t)
CODEY = re.compile(r'^[\w.#\[\]=:\-*>~+()\'" ,/]*$')
def js_strings(src):
    out=[]
    for m in re.finditer(r"'((?:[^'\\\n]|\\.){2,400})'|\"((?:[^\"\\\n]|\\.){2,400})\"|`((?:[^`\\]|\\.){2,600})`", src):
        s=m.group(1) or m.group(2) or m.group(3)
        if not s or not re.search(r'[A-Za-z]{2,}', s): continue
        if re.match(r'^(https?:|/|#|\.|data-|mx|[a-z\-]+:)', s) and ' ' not in s: continue
        if ' ' not in s and not re.match(r'^[A-Z][a-z]+$', s): continue   # identifiers, keys, selectors
        if re.search(r'[{};]|=>|function|querySelector|\bvar\b|px|rgba?\(|linear-gradient|\.\w+\(', s): continue
        if re.match(r'^[\w\-]+( [\w\-]+)*$', s) and s.lower()==s and len(s.split())<3: continue
        out.append(html.unescape(s.replace("\\'","'").replace('\\"','"')))
    return out
import subprocess
from html.parser import HTMLParser as _HP
def ui_like(s):
    s2=s.strip()
    if not re.search(r'[A-Za-z]{2,}', s2): return False
    if re.search(r'[{};]|=>|querySelector|\bvar\b|rgba?\(|linear-gradient|^https?:|^mailto:|^tel:', s2): return False
    if re.match(r'^[a-z0-9_\-\.\[\]=:#>*~+ "\'(),]+$', s2) and not re.search(r'[a-z]{3,} [a-z]{3,} [a-z]{3,}', s2): return False  # selectors, keys
    if re.match(r'^[A-Za-z]+$', s2) and not re.match(r'^[A-Z][a-z]+$', s2): return False
    return True
def html_frag_text(s):
    if '<' not in s: return [s]
    p=P(); p.feed(s); return p.out
def extract(path):
    h=open(path,encoding='utf-8').read()
    p=P(); p.feed(h)
    js=[]
    for sc in p.scripts:
        r=subprocess.run(['node','/home/claude/build/jsstr.js'],input=sc,capture_output=True,text=True).stdout
        try: arr=json.loads(r)
        except Exception: arr=[]
        if isinstance(arr,dict): print('  js parse error',arr); arr=[]
        for x in arr:
            for t in html_frag_text(x):
                t=re.sub(r'\s+',' ',t).strip()
                if t and ui_like(t): js.append(t)
    seen=[];[seen.append(x) for x in p.out+js if x not in seen]
    return seen
if __name__=='__main__':
    for f in sys.argv[1:]:
        r=extract(f); print(f, len(r))
        json.dump(r, open('/home/claude/build/es/_src_'+f.split('/')[-1].replace('.html','.json'),'w'), ensure_ascii=False, indent=0)

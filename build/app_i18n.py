"""Add (or refresh) the Spanish layer inside each calculator app's index.html. Run after publish_es.sh pins the dictionaries."""
import re, sys
from i18n import I18N_JS
PIN = open('/home/claude/build/es/_cdn.txt').read().strip()
APPS = {'/home/claude/mortgage-calculator/index.html': 'app-mortgage',
        '/home/claude/affordability-calculator/index.html': 'app-afford',
        '/home/claude/rent-vs-buy-calculator/index.html': 'app-rentbuy'}
for path, name in APPS.items():
    url = f'https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@{PIN}/website/es/{name}.json'
    block = f'''<!--mx-i18n-->
<style>.mx-es-wait{{visibility:hidden}}</style>
<script>
{I18N_JS.strip()}
(function () {{
  // Spanish: opens in ?lang=es, follows the parent page's EN/ES toggle, translates text in place so the calculator keeps working
  function start() {{ MX.i18n.load(document.body, '{url}'); }}
  if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
  window.addEventListener('message', function (e) {{
    if (!/^https:\\/\\/(www\\.)?moxiemortgage\\.com$/.test(e.origin)) return;
    var l = e.data && e.data.mxLang; if (l === 'es' || l === 'en') MX.i18n.set(l);
  }});
}})();
</script>
<!--/mx-i18n-->'''
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'\n?<!--mx-i18n-->.*?<!--/mx-i18n-->', '', s, flags=re.S)
    i = s.rfind('</body>')
    s = s[:i] + block + '\n' + s[i:] if i >= 0 else s + block
    open(path, 'w', encoding='utf-8').write(s)
    print(name, 'ok', len(s))

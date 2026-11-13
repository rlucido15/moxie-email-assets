"""Spanish add-on for the /heloc page: a small Custom Code block placed after the HELOC block. It leaves the HELOC embed untouched
and translates it in place when the visitor picks ES (dictionary fetched only for Spanish)."""
import os
from i18n import I18N_JS
from optimize import optimize
PIN = open('/home/claude/build/es/_cdn.txt').read().strip()
URL = f'https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@{PIN}/website/es/heloc.json'
html = f"""<!--
  MOXIE MORTGAGE · HELOC SPANISH ADD-ON
  Paste into a Lofty "Custom Code / Embed" block directly BELOW the HELOC block on /heloc. It adds Spanish to the HELOC section
  (follows the header's EN | ES toggle). The HELOC block itself stays exactly as it is.
-->
<style>.mx-es-wait{{visibility:hidden}}</style>
<script>
{I18N_JS.strip()}
(function () {{
  function go() {{ var r = document.querySelector('.mxfh'); if (r) MX.i18n.load(r, '{URL}'); }}
  if (document.querySelector('.mxfh')) go(); else document.addEventListener('DOMContentLoaded', go);
}})();
</script>
"""
out = '/home/claude/build/out/moxie-heloc-es-addon.html'
open(out, 'w').write(optimize(html))
print('heloc add-on ok', os.path.getsize(out))

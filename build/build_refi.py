"""Rebuild refi-widget.js: React + ReactDOM from the original widget export, plus the edited app source, minified."""
import re,subprocess
s=open('/tmp/refiw/widget.html').read()
a=re.findall(r'<script[^>]*>(.*?)</script>',s,re.S)
m=subprocess.run(['node','/tmp/jsmin/node_modules/terser/bin/terser','/home/claude/build/widgets/refi-app.src.js','-c','-m','--comments','false'],capture_output=True,text=True)
assert m.returncode==0,m.stderr
open('/home/claude/build/widgets/refi-widget.js','w').write(a[0].strip()+'\n'+a[1].strip()+'\n'+m.stdout.strip()+'\n'+a[3].strip()+'\n')
print('widget ok')

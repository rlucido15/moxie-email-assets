"""Lofty Custom Code block for the Refinance Review widget ("How much could you be saving"). The widget code is hosted on jsDelivr,
so the block itself is tiny. The /refinance page embed moves this block into its hero automatically."""
W = 'https://cdn.jsdelivr.net/gh/rlucido15/moxie-email-assets@9a43f72/website/widgets/refi-widget.js'
html = f"""<!--
  MOXIE MORTGAGE · REFINANCE REVIEW WIDGET ("How much could you be saving on your mortgage?")
  Paste into a Lofty "Custom Code / Embed" block anywhere on /refinance (e.g. right below the refinance block).
  The refinance page moves it into the hero card on its own. Leads go to Lofty tagged "CTA: Refinance Review".
-->
<div id="moxie-refinance-root" data-mx-host="1" style="width:100%;min-height:360px"></div>
<script src="{W}" defer></script>
"""
open('out/moxie-refi-widget.html','w').write(html); print('ok')

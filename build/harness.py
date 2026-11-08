import asyncio, json, sys, re
from playwright.async_api import async_playwright
OUT='/home/claude/build/out/'
def page(embed, extra=''):
    e=open(OUT+embed).read()
    f=open(OUT+'moxie-footer-embed.html').read()
    return f"""<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<style>body{{margin:0;font-family:Barlow,sans-serif}} .lofty-header{{height:80px;background:#eee}} .mg-container{{max-width:1170px;margin:0 auto;padding:0 15px;overflow:hidden}} .custom-code-html-content ul li{{list-style:disc;padding:0;margin-left:20px}} .custom-code-html-content ul{{padding-left:40px}}</style></head>
<body><div class=lofty-header>Lofty header</div><main class="page-content" id="app">
<div class="md-custom-code html-code"><div class="mg-container"><div class="custom-code-html-content">{e}</div></div></div>
{extra}
<div class="md-custom-code html-code"><div class="mg-container"><div class="custom-code-html-content">{f}</div></div></div>
</main></body></html>"""
WIDGET='<div class="md-custom-code html-code"><div class="mg-container"><div class="custom-code-html-content"><div id="fakewidget" style="background:#123;color:#fff;padding:40px;border-radius:20px">YOUR NEW PAYMENT IN 60 SECONDS<h2>How much could you be saving on your mortgage?</h2><button onclick="this.textContent=\'clicked\'">Show me my numbers</button></div></div></div></div>'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,embed,extra in [('buy','moxie-buy-embed.html',''),('refi','moxie-refinance-embed.html',WIDGET),('products','moxie-products-embed.html',''),('faqs','moxie-faqs-embed.html','')]:
            open(f'{name}.html','w').write(page(embed,extra))
        async def run(name, q='', tz='America/New_York', vw=1440, shot=None, fn=None):
            ctx=await b.new_context(viewport={'width':vw,'height':900},timezone_id=tz)
            await ctx.route(re.compile(r'https?://(?!localhost).*'), lambda r: r.abort())
            pg=await ctx.new_page(); errs=[]
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(f'file:///home/claude/test/{name}.html{q}'); await pg.wait_for_timeout(700)
            res = await fn(pg) if fn else None
            if shot: await pg.screenshot(path=shot, full_page=True)
            # json-ld validity
            lds = await pg.eval_on_selector_all('script[type="application/ld+json"]','els=>els.map(e=>e.textContent)')
            for t in lds: json.loads(t)
            hs = await pg.eval_on_selector_all('h1','els=>els.length')
            ow = await pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            print(f'{name}{q} tz={tz} vw={vw} errs={errs} h1={hs} overflowX={ow} res={res}')
            await ctx.close()
        h=lambda pg: pg.evaluate("[document.querySelector('[data-mx=eyebrow]')?.textContent, document.querySelector('[data-mx=h1]')?.textContent, document.querySelector('[data-mx=cta]')?.textContent, document.querySelector('[data-mx=cta2]')?.textContent, document.querySelector('[data-mx=img]')?.getAttribute('src')?.split('/').pop()]")
        await run('buy', fn=h, shot='buy.png')
        await run('buy', tz='Pacific/Honolulu', fn=h)
        await run('buy','?hero=returning', fn=h)
        await run('buy','?hero=hawaii', vw=390, fn=h, shot='buy-m.png')
        async def tabs(pg):
            await pg.click('#mxb-t2'); return await pg.evaluate("[document.getElementById('mxb-p1').hidden, document.getElementById('mxb-p2').hidden]")
        await run('buy', fn=tabs)
        async def refi(pg):
            return await pg.evaluate("[!!document.querySelector('#mx-refi-slot #fakewidget'), document.querySelector('[data-mx=h1]').textContent, getComputedStyle(document.querySelectorAll('.md-custom-code')[1]).display]")
        await run('refi', fn=refi, shot='refi.png')
        await run('refi', tz='Pacific/Honolulu', fn=refi)
        async def prod(pg):
            await pg.click('.mx-chip[data-f="self"]')
            return await pg.evaluate("[document.querySelectorAll('.mx-prod:not([hidden])').length, document.querySelectorAll('.mx-group:not([hidden])').length]")
        await run('products', fn=prod, shot='products.png')
        await run('products', vw=390, shot='products-m.png')
        async def faq(pg):
            await pg.fill('#mxf-q','down payment'); await pg.wait_for_timeout(100)
            a=await pg.evaluate("[document.getElementById('mxf-sum').textContent, document.querySelectorAll('.mx-cgroup details:not([hidden])').length]")
            await pg.fill('#mxf-q','zzzz'); b2=await pg.evaluate("!document.getElementById('mxf-empty').hidden")
            await pg.click('#mxf-clear'); await pg.click('.mx-cat[data-c="credit"]'); c=await pg.evaluate("document.getElementById('mxf-sum').textContent")
            return a,b2,c
        await run('faqs', fn=faq)
        await run('faqs', shot='faqs.png')
        await b.close()
asyncio.run(main())

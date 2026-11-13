p = '/home/claude/canvas/project/Main.dc.html'
s = open(p, encoding='utf-8').read()
sec = '''  <!-- SAVINGS ESTIMATOR -->
  <section aria-labelledby="sav-h2" style="padding: 92px 24px">
    <div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 48px; align-items: center">
      <div style="flex: 1 1 440px; min-width: 0">
        <p style="margin: 0 0 10px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; font-size: 15px; color: #127C8F">Savings estimator</p>
        <h2 id="sav-h2" style="margin: 0; font-size: clamp(32px, 3.6vw, 46px); line-height: 1.08; font-weight: 800; letter-spacing: -0.015em">See what you could save with Moxie</h2>
        <p style="margin: 16px 0 0; color: #4A5868; font-size: 19px; max-width: 520px">Our rates have averaged <strong style="color: #0E2A47">0.559% lower</strong> than the nation's largest retail lender over the past 12 months.<span class="mx-dag">‡</span></p>
        <div style="margin-top: 36px; max-width: 520px">
          <div style="display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-bottom: 12px">
            <label for="sav-amt" style="font-weight: 700; font-size: 17px">Loan amount</label>
            <output for="sav-amt" style="font-size: 32px; font-weight: 800; font-variant-numeric: tabular-nums">{{amtLabel}}</output>
          </div>
          <input id="sav-amt" type="range" min="100000" max="1500000" step="10000" value="{{amount}}" onInput="{{onAmt}}" style="width: 100%; accent-color: #1C97AE; height: 28px; cursor: pointer">
          <div style="display: flex; justify-content: space-between; font-size: 14px; color: #4A5868; margin-top: 4px"><span>$100K</span><span>$1.5M</span></div>
        </div>
      </div>
      <div style="flex: 1 1 400px; min-width: 0; background: #0E2A47; color: #ffffff; border-radius: 24px; padding: 36px; box-shadow: 0 24px 50px rgba(14,42,71,.22)">
        <p style="margin: 0; font-size: 15px; color: #C9D6DF; font-weight: 600">Your estimated savings with Moxie</p>
        <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin-top: 18px">
          <div style="background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.14); border-radius: 16px; padding: 20px">
            <strong style="display: block; font-size: clamp(30px, 3.2vw, 42px); line-height: 1.05; font-variant-numeric: tabular-nums; color: #ffffff">{{monthly}}</strong>
            <span style="font-size: 15px; color: #C9D6DF">per month</span>
          </div>
          <div style="background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.14); border-radius: 16px; padding: 20px">
            <strong style="display: block; font-size: clamp(30px, 3.2vw, 42px); line-height: 1.05; font-variant-numeric: tabular-nums; color: #F46744">{{lifetime}}</strong>
            <span style="font-size: 15px; color: #C9D6DF">over the life of a 30-year loan</span>
          </div>
        </div>
        <p style="margin: 16px 0 24px; font-size: 15px; color: #C9D6DF">That's about <strong style="color: #ffffff">{{fiveYear}}</strong> in your first five years.</p>
        <a href="#" class="mx-btn-p" style="display: flex; justify-content: center; align-items: center; min-height: 52px; background: #F46744; color: #0E2A47; font-weight: 700; font-size: 18px; border-radius: 12px; text-decoration: none">Lock in my savings</a>
        <p style="margin: 14px 0 0; font-size: 12px; line-height: 1.5; color: #9FB3C2">Estimate only, not a loan offer. Principal and interest on a 30-year fixed loan. Your rate and savings depend on credit, property, and market conditions.</p>
      </div>
    </div>
  </section>

'''
anchor = '  <!-- TIME IS OF THE ESSENCE -->'
assert anchor in s
s = s.replace(anchor, sec + anchor, 1)
old = 'Conditions and exclusions apply.</p>'
assert old in s
s = s.replace(old, old + '\n    <p style="margin: 10px 0 0">‡ Based on Moxie Mortgage’s apples-to-apples comparison of weekly rates against Rocket Mortgage from November 2025 to November 2026; average difference 0.559%. Savings estimates compare principal and interest at a 6.75% example rate with a rate 0.559% lower. Individual results vary.</p>', 1)
s = s.replace("this.state = { tab: 'now' };", "this.state = { tab: 'now', amount: 400000 };")
old2 = "    return {\n      ...hero,"
assert old2 in s
s = s.replace(old2, """    const L = this.state.amount, pay = (r) => { const i = r / 1200; return L * i / (1 - Math.pow(1 + i, -360)); };
    const save = pay(6.75) - pay(6.75 - 0.559);
    const usd = (n) => '$' + Math.round(n).toLocaleString('en-US');
    return {
      ...hero,
      amount: L, amtLabel: usd(L), monthly: usd(save), lifetime: usd(save * 360), fiveYear: usd(save * 60),
      onAmt: (e) => this.setState({ amount: Number(e.target.value) }),""", 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')

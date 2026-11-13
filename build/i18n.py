"""Shared English/Spanish switch for every Moxie embed (header, footer, pages).

How it works
- Language = ?lang=es|en in the URL, else the visitor's saved choice (localStorage "mx_lang"), else English.
- MX.i18n.set('es') saves the choice, rewrites the URL (?lang=es) and every internal link so the choice
  follows the visitor and Spanish pages can be shared, sets <html lang>, and fires a "mx:lang" event.
- Markup opts in with attributes, so one embed carries both languages:
    data-es="<Spanish inner HTML>"        swaps the element's content
    data-es-aria / data-es-title / data-es-placeholder / data-es-alt   swap that attribute
  Embeds that hold a whole Spanish body use <template data-mx-es> + MX.i18n.swap(root) instead.
Defined once per page no matter how many embeds include it.
"""

I18N_JS = r"""
(function () {
  var MX = window.MX || (window.MX = {});
  if (MX.i18n) return;
  var KEY = 'mx_lang', ATTRS = ['aria-label', 'title', 'placeholder', 'alt'];
  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function save(l) { try { localStorage.setItem(KEY, l); } catch (e) {} }
  var q = null; try { q = new URLSearchParams(location.search).get('lang'); } catch (e) {}
  var lang = (q === 'es' || q === 'en') ? q : (saved() === 'es' ? 'es' : 'en');
  if (q === 'es' || q === 'en') save(lang);
  function withLang(href) {
    try {
      var u = new URL(href, location.href);
      if (u.origin !== location.origin || /^(mailto|tel):/.test(href)) return null;
      if (lang === 'es') u.searchParams.set('lang', 'es'); else u.searchParams.delete('lang');
      return u.pathname + u.search + u.hash;
    } catch (e) { return null; }
  }
  function links(scope) {
    (scope || document).querySelectorAll('a[href]').forEach(function (a) {
      var h = a.getAttribute('href'); if (!h || h.charAt(0) === '#' || a.hasAttribute('data-mx-nolang')) return;
      var n = withLang(h); if (n !== null && n !== h) a.setAttribute('href', n);
    });
  }
  function apply(scope) {
    scope = scope || document;
    scope.querySelectorAll('[data-es]').forEach(function (el) {
      if (!el.hasAttribute('data-en')) el.setAttribute('data-en', el.innerHTML);
      el.innerHTML = lang === 'es' ? el.getAttribute('data-es') : el.getAttribute('data-en');
    });
    ATTRS.forEach(function (a) {
      scope.querySelectorAll('[data-es-' + a.replace('aria-label', 'aria') + ']').forEach(function (el) {
        var k = 'data-es-' + a.replace('aria-label', 'aria'), ke = 'data-en-' + a.replace('aria-label', 'aria');
        if (!el.hasAttribute(ke)) el.setAttribute(ke, el.getAttribute(a) || '');
        el.setAttribute(a, lang === 'es' ? el.getAttribute(k) : el.getAttribute(ke));
      });
    });
    links(scope);
  }
  // Whole-body swap for page embeds: <template data-mx-es> holds the Spanish markup for that root.
  function swap(root) {
    var t = root && root.querySelector('template[data-mx-es]');
    if (!t) return false;
    var host = root.querySelector('[data-mx-body]');
    if (!host) return false;
    if (!host.__en) host.__en = host.innerHTML;
    host.innerHTML = lang === 'es' ? t.innerHTML : host.__en;
    return true;
  }

  // ---- dictionary translation: swaps text nodes / attributes in place, so every listener, form and calculator keeps working.
  // D = { t: { "English text": "Spanish text", ... }, r: [ ["^regex source$", "Spanish with $1"], ... ] }
  var REGS = [], TATTR = ['placeholder', 'aria-label', 'title', 'alt'];
  var SKIP = { SCRIPT: 1, STYLE: 1, TEXTAREA: 1, NOSCRIPT: 1, TEMPLATE: 1, CODE: 1 };
  function norm(s) { return s.replace(/\s+/g, ' ').trim(); }
  function look(reg, raw) {
    var k = norm(raw); if (!k) return null;
    var v = reg.t[k]; if (v != null) return v;
    for (var i = 0; i < reg.rx.length; i++) { if (reg.rx[i][0].test(k)) return k.replace(reg.rx[i][0], reg.rx[i][1]); }
    return null;
  }
  function skipEl(el) { for (; el && el !== document; el = el.parentNode) { if (el.nodeType === 1 && (SKIP[el.tagName] || el.hasAttribute('data-mx-noi18n'))) return true; } return false; }
  function doText(reg, n) {
    if (lang === 'es') {
      var cur = n.nodeValue;
      if (n.__mxEs != null && cur === n.__mxEs) return;
      var es = look(reg, cur); if (es == null) return;
      n.__mxEn = cur; var m = cur.match(/^(\s*)[\s\S]*?(\s*)$/);
      n.__mxEs = m[1] + es + m[2]; n.nodeValue = n.__mxEs;
    } else if (n.__mxEn != null) {
      if (n.nodeValue === n.__mxEs) n.nodeValue = n.__mxEn;
      n.__mxEn = n.__mxEs = null;
    }
  }
  function doAttrs(reg, el) {
    var list = TATTR.slice(); if (el.tagName === 'INPUT' && /^(submit|button)$/i.test(el.type)) list.push('value');
    for (var i = 0; i < list.length; i++) {
      var a = list[i]; if (!el.hasAttribute(a) || el.hasAttribute('data-es-' + a.replace('aria-label', 'aria'))) continue;
      var store = el.__mxA || (el.__mxA = {}), cur = el.getAttribute(a);
      if (lang === 'es') {
        if (store[a] && cur === store[a].es) continue;
        var es = look(reg, cur); if (es == null) continue;
        store[a] = { en: cur, es: es }; el.setAttribute(a, es);
      } else if (store[a]) { if (cur === store[a].es) el.setAttribute(a, store[a].en); delete store[a]; }
    }
  }
  function walk(reg, node) {
    if (node.nodeType === 3) { if (!skipEl(node.parentNode)) doText(reg, node); return; }
    if (node.nodeType !== 1 || SKIP[node.tagName] || node.hasAttribute('data-mx-noi18n')) return;
    doAttrs(reg, node);
    if (node.tagName === 'TEMPLATE') return;
    var tw = document.createTreeWalker(node, 5, null), n;
    while ((n = tw.nextNode())) {
      if (n.nodeType === 1) { if (SKIP[n.tagName] || n.hasAttribute('data-mx-noi18n')) continue; doAttrs(reg, n); }
      else if (!skipEl(n.parentNode)) doText(reg, n);
    }
  }
  function run(reg) {
    reg.busy = true; walk(reg, reg.root); reg.busy = false;
    if (lang === 'es' && !reg.obs && window.MutationObserver) {
      reg.obs = new MutationObserver(function (ms) {
        if (reg.busy || lang !== 'es') return; reg.busy = true;
        ms.forEach(function (m) {
          if (m.type === 'characterData') doText(reg, m.target);
          else if (m.type === 'attributes') doAttrs(reg, m.target);
          else m.addedNodes.forEach(function (x) { walk(reg, x); });
        });
        reg.busy = false;
      });
      reg.obs.observe(reg.root, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: TATTR.concat('value') });
    }
  }
  function dict(root, D) {
    if (!root || !D) return;
    var rx = (D.r || []).map(function (p) { return [new RegExp(p[0]), p[1]]; });
    var t = {}; for (var k in D.t) if (Object.prototype.hasOwnProperty.call(D.t, k)) t[norm(k)] = D.t[k];
    var reg = { root: root, t: t, rx: rx }; REGS.push(reg); run(reg); return reg;
  }
  // lazy dictionaries: English visitors never download them; Spanish visitors fetch once (cached by the CDN)
  var PEND = [];
  function fire(root) { try { document.dispatchEvent(new CustomEvent('mx:lang', { detail: { lang: lang, root: root } })); } catch (e) {} }
  function fetchDict(p) {
    if (p.state) return; p.state = 'loading';
    if (lang === 'es') p.root.classList.add('mx-es-wait');
    var done = function () { p.root.classList.remove('mx-es-wait'); };
    var t = setTimeout(done, 2500);
    fetch(p.url).then(function (r) { return r.json(); }).then(function (D) {
      p.state = 'ok'; dict(p.root, D); clearTimeout(t); done(); fire(p.root);
    }).catch(function () { p.state = null; clearTimeout(t); done(); });
  }
  function load(root, url) {
    if (!root || !url) return;
    var p = { root: root, url: url }; PEND.push(p);
    if (lang === 'es') fetchDict(p);
  }
  // translate / un-translate a single string with the page dictionaries (for scripts that rebuild text themselves)
  function lookAny(s) { for (var i = 0; i < REGS.length; i++) { var v = look(REGS[i], s); if (v != null) return v; } return null; }
  function rev(s) {
    var k = norm(s);
    for (var i = 0; i < REGS.length; i++) {
      var r = REGS[i]; if (!r.rv) { r.rv = {}; for (var e in r.t) r.rv[norm(r.t[e])] = e; }
      if (r.rv[k] != null) return r.rv[k];
    }
    return null;
  }
  function syncUrl() {
    try {
      var u = new URL(location.href);
      if (lang === 'es') u.searchParams.set('lang', 'es'); else u.searchParams.delete('lang');
      if (u.href !== location.href) history.replaceState(history.state, '', u.href);
    } catch (e) {}
  }
  MX.i18n = {
    get lang() { return lang; },
    t: function (en, es) { return lang === 'es' ? es : en; },
    apply: apply, swap: swap, links: links, dict: dict, load: load,
    text: function (en) { return lang === 'es' ? (lookAny(en) || en) : en; },
    en: function (s) { return rev(s) || s; },
    set: function (l) {
      l = l === 'es' ? 'es' : 'en'; if (l === lang) return;
      lang = l; save(l); syncUrl(); document.documentElement.lang = l === 'es' ? 'es' : 'en-US';
      apply(document);
      REGS.forEach(run); PEND.forEach(function (p) { if (l === 'es') fetchDict(p); });
      try { document.dispatchEvent(new CustomEvent('mx:lang', { detail: { lang: l } })); } catch (e) {}
      if (MX.track) MX.track('language_switch', { lang: l });
    }
  };
  syncUrl();
  if (lang === 'es') document.documentElement.lang = 'es';
  function ready() { apply(document); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready); else ready();
})();
"""

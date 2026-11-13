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
    apply: apply, swap: swap, links: links,
    set: function (l) {
      l = l === 'es' ? 'es' : 'en'; if (l === lang) return;
      lang = l; save(l); syncUrl(); document.documentElement.lang = l === 'es' ? 'es' : 'en-US';
      apply(document);
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

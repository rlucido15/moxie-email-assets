/**
 * Moxie Area Director application relay
 * ------------------------------------------------------------
 * Receives applications from the /areadirector page and creates the lead in
 * Lofty, tagged "CTA: AD Application". The Lofty API key lives only here
 * (Script Properties), never in the website code.
 *
 * Setup (one time):
 * 1. Lofty > Settings > Integrations > API: create a key with Leads > ADD permission.
 * 2. In this Apps Script project: Project Settings (gear) > Script Properties > Add:
 *      LOFTY_API_KEY   = <the key>
 *      NOTIFY_EMAIL    = robert@moxiemortgage.com   (backup copy of every application)
 * 3. Deploy > New deployment > type "Web app":
 *      Execute as: Me      Who has access: Anyone
 *    Copy the Web app URL (ends in /exec) and send it to Claude to plug into the page.
 */

var TAG = 'CTA: AD Application';
var SOURCE = 'Website - Area Director Application';

function doPost(e) {
  var props = PropertiesService.getScriptProperties();
  var d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return out({ ok: false, error: 'bad request' }); }

  // basic validation + abuse limits
  var s = function (v, n) { return String(v || '').replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, n); };
  var name = s(d.name, 60), phone = s(d.phone, 20), email = s(d.email, 80);
  if (!name || !email || phone.replace(/\D/g, '').length < 10 || !d.consent) return out({ ok: false, error: 'missing fields' });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return out({ ok: false, error: 'bad email' });
  var cache = CacheService.getScriptCache(), key = 'ad:' + email.toLowerCase();
  if (cache.get(key)) return out({ ok: true, dup: true });          // same person within 10 minutes: don't create twice
  cache.put(key, '1', 600);

  var parts = name.split(/\s+/), first = parts.shift(), last = parts.join(' ');
  var note = [
    'Area Director application (website)',
    'Buyer sales, last 12 months (units): ' + s(d.units, 20),
    'Sales volume, last 12 months: ' + s(d.volume, 30),
    'States: ' + s(d.states, 120),
    d.message ? 'Message: ' + s(d.message, 1000) : '',
    '',
    'TCPA consent: checked at ' + s(d.ts, 40) + ' on ' + s(d.page, 200),
    'Consent text: ' + s(d.consentText, 1200)
  ].filter(function (x) { return x !== ''; }).join('\n');

  var ok = false, leadId = '', detail = '';
  try {
    var res = UrlFetchApp.fetch('https://api.lofty.com/v1.0/leads', {
      method: 'post',
      contentType: 'application/json',
      headers: { Authorization: 'token ' + props.getProperty('LOFTY_API_KEY'), 'X-Error-Status': 'true' },
      payload: JSON.stringify({
        firstName: first, lastName: last, emails: [email], phones: [phone],
        source: SOURCE, tags: [TAG], content: note, isPin: true
      }),
      muteHttpExceptions: true
    });
    detail = res.getResponseCode() + ' ' + res.getContentText().slice(0, 300);
    var m = res.getContentText().match(/"leadId"\s*:\s*(\d+)/);       // read as text: the id is too long for a JS number
    ok = res.getResponseCode() < 300 && !!m;
    if (m) leadId = m[1];
  } catch (err) { detail = String(err); }

  // backup copy so an application is never lost, even if Lofty is down
  var to = props.getProperty('NOTIFY_EMAIL');
  if (to) {
    MailApp.sendEmail(to,
      (ok ? 'New AD application: ' : 'AD application (Lofty push FAILED): ') + name,
      'Name: ' + name + '\nPhone: ' + phone + '\nEmail: ' + email + '\n\n' + note +
      '\n\nLofty: ' + (ok ? 'lead ' + leadId + ' created, tagged "' + TAG + '"' : 'NOT created - ' + detail));
  }
  return out({ ok: ok || !!to });
}

function out(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

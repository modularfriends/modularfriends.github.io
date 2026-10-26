// Modular Friends newsletter progressive embed.
// GitHub Pages cannot store email submissions itself; use the official hosted Brevo form.
(function () {
  'use strict';
  const cfg = window.MF_NEWSLETTER || {};
  const formUrl = typeof cfg.formUrl === 'string' ? cfg.formUrl.trim() : '';
  if (!formUrl) return; // Never collect addresses without a working backend.
  let target;
  try {
    const parsed = new URL(formUrl);
    const allowed = parsed.protocol === 'https:' && (
      parsed.hostname === 'sibforms.com' || parsed.hostname.endsWith('.sibforms.com') ||
      parsed.hostname === 'brevo.com' || parsed.hostname.endsWith('.brevo.com') ||
      parsed.hostname === 'sendinblue.com' || parsed.hostname.endsWith('.sendinblue.com')
    );
    if (!allowed || !parsed.pathname || parsed.pathname === '/') return;
    target = parsed.href;
  } catch(e) { return; }
  document.querySelectorAll('[data-mf-newsletter-form]').forEach(function(host) {
    host.innerHTML = '';
    host.classList.add('is-connected');
    const help = document.createElement('p');
    help.className = 'mf-newsletter-form-note';
    help.textContent = 'Enter your email below, then confirm your subscription via the email you receive.';
    host.appendChild(help);
    const backup = document.createElement('a');
    backup.className = 'mf-newsletter-external';
    backup.href = target;
    backup.textContent = 'OPEN SECURE SUBSCRIPTION FORM ↗';
    backup.target = '_blank';
    backup.rel = 'noopener noreferrer';
    backup.style.cssText = 'display:block;margin:12px 0 16px;text-align:center;padding:15px 10px;border:1px solid currentColor;color:inherit;font-size:11px;font-weight:700;letter-spacing:.04em;text-decoration:none';
    const frame = document.createElement('iframe');
    frame.className = 'mf-newsletter-iframe';
    frame.src = target;
    frame.title = 'Subscribe to Modular Friends email updates';
    frame.loading = 'lazy';
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    frame.setAttribute('scrolling', 'auto');
    host.appendChild(frame);
    host.appendChild(backup);
  });
})();

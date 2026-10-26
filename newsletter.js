// Modular Friends newsletter — embeds a verified provider signup form when configured.
// Without a validated form URL, the preview remains disabled so no email is falsely accepted.
(function(){
  'use strict';
  const cfg = window.MF_NEWSLETTER || {};
  const raw = cfg.formUrl;
  const host = document.querySelector('[data-mf-newsletter-form]');
  if (!raw || !host) return;
  let parsed;
  try { parsed = new URL(raw); } catch (_) { return; }
  const hostname = parsed.hostname.toLowerCase();
  if (parsed.protocol !== 'https:' || parsed.username || parsed.password ||
      !(hostname === 'sibforms.com' || hostname.endsWith('.sibforms.com')) ||
      !parsed.pathname.startsWith('/serve/')) return;
  const frame = document.createElement('iframe');
  frame.className = 'mf-newsletter-iframe';
  frame.title = 'Modular Friends email newsletter subscription';
  frame.loading = 'lazy';
  frame.referrerPolicy = 'strict-origin-when-cross-origin';
  frame.src = parsed.href;
  host.replaceChildren(frame);
  host.classList.add('is-connected');
})();

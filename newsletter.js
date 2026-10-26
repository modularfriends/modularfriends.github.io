// Luma remains active unless a tested EmailOctopus embed is configured.
// This file is intentionally safe for GitHub Pages (static hosting; no secret keys).
(function () {
  'use strict';
  const cfg = window.MF_NEWSLETTER || {};
  const rawCalendar = cfg.calendarUrl;
  if (rawCalendar) {
    try {
      const calendar = new URL(rawCalendar);
      if (calendar.protocol === 'https:' && calendar.hostname === 'luma.com' &&
          calendar.pathname !== '/' && !calendar.username && !calendar.password) {
        document.querySelectorAll('[data-mf-calendar-link]').forEach(a => { a.href = calendar.href; });
      }
    } catch (_) { /* Retain the original Luma link. */ }
  }

  const provider = cfg.emailOctopus;
  const host = document.querySelector('[data-mf-newsletter-form]');
  if (!provider || provider.enabled !== true || !host) return;

  let scriptUrl;
  try { scriptUrl = new URL(provider.formScriptUrl); } catch (_) { return; }
  const id = String(provider.formId || '');
  const match = /^\/form\/([A-Za-z0-9-]{8,128})\.js$/.exec(scriptUrl.pathname);
  if (scriptUrl.protocol !== 'https:' ||
      !/^eocampaign[0-9]+\.com$/.test(scriptUrl.hostname) ||
      scriptUrl.username || scriptUrl.password ||
      !match || match[1] !== id || scriptUrl.search || scriptUrl.hash) return;

  // Stage the provider script without removing the working Luma link.
  // Switch only if its script really renders a form.
  const fallback = document.createElement('div');
  fallback.className = 'mf-luma-fallback';
  while (host.firstChild) fallback.appendChild(host.firstChild);
  host.appendChild(fallback);

  const slot = document.createElement('div');
  slot.className = 'mf-emailoctopus-form';
  slot.hidden = true;
  host.appendChild(slot);

  const script = document.createElement('script');
  script.async = true;
  script.src = scriptUrl.href;
  script.dataset.form = id;

  let finished = false;
  let watcher;
  const reveal = () => {
    if (finished) return;
    if (!slot.querySelector('form, iframe, input[type="email"], input[name="email"]')) return;
    finished = true;
    if (watcher) watcher.disconnect();
    slot.hidden = false;
    fallback.hidden = true;
    host.classList.add('is-connected');
  };
  watcher = new MutationObserver(reveal);
  watcher.observe(slot, {childList: true, subtree: true});
  script.addEventListener('load', reveal);
  script.addEventListener('error', () => {
    if (watcher) watcher.disconnect();
    slot.remove();
    fallback.hidden = false;
  });
  slot.appendChild(script);
  window.setTimeout(() => { reveal(); if (watcher) watcher.disconnect(); }, 12000);
})();

(() => {
  'use strict';
  const slots = [...document.querySelectorAll('[data-mf-radio]')];
  if (!slots.length) return;
  const base = new URL('.', document.currentScript.src);
  const audio = new Audio();
  audio.preload = 'none';
  audio.setAttribute('playsinline', '');
  audio.id = 'mf-radio-audio';
  document.body.append(audio);
  let tracks = [], queue = [], current = null, last = null;
  let wanted = false, loading = false, generation = 0, timer;
  const failed = new Set();
  let status = 'Loading track list…';
  slots.forEach(slot => {
    slot.classList.add('mf-radio');
    slot.innerHTML = `<img class="mf-radio-logo" src="${new URL('../assets/modular-friends-logo-black.png', base)}" alt="Modular Friends" width="64" height="64"><div class="mf-radio-copy"><h3>MODULAR FRIENDS RADIO</h3><p class="mf-radio-title">Live recordings &amp; improvisations</p><p class="mf-radio-artist"></p><p class="mf-radio-status" role="status" aria-live="polite"></p></div><button class="mf-radio-toggle" type="button" disabled>PLAY</button>`;
    slot.querySelector('button').addEventListener('click', toggle);
  });
  function render() {
    slots.forEach(slot => {
      slot.querySelector('.mf-radio-title').textContent = current?.title || 'Live recordings & improvisations';
      slot.querySelector('.mf-radio-artist').textContent = current?.artist || '';
      slot.querySelector('.mf-radio-status').textContent = status;
      const button = slot.querySelector('button');
      button.disabled = !tracks.length;
      button.textContent = wanted ? 'PAUSE' : 'PLAY';
      button.setAttribute('aria-label', wanted ? 'Pause Modular Friends Radio' : 'Play Modular Friends Radio');
      button.setAttribute('aria-pressed', String(wanted));
    });
  }
  function refill() {
    queue = tracks.filter(t => !failed.has(t.id));
    for (let i = queue.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [queue[i], queue[j]] = [queue[j], queue[i]];
    }
    if (queue.length > 1 && queue[0].id === last) [queue[0], queue[1]] = [queue[1], queue[0]];
  }
  function watch(token) {
    clearTimeout(timer);
    timer = setTimeout(() => { if (wanted && token === generation) skip(token); }, 25000);
  }
  function stop(message) {
    wanted = false; loading = false; generation++; clearTimeout(timer); audio.pause(); status = message; render();
  }
  function skip(token) {
    if (token !== generation || !wanted || !current || failed.has(current.id)) return;
    failed.add(current.id);
    queue = queue.filter(t => !failed.has(t.id));
    next();
  }
  function next() {
    clearTimeout(timer);
    if (!queue.length) refill();
    if (!queue.length) { stop('Tracks are temporarily unavailable. Press Play to retry.'); return; }
    current = queue.shift(); last = current.id;
    generation++;
    audio.src = new URL(current.src, base).href;
    start();
  }
  function start() {
    const token = generation;
    loading = true; status = 'Loading audio…'; render(); watch(token);
    audio.play().then(() => {
      if (token !== generation) return;
      if (!wanted) { audio.pause(); return; }
      loading = false; status = 'Playing · shuffled without repeats'; clearTimeout(timer); render();
    }).catch(error => {
      if (token !== generation || !wanted) return;
      if (error.name === 'NotAllowedError') stop('Press Play to begin listening.');
      else if (error.name !== 'AbortError') skip(token);
    });
  }
  function toggle() {
    if (wanted) { stop('Paused'); return; }
    wanted = true;
    if (failed.size >= tracks.length) { failed.clear(); queue = []; current = null; }
    if (!current || failed.has(current.id) || audio.ended) next(); else start();
  }
  audio.addEventListener('ended', () => { if (wanted) next(); });
  audio.addEventListener('error', () => { if (audio.error) skip(generation); });
  audio.addEventListener('waiting', () => { if (wanted) { status = 'Buffering…'; render(); watch(generation); } });
  audio.addEventListener('playing', () => { if (wanted) { loading = false; clearTimeout(timer); status = 'Playing · shuffled without repeats'; render(); } });
  audio.addEventListener('timeupdate', () => { if (wanted && !audio.paused && audio.readyState >= 3) clearTimeout(timer); });
  fetch(new URL('tracks.json', base), {cache: 'no-cache'}).then(r => {
    if (!r.ok) throw new Error('playlist'); return r.json();
  }).then(data => {
    const seen = new Set();
    tracks = (data.tracks || []).filter(t => {
      if (!t.id || !t.src || !t.title || !t.artist || seen.has(t.id)) return false;
      const url = new URL(t.src, base);
      if (!['https:', 'http:'].includes(url.protocol)) return false;
      seen.add(t.id); return true;
    });
    status = tracks.length ? `${tracks.length} recordings · press Play to listen` : 'Radio recordings will be available soon.';
    render();
  }).catch(() => { status = 'Track list unavailable. Please reload to retry.'; render(); });
})();

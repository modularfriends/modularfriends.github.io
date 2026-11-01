// Keep only current/future event cards. Dates are always evaluated in Tbilisi.
(() => {
  const list = document.getElementById('upcomingEventList');
  const empty = document.getElementById('upcomingEmpty');
  if (!list) return;
  const dateKey = value => {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return null;
    const parts = new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Asia/Tbilisi', year: 'numeric', month: '2-digit', day: '2-digit'
    }).formatToParts(date);
    const part = type => parts.find(p => p.type === type).value;
    return `${part('year')}-${part('month')}-${part('day')}`;
  };
  function refreshUpcoming() {
    const today = dateKey(Date.now());
    const cards = [...list.querySelectorAll('.upcoming-event-layout')];
    cards.forEach(card => {
      const end = card.dataset.eventEnd || card.querySelector('time[datetime]')?.dateTime;
      const eventDay = end && dateKey(end);
      card.hidden = Boolean(eventDay && eventDay < today);
    });
    const visible = cards.some(card => !card.hidden);
    list.hidden = !visible;
    if (empty) empty.hidden = visible;
  }
  refreshUpcoming();
  setInterval(refreshUpcoming, 60000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refreshUpcoming(); });
})();

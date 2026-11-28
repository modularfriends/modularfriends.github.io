// Hide expired listings at their exact confirmed end time; persistent archiving
// is performed only after official completion verification by the editor task.
(() => {
  function refresh() {
    document.querySelectorAll('[data-event-end]').forEach(card => {
      const end=Date.parse(card.dataset.eventEnd);
      card.hidden=Number.isFinite(end) && end<=Date.now();
    });
    const list=document.getElementById('upcomingEventList');
    if(list){const visible=[...list.querySelectorAll('[data-event-end]')].some(x=>!x.hidden);list.hidden=!visible;const empty=document.getElementById('upcomingEmpty');if(empty)empty.hidden=visible;}
    const tickets=document.getElementById('tickets');
    if(tickets){const empty=tickets.querySelector('[data-ticket-empty]');if(empty)empty.hidden=[...tickets.querySelectorAll('[data-event-end]')].some(x=>!x.hidden);}
  }
  refresh();setInterval(refresh,60000);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh();});
})();

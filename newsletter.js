// Public Luma calendar links work without JavaScript; configuration can update them.
(function(){'use strict';const raw=(window.MF_NEWSLETTER||{}).calendarUrl;if(!raw)return;try{const u=new URL(raw);if(u.protocol!=='https:'||u.hostname!=='luma.com'||u.username||u.password||u.pathname==='/')return;document.querySelectorAll('[data-mf-calendar-link]').forEach(a=>{a.href=u.href;});}catch(e){}})();

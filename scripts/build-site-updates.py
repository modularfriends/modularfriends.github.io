"""Render verified announcements. Never infer completion or artist credits."""
import json,re
from datetime import datetime,timezone
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
e=lambda value: escape(str(value or ''),quote=True)
def load(name): return json.loads((ROOT/name).read_text())
def save(name,data): (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def links(people): return ' × '.join(f'<a href="{e(p["url"])}">{e(p["name"])}</a>' for p in people)
def embed(v):
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}',v['id']): raise ValueError('Invalid YouTube ID')
    return f'<div class="mf-video-frame"><iframe src="https://www.youtube-nocookie.com/embed/{v["id"]}?rel=0&amp;playsinline=1" title="{e(v["title"])} | Modular Friends" width="560" height="315" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>'
def replace(page,key,html):
    pattern=rf'<!-- MF:{key}:START -->.*?<!-- MF:{key}:END -->'
    page,count=re.subn(pattern,lambda _:f'<!-- MF:{key}:START -->{html}<!-- MF:{key}:END -->',page,flags=re.S)
    if count!=1: raise ValueError(f'Expected one {key} region, found {count}')
    return page

def build(now=None):
    now=now or datetime.now(timezone.utc)
    data=load('content/site-updates.json'); archive=load('content/event-archive.json')
    changed=False
    for item in data['events']:
        if item['status']=='archived':
            if not item.get('completion_confirmed') or datetime.fromisoformat(item['ends_at'])>now:
                raise ValueError('Archiving requires confirmed completion and an elapsed end time')
            sources=[{'label':label,'url':item[key]} for label,key in [('Event details','page'),('Luma','luma'),('Resident Advisor','ra')] if item.get(key)]
            record=dict(id=item['id'],title=item['title'],date=item['date'],date_label=item['date_label'],venue=item['venue'],artists=item.get('artists',''),visuals=item.get('visuals',''),description=item['description']+' '+item['support'],image=item['image'],image_kind='Original event poster',sources=sources,verification_notes='Completion confirmed from official event sources.',media_folder=item.get('media_folder',''))
            existing=next((i for i,x in enumerate(archive['events']) if x['id']==item['id']),None)
            if existing is None: archive['events'].append(record);changed=True
            # Preserve all subsequently supplied historical media/credits.
    if changed:
        archive['events'].sort(key=lambda x:x.get('date') or '',reverse=True);archive['updated']=now.date().isoformat();save('content/event-archive.json',archive)
    upcoming=sorted((x for x in data['events'] if x['status']=='upcoming' and datetime.fromisoformat(x['ends_at'])>now),key=lambda x:x['starts_at'])
    cards=[];tickets=[]
    for item in upcoming:
        img=f'<img src="{e(item["image"])}" alt="{e(item["title"])} — original event poster" width="1080" height="1350" loading="lazy"/>'
        copy=f'<h3>{e(item["title"])}</h3><p><time datetime="{e(item["starts_at"])}">{e(item["date_label"])}</time></p><p>{e(item["venue"])}</p><p>{e(item["description"])}</p>'
        actions=f'<a href="{e(item["luma"])}">FREE REGISTRATION ↗</a><a href="{e(item["page"])}">EVENT DETAILS ↗</a>'
        cards.append(f'<article class="upcoming-event-layout" data-event-end="{e(item["ends_at"])}"><figure class="random-fridays-poster"><a href="{e(item["page"])}">{img}</a></figure><div class="upcoming-card"><small>COMMUNITY &amp; JAM SESSION</small>{copy}<p>{e(item["support"])}</p><div class="upcoming-links">{actions}</div></div></article>')
        tickets.append(f'<div class="mf-ticket-event" data-event-end="{e(item["ends_at"])}"><a class="mf-ticket-poster" href="{e(item["page"])}">{img}</a><div>{copy}<p><strong>FREE ENTRY / VOLUNTARY DONATIONS</strong></p><p>All donations support Modular Friends.</p><a class="button" href="{e(item["luma"])}">FREE REGISTRATION ↗</a></div></div>')
    v=data['current_video']; seen=set(); history=[]
    for video in [v]+data['videos']:
        if video['id'] not in seen: history.append(video);seen.add(video['id'])
    if history!=data['videos']: data['videos']=history;save('content/site-updates.json',data)
    watch=f'https://www.youtube.com/watch?v={v["id"]}'
    video_copy=f'<h3 id="latest-release-title">{e(v["title"])}</h3><p>{e(v["description"])}</p><p class="upcoming-release-credits">VISUALS — {links(v["visuals"])}<br/>SOUND — {links(v["sound"])}</p><a class="upcoming-release-watch" href="{watch}" target="_blank" rel="noopener noreferrer">WATCH ON YOUTUBE ↗</a>'
    empty=f'<div id="upcomingEmpty" class="mf-event-placeholder"{ " hidden" if cards else ""}><h3>Next announcement coming soon.</h3><p>Follow our calendar for the next gathering.</p></div>'
    section=f'<section class="upcoming" id="upcoming"><div class="container"><div class="section-tag"><span>003 / UPCOMING</span><span>EVENTS &amp; LATEST NEWS</span></div><div class="upcoming-intro"><h2>UPCOMING.</h2><p>New videos, community news and upcoming gatherings — the latest from Modular Friends.</p></div><div class="mf-news-grid"><div class="mf-event-slot"><div id="upcomingEventList" aria-live="polite">{"".join(cards)}</div>{empty}</div><article class="upcoming-release" aria-labelledby="latest-release-title">{embed(v)}<div class="upcoming-release-copy"><p class="upcoming-release-label">NEW VIDEO / OUT NOW</p>{video_copy}</div></article></div><div class="upcoming-empty upcoming-calendar"><span aria-hidden="true" class="status-dot"></span><div><h3>STAY IN THE LOOP.</h3><p>Follow our official calendar for live performances, community gatherings, workshops and new announcements.</p></div><a href="{e(data["calendar"])}" target="_blank" rel="noopener noreferrer">FOLLOW THE CALENDAR ↗</a></div></div></section>'
    page=replace((ROOT/'index.html').read_text(),'UPCOMING',section);(ROOT/'index.html').write_text(page)
    ticket=f'<article class="panel dark" id="tickets"><small>LIVE / TICKETS</small><h3>TICKETS.</h3>{"".join(tickets)}<div data-ticket-empty{ " hidden" if tickets else ""}><p>No event tickets are currently on sale.</p><p>Follow our calendar for upcoming live performances and new announcements.</p><a class="button" href="{e(data["calendar"])}" data-mf-calendar-link>FOLLOW THE CALENDAR ↗</a></div></article>'
    videos=''.join(f'<li><a href="https://www.youtube.com/watch?v={e(x["id"])}">{e(x["title"])}</a></li>' for x in history if x['id']!=v['id'])
    latest=f'<figure class="mf-latest-video" id="latest-video"><figcaption>LATEST RELEASE</figcaption>{embed(v)}<h4>{e(v["title"])}</h4><p>Visuals: {links(v["visuals"])}<br/>Sound: {links(v["sound"])}</p><a class="mf-youtube-link" href="{watch}">WATCH THE FULL VIDEO ON YOUTUBE ↗</a></figure><ul class="mf-previous-videos">{videos}</ul>'
    page=replace((ROOT/'shop.html').read_text(),'TICKETS',ticket);page=replace(page,'VIDEO',latest);(ROOT/'shop.html').write_text(page)
if __name__=='__main__': build()

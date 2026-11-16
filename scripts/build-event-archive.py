"""Rebuild only the two-column live archive from verified event records."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'content/event-archive.json').read_text())
page = (ROOT / 'index.html').read_text()
e = lambda text: escape(str(text or ''), quote=True)

def body(item):
    artists = ''.join(f'<li>{e(name.strip())}</li>' for name in item['artists'].split(';') if name.strip())
    visuals = f'<p class="archive-visuals">VISUALS — {e(item["visuals"])}</p>' if item.get('visuals') else ''
    sources = ''.join(f'<a href="{e(s["url"])}">{e(s["label"])} ↗</a>' for s in item['sources'])
    return f'<p class="archive-description">{e(item["description"])}</p><ul class="archive-lineup" aria-label="Artists">{artists}</ul>{visuals}<div class="archive-sources">{sources}</div>'

def poster(item, latest=False):
    # Original proportions are retained. Never crop lettering off posters.
    img = f'<img src="{e(item["image"])}" alt="{e(item["title"])} — {e(item["image_kind"])}" loading="lazy" decoding="async"/>'
    if not latest:
        return f'<span class="archive-thumb">{img}</span>'
    return f'<figure class="archive-poster"><button type="button" class="gallery-open" aria-label="Enlarge poster: {e(item["title"])}" data-gallery-src="{e(item["image"])}" data-gallery-alt="{e(item["title"])} event poster or documentation">{img}</button><figcaption><span>{e(item["title"])} / ARCHIVE</span></figcaption></figure>'

def card(item):
    return f'<details class="edition-card archive-entry" id="archive-{e(item["id"])}"><summary>{poster(item)}<span class="archive-card-copy"><span class="edition-card-date">{e(item["date_label"])}</span><strong>{e(item["title"])}</strong><span class="archive-venue">{e(item["venue"])}</span><span class="edition-card-open">VIEW ACTIVITY +</span></span></summary><div class="edition-card-body">{body(item)}<a class="archive-full-poster" href="{e(item["image"])}">VIEW FULL POSTER / PHOTO ↗</a></div></details>'

def panel(items, title, id, gallery=''):
    latest, *earlier = items
    return f'''<div class="archive-panel" aria-labelledby="{id}-title">
    <div class="archive-panel-heading"><h2 id="{id}-title">{title}.</h2><span>{len(items):02} / LIVE ARCHIVE</span></div>
    <article class="archive-feature" id="archive-{e(latest['id'])}">{poster(latest,True)}<div class="archive-feature-copy"><p class="edition-card-date">{e(latest['date_label'])}</p><h3>{e(latest['title'])}</h3><p class="archive-venue">{e(latest['venue'])}</p>{body(latest)}</div></article>
    <details class="editions-archive" id="{id}"><summary><span class="editions-show-more">SHOW MORE {title} +</span><span class="editions-show-less">SHOW FEWER {title} −</span><span class="editions-archive-count">{len(earlier)} EARLIER</span></summary><div class="edition-archive-content"><div class="archive-entry-list">{''.join(card(x) for x in earlier)}</div>{gallery}</div></details></div>'''

start = page.index('<section class="chap container editions-compact" id="events">')
end = page.index('</section>', start) + len('</section>')
old = page[start:end]
# Preserve the existing photo documentation and YouTube entry point unchanged.
gallery_match = re.search(r'(<div class="edition-documentation" id="gallery">.*?</div><p class="editorial-note">.*?</p></div>)', old, re.S)
gallery = gallery_match.group(1) if gallery_match else ''
youtube_match = re.search(r'(<div class="mf-youtube-callout".*)</section>', old, re.S)
youtube = youtube_match.group(1) if youtube_match else ''
if not gallery or not youtube:
    raise ValueError('Existing gallery / video entry point was not found; refusing to remove it.')
section = '<section class="chap container editions-compact" id="events"><div class="section-tag"><span>004 / EDITIONS &amp; EVENTS</span><span>NO TWO SETS ALIKE / THE LIVE ARCHIVE</span></div><div class="archive-intro"><p>Live sessions, shared spaces and unrepeatable moments.</p><p>Numbered editions and other gatherings — in Georgia and beyond.</p></div><div class="archive-columns">' + panel(data['editions'],'EDITIONS','editionArchive',gallery) + panel(data['events'],'EVENTS','eventArchive') + '</div>' + youtube + '</section>'
page = page[:start] + section + page[end:]
link = '<link rel="stylesheet" href="assets/event-archive.css?v=20261116"/>'
if link not in page:
    page = page.replace('</head>', link + '</head>')
(ROOT / 'index.html').write_text(page)
print(f"Built {len(data['editions'])} editions and {len(data['events'])} events")

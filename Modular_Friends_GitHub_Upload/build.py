#!/usr/bin/env python3
"""Generate an indexable HTML website and a text-selectable PDF from ONE JSON file."""
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse
from xml.sax.saxutils import escape as xescape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
OUT.mkdir(parents=True, exist_ok=True)
content = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
site_url = os.environ.get("SITE_URL", "").strip().rstrip("/") or content.get("site_url", "").strip().rstrip("/")
if site_url and not re.match(r"^https://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+$", site_url):
    raise ValueError("SITE_URL must be a full https:// URL")
if site_url and urlparse(site_url).query:
    raise ValueError("SITE_URL must not contain query parameters")
E = lambda value: html.escape(str(value), quote=True)
name=content["name"]
insta=content["instagram_url"]
insta_text=content["instagram_handle"]
if urlparse(insta).netloc != "www.instagram.com":
    raise ValueError("Instagram source must be instagram.com")

# Static HTML markup keeps the public text accessible to search crawlers.
format_html = "\n".join(
    '<article class="format"><div class="symbol">0' + str(i) + '</div><h3>' + E(f["title"]) + '</h3><p>' + E(f["description"]) + '</p></article>'
    for i, f in enumerate(content["formats"], 1)
)
if content.get("events"):
    event_html = '<p class="archive-status">' + E(content["archive_intro"]) + '</p><div class="events">' + '\n'.join(
        '<article class="event"><div class="event-date">' + E(e.get("date", "")) + '</div><div><h3>' + E(e["title"]) + '</h3><p>' + E(e.get("description", "")) + '</p>' +
        ('<p class="event-credit"><strong>Performers:</strong> ' + E(e['artists']) + '</p>' if e.get('artists') else '') +
        ('<p class="event-credit"><strong>Visual artists:</strong> ' + E(e['visual_artists']) + '</p>' if e.get('visual_artists') else '') +
        ('<a class="source-link" href="' + E(e["source_url"]) + '" target="_blank" rel="noopener noreferrer">Source: ' + E(e.get("source_label","Reference")) + ' ↗</a>' if e.get("source_url") else '') + '</div></article>'
        for e in content["events"] if e.get("confirmed", False)
    ) + '</div>'
else:
    event_html = '<p class="archive-status">' + E(content["archive_intro"]) + '</p>'

# Separate editorial coverage from event listings; links are factual references, not endorsements.
references_html = "\n".join(
    '<article class="reference"><div class="reference-date">' + E(ref["date"]) + ' / ' + E(ref["kind"]) + '</div>' +
    '<h3><a href="' + E(ref["url"]) + '" target="_blank" rel="noopener noreferrer">' + E(ref["title"]) + ' ↗</a></h3>' +
    '<p>' + E(ref["description"]) + '</p></article>'
    for ref in content.get("references", [])
)

canonical = f'<link rel="canonical" href="{E(site_url)}/">' if site_url else ''
ogurl = f'<meta property="og:url" content="{E(site_url)}/">' if site_url else ''
ld = {"@context":"https://schema.org","@type":"Organization","name":name,"description":content["short_description"],"sameAs":[insta],"areaServed":{"@type":"Place","name":content["location"]}}
if site_url: ld["url"] = site_url + "/"
ld_json = json.dumps(ld, ensure_ascii=False).replace("<", "\\u003c")

website = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f9f9f6">
  <title>'''+E(name)+''' — Modular Synthesis &amp; Live Electronic Music | Tbilisi</title>
  <meta name="description" content="'''+E(content["short_description"])+'''">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Modular Friends — More than sound.">
  <meta property="og:description" content="'''+E(content["short_description"])+'''">
  '''+canonical+ogurl+'''
  <script type="application/ld+json">'''+ld_json+'''</script>
  <style>
    :root{color-scheme:light;--bg:#f9f9f6;--text:#181915;--muted:#646962;--line:#d8dbd4;--accent:#495a48}
    *{box-sizing:border-box} html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:Arial,Helvetica,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}
    a{color:inherit;text-decoration:none}a:focus-visible{outline:2px solid var(--accent);outline-offset:5px}
    .wrap{max-width:1360px;margin:auto;padding:0 clamp(22px,5vw,74px)}
    header{border-bottom:1px solid var(--line)} header .wrap{min-height:78px;display:flex;align-items:center;justify-content:space-between;gap:20px}
    .wordmark{font-size:14px;font-weight:700;letter-spacing:.24em;white-space:nowrap}
    nav{display:flex;flex-wrap:wrap;gap:clamp(13px,3vw,38px)}nav a{font-size:12px;letter-spacing:.10em;text-transform:uppercase}
    nav a:hover,.foot-links a:hover,.text-link:hover{text-decoration:underline;text-underline-offset:5px}
    .hero{min-height:calc(86svh - 80px);display:flex;align-items:end;padding:80px 0 75px}
    .eyebrow,.kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
    .hero h1{font-size:clamp(74px,13vw,190px);line-height:.84;letter-spacing:-.095em;font-weight:500;max-width:1100px;margin:34px 0 45px}
    .hero h1 span{display:block}.hero-bottom{display:flex;justify-content:space-between;align-items:end;gap:34px}
    .hero-intro{font-size:clamp(16px,1.9vw,23px);line-height:1.5;max-width:680px;letter-spacing:-.02em;margin:0}
    .cta{border:1px solid var(--text);padding:13px 18px;font-size:12px;white-space:nowrap;letter-spacing:.1em;text-transform:uppercase;display:inline-block}
    .cta:hover{background:var(--text);color:var(--bg)}
    section.content{border-top:1px solid var(--line);padding:90px 0 110px;scroll-margin-top:20px}
    .section-layout{display:grid;grid-template-columns:25% 1fr;gap:36px}
    h2{font-size:clamp(30px,4vw,56px);font-weight:500;line-height:1.05;letter-spacing:-.055em;margin:0 0 30px}
    .large-copy{font-size:clamp(22px,2.6vw,38px);line-height:1.34;letter-spacing:-.042em;max-width:920px;margin:0}
    .formats{display:grid;grid-template-columns:repeat(3,1fr);gap:34px}.format{border-top:1px solid var(--line);padding-top:15px}
    .symbol{font-family:monospace;font-size:12px;color:var(--muted);margin-bottom:80px}.format h3{font-size:21px;font-weight:500;letter-spacing:-.04em}
    .format p,.archive-status,.event p{max-width:340px;font-size:15px;color:var(--muted);line-height:1.7}
    .archive-status{max-width:650px;font-size:18px;margin-bottom:35px}.source-link{font-size:12px;color:var(--accent);text-decoration:underline;text-underline-offset:4px}.events{border-top:1px solid var(--line)}.event{display:grid;grid-template-columns:140px 1fr;padding:27px 0;border-bottom:1px solid var(--line);gap:25px}.event-date{color:var(--muted)}.event h3{margin:0;font-weight:500;font-size:23px}.event .event-credit{max-width:830px;font-size:13px;line-height:1.7;margin:14px 0}.event .event-credit strong{color:var(--text);font-weight:500}
    .press-row{display:flex;gap:20px;align-items:center;flex-wrap:wrap}.text-link{font-size:18px;text-decoration:underline;text-underline-offset:5px}
    footer{border-top:1px solid var(--line);padding:32px 0 48px}.footer-inner{display:flex;justify-content:space-between;align-items:center;gap:30px;flex-wrap:wrap}
    .references{display:grid;gap:30px}.reference{padding:24px 0;border-bottom:1px solid var(--line)}.reference h3{font-size:clamp(20px,2vw,29px);font-weight:500;margin:8px 0 10px}.reference h3 a{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:5px}.reference p{color:var(--muted);font-size:14px;max-width:690px;margin:0}.reference-date{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}.foot-links{display:flex;gap:25px;flex-wrap:wrap;font-size:13px}.small{color:var(--muted);font-size:12px;letter-spacing:.08em}
    @media(max-width:760px){header .wrap{align-items:flex-start;flex-direction:column;padding-top:23px;padding-bottom:23px;gap:16px}nav{gap:20px}.hero{min-height:70svh;padding:65px 0}.hero h1{font-size:clamp(70px,16vw,110px);margin:40px 0}.hero-bottom{align-items:flex-start;flex-direction:column}.section-layout{grid-template-columns:1fr;gap:30px}section.content{padding:60px 0 70px}.formats{grid-template-columns:1fr;gap:35px}.symbol{margin-bottom:25px}.event{grid-template-columns:1fr;gap:5px}}
    @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  </style>
</head>
<body>
  <header><div class="wrap"><a class="wordmark" href="#top" aria-label="Modular Friends home">MODULAR FRIENDS</a><nav aria-label="Main navigation"><a href="#about">About</a><a href="#formats">Programme</a><a href="#archive">Archive</a><a href="#sources">In the press</a><a href="#press">Press kit</a></nav></div></header>
  <main id="top">
    <div class="hero wrap"><div><div class="eyebrow">'''+E(content["location"])+''' / Independent community &amp; event series</div><h1><span>More than</span><span>sound.</span></h1><div class="hero-bottom"><p class="hero-intro">'''+E(content["short_description"])+'''</p><a class="cta" href="'''+E(insta)+'''" target="_blank" rel="noopener noreferrer">Instagram ↗</a></div></div></div>
    <section class="content" id="about"><div class="wrap section-layout"><div class="kicker">01 / About</div><div><h2>A space to connect.</h2><p class="large-copy">'''+E(content["about"])+'''</p></div></div></section>
    <section class="content" id="formats"><div class="wrap section-layout"><div class="kicker">02 / Programme</div><div><h2>How we gather.</h2><div class="formats">'''+format_html+'''</div></div></div></section>
    <section class="content" id="archive"><div class="wrap section-layout"><div class="kicker">03 / Archive</div><div><h2>Every edition matters.</h2>'''+event_html+'''</div></div></section>
    <section class="content" id="sources"><div class="wrap section-layout"><div class="kicker">04 / References</div><div><h2>Coverage &amp; listings.</h2><p class="archive-status">Independent coverage and public listings documenting Modular Friends.</p><div class="references">'''+references_html+'''</div></div></div></section>
    <section class="content" id="press"><div class="wrap section-layout"><div class="kicker">05 / Press</div><div><h2>Project profile.</h2><div class="press-row"><a class="text-link" href="Modular_Friends_Press_Kit.pdf" target="_blank" rel="noopener noreferrer">Open the PDF profile ↗</a><a class="text-link" href="'''+E(insta)+'''" target="_blank" rel="noopener noreferrer">'''+E(insta_text)+''' ↗</a></div></div></div></section>
  </main>
  <footer><div class="wrap footer-inner"><div class="wordmark">MODULAR FRIENDS</div><div class="foot-links"><a href="'''+E(insta)+'''" rel="noopener noreferrer">Instagram</a><a href="#sources">Coverage</a><a href="Modular_Friends_Press_Kit.pdf">PDF profile</a></div><div class="small">TBILISI, GEORGIA</div></div></footer>
</body>
</html>'''
(OUT / "index.html").write_text(website, encoding="utf-8")
(OUT / ".nojekyll").write_text("",encoding="utf-8")
if site_url:
    sitemap='<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+xescape(site_url+'/')+'</loc><lastmod>'+content["updated"]+'</lastmod></url></urlset>\n'
    (OUT/"sitemap.xml").write_text(sitemap, encoding="utf-8")
    robots=f'User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n'
else:
    for fp in (OUT/"sitemap.xml", OUT/"robots.txt"):
        if fp.exists(): fp.unlink()
    robots='User-agent: *\nAllow: /\n'
(OUT/"robots.txt").write_text(robots, encoding="utf-8")

# Vector PDF with live selectable text, functional web link, and document metadata.
font_regular="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not Path(font_regular).exists(): raise FileNotFoundError(font_regular)
pdfmetrics.registerFont(TTFont("MF",font_regular))
pdfmetrics.registerFont(TTFont("MF-Bold",font_bold))
W,H=A4
path=OUT/"Modular_Friends_Press_Kit.pdf"
c=canvas.Canvas(str(path),pagesize=A4,pageCompression=1)
c.setTitle("Modular Friends - Project Profile")
c.setSubject(content["short_description"])
c.setAuthor("Modular Friends")
c.setKeywords("Modular Friends, Tbilisi, modular synthesis, experimental music, live electronic music")
dark=HexColor('#1b1d1a'); muted=HexColor('#666c64'); line=HexColor('#d7dbd4')
def txt(x,y,t,sz=12,bold=False,color=dark):
    c.setFillColor(color);c.setFont('MF-Bold' if bold else 'MF',sz);c.drawString(x,y,t)
def rule(y): c.setStrokeColor(line);c.setLineWidth(.8);c.line(50,y,W-50,y)
def wrapped(t,x,y,maxw,sz=12,leading=19,color=dark):
    words=t.split(); current=''; lines=[]
    for word in words:
        trial=(current+' '+word).strip()
        if pdfmetrics.stringWidth(trial,'MF',sz)>maxw and current:lines.append(current);current=word
        else:current=trial
    if current: lines.append(current)
    for ln in lines:
        txt(x,y,ln,sz,color=color);y-=leading
    return y

# Page frame
c.setFillColor(HexColor('#f9f9f6'));c.rect(0,0,W,H,fill=1,stroke=0)
txt(50,H-66,'MODULAR FRIENDS',14,True)
txt(W-170,H-66,content['location'].upper(),8,color=muted)
rule(H-84)
txt(50,H-155,content['tagline'],40)
txt(50,H-185,'MODULAR SYNTHESIS  /  LIVE IMPROVISATION  /  VISUAL COLLABORATION',8,color=muted)
y=H-235
y=wrapped(content['short_description'],50,y,W-100,15,24)
y-=36
rule(y+12)
txt(50,y-24,'ABOUT',9,True,color=muted)
y=wrapped(content['about'],160,y-24,W-211,10,17)
y-=34
rule(y+13)
txt(50,y-22,'PROGRAMME',9,True,color=muted)
fx=160; xx=y-20
for i,f in enumerate(content['formats'],1):
    txt(fx,xx,f"0{i}  {f['title']}",10,True)
    xx=wrapped(f['description'],fx+33,xx-16,W-235,9,14,color=muted)-8
y=xx-23
rule(y+10)
txt(50,y-22,'ARCHIVE',9,True,color=muted)
if content.get('events'):
    y=y-23
    shown=[e for e in content['events'] if e.get('confirmed',False)][:3]
    for e in shown:
        # Brief edition references appear in the PDF as well as on the HTML page.
        snippet=f"{e['date']}  /  {e['title']}"
        txt(160,y,snippet,8,color=muted)
        if e.get('source_url'):
            c.linkURL(e['source_url'],(158,y-4,W-50,y+10),relative=0,thickness=0)
        y-=16
else:
    y=wrapped(content['archive_intro'],160,y-22,W-210,9,16,color=muted)
y-=33
rule(y+12)
txt(50,y-20,'ONLINE',9,True,color=muted)
txt(160,y-20,insta,9)
c.linkURL(insta,(158,y-26,W-50,y-8),relative=0,thickness=0)
rule(89)
txt(50,64,'PRE-LAUNCH PROJECT PROFILE',8,color=muted)
txt(50,47,'This PDF and the website are generated from the same content source.',8,color=muted)
txt(W-145,47,content['updated'],8,color=muted)
c.save()
print(f'Wrote {OUT / "index.html"}\nWrote {path}\nSite URL: {site_url or "not configured; no sitemap generated"}')

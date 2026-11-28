# Modular Friends content management

Official website: https://modularfriends.github.io/
Official Google account: mfmodularfriends@gmail.com. Use free tools only.

## One verified source, two announcements

`content/site-updates.json` controls the event listings in Upcoming and Shop & Media / Tickets, the single homepage video, and the latest video plus individual previous release links in Shop & Media. Keep all existing `videos` records when changing `current_video`. Verify the public YouTube publication timestamp, title, artist spelling/roles and links before adding a new release. Use the original public YouTube video; its embed supplies its official thumbnail and playback. Do not replace LIAMEORE until a newer verified public video or confirmed relevant news exists. Do not invent missing dates/credits. The legacy current video's publication date remains explicitly unknown until verified; do not use an assumed date to decide what is newer.

After verified edits:

```
python scripts/build-site-updates.py
python scripts/build-event-archive.py
python -m unittest discover -s tests -p 'test_site_updates.py'
```

These scripts change only the marked announcements and existing archive section, preserving unrelated Work edits. Always fetch current main before editing and check its SHA again before pushing; rebase if changed. Never overwrite another Work session. The generator has no scheduled network scraping or external credentials.

## Event lifecycle

Announced, verified event: `status: upcoming`, precise ISO timestamps with timezone, original poster, historic page, Luma and RA links; confirmed free entry uses FREE REGISTRATION and voluntary donations only. Each event appears in Upcoming and Tickets. Next confirmed events are sorted chronologically. Exact end timestamps automatically hide expired listings in the browser, including Tickets, without waiting for an editor run. Calendar remains visible, with “Next announcement coming soon.” when no upcoming event exists.

Persistent archiving requires official confirmation of completion (check cancellation/rescheduling), `completion_confirmed: true` and `status: archived`; the generator refuses to archive a future or unconfirmed event. It inserts the event once into `content/event-archive.json`, newest first, under unnumbered events. Then rebuild the existing archive. Retain date/location/description, original poster and historical page, Luma/RA and later verified credits/media. Never assign an edition number to a meetup. Never delete a historical page or asset. Add any new confirmed media/credits to its existing archive record; reruns preserve that record.

Meetup: 5 December 2026, 16:00–22:00 Asia/Tbilisi, Plant Lovers — Niaghvari St. 4A. Luma https://luma.com/afkx210b (evt-swHkkgmDFZh2eBy); RA https://ra.co/events/2595834; page `events/2026-12-05-meetup.html`. Persistent archiving is due **6 December 2026 at 10:00 Asia/Tbilisi**, after completion verification.

## Scheduled editor

Existing task `Automation_4f3d84af4e2c81918384650a08061c8a`, “MF — საიტი, ვიდეოები და არქივი”, now runs **daily at 10:00 Asia/Tbilisi**, first check 29 November 2026. It includes the originally scheduled 6 December 10:00 Meetup action and checks future event lifecycle and official YouTube channel `UCW2AfTLV2mZ76JIVBLo7ZAg`. It verifies and publishes changes, checking live desktop/mobile. No duplicate monitor was created. Execution is scheduled agent work and depends on connected account access; it is not a guaranteed real-time webhook. If an authorized workflow publishes a YouTube video, update the website immediately in that same workflow.

Official feed: https://www.youtube.com/feeds/videos.xml?channel_id=UCW2AfTLV2mZ76JIVBLo7ZAg

Do not send email, newsletters or DMs as part of this website workflow. Luma calendar followers and registered event guests are different audiences; posting an event is not a substitute for sending a calendar newsletter.

## Media

Reuse original files and links. One asset has one primary event-named storage location; do not duplicate, delete historical media or create empty folders. Meetup existing canonical Drive folder: https://drive.google.com/drive/folders/1UWl5vNSR0gk993TBNXdiGFP-sjynUVpk (poster subfolder 1xs7_WG_b2d3ATBEh-t06GNJ-pBNmb22q). The existing website poster is a delivery rendition, not another canonical source. Add photos/video/participants only when verified and available.

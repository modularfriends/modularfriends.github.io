# MODULAR FRIENDS — WORK STATUS

Last checkpoint: 2026-11-13 (Asia/Tbilisi)
Repository: modularfriends/modularfriends.github.io
Active branch: main
Last verified code commit before this status file: 2c9d488d22ff1a82283f8045e416b5248eea8f89 (2026-11-05)
Commit message: Refine toolbar to 66:34 fields and align all controls at 70px

## Purpose
Persist a small, verifiable handoff across ChatGPT Work conversation interruptions. This is a status document, not a claim that unpublished edits were committed.

## Modular Friends Radio — published and playback verified
- Implementation commit: 99bdba44055617be2a36cef8898465d9c4268543.
- Audio sync commit: c69f325e3d51dd4f4656c76e373c91e5b9ba8eb4.
- 20 MP3 recordings, 6521.73 seconds total, hosted under radio/media. tracks.json is generated automatically.
- Shared HTML5 player appears at /#radio, /#artists, and /shop.html#audio. Light background, logo, Play/Pause, no Next, no autoplay, shuffle without repeats, bounded failures.
- Moved the 20 already-created MF-owned WAV copies from the older source folder into the requested radio folder; did not create duplicate Drive files or modify the originals.
- Public Drive folder (including sent by artists) syncs daily at 03:17 UTC / 07:17 Asia/Tbilisi, plus manual Actions dispatch. New MP3 files are copied unchanged. WAV-to-MP3 conversion happens only when the generated MP3 does not exist. Existing IDs are skipped; replacement audio requires a new Drive file ID.
- Successful first sync: https://github.com/modularfriends/modularfriends.github.io/actions/runs/43467672187
- Successful live Chromium tests: https://github.com/modularfriends/modularfriends.github.io/actions/runs/43468371159
- Live tests at 1280px and 390px: real MP3 playback on home and Audio, Play/Pause, shared artist controls, artist/title, responsive bounds; desktop automatic transition through a real ended event.
- Unit tests: three shuffled cycles with no repeats, cycle boundary, no autoplay, all-failed termination, empty playlist. Sync test: a new MP3 is added unchanged, existing media is not downloaded again, failed sync retains the published playlist.
- Independent cloud-browser playback confirmed currentTime advancing and readyState=4 on the published MP3.
- No API secrets, Base64 audio, paid services, or outstanding playback blockers.

## Next after radio
- About page: correct proportions of photo #03 (reported filename `gallery-collective-live.webp`, MF-011) to fit adjacent images, avoiding design disruptions.
- Audit all previously agreed website changes and preserve working components.

## ChatGPT Work incident
2026-11-13: multiple newly created Work chats ended within minutes with "You've reached the maximum length for this conversation." This is an app-side issue, not a confirmed GitHub issue. User is seeking OpenAI Support resolution. For continuity, checkpoint successful changes in GitHub with verifiable commit SHAs. Never assume a Work message "edited files" implies committed or deployed changes.

## Working rules
1. Compare repository head and live website before editing.
2. Make bounded changes and commit each finished work unit.
3. Verify build/deployment and log evidence here, including exact commit SHA and pending blockers.
4. Never overwrite functioning features or rerun already-completed media imports without checking the source and destination.

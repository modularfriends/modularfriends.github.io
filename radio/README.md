# Modular Friends Radio

One HTML5 audio element per document powers every `[data-mf-radio]` view. No autoplay, next button, embedded audio, or paid service.

Source: https://drive.google.com/drive/folders/1U9dLhBoj3UwKXGvL6SrDRJlKNa8NfhYS (including `sent by artists`). Public read access is required for automatic discovery and downloads. No API secrets are used.

The **Sync Modular Friends Radio** Actions workflow runs daily at 07:17 Asia/Tbilisi (03:17 UTC), on sync-code changes, and through **Run workflow**. It downloads new files only, copies MP3 bytes without conversion, converts original WAV files once to 192 kbps MP3, validates each audio stream, and commits the audio and `tracks.json`. GitHub Pages serves the audio with byte-range support. A failed sync preserves the previous playlist and does not publish partial results.

Use `Artist - Track Title.mp3`, or embedded artist/title tags. New Drive IDs are imported automatically; to replace audio, upload a new file rather than replacing the bytes behind an existing ID. A rename updates displayed fallback metadata on the next sync. Removing a file from the radio folder removes it on the next complete sync (an empty source fails safely). Source WAV files remain unchanged.

The public Drive folder contains the 20 already-created MF-owned copies moved from the older submissions folder on 2026-11-13. No duplicate Drive files were created.

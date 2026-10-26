# Modular Friends — one mailing list, all meaningful updates

This is the editorial configuration for Modular Friends email updates. The signup form on the public website must not accept addresses until a real, consent-based mailing-list provider is connected and tested.

## Audience and consent

- One list: `Modular Friends — All Updates`.
- Visitors subscribe on `https://modularfriends.github.io/#newsletter`; require an email address, an explicit consent statement and double opt-in confirmation.
- Store contacts in the provider, not in GitHub or the public repository. Only send to confirmed, currently subscribed contacts.
- Include a clear unsubscribe link in every email. Never import followers, scraped addresses or Luma calendar attendees without consent for these broader updates.

## What counts as an update

- Modular Friends live sessions, line-ups, venue/date announcements and ticket or calendar links.
- Festival appearances, site-specific performances and audiovisual installations.
- Workshops, lectures, educational sessions, open calls and community announcements.
- YouTube videos, live recordings and newly published documentation.
- New music and releases on Bandcamp, Spotify and any other official platform.
- New merchandise, limited editions, shop links and special collaborations.
- Significant project/site milestones and related announcements.

Do not send emails for typos, routine site edits or unverified future plans. Combine several small announcements into one concise digest when they happen close together. Each message should link to the public original source and never make a claimed event or release date without checking it.

## Publishing workflow

1. Confirm the news, original link and release/announcement date.
2. Select one category and populate `email-template.html`.
3. Send a preview to the official Modular Friends address.
4. Check mobile rendering, dates, artist names, links, unsubscribe and sender identity.
5. Send to the confirmed list in Brevo and record the campaign date/URL to avoid duplicates.

## Provider and configuration

The site reads `window.MF_NEWSLETTER.formUrl` from `newsletter-config.js`. Provide the HTTPS `https://sibforms.com/serve/...` link for the working Brevo double-opt-in iframe, then verify subscriptions end-to-end. Never put the Brevo API key or private credentials in the public repository. Sending campaigns requires a connected provider account; creating this template does not automatically broadcast updates.

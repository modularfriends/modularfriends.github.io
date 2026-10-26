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

## Current publishing state (27 October 2026)

The public site is restored to **Luma-only** for calendar follows: `https://luma.com/modularfriends`. There is no active embedded email form or independent subscriber database on the site. Do not claim that it is collecting newsletter emails.

## Evaluating a permanent no-trial free solution

EmailOctopus Starter is the preferred candidate, subject to a real account and end-to-end tests. On the published October 2026 free terms: no trial or credit card required; up to 2,500 subscribers, 10,000 emails/month, one inline form, one landing page, and up to three automations. It offers JavaScript embed forms and optional double opt-in (not enabled by default). Kit's explicitly Free plan is another option: up to 10,000 subscribers, unlimited broadcasts, but RSS campaigns and workflows need paid tiers.

The user has registered for EmailOctopus with the official Modular Friends Google account, but the dashboard, list and form have NOT yet been configured or verified. Do not embed any script or activate a public signup until:
1. A Modular Friends account on the provider is operational and free after 14 days, with a real test list.
2. The inline form is added to a test page and tried on iOS Safari, Chrome and Firefox.
3. A test email is successfully submitted, the confirmation email arrives, and subscriber status changes from Pending to Subscribed.
4. An actual test newsletter arrives, and unsubscribe works.
5. Verify any sender rewrite caused by using mfmodularfriends@gmail.com as the sender. An authenticated custom domain is preferable but not a precondition for exploring the free plan.
6. Only then replace the Luma signup CTA with a working embedded provider form; keep Luma separately for calendar/events.

Never put provider API tokens or personal mailing-list addresses in this public repository.

## Current integration code (dormant until verified)

The live website still displays the Luma Follow CTA. Set `emailOctopus.enabled: true` in `newsletter-config.js` only AFTER a complete successful test. Copy the exact PUBLIC script `src` and `data-form` values from **Grow → Forms → [inline form] → </> Add to your website** into `formScriptUrl` and `formId`. Valid sources are EmailOctopus's `https://eocampaignN.com/form/<id>.js` scripts. Never paste an API key or grant provider admin access to public web code.

The form's actual data storage lives in EmailOctopus, not the GitHub Pages repository. The production loader will keep the Luma CTA visible unless a real form is rendered. Full end-to-end subscription and unsubscribe tests are still required before publishing it to visitors.

### Confirmed product behaviour

**Contacts → List → Consent & customisation → Double opt-in email**: turn it on explicitly (EmailOctopus starts with single opt-in). Then create the **Grow → Forms → Inline** signup, with one email field and a clear consent statement saying messages may include events, festival appearances, workshops, lectures, YouTube videos, Bandcamp/Spotify releases, new merchandise and announcements. Use one `Modular Friends — All Updates` list.

Starter is permanently free up to 2,500 subscribers and 10,000 emails/month; it permits only one hosted form and one landing page. Nonprofits/other options may differ; check the account plan before sending. EmailOctopus requires `{{UnsubscribeURL}}` as a text link, `{{SenderInfo}}` or `{{SenderInfoLine}}`, and `{{RewardsURL}}` as a text link on the free Starter plan. Set a non-sensitive mailing address in the account's Sender info (do not publish someone's home address just for the campaign).

### Signup microcopy

- List name: `Modular Friends — All Updates`
- Heading: `DON'T MISS WHAT'S NEXT.`
- Subheading: `Live sets, festivals, workshops, talks, new music, YouTube videos, Bandcamp and Spotify releases, new merch and occasional community news.`
- Input: `Your email address`
- Button: `SUBSCRIBE`
- Consent: `I agree to receive Modular Friends email updates. I can unsubscribe at any time.`
- Pending confirmation: `Check your inbox and confirm your email address to complete your subscription.`
- Confirmation email subject: `Confirm your Modular Friends subscription`
- Confirmation success: `You're subscribed. See you at the next one.`
- Official sender: `Modular Friends <mfmodularfriends@gmail.com>`, subject to EmailOctopus sender validation and Gmail-domain rewrites.

# Focus Library

Static web app (installable on a phone). No build step.

- `index.html`, `sw.js`, `manifest.webmanifest`, icons: the app
- `channels.json`: channels to track, e.g. `[{"key":"@handle","name":"Podcast name","id":"UC..."}]`
- `scripts/update_feeds.py` + `.github/workflows/feeds.yml`: every 3 hours GitHub fetches each channel's public feed and commits `feeds.json`; the app adds new episodes to any folder linked to that channel
- Host on any HTTPS static host (GitHub Pages: Settings -> Pages -> Deploy from branch -> main / root)
- Opening `index.html` from disk will not play videos; YouTube requires a real https page
- Your library is stored in the browser on each device. Use Edit -> Export backup to save a copy.
- If you block YouTube, allow the embedded player (`youtube.com/embed`) in your blocker. Sign in to YouTube in the same browser (Premium) to avoid ads.

## Notes and transcripts

- **Notes** (button under the player): one note per video, with headings, lists, quotes, text and highlight colors. `# `, `## `, `- `, `1. ` and `> ` at the start of a line work like in Notion.
- **Transcript** tab: pulls the video's transcript through your own Apify account. "Get captions" uses YouTube's captions (no speaker names). "Split by speaker" transcribes the audio and labels speakers; it is a paid run. Tap ⚙ to paste your Apify API token. The token is kept in the browser only, never in this repo.
- Select transcript text and choose **Save quote**: the words, start and end time and a named link go into the note. Tapping a link jumps the video to that second.
- **Copy for Notion** puts the note on the clipboard. Links look like `https://<this site>/?v=<video id>&t=<seconds>` and open the video here at that moment. Colors are not kept by Notion when pasting.
- Notes and transcripts are stored in the browser on each device and are included in Edit -> Export backup.

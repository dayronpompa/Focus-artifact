# Focus Library

Static web app (installable on a phone). No build step.

- `index.html`, `sw.js`, `manifest.webmanifest`, icons: the app
- `channels.json`: channels to track, e.g. `[{"key":"@handle","name":"Podcast name","id":"UC..."}]`
- `scripts/update_feeds.py` + `.github/workflows/feeds.yml`: every 3 hours GitHub fetches each channel's public feed and commits `feeds.json`; the app adds new episodes to any folder linked to that channel
- Host on any HTTPS static host (GitHub Pages: Settings -> Pages -> Deploy from branch -> main / root)
- Opening `index.html` from disk will not play videos; YouTube requires a real https page
- Your library is stored in the browser on each device. Use Edit -> Export backup to save a copy.
- If you block YouTube, allow `youtube-nocookie.com` (the embedded player) in your blocker.

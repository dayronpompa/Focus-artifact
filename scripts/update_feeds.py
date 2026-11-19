#!/usr/bin/env python3
"""Reads channels.json, fetches each channel's public YouTube feed, writes feeds.json.

channels.json example:
[
  {"key": "@handle", "name": "Podcast name", "id": "UCxxxxxxxxxxxxxxxxxxxxxx"}
]
"id" is optional; if missing the script looks it up from the @handle page.
"""
import json, re, sys, pathlib, urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (compatible; FocusLibraryFeed/1.0)"}
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
MAX_VIDEOS = 30


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30).read()


def resolve_id(entry):
    if entry.get("id"):
        return entry["id"]
    key = entry["key"]
    handle = key if key.startswith("@") else "@" + key
    html = get("https://www.youtube.com/" + handle).decode("utf-8", "ignore")
    m = re.search(r'"channelId":"(UC[\w-]{22})"', html) or re.search(r"channel/(UC[\w-]{22})", html)
    return m.group(1) if m else None


def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    title = root.findtext("a:title", namespaces=NS)
    videos = []
    for e in root.findall("a:entry", NS):
        vid = e.findtext("yt:videoId", namespaces=NS)
        t = e.findtext("a:title", namespaces=NS)
        pub = e.findtext("a:published", namespaces=NS)
        if vid and t:
            videos.append({"id": vid, "title": t, "published": pub})
    return title, videos


def main():
    cfg = json.loads((ROOT / "channels.json").read_text())
    out_path = ROOT / "feeds.json"
    try:
        old = json.loads(out_path.read_text())
    except Exception:
        old = {"channels": {}}
    res = {"channels": {}}
    for entry in cfg:
        key = entry["key"]
        try:
            cid = resolve_id(entry)
            if not cid:
                raise RuntimeError("could not find channel id")
            title, videos = parse(get("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid))
            res["channels"][key] = {"name": entry.get("name") or title or key, "id": cid, "videos": videos[:MAX_VIDEOS]}
        except Exception as ex:  # keep the previous data if a fetch fails
            print("WARN", key, ex, file=sys.stderr)
            if key in old.get("channels", {}):
                res["channels"][key] = old["channels"][key]
    out_path.write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

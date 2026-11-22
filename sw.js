// Network first, cache as fallback: updates arrive immediately, the app still opens offline.
const CACHE = 'focus-v4';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET' || new URL(r.url).origin !== location.origin) return;
  // Timestamp links (?v=...&t=...) are the same page: do not store one copy per link, and serve the app when offline.
  const plain = !new URL(r.url).search;
  e.respondWith(fetch(r, { cache:'no-cache' }).then(res => {   // always ask GitHub for the newest copy; fall back to the saved one offline
    if (res.ok && plain){ const copy = res.clone(); caches.open(CACHE).then(c => c.put(r, copy)); }
    return res;
  }).catch(() => caches.match(r).then(m => m || (r.mode === 'navigate' ? caches.match('index.html') : undefined))));
});

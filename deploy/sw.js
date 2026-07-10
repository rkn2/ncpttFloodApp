/* Service worker — Historic Flood Recovery Tool
 *
 * Offline is a CORE requirement: after a flood there is often no cell/internet, so the whole app
 * (shell + guidance bundle + knowledge base) is PRECACHED at install. Fail-closed: if any shell
 * asset can't be cached, install fails loudly rather than leaving a half-offline app.
 *
 * CACHE_VERSION MUST be bumped on every deploy — otherwise returning users are stranded on the
 * old cached app forever. This is the #1 hand-written-SW failure mode.
 */
const CACHE_VERSION = 'flood-recovery-v2';   // ⬅ bump this string on every deploy
const SHELL = [
  './',
  './index.html',
  './content-bundle.json',
  './knowledge-base.json',
  './manifest.webmanifest',
  './icon.svg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then((cache) => cache.addAll(SHELL))   // rejects (install fails) if any asset is missing
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Only handle same-origin GETs. The Groq chat API is cross-origin and must NEVER be cached —
  // let it hit the network; offline, the app already falls back to local passage retrieval.
  if (req.method !== 'GET' || url.origin !== self.location.origin) {
    return; // default browser handling (network)
  }

  // Cache-first for the app shell + assets.
  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req)
        .then((resp) => {
          // opportunistically cache successful same-origin GETs
          if (resp && resp.ok) {
            const copy = resp.clone();
            caches.open(CACHE_VERSION).then((c) => c.put(req, copy));
          }
          return resp;
        })
        .catch(() => {
          // Navigation request offline with nothing cached -> serve the cached app shell.
          if (req.mode === 'navigate') return caches.match('./index.html');
          return Response.error();
        });
    })
  );
});

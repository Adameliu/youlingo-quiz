const CACHE = "youlingo-v1";
const DATA_CACHE = "youlingo-data-v1";

// Files to cache on install
const STATIC_FILES = [
  "/",
  "/index.html",
  "/study_app.html",
  "/manifest.json",
  "/icon-192.png",
  "/icon-512.png"
];

self.addEventListener("install", function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll(STATIC_FILES);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) { return k !== CACHE && k !== DATA_CACHE; })
          .map(function(k) { return caches.delete(k); })
      );
    })
  );
  self.clients.claim();
});

// Cache JSON data files separately
self.addEventListener("fetch", function(e) {
  var url = new URL(e.request.url);
  
  // For JSON data files, cache them
  if (url.pathname.endsWith(".json") && url.hostname !== "firebaseio.com") {
    e.respondWith(
      caches.open(DATA_CACHE).then(function(cache) {
        return fetch(e.request).then(function(resp) {
          cache.put(e.request, resp.clone());
          return resp;
        }).catch(function() {
          return caches.match(e.request);
        });
      })
    );
    return;
  }
  
  // For R2 audio, network first, fallback to cache
  if (url.hostname.includes("r2.dev")) {
    e.respondWith(
      fetch(e.request).catch(function() {
        return caches.match(e.request);
      })
    );
    return;
  }
  
  // For everything else, cache-first (offline first)
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      return cached || fetch(e.request).then(function(resp) {
        if (resp.status === 200) {
          var respClone = resp.clone();
          caches.open(CACHE).then(function(cache) { cache.put(e.request, respClone); });
        }
        return resp;
      });
    })
  );
});

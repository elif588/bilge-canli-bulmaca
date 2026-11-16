// Almina Tarot PWA Service Worker
const CACHE_NAME = 'almina-tarot-v1';

self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', (e) => {
  // Canlı WebSocket ve dinamik sesler için doğrudan network kullan
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});

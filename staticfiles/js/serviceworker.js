const CACHE_NAME = 'hangarin-cache-v1';
const URLS_TO_CACHE = [
    '/',
    '/tasks/',
    '/static/css/',
];

// Install — cache core assets
self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(URLS_TO_CACHE);
        })
    );
    self.skipWaiting();
});

// Activate — clean up old caches
self.addEventListener('activate', function(e) {
    e.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames
                    .filter(name => name !== CACHE_NAME)
                    .map(name => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

// Fetch — serve from cache, fall back to network
self.addEventListener('fetch', function(e) {
    // Skip non-GET and admin/API requests
    if (
        e.request.method !== 'GET' ||
        e.request.url.includes('/admin/') ||
        e.request.url.includes('/api/') ||
        e.request.url.includes('/accounts/')
    ) {
        return;
    }

    e.respondWith(
        caches.match(e.request).then(function(response) {
            if (response) {
                return response;
            }
            return fetch(e.request).then(function(networkResponse) {
                // Cache successful page responses
                if (
                    networkResponse &&
                    networkResponse.status === 200 &&
                    networkResponse.type === 'basic'
                ) {
                    const responseClone = networkResponse.clone();
                    caches.open(CACHE_NAME).then(function(cache) {
                        cache.put(e.request, responseClone);
                    });
                }
                return networkResponse;
            });
        }).catch(function() {
            // Offline fallback — return cached homepage
            return caches.match('/');
        })
    );
});
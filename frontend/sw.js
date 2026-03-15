// FRAS Service Worker — Basic caching for offline support
const CACHE_NAME = 'fras-cache-v1';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/login.html',
    '/survey.html',
    '/dashboard.html',
    '/history.html',
    '/result.html',
    '/image_assessment.html',
    '/improvement.html',
    '/css/main.css',
    '/css/survey.css',
    '/css/dashboard.css',
    '/js/api.js',
    '/js/survey.js',
    '/js/charts.js',
    '/js/export.js',
];

// Install — cache static assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(STATIC_ASSETS).catch(() => { });
        })
    );
    self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

// Fetch — network first, cache fallback for pages
self.addEventListener('fetch', event => {
    const { request } = event;

    // Skip non-GET, API calls, and chrome-extension requests
    if (request.method !== 'GET' || request.url.includes('/api/') || !request.url.startsWith('http')) {
        return;
    }

    event.respondWith(
        fetch(request).then(response => {
            // Cache successful responses
            if (response.ok) {
                const clone = response.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
            }
            return response;
        }).catch(() => {
            // Fallback to cache
            return caches.match(request).then(cached => {
                return cached || new Response('Offline — Vui lòng kết nối mạng', {
                    status: 503,
                    headers: { 'Content-Type': 'text/html; charset=utf-8' }
                });
            });
        })
    );
});

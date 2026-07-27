const CACHE_NAME = "asi-alignment-site-v1";
const OFFLINE_URL = "/";
const CORE_URLS = [
  "/",
  "/paths/",
  "/cards/",
  "/book/",
  "/faq/",
  "/glossary/",
  "/notation/",
  "/experiments/",
  "/lean/",
  "/references/",
  "/updates/",
  "/news/",
  "/badges/",
  "/about/",
  "/search-index.json",
  "/og-image.png"
];

function isExcluded(url) {
  return url.pathname.endsWith(".pdf") ||
    url.pathname === "/demos" ||
    url.pathname.startsWith("/demos/") ||
    url.pathname === "/chapter-demos" ||
    url.pathname.startsWith("/chapter-demos/");
}

async function cacheSite() {
  const cache = await caches.open(CACHE_NAME);
  const sitemapResponse = await fetch("/sitemap-0.xml", { cache: "no-store" });
  const sitemap = await sitemapResponse.text();
  const sitemapUrls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)]
    .map((match) => new URL(match[1], self.location.origin))
    .filter((url) => url.origin === self.location.origin && !isExcluded(url))
    .map((url) => url.href);
  const urls = [...new Set([...CORE_URLS, ...sitemapUrls])];
  let completed = 0;
  for (const url of urls) {
    try {
      await cache.add(url);
    } catch (error) {
      console.warn("Offline cache skipped", url, error);
    }
    completed += 1;
    const clients = await self.clients.matchAll({ type: "window" });
    for (const client of clients) {
      client.postMessage({ type: "offline-progress", completed, total: urls.length });
    }
  }
  return { completed, total: urls.length };
}

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(CORE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (event) => {
  if (event.data?.type !== "cache-site") return;
  event.waitUntil(
    cacheSite().then((result) => {
      self.clients.matchAll({ type: "window" }).then((clients) => {
        for (const client of clients) {
          client.postMessage({ type: "offline-complete", ...result });
        }
      });
    })
  );
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin || isExcluded(url)) return;
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request).then((response) => {
      if (response.ok) {
        const copy = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
      }
      return response;
    }).catch(() => caches.match(OFFLINE_URL)))
  );
});

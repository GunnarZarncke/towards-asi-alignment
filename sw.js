const CACHE_NAME = "asi-alignment-site-v7";
const CACHE_MAX_AGE_MS = 60 * 60 * 1000;
const OFFLINE_URL = "/offline/";
const OFFLINE_ENABLED = "offline-enabled";
const CORE_URLS = [
  "/",
  OFFLINE_URL,
  "/paths/",
  "/cards/",
  "/book/",
  "/faq/",
  "/experiments/",
  "/lean/",
  "/references/",
  "/updates/",
  "/news/",
  "/badges/",
  "/about/",
  "/glossary/",
  "/notation/",
  "/search-index.json"
];
const OFFLINE_FALLBACK = new Response(
  `<!doctype html><title>Not available offline yet</title><meta name="viewport" content="width=device-width,initial-scale=1"><main><h1>Not available offline yet</h1><p>This page has not been saved for offline use. While online, click “Make site available offline” at the bottom of any page to save the full site.</p></main>`,
  { headers: { "content-type": "text/html; charset=utf-8" } }
);

function isExcluded(url) {
  return url.pathname.endsWith(".pdf") ||
    url.pathname === "/demos" ||
    url.pathname.startsWith("/demos/") ||
    url.pathname === "/chapter-demos" ||
    url.pathname.startsWith("/chapter-demos/");
}

async function cacheWithTimestamp(cache, request, response) {
  const headers = new Headers(response.headers);
  headers.set("x-sw-cached-at", String(Date.now()));
  await cache.put(request, new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  }));
}

async function cacheSite() {
  const cache = await caches.open(CACHE_NAME);
  const sitemapResponse = await fetch("/sitemap-0.xml", { cache: "no-store" });
  if (!sitemapResponse.ok) throw new Error(`Could not load sitemap (${sitemapResponse.status})`);
  const sitemap = await sitemapResponse.text();
  const sitemapUrls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)]
    .map((match) => new URL(match[1], self.location.origin))
    .filter((url) => url.origin === self.location.origin && !isExcluded(url))
    .map((url) => url.href);
  let completed = 0;
  const queued = [...new Set([...CORE_URLS, ...sitemapUrls])];
  const seen = new Set();
  while (queued.length > 0) {
    const url = queued.shift();
    if (seen.has(url)) continue;
    seen.add(url);
    try {
      const response = await fetch(url, { cache: "no-store" });
      if (response.ok) {
        await cacheWithTimestamp(cache, url, response.clone());
        if (response.headers.get("content-type")?.includes("text/html")) {
          const html = await response.text();
          for (const match of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
            const dependency = new URL(match[1], url);
            if (
              dependency.origin === self.location.origin &&
              !isExcluded(dependency) &&
              !seen.has(dependency.href)
            ) {
              queued.push(dependency.href);
            }
          }
        }
      }
    } catch (error) {
      console.warn("Offline cache skipped", url, error);
    }
    completed += 1;
    const clients = await self.clients.matchAll({ type: "window" });
    for (const client of clients) {
      client.postMessage({
        type: "offline-progress",
        completed,
        total: Math.max(sitemapUrls.length + CORE_URLS.length, seen.size + queued.length)
      });
    }
  }
  await cache.put(OFFLINE_ENABLED, new Response("true"));
  return { completed, total: seen.size };
}

async function notifyClients(message) {
  const clients = await self.clients.matchAll({ type: "window" });
  for (const client of clients) client.postMessage(message);
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
    cacheSite()
      .then((result) => notifyClients({ type: "offline-complete", ...result }))
      .catch((error) => notifyClients({ type: "offline-error", message: error.message }))
  );
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin || isExcluded(url)) return;
  event.respondWith(caches.open(CACHE_NAME).then(async (cache) => {
    const cached = await cache.match(event.request);
    const cachedAt = Number(cached?.headers.get("x-sw-cached-at") ?? 0);
    if (cached && cachedAt && Date.now() - cachedAt < CACHE_MAX_AGE_MS) return cached;
    try {
      const response = await fetch(event.request);
      if (response.ok) await cacheWithTimestamp(cache, event.request, response.clone());
      return response;
    } catch {
      if (cached) return cached;
      if (event.request.mode === "navigate") return (await cache.match(OFFLINE_URL)) || OFFLINE_FALLBACK;
      throw new Error("Offline asset unavailable");
    }
  }));
});

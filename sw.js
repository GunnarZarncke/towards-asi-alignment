const CACHE_NAME = "asi-alignment-site-v9";
const CACHE_PREFIX = "asi-alignment-site-";
const OFFLINE_URL = "/offline/";
const OFFLINE_ENABLED = "offline-enabled";
const OFFLINE_PROGRESS = "offline-progress";
const SHELL_URLS = ["/", OFFLINE_URL, "/search-index.json"];
const STATIC_ASSETS = [
  "/manifest.webmanifest",
  "/favicon.ico",
  "/favicon.svg",
  "/apple-touch-icon.png",
  "/logo-circle.svg",
  "/logo.svg",
  "/icon-192.png",
  "/icon-512.png",
  "/og-image.png"
];
const OFFLINE_FALLBACK = new Response(
  `<!doctype html><title>Not available offline yet</title><meta name="viewport" content="width=device-width,initial-scale=1"><main><h1>Not available offline yet</h1><p>This page has not been saved for offline use. While online, click “Make site available offline” at the bottom of any page to save the full site.</p></main>`,
  { headers: { "content-type": "text/html; charset=utf-8" } }
);

let cacheSitePromise = null;

function isExcluded(url) {
  return url.pathname.endsWith(".pdf") ||
    url.pathname === "/demos" ||
    url.pathname.startsWith("/demos/") ||
    url.pathname === "/chapter-demos" ||
    url.pathname.startsWith("/chapter-demos/");
}

function assetPriority(url) {
  const path = new URL(url).pathname;
  if (path.endsWith(".css")) return 0;
  if (path.endsWith(".woff2")) return 1;
  if (path.endsWith(".woff") || path.endsWith(".ttf")) return 2;
  if (path.startsWith("/_astro/") && path.endsWith(".js")) return 3;
  if (/\.(svg|png|ico|webp|webmanifest)$/.test(path)) return 4;
  if (path.endsWith(".js")) return 5;
  if (path.endsWith(".json") || path.endsWith(".xml")) return 6;
  return 7;
}

function extractDependencies(html, baseUrl) {
  const deps = [];
  for (const match of html.matchAll(/(?:src|href)="([^"]+)"/g)) {
    const dependency = new URL(match[1], baseUrl);
    if (dependency.origin === self.location.origin && !isExcluded(dependency)) {
      deps.push(dependency.href);
    }
  }
  return deps;
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

async function isCachedOk(cache, url) {
  const response = await cache.match(url);
  return Boolean(response && response.ok);
}

async function notifyClients(message) {
  const clients = await self.clients.matchAll({ type: "window" });
  for (const client of clients) client.postMessage(message);
}

async function reportProgress(cache, phase, completed, total) {
  const payload = { phase, completed, total };
  await cache.put(OFFLINE_PROGRESS, new Response(JSON.stringify(payload)));
  await notifyClients({ type: "offline-progress", ...payload });
}

async function fetchAndCache(cache, url) {
  if (await isCachedOk(cache, url)) {
    return { discovered: [] };
  }
  try {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) return { discovered: [] };
    await cacheWithTimestamp(cache, url, response.clone());
    if (!response.headers.get("content-type")?.includes("text/html")) {
      return { discovered: [] };
    }
    const html = await response.text();
    return { discovered: extractDependencies(html, url) };
  } catch (error) {
    console.warn("Offline cache skipped", url, error);
    return { discovered: [] };
  }
}

async function loadSitemapUrls() {
  const sitemapResponse = await fetch("/sitemap-0.xml", { cache: "no-store" });
  if (!sitemapResponse.ok) throw new Error(`Could not load sitemap (${sitemapResponse.status})`);
  const sitemap = await sitemapResponse.text();
  return [...new Set(
    [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)]
      .map((match) => new URL(match[1], self.location.origin))
      .filter((url) => url.origin === self.location.origin && !isExcluded(url))
      .map((url) => url.href)
  )];
}

async function discoverAssetUrls(cache) {
  const discovered = new Set(STATIC_ASSETS);
  for (const url of SHELL_URLS) {
    const result = await fetchAndCache(cache, url);
    for (const dep of result.discovered) discovered.add(dep);
  }
  for (const url of SHELL_URLS) discovered.delete(url);
  return [...discovered].sort((a, b) => assetPriority(a) - assetPriority(b));
}

async function cacheSite() {
  const cache = await caches.open(CACHE_NAME);
  const sitemapUrls = await loadSitemapUrls();
  const pageUrls = [...new Set([...SHELL_URLS, ...sitemapUrls])];
  const assetUrls = await discoverAssetUrls(cache);
  const total = assetUrls.length + pageUrls.length;
  let completed = 0;

  for (const url of assetUrls) {
    await fetchAndCache(cache, url);
    completed += 1;
    await reportProgress(cache, "assets", completed, total);
  }

  await cache.put(OFFLINE_ENABLED, new Response("true"));
  await reportProgress(cache, "pages", completed, total);

  for (const url of pageUrls) {
    const result = await fetchAndCache(cache, url);
    for (const dep of result.discovered) {
      if (await isCachedOk(cache, dep)) continue;
      await fetchAndCache(cache, dep);
    }
    completed += 1;
    await reportProgress(cache, "pages", completed, total);
  }

  await cache.delete(OFFLINE_PROGRESS);
  return { completed, total };
}

function runCacheSite() {
  if (!cacheSitePromise) {
    cacheSitePromise = cacheSite()
      .then((result) => {
        notifyClients({ type: "offline-complete", ...result });
        return result;
      })
      .catch((error) => {
        notifyClients({ type: "offline-error", message: error.message });
        throw error;
      })
      .finally(() => {
        cacheSitePromise = null;
      });
  }
  return cacheSitePromise;
}

async function getOfflineStatus() {
  const cache = await caches.open(CACHE_NAME);
  const enabled = await cache.match(OFFLINE_ENABLED);
  const progressResponse = await cache.match(OFFLINE_PROGRESS);
  let progress = null;
  if (progressResponse) {
    try {
      progress = await progressResponse.json();
    } catch {
      progress = null;
    }
  }
  return {
    enabled: Boolean(enabled),
    caching: Boolean(cacheSitePromise),
    progress
  };
}

async function migrateLegacyCaches() {
  const keys = await caches.keys();
  const legacyKeys = keys.filter((key) => key.startsWith(CACHE_PREFIX) && key !== CACHE_NAME);
  if (legacyKeys.length === 0) return;

  const target = await caches.open(CACHE_NAME);
  for (const key of legacyKeys) {
    const legacy = await caches.open(key);
    const requests = await legacy.keys();
    await Promise.all(requests.map(async (request) => {
      if (await target.match(request)) return;
      const response = await legacy.match(request);
      if (response) await target.put(request, response);
    }));
    await caches.delete(key);
  }
}

async function fetchFromNetwork(request) {
  return fetch(request, { cache: "no-store" });
}

async function handleFetch(request, cache, offlineEnabled) {
  if (!offlineEnabled) {
    try {
      return await fetchFromNetwork(request);
    } catch {
      if (request.mode === "navigate") return OFFLINE_FALLBACK;
      throw new Error("Offline asset unavailable");
    }
  }

  try {
    const response = await fetchFromNetwork(request);
    if (response.ok) await cacheWithTimestamp(cache, request, response.clone());
    return response;
  } catch {
    const cached = await cache.match(request);
    if (cached) return cached;
    if (request.mode === "navigate") return (await cache.match(OFFLINE_URL)) || OFFLINE_FALLBACK;
    throw new Error("Offline asset unavailable");
  }
}

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(SHELL_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    migrateLegacyCaches()
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (event) => {
  if (event.data?.type === "cache-site") {
    event.waitUntil(runCacheSite());
    return;
  }
  if (event.data?.type === "offline-status") {
    event.waitUntil(
      getOfflineStatus().then((status) => {
        if (event.source) event.source.postMessage({ type: "offline-status", ...status });
      })
    );
  }
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin || isExcluded(url)) return;
  event.respondWith(
    caches.open(CACHE_NAME)
      .then(async (cache) => {
        const offlineEnabled = await cache.match(OFFLINE_ENABLED);
        return handleFetch(event.request, cache, offlineEnabled);
      })
  );
});

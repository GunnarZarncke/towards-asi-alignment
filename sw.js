const CACHE_NAME = "asi-alignment-site-v11";
const CACHE_PREFIX = "asi-alignment-site-";
const OFFLINE_URL = "/offline/";
const OFFLINE_STATE = "offline-state";
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

function originUrl(value, base = self.location.origin) {
  try {
    const url = new URL(value, base);
    if (url.origin !== self.location.origin) return null;
    if (url.protocol !== "http:" && url.protocol !== "https:") return null;
    url.hash = "";
    if (isExcluded(url)) return null;
    return url;
  } catch {
    return null;
  }
}

function isExcluded(url) {
  return url.pathname.endsWith(".pdf") ||
    url.pathname === "/demos" ||
    url.pathname.startsWith("/demos/") ||
    url.pathname === "/chapter-demos" ||
    url.pathname.startsWith("/chapter-demos/");
}

function assetPriority(href) {
  const url = originUrl(href);
  const path = url?.pathname ?? String(href);
  if (path.endsWith(".css")) return 0;
  if (path.endsWith(".woff2")) return 1;
  if (path.endsWith(".woff") || path.endsWith(".ttf")) return 2;
  if (path.startsWith("/_astro/") && path.endsWith(".js")) return 3;
  if (/\.(svg|png|ico|webp|webmanifest)$/.test(path)) return 4;
  if (path.endsWith(".js")) return 5;
  if (path.endsWith(".json") || path.endsWith(".xml")) return 6;
  return 7;
}

function extractDependencies(body, baseUrl, contentType) {
  const deps = [];
  const add = (value) => {
    const url = originUrl(value, baseUrl);
    if (url) deps.push(url.href);
  };
  if (contentType.includes("text/css")) {
    for (const match of body.matchAll(/url\(\s*['"]?([^'")]+)['"]?\s*\)/g)) {
      add(match[1].trim());
    }
    return deps;
  }
  for (const match of body.matchAll(/(?:src|href)=["']([^"']+)["']/g)) {
    add(match[1]);
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

function defaultState() {
  return {
    phase: "idle",
    completed: 0,
    total: 0,
    enabled: false,
    error: null,
    finished: false
  };
}

async function readState(cache) {
  const response = await cache.match(OFFLINE_STATE);
  if (response) {
    try {
      return { ...defaultState(), ...await response.json() };
    } catch {
      return defaultState();
    }
  }
  if (await cache.match("offline-enabled")) {
    return { ...defaultState(), enabled: true, phase: "pages", finished: false };
  }
  return defaultState();
}

async function writeState(cache, state) {
  await cache.put(OFFLINE_STATE, new Response(JSON.stringify(state)));
  await notifyClients({ type: "offline-progress", ...state, caching: Boolean(cacheSitePromise) });
}

async function maybeEnableOffline(cache, state) {
  if (state.enabled) return state;
  const homeReady = await isCachedOk(cache, new URL("/", self.location.origin).href);
  const cssReady = (await cache.keys()).some((request) => {
    const url = originUrl(request.url);
    return Boolean(url?.pathname.endsWith(".css"));
  });
  if (homeReady && cssReady) {
    state.enabled = true;
    await writeState(cache, state);
  }
  return state;
}

async function fetchAndCache(cache, href) {
  const url = originUrl(href);
  if (!url) return { discovered: [] };
  if (await isCachedOk(cache, url.href)) {
    return { discovered: [] };
  }
  try {
    const response = await fetch(url.href, { cache: "no-store" });
    if (!response.ok) return { discovered: [] };
    const contentType = response.headers.get("content-type") ?? "";
    await cacheWithTimestamp(cache, url.href, response.clone());
    if (!contentType.includes("text/html") && !contentType.includes("text/css")) {
      return { discovered: [] };
    }
    const body = await response.text();
    return { discovered: extractDependencies(body, url.href, contentType) };
  } catch (error) {
    console.warn("Offline cache skipped", url.href, error);
    return { discovered: [] };
  }
}

async function loadSitemapUrls() {
  const sitemapResponse = await fetch("/sitemap-0.xml", { cache: "no-store" });
  if (!sitemapResponse.ok) throw new Error(`Could not load sitemap (${sitemapResponse.status})`);
  const sitemap = await sitemapResponse.text();
  return [...new Set(
    [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)]
      .map((match) => originUrl(match[1]))
      .filter(Boolean)
      .map((url) => url.href)
  )];
}

async function discoverAssetUrls(cache) {
  const discovered = new Set(STATIC_ASSETS.map((path) => originUrl(path)?.href).filter(Boolean));
  const seed = [...SHELL_URLS, ...STATIC_ASSETS];
  for (const href of seed) {
    const result = await fetchAndCache(cache, href);
    for (const dep of result.discovered) discovered.add(dep);
  }
  for (const href of SHELL_URLS) {
    const url = originUrl(href);
    if (url) discovered.delete(url.href);
  }
  return [...discovered].sort((a, b) => assetPriority(a) - assetPriority(b));
}

async function cacheSite() {
  const cache = await caches.open(CACHE_NAME);
  const state = {
    ...defaultState(),
    phase: "assets",
    error: null,
    finished: false
  };
  await writeState(cache, state);

  const sitemapUrls = await loadSitemapUrls();
  const pageUrls = [...new Set([...SHELL_URLS.map((path) => originUrl(path)?.href).filter(Boolean), ...sitemapUrls])];
  const assetUrls = await discoverAssetUrls(cache);
  state.total = assetUrls.length + pageUrls.length;
  state.completed = 0;
  await maybeEnableOffline(cache, state);
  await writeState(cache, state);

  for (const href of assetUrls) {
    const result = await fetchAndCache(cache, href);
    for (const dep of result.discovered) {
      await fetchAndCache(cache, dep);
    }
    state.completed += 1;
    await maybeEnableOffline(cache, state);
    await writeState(cache, state);
  }

  state.phase = "pages";
  await maybeEnableOffline(cache, state);
  if (!state.enabled) {
    state.enabled = true;
  }
  await writeState(cache, state);

  for (const href of pageUrls) {
    const result = await fetchAndCache(cache, href);
    for (const dep of result.discovered) {
      await fetchAndCache(cache, dep);
    }
    state.completed += 1;
    await writeState(cache, state);
  }

  state.phase = "complete";
  state.finished = true;
  state.enabled = true;
  state.error = null;
  await writeState(cache, state);
  return state;
}

function runCacheSite() {
  if (!cacheSitePromise) {
    cacheSitePromise = cacheSite()
      .then((result) => {
        notifyClients({ type: "offline-complete", ...result, caching: false });
        return result;
      })
      .catch(async (error) => {
        const cache = await caches.open(CACHE_NAME);
        const state = await readState(cache);
        state.error = error.message;
        state.finished = false;
        await maybeEnableOffline(cache, state);
        await writeState(cache, state);
        notifyClients({ type: "offline-error", ...state, caching: false, message: error.message });
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
  const state = await readState(cache);
  return {
    ...state,
    caching: Boolean(cacheSitePromise)
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

async function handleFetch(request, cache, state) {
  const useOfflineCache = state.enabled || state.phase !== "idle";

  if (!useOfflineCache) {
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
  const url = originUrl(event.request.url);
  if (event.request.method !== "GET" || !url) return;
  event.respondWith(
    caches.open(CACHE_NAME)
      .then(async (cache) => {
        const state = await readState(cache);
        return handleFetch(event.request, cache, state);
      })
  );
});

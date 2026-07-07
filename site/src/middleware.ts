import { readFile } from "node:fs/promises";
import path from "node:path";
import type { MiddlewareHandler } from "astro";

type ProxyMode = "full" | "api";

type DemoProxyConfig = {
  portEnv: string;
  defaultPort: string;
  mode: ProxyMode;
};

const DEMO_PROXIES: Record<string, DemoProxyConfig> = {
  "ch09-uad-coalition-board": {
    portEnv: "DEMO_BACKEND_PORT",
    defaultPort: "8766",
    mode: "full"
  },
  "ch01-scaffold-misuse": {
    portEnv: "SCAFFOLD_MISUSE_BACKEND_PORT",
    defaultPort: "8767",
    mode: "api"
  }
};

function routePath(pathname: string, base: string): string {
  if (!base || base === "/") return pathname;
  const prefix = base.endsWith("/") ? base.slice(0, -1) : base;
  if (pathname === prefix) return "/";
  if (pathname.startsWith(`${prefix}/`)) return pathname.slice(prefix.length);
  return pathname;
}

async function readPublicIndex(demoId: string): Promise<Response | null> {
  try {
    const html = await readFile(
      path.join(process.cwd(), "public", "chapter-demos", demoId, "index.html"),
      "utf8"
    );
    return new Response(html, {
      headers: { "Content-Type": "text/html; charset=utf-8" }
    });
  } catch {
    return null;
  }
}

async function proxyDemoBackend(
  request: Request,
  pathname: string,
  search: string,
  demoId: string,
  config: DemoProxyConfig
): Promise<Response | null> {
  const prefix = `/chapter-demos/${demoId}`;
  const port = process.env[config.portEnv] ?? config.defaultPort;
  const backendBase = `http://127.0.0.1:${port}`;

  let backendPath = "/";
  if (config.mode === "full") {
    if (!pathname.startsWith(prefix)) return null;
    backendPath = pathname.replace(prefix, "") || "/";
  } else {
    const apiPrefix = `${prefix}/api/`;
    if (!pathname.startsWith(apiPrefix)) return null;
    backendPath = pathname.slice(prefix.length) || "/";
  }

  const backendUrl = `${backendBase}${backendPath}${search}`;
  const headers = new Headers(request.headers);
  headers.delete("host");

  const init: RequestInit & { duplex?: "half" } = {
    method: request.method,
    headers
  };

  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = request.body;
    init.duplex = "half";
  }

  try {
    const res = await fetch(backendUrl, init);
    if (res.status !== 502 && res.status !== 503) return res;
  } catch {
    // backend unavailable
  }

  if (config.mode === "full" && backendPath === "/") {
    const fallback = await readPublicIndex(demoId);
    if (fallback) return fallback;
  }

  if (config.mode === "api" && backendPath === "/api/health") {
    return Response.json({ available: false, model: null, scenarios: [] });
  }

  return new Response(
    "Chapter demo backend unavailable. Run ./serve-site.sh or install demo requirements.",
    {
      status: 503,
      headers: { "Content-Type": "text/plain; charset=utf-8" }
    }
  );
}

export const onRequest: MiddlewareHandler = async (context, next) => {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  const pathname = routePath(context.url.pathname, base);
  const { search } = context.url;

  for (const [demoId, config] of Object.entries(DEMO_PROXIES)) {
    const prefix = `/chapter-demos/${demoId}`;
    const matches =
      config.mode === "full"
        ? pathname === prefix || pathname.startsWith(`${prefix}/`)
        : pathname.startsWith(`${prefix}/api/`);
    if (!matches) continue;
    const proxied = await proxyDemoBackend(context.request, pathname, search, demoId, config);
    if (proxied) return proxied;
  }

  const demoMatch = pathname.match(/^\/chapter-demos\/([^/]+)\/?$/);
  if (demoMatch) {
    const index = await readPublicIndex(demoMatch[1]);
    if (index) return index;
  }

  return next();
};

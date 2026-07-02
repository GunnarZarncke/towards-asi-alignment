import { readFile } from "node:fs/promises";
import path from "node:path";
import type { MiddlewareHandler } from "astro";

const CH09_ID = "ch09-uad-coalition-board";
const DEMO_BACKEND = `http://127.0.0.1:${process.env.DEMO_BACKEND_PORT ?? "8766"}`;

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

async function proxyCh09(request: Request, pathname: string, search: string): Promise<Response> {
  const backendPath = pathname.replace(`/chapter-demos/${CH09_ID}`, "") || "/";
  const backendUrl = `${DEMO_BACKEND}${backendPath}${search}`;

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

  if (backendPath === "/") {
    const fallback = await readPublicIndex(CH09_ID);
    if (fallback) return fallback;
  }

  return new Response("Chapter demo backend unavailable. Run ./serve-site.sh or install demo requirements.", {
    status: 503,
    headers: { "Content-Type": "text/plain; charset=utf-8" }
  });
}

export const onRequest: MiddlewareHandler = async (context, next) => {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  const pathname = routePath(context.url.pathname, base);
  const { search } = context.url;

  if (pathname === `/chapter-demos/${CH09_ID}` || pathname.startsWith(`/chapter-demos/${CH09_ID}/`)) {
    return proxyCh09(context.request, pathname, search);
  }

  const demoMatch = pathname.match(/^\/chapter-demos\/([^/]+)\/?$/);
  if (demoMatch) {
    const index = await readPublicIndex(demoMatch[1]);
    if (index) return index;
  }

  return next();
};

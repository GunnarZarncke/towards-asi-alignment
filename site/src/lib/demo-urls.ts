/** Demo row shape from sync-demos (subset used for link resolution). */
export type DemoLinkTarget = {
  sitePath: string;
  liveUrl?: string | null;
  requiresBackend?: boolean;
  optionalBackend?: boolean;
};

/**
 * Best URL for opening a demo in a new tab from the companion site.
 * Static demos stay on-site; backend/hybrid demos use the hosted Replit stack when configured.
 */
export function demoOpenHref(
  demo: DemoLinkTarget,
  withBase: (path: string) => string
): string {
  if (demo.liveUrl && (demo.requiresBackend || demo.optionalBackend)) {
    return demo.liveUrl;
  }
  return withBase(demo.sitePath);
}

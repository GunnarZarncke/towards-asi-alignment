const config =
  typeof window !== "undefined" ? window.__POSTHOG_CONFIG__ ?? {} : {};
const token = String(config.token || "").trim();
const host = String(config.host || "").trim();

/** @type {{ capture: (...args: unknown[]) => void; register: (...args: unknown[]) => void }} */
const disabled = { capture() {}, register() {} };

let demoSlug = "";
/** @type {Promise<typeof disabled> | null} */
let clientPromise = null;

function ensureClient() {
  if (typeof window === "undefined") {
    return Promise.resolve(disabled);
  }
  if (!token || !host) {
    if (config.isDevelopment) {
      console.warn("[posthog] PostHog not configured; demo analytics disabled.");
    }
    return Promise.resolve(disabled);
  }
  if (!clientPromise) {
    clientPromise = import("/vendor/posthog/module.js").then(({ default: posthog }) => {
      posthog.init(token, {
        api_host: host,
        person_profiles: "identified_only",
        capture_pageview: false,
        autocapture: false,
        disable_session_recording: true,
        capture_exceptions: {
          capture_unhandled_errors: true,
          capture_unhandled_rejections: true,
          capture_console_errors: false,
        },
      });
      return posthog;
    });
  }
  return clientPromise;
}

export async function initDemo(slug) {
  demoSlug = slug;
  const client = await ensureClient();
  client.register({ app: "chapter_demo", demo_slug: slug });
  client.capture("demo_loaded");
}

export function trackDemo(event, properties = {}) {
  void ensureClient().then((client) => {
    client.capture(event, { demo_slug: demoSlug, ...properties });
  });
}

export default disabled;

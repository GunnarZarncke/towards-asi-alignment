import posthog from '/vendor/posthog/module.js';

const config = window.__POSTHOG_CONFIG__ ?? {};
const token = String(config.token || '').trim();
const host = String(config.host || '').trim();

/** @type {{ capture: (...args: unknown[]) => void }} */
const disabled = { capture() {} };

if (!token || !host) {
  if (config.isDevelopment) {
    console.warn(
      '[posthog] POSTHOG_PROJECT_TOKEN and POSTHOG_HOST not set; game analytics disabled.',
    );
  }
} else {
  posthog.init(token, {
    api_host: host,
    person_profiles: 'identified_only',
    capture_pageview: false,
    autocapture: false,
    disable_session_recording: true,
    capture_exceptions: {
      capture_unhandled_errors: true,
      capture_unhandled_rejections: true,
      capture_console_errors: false,
    },
  });
}

export default token && host ? posthog : disabled;

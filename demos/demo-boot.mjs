import { initDemo } from "./posthog.js";

const parts = window.location.pathname.split("/").filter(Boolean);
const slug =
  parts.find((part) => /^(ch\d+|app[A-Za-z])/.test(part)) ?? "demos_index";
await initDemo(slug);

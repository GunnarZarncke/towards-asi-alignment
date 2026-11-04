import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeConceptLinkLogos from "./scripts/lib/rehype-concept-link-logos.mjs";
import cardRedirects from "./src/data/card-redirects.json";

const site = "https://towards-alignment.com";

const botOrientationPages = [
  `${site}/llms.txt`,
  `${site}/llms-full.txt`,
  `${site}/reviewing-for-agents.md`,
  `${site}/search-index.json`,
  `${site}/feed.xml`
];

export default defineConfig({
  site,
  trailingSlash: "always",
  redirects: {
    ...cardRedirects,
    "/demos/all/": "/demos/",
    "/predictions/assurance/": "/predictions/safety-case/"
  },
  integrations: [
    sitemap({
      // Illustration-prompt pages are unlisted and noindex; keep them out of
      // the sitemap too so they stay reachable only via the chapter link.
      filter: (page) => {
        if (page.includes("/illustrations/")) return false;
        // `/book/chNN/` and `/book/appX/` are noindex redirect stubs, not index targets.
        if (/\/book\/ch\d+\/?$/i.test(page) || /\/book\/app[a-z]\/?$/i.test(page)) return false;
        // Chapter/appendix full text is canonical on the hub URL except appendix M overview hub.
        if (/\/cards\/(chapter|appendix)\/[^/]+\/full\/?$/i.test(page) && !/\/cards\/appendix\/appm\/full\/?$/i.test(page)) {
          return false;
        }
        return true;
      },
      customPages: [`${site}/towards-superintelligence-alignment.pdf`, ...botOrientationPages]
    })
  ],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [
      [
        rehypeKatex,
        {
          strict: (errorCode) => (errorCode === "unknownSymbol" ? "ignore" : "warn"),
          macros: {
            "\\MI": "\\mathrm{I}",
            "\\Correctable": "\\mathcal{K}",
            "\\DL": "\\mathrm{DL}"
          }
        }
      ],
      rehypeConceptLinkLogos
    ]
  }
});

import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeConceptLinkLogos from "./scripts/lib/rehype-concept-link-logos.mjs";

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
  integrations: [
    sitemap({
      // Illustration-prompt pages are unlisted and noindex; keep them out of
      // the sitemap too so they stay reachable only via the chapter link.
      filter: (page) => !page.includes("/illustrations/"),
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

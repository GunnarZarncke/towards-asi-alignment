import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

const site = "https://towards-alignment.com";

const botOrientationPages = [
  `${site}/llms.txt`,
  `${site}/llms-full.txt`,
  `${site}/reviewing-for-agents.md`,
  `${site}/search-index.json`
];

export default defineConfig({
  site,
  trailingSlash: "always",
  integrations: [
    sitemap({
      customPages: [`${site}/towards-superintelligence-alignment.pdf`, ...botOrientationPages]
    })
  ],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [
      [
        rehypeKatex,
        {
          macros: {
            "\\MI": "\\mathrm{I}",
            "\\Correctable": "\\mathcal{K}",
            "\\DL": "\\mathrm{DL}"
          }
        }
      ]
    ]
  }
});

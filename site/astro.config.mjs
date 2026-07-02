import { defineConfig } from "astro/config";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

const siteBase = process.env.ASTRO_BASE ?? "/towards-asi-alignment";

export default defineConfig({
  site: "https://gunnarzarncke.github.io",
  base: siteBase,
  trailingSlash: "always",
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

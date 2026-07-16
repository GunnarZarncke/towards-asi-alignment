import { defineConfig } from "astro/config";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

export default defineConfig({
  site: "https://towards-alignment.com",
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

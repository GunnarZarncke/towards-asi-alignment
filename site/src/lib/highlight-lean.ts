import { createHighlighter, type Highlighter } from "shiki";

let highlighter: Highlighter | undefined;

async function getHighlighterInstance() {
  if (!highlighter) {
    highlighter = await createHighlighter({
      themes: ["github-light"],
      langs: ["lean4"]
    });
  }
  return highlighter;
}

export async function highlightLean(code: string) {
  const instance = await getHighlighterInstance();
  return instance.codeToHtml(code.trimEnd(), {
    lang: "lean4",
    theme: "github-light"
  });
}

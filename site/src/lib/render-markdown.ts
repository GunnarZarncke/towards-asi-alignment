import { createMarkdownProcessor } from "@astrojs/markdown-remark";

let processor: Awaited<ReturnType<typeof createMarkdownProcessor>> | null = null;

async function getProcessor() {
  if (!processor) {
    processor = await createMarkdownProcessor();
  }
  return processor;
}

export async function renderMarkdown(source: string): Promise<string> {
  const trimmed = source.trim();
  if (!trimmed) return "";
  const md = await getProcessor();
  const { code } = await md.render(trimmed);
  return code;
}

export async function renderMarkdownList(sources: string[]): Promise<string[]> {
  return Promise.all(sources.map((source) => renderMarkdown(source)));
}

interface FindingsDetailLine {
  kind?: string;
  numbers?: string;
  outcome?: string;
}

function labeledBlock(label: string, text?: string) {
  const trimmed = text?.trim();
  if (!trimmed) return "";
  return `**${label}.**\n\n${trimmed}`;
}

/** Body for /experiments/findings/{id}/ — verdict and stats, not experiment setup. */
export function experimentFindingsBodyMarkdown(line: FindingsDetailLine): string {
  if (line.kind !== "witness") {
    return "";
  }
  return [labeledBlock("Numbers", line.numbers), labeledBlock("Outcome", line.outcome)]
    .filter(Boolean)
    .join("\n\n");
}

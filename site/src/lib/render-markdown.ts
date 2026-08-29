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

interface WitnessDetailLine {
  kind?: string;
  role?: string;
  host?: string;
  setup?: string;
  analysis?: string;
  numbers?: string;
  outcome?: string;
}

function labeledBlock(label: string, text?: string) {
  const trimmed = text?.trim();
  if (!trimmed) return "";
  return `**${label}.**\n\n${trimmed}`;
}

export function witnessFindingsMarkdown(line: WitnessDetailLine): string {
  return [
    line.role?.trim(),
    labeledBlock("Host", line.host),
    labeledBlock("Setup", line.setup),
    labeledBlock("Analysis", line.analysis),
    labeledBlock("Numbers", line.numbers),
    labeledBlock("Outcome", line.outcome)
  ]
    .filter(Boolean)
    .join("\n\n");
}

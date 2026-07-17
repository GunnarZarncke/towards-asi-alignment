import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const card = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/cards" }),
  schema: z.object({
    title: z.string(),
    type: z.enum(["concept", "bridge", "objection", "artifact", "glossary", "chapter", "appendix", "frontmatter", "reference", "experiment", "release"]),
    status: z.enum(["established", "plausible", "framework", "bridge", "open", "negative", "reviewed"]).default("framework"),
    summary: z.string(),
    decision: z.string().optional(),
    evidence: z.string().optional(),
    bookPageId: z.string().optional(),
    overviewOnly: z.boolean().optional(),
    bibKey: z.string().optional(),
    experimentLineId: z.string().optional(),
    /** Optional link to a metadata/claims-ledger.md entry (e.g. "C-004a"). */
    claimId: z.string().optional(),
    /** ISO date (YYYY-MM-DD) for release cards; omit on the hub card. */
    releasedAt: z.string().optional(),
    /** Semver string for versioned release cards (e.g. "1.1.0"). */
    version: z.string().optional(),
    citedIn: z.array(z.string()).default([]),
    part: z.string().optional(),
    formalDensity: z.enum(["low", "medium", "high"]).optional(),
    bookChapters: z.array(z.string()).default([]),
    bookLabels: z.array(z.string()).default([]),
    bookSections: z.array(z.object({
      chapterId: z.string(),
      label: z.string()
    })).default([]),
    formulas: z.array(z.object({
      id: z.string(),
      latex: z.string(),
      explanation: z.string(),
      chapterId: z.string().optional()
    })).default([]),
    leanNodes: z.array(z.object({
      nodeId: z.string(),
      kind: z.enum(["proof", "counterexample", "bridge", "definition"]),
      summary: z.string(),
      module: z.string()
    })).default([]),
    evidenceNotes: z.array(z.object({
      source: z.string(),
      scenario: z.string().optional(),
      finding: z.enum(["support", "bound", "negative", "open"]),
      summary: z.string(),
      resultsPath: z.string()
    })).default([]),
    demos: z.array(z.object({
      demoId: z.string(),
      summary: z.string()
    })).default([]),
    related: z.array(z.string()).default([]),
    citeKeys: z.array(z.string()).default([]),
    external: z.array(z.object({
      label: z.string(),
      url: z.string()
    })).default([])
  })
});

const readingPathStep = z.object({
  kind: z.enum(["card", "demo", "experiment", "book", "lean"]),
  ref: z.string(),
  note: z.string().optional()
});

const readingPath = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/reading-paths" }),
  schema: z.object({
    title: z.string(),
    audience: z.string(),
    summary: z.string(),
    steps: z.array(readingPathStep),
    featuredLean: z.boolean().optional(),
    featuredWorkedExample: z.boolean().optional()
  })
});

const book = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/book" }),
  schema: z.object({
    id: z.string(),
    title: z.string(),
    kind: z.enum(["chapter", "frontmatter", "appendix"]),
    part: z.string().optional(),
    order: z.number(),
    sourceFile: z.string()
  })
});

export const collections = {
  cards: card,
  "reading-paths": readingPath,
  book
};

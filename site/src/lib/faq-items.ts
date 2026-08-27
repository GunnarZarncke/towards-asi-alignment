import type { CardType } from "./badges";
import type { PathId } from "./path-order";

export type FaqHref =
  | { kind: "route"; path: string }
  | { kind: "card"; id: string; type?: CardType }
  | { kind: "path"; id: PathId }
  | { kind: "pdf" }
  | { kind: "essay" }
  | { kind: "external"; url: string; indicator?: "github" | "external" };

export type FaqSegment = string | { label: string; href: FaqHref };

export type FaqItem = {
  question: string;
  answer: FaqSegment[];
};

export const FAQ_ITEMS: FaqItem[] = [
  {
    question: "Where should a new reader start?",
    answer: [
      "Read the short essays. They begin on ",
      { label: "Start Here", href: { kind: "route", path: "/start/" } },
      " — or open the ",
      { label: "first essay", href: { kind: "essay" } },
      " directly. If you already know your role, use the ",
      { label: "Guided Tour", href: { kind: "route", path: "/paths/" } },
      "."
    ]
  },
  {
    question: "What is this site?",
    answer: [
      "Orientation for the Towards Superintelligence Alignment project: short ",
      { label: "essays", href: { kind: "essay" } },
      ", ",
      { label: "knowledge cards", href: { kind: "route", path: "/cards/" } },
      ", a ",
      { label: "field map", href: { kind: "route", path: "/field/" } },
      ", ",
      { label: "experiments", href: { kind: "route", path: "/experiments/" } },
      ", ",
      { label: "Lean checks", href: { kind: "route", path: "/lean/" } },
      ", and the ",
      { label: "book PDF", href: { kind: "route", path: "/book/" } },
      "."
    ]
  },
  {
    question: "Is this a new knowledge platform?",
    answer: [
      "No. It is an authored reference layer for one framework. Discussion and contributions can happen elsewhere."
    ]
  },
  {
    question: "Does this project claim alignment is solved?",
    answer: [
      "No. It offers a framework and a conditional dependency spine, not a certificate that current systems are safe. See ",
      {
        label: "what we are not claiming",
        href: { kind: "card", id: "what-not-claiming", type: "objection" }
      },
      "."
    ]
  },
  {
    question: "What is the central thesis?",
    answer: [
      "Alignment means preserving grounded, human-correctable value-bearing processes across capability growth, ontology shift, successor creation, and selection pressure — while civilization can still correct."
    ]
  },
  {
    question: "What are the six thesis claims?",
    answer: [
      "The Introduction's reader contract: boundary, value-bundle, grounding, correction, successor, and basin. Chapter 48 revisits them with status labels and open gaps; it does not treat them as discharged. See the ",
      {
        label: "six thesis claims hub",
        href: { kind: "card", id: "six-thesis-claims", type: "concept" }
      },
      "."
    ]
  },
  {
    question: "What is correction-channel integrity?",
    answer: [
      "The condition that legitimate human correction still causally changes future system behavior before irreversible damage. See the ",
      {
        label: "correction-channel integrity",
        href: { kind: "card", id: "correction-channel-integrity", type: "concept" }
      },
      " card."
    ]
  },
  {
    question: "What is a value bundle?",
    answer: [
      "A compressed direction of control that changes behavior across contexts. The framework cares whether this structure survives transformation — not whether the slogans stay the same. See ",
      {
        label: "value-bundle transport",
        href: { kind: "card", id: "value-bundle-transport", type: "concept" }
      },
      "."
    ]
  },
  {
    question: "Why start with boundary discovery?",
    answer: [
      "Because the deployed actor may be a loop of model, memory, tools, dashboards, and people. Auditing only the model can miss the real controller. See ",
      {
        label: "boundary discovery",
        href: { kind: "card", id: "boundary-discovery", type: "concept" }
      },
      "."
    ]
  },
  {
    question: "Does Lean prove alignment?",
    answer: [
      "No. The ",
      { label: "Lean dependency spine", href: { kind: "route", path: "/lean/" } },
      " checks conditional structure. It does not prove that real systems satisfy the bridge assumptions."
    ]
  },
  {
    question: "Do the experiments validate the thesis?",
    answer: [
      "No. They are methodology-building and sanity checks. Negative results bound what the manuscript may claim. The ",
      { label: "Experiments page", href: { kind: "route", path: "/experiments/" } },
      " lists the in-repo lines; ",
      { label: "coverage", href: { kind: "route", path: "/experiments/coverage/" } },
      " and ",
      {
        label: "negative results",
        href: { kind: "card", id: "negative-results", type: "concept" }
      },
      " sit next to them. Narrative prose is in ",
      {
        label: "docs/EXPERIMENTS.md",
        href: {
          kind: "external",
          url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/docs/EXPERIMENTS.md",
          indicator: "github"
        }
      },
      "."
    ]
  },
  {
    question: "Where should safety engineers start?",
    answer: [
      "Use the ",
      { label: "Engineer / evals path", href: { kind: "path", id: "engineer-evals" } },
      ", then read ",
      {
        label: "correction-channel integrity",
        href: { kind: "card", id: "correction-channel-integrity", type: "concept" }
      },
      " and the ",
      {
        label: "deployment-gate",
        href: { kind: "card", id: "deployment-gate", type: "artifact" }
      },
      " card."
    ]
  },
  {
    question: "Where should policy readers start?",
    answer: [
      "Use the ",
      { label: "Funder / policy path", href: { kind: "path", id: "funder-policy" } },
      ". It emphasizes decision triggers, scope assumptions, artifacts, and uncertainty. Appendix C is the ",
      {
        label: "institutional translation",
        href: { kind: "card", id: "chapters/appC", type: "appendix" }
      },
      " entry."
    ]
  },
  {
    question: "What is the Field page?",
    answer: [
      "A map of who in alignment research works on which problems, relative to this project's bridges. Start at ",
      { label: "Field", href: { kind: "route", path: "/field/" } },
      ". The ",
      { label: "longer briefing", href: { kind: "route", path: "/field/v2/" } },
      " is one click further."
    ]
  },
  {
    question: "Where is the full book?",
    answer: [
      "The PDF is bundled with this site — ",
      { label: "Download PDF", href: { kind: "pdf" } },
      " from the ",
      { label: "book page", href: { kind: "route", path: "/book/" } },
      " or ",
      { label: "Start Here", href: { kind: "route", path: "/start/" } },
      ". The book page lists contents in PDF order. It opens in the browser without GitHub login."
    ]
  },
  {
    question: "What is the quiz?",
    answer: [
      "A field-knowledge quiz. Select all that apply; get immediate feedback. After enough answers, it names ",
      { label: "which researcher knows most about what you already know", href: { kind: "route", path: "/quiz/" } },
      " — coverage, not agreement."
    ]
  },
  {
    question: "Will there be translations?",
    answer: [
      "Not yet. English is the working language of the book and this site. Other-language editions are not in progress."
    ]
  }
];

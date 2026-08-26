export type FaqItem = {
  question: string;
  answer: string;
};

export const FAQ_ITEMS: FaqItem[] = [
  {
    question: "What is this site?",
    answer:
      "A site for the book Towards Superintelligence Alignment. It helps you find the core ideas, pick a reading path, and open the PDF."
  },
  {
    question: "Is this a new knowledge platform?",
    answer: "No. It is an authored reference layer for one framework. Discussion and contributions can happen elsewhere."
  },
  {
    question: "What is the central thesis?",
    answer:
      "Alignment means preserving human-correctable value-bearing processes across capability growth, ontology shift, successor creation, and selection pressure."
  },
  {
    question: "What are the six thesis claims?",
    answer:
      "The Introduction's reader contract: boundary, value-bundle, grounding, correction, successor, and basin/selection."
  },
  {
    question: "What is correction-channel integrity?",
    answer:
      "It is the condition that legitimate human correction still causally changes future system behavior before irreversible damage."
  },
  {
    question: "What is a value bundle?",
    answer:
      "A compressed direction of control that changes behavior across contexts. The framework cares whether this structure survives transformation."
  },
  {
    question: "Why start with boundary discovery?",
    answer:
      "Because the deployed actor may be a loop of model, memory, tools, dashboards, and people. Auditing only the model can miss the real controller."
  },
  {
    question: "Does Lean prove alignment?",
    answer: "No. Lean checks conditional structure. It does not prove that real systems satisfy the bridge assumptions."
  },
  {
    question: "Do the experiments validate the thesis?",
    answer:
      "No. They are methodology-building and sanity checks. Negative results bound what the manuscript may claim."
  },
  {
    question: "Where are the experiment lines documented?",
    answer: "experiments"
  },
  {
    question: "Where should safety engineers start?",
    answer: "Use the engineer/evals path, then read the correction-channel integrity and deployment-gate cards."
  },
  {
    question: "Where should policy readers start?",
    answer: "Use the funder/policy path. It emphasizes decision triggers, scope assumptions, artifacts, and uncertainty."
  },
  {
    question: "Where is the full book?",
    answer: "book"
  },
  {
    question: "Will there be translations?",
    answer: "Later, after the English card structure stabilizes."
  }
];

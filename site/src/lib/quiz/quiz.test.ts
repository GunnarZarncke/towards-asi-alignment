import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { rankResearchers, researcherFit } from "./fit.ts";
import { pickNextQuestion } from "./pick.ts";
import { scoreQuestion, summarizeProgress } from "./score.ts";
import {
  afterPlayerAnswer,
  canStartRetake,
  questionStatus,
  startRetakeSession
} from "./status.ts";
import { emptyQuizState, parseQuizState, recordAttempt } from "./storage.ts";
import { shuffledOptions } from "./ui.ts";
import { BRIDGE_IDS, type BridgeId, type QuizQuestion, type QuizResearcher } from "./types.ts";

const sampleQuestions: QuizQuestion[] = [
  {
    id: "wiener-coupled-agencies",
    prompt: "Who first wrote the Wiener quote?",
    options: [
      { id: "wiener", text: "Norbert Wiener", correct: true },
      { id: "turing", text: "Alan Turing", correct: false },
      { id: "shannon", text: "Claude Shannon", correct: false }
    ],
    explanation: "Norbert Wiener, Science (1960).",
    source: { href: "/cards/chapter/ch01/", label: "Chapter 1" },
    topics: ["MB1"]
  },
  {
    id: "embedded-agency-lead-author",
    prompt: "Lead author of Embedded Agency?",
    options: [
      { id: "garrabrant", text: "Scott Garrabrant", correct: true },
      { id: "russell", text: "Stuart Russell", correct: false }
    ],
    explanation: "Scott Garrabrant.",
    source: { href: "/cards/chapter/ch01/", label: "Chapter 1" },
    topics: ["MB1"]
  }
];

const researchers: QuizResearcher[] = [
  {
    id: "garrabrant",
    name: "Scott Garrabrant",
    live: true,
    blurb: "Embedded Agency.",
    expertise: { MB1: 3, MB2: 1 }
  },
  {
    id: "soares",
    name: "Nate Soares",
    live: true,
    blurb: "Corrigibility.",
    expertise: { MB4: 3, MB1: 2 }
  },
  {
    id: "yudkowsky",
    name: "Eliezer Yudkowsky",
    live: true,
    blurb: "CEV.",
    expertise: { MB8: 3, MB1: 2 }
  },
  {
    id: "hubinger",
    name: "Evan Hubinger",
    live: true,
    blurb: "Inner alignment.",
    expertise: { MB7: 3, MB7c: 3, MB1: 1 }
  }
];

function vectorForBridge(id: BridgeId, value = 1) {
  return Object.fromEntries(BRIDGE_IDS.map((bridge) => [bridge, bridge === id ? value : 0])) as Record<
    BridgeId,
    number
  >;
}

describe("shuffledOptions", () => {
  it("returns a permutation of the input", () => {
    const input = ["a", "b", "c", "d"];
    const shuffled = shuffledOptions(input, () => 0);
    assert.deepEqual([...shuffled].sort(), input);
    assert.notDeepEqual(shuffled, input);
  });
});

describe("scoreQuestion", () => {
  it("scores each option as a true/false item", () => {
    const question = sampleQuestions[0];
    const result = scoreQuestion(question, ["wiener"]);
    assert.equal(result.exact, true);
    assert.equal(result.earned, 3);
    assert.equal(result.max, 3);
  });

  it("allows zero correct selections", () => {
    const question = sampleQuestions[0];
    const result = scoreQuestion(question, []);
    assert.equal(result.exact, false);
    assert.equal(result.earned, 2);
  });
});

describe("pickNextQuestion", () => {
  it("prefers bridges with fewer than two answers", () => {
    const [first, second] = sampleQuestions;
    const state = recordAttempt(emptyQuizState(), first.id, {
      selected: ["wiener"],
      exact: true,
      earned: 3,
      max: 3
    });
    const next = pickNextQuestion(sampleQuestions, state, () => 0);
    assert.equal(next?.id, second.id);
    const skipped = pickNextQuestion(sampleQuestions, emptyQuizState(), () => 0, [first.id]);
    assert.equal(skipped?.id, second.id);
  });

  it("includes retakeable questions during a retake session", () => {
    let state = emptyQuizState();
    for (const question of sampleQuestions) {
      const correct = question.options.filter((option) => option.correct).map((option) => option.id);
      const score = scoreQuestion(question, correct);
      state = recordAttempt(state, question.id, { selected: correct, ...score });
    }
    assert.equal(pickNextQuestion(sampleQuestions, state), null);
    state = startRetakeSession(state);
    assert.equal(questionStatus(state, sampleQuestions[0].id), "retakeable");
    const next = pickNextQuestion(sampleQuestions, state, () => 0);
    assert.equal(next?.id, sampleQuestions[0].id);
  });
});

describe("retake session", () => {
  it("keeps attempts when starting retake", () => {
    let state = recordAttempt(emptyQuizState(), sampleQuestions[0].id, {
      selected: ["wiener"],
      exact: true,
      earned: 3,
      max: 3
    });
    state = startRetakeSession(state);
    assert.equal(state.attempts[sampleQuestions[0].id]?.selected[0], "wiener");
    assert.equal(state.retakeSession, 1);
    assert.deepEqual(state.retakeCompleted, []);
  });

  it("preserves retake session when recording a new attempt", () => {
    let state = recordAttempt(emptyQuizState(), sampleQuestions[0].id, {
      selected: ["wiener"],
      exact: true,
      earned: 3,
      max: 3
    });
    state = startRetakeSession(state);
    state = recordAttempt(state, sampleQuestions[0].id, {
      selected: ["turing"],
      exact: false,
      earned: 2,
      max: 3
    });
    assert.equal(state.retakeSession, 1);
    assert.deepEqual(state.retakeCompleted, []);
  });

  it("marks a question answered again and ends session when done", () => {
    let state = emptyQuizState();
    for (const question of sampleQuestions) {
      const correct = question.options.filter((option) => option.correct).map((option) => option.id);
      state = recordAttempt(state, question.id, { selected: correct, ...scoreQuestion(question, correct) });
    }
    state = startRetakeSession(state);
    state = recordAttempt(state, sampleQuestions[0].id, {
      selected: ["turing"],
      exact: false,
      earned: 2,
      max: 3
    });
    state = afterPlayerAnswer(state, sampleQuestions[0].id, sampleQuestions);
    assert.equal(questionStatus(state, sampleQuestions[0].id), "answered");
    assert.equal(state.attempts[sampleQuestions[0].id]?.selected[0], "turing");
    assert.equal(questionStatus(state, sampleQuestions[1].id), "retakeable");

    state = recordAttempt(state, sampleQuestions[1].id, {
      selected: ["garrabrant"],
      exact: true,
      earned: 2,
      max: 2
    });
    state = afterPlayerAnswer(state, sampleQuestions[1].id, sampleQuestions);
    assert.equal(state.retakeSession, undefined);
    assert.equal(canStartRetake(state), true);
  });
});

describe("researcher fit", () => {
  it("matches Garrabrant on pure MB1", () => {
    const ranked = rankResearchers(researchers, vectorForBridge("MB1"));
    assert.equal(ranked[0]?.researcher.id, "garrabrant");
  });

  it("matches Soares on pure MB4", () => {
    const ranked = rankResearchers(researchers, vectorForBridge("MB4"));
    assert.equal(ranked[0]?.researcher.id, "soares");
  });

  it("matches Yudkowsky on pure MB8", () => {
    const ranked = rankResearchers(researchers, vectorForBridge("MB8"));
    assert.equal(ranked[0]?.researcher.id, "yudkowsky");
  });

  it("matches Hubinger when MB7 and MB7c are both strong", () => {
    const vector = vectorForBridge("MB1", 0);
    vector.MB7 = 1;
    vector.MB7c = 1;
    const ranked = rankResearchers(researchers, vector);
    assert.equal(ranked[0]?.researcher.id, "hubinger");
  });
});

describe("summarizeProgress", () => {
  it("locks the result until every bridge has two answers", () => {
    let state = emptyQuizState();
    for (const question of sampleQuestions) {
      const correct = question.options.filter((option) => option.correct).map((option) => option.id);
      const score = scoreQuestion(question, correct);
      state = recordAttempt(state, question.id, { selected: correct, ...score });
    }
    const summary = summarizeProgress(sampleQuestions, state);
    assert.equal(summary.resultUnlocked, false);
    assert.equal(summary.topicsCovered, 1);
  });
});

describe("parseQuizState", () => {
  it("returns empty state for invalid JSON", () => {
    assert.deepEqual(parseQuizState("{"), emptyQuizState());
  });
});

describe("researcherFit", () => {
  it("sums user vector times expertise", () => {
    const garrabrant = researchers.find((researcher) => researcher.id === "garrabrant")!;
    const fit = researcherFit(garrabrant, vectorForBridge("MB1"));
    assert.equal(fit, 3);
  });
});

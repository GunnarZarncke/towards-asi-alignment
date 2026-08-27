import type { QuizProgressState, QuizQuestion } from "./types.ts";

export type QuestionStatus = "unanswered" | "answered" | "retakeable";

export function questionStatus(state: QuizProgressState, questionId: string): QuestionStatus {
  if (!state.attempts[questionId]) return "unanswered";
  if (!state.retakeSession) return "answered";
  if (state.retakeCompleted?.includes(questionId)) return "answered";
  return "retakeable";
}

export function isRetakeActive(state: QuizProgressState): boolean {
  return typeof state.retakeSession === "number" && state.retakeSession > 0;
}

export function hasRetakeableQuestions(
  questions: QuizQuestion[],
  state: QuizProgressState
): boolean {
  return questions.some((question) => questionStatus(state, question.id) === "retakeable");
}

export function playerEligibleQuestions(
  questions: QuizQuestion[],
  state: QuizProgressState
): QuizQuestion[] {
  return questions.filter((question) => {
    const status = questionStatus(state, question.id);
    return status === "unanswered" || status === "retakeable";
  });
}

export function startRetakeSession(state: QuizProgressState): QuizProgressState {
  const answeredCount = Object.keys(state.attempts).length;
  if (answeredCount === 0) return state;
  return {
    ...state,
    retakeSession: (state.retakeSession ?? 0) + 1,
    retakeCompleted: []
  };
}

export function afterPlayerAnswer(
  state: QuizProgressState,
  questionId: string,
  questions: QuizQuestion[]
): QuizProgressState {
  if (!isRetakeActive(state)) return state;

  const retakeCompleted = [...(state.retakeCompleted ?? []), questionId];
  let next: QuizProgressState = { ...state, retakeCompleted };
  if (!hasRetakeableQuestions(questions, next)) {
    next = { ...next, retakeSession: undefined, retakeCompleted: undefined };
  }
  return next;
}

export function canStartRetake(state: QuizProgressState): boolean {
  return Object.keys(state.attempts).length > 0 && !isRetakeActive(state);
}

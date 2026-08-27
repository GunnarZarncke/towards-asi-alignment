import { QUIZ_STORAGE_KEY, type QuizAttempt, type QuizProgressState } from "./types.ts";

export function emptyQuizState(): QuizProgressState {
  return { v: 1, attempts: {} };
}

export function parseQuizState(raw: string | null): QuizProgressState {
  if (!raw) return emptyQuizState();
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (!parsed || typeof parsed !== "object") return emptyQuizState();
    const row = parsed as QuizProgressState;
    if (row.v !== 1 || !row.attempts || typeof row.attempts !== "object") {
      return emptyQuizState();
    }
    const attempts: Record<string, QuizAttempt> = {};
    for (const [id, attempt] of Object.entries(row.attempts)) {
      if (!attempt || typeof attempt !== "object") continue;
      const a = attempt as QuizAttempt;
      if (
        !Array.isArray(a.selected) ||
        typeof a.exact !== "boolean" ||
        typeof a.earned !== "number" ||
        typeof a.max !== "number" ||
        typeof a.t !== "number"
      ) {
        continue;
      }
      attempts[id] = {
        selected: a.selected.filter((item): item is string => typeof item === "string"),
        exact: a.exact,
        earned: a.earned,
        max: a.max,
        t: a.t
      };
    }
    const retakeSession =
      typeof row.retakeSession === "number" && row.retakeSession > 0 ? row.retakeSession : undefined;
    const retakeCompleted = Array.isArray(row.retakeCompleted)
      ? row.retakeCompleted.filter((item): item is string => typeof item === "string")
      : undefined;
    return { v: 1, attempts, retakeSession, retakeCompleted };
  } catch {
    return emptyQuizState();
  }
}

export function loadQuizState(): QuizProgressState {
  if (typeof localStorage === "undefined") return emptyQuizState();
  try {
    return parseQuizState(localStorage.getItem(QUIZ_STORAGE_KEY));
  } catch {
    return emptyQuizState();
  }
}

export function saveQuizState(state: QuizProgressState): void {
  if (typeof localStorage === "undefined") return;
  try {
    localStorage.setItem(QUIZ_STORAGE_KEY, JSON.stringify(state));
  } catch {
    // private mode / quota
  }
}

export function recordAttempt(
  state: QuizProgressState,
  questionId: string,
  attempt: Omit<QuizAttempt, "t"> & { t?: number }
): QuizProgressState {
  return {
    ...state,
    v: 1,
    attempts: {
      ...state.attempts,
      [questionId]: { ...attempt, t: attempt.t ?? Date.now() }
    }
  };
}

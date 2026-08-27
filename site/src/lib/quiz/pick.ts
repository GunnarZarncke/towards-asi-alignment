import { MIN_ANSWERS_PER_TOPIC, type BridgeId, type QuizProgressState, type QuizQuestion } from "./types.ts";
import { playerEligibleQuestions } from "./status.ts";
import { primaryTopic, topicAnswerCounts } from "./score.ts";

export function pickNextQuestion(
  questions: QuizQuestion[],
  state: QuizProgressState,
  random: () => number = Math.random,
  excludeIds: readonly string[] = []
): QuizQuestion | null {
  const remaining = playerEligibleQuestions(questions, state).filter(
    (question) => !excludeIds.includes(question.id)
  );
  const poolSource =
    remaining.length > 0 ? remaining : playerEligibleQuestions(questions, state);
  if (poolSource.length === 0) return null;

  const counts = topicAnswerCounts(questions, state.attempts);
  const underCovered = poolSource.filter(
    (question) => counts[primaryTopic(question)] < MIN_ANSWERS_PER_TOPIC
  );
  const pool = underCovered.length > 0 ? underCovered : poolSource;
  const index = Math.floor(random() * pool.length);
  return pool[index] ?? null;
}

export function bridgesNeedingAnswers(
  questions: QuizQuestion[],
  state: QuizProgressState
): BridgeId[] {
  const counts = topicAnswerCounts(questions, state.attempts);
  return (Object.entries(counts) as [BridgeId, number][])
    .filter(([, count]) => count < MIN_ANSWERS_PER_TOPIC)
    .map(([id]) => id);
}

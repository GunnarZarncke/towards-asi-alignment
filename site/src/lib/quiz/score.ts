import {
  BRIDGE_IDS,
  MIN_ANSWERS_PER_TOPIC,
  type BridgeId,
  type QuestionScore,
  type QuizAttempt,
  type QuizProgressState,
  type QuizProgressSummary,
  type QuizQuestion
} from "./types.ts";

export function primaryTopic(question: QuizQuestion): BridgeId {
  const topic = question.topics[0];
  if (!topic) {
    throw new Error(`Question ${question.id} has no topics`);
  }
  return topic;
}

export function scoreQuestion(question: QuizQuestion, selected: string[]): QuestionScore {
  const selectedSet = new Set(selected);
  let earned = 0;
  for (const option of question.options) {
    const marked = selectedSet.has(option.id);
    if (marked === option.correct) earned++;
  }
  const correctIds = question.options.filter((option) => option.correct).map((option) => option.id);
  const exact =
    selectedSet.size === correctIds.length && correctIds.every((id) => selectedSet.has(id));
  return { exact, earned, max: question.options.length };
}

export function topicAnswerCounts(
  questions: QuizQuestion[],
  attempts: Record<string, QuizAttempt>
): Record<BridgeId, number> {
  const counts = Object.fromEntries(BRIDGE_IDS.map((id) => [id, 0])) as Record<BridgeId, number>;
  for (const question of questions) {
    if (!attempts[question.id]) continue;
    counts[primaryTopic(question)]++;
  }
  return counts;
}

export function summarizeProgress(
  questions: QuizQuestion[],
  state: QuizProgressState
): QuizProgressSummary {
  const attempts = state.attempts;
  const answered = questions.filter((question) => attempts[question.id]).length;
  const total = questions.length;
  let scoreEarned = 0;
  let scoreMax = 0;
  let exactCount = 0;
  for (const question of questions) {
    const attempt = attempts[question.id];
    if (!attempt) continue;
    scoreEarned += attempt.earned;
    scoreMax += attempt.max;
    if (attempt.exact) exactCount++;
  }
  const topicCounts = topicAnswerCounts(questions, attempts);
  const topicsCovered = BRIDGE_IDS.filter((id) => topicCounts[id] >= MIN_ANSWERS_PER_TOPIC).length;
  return {
    answered,
    total,
    percentComplete: total === 0 ? 0 : Math.round((answered / total) * 100),
    scoreEarned,
    scoreMax,
    exactCount,
    topicsCovered,
    topicTotal: BRIDGE_IDS.length,
    resultUnlocked: topicsCovered >= BRIDGE_IDS.length
  };
}

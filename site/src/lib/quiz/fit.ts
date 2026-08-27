import {
  BRIDGE_IDS,
  type BridgeId,
  type QuizAttempt,
  type QuizQuestion,
  type QuizResearcher,
  type ResearcherRank
} from "./types.ts";
import { primaryTopic } from "./score.ts";

export type UserBridgeVector = Record<BridgeId, number>;

export function topicTotals(
  questions: QuizQuestion[],
  attempts: Record<string, QuizAttempt>
): Record<BridgeId, { earned: number; max: number }> {
  const totals = Object.fromEntries(
    BRIDGE_IDS.map((id) => [id, { earned: 0, max: 0 }])
  ) as Record<BridgeId, { earned: number; max: number }>;

  for (const question of questions) {
    const attempt = attempts[question.id];
    if (!attempt) continue;
    const topic = primaryTopic(question);
    totals[topic].earned += attempt.earned;
    totals[topic].max += attempt.max;
  }
  return totals;
}

export function userBridgeVector(
  questions: QuizQuestion[],
  attempts: Record<string, QuizAttempt>
): UserBridgeVector {
  const totals = topicTotals(questions, attempts);
  return Object.fromEntries(
    BRIDGE_IDS.map((id) => {
      const row = totals[id];
      return [id, row.max === 0 ? 0 : row.earned / row.max];
    })
  ) as UserBridgeVector;
}

export function strongestBridge(vector: UserBridgeVector): BridgeId {
  let best: BridgeId = "MB1";
  let bestValue = -1;
  for (const id of BRIDGE_IDS) {
    if (vector[id] > bestValue) {
      bestValue = vector[id];
      best = id;
    }
  }
  return best;
}

export function researcherFit(researcher: QuizResearcher, vector: UserBridgeVector): number {
  let sum = 0;
  for (const id of BRIDGE_IDS) {
    const level = researcher.expertise[id] ?? 0;
    sum += vector[id] * level;
  }
  return sum;
}

export function rankResearchers(
  researchers: QuizResearcher[],
  vector: UserBridgeVector
): ResearcherRank[] {
  const live = researchers.filter((researcher) => researcher.live);
  const peak = strongestBridge(vector);
  return live
    .map((researcher) => ({ researcher, fit: researcherFit(researcher, vector) }))
    .sort((a, b) => {
      if (b.fit !== a.fit) return b.fit - a.fit;
      const aPeak = a.researcher.expertise[peak] ?? 0;
      const bPeak = b.researcher.expertise[peak] ?? 0;
      if (bPeak !== aPeak) return bPeak - aPeak;
      return a.researcher.name.localeCompare(b.researcher.name);
    });
}

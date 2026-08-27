import { MIN_ANSWERS_PER_TOPIC, type QuizBank, type QuizQuestion, type QuizResearcher, type QuizTopic } from "./types.ts";

export type QuizClientPayload = {
  questions: QuizQuestion[];
  topics: QuizTopic[];
  researchers: QuizResearcher[];
  minAnswersPerTopic: number;
};

export function quizClientPayload(bank: QuizBank): QuizClientPayload {
  return {
    questions: bank.questions,
    topics: bank.topics,
    researchers: bank.researchers,
    minAnswersPerTopic: MIN_ANSWERS_PER_TOPIC
  };
}

export function withBase(base: string, path: string): string {
  const prefix = base.endsWith("/") ? base : `${base}/`;
  return `${prefix}${path.replace(/^\/+/, "")}`;
}

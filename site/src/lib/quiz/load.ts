import yaml from "js-yaml";
import { BRIDGE_IDS, type BridgeId, type QuizBank, type QuizQuestion, type QuizResearcher, type QuizTopic } from "./types";

import questionsRaw from "../../content/quiz/questions.yml?raw";
import topicsRaw from "../../content/quiz/topics.yml?raw";
import researchersRaw from "../../content/quiz/researchers.yml?raw";

function assertBridgeId(id: string): BridgeId {
  if (!(BRIDGE_IDS as readonly string[]).includes(id)) {
    throw new Error(`Unknown bridge topic: ${id}`);
  }
  return id as BridgeId;
}

function parseQuestions(raw: string): QuizQuestion[] {
  const data = yaml.load(raw) as { questions?: QuizQuestion[] };
  const questions = data.questions ?? [];
  for (const question of questions) {
    if (!question.id || !question.prompt || !question.options?.length) {
      throw new Error(`Invalid quiz question: ${question.id ?? "(missing id)"}`);
    }
    question.topics = question.topics.map(assertBridgeId);
  }
  return questions;
}

function parseTopics(raw: string): QuizTopic[] {
  const data = yaml.load(raw) as { topics?: QuizTopic[] };
  const topics = data.topics ?? [];
  for (const topic of topics) {
    assertBridgeId(topic.id);
  }
  return topics;
}

function parseResearchers(raw: string): QuizResearcher[] {
  const data = yaml.load(raw) as { researchers?: QuizResearcher[] };
  return data.researchers ?? [];
}

let cached: QuizBank | null = null;

export function loadQuizBank(): QuizBank {
  if (cached) return cached;
  cached = {
    questions: parseQuestions(questionsRaw),
    topics: parseTopics(topicsRaw),
    researchers: parseResearchers(researchersRaw)
  };
  return cached;
}

export function questionsForAppearOn(bank: QuizBank, appearOn: string): QuizQuestion[] {
  return bank.questions.filter((question) => question.appearOn?.includes(appearOn));
}

export function topicTitle(bank: QuizBank, id: BridgeId): string {
  return bank.topics.find((topic) => topic.id === id)?.title ?? id;
}

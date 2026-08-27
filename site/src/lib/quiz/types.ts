export const BRIDGE_IDS = [
  "MB1",
  "MB2",
  "MB3",
  "MB4",
  "MB4a",
  "MB5",
  "MB6",
  "MB7",
  "MB7a",
  "MB7b",
  "MB7c",
  "MB7d",
  "MB8",
  "MB9",
  "MB10",
  "MB11"
] as const;

export type BridgeId = (typeof BRIDGE_IDS)[number];

/** Answers per bridge before the researcher result unlocks. Drop to 1 if feedback says 32 is too long. */
export const MIN_ANSWERS_PER_TOPIC = 2;

export type QuizOption = {
  id: string;
  text: string;
  correct: boolean;
};

export type QuizSource = {
  href: string;
  label: string;
};

export type QuizQuestion = {
  id: string;
  prompt: string;
  options: QuizOption[];
  explanation: string;
  source: QuizSource;
  topics: BridgeId[];
  appearOn?: string[];
  tags?: string[];
};

export type QuizTopic = {
  id: BridgeId;
  title: string;
  short?: string;
};

export type ResearcherExpertise = Partial<Record<BridgeId, number>>;

export type QuizResearcher = {
  id: string;
  name: string;
  agendas?: string[];
  live: boolean;
  blurb: string;
  expertise: ResearcherExpertise;
};

export type QuizAttempt = {
  selected: string[];
  exact: boolean;
  earned: number;
  max: number;
  t: number;
};

export type QuizProgressState = {
  v: 1;
  attempts: Record<string, QuizAttempt>;
  /** Incremented when the user starts a retake-all pass on /quiz/. */
  retakeSession?: number;
  /** Question ids re-checked during the current retake session. */
  retakeCompleted?: string[];
};

export type QuestionScore = {
  exact: boolean;
  earned: number;
  max: number;
};

export type QuizProgressSummary = {
  answered: number;
  total: number;
  percentComplete: number;
  scoreEarned: number;
  scoreMax: number;
  exactCount: number;
  topicsCovered: number;
  topicTotal: number;
  resultUnlocked: boolean;
};

export type ResearcherRank = {
  researcher: QuizResearcher;
  fit: number;
};

export type QuizBank = {
  questions: QuizQuestion[];
  topics: QuizTopic[];
  researchers: QuizResearcher[];
};

export const QUIZ_STORAGE_KEY = "tsa-quiz-v1";

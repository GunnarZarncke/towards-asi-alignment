import { type QuizAttempt, type QuizQuestion } from "./types.ts";
import { rankResearchers, userBridgeVector } from "./fit.ts";
import { pickNextQuestion } from "./pick.ts";
import { scoreQuestion, summarizeProgress } from "./score.ts";
import {
  afterPlayerAnswer,
  canStartRetake,
  isRetakeActive,
  playerEligibleQuestions,
  questionStatus,
  startRetakeSession
} from "./status.ts";
import { loadQuizState, recordAttempt, saveQuizState } from "./storage.ts";
import type { QuizClientPayload } from "./client-payload.ts";
import { withBase } from "./client-payload.ts";

export type QuizUiOptions = {
  base: string;
  payload: QuizClientPayload;
  mode: "player" | "block";
  appearOn?: string;
};

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function selectedFromRoot(root: HTMLElement): string[] {
  return [...root.querySelectorAll<HTMLInputElement>('input[type="checkbox"]:checked')].map(
    (input) => input.value
  );
}

export function shuffledOptions<T>(
  options: readonly T[],
  random: () => number = Math.random
): T[] {
  const copy = [...options];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function optionOrderFromSlot(
  slot: HTMLElement,
  question: QuizQuestion
): QuizQuestion["options"] {
  const ids = [...slot.querySelectorAll<HTMLInputElement>(".quiz-options input")].map(
    (input) => input.value
  );
  return ids
    .map((id) => question.options.find((option) => option.id === id))
    .filter((option): option is QuizQuestion["options"][number] => !!option);
}

function renderRetakeControls(root: HTMLElement, payload: QuizClientPayload): void {
  const state = loadQuizState();
  const retakeBtn = root.querySelector<HTMLButtonElement>("[data-quiz-retake]");
  const retakeNote = root.querySelector<HTMLElement>("[data-quiz-retake-note]");
  const canRetake = canStartRetake(state);
  const retakeActive = isRetakeActive(state);
  const remaining = playerEligibleQuestions(payload.questions, state).length;

  if (retakeBtn) {
    retakeBtn.hidden = !canRetake;
    retakeBtn.disabled = false;
  }
  if (retakeNote) {
    if (retakeActive) {
      retakeNote.hidden = false;
      retakeNote.textContent = `${remaining} question${remaining === 1 ? "" : "s"} left in this retake. Saved scores update when you check each answer.`;
    } else {
      retakeNote.hidden = true;
      retakeNote.textContent = "";
    }
  }
}

function renderProgress(root: HTMLElement, payload: QuizClientPayload): void {
  const summary = summarizeProgress(payload.questions, loadQuizState());
  const answeredEl = root.querySelector("[data-quiz-answered]");
  const percentEl = root.querySelector("[data-quiz-percent]");
  const scoreEl = root.querySelector("[data-quiz-score]");
  const exactEl = root.querySelector("[data-quiz-exact]");
  const resultEl = root.querySelector("[data-quiz-result]");
  const lockedEl = root.querySelector("[data-quiz-locked]");

  if (answeredEl) answeredEl.textContent = `${summary.answered} / ${summary.total}`;
  if (percentEl) percentEl.textContent = `${summary.percentComplete}%`;
  if (scoreEl) scoreEl.textContent = `${summary.scoreEarned} / ${summary.scoreMax}`;
  if (exactEl) exactEl.textContent = `${summary.exactCount} exact`;

  renderRetakeControls(root, payload);

  if (resultEl && lockedEl) {
    if (summary.resultUnlocked) {
      lockedEl.hidden = true;
      resultEl.hidden = false;
      renderResult(resultEl, payload);
    } else {
      lockedEl.hidden = false;
      resultEl.hidden = true;
    }
  }
}

function renderResult(container: Element, payload: QuizClientPayload): void {
  const state = loadQuizState();
  const ranked = rankResearchers(payload.researchers, userBridgeVector(payload.questions, state.attempts));
  const [first, second, third] = ranked;
  if (!first) return;

  const lines = [
    `<p class="quiz-result-lead"><strong>${escapeHtml(first.researcher.name)}</strong> knows most about the topics you already scored on.</p>`,
    `<p>${escapeHtml(first.researcher.blurb)}</p>`
  ];
  if (second) {
    lines.push(
      `<p class="side-panel-meta">Also close: ${escapeHtml(second.researcher.name)}${third ? `, ${escapeHtml(third.researcher.name)}` : ""}.</p>`
    );
  }
  lines.push(
    `<p class="side-panel-meta">This names who has written about what you got right — not who you should agree with.</p>`
  );
  container.innerHTML = lines.join("");
}

function optionClass(option: QuizQuestion["options"][number], selected: string[], revealed: boolean): string {
  const classes = ["quiz-option"];
  if (selected.includes(option.id)) classes.push("is-selected");
  if (revealed) {
    if (option.correct) classes.push("is-correct");
    else if (selected.includes(option.id)) classes.push("is-wrong");
  }
  return classes.join(" ");
}

function renderQuestionMarkup(
  question: QuizQuestion,
  base: string,
  attempt: QuizAttempt | undefined,
  revealed: boolean,
  displayOptions: QuizQuestion["options"],
  showSkip: boolean
): string {
  const selected = attempt?.selected ?? [];
  const options = displayOptions
    .map((option) => {
      const checked = selected.includes(option.id) ? " checked" : "";
      const disabled = revealed ? " disabled" : "";
      return `<label class="${optionClass(option, selected, revealed)}">
  <input type="checkbox" value="${escapeHtml(option.id)}"${checked}${disabled} />
  <span>${escapeHtml(option.text)}</span>
</label>`;
    })
    .join("");

  const feedback =
    revealed && attempt
      ? `<div class="quiz-feedback">
  <p>${escapeHtml(question.explanation)}</p>
  <p class="side-panel-meta">Source: <a href="${withBase(base, question.source.href)}">${escapeHtml(question.source.label)}</a></p>
  <p class="side-panel-meta">Score on this question: ${attempt.earned} / ${attempt.max}${attempt.exact ? " (exact)" : ""}</p>
</div>`
      : "";

  const checkButton = revealed
    ? ""
    : `<p class="button-row">
  <button type="button" class="button primary" data-quiz-check>Check</button>
  ${showSkip ? `<button type="button" class="button" data-quiz-skip>Skip</button>` : ""}
</p>`;

  return `<article class="quiz-question" data-question-id="${escapeHtml(question.id)}">
  <p class="quiz-prompt">${escapeHtml(question.prompt)}</p>
  <div class="quiz-options">${options}</div>
  ${checkButton}
  ${feedback}
</article>`;
}

function bindQuestion(root: HTMLElement, onCheck?: () => void, onSkip?: () => void): void {
  root.querySelectorAll<HTMLLabelElement>(".quiz-option").forEach((label) => {
    label.addEventListener("click", (event) => {
      const article = label.closest(".quiz-question");
      if (!article || article.querySelector("[data-quiz-check]") === null) return;
      const input = label.querySelector("input");
      if (!input || event.target === input) return;
      event.preventDefault();
      input.checked = !input.checked;
      label.classList.toggle("is-selected", input.checked);
    });
  });

  const check = root.querySelector<HTMLButtonElement>("[data-quiz-check]");
  if (check) {
    check.addEventListener("click", () => onCheck?.());
  }
  const skip = root.querySelector<HTMLButtonElement>("[data-quiz-skip]");
  if (skip) {
    skip.addEventListener("click", () => onSkip?.());
  }
}

function mountQuestion(
  container: HTMLElement,
  question: QuizQuestion,
  base: string,
  attempt: QuizAttempt | undefined,
  revealed: boolean,
  onCheck?: () => void,
  displayOptions: QuizQuestion["options"] = shuffledOptions(question.options),
  onSkip?: () => void
): HTMLElement {
  container.innerHTML = renderQuestionMarkup(
    question,
    base,
    attempt,
    revealed,
    displayOptions,
    Boolean(onSkip) && !revealed
  );
  const article = container.querySelector(".quiz-question") as HTMLElement;
  bindQuestion(article, onCheck, onSkip);
  return article;
}

export function initQuizPlayer(root: HTMLElement, options: QuizUiOptions): void {
  const stack = root.querySelector("[data-quiz-stack]");
  const progressRoot = root.closest(".quiz-shell") ?? root;
  if (!stack) return;

  let revealedEl: HTMLElement | null = null;

  const refreshProgress = () => renderProgress(progressRoot, options.payload);

  const clearStack = () => {
    stack.replaceChildren();
    revealedEl = null;
  };

  const showNext = (excludeId?: string) => {
    const state = loadQuizState();
    const next = pickNextQuestion(
      options.payload.questions,
      state,
      Math.random,
      excludeId ? [excludeId] : []
    );
    if (!next) {
      refreshProgress();
      return;
    }
    const slot = document.createElement("div");
    slot.className = "quiz-slot";
    stack.appendChild(slot);
    const displayOptions = shuffledOptions(next.options);
    const canSkip =
      playerEligibleQuestions(options.payload.questions, state).filter((question) => question.id !== next.id)
        .length > 0;
    mountQuestion(
      slot,
      next,
      options.base,
      undefined,
      false,
      () => {
        const current = loadQuizState();
        const selected = selectedFromRoot(slot);
        const scored = scoreQuestion(next, selected);
        let newState = recordAttempt(current, next.id, { selected, ...scored });
        newState = afterPlayerAnswer(newState, next.id, options.payload.questions);
        saveQuizState(newState);

        mountQuestion(slot, next, options.base, newState.attempts[next.id], true, undefined, displayOptions);

        if (revealedEl && revealedEl !== slot) {
          revealedEl.remove();
        }
        revealedEl = slot;

        refreshProgress();

        const stillRemaining = pickNextQuestion(options.payload.questions, newState);
        if (stillRemaining) {
          showNext();
        }
      },
      displayOptions,
      canSkip
        ? () => {
            slot.remove();
            if (revealedEl === slot) revealedEl = null;
            showNext(next.id);
          }
        : undefined
    );
  };

  const startPlayer = () => {
    clearStack();
    refreshProgress();
    const state = loadQuizState();
    if (playerEligibleQuestions(options.payload.questions, state).length === 0) {
      return;
    }
    showNext();
  };

  const retakeBtn = progressRoot.querySelector<HTMLButtonElement>("[data-quiz-retake]");
  retakeBtn?.addEventListener("click", () => {
    const current = loadQuizState();
    if (!canStartRetake(current)) return;
    const next = startRetakeSession(current);
    saveQuizState(next);
    startPlayer();
  });

  startPlayer();
}

export function initQuizBlock(root: HTMLElement, options: QuizUiOptions): void {
  const list = root.querySelector("[data-quiz-block-list]");
  if (!list || !options.appearOn) return;

  const questions = options.payload.questions.filter((question) =>
    question.appearOn?.includes(options.appearOn!)
  );
  const tagged = questions.filter((question) => question.tags?.includes("takeaway"));
  const rest = questions.filter((question) => !question.tags?.includes("takeaway"));
  const ordered = [...tagged, ...rest];
  const displayOrderByQuestion = new Map<string, QuizQuestion["options"]>();
  const skipped = new Set<string>();

  const renderBlock = () => {
    list.replaceChildren();
    const state = loadQuizState();

    for (const question of ordered) {
      if (skipped.has(question.id) && questionStatus(state, question.id) === "unanswered") {
        continue;
      }
      const slot = document.createElement("div");
      slot.className = "quiz-slot";
      list.appendChild(slot);
      const status = questionStatus(state, question.id);
      const attempt = state.attempts[question.id];
      const revealed = status === "answered";
      const editable = status === "unanswered" || status === "retakeable";
      let displayOptions: QuizQuestion["options"];
      if (revealed) {
        displayOptions =
          displayOrderByQuestion.get(question.id) ?? shuffledOptions(question.options);
      } else if (status === "retakeable") {
        displayOptions = shuffledOptions(question.options);
      } else {
        displayOptions =
          displayOrderByQuestion.get(question.id) ?? shuffledOptions(question.options);
      }
      displayOrderByQuestion.set(question.id, displayOptions);

      mountQuestion(
        slot,
        question,
        options.base,
        revealed ? attempt : undefined,
        revealed,
        editable
          ? () => {
              displayOrderByQuestion.set(question.id, optionOrderFromSlot(slot, question));
              const current = loadQuizState();
              const selected = selectedFromRoot(slot);
              const scored = scoreQuestion(question, selected);
              let newState = recordAttempt(current, question.id, { selected, ...scored });
              newState = afterPlayerAnswer(newState, question.id, options.payload.questions);
              saveQuizState(newState);
              renderBlock();
            }
          : undefined,
        displayOptions,
        editable
          ? () => {
              skipped.add(question.id);
              renderBlock();
            }
          : undefined
      );
    }
  };

  renderBlock();
}

export function initQuizUi(root: HTMLElement, options: QuizUiOptions): void {
  if (options.mode === "player") {
    initQuizPlayer(root, options);
  } else {
    initQuizBlock(root, options);
  }
}

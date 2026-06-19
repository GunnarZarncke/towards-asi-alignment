/**
 * Value Bundle Simulator
 *
 * A small, transparent toy model that maps ecological/social environment
 * parameters to culturally salient value terms.
 *
 * The model is deliberately simple. It is not a culture predictor. It is a
 * hypothesis generator for an interactive book module.
 */

export type Env = {
  /** Resource slack: 0 = scarcity, 1 = abundance */
  R: number;
  /** Effective group scale: 0 = small band, 1 = large anonymous society */
  N: number;
  /** Gossip / visibility: 0 = private, 1 = reputation-saturated */
  G: number;
  /** Disease load: 0 = low pathogen pressure, 1 = high pathogen pressure */
  D: number;
  /** Seasonality / shocks: 0 = stable, 1 = harsh or shock-prone */
  S: number;
  /** Mobility: 0 = sedentary, 1 = mobile / migratory */
  M: number;
  /** Contestable wealth: 0 = secure/non-stealable, 1 = stealable/raidable */
  C: number;
};

export type DerivedFeatures = Env & {
  /** Scarcity */
  A: number;
  /** Small-scale social world */
  K: number;
  /** Sedentism */
  Z: number;
  /** Pathogen safety */
  Q: number;
  /** Secure property / low raiding */
  P: number;
  /** Abundant, mobile, high-reputation, low-raiding ecology */
  forager: number;
  /** Reputation-sensitive defense of contestable resources */
  honor: number;
  /** Contamination/order pressure */
  purity: number;
  /** Coordination pressure under scarcity and sedentism */
  hierarchy: number;
  /** Large-scale rule/contract pressure */
  legalism: number;
  /** Small-scale mutual dependence */
  kinship: number;
  /** Slack plus safe mobility */
  exploration: number;
};

export type ValueScore = {
  name: string;
  weight: number;
  raw: number;
};

export const sliderDefinitions: Array<{
  key: keyof Env;
  label: string;
  low: string;
  high: string;
}> = [
  { key: "R", label: "Resource slack", low: "scarce", high: "abundant" },
  { key: "N", label: "Group scale", low: "small", high: "large" },
  { key: "G", label: "Gossip / visibility", low: "private", high: "visible" },
  { key: "D", label: "Disease load", low: "low", high: "high" },
  { key: "S", label: "Seasonality / shocks", low: "stable", high: "harsh" },
  { key: "M", label: "Mobility", low: "sedentary", high: "mobile" },
  { key: "C", label: "Contestable wealth", low: "secure", high: "raidable" },
];

export const presets: Record<string, Env> = {
  "Mobile forager band": {
    R: 0.45, N: 0.10, G: 0.85, D: 0.25, S: 0.50, M: 0.95, C: 0.15,
  },
  "Arctic hunter camp": {
    R: 0.20, N: 0.08, G: 0.75, D: 0.15, S: 0.95, M: 0.80, C: 0.25,
  },
  "Pastoral herder honor culture": {
    R: 0.35, N: 0.30, G: 0.80, D: 0.35, S: 0.60, M: 0.85, C: 0.90,
  },
  "Intensive rice village": {
    R: 0.40, N: 0.65, G: 0.70, D: 0.75, S: 0.65, M: 0.10, C: 0.25,
  },
  "Plough grain village": {
    R: 0.30, N: 0.55, G: 0.60, D: 0.55, S: 0.70, M: 0.10, C: 0.35,
  },
  "Merchant port city": {
    R: 0.65, N: 0.80, G: 0.60, D: 0.55, S: 0.35, M: 0.35, C: 0.35,
  },
  "Imperial bureaucracy": {
    R: 0.55, N: 0.95, G: 0.70, D: 0.55, S: 0.50, M: 0.15, C: 0.25,
  },
  "Mediterranean honor town": {
    R: 0.45, N: 0.55, G: 0.90, D: 0.45, S: 0.50, M: 0.30, C: 0.75,
  },
  "Modern affluent online society": {
    R: 0.85, N: 0.90, G: 0.95, D: 0.15, S: 0.20, M: 0.30, C: 0.15,
  },
  "Frontier settler society": {
    R: 0.50, N: 0.25, G: 0.50, D: 0.30, S: 0.60, M: 0.60, C: 0.65,
  },
};

function clamp01(x: number): number {
  if (!Number.isFinite(x)) return 0;
  return Math.max(0, Math.min(1, x));
}

export function normalizeEnv(env: Env): Env {
  return {
    R: clamp01(env.R),
    N: clamp01(env.N),
    G: clamp01(env.G),
    D: clamp01(env.D),
    S: clamp01(env.S),
    M: clamp01(env.M),
    C: clamp01(env.C),
  };
}

export function features(env: Env): DerivedFeatures {
  const e = normalizeEnv(env);
  const A = 1 - e.R;
  const K = 1 - e.N;
  const Z = 1 - e.M;
  const Q = 1 - e.D;
  const P = 1 - e.C;

  const forager = e.R * e.G * e.M * P * Q;
  const honor = e.C * e.G * (0.4 + 0.6 * e.M) * (0.4 + 0.6 * A);
  const purity = e.D * (0.5 + 0.5 * Z) + 0.25 * e.S;
  const hierarchy = A * Z * (0.4 + 0.6 * e.N) + 0.25 * e.S;
  const legalism = e.N * e.G * P * (0.4 + 0.6 * e.R);
  const kinship = 0.55 * K * e.G + 0.30 * e.S + 0.25 * e.D;
  const exploration = e.R * e.M * Q;

  return { ...e, A, K, Z, Q, P, forager, honor, purity, hierarchy, legalism, kinship, exploration };
}

export function sigmoid(x: number): number {
  return 1 / (1 + Math.exp(-x));
}

export function weightFromRaw(raw: number): number {
  return Math.round(100 * sigmoid(raw));
}

export function rawValueScores(env: Env): Record<string, number> {
  const e = features(env);

  return {
    Benevolence:      -0.2 + 0.7*e.R + 0.6*e.G + 0.5*e.K + 0.3*e.S - 0.4*e.C,
    Universalism:    -0.6 + 0.9*e.R + 0.8*e.N + 0.5*e.G + 0.4*e.Q - 0.5*e.kinship,
    "Self-direction":-0.4 + 1.0*e.R + 0.7*e.M + 0.4*e.N - 0.6*e.D - 0.6*e.hierarchy,
    Security:        -0.2 + 0.9*e.A + 0.7*e.S + 0.7*e.D + 0.5*e.C + 0.3*e.N,
    Conformity:      -0.28 + 0.8*e.D + 0.7*e.S + 0.6*e.hierarchy + 0.5*e.G - 0.5*e.R,
    Tradition:       -0.3 + 0.8*e.Z + 0.7*e.K + 0.5*e.D + 0.5*e.S + 0.4*e.hierarchy,
    Achievement:     -0.5 + 0.8*e.N + 0.6*e.R + 0.5*e.G + 0.4*e.S + 0.3*e.C,
    Power:           -0.7 + 0.9*e.C + 0.8*e.A + 0.7*e.N + 0.5*e.hierarchy - 0.4*e.legalism,
    Hedonism:        -0.8 + 1.1*e.R + 0.6*e.Q + 0.4*e.N - 0.6*e.D - 0.5*e.S,
    Stimulation:     -0.7 + 0.9*e.R + 0.9*e.M + 0.6*e.exploration - 0.4*e.D - 0.3*e.hierarchy,

    Care:            -0.2 + 0.8*e.K + 0.7*e.S + 0.6*e.R + 0.5*e.kinship - 0.3*e.N,
    Fairness:        -0.39 + 1.4*e.legalism + 0.7*e.G + 0.5*e.R + 0.5*e.N - 0.5*e.C,
    Loyalty:         -0.2 + 0.9*e.kinship + 0.6*e.D + 0.5*e.S + 0.4*e.C - 0.4*e.N,
    Authority:       -0.5 + 1.2*e.hierarchy + 0.85*e.N + 0.4*e.D + 0.4*e.S - 0.5*e.forager,
    Purity:          -0.52 + 1.65*e.purity + 0.5*e.Z + 0.3*e.K - 0.4*e.R,
    Honor:           -0.7 + 1.5*e.honor + 0.5*e.M + 0.4*e.G + 0.3*e.A - 0.4*e.legalism,
    Liberty:         -0.40 + 1.0*e.R + 0.8*e.M + 0.5*e.P + 0.4*e.N - 0.7*e.hierarchy,
    Equality:        -0.38 + 2.2*e.forager + 0.6*e.G + 0.5*e.R + 0.2*e.N + 0.5*e.K + 0.6*e.legalism - 0.7*e.C - 0.6*e.hierarchy,
    Fraternity:      -0.4 + 0.8*e.K + 0.7*e.kinship + 0.5*e.G + 0.4*e.S - 0.3*e.N,
    Justice:         -0.44 + 1.4*e.legalism + 0.8*e.N + 0.5*e.G + 0.3*e.R - 0.4*e.kinship,

    Piety:           -0.8 + 0.9*e.S + 0.8*e.D + 0.6*e.Z + 0.5*e.K + 0.3*e.hierarchy,
    Courage:         -0.42 + 0.8*e.C + 0.7*e.S + 0.6*e.M + 0.5*e.honor + 0.3*e.A,
    Temperance:      -0.5 + 0.8*e.S + 0.7*e.D + 0.6*e.Z + 0.4*e.A - 0.4*e.R,
    Wisdom:          -0.4 + 0.7*e.S + 0.6*e.N + 0.5*e.R + 0.5*e.legalism + 0.3*e.Z,
    Truth:           -0.38 + 1.1*e.legalism + 0.7*e.N + 0.5*e.R + 0.4*e.Q - 0.4*e.honor,
    Hospitality:     -0.4 + 0.8*e.M + 0.7*e.K + 0.6*e.S + 0.4*e.kinship - 0.3*e.D,
    "Filial piety":  -0.6 + 0.9*e.Z + 0.8*e.K + 0.7*e.hierarchy + 0.5*e.D,
    Duty:            -0.35 + 0.8*e.S + 1.0*e.hierarchy + 0.7*e.kinship + 0.6*e.D + 0.3*e.N - 0.3*e.R,
    Chastity:        -0.9 + 1.0*e.D + 0.8*e.Z + 0.6*e.K + 0.5*e.hierarchy,
    Humility:        -0.5 + 1.4*e.forager + 1.0*e.K + 0.5*e.G + 0.3*e.Z - 0.5*e.N - 0.4*e.C,

    Solidarity:      -0.3 + 0.8*e.S + 0.7*e.G + 0.6*e.K + 0.5*e.A - 0.3*e.C,
    Autonomy:        -0.5 + 1.0*e.R + 0.8*e.M + 0.6*e.P + 0.4*e.Q - 0.7*e.hierarchy,
    Hierarchy:       -0.48 + 1.6*e.hierarchy + 0.5*e.N + 0.4*e.D + 0.4*e.A - 0.5*e.forager,
    Karma:           -0.8 + 0.8*e.legalism + 0.7*e.K + 0.5*e.D + 0.4*e.S + 0.3*e.Z,
    Ahimsa:          -0.7 + 0.9*e.R + 0.8*e.D + 0.6*e.purity + 0.4*e.Z - 0.5*e.C,
    Ubuntu:          -0.5 + 0.9*e.K + 0.8*e.kinship + 0.6*e.G + 0.4*e.S - 0.3*e.N,
    Stewardship:     -0.5 + 0.8*e.S + 0.7*e.Z + 0.6*e.legalism + 0.5*e.R + 0.3*e.Q,
    Frugality:       -0.30 + 0.9*e.A + 0.8*e.S + 0.5*e.Z + 0.4*e.D - 0.5*e.R,
    Stoicism:        -0.45 + 0.95*e.S + 0.8*e.A + 0.5*e.C + 0.4*e.Z - 0.3*e.R,
    Legacy:          -0.5 + 0.8*e.N + 0.7*e.Z + 0.6*e.hierarchy + 0.5*e.R + 0.3*e.S,
  };
}

export function valueScores(env: Env): ValueScore[] {
  const raw = rawValueScores(env);
  return Object.entries(raw)
    .map(([name, r]) => ({ name, raw: r, weight: weightFromRaw(r) }))
    .sort((a, b) => b.raw - a.raw || a.name.localeCompare(b.name));
}

export function topValues(env: Env, count = 7): ValueScore[] {
  return valueScores(env).slice(0, count);
}

function envEquals(a: Env, b: Env): boolean {
  return sliderDefinitions.every(({ key }) => Math.abs(a[key] - b[key]) < 1e-9);
}

function createElement<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  attrs: Record<string, string> = {},
  text?: string,
): HTMLElementTagNameMap[K] {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
  if (text !== undefined) el.textContent = text;
  return el;
}

export function mountValueBundleSimulator(container: HTMLElement, initialPreset = "Mobile forager band") {
  let env = { ...(presets[initialPreset] ?? presets["Mobile forager band"]) };

  container.innerHTML = "";
  container.classList.add("value-bundle-simulator");

  const style = createElement("style");
  style.textContent = `
    .value-bundle-simulator {
      font-family: system-ui, -apple-system, Segoe UI, sans-serif;
      max-width: 760px;
      border: 1px solid #ddd;
      border-radius: 12px;
      padding: 14px;
      box-sizing: border-box;
      background: #fff;
    }
    .vbs-title { font-weight: 700; margin-bottom: 8px; }
    .vbs-layout { display: grid; grid-template-columns: minmax(260px, 1fr) minmax(220px, 1fr); gap: 16px; }
    .vbs-row { display: grid; grid-template-columns: 118px 1fr 36px; gap: 8px; align-items: center; margin: 7px 0; font-size: 13px; }
    .vbs-row input { width: 100%; }
    .vbs-select { width: 100%; margin-bottom: 8px; }
    .vbs-values { display: grid; gap: 6px; }
    .vbs-value { display: grid; grid-template-columns: 92px 34px 1fr; gap: 8px; align-items: center; font-size: 13px; }
    .vbs-bar-track { background: #eee; border-radius: 999px; height: 9px; overflow: hidden; }
    .vbs-bar { background: #555; height: 100%; }
    .vbs-note { color: #666; font-size: 12px; margin-top: 10px; line-height: 1.3; }
    @media (max-width: 620px) { .vbs-layout { grid-template-columns: 1fr; } }
  `;
  container.appendChild(style);

  const title = createElement("div", { class: "vbs-title" }, "Ecology → Value Salience");
  container.appendChild(title);

  const layout = createElement("div", { class: "vbs-layout" });
  container.appendChild(layout);

  const controls = createElement("div");
  const output = createElement("div", { class: "vbs-values" });
  layout.appendChild(controls);
  layout.appendChild(output);

  const select = createElement("select", { class: "vbs-select" }) as HTMLSelectElement;
  for (const name of Object.keys(presets)) {
    const option = createElement("option", { value: name }, name) as HTMLOptionElement;
    if (name === initialPreset) option.selected = true;
    select.appendChild(option);
  }
  controls.appendChild(select);

  const sliders = new Map<keyof Env, HTMLInputElement>();

  for (const def of sliderDefinitions) {
    const row = createElement("label", { class: "vbs-row" });
    row.appendChild(createElement("span", {}, def.label));
    const input = createElement("input", { type: "range", min: "0", max: "1", step: "0.01" }) as HTMLInputElement;
    input.value = String(env[def.key]);
    const num = createElement("span", {}, env[def.key].toFixed(2));
    input.addEventListener("input", () => {
      env = { ...env, [def.key]: Number(input.value) };
      num.textContent = env[def.key].toFixed(2);
      const matchingPreset = Object.entries(presets).find(([, value]) => envEquals(value, env));
      select.value = matchingPreset?.[0] ?? "";
      render();
    });
    row.appendChild(input);
    row.appendChild(num);
    controls.appendChild(row);
    sliders.set(def.key, input);
  }

  const note = createElement(
    "div",
    { class: "vbs-note" },
    "Toy model. The weights are editable priors, not empirical estimates. Output shows the seven most salient value terms."
  );
  controls.appendChild(note);

  select.addEventListener("change", () => {
    env = { ...presets[select.value] };
    for (const def of sliderDefinitions) {
      const input = sliders.get(def.key);
      if (input) input.value = String(env[def.key]);
      const row = input?.parentElement;
      const num = row?.lastElementChild;
      if (num) num.textContent = env[def.key].toFixed(2);
    }
    render();
  });

  function render() {
    output.innerHTML = "";
    const values = topValues(env, 7);
    for (const v of values) {
      const row = createElement("div", { class: "vbs-value" });
      row.appendChild(createElement("span", {}, v.name));
      row.appendChild(createElement("span", {}, String(v.weight)));
      const track = createElement("div", { class: "vbs-bar-track" });
      const bar = createElement("div", { class: "vbs-bar" });
      bar.style.width = `${v.weight}%`;
      track.appendChild(bar);
      row.appendChild(track);
      output.appendChild(row);
    }
  }

  render();

  return {
    getEnv: () => ({ ...env }),
    setEnv: (next: Env) => {
      env = normalizeEnv(next);
      for (const def of sliderDefinitions) {
        const input = sliders.get(def.key);
        if (input) input.value = String(env[def.key]);
      }
      render();
    },
  };
}

// Browser convenience: <div id="value-bundle-simulator"></div>
declare global {
  interface Window {
    mountValueBundleSimulator?: typeof mountValueBundleSimulator;
  }
}

if (typeof window !== "undefined") {
  window.mountValueBundleSimulator = mountValueBundleSimulator;
  const autoMount = document.getElementById("value-bundle-simulator");
  if (autoMount) mountValueBundleSimulator(autoMount);
}

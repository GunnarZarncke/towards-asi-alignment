const sliderDefinitions = [
  { key: "R", label: "Resource slack", low: "scarce", high: "abundant" },
  { key: "N", label: "Group scale", low: "small", high: "large" },
  { key: "G", label: "Gossip / visibility", low: "private", high: "visible" },
  { key: "D", label: "Disease load", low: "low", high: "high" },
  { key: "S", label: "Seasonality / shocks", low: "stable", high: "harsh" },
  { key: "M", label: "Mobility", low: "sedentary", high: "mobile" },
  { key: "C", label: "Contestable wealth", low: "secure", high: "raidable" }
];
const presets = {
  "Mobile forager band": {
    R: 0.45,
    N: 0.1,
    G: 0.85,
    D: 0.25,
    S: 0.5,
    M: 0.95,
    C: 0.15
  },
  "Arctic hunter camp": {
    R: 0.2,
    N: 0.08,
    G: 0.75,
    D: 0.15,
    S: 0.95,
    M: 0.8,
    C: 0.25
  },
  "Pastoral herder honor culture": {
    R: 0.35,
    N: 0.3,
    G: 0.8,
    D: 0.35,
    S: 0.6,
    M: 0.85,
    C: 0.9
  },
  "Intensive rice village": {
    R: 0.4,
    N: 0.65,
    G: 0.7,
    D: 0.75,
    S: 0.65,
    M: 0.1,
    C: 0.25
  },
  "Plough grain village": {
    R: 0.3,
    N: 0.55,
    G: 0.6,
    D: 0.55,
    S: 0.7,
    M: 0.1,
    C: 0.35
  },
  "Merchant port city": {
    R: 0.65,
    N: 0.8,
    G: 0.6,
    D: 0.55,
    S: 0.35,
    M: 0.35,
    C: 0.35
  },
  "Imperial bureaucracy": {
    R: 0.55,
    N: 0.95,
    G: 0.7,
    D: 0.55,
    S: 0.5,
    M: 0.15,
    C: 0.25
  },
  "Mediterranean honor town": {
    R: 0.45,
    N: 0.55,
    G: 0.9,
    D: 0.45,
    S: 0.5,
    M: 0.3,
    C: 0.75
  },
  "Modern affluent online society": {
    R: 0.85,
    N: 0.9,
    G: 0.95,
    D: 0.15,
    S: 0.2,
    M: 0.3,
    C: 0.15
  },
  "Frontier settler society": {
    R: 0.5,
    N: 0.25,
    G: 0.5,
    D: 0.3,
    S: 0.6,
    M: 0.6,
    C: 0.65
  }
};
function clamp01(x) {
  if (!Number.isFinite(x)) return 0;
  return Math.max(0, Math.min(1, x));
}
function normalizeEnv(env) {
  return {
    R: clamp01(env.R),
    N: clamp01(env.N),
    G: clamp01(env.G),
    D: clamp01(env.D),
    S: clamp01(env.S),
    M: clamp01(env.M),
    C: clamp01(env.C)
  };
}
function features(env) {
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
  const kinship = 0.55 * K * e.G + 0.3 * e.S + 0.25 * e.D;
  const exploration = e.R * e.M * Q;
  return { ...e, A, K, Z, Q, P, forager, honor, purity, hierarchy, legalism, kinship, exploration };
}
function sigmoid(x) {
  return 1 / (1 + Math.exp(-x));
}
function weightFromRaw(raw) {
  return Math.round(100 * sigmoid(raw));
}
function rawValueScores(env) {
  const e = features(env);
  return {
    Benevolence: -0.2 + 0.7 * e.R + 0.6 * e.G + 0.5 * e.K + 0.3 * e.S - 0.4 * e.C,
    Universalism: -0.6 + 0.9 * e.R + 0.8 * e.N + 0.5 * e.G + 0.4 * e.Q - 0.5 * e.kinship,
    "Self-direction": -0.4 + 1 * e.R + 0.7 * e.M + 0.4 * e.N - 0.6 * e.D - 0.6 * e.hierarchy,
    Security: -0.2 + 0.9 * e.A + 0.7 * e.S + 0.7 * e.D + 0.5 * e.C + 0.3 * e.N,
    Conformity: -0.28 + 0.8 * e.D + 0.7 * e.S + 0.6 * e.hierarchy + 0.5 * e.G - 0.5 * e.R,
    Tradition: -0.3 + 0.8 * e.Z + 0.7 * e.K + 0.5 * e.D + 0.5 * e.S + 0.4 * e.hierarchy,
    Achievement: -0.5 + 0.8 * e.N + 0.6 * e.R + 0.5 * e.G + 0.4 * e.S + 0.3 * e.C,
    Power: -0.7 + 0.9 * e.C + 0.8 * e.A + 0.7 * e.N + 0.5 * e.hierarchy - 0.4 * e.legalism,
    Hedonism: -0.8 + 1.1 * e.R + 0.6 * e.Q + 0.4 * e.N - 0.6 * e.D - 0.5 * e.S,
    Stimulation: -0.7 + 0.9 * e.R + 0.9 * e.M + 0.6 * e.exploration - 0.4 * e.D - 0.3 * e.hierarchy,
    Care: -0.2 + 0.8 * e.K + 0.7 * e.S + 0.6 * e.R + 0.5 * e.kinship - 0.3 * e.N,
    Fairness: -0.39 + 1.4 * e.legalism + 0.7 * e.G + 0.5 * e.R + 0.5 * e.N - 0.5 * e.C,
    Loyalty: -0.2 + 0.9 * e.kinship + 0.6 * e.D + 0.5 * e.S + 0.4 * e.C - 0.4 * e.N,
    Authority: -0.5 + 1.2 * e.hierarchy + 0.85 * e.N + 0.4 * e.D + 0.4 * e.S - 0.5 * e.forager,
    Purity: -0.52 + 1.65 * e.purity + 0.5 * e.Z + 0.3 * e.K - 0.4 * e.R,
    Honor: -0.7 + 1.5 * e.honor + 0.5 * e.M + 0.4 * e.G + 0.3 * e.A - 0.4 * e.legalism,
    Liberty: -0.4 + 1 * e.R + 0.8 * e.M + 0.5 * e.P + 0.4 * e.N - 0.7 * e.hierarchy,
    Equality: -0.38 + 2.2 * e.forager + 0.6 * e.G + 0.5 * e.R + 0.2 * e.N + 0.5 * e.K + 0.6 * e.legalism - 0.7 * e.C - 0.6 * e.hierarchy,
    Fraternity: -0.4 + 0.8 * e.K + 0.7 * e.kinship + 0.5 * e.G + 0.4 * e.S - 0.3 * e.N,
    Justice: -0.44 + 1.4 * e.legalism + 0.8 * e.N + 0.5 * e.G + 0.3 * e.R - 0.4 * e.kinship,
    Piety: -0.8 + 0.9 * e.S + 0.8 * e.D + 0.6 * e.Z + 0.5 * e.K + 0.3 * e.hierarchy,
    Courage: -0.42 + 0.8 * e.C + 0.7 * e.S + 0.6 * e.M + 0.5 * e.honor + 0.3 * e.A,
    Temperance: -0.5 + 0.8 * e.S + 0.7 * e.D + 0.6 * e.Z + 0.4 * e.A - 0.4 * e.R,
    Wisdom: -0.4 + 0.7 * e.S + 0.6 * e.N + 0.5 * e.R + 0.5 * e.legalism + 0.3 * e.Z,
    Truth: -0.38 + 1.1 * e.legalism + 0.7 * e.N + 0.5 * e.R + 0.4 * e.Q - 0.4 * e.honor,
    Hospitality: -0.4 + 0.8 * e.M + 0.7 * e.K + 0.6 * e.S + 0.4 * e.kinship - 0.3 * e.D,
    "Filial piety": -0.6 + 0.9 * e.Z + 0.8 * e.K + 0.7 * e.hierarchy + 0.5 * e.D,
    Duty: -0.35 + 0.8 * e.S + 1 * e.hierarchy + 0.7 * e.kinship + 0.6 * e.D + 0.3 * e.N - 0.3 * e.R,
    Chastity: -0.9 + 1 * e.D + 0.8 * e.Z + 0.6 * e.K + 0.5 * e.hierarchy,
    Humility: -0.5 + 1.4 * e.forager + 1 * e.K + 0.5 * e.G + 0.3 * e.Z - 0.5 * e.N - 0.4 * e.C,
    Solidarity: -0.3 + 0.8 * e.S + 0.7 * e.G + 0.6 * e.K + 0.5 * e.A - 0.3 * e.C,
    Autonomy: -0.5 + 1 * e.R + 0.8 * e.M + 0.6 * e.P + 0.4 * e.Q - 0.7 * e.hierarchy,
    Hierarchy: -0.48 + 1.6 * e.hierarchy + 0.5 * e.N + 0.4 * e.D + 0.4 * e.A - 0.5 * e.forager,
    Karma: -0.8 + 0.8 * e.legalism + 0.7 * e.K + 0.5 * e.D + 0.4 * e.S + 0.3 * e.Z,
    Ahimsa: -0.7 + 0.9 * e.R + 0.8 * e.D + 0.6 * e.purity + 0.4 * e.Z - 0.5 * e.C,
    Ubuntu: -0.5 + 0.9 * e.K + 0.8 * e.kinship + 0.6 * e.G + 0.4 * e.S - 0.3 * e.N,
    Stewardship: -0.5 + 0.8 * e.S + 0.7 * e.Z + 0.6 * e.legalism + 0.5 * e.R + 0.3 * e.Q,
    Frugality: -0.3 + 0.9 * e.A + 0.8 * e.S + 0.5 * e.Z + 0.4 * e.D - 0.5 * e.R,
    Stoicism: -0.45 + 0.95 * e.S + 0.8 * e.A + 0.5 * e.C + 0.4 * e.Z - 0.3 * e.R,
    Legacy: -0.5 + 0.8 * e.N + 0.7 * e.Z + 0.6 * e.hierarchy + 0.5 * e.R + 0.3 * e.S
  };
}
function valueScores(env) {
  const raw = rawValueScores(env);
  return Object.entries(raw).map(([name, r]) => ({ name, raw: r, weight: weightFromRaw(r) })).sort((a, b) => b.raw - a.raw || a.name.localeCompare(b.name));
}
function topValues(env, count = 7) {
  return valueScores(env).slice(0, count);
}
function envEquals(a, b) {
  return sliderDefinitions.every(({ key }) => Math.abs(a[key] - b[key]) < 1e-9);
}
function createElement(tag, attrs = {}, text) {
  const el = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
  if (text !== void 0) el.textContent = text;
  return el;
}
function mountValueBundleSimulator(container, initialPreset = "Mobile forager band") {
  let env = { ...presets[initialPreset] ?? presets["Mobile forager band"] };
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
  const title = createElement("div", { class: "vbs-title" }, "Ecology \u2192 Value Salience");
  container.appendChild(title);
  const layout = createElement("div", { class: "vbs-layout" });
  container.appendChild(layout);
  const controls = createElement("div");
  const output = createElement("div", { class: "vbs-values" });
  layout.appendChild(controls);
  layout.appendChild(output);
  const select = createElement("select", { class: "vbs-select" });
  for (const name of Object.keys(presets)) {
    const option = createElement("option", { value: name }, name);
    if (name === initialPreset) option.selected = true;
    select.appendChild(option);
  }
  controls.appendChild(select);
  const sliders = /* @__PURE__ */ new Map();
  for (const def of sliderDefinitions) {
    const row = createElement("label", { class: "vbs-row" });
    row.appendChild(createElement("span", {}, def.label));
    const input = createElement("input", { type: "range", min: "0", max: "1", step: "0.01" });
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
    setEnv: (next) => {
      env = normalizeEnv(next);
      for (const def of sliderDefinitions) {
        const input = sliders.get(def.key);
        if (input) input.value = String(env[def.key]);
      }
      render();
    }
  };
}
if (typeof window !== "undefined") {
  window.mountValueBundleSimulator = mountValueBundleSimulator;
  const autoMount = document.getElementById("value-bundle-simulator");
  if (autoMount) mountValueBundleSimulator(autoMount);
}
export {
  features,
  mountValueBundleSimulator,
  normalizeEnv,
  presets,
  rawValueScores,
  sigmoid,
  sliderDefinitions,
  topValues,
  valueScores,
  weightFromRaw
};

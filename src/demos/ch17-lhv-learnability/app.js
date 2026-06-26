const defaultConfig = {
  seed: 17,
  total: 2200,
  testCount: 700,
  ambientDim: 64,
  hubDim: 6,
  noise: 0.75
};
function mulberry32(seed) {
  let t = seed >>> 0;
  return () => {
    t += 1831565813;
    let x = Math.imul(t ^ t >>> 15, 1 | t);
    x ^= x + Math.imul(x ^ x >>> 7, 61 | x);
    return ((x ^ x >>> 14) >>> 0) / 4294967296;
  };
}
function gaussian(rng) {
  const u = Math.max(rng(), 1e-12);
  const v = Math.max(rng(), 1e-12);
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}
function dot(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i += 1) s += a[i] * b[i];
  return s;
}
function mean(values) {
  return values.reduce((a, b) => a + b, 0) / values.length;
}
function std(values) {
  const m = mean(values);
  return Math.sqrt(mean(values.map((v) => (v - m) ** 2)) + 1e-9);
}
function centeredColumns(rows) {
  const d = rows[0].length;
  const center = Array.from({ length: d }, (_, j) => mean(rows.map((r) => r[j])));
  const scale = Array.from({ length: d }, (_, j) => std(rows.map((r) => r[j])));
  return {
    center,
    scale,
    centered: rows.map((r) => r.map((v, j) => (v - center[j]) / scale[j]))
  };
}
function covariance(rows) {
  const n = rows.length;
  const d = rows[0].length;
  const cov = Array.from({ length: d }, () => Array(d).fill(0));
  for (const row of rows) {
    for (let i = 0; i < d; i += 1) {
      for (let j = i; j < d; j += 1) cov[i][j] += row[i] * row[j];
    }
  }
  for (let i = 0; i < d; i += 1) {
    for (let j = i; j < d; j += 1) {
      cov[i][j] /= n - 1;
      cov[j][i] = cov[i][j];
    }
  }
  return cov;
}
function matVec(m, v) {
  return m.map((row) => dot(row, v));
}
function norm(v) {
  return Math.sqrt(dot(v, v)) || 1;
}
function topEigenpairs(covIn, count, seed) {
  const rng = mulberry32(seed);
  const cov = covIn.map((row) => [...row]);
  const d = cov.length;
  const pairs = [];
  for (let k = 0; k < count; k += 1) {
    let v = Array.from({ length: d }, () => gaussian(rng));
    for (let iter = 0; iter < 45; iter += 1) {
      const mv = matVec(cov, v);
      const n = norm(mv);
      v = mv.map((x) => x / n);
    }
    const value = dot(v, matVec(cov, v));
    pairs.push({ value, vector: v });
    for (let i = 0; i < d; i += 1) {
      for (let j = 0; j < d; j += 1) cov[i][j] -= value * v[i] * v[j];
    }
  }
  return pairs;
}
function quantile(values, q) {
  const sorted = [...values].sort((a, b) => a - b);
  const idx = Math.min(sorted.length - 1, Math.max(0, Math.ceil(q * sorted.length) - 1));
  return sorted[idx];
}
function shuffleColumnNull(rows, rng) {
  const n = rows.length;
  const d = rows[0].length;
  const out = Array.from({ length: n }, () => Array(d).fill(0));
  for (let j = 0; j < d; j += 1) {
    const col = rows.map((r) => r[j]);
    for (let i = col.length - 1; i > 0; i -= 1) {
      const k = Math.floor(rng() * (i + 1));
      [col[i], col[k]] = [col[k], col[i]];
    }
    for (let i = 0; i < n; i += 1) out[i][j] = col[i];
  }
  return out;
}
function pcaScores(rows, vectors) {
  return rows.map((row) => vectors.map((v) => dot(row, v)));
}
function generate(config) {
  const rng = mulberry32(config.seed);
  const { total, ambientDim: d, hubDim: k, noise } = config;
  const loadings = Array.from({ length: k }, () => Array(d).fill(0));
  for (let j = 0; j < d; j += 1) {
    const hub = j < k * 8 ? Math.floor(j / 8) : Math.floor(rng() * k);
    for (let h = 0; h < k; h += 1) {
      loadings[h][j] = h === hub ? 0.9 + 0.2 * rng() : 0.08 * gaussian(rng);
    }
  }
  const hubs = [];
  const embeddings = [];
  const scores = [];
  for (let i = 0; i < total; i += 1) {
    const z = Array.from({ length: k }, () => gaussian(rng));
    const x = Array.from({ length: d }, (_, j) => {
      let value = 0;
      for (let h = 0; h < k; h += 1) value += z[h] * loadings[h][j];
      return value + noise * gaussian(rng);
    });
    const moralScore = 1.1 * z[0] - 0.9 * z[1] + 0.7 * z[2] + 0.55 * z[3] * z[4] - 0.45 * Math.abs(z[5]) + 0.55 * gaussian(rng);
    hubs.push(z);
    embeddings.push(x);
    scores.push(moralScore);
  }
  const threshold = quantile(scores, 0.5);
  const labels = scores.map((s) => s > threshold ? 1 : 0);
  return { hubs, embeddings, labels };
}
function trainLogistic(rows, labels, trainCount) {
  const d = rows[0].length;
  const weights = Array(d).fill(0);
  let bias = 0;
  const epochs = 70;
  const l2 = 0.02;
  for (let epoch = 0; epoch < epochs; epoch += 1) {
    const lr = 0.08 / Math.sqrt(1 + epoch);
    for (let i = 0; i < trainCount; i += 1) {
      const score = dot(weights, rows[i]) + bias;
      const pred = 1 / (1 + Math.exp(-score));
      const err = pred - labels[i];
      for (let j = 0; j < d; j += 1) weights[j] -= lr * (err * rows[i][j] + l2 * weights[j]);
      bias -= lr * err;
    }
  }
  return { weights, bias };
}
function auc(scores, labels) {
  const pairs = scores.map((score, i) => ({ score, label: labels[i] })).sort((a, b) => a.score - b.score);
  let rankSum = 0;
  let positives = 0;
  let negatives = 0;
  for (let i = 0; i < pairs.length; i += 1) {
    if (pairs[i].label === 1) {
      positives += 1;
      rankSum += i + 1;
    } else {
      negatives += 1;
    }
  }
  if (positives === 0 || negatives === 0) return 0.5;
  return (rankSum - positives * (positives + 1) / 2) / (positives * negatives);
}
function scoreModel(model, rows, start) {
  return rows.slice(start).map((r) => dot(model.weights, r) + model.bias);
}
function accuracy(scores, labels) {
  let correct = 0;
  for (let i = 0; i < scores.length; i += 1) {
    if ((scores[i] > 0 ? 1 : 0) === labels[i]) correct += 1;
  }
  return correct / scores.length;
}
function binaryEntropy(p) {
  if (p <= 0 || p >= 1) return 0;
  return -(p * Math.log2(p) + (1 - p) * Math.log2(1 - p));
}
function runLhvExperiment(config = defaultConfig) {
  const data = generate(config);
  const trainLimit = config.total - config.testCount;
  const labelsTest = data.labels.slice(trainLimit);
  const rawStd = centeredColumns(data.embeddings);
  const hubStd = centeredColumns(data.hubs);
  const cov = covariance(rawStd.centered);
  const eigenpairs = topEigenpairs(cov, config.hubDim + 1, config.seed + 1e3);
  const vectors = eigenpairs.slice(0, config.hubDim).map((p) => p.vector);
  const lhvRows = pcaScores(rawStd.centered, vectors);
  const rng = mulberry32(config.seed + 2e3);
  const nullValues = Array.from({ length: config.hubDim + 1 }, () => []);
  for (let rep = 0; rep < 10; rep += 1) {
    const nullRows = shuffleColumnNull(rawStd.centered, rng);
    const nullPairs = topEigenpairs(covariance(nullRows), config.hubDim + 1, config.seed + 3e3 + rep);
    nullPairs.forEach((pair, i) => nullValues[i].push(pair.value));
  }
  const spectrum = eigenpairs.map((pair, i) => {
    const null95 = quantile(nullValues[i], 0.95);
    return {
      component: i + 1,
      eigenvalue: pair.value,
      null95,
      significant: pair.value > null95
    };
  });
  const recoveredHubDim = spectrum.filter((row) => row.significant).length;
  const probeSizes = [32, 64, 128, 256, 512, 1024].filter((n) => n < trainLimit);
  const probes = probeSizes.map((nTrain) => {
    const rawModel = trainLogistic(rawStd.centered, data.labels, nTrain);
    const lhvModel = trainLogistic(lhvRows, data.labels, nTrain);
    const oracleModel = trainLogistic(hubStd.centered, data.labels, nTrain);
    const rawScores = scoreModel(rawModel, rawStd.centered, trainLimit);
    const lhvScores = scoreModel(lhvModel, lhvRows, trainLimit);
    const oracleScores = scoreModel(oracleModel, hubStd.centered, trainLimit);
    return {
      nTrain,
      rawAuc: auc(rawScores, labelsTest),
      lhvAuc: auc(lhvScores, labelsTest),
      oracleAuc: auc(oracleScores, labelsTest),
      rawAccuracy: accuracy(rawScores, labelsTest),
      lhvAccuracy: accuracy(lhvScores, labelsTest),
      oracleAccuracy: accuracy(oracleScores, labelsTest)
    };
  });
  const finalError = 1 - probes[probes.length - 1].lhvAccuracy;
  return {
    config,
    spectrum,
    recoveredHubDim,
    probes,
    infoLowerBoundBits: Math.max(0, 1 - binaryEntropy(finalError))
  };
}
function fmt(x) {
  return x.toFixed(3);
}
function renderTable(headers, rows) {
  const table = document.createElement("table");
  const thead = document.createElement("thead");
  const tr = document.createElement("tr");
  headers.forEach((h) => {
    const th = document.createElement("th");
    th.textContent = h;
    tr.appendChild(th);
  });
  thead.appendChild(tr);
  table.appendChild(thead);
  const tbody = document.createElement("tbody");
  rows.forEach((row) => {
    const trBody = document.createElement("tr");
    row.forEach((cell) => {
      const td = document.createElement("td");
      td.textContent = cell;
      trBody.appendChild(td);
    });
    tbody.appendChild(trBody);
  });
  table.appendChild(tbody);
  return table;
}
function mountLhvLearnabilityDemo(container) {
  const result = runLhvExperiment();
  container.innerHTML = "";
  container.classList.add("lhv-demo");
  const style = document.createElement("style");
  style.textContent = `
    .lhv-demo { font-family: system-ui, -apple-system, Segoe UI, sans-serif; max-width: 920px; border: 1px solid #ddd; border-radius: 12px; padding: 16px; background: #fff; color: #111; }
    .lhv-demo h2 { font-size: 1.1rem; margin: 0 0 8px; }
    .lhv-demo p { color: #444; line-height: 1.45; max-width: 78ch; }
    .lhv-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; align-items: start; }
    .lhv-card { border: 1px solid #eee; border-radius: 10px; padding: 12px; }
    .lhv-card h3 { font-size: 0.95rem; margin: 0 0 8px; }
    .lhv-demo table { border-collapse: collapse; width: 100%; font-size: 0.85rem; }
    .lhv-demo th, .lhv-demo td { border-bottom: 1px solid #eee; padding: 5px 6px; text-align: right; }
    .lhv-demo th:first-child, .lhv-demo td:first-child { text-align: left; }
    .lhv-note { font-size: 0.85rem; color: #666; margin-top: 10px; }
  `;
  container.appendChild(style);
  const title = document.createElement("h2");
  title.textContent = "LHV learnability toy experiment";
  container.appendChild(title);
  const intro = document.createElement("p");
  intro.textContent = `Synthetic setup: ${result.config.ambientDim} observable embedding dimensions, ${result.config.hubDim} planted hub coordinates, and binary judgments from nonlinear hub interactions. The recovered dimension count is ${result.recoveredHubDim}; the final LHV accuracy implies at least ${fmt(result.infoLowerBoundBits)} bits of value-relevant information per balanced binary judgment.`;
  container.appendChild(intro);
  const grid = document.createElement("div");
  grid.className = "lhv-grid";
  container.appendChild(grid);
  const spectrumCard = document.createElement("div");
  spectrumCard.className = "lhv-card";
  spectrumCard.appendChild(Object.assign(document.createElement("h3"), { textContent: "Parallel analysis" }));
  spectrumCard.appendChild(
    renderTable(
      ["PC", "eigen", "null 95%", "sig."],
      result.spectrum.map((r) => [String(r.component), fmt(r.eigenvalue), fmt(r.null95), r.significant ? "yes" : "no"])
    )
  );
  grid.appendChild(spectrumCard);
  const probeCard = document.createElement("div");
  probeCard.className = "lhv-card";
  probeCard.appendChild(Object.assign(document.createElement("h3"), { textContent: "Held-out prediction" }));
  probeCard.appendChild(
    renderTable(
      ["n", "raw AUC", "LHV AUC", "oracle AUC", "LHV acc."],
      result.probes.map((r) => [String(r.nTrain), fmt(r.rawAuc), fmt(r.lhvAuc), fmt(r.oracleAuc), fmt(r.lhvAccuracy)])
    )
  );
  grid.appendChild(probeCard);
  const note = document.createElement("div");
  note.className = "lhv-note";
  note.textContent = "Research toy only. It tests the experimental shape: hub structure can be recoverable and useful in a sample window where raw ambient features are harder to learn.";
  container.appendChild(note);
}
if (typeof window !== "undefined") {
  window.mountLhvLearnabilityDemo = mountLhvLearnabilityDemo;
  const autoMount = document.getElementById("lhv-learnability-demo");
  if (autoMount) mountLhvLearnabilityDemo(autoMount);
}
export {
  mountLhvLearnabilityDemo,
  runLhvExperiment
};

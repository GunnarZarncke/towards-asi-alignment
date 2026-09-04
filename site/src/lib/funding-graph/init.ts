import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import type { FundingGraphPayload } from "./build-payload";

cytoscape.use(dagre);

const FUNDING_GLYPH: Record<string, string> = {
  open: "○",
  unfunded: "∅",
  partial: "◐",
  funded: "●"
};

const DONE_GLYPH: Record<string, string> = {
  not_started: "□",
  partial: "◧",
  done: "■"
};

function cssVar(name: string, fallback: string) {
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return value || fallback;
}

function nodeLabel(node: FundingGraphPayload["nodes"][number]) {
  const funding = node.fundingState ? FUNDING_GLYPH[node.fundingState] ?? "" : "";
  const done = node.doneState ? DONE_GLYPH[node.doneState] ?? "" : "";
  const status = [funding, done].filter(Boolean).join(" ");
  return status ? `${node.label}\n${status}` : node.label;
}

export function initFundingDependencyGraph(
  root: HTMLElement,
  payload: FundingGraphPayload
) {
  const container = root.querySelector<HTMLElement>("[data-funding-graph-cy]");
  if (!container) return;

  const border = cssVar("--color-border", "#c8d4e0");
  const borderStrong = cssVar("--color-border-strong", "#8899aa");
  const accent = cssVar("--color-accent", "#336699");
  const text = cssVar("--color-text", "#1a2433");
  const bg = cssVar("--color-bg", "#ffffff");

  const elements = [
    ...payload.nodes.map((node) => ({
      data: {
        id: node.id,
        label: nodeLabel(node),
        href: node.href,
        fundingState: node.fundingState ?? "",
        doneState: node.doneState ?? ""
      }
    })),
    ...payload.edges.map((edge, index) => ({
      data: {
        id: `e-${index}-${edge.source}-${edge.target}`,
        source: edge.source,
        target: edge.target
      }
    }))
  ];

  const cy = cytoscape({
    container,
    elements,
    minZoom: 0.45,
    maxZoom: 1.5,
    wheelSensitivity: 0.18,
    layout: {
      name: "dagre",
      rankDir: "TB",
      nodeSep: 36,
      edgeSep: 24,
      rankSep: 72,
      animate: false
    },
    style: [
      {
        selector: "node",
        style: {
          label: "data(label)",
          "text-wrap": "wrap",
          "text-max-width": "120px",
          "text-valign": "center",
          "text-halign": "center",
          "font-size": "11px",
          "font-family": 'system-ui, -apple-system, "Segoe UI", sans-serif',
          color: text,
          "background-color": bg,
          "border-width": 2,
          "border-color": border,
          shape: "round-rectangle",
          width: "label",
          height: "label",
          padding: "14px"
        }
      },
      {
        selector: "node[fundingState = 'partial']",
        style: {
          "background-fill": "linear-gradient",
          "background-gradient-direction": "to-right",
          "background-gradient-stop-colors": `${borderStrong} ${bg}`,
          "background-gradient-stop-positions": "50% 50%"
        }
      },
      {
        selector: "node[fundingState = 'funded']",
        style: {
          "background-color": borderStrong,
          color: bg
        }
      },
      {
        selector: "node:active",
        style: {
          "overlay-opacity": 0
        }
      },
      {
        selector: "node:selected",
        style: {
          "border-color": accent,
          "border-width": 3
        }
      },
      {
        selector: "edge",
        style: {
          width: 2,
          "line-color": borderStrong,
          "target-arrow-color": borderStrong,
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
          "arrow-scale": 0.9
        }
      }
    ]
  });

  cy.on("tap", "node", (event) => {
    const href = event.target.data("href") as string | undefined;
    if (href) window.location.assign(href);
  });

  cy.on("mouseover", "node", (event) => {
    container.style.cursor = "pointer";
    event.target.style("border-color", accent);
  });

  cy.on("mouseout", "node", (event) => {
    container.style.cursor = "default";
    if (!event.target.selected()) {
      event.target.style("border-color", border);
    }
  });

  const fit = () => {
    cy.resize();
    cy.fit(undefined, 36);
  };

  fit();
  window.addEventListener("resize", fit);

  root.dataset.graphReady = "true";
  return cy;
}

// Copy selected experiment result figures into site/public/experiments/ for
// companion-site rendering (findings page + field-news cards).
import { cp, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");

/** @type {{ src: string; dest: string }[]} */
const FIGURES = [
  {
    src: "experiments/lab-simulation/results/et3_foster_trajectories_median.png",
    dest: "experiments/lab-simulation/et3_foster_trajectories_median.png"
  },
  {
    src: "experiments/lab-simulation/results/et3_foster_trajectories_sar_kde.png",
    dest: "experiments/lab-simulation/et3_foster_trajectories_sar_kde.png"
  }
];

async function sync() {
  for (const { src, dest } of FIGURES) {
    const from = path.join(repoRoot, src);
    const to = path.join(siteRoot, "public", dest);
    await mkdir(path.dirname(to), { recursive: true });
    await cp(from, to);
  }
  console.log(`[sync-experiment-figures] copied ${FIGURES.length} PNGs -> site/public/`);
}

sync().catch((err) => {
  console.error(err);
  process.exit(1);
});

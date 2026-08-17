// Generates field-v2.json (lifecycle roles + open spine interfaces) for /field/v2/ (live field hub).
// Usage: node scripts/sync-field-v2.mjs [--check]
import { readFile, writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(scriptDir, "..");
const repoRoot = path.resolve(siteRoot, "..");
const dataRoot = path.join(repoRoot, "reference", "field-agendas", "data");
const outPath = path.join(siteRoot, "src", "data", "field-v2.json");
const SYNC_CMD = "cd site && npm run sync:field-v2";

function generatedBanner() {
  return `<!-- GENERATED FILE — do not edit. Regenerate: ${SYNC_CMD} -->`;
}

async function loadYaml(name) {
  return yaml.load(await readFile(path.join(dataRoot, name), "utf8"));
}

async function writeFileCheck(filePath, contents, check, mismatches) {
  if (check) {
    let existing = "";
    try {
      existing = await readFile(filePath, "utf8");
    } catch {}
    if (existing !== contents) mismatches.push(filePath);
  } else {
    await mkdir(path.dirname(filePath), { recursive: true });
    await writeFile(filePath, contents, "utf8");
  }
}

async function main() {
  const check = process.argv.includes("--check");
  const meta = await loadYaml("meta.yml");
  const { bridges: bridgeRows } = await loadYaml("bridges.yml");
  const { bridges: lifecycleRows } = await loadYaml("bridges-v2.yml");
  const { openSpineInterfaces } = await loadYaml("open-spine-interfaces.yml");
  const lifecycle = await loadYaml("lifecycle.yml");
  const adjacentWork = await loadYaml("adjacent-work-v2.yml");
  const specifyConstruct = await loadYaml("specify-construct-instances.yml");

  const lifecycleByKey = Object.fromEntries(lifecycleRows.map((row) => [row.key, row]));

  const bridges = bridgeRows.map((row) => ({
    ...row,
    lifecycleRole: lifecycleByKey[row.key]?.lifecycleRole ?? null,
    leanCrux: lifecycleByKey[row.key]?.leanCrux ?? row.leanAxiom ?? null
  }));

  const lifecycleOrder = ["specify", "construct", "identify", "certify", "preserve"];
  const lifecyclePhases = lifecycleOrder.map((id) => ({
    id,
    label: lifecycle.phases[id]?.label ?? id,
    summary: lifecycle.phases[id]?.summary ?? ""
  }));

  const payload = {
    _generated: generatedBanner(),
    meta: {
      lifecycleIntro: lifecycle.intro,
      lifecycleBridgeAssignmentNote: lifecycle.bridgeAssignmentNote ?? "",
      lifecycleGapsNote: lifecycle.gapsNote ?? "",
      lifecycleAxis: lifecycleOrder.join(" → "),
      openSpineInterfaces: meta.openSpineInterfaces,
      note: "Live field hub at /field/ (redirects to /field/v2/). Archived v1 at /field/v1/.",
      adjacentWorkIntro: adjacentWork.intro ?? "",
      adjacentWorkFirewall: adjacentWork.firewall ?? "",
      adjacentWorkPhenomenalityNote: adjacentWork.phenomenalityNote ?? "",
      specifyConstructIntro: specifyConstruct.intro ?? "",
      specifyConstructPlaceholderNote: specifyConstruct.placeholderNote ?? ""
    },
    lifecyclePhases,
    bridges,
    openSpineInterfaces,
    adjacentWork: adjacentWork.items ?? [],
    specifyConstructInstances: specifyConstruct.instances ?? [],
    specifyConstructPeerRows: specifyConstruct.peerRows ?? []
  };

  const contents = JSON.stringify(payload, null, 2) + "\n";
  const mismatches = [];
  await writeFileCheck(outPath, contents, check, mismatches);

  if (check && mismatches.length > 0) {
    console.error(`sync-field-v2 --check: ${mismatches.length} file(s) out of date:`);
    for (const f of mismatches) console.error(`  ${path.relative(repoRoot, f)}`);
    process.exit(1);
  }
  console.log(`sync-field-v2: wrote field-v2.json (${check ? "check ok" : "generated"}).`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

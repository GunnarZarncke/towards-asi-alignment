#!/usr/bin/env node
/** Write stance mark SVGs to site/public/icons/stance/ */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { STANCE_ICON_IDS, STANCE_ICON_SVG } from "../../reference/field-agendas/scripts/stance-icons.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = path.join(root, "public", "icons", "stance");

fs.mkdirSync(outDir, { recursive: true });
for (const id of STANCE_ICON_IDS) {
  fs.writeFileSync(path.join(outDir, `${id}.svg`), STANCE_ICON_SVG[id], "utf8");
}
console.log(`sync-stance-icons: wrote ${STANCE_ICON_IDS.length} icons to public/icons/stance/`);

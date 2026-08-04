#!/usr/bin/env node
import path from "node:path";
import { fileURLToPath } from "node:url";
import { BOOK_PDF_FILENAME, fetchBookPdf } from "./lib/fetch-book-pdf-core.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "../..");
const outPath = path.join(repoRoot, "dist", "pdf", BOOK_PDF_FILENAME);

const { releaseTag } = await fetchBookPdf(outPath);
console.log(`Downloaded ${BOOK_PDF_FILENAME} from ${releaseTag} to ${outPath}`);

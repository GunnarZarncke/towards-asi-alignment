#!/usr/bin/env python3
"""Final bibliography URL/DOI cleanup: remove spurious Crossref matches, add landing URLs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "references"

# Remove spurious doi/url (Crossref title-search pollution on internal / misc entries).
REMOVE: dict[str, list[str]] = {
    "zarncke2025acausal": ["doi", "url"],
    "zarncke2025alignment-attractor": ["doi"],
    "zarncke2025biq": ["doi"],
    "zarncke2025consciousness-backbone": ["doi"],
    "zarncke2025construction": ["doi", "url"],
    "zarncke2025loop-hub-value": ["doi", "url"],
    "zarncke2025status-regulation": ["doi", "url"],
    "zarncke2025stratification": ["doi"],
    "zarncke2026access": ["doi", "url"],
    "zarncke2026rainbow": ["doi", "url"],
    "zarncke2026smoothing": ["doi", "url"],
    "zarncke2026stealth": ["doi", "url"],
    "dennett1981true": ["doi"],
    "descartes1996meditations": ["doi"],
    "euaiact2024": ["doi"],
    "gsn2021standard": ["doi"],
    "yeung2017hypernudge": ["doi"],
    "HenrichGilWhite2001": ["doi"],
}

# Set/replace fields (--force always overwrites listed fields).
SET: dict[str, dict[str, str]] = {
    "schwartz2012refining": {
        "url": "https://doi.apa.org/doiLanding?doi=10.1037/a0029393",
    },
    "klyubin2005empowerment": {"url": "https://ieeexplore.ieee.org/document/1554676/"},
    "rosas2020synergistic": {"url": "https://iopscience.iop.org/article/10.1088/1751-8121/abb723"},
    "variationalagent2025": {"url": "https://www.ijcai.org/proceedings/2025/538"},
    "btesh2022redressing": {
        "url": "https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/redressing-the-emperor-in-causal-clothing/S0140525X22000176",
    },
    "friston2021fepresponse": {"url": "https://www.mdpi.com/1099-4300/23/8/1076"},
    "hauskrecht2000value": {"url": "https://www.jair.org/index.php/jair/article/view/639"},
    "mcgregor2025intentional": {
        "url": "https://www.taylorfrancis.com/books/9781003632511/chapters/10.4324/9781003632511-9",
    },
    "euaiact2024": {
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689",
    },
    "biehl2020fepcritique": {"url": "https://www.mdpi.com/1099-4300/23/3/293"},
    "frankfurt1971freedom": {"url": "https://www.jstor.org/stable/2024717"},
    "graham2011mapping": {"url": "https://doi.apa.org/doiLanding?doi=10.1037/a0021847"},
    "yeung2017hypernudge": {
        "doi": "10.1080/1369118X.2016.1186713",
        "url": "https://www.tandfonline.com/doi/full/10.1080/1369118X.2016.1186713",
    },
    "gsn2021standard": {
        "doi": "10.65391/r1386",
        "url": "https://scsc.uk/r1386.pdf",
    },
    "bruineberg2021emperor": {
        "url": "https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/emperors-new-markov-blankets/E0531375A4AF5574261CE96E34701384",
    },
    "Chudek2011": {"url": "https://academic.oup.com/book/3522/chapter/144759521"},
    "frassle2014_binocular": {"url": "https://www.jneurosci.org/content/34/5/1738"},
    "freeman2023glial": {
        "url": "https://www.taylorfrancis.com/books/9781003444909/chapters/10.4324/9781003444909-12",
    },
    "gruber2022curiosity": {
        "year": "2016",
        "volume": "89",
        "number": "5",
        "pages": "1110--1120",
        "doi": "10.1016/j.neuron.2016.01.017",
        "url": "https://www.cell.com/neuron/fulltext/S0896-6273(16)00018-0",
    },
    "HenrichGilWhite2001": {
        "doi": "10.1016/S1090-5138(00)00071-4",
        "url": "https://www.sciencedirect.com/science/article/pii/S1090513800000714",
    },
    "albantakis2023integrated": {"url": "https://osf.io/preprints/psyarxiv/uscwt"},
    "descartes1996meditations": {
        "url": "https://www.cambridge.org/core/books/meditations-on-first-philosophy/1315896411",
    },
    "fleming2014_how": {
        "url": "https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2014.00443/full",
    },
    "Graziano2013": {
        "url": "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00412/full",
    },
    "milliere2018psychedelics": {
        "url": "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2018.01475/full",
    },
    "morales2018_domain": {"url": "https://www.jneurosci.org/content/38/14/3534"},
    "rosenthal2005_consciousness": {"url": "https://academic.oup.com/book/49740"},
    "Ryle1949": {"url": "https://philpapers.org/rec/RYLRCO"},
}


def find_block(text: str, key: str) -> tuple[int, int, str] | None:
    m = re.search(rf"@\w+\{{{re.escape(key)},", text)
    if not m:
        return None
    start = m.start()
    nxt = text.find("\n@", start + 1)
    end = nxt if nxt != -1 else len(text)
    return start, end, text[start:end]


def remove_fields(block: str, fields: list[str]) -> str:
    for field in fields:
        block = re.sub(rf",?\n\s*{re.escape(field)}\s*=\s*\{{[^}}]*\}}", "", block)
    return block


def set_fields(block: str, fields: dict[str, str]) -> str:
    for field, val in fields.items():
        pat = rf"^\s*{re.escape(field)}\s*=\s*\{{[^}}]*\}}"
        repl = f"  {field} = {{{val}}}"
        if re.search(pat, block, re.M):
            block = re.sub(pat, repl, block, count=1, flags=re.M)
        else:
            close = block.rfind("}")
            body = block[:close].rstrip()
            sep = "\n" if body.endswith(",") else ",\n"
            block = body + sep + repl + ",\n" + block[close:]
    return block


def main() -> int:
    changed = 0
    for bib in sorted(REFS.glob("*.bib")):
        if bib.name == "main.bib":
            continue
        text = bib.read_text()
        orig = text
        for key, fields in REMOVE.items():
            hit = find_block(text, key)
            if not hit:
                continue
            start, end, block = hit
            nb = remove_fields(block, fields)
            if nb != block:
                text = text[:start] + nb + text[end:]
                changed += 1
        for key, fields in SET.items():
            hit = find_block(text, key)
            if not hit:
                continue
            start, end, block = hit
            nb = set_fields(block, fields)
            if nb != block:
                text = text[:start] + nb + text[end:]
                changed += 1
        if text != orig:
            bib.write_text(text)
    print(f"Updated {changed} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

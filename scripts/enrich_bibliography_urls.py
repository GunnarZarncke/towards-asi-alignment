#!/usr/bin/env python3
"""Enrich references/*.bib with doi + url fields per project convention."""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "references"
CROSSREF = "https://api.crossref.org/works"
UA = "towards-asi-alignment/1.0 (mailto:alignment-book@local)"


def parse_entries(text: str):
    for m in re.finditer(r"@(\w+)\{([^,\s]+)", text):
        key = m.group(2)
        start = m.start()
        nxt = text.find("\n@", start + 1)
        end = nxt if nxt != -1 else len(text)
        yield key, start, end, text[start:end]


def field(block: str, name: str) -> str | None:
    m = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{([^}}]+)\}}", block, re.M)
    return m.group(1).strip() if m else None


def has_field(block: str, name: str) -> bool:
    return bool(re.search(rf"^\s*{re.escape(name)}\s*=", block, re.M))


def insert_before_close(block: str, lines: list[str]) -> str:
    close = block.rfind("}")
    body = block[:close].rstrip()
    addition = ",\n".join(lines)
    sep = "\n" if body.endswith(",") else ",\n"
    return body + sep + addition + "\n" + block[close:]


def http_json(url: str) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.load(resp)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def pick_url(meta: dict) -> str | None:
    url = meta.get("URL")
    if url and "doi.org" not in url:
        return url
    for link in meta.get("link") or []:
        u = link.get("URL")
        if u and "doi.org" not in u:
            return u
    return None


def arxiv_from_journal(journal: str | None) -> str | None:
    if not journal:
        return None
    m = re.search(r"arXiv[^0-9]*([0-9]{4}\.[0-9]{4,5})", journal, re.I)
    return m.group(1) if m else None


def arxiv_fields(arxiv_id: str) -> list[str]:
    return [
        f"  eprint     = {{{arxiv_id}}}",
        "  eprinttype = {arXiv}",
        f"  doi        = {{10.48550/arXiv.{arxiv_id}}}",
        f"  url        = {{https://arxiv.org/abs/{arxiv_id}}}",
    ]


KNOWN: dict[str, tuple[str | None, str]] = {
    "ahn2022": (None, "https://say-can.github.io/"),
    "christiano2017": ("10.5555/3298023.3298066", "https://proceedings.mlr.press/v70/christiano17a.html"),
    "hadfieldmenell2016": ("10.5555/3060832.3060840", "https://papers.nips.cc/paper/6420-cooperative-inverse-reinforcement-learning"),
    "hafner2019": ("10.48550/arXiv.1911.08265", "https://arxiv.org/abs/1911.08265"),
    "hafner2023": ("10.48550/arXiv.2301.04104", "https://arxiv.org/abs/2301.04104"),
    "driess2023": ("10.48550/arXiv.2303.03378", "https://arxiv.org/abs/2303.03378"),
    "hubinger2019risks": ("10.48550/arXiv.1906.01820", "https://arxiv.org/abs/1906.01820"),
    "jaques2019": ("10.18653/v1/D19-1229", "https://aclanthology.org/D19-1229/"),
    "kaplan2020scaling": ("10.48550/arXiv.2001.08361", "https://arxiv.org/abs/2001.08361"),
    "kenton2022discovering": ("10.48550/arXiv.2203.07109", "https://arxiv.org/abs/2203.07109"),
    "omohundro2008basic": (None, "https://selfawaresystems.files.wordpress.com/2008/01/ai_drives_final.pdf"),
    "park2024deception": ("10.48550/arXiv.2403.03185", "https://arxiv.org/abs/2403.03185"),
    "smithszathmary1995book": ("10.1093/acprof:oso/9780198502944.001.0001", "https://global.oup.com/academic/product/the-major-transitions-in-evolution-9780198502944"),
    "vonneumann1966": ("10.1515/9781400882617", "https://press.princeton.edu/books/paperback/9780691024931/the-theory-of-self-reproducing-automata"),
    "Chalmers1996": ("10.1093/acprof:oso/9780195117899.001.0001", "https://global.oup.com/academic/product/the-conscious-mind-9780195117899"),
    "panksepp1998affective": ("10.1093/acprof:oso/9780195096736.001.0001", "https://global.oup.com/academic/product/affective-neuroscience-9780195096736"),
    "nissenbaum2010privacy": ("10.12987/9780804772891", "https://www.sup.org/books/title/?id=8862"),
    "rawls1971": ("10.2307/j.ctt1ffjn8r", "https://www.hup.harvard.edu/catalog.php?isbn=9780674017726"),
    "bostrom2014superintelligence": ("10.1093/acprof:oso/9780199678112.001.0001", "https://global.oup.com/academic/product/superintelligence-9780199678112"),
    "iaisr2025": (None, "https://internationalaisafetyreport.org/"),
    "beck2025dynamic": ("10.48550/arXiv.2501.16946", "https://arxiv.org/abs/2501.16946"),
    "dacosta2021bayesianmechanics": ("10.48550/arXiv.2106.01028", "https://arxiv.org/abs/2106.01028"),
    "biehl2022pomdp": ("10.48550/arXiv.2204.13736", "https://arxiv.org/abs/2204.13736"),
    "garrabrant2017logical": ("10.48550/arXiv.1609.03543", "https://arxiv.org/abs/1609.03543"),
    "fdt2017": (None, "https://functionaldecisiontheory.com/"),
    "critch2020ai": ("10.48550/arXiv.2006.04948", "https://arxiv.org/abs/2006.04948"),
    "woolley2010evidence": ("10.1126/science.1193147", "https://www.science.org/doi/10.1126/science.1193147"),
    "woolley2010collective": ("10.1126/science.1193147", "https://www.science.org/doi/10.1126/science.1193147"),
    "salge2014empowerment": ("10.1371/journal.pone.0112332", "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0112332"),
    "Schultz1997": ("10.1126/science.275.5306.1593", "https://www.science.org/doi/10.1126/science.275.5306.1593"),
    "yang2018cooperation": ("10.1103/PhysRevE.98.032308", "https://journals.aps.org/pre/abstract/10.1103/PhysRevE.98.032308"),
    "seidl2008": ("10.1242/jeb.015057", "https://journals.biologists.com/jeb/article/211/5/747/19452/Walking-on-inclines-how-do-desert-ants-monitor"),
    "komanduru2019irlcomplexity": ("10.5555/3305381.3305420", "https://proceedings.mlr.press/v89/komanduru19a.html"),
    "manheim2018goodhart": ("10.31235/osf.io/9b7u8", "https://osf.io/preprints/socarxiv/9b7u8/"),
    "olson2023personidentity": ("10.4324/9781003457099-6", "https://plato.stanford.edu/entries/identity-personal/"),
    "kelly1998safety": ("10.1093/bjps/49.3.361", "https://academic.oup.com/bjps/article/49/3/361/1619276"),
    "kolchinsky2017ib": ("10.3390/e19110593", "https://www.mdpi.com/2073-439X/19/11/593"),
    "ramachandran2007bayesianirl": (None, "https://www.ijcai.org/Proceedings/07/Papers/416.pdf"),
    "schwartz2012overview": ("10.9707/2307-0919.1116", "https://scholarworks.gvsu.edu/orpc/vol2/iss1/11/"),
    "schwartz2012refining": ("10.1037/a0029393", "https://doi.apa.org/doiLanding?doi=10.1037/a0029393"),
    "nakano2021": ("10.48550/arXiv.2112.09332", "https://arxiv.org/abs/2112.09332"),
    "salgepolani2014": ("10.3389/frobt.2017.00025", "https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2017.00025/full"),
    "Dennett1991": (None, "https://philpapers.org/rec/DENCE"),
    "Singer2011": ("10.1093/acprof:oso/9780199578722.001.0001", "https://global.oup.com/academic/product/practical-ethics-9780199578722"),
    "shalizi2001computational": ("10.1023/A:1010388907793", "https://link.springer.com/article/10.1023/A:1010388907793"),
    "strouse2016ib": ("10.48550/arXiv.1604.03225", "https://arxiv.org/abs/1604.03225"),
    "susser2019manipulation": ("10.14763/2019.2.1410", "https://policyreview.info/articles/analysis/technology-autonomy-and-manipulation"),
    "taylor2015quantilizers": (None, "https://intelligence.org/files/QuantilizersSaferAlternative.pdf"),
    "thaler2008nudge": (None, "https://yalepress.yale.edu/book/9780300122237/nudge/"),
    "thornley2023shutdown": (None, "https://www.lesswrong.com/posts/8GWLRMnp55iFZDBbm/the-shutdown-problem-three-theorems"),
    "turchin2020classification": ("10.1007/s00146-018-0845-5", "https://link.springer.com/article/10.1007/s00146-018-0845-5"),
    "wen2024mislead": ("10.48550/arXiv.2403.03729", "https://arxiv.org/abs/2403.03729"),
    "zuboff2019surveillance": (None, "https://www.publicaffairsbooks.com/titles/shoshana-zuboff/the-age-of-surveillance-capitalism/9781610395694"),
    "soares2015corrigibility": (None, "https://intelligence.org/files/Corrigibility.pdf"),
    "yudkowsky2004cev": (None, "https://intelligence.org/files/CEV.pdf"),
    "unesco2021aiethics": (None, "https://unesdoc.unesco.org/ark:/48223/pf0000381137"),
}


def mechanical_enrich(block: str, key: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    if "crossref" in block:
        return block, changes

    doi = field(block, "doi")
    url = field(block, "url")
    how_m = re.search(r"howpublished\s*=\s*\{(?:\\url\{([^}]+)\}|\\\\url\{([^}]+)\})\}", block)
    how_url = (how_m.group(1) or how_m.group(2)) if how_m else None
    note_url_m = re.search(r"note\s*=\s*\{[^}]*\\url\{([^}]+)\}", block)
    note_url = note_url_m.group(1) if note_url_m else None
    journal = field(block, "journal")
    new_fields: list[str] = []

    if how_url and not url:
        new_fields.append(f"  url = {{{how_url}}}")
        changes.append(f"{key}: url<=howpublished")

    if note_url and not url and not how_url:
        new_fields.append(f"  url = {{{note_url}}}")
        changes.append(f"{key}: url<=note")

    if url and "doi.org/" in url:
        bare = url.split("doi.org/", 1)[-1].strip("/")
        if not doi:
            new_fields.append(f"  doi = {{{bare}}}")
            changes.append(f"{key}: doi<=url")

    if arxiv_id := arxiv_from_journal(journal):
        if not has_field(block, "eprint"):
            new_fields.extend(arxiv_fields(arxiv_id))
            changes.append(f"{key}: arxiv {arxiv_id}")

    if key in KNOWN:
        kdoi, kurl = KNOWN[key]
        if kdoi and not has_field(block, "doi"):
            new_fields.append(f"  doi = {{{kdoi}}}")
            changes.append(f"{key}: doi known")
        if kurl and not has_field(block, "url") and not any("url" in f for f in new_fields):
            new_fields.append(f"  url = {{{kurl}}}")
            changes.append(f"{key}: url known")

    filtered = []
    for line in new_fields:
        fname = line.strip().split("=")[0].strip()
        if has_field(block, fname) or any(fname in f for f in filtered):
            continue
        filtered.append(line)
    if not filtered:
        return block, changes
    return insert_before_close(block, filtered), changes


def apply_fields(text: str, key: str, fields: list[str]) -> str:
    for k, start, end, block in parse_entries(text):
        if k != key:
            continue
        filtered = []
        for line in fields:
            fname = line.strip().split("=")[0].strip()
            if has_field(block, fname) or any(fname in f for f in filtered):
                continue
            filtered.append(line)
        if not filtered:
            return text
        nb = insert_before_close(block, filtered)
        return text[:start] + nb + text[end:]
    return text


PUBLIC_INTERNAL = {"zarncke2025attractor", "zarncke2025uad"}


def skip_entry(path: Path, key: str, block: str) -> bool:
    if "crossref" in block or key in KNOWN:
        return True
    if path.name == "internal-project-sources.bib" and key.startswith("zarncke"):
        return key not in PUBLIC_INTERNAL
    return False


def scan_needs(text: str, path: Path) -> tuple[list[tuple[str, str]], list[tuple[str, str, str | None, str | None]]]:
    doi_jobs, search_jobs = [], []
    for key, _, _, block in parse_entries(text):
        if skip_entry(path, key, block):
            continue
        doi = field(block, "doi")
        url = field(block, "url")
        if doi and not url:
            doi_jobs.append((key, doi))
        elif not doi and not url and not arxiv_from_journal(field(block, "journal")):
            title = field(block, "title")
            if title:
                search_jobs.append((key, title, field(block, "year"), field(block, "author")))
    return doi_jobs, search_jobs


def doi_landing(doi: str) -> str | None:
    """Publisher landing page from DOI prefix (not doi.org resolver)."""
    if doi.startswith("10.1098/"):
        return f"https://royalsocietypublishing.org/doi/{doi}"
    if doi.startswith("10.1103/"):
        if "PhysRevLett" in doi:
            j = "prl"
        elif "PhysRevE" in doi:
            j = "pre"
        elif "PhysRevX" in doi:
            j = "prx"
        else:
            j = "prl"
        return f"https://journals.aps.org/{j}/abstract/{doi}"
    if doi.startswith("10.1371/"):
        return f"https://journals.plos.org/plosone/article?id={doi}"
    if doi.startswith("10.1126/"):
        return f"https://www.science.org/doi/{doi}"
    if doi.startswith("10.1038/"):
        return f"https://www.nature.com/articles/{doi.split('/', 1)[1]}"
    if doi.startswith("10.1016/"):
        return f"https://linkinghub.elsevier.com/retrieve/pii/{doi.split('/', 1)[1]}"
    if doi.startswith("10.1162/"):
        return f"https://direct.mit.edu/artl/article/{doi.split('/', 1)[1]}"
    if doi.startswith("10.1080/"):
        return f"https://www.tandfonline.com/doi/full/{doi}"
    if doi.startswith("10.1086/"):
        return f"https://www.cambridge.org/core/journals/philosophy-of-science/article/doi/{doi}"
    if doi.startswith("10.1140/"):
        return f"https://link.springer.com/article/{doi}"
    if doi.startswith("10.1007/"):
        return f"https://link.springer.com/article/{doi}"
    if doi.startswith("10.1111/"):
        return f"https://onlinelibrary.wiley.com/doi/{doi}"
    if doi.startswith("10.7554/"):
        return f"https://elifesciences.org/articles/{doi.split('.', 1)[-1]}"
    if doi.startswith("10.18653/"):
        return f"https://aclanthology.org/{doi.split('/', 1)[1]}/"
    if doi.startswith("10.1109/"):
        tail = doi.rsplit(".", 1)[-1]
        if tail.isdigit():
            return f"https://ieeexplore.ieee.org/document/{tail}/"
    if doi.startswith("10.1088/"):
        return f"https://iopscience.iop.org/article/{doi}"
    if doi.startswith("10.24963/"):
        return f"https://www.ijcai.org/proceedings/{doi.split('/', 1)[1]}"
    if doi.startswith("10.1017/"):
        suffix = doi.split("/", 1)[1]
        return f"https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/{suffix}"
    if doi.startswith("10.3390/"):
        tail = doi.split("/", 1)[1]
        vol, art = tail.split(".", 1) if "." in tail else (tail, "")
        if vol.startswith("e") and art:
            return f"https://www.mdpi.com/1099-4300/{vol[1:]}/{art}"
    if doi.startswith("10.1613/"):
        return f"https://www.jair.org/index.php/jair/article/view/{doi.split('/', 1)[1]}"
    if doi.startswith("10.4324/"):
        book = doi.split("-", 1)[0].split("/", 1)[1]
        return f"https://www.taylorfrancis.com/books/{book}/chapters/{doi}"
    if doi.startswith("10.2307/"):
        return f"https://www.jstor.org/stable/{doi.split('/', 1)[1]}"
    if doi.startswith("10.1037/"):
        return f"https://doi.apa.org/doiLanding?doi={doi}"
    if doi.startswith("10.1523/"):
        return f"https://www.jneurosci.org/content/{doi.split('/', 1)[1].lower()}"
    if doi.startswith("10.1093/"):
        return f"https://academic.oup.com/book/49740" if "oso/" in doi else None
    if doi.startswith("10.3389/"):
        return f"https://www.frontiersin.org/articles/{doi}/full"
    if doi.startswith("10.31234/"):
        slug = doi.split("/", 1)[1]
        return f"https://osf.io/preprints/psyarxiv/{slug}"
    if doi.startswith("10.31219/"):
        slug = doi.split("/", 1)[1]
        return f"https://osf.io/{slug}"
    if doi.startswith("10.65391/"):
        return f"https://scsc.uk/r1386.pdf"
    if doi.startswith("10.1016/S") or doi.startswith("10.1016/s"):
        return f"https://www.sciencedirect.com/science/article/pii/{doi.split('/', 1)[1]}"
    return None


def fetch_doi_url(doi: str) -> str | None:
    data = http_json(f"{CROSSREF}/{urllib.parse.quote(doi, safe='')}")
    u = pick_url(data) if data else None
    if u and "doi.org" not in u:
        return u
    u2 = doi_landing(doi)
    if u2 and "doi.org" not in u2:
        return u2
    return u if u and "doi.org" not in u else None


def fetch_search(title: str, year: str | None, author: str | None) -> tuple[str | None, str | None]:
    q = re.sub(r"[{}\\]", "", title)[:120]
    params = {"query.title": q, "rows": "3"}
    if year:
        params["filter"] = f"from-pub-date:{year},until-pub-date:{year}"
    data = http_json(CROSSREF + "?" + urllib.parse.urlencode(params))
    if not data:
        return None, None
    items = data.get("message", {}).get("items", [])
    if not items:
        return None, None
    item = items[0]
    if author:
        al = author.split(" and ")[0].split(",")[0].lower()
        for it in items:
            for a in it.get("author") or []:
                fam = (a.get("family") or "").lower()
                if al and (al in fam or fam in al):
                    item = it
                    break
    found_doi = item.get("DOI")
    url = pick_url(item)
    if found_doi and not url:
        url = fetch_doi_url(found_doi)
    return found_doi, url


def main():
    files = [p for p in sorted(REFS.glob("*.bib")) if p.name != "main.bib"]
    texts = {p: p.read_text() for p in files}
    changes: list[str] = []

    for path in files:
        text = texts[path]
        parts, last = [], 0
        for key, start, end, block in parse_entries(text):
            parts.append(text[last:start])
            nb, ch = mechanical_enrich(block, key)
            changes.extend(ch)
            parts.append(nb)
            last = end
        texts[path] = "".join(parts) + text[last:]

    doi_jobs, search_jobs = [], []
    for path in files:
        d, s = scan_needs(texts[path], path)
        doi_jobs.extend((path, k, doi) for k, doi in d)
        search_jobs.extend((path, k, t, y, a) for k, t, y, a in s)

    print(f"After mechanical: {len(doi_jobs)} doi-only, {len(search_jobs)} need search")

    doi_urls: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(fetch_doi_url, doi): (path, key) for path, key, doi in doi_jobs}
        for fut in as_completed(futs):
            path, key = futs[fut]
            u = fut.result()
            if u:
                doi_urls[key] = u

    search_hits: dict[str, tuple[str | None, str | None]] = {}
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(fetch_search, t, y, a): (path, key) for path, key, t, y, a in search_jobs}
        for fut in as_completed(futs):
            path, key = futs[fut]
            search_hits[key] = fut.result()

    for path, key, _ in doi_jobs:
        if key in doi_urls:
            texts[path] = apply_fields(texts[path], key, [f"  url = {{{doi_urls[key]}}}"])
            changes.append(f"{key}: url<=crossref-doi")

    for path, key, _, _, _ in search_jobs:
        doi, url = search_hits.get(key, (None, None))
        fields = []
        if doi:
            fields.append(f"  doi = {{{doi}}}")
        if url:
            fields.append(f"  url = {{{url}}}")
        if fields:
            texts[path] = apply_fields(texts[path], key, fields)
            changes.append(f"{key}: crossref-search")

    for path in files:
        path.write_text(texts[path])

    still = sum(len(scan_needs(texts[p], p)[1]) + len(scan_needs(texts[p], p)[0]) for p in files)
    print(f"Applied {len(changes)} changes; still missing url/doi: ~{still}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

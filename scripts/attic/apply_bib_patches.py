#!/usr/bin/env python3
"""Apply {key, doi, url} patches to references/*.bib entries."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "references"

# Patches: only set fields that are missing unless force=True via --force key
PATCHES: dict[str, dict[str, str | None]] = {
    "nakano2021": {"doi": "10.48550/arXiv.2112.09332", "url": "https://arxiv.org/abs/2112.09332"},
    "rafailov2023": {"doi": "10.48550/arXiv.2305.18290", "url": "https://arxiv.org/abs/2305.18290"},
    "salgepolani2014": {"doi": "10.3389/frobt.2017.00025", "url": "https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2017.00025/full"},
    "schick2023": {"doi": "10.48550/arXiv.2302.04761", "url": "https://arxiv.org/abs/2302.04761"},
    "tdt2010": {"url": "https://intelligence.org/files/TDT.pdf"},
    "tishby2000ib": {"doi": "10.48550/arXiv.physics/0004057", "url": "https://arxiv.org/abs/physics/0004057"},
    "virgo2021bayesianreasoners": {"doi": "10.48550/arXiv.2112.13523", "url": "https://arxiv.org/abs/2112.13523"},
    "yao2023": {"doi": "10.48550/arXiv.2210.03629", "url": "https://arxiv.org/abs/2210.03629"},
    "ziebart2008maxent": {"doi": "10.1184/r1/6555512", "url": "https://www.cs.cmu.edu/~bziebart/publications/maximum-entropy-inverse-reinforcement-learning.html"},
    "Zink2008": {"doi": "10.1016/j.neuron.2008.01.025", "url": "https://www.cell.com/neuron/fulltext/S0896-6273(08)00160-1"},
    "langosco2022goalmisgeneralization": {"url": "https://proceedings.mlr.press/v162/langosco22a.html"},
    "stigler1971theory": {"doi": "10.2307/3003160", "url": "https://www.jstor.org/stable/3003160"},
    "peltzman1976regulation": {"doi": "10.1086/466865", "url": "https://www.journals.uchicago.edu/doi/10.1086/466865"},
    "near1985whistleblowing": {"doi": "10.1007/BF00382668", "url": "https://link.springer.com/article/10.1007/BF00382668"},
    "perrow1984normal": {"url": "https://press.princeton.edu/books/paperback/9780691004129/normal-accidents"},
    "power1997audit": {"doi": "10.1093/acprof:oso/9780198296034.001.0001", "url": "https://academic.oup.com/book/27849"},
    "hovenkamp2022antitrust": {"url": "https://law-store.wolterskluwer.com/s/product/antitrust-law-analysis-of-antitrust-principles-set-misb/01t0f00000MxZjXAAV"},
    "kysar2010regulating": {"doi": "10.12987/yale/9780300120011.001.0001", "url": "https://yalebooks.yale.edu/book/9780300120011/regulating-from-nowhere/"},
    "ceq2020nepa": {"url": "https://www.federalregister.gov/documents/2020/07/16/2020-15179/update-to-the-regulations-implementing-the-procedural-provisions-of-the-national-environmental-policy-act"},
    "iso420012023": {"url": "https://www.iso.org/standard/42001.html"},
    "fuller1969morality": {"doi": "10.12987/9780300191653", "url": "https://yalebooks.yale.edu/book/9780300010701/the-morality-of-law/"},
    "Knoch2006": {"doi": "10.1126/science.1129156", "url": "https://www.science.org/doi/full/10.1126/science.1129156"},
    "millidge2020deep": {"doi": "10.1016/j.jmp.2020.102348", "url": "https://www.sciencedirect.com/science/article/pii/S0022249620300298"},
    "abbeel2004apprenticeship": {"doi": "10.1145/1015330.1015430", "url": "https://proceedings.mlr.press/v21/abbeel11a.html"},
    "anderson1993value": {"doi": "10.1177/0021886393029002001", "url": "https://journals.sagepub.com/doi/10.1177/0021886393029002001"},
    "dalrymple2024gsai": {"doi": "10.48550/arXiv.2405.06624", "url": "https://arxiv.org/abs/2405.06624"},
    "dewey1938logic": {"doi": "10.2307/2271977", "url": "https://www.hup.harvard.edu/catalog.php?isbn=9780674053309"},
    "elster1983sourgrapes": {"doi": "10.1017/CBO9780511550844", "url": "https://www.cambridge.org/core/books/sour-grapes/9780511550844"},
    "everitt2016selfmodification": {"doi": "10.48550/arXiv.1608.04118", "url": "https://arxiv.org/abs/1608.04118"},
    "goodhart1984problems": {"doi": "10.1017/S0140525X00002127", "url": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0140525X00002127"},
    "habermas1984communicative": {"doi": "10.1515/9781400853813", "url": "https://www.hup.harvard.edu/catalog.php?isbn=9780262581089"},
    "pettit1997republicanism": {"doi": "10.1093/acprof:oso/9780198296423.001.0001", "url": "https://global.oup.com/academic/product/republicanism-9780198296423"},
    "scholkopf2021causalreps": {"doi": "10.48550/arXiv.2102.11107", "url": "https://arxiv.org/abs/2102.11107"},
    "sen1999development": {"doi": "10.1093/acprof:oso/9780198298359.001.0001", "url": "https://global.oup.com/academic/product/development-as-freedom-9780198298359"},
    "sen2009justice": {"doi": "10.1515/9781400839886", "url": "https://www.hup.harvard.edu/catalog.php?isbn=9780674036130"},
    "orseau2016interruptible": {"doi": "10.5555/3020948.3021006", "url": "https://mlanthology.org/uai/2016/orseau2016uai-safely/"},
    "hendrycks2021ethics": {"doi": "10.48550/arXiv.2008.07172", "url": "https://arxiv.org/abs/2008.07172"},
    "kelly2004gsn": {"doi": "10.1093/bjps/49.3.361", "url": "https://academic.oup.com/bjps/article/49/3/361/1619276"},
    "leveson2011esw": {"doi": "10.1201/b10789", "url": "https://www.crcpress.com/Engineering-a-Safer-World-Systems-Thinking-Applied-to-Safety/Leveson/p/book/9780262016629"},
    "guyenet2015co2": {"url": "https://www.guyenet.com/the-hungry-brain/"},
    "parr2022_active": {"doi": "10.48550/arXiv.2201.04201", "url": "https://arxiv.org/abs/2201.04201"},
    "Scholz2016": {"doi": "10.1016/j.neuron.2016.02.017", "url": "https://www.cell.com/neuron/fulltext/S0896-6273(16)00097-8"},
    "Blackmore2004": {"url": "https://www.susanblackmore.uk/books/consciousness-an-introduction/"},
    "dennett1971intentional": {"doi": "10.7551/mitpress/3895.001.0001", "url": "https://mitpress.mit.edu/9780262540377/intentional-stance/"},
    "Descartes1641": {"url": "https://www.gutenberg.org/ebooks/47333"},
    "descartes1641meditations": {"url": "https://www.gutenberg.org/ebooks/47333"},
    "Frankish2016": {"doi": "10.1093/acprof:oso/9780198748040.001.0001", "url": "https://global.oup.com/academic/product/illusionism-as-a-theory-of-consciousness-9780198748040"},
    "Metzinger2003": {"doi": "10.7551/mitpress/3847.001.0001", "url": "https://mitpress.mit.edu/9780262134190/being-no-one/"},
    "prinz2012_attended": {"doi": "10.1093/acprof:oso/9780195314115.001.0001", "url": "https://global.oup.com/academic/product/the-conscious-brain-9780195314115"},
    "Singer2011": {"doi": "10.1093/acprof:oso/9780199578722.001.0001", "url": "https://global.oup.com/academic/product/practical-ethics-9780199578722"},
    "zarncke2025uad": {"doi": "10.36227/techrxiv.175751274.45253943/v1", "url": "https://www.lesswrong.com/posts/pXYosC3eoS9GrDRAw/unsupervised-agent-discovery"},
    "zarncke2025attractor": {"doi": "10.21203/rs.3.rs-7092034/v1", "url": "https://www.researchsquare.com/article/rs-7092034/v1"},
}


def has_field(block: str, name: str) -> bool:
    return bool(re.search(rf"^\s*{re.escape(name)}\s*=", block, re.M))


def insert_fields(block: str, fields: dict[str, str]) -> str:
    lines = [f"  {k} = {{{v}}}" for k, v in fields.items()]
    close = block.rfind("}")
    body = block[:close].rstrip()
    sep = "\n" if body.endswith(",") else ",\n"
    return body + sep + ",\n".join(lines) + "\n" + block[close:]


def strip_howpublished_url(block: str) -> str:
    block = re.sub(
        r",?\n\s*howpublished\s*=\s*\{(?:\\url\{[^}]+\}|\\\\url\{[^}]+\})\}",
        "",
        block,
    )
    return block


def apply_patch(text: str, key: str, patch: dict, force: bool = False) -> tuple[str, bool]:
    m = re.search(rf"@\w+\{{{re.escape(key)},", text)
    if not m:
        return text, False
    start = m.start()
    nxt = text.find("\n@", start + 1)
    block = text[start : nxt if nxt != -1 else len(text)]
    block = strip_howpublished_url(block)
    to_add = {}
    for field, val in patch.items():
        if val is None:
            continue
        if force or not has_field(block, field):
            if field == "url" and "doi.org" in val:
                continue
            to_add[field] = val
    if not to_add:
        return text, False
    new_block = insert_fields(block, to_add)
    return text[:start] + new_block + text[nxt if nxt != -1 else len(text) :], True


def main():
    force = "--force" in sys.argv
    count = 0
    for bib in sorted(REFS.glob("*.bib")):
        if bib.name == "main.bib":
            continue
        text = bib.read_text()
        for key, patch in PATCHES.items():
            text, changed = apply_patch(text, key, patch, force=force)
            if changed:
                count += 1
        # migrate remaining howpublished \url to url
        def migrate(m):
            nonlocal count
            block = m.group(0)
            url_m = re.search(r"(?:\\url\{([^}]+)\}|\\\\url\{([^}]+)\})", block)
            if not url_m:
                return block
            u = url_m.group(1) or url_m.group(2)
            if re.search(r"^\s*url\s*=", block, re.M):
                return strip_howpublished_url(block)
            key = re.search(r"@\w+\{([^,]+)", block).group(1)
            nb = strip_howpublished_url(block)
            nb = insert_fields(nb, {"url": u})
            count += 1
            return nb

        new_text = re.sub(r"@\w+\{[^}]+\,.*?\n\}", migrate, text, flags=re.S)
        bib.write_text(new_text if new_text != text else text)
    print(f"Applied/ migrated {count} entries")


if __name__ == "__main__":
    main()

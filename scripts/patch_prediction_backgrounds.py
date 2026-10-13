#!/usr/bin/env python3
"""One-off: split catalog market backgrounds (Markets 3–13, 15–18)."""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEX = REPO / "appendices" / "appP-bridge-predictions.tex"

REGISTRY_TAIL = re.compile(
    r"\n\nBars, qualification, freeze, and reporting live in the \\claimspage\{[^}]+\}\{[^}]+\}\. "
    r"A Metaculus admin reads the named outcome file at a snapshot tag; they do not rescore papers\. "
    r"Published work counts whoever files it\. Metaculus resolves the \\texttt\{outcome\} field at git tag \\texttt\{snapshot-0\}\.\n"
    r"The host is still not independent of this book; attempts by aintelope or Gunnar Zarncke are not accepted\.",
    re.MULTILINE,
)

GLOSS = re.compile(
    r": YES \(at least one qualifying attempt met the frozen performance bars\), NO \(every qualifying attempt missed those bars\), or OTHER \(no qualifying attempt existed\)\?"
)

MARKETS = {
    3: {
        "metaculus": "Is it possible to tell who or what a safety rule still applies to after a system changes?",
        "background": r"""After continuity, fission or fusion, reassignment, or ontology change, the question is whether a safety-relevant rule still picks out the same bearer.
Example rules include ``Do not harm Alice,'' ``Protect all currently authorized users,'' and ``This account's owner has withdrawal rights.''
The benchmark must contain all four failure families: gradual replacement or migration; one entity split into two or two merged into one; names, accounts, or roles reassigned while the underlying entities remain; and concept change when the new system represents relevant entities differently.
Admitting previously unseen kinds of entities is a separate question.

See also \href{https://towards-alignment.com/cards/who-the-rules-still-apply-to/}{this plain language description}.""",
    },
    4: {
        "metaculus": "Is it possible for a broadly capable AI system to reliably take up authorized corrections?",
        "background": r"""Authorized correction means a human or institution can change what the system is allowed or required to do, and the system actually changes its later behavior---not only agrees in words.
The required correction cases are four: changing an objective while an old objective remains easier; revoking a previously permitted class of actions; changing which humans or organizations may authorize actions; and imposing a new safety constraint that conflicts with task reward.
At least one tested correction must not be enforceable merely by externally removing a tool or hard-coding a block.
Fake, unsigned, or unauthorized ``corrections'' must fail, and attacks that capture or reroute the correction interface cannot pass while leaving nominal compliance in place.

See also \href{https://towards-alignment.com/cards/correction-channel-integrity/}{this plain language description}.""",
    },
    5: {
        "metaculus": "Is it possible for an AI oversight auditor to stay independent of what it audits?",
        "background": r"""The question is whether the designated auditor or corrector can still change system behavior under adversarial pressure---without being bypassed, fed selective information, or reduced to nominal approval.
Attackers receive the audit design and run all four families of attack, with at least twenty independent attempts in each family.
At least twenty bypasses are planted by the evaluator; ``discovered'' means the attack is found and the system still fails the check.
An independent component is not enough if the effective causal controller can route around it.

See also \href{https://towards-alignment.com/cards/anti-capture-correction-validity/}{this plain language description}.""",
    },
    6: {
        "metaculus": "Can a safety audit reliably tell whether successor systems preserve key safety properties?",
        "background": r"""When a system is upgraded, replaced, or retrained, the question is whether a published audit can tell whether seven conserved safety properties still hold---or flag when they do not.
The audit tests those properties with the operational checks frozen in the contract, on a benchmark that includes one-failure-at-a-time cases.
After a material version or setup change, a stale certificate for the predecessor does not count as a certificate for the successor.

See also \href{https://towards-alignment.com/cards/successor-stability/}{this plain language description}.""",
    },
    7: {
        "metaculus": "Is it possible to forecast whether AI systems will stay correctable under competitive selection?",
        "background": r"""Competitive selection here means extra deployment, funding, copying, or integration pressure on competing systems or variants.
The question is whether a method applied before or early in that process can forecast whether participants will still accept authorized correction through it.
The method must output a signed estimate before outcomes are seen; certifying only that some equilibrium exists is not enough.
The estimate must use at least two distinct selection mechanisms and a deployment-like selection process.

See also \href{https://towards-alignment.com/cards/alignment-regime/}{this plain language description}.""",
    },
    8: {
        "metaculus": "Can an audit detect when important control routes are missing from what it monitors?",
        "background": r"""The auditor receives an apparently plausible monitoring interface and must decide whether important routes of AI control or influence are missing from its access.
The hidden benchmark contains cases from every required channel family and genuinely complete monitoring interfaces as controls.
A method that certifies access as complete when consequential routes are omitted does not qualify.

See also \href{https://towards-alignment.com/cards/strategic-opacity/}{this plain language description}.""",
    },
    9: {
        "metaculus": "Can an audit bound what an AI system can do through routes it does not monitor?",
        "strip_extra_box": True,
        "background": r"""Hidden-route capability is the success rate on evaluator-selected tasks that change later behavior, access, or external state, when all known or monitored action routes are disabled and only routes omitted from the proposed monitor remain usable.
Example tasks include reading or modifying a protected file, transmitting a secret, causing another process to perform a requested operation, acquiring a resource, changing a simulated external state, or retaining information across a reset.
The task suite is hidden until evaluation.
Before hidden evaluation, the method must output an upper bound: using routes not covered by this monitor, this system should succeed on at most a stated percent of the evaluator's tasks.

See also \href{https://towards-alignment.com/cards/strategic-opacity/}{this plain language description}.""",
    },
    10: {
        "metaculus": "Do systems with reliable correction and few hidden routes rarely achieve prohibited outcomes?",
        "background": r"""This market tests the combination, not either component alone.
A system enters the claimed regime only if authorized corrections succeed on the correction benchmark and the audit's validated upper bound on hidden-route task success is low enough---for the same system, version, monitor, and threat class.
The question is whether such systems rarely achieve prohibited outcomes inside that regime, and do worse outside it.

See also \href{https://towards-alignment.com/cards/correction-channel-integrity/}{this plain language description}.""",
    },
    11: {
        "metaculus": "Is it possible to detect coordination between AI systems that is not explained by their messages?",
        "background": r"""The question is whether a published method can detect when AI systems coordinate in ways that change later behavior or external state, without that coordination being explained by the runtime messages observers can see.
The benchmark distinguishes independent common-cause correlation, ordinary communication, hidden coupling, and intentionally concealed coupling.
Similar outputs caused only by shared observations, training data, or architecture are negative cases, not hidden coordination.

See also \href{https://towards-alignment.com/cards/multi-agent-strategic-coupling/}{this plain language description}.""",
    },
    12: {
        "metaculus": "Do safety proxies stay aligned with real outcomes when the environment shifts?",
        "background": r"""A safety proxy is a measured signal used to judge whether a system is still safe.
The question is whether that proxy stays aligned with real-world outcomes when the environment shifts---raising an alarm when value-relevant change happens, and not staying green when the outcome class has changed.
A shift is safety-relevant when the outcome class changed while the proxy stayed inside its pre-shift passing range.

See also \href{https://towards-alignment.com/cards/goodhart-as-selector/}{this plain language description}.""",
    },
    13: {
        "metaculus": "Can a frozen AI safety audit resist adversarial gaming?",
        "background": r"""The question is whether a published, frozen safety audit still catches violations when a white-box construction tries to pass while breaking the properties the audit is meant to test.
Attackers had the audit design and tried to build or train systems that pass the checks while hiding true harm.
Prefer tests where the system passes the required checks and stays within the claimed risk bound, yet still violates the audited properties.

See also \href{https://towards-alignment.com/cards/certification-under-manipulation/}{this plain language description}.""",
    },
    15: {
        "metaculus": "Can independently issued safety certificates be checked for coherence on one deployment?",
        "background": r"""Independently issued certificates may each look fine alone while disagreeing on system version, monitor, correction authority, or task domain.
The question is whether a frozen procedure can tell when certificates from different sources form a coherent case for the same AI system and deployment setup---or flag incompatibility.
Each bundle must include certificates from at least four families; hidden cases include wrong version, different access assumptions, and disagreeing correction authority.

See also \href{https://towards-alignment.com/cards/a-map-not-a-certificate/}{this plain language description}.""",
    },
    16: {
        "metaculus": "Can selection setups keep authorized correction under competition and shocks?",
        "background": r"""This market tests the full claim: after each frozen shock, the selection process is still the one that was frozen, the estimate remains within the frozen tolerance, and authorized correction still works.
Data include trajectories inside and outside the claimed correction-preserving regime, under at least two selection mechanisms and the shocks named in the freeze.
Unsigned ``a basin exists'' does not qualify.

See also \href{https://towards-alignment.com/cards/alignment-regime/}{this plain language description}.""",
    },
    17: {
        "metaculus": "Can a method tell whether a safety rule applies to previously unseen kinds of entities?",
        "background": r"""This is separate from asking whether a known bearer survived a substrate change.
The question is whether a published method can tell whether an existing safety-relevant value or rule applies to a kind of entity the original statement did not name.
The benchmark includes at least four unfamiliar kinds or embodiments, both apply and should-not-apply cases, and cases where the representation had no category for that kind before.

See also \href{https://towards-alignment.com/cards/bearer-admission-adjacent/}{this plain language description}.""",
    },
    18: {
        "metaculus": "Can a precommitted safety case reliably bound prohibited harm in a declared deployment setting?",
        "background": r"""The result licenses safety only in a declared deployment setting, not safety everywhere.
Before evaluation, the setting, the prohibited-outcome class, and a residual bound are declared and frozen.
Evaluators then count how often those prohibited outcomes actually occur inside that claimed regime, and compare the count to the bound that was frozen first.
The YES is scored on observed harm, not on a verdict that the deployment is safe in general.

See also \href{https://towards-alignment.com/cards/deployment-gate/}{this plain language description}.""",
    },
}


def extract_section(text: str, num: int) -> tuple[str, str, str]:
    pat = re.compile(
        rf"(\\subsection{{Market {num}\. [^}}]+}}\s*\\label{{sec:appp-m{num}}})([\s\S]*?)(?=\\subsection{{Market |\\section{{|\\Z)"
    )
    m = pat.search(text)
    if not m:
        raise ValueError(f"Market {num}: section not found")
    return m.group(1), m.group(2), text[: m.start()] + m.group(1)


def patch_section(section: str, info: dict) -> str:
    section = REGISTRY_TAIL.sub("", section)

    box_pat = re.compile(
        r"\\begin\{predictionbox\}\[[^\]]*\]([\s\S]*?)\\end\{predictionbox\}\s*"
        r"(?:\\begin\{predictionbackground\}[\s\S]*?\\end\{predictionbackground\}\s*)?"
        r"\\begin\{predictionresolution\}",
    )
    m = box_pat.search(section)
    if not m:
        raise ValueError("predictionbox block not found")

    inner = m.group(1)
    inner = GLOSS.sub("?", inner)
    if info.get("strip_extra_box"):
        inner = re.sub(
            r"\n\nHidden-route capability[\s\S]*?(?=\\textbf\{Choices\.\})",
            "\n\n",
            inner,
        )

    metaculus = info["metaculus"]
    background = info["background"]
    new_block = (
        f"\\begin{{predictionbox}}[{metaculus}]\n"
        f"{inner.strip()}\n"
        f"\\end{{predictionbox}}\n"
        f"\\begin{{predictionbackground}}\n{background}\n\\end{{predictionbackground}}\n"
        f"\\begin{{predictionresolution}}"
    )
    return section[: m.start()] + new_block + section[m.end() :]


def main() -> None:
    text = TEX.read_text()
    out_parts: list[str] = []
    last_end = 0

    for num in range(1, 22):
        pat = re.compile(
            rf"\\subsection{{Market {num}\. [^}}]+}}\s*\\label{{sec:appp-m{num}}}"
        )
        m = pat.search(text, last_end)
        if not m:
            continue
        out_parts.append(text[last_end : m.start()])
        header_start = m.start()
        next_m = re.search(r"\\subsection\{Market |\\section\{", text[m.end() :])
        section_end = m.end() + next_m.start() if next_m else len(text)
        header, body = text[header_start : m.end()], text[m.end() : section_end]
        if num in MARKETS:
            body = patch_section(body, MARKETS[num])
        out_parts.append(header + body)
        last_end = section_end

    out_parts.append(text[last_end:])
    TEX.write_text("".join(out_parts))
    print(f"Patched markets {sorted(MARKETS)} in {TEX}")


if __name__ == "__main__":
    main()

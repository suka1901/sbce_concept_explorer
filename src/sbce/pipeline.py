"""Set-based concept exploration.

Round 0   scout the knowledge base -> generate a set of concepts -> evaluate each with score RANGES
Round 1+  learning loop: for every surviving concept, retrieve evidence aimed at its most uncertain
          criterion and re-evaluate, then narrow the set.

Narrowing follows set-based concurrent engineering: a concept is only removed when the evidence shows it
is infeasible (a must requirement is violated, with a citation) or when it is dominated WITH CONFIDENCE
(its optimistic weighted score is below another concept's pessimistic weighted score). Uncertain concepts
stay in the set until evidence decides. Every elimination is logged with its reason and evidence.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import numpy as np

from . import prompts
from .kb import KnowledgeBase, normalize
from .llm import LLM
from .schemas import (BaselineAnswer, Concept, ConceptList, Elimination, Evaluation, MustCheck, MustReview, Queries,
                      StrictEvaluation)


# ---------------------------------------------------------------------------
# brief parsing
# ---------------------------------------------------------------------------

def must_requirements(brief: str) -> list[str]:
    """Bullet lines under a heading that contains 'must'."""
    out, active = [], False
    for line in brief.splitlines():
        if line.startswith("#"):
            active = "must" in line.lower()
        elif active and line.strip().startswith(("-", "*")):
            out.append(line.strip()[1:].strip())
    return out


# ---------------------------------------------------------------------------
# pure SBCE logic (no LLM) - unit tested directly
# ---------------------------------------------------------------------------

def weighted_range(ev: Evaluation, criteria: list[dict]) -> tuple[float, float]:
    """Weighted pessimistic and optimistic score. A criterion the LLM skipped counts as fully uncertain (1..5)."""
    by_name = {s.criterion: s for s in ev.scores}
    total = sum(c["weight"] for c in criteria)
    low = high = 0.0
    for c in criteria:
        s = by_name.get(c["name"])
        low += c["weight"] * (s.low if s else 1.0)
        high += c["weight"] * (s.high if s else 5.0)
    return low / total, high / total


def most_uncertain(ev: Evaluation, criteria: list[dict]) -> dict:
    by_name = {s.criterion: s for s in ev.scores}
    width = lambda c: c["weight"] * ((by_name[c["name"]].high - by_name[c["name"]].low) if c["name"] in by_name else 4.0)
    return max(criteria, key=width)


def narrow(alive: list[str], evals: dict[str, Evaluation], criteria: list[dict], round_no: int,
           valid_ids: set[str], margin: float = 0.0, min_keep: int = 2) -> list[Elimination]:
    """Return the eliminations for this round (never shrinks the set below `min_keep`)."""
    cands: list[tuple[int, float, Elimination]] = []
    ranges = {c: weighted_range(evals[c], criteria) for c in alive}

    for c in alive:
        for m in evals[c].must:
            cited = [e for e in m.evidence_ids if e in valid_ids]
            if m.status.lower() == "violated" and cited:
                cands.append((0, ranges[c][1], Elimination(
                    concept_id=c, round=round_no, rule="must_violation",
                    reason=f"violates '{m.requirement}': {m.reason}".strip(), evidence_ids=cited)))
                break

    flagged = {e.concept_id for _, _, e in cands}
    for c in alive:
        if c in flagged:
            continue
        lo_c, hi_c = ranges[c]
        rivals = [(ranges[o][0], o) for o in alive if o != c and o not in flagged and ranges[o][0] > hi_c + margin]
        if rivals:
            lo_o, o = max(rivals)
            cands.append((1, hi_c, Elimination(
                concept_id=c, round=round_no, rule="dominated", dominated_by=o,
                reason=f"optimistic score {hi_c:.2f} is below the pessimistic score {lo_o:.2f} of {o}")))

    cands.sort(key=lambda t: (t[0], t[1]))               # violations first, then the weakest
    budget = max(0, len(alive) - min_keep)
    return [e for _, _, e in cands[:budget]]


def rank(alive: list[str], evals: dict[str, Evaluation], criteria: list[dict]) -> list[str]:
    mid = {c: sum(weighted_range(evals[c], criteria)) / 2 for c in alive}
    return sorted(alive, key=lambda c: -mid[c])


def dedupe(concepts: list[Concept], vectors: np.ndarray, threshold: float) -> list[int]:
    """Indices to keep: drop a concept whose embedding is too close to an earlier kept one."""
    v = normalize(vectors)
    keep: list[int] = []
    for i in range(len(concepts)):
        if all(float(v[i] @ v[j]) < threshold for j in keep):
            keep.append(i)
    return keep


# ---------------------------------------------------------------------------
# LLM-driven steps
# ---------------------------------------------------------------------------

def concept_text(c: Concept) -> str:
    return f"{c.id}: {c.name} ({c.principle}). {c.description}"


def clean_ids(ids: list[str], allowed: set[str]) -> list[str]:
    """Keep only ids that were actually shown to the model; strip brackets the model may add."""
    out = []
    for i in ids:
        i = re.sub(r"^\[|\]$", "", i.strip())
        if i in allowed and i not in out:
            out.append(i)
    return out


@dataclass
class RunResult:
    method: str
    concepts: dict[str, Concept]
    rounds: list[dict[str, Evaluation]] = field(default_factory=list)   # evaluations per round
    evidence: dict[str, list[str]] = field(default_factory=dict)       # evidence shown per concept
    eliminations: list[Elimination] = field(default_factory=list)
    final: list[str] = field(default_factory=list)                     # recommended set, best first
    scout_queries: list[str] = field(default_factory=list)

    @property
    def last(self) -> dict[str, Evaluation]:
        merged: dict[str, Evaluation] = {}
        for r in self.rounds:
            merged.update(r)
        return merged


def run_sbce(brief: str, kb: KnowledgeBase, llm: LLM, criteria: list[dict], sbce: dict,
             log=print) -> RunResult:
    must = must_requirements(brief)
    valid = set(kb.by_id)

    # scouting
    queries = llm.chat_json(prompts.SYSTEM, prompts.scout(brief), Queries).queries[:6] or [brief]
    per_q = max(2, sbce["top_k_scout"] // max(len(queries), 1))
    scout_ids: list[str] = []
    for q in queries:
        for ch in kb.search(q, k=per_q, exclude=set(scout_ids)):
            scout_ids.append(ch.id)
    log(f"scouted {len(scout_ids)} chunks with {len(queries)} queries")

    # concept generation (set-based: many alternatives) + near-duplicate removal
    gen = llm.chat_json(prompts.SYSTEM, prompts.generate(brief, kb.format(scout_ids), sbce["n_concepts"]), ConceptList)
    raw = gen.concepts[: sbce["n_concepts"]]
    keep = dedupe(raw, llm.embed([f"{c.name}: {c.principle}" for c in raw]), sbce["dedupe_similarity"]) if raw else []
    concepts: dict[str, Concept] = {}
    for n, i in enumerate(keep, start=1):
        c = raw[i].model_copy(update={"id": f"C{n}"})
        c.evidence_ids = clean_ids(c.evidence_ids, set(scout_ids))
        concepts[c.id] = c
    log(f"generated {len(raw)} concepts, kept {len(concepts)} after de-duplication")
    res = RunResult("sbce", concepts, scout_queries=queries)

    strict = bool(sbce.get("require_citations", False))
    schema: type[Evaluation] = StrictEvaluation if strict else Evaluation
    separate = sbce.get("must_check", "inline") == "separate"
    k_must = sbce.get("top_k_must", 2)

    def check_musts(cid: str) -> list[MustCheck]:
        """Separate must step: evidence per requirement, then a worked comparison per requirement."""
        c = concepts[cid]
        blocks, shown = [], set()
        for req in must:
            hits = kb.search(f"{c.name} {c.principle} {req}", k=k_must)
            shown |= {h.id for h in hits}
            res.evidence[cid] += [h.id for h in hits if h.id not in res.evidence[cid]]
            blocks.append((req, kb.format([h.id for h in hits])))
        review = llm.chat_json(prompts.SYSTEM, prompts.must_check(brief, concept_text(c), blocks), MustReview)
        out = []
        for chk in review.checks:
            ids = clean_ids(chk.evidence_ids, shown)
            violated = chk.status == "violated" and chk.evidence_value.strip().lower() != "not covered"
            out.append(MustCheck(requirement=chk.requirement, status="violated" if violated else
                                 ("unclear" if chk.status == "violated" else chk.status), evidence_ids=ids,
                                 reason=f"{chk.evidence_value} vs {chk.limit}: {chk.comparison}"))
        return out

    def assess(cid: str, round_no: int, new_ids: list[str], previous: Evaluation | None) -> Evaluation:
        res.evidence.setdefault(cid, list(dict.fromkeys(concepts[cid].evidence_ids)))
        res.evidence[cid] += [i for i in new_ids if i not in res.evidence[cid]]
        shown = res.evidence[cid]
        ev = llm.chat_json(prompts.SYSTEM, prompts.evaluate(
            brief, concept_text(concepts[cid]), criteria, [] if separate else must, kb.format(shown), round_no,
            previous.model_dump_json() if previous else None, strict), schema)
        ev.concept_id = cid
        for s in ev.scores:
            s.evidence_ids = clean_ids(s.evidence_ids, set(shown))
        for m in ev.must:
            m.evidence_ids = clean_ids(m.evidence_ids, set(shown))
        if separate:
            ev.must = check_musts(cid) if previous is None or not previous.must else previous.must
        return ev

    # round 0
    alive = list(concepts)
    evals: dict[str, Evaluation] = {}
    for cid in alive:
        hits = kb.search(f"{concepts[cid].name} {concepts[cid].principle}", k=sbce["top_k_round"])
        evals[cid] = assess(cid, 0, [h.id for h in hits], None)
    res.rounds.append(dict(evals))

    for round_no in range(0, sbce["max_rounds"] + 1):
        if round_no > 0:                                     # learning loop
            for cid in alive:
                target = most_uncertain(evals[cid], criteria)
                q = f"{concepts[cid].name} {concepts[cid].principle} {target['name'].replace('_', ' ')} {target['description']}"
                hits = kb.search(q, k=sbce["top_k_round"], exclude=set(res.evidence[cid]))
                evals[cid] = assess(cid, round_no, [h.id for h in hits], evals[cid])
            res.rounds.append({c: evals[c] for c in alive})
        out = narrow(alive, evals, criteria, round_no, valid, sbce["dominance_margin"], sbce["min_keep"])
        res.eliminations += out
        gone = {e.concept_id for e in out}
        alive = [c for c in alive if c not in gone]
        log(f"round {round_no}: {len(out)} eliminated, {len(alive)} remain")
        if len(alive) <= sbce["target_set_size"]:
            break

    res.final = rank(alive, evals, criteria)[: sbce["target_set_size"]]
    return res


def run_baseline(brief: str, llm: LLM, criteria: list[dict], sbce: dict) -> RunResult:
    """Single prompt, no retrieval and no narrowing: what you get by just asking the LLM."""
    ans = llm.chat_json(prompts.SYSTEM, prompts.baseline(brief, criteria, sbce["n_concepts"], sbce["target_set_size"]),
                        BaselineAnswer)
    concepts = {}
    for n, c in enumerate(ans.concepts[: sbce["n_concepts"]], start=1):
        concepts[c.id or f"C{n}"] = c.model_copy(update={"id": c.id or f"C{n}", "evidence_ids": []})
    evals = {e.concept_id: e for e in ans.evaluations if e.concept_id in concepts}
    for e in evals.values():
        for s in e.scores:
            s.evidence_ids = []                              # nothing was shown, so no citation can be valid
    final = [c for c in ans.recommended if c in concepts][: sbce["target_set_size"]]
    if not final and evals:
        final = rank(list(evals), evals, criteria)[: sbce["target_set_size"]]
    return RunResult("baseline", concepts, rounds=[evals], final=final)

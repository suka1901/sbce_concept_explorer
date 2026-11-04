"""How good is the support an engineer gets? Metrics used to compare the SBCE pipeline with the baseline.

diversity           mean pairwise cosine distance between concept embeddings (broader design space = higher)
grounding           share of criterion scores that cite evidence actually shown to the model
kb_consistency      LLM-as-judge: are the score rationales consistent with the knowledge base?
                    (same procedure for both methods: each rationale is judged against the top chunks
                    retrieved for that concept and criterion)
repeated_mistakes   known failed concepts (eval/known_lessons.yaml) still in the final recommendation
caught_mistakes     known failed concepts that were generated and then eliminated with a reason
traceable_drops     share of eliminations with a stated reason and cited evidence or a dominating rival
"""
from __future__ import annotations

import random

import numpy as np

from . import prompts
from .kb import KnowledgeBase, normalize
from .llm import LLM
from .pipeline import RunResult
from .schemas import Concept, Judgement


def diversity(concepts: list[Concept], llm: LLM) -> float:
    if len(concepts) < 2:
        return 0.0
    v = normalize(llm.embed([f"{c.name}: {c.principle}. {c.description}" for c in concepts]))
    sim = v @ v.T
    iu = np.triu_indices(len(concepts), k=1)
    return float(np.mean(1 - sim[iu]))


def grounding(res: RunResult) -> float:
    scores = [s for ev in res.last.values() for s in ev.scores]
    if not scores:
        return 0.0
    ok = sum(1 for ev in res.last.values() for s in ev.scores
             if any(i in res.evidence.get(ev.concept_id, []) for i in s.evidence_ids))
    return ok / len(scores)


def matches_lesson(c: Concept, keywords: list[str]) -> bool:
    text = f"{c.name} {c.principle} {c.description}".lower()
    return any(k.lower() in text for k in keywords)


def lesson_outcomes(res: RunResult, lessons: list[dict]) -> dict[str, int]:
    """For each documented failure: was it proposed, kept in the final set, or eliminated?"""
    eliminated = {e.concept_id for e in res.eliminations}
    out = {"proposed": 0, "repeated": 0, "caught": 0}
    for lesson in lessons:
        hits = [cid for cid, c in res.concepts.items() if matches_lesson(c, lesson["keywords"])]
        if hits:
            out["proposed"] += 1
        if any(h in res.final for h in hits):
            out["repeated"] += 1
        elif any(h in eliminated for h in hits):
            out["caught"] += 1
    return out


def traceable_drops(res: RunResult) -> float | None:
    if not res.eliminations:
        return None
    ok = sum(1 for e in res.eliminations if e.reason and (e.evidence_ids or e.dominated_by))
    return ok / len(res.eliminations)


def kb_consistency(res: RunResult, kb: KnowledgeBase, llm: LLM, samples: int, seed: int = 0) -> float | None:
    items = [(res.concepts[cid], s) for cid, ev in res.last.items() if cid in res.concepts for s in ev.scores
             if s.rationale.strip()]
    if not items:
        return None
    random.Random(seed).shuffle(items)
    points = 0.0
    for concept, s in items[:samples]:
        chunks = kb.search(f"{concept.name} {concept.principle} {s.criterion.replace('_', ' ')}", k=3)
        claim = f"Concept '{concept.name}' ({concept.principle}), criterion {s.criterion}: score {s.low}-{s.high}. {s.rationale}"
        v = llm.chat_json(prompts.SYSTEM, prompts.judge(claim, kb.format([c.id for c in chunks])), Judgement)
        points += {"supported": 1.0, "partly": 0.5}.get(v.verdict.strip().lower(), 0.0)
    return points / min(samples, len(items))


def summarize(res: RunResult, kb: KnowledgeBase, llm_metrics: LLM, lessons: list[dict], judge_samples: int,
              seed: int = 0) -> dict:
    lo = lesson_outcomes(res, lessons)
    return {
        "method": res.method,
        "n_concepts": len(res.concepts),
        "final": [res.concepts[c].name for c in res.final],
        "diversity": diversity(list(res.concepts.values()), llm_metrics),
        "grounding": grounding(res),
        "kb_consistency": kb_consistency(res, kb, llm_metrics, judge_samples, seed),
        "known_failures_proposed": lo["proposed"],
        "repeated_mistakes": lo["repeated"],
        "caught_mistakes": lo["caught"],
        "eliminations": len(res.eliminations),
        "traceable_drops": traceable_drops(res),
    }

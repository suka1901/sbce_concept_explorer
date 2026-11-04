"""Human-readable outputs: a decision log for one run and a comparison table for the experiment."""
from __future__ import annotations

import statistics

from .kb import KnowledgeBase
from .pipeline import RunResult, weighted_range


def decision_log(res: RunResult, kb: KnowledgeBase, criteria: list[dict]) -> str:
    L = ["# Decision log", ""]
    if res.scout_queries:
        L += ["## Scouting queries", ""] + [f"- {q}" for q in res.scout_queries] + [""]
    L += ["## Concepts", ""]
    for cid, c in res.concepts.items():
        L.append(f"- **{cid} {c.name}** ({c.principle}): {c.description}")
    for r, evals in enumerate(res.rounds):
        L += ["", f"## Round {r}", "", "| Concept | Weighted score range | Must checks |", "|---|---|---|"]
        for cid, ev in evals.items():
            lo, hi = weighted_range(ev, criteria)
            musts = "; ".join(f"{m.status}" for m in ev.must) or "-"
            L.append(f"| {cid} {res.concepts[cid].name} | {lo:.2f} - {hi:.2f} | {musts} |")
        dropped = [e for e in res.eliminations if e.round == r]
        if dropped:
            L += ["", "Eliminated:"]
            for e in dropped:
                cite = ", ".join(f"`{i}`" for i in e.evidence_ids)
                L.append(f"- {e.concept_id} {res.concepts[e.concept_id].name}: {e.reason}" + (f" (evidence: {cite})" if cite else ""))
    L += ["", "## Recommended set (kept open for detailed design)", ""]
    for cid in res.final:
        ev = res.last[cid]
        L.append(f"### {cid} {res.concepts[cid].name}")
        for s in ev.scores:
            cite = ", ".join(f"`{i}`" for i in s.evidence_ids) or "no evidence cited"
            L.append(f"- {s.criterion}: {s.low:g}-{s.high:g}. {s.rationale} ({cite})")
        L.append("")
    used = sorted({i for ids in res.evidence.values() for i in ids})
    L += ["## Evidence used", ""] + [f"- `{i}`: {kb.by_id[i].title}" for i in used if i in kb.by_id]
    return "\n".join(L) + "\n"


def fmt(values: list) -> str:
    vals = [v for v in values if v is not None]
    if not vals:
        return "-"
    if all(isinstance(v, int) for v in vals):
        return f"{sum(vals)} / {len(vals)} runs"
    m = statistics.mean(vals)
    return f"{m:.2f} ± {statistics.stdev(vals):.2f}" if len(vals) > 1 else f"{m:.2f}"


ROWS = [("diversity", "Concept diversity (0-1, higher = broader)"),
        ("grounding", "Scores citing evidence"),
        ("kb_consistency", "Consistent with knowledge base (LLM judge)"),
        ("known_failures_proposed", "Known failed concepts proposed"),
        ("repeated_mistakes", "Known failed concepts in final recommendation"),
        ("caught_mistakes", "Known failed concepts eliminated with a reason"),
        ("traceable_drops", "Eliminations with reason and evidence"),
        ("llm_calls", "LLM calls per run"),
        ("seconds", "LLM time per run (s)")]


def comparison(runs: dict[str, list[dict]], model: str) -> str:
    methods = list(runs)
    L = ["# Results", "", f"Model: `{model}` via Ollama, {len(runs[methods[0]])} runs per method.", "",
         "| Metric | " + " | ".join(methods) + " |", "|---|" + "---|" * len(methods)]
    for key, label in ROWS:
        L.append(f"| {label} | " + " | ".join(fmt([r.get(key) for r in runs[m]]) for m in methods) + " |")
    L += ["", "Final recommendations per run:", ""]
    for m in methods:
        for i, r in enumerate(runs[m]):
            L.append(f"- {m} run {i + 1}: " + ", ".join(r["final"]))
    return "\n".join(L) + "\n"

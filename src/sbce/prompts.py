"""Prompt templates. Each user prompt starts with 'TASK: <name>' (used for call statistics and by the test fake)."""
from __future__ import annotations

SYSTEM = (
    "You are an engineering assistant in early product development. Be concrete and brief. "
    "When evidence is given, base every claim on it and cite chunk ids exactly as written in square brackets, "
    "e.g. steel_spring_isolators#1, in the evidence_ids fields. Never invent ids. "
    "If the evidence does not cover something, say so and widen the score range instead of guessing. "
    "Answer with JSON only."
)


def criteria_text(criteria: list[dict]) -> str:
    return "\n".join(f"- {c['name']} (weight {c['weight']}): {c['description']}" for c in criteria)


def scout(brief: str) -> str:
    return f"""TASK: scout
Design brief:
{brief}

Write 4 to 6 short search queries for an internal engineering knowledge base (concept notes, test reports,
field reports, cost data, post-mortems of stopped projects). Cover different solution principles and the
risks behind each must requirement. Return {{"queries": [...]}}."""


def generate(brief: str, evidence: str, n: int) -> str:
    return f"""TASK: generate
Design brief:
{brief}

Evidence from the knowledge base:
{evidence}

Propose {n} concepts that use clearly DIFFERENT working principles. Include concepts the evidence warns about
if they are plausible, so they can be evaluated openly. For each concept give id (C1, C2, ...), name,
principle (a few words), a two-sentence description, and evidence_ids that informed it.
Return {{"concepts": [...]}}."""


def evaluate(brief: str, concept: str, criteria: list[dict], must: list[str], evidence: str,
             round_no: int, previous: str | None) -> str:
    prev = f"\nYour previous evaluation (update it with the new evidence):\n{previous}\n" if previous else ""
    musts = "\n".join(f"- {m}" for m in must)
    return f"""TASK: evaluate
Round: {round_no}
Design brief:
{brief}

Concept:
{concept}

Evidence:
{evidence}
{prev}
Score the concept on each criterion from 1 (poor) to 5 (excellent) as a range: low = pessimistic,
high = optimistic. A wide range means uncertainty; narrow it only when evidence supports it.
Criteria:
{criteria_text(criteria)}

Then check each must requirement and give status 'met', 'violated' or 'unclear'. Use 'violated' only when the
evidence clearly shows it, and cite that evidence.
Must requirements:
{musts}

Return {{"concept_id": "...", "scores": [{{"criterion", "low", "high", "evidence_ids", "rationale"}}],
"must": [{{"requirement", "status", "evidence_ids", "reason"}}]}}."""


def baseline(brief: str, criteria: list[dict], n: int, k: int) -> str:
    return f"""TASK: baseline
Design brief:
{brief}

Propose {n} concepts (ids C1, C2, ...) with name, principle and a two-sentence description. Score each concept on
every criterion from 1 to 5 as a range (low, high) with a short rationale, then recommend the best {k}.
Criteria:
{criteria_text(criteria)}

Return {{"concepts": [...], "evaluations": [{{"concept_id", "scores": [...]}}], "recommended": ["C.."]}}."""


def judge(claim: str, evidence: str) -> str:
    return f"""TASK: judge
Claim about a design concept:
{claim}

Knowledge-base evidence:
{evidence}

Is the claim supported by the evidence? Answer 'supported', 'partly' or 'unsupported' with a one-sentence reason.
Return {{"verdict": "...", "reason": "..."}}."""

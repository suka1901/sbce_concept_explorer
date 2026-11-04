"""A deterministic stand-in for Ollama, so the whole pipeline can be tested offline.

It behaves like a reasonable model: it proposes concepts (including the two known failures), cites the
evidence ids it was shown, gives narrower score ranges in later rounds, flags must violations when a
post-mortem is in the evidence, and the baseline (no evidence) happily recommends active cancellation.
"""
from __future__ import annotations

import hashlib
import re

import numpy as np
from pydantic import BaseModel

from sbce.llm import CallStats, task_of

CONCEPTS = [
    ("Steel spring handle suspension", "coil springs with boots", 4, 4, 4, 4, 4),
    ("Silicone elastomer isolators", "cold-proof rubber mounts", 3, 5, 5, 5, 5),
    ("Active cancellation handle", "electromagnetic actuator counter-force", 5, 1, 1, 2, 1),
    ("Added ballast mass", "heavier housing", 2, 1, 4, 4, 4),
    ("Tuned mass absorber", "spring-mass tuned to drive frequency", 3, 3, 4, 4, 4),
    ("Decoupled linkage handle", "parallel linkage with damper", 5, 3, 3, 4, 3),
    ("Ergonomic grip", "handle geometry and soft grip", 1, 5, 5, 5, 5),
    ("Source balancing", "counter-rotating mass in drive", 3, 4, 4, 4, 1),
]
CRITERIA = ["vibration_reduction", "mass", "cost", "robustness", "development_effort"]


def ids_in(text: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\[([a-z_]+#\d+)\]", text)))


class FakeLLM:
    embed_model = "fake-embed"

    def __init__(self, dim: int = 256):
        self.dim = dim
        self.stats = CallStats()

    # ---- embeddings: hashed bag of words (similar words -> similar vectors)
    def embed(self, texts: list[str]) -> np.ndarray:
        out = np.zeros((len(texts), self.dim))
        for i, t in enumerate(texts):
            for w in re.findall(r"[a-z]+", t.lower()):
                out[i, int(hashlib.md5(w.encode()).hexdigest(), 16) % self.dim] += 1.0
        return out

    # ---- chat
    def chat_json(self, system: str, user: str, model: type[BaseModel]):
        task = task_of(user)
        self.stats.count(task)
        return model.model_validate(getattr(self, f"_{task}")(user))

    def _scout(self, user: str) -> dict:
        return {"queries": ["handle vibration isolation", "post-mortem stopped project", "cold weather rubber",
                            "dust sealing moving parts", "cost of vibration solutions"]}

    def _generate(self, user: str) -> dict:
        ev = ids_in(user)
        return {"concepts": [{"id": f"X{i}", "name": n, "principle": p, "description": f"{n} using {p}.",
                              "evidence_ids": ev[i % len(ev): i % len(ev) + 2] + ["made_up#9"]}
                             for i, (n, p, *_) in enumerate(CONCEPTS)]}

    def _evaluate(self, user: str) -> dict:
        name = re.search(r"Concept:\n\w+: (.+?) \(", user).group(1)          # type: ignore[union-attr]
        rnd = int(re.search(r"Round: (\d+)", user).group(1))                 # type: ignore[union-attr]
        base = next(c for c in CONCEPTS if c[0] == name)[2:]
        ev = ids_in(user.split("Evidence:")[1])
        spread = max(0.0, 1.5 - 0.5 * rnd)                                   # learning loop narrows ranges
        scores = [{"criterion": c, "low": max(1, v - spread), "high": min(5, v + spread),
                   "evidence_ids": ev[:1], "rationale": f"{name} rated on {c} from the evidence."}
                  for c, v in zip(CRITERIA, base)]
        must = []
        for pm, req in (("active_cancellation_postmortem", "dust"), ("added_mass_postmortem", "mass")):
            hit = [i for i in ev if i.startswith(pm)]
            if hit and pm.split("_")[0] in name.lower():
                must.append({"requirement": req, "status": "violated", "evidence_ids": hit[:1], "reason": "see post-mortem"})
        return {"concept_id": "ignored", "scores": scores, "must": must}

    def _baseline(self, user: str) -> dict:
        concepts = [{"id": f"C{i + 1}", "name": n, "principle": p, "description": f"{n}."} for i, (n, p, *_) in enumerate(CONCEPTS)]
        evals = [{"concept_id": f"C{i + 1}", "scores": [{"criterion": c, "low": v, "high": v, "evidence_ids": ["x#1"],
                                                         "rationale": "Generally effective."} for c, v in zip(CRITERIA, vals)]}
                 for i, (_, _, *vals) in enumerate(CONCEPTS)]
        return {"concepts": concepts, "evaluations": evals, "recommended": ["C3", "C6"]}

    def _judge(self, user: str) -> dict:
        claim, evidence = user.split("Knowledge-base evidence:")
        words = set(re.findall(r"[a-z]{5,}", claim.lower())) - {"concept", "criterion", "score", "rated", "evidence"}
        overlap = len(words & set(re.findall(r"[a-z]{5,}", evidence.lower())))
        return {"verdict": "supported" if overlap >= 3 else "partly" if overlap else "unsupported", "reason": "fake"}

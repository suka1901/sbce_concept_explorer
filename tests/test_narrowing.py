"""The set-based narrowing rule: only eliminate on evidence or confident dominance."""
from __future__ import annotations

import numpy as np

from sbce.pipeline import dedupe, most_uncertain, must_requirements, narrow, rank, weighted_range
from sbce.schemas import Concept, CriterionScore, Evaluation, MustCheck

CRIT = [{"name": "a", "weight": 0.5, "description": ""}, {"name": "b", "weight": 0.5, "description": ""}]
VALID = {"pm#0", "note#1"}


def ev(cid, a, b, must=()):
    return Evaluation(concept_id=cid, scores=[CriterionScore(criterion="a", low=a[0], high=a[1], rationale=""),
                                              CriterionScore(criterion="b", low=b[0], high=b[1], rationale="")],
                      must=list(must))


def test_weighted_range():
    assert weighted_range(ev("x", (2, 4), (4, 4)), CRIT) == (3.0, 4.0)


def test_missing_criterion_counts_as_fully_uncertain():
    e = Evaluation(scores=[CriterionScore(criterion="a", low=4, high=4, rationale="")])
    assert weighted_range(e, CRIT) == (2.5, 4.5)


def test_overlapping_ranges_keep_both_concepts():
    evals = {"C1": ev("C1", (3, 5), (3, 5)), "C2": ev("C2", (2, 4), (2, 4))}
    assert narrow(["C1", "C2"], evals, CRIT, 0, VALID, min_keep=1) == []


def test_confidently_dominated_concept_is_eliminated_with_its_rival():
    evals = {"C1": ev("C1", (4, 5), (4, 5)), "C2": ev("C2", (1, 2), (1, 2)), "C3": ev("C3", (3, 5), (3, 5))}
    out = narrow(["C1", "C2", "C3"], evals, CRIT, 1, VALID, min_keep=1)
    assert [(e.concept_id, e.rule, e.dominated_by) for e in out] == [("C2", "dominated", "C1")]


def test_must_violation_needs_cited_evidence():
    no_cite = MustCheck(requirement="mass", status="violated", evidence_ids=[], reason="guess")
    fake_cite = MustCheck(requirement="mass", status="violated", evidence_ids=["invented#3"], reason="")
    real_cite = MustCheck(requirement="mass", status="violated", evidence_ids=["pm#0"], reason="too heavy")
    base = (4, 4), (4, 4)
    evals = {"C1": ev("C1", *base, must=[no_cite]), "C2": ev("C2", *base, must=[fake_cite]),
             "C3": ev("C3", *base, must=[real_cite]), "C4": ev("C4", *base)}
    out = narrow(list(evals), evals, CRIT, 0, VALID, min_keep=1)
    assert [(e.concept_id, e.rule, e.evidence_ids) for e in out] == [("C3", "must_violation", ["pm#0"])]


def test_unclear_must_status_does_not_eliminate():
    unclear = MustCheck(requirement="dust", status="unclear", evidence_ids=["note#1"])
    evals = {"C1": ev("C1", (4, 4), (4, 4), must=[unclear]), "C2": ev("C2", (4, 4), (4, 4))}
    assert narrow(["C1", "C2"], evals, CRIT, 0, VALID, min_keep=1) == []


def test_never_narrows_below_min_keep_and_drops_violations_first():
    bad = MustCheck(requirement="x", status="violated", evidence_ids=["pm#0"])
    evals = {"C1": ev("C1", (5, 5), (5, 5)), "C2": ev("C2", (4, 5), (4, 5), must=[bad]),
             "C3": ev("C3", (1, 1), (1, 1))}
    out = narrow(list(evals), evals, CRIT, 0, VALID, min_keep=2)
    assert [e.concept_id for e in out] == ["C2"]


def test_most_uncertain_uses_weighted_width():
    crit = [{"name": "a", "weight": 0.9, "description": ""}, {"name": "b", "weight": 0.1, "description": ""}]
    assert most_uncertain(ev("x", (2, 4), (1, 5)), crit)["name"] == "a"


def test_rank_by_midpoint():
    evals = {"C1": ev("C1", (2, 4), (2, 4)), "C2": ev("C2", (3, 5), (3, 5))}
    assert rank(["C1", "C2"], evals, CRIT) == ["C2", "C1"]


def test_dedupe_drops_near_identical_concepts():
    cs = [Concept(name=n, principle="", description="") for n in "abc"]
    v = np.array([[1.0, 0.0], [0.999, 0.01], [0.0, 1.0]])
    assert dedupe(cs, v, 0.95) == [0, 2]


def test_must_requirements_are_read_from_the_brief(brief):
    must = must_requirements(brief)
    assert len(must) == 4 and any("0.6 kg" in m for m in must)

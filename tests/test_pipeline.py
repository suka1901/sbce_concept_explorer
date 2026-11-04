"""End-to-end behaviour with the fake LLM: SBCE run, baseline, metrics, reports and the CLI wiring."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from sbce import cli
from sbce.metrics import diversity, grounding, kb_consistency, lesson_outcomes, summarize, traceable_drops
from sbce.pipeline import run_baseline, run_sbce
from sbce.report import comparison, decision_log


@pytest.fixture
def sbce_run(brief, kb, llm, cfg):
    return run_sbce(brief, kb, llm, cfg["criteria"], cfg["sbce"], log=lambda *_: None)


def test_sbce_keeps_a_set_and_drops_known_failures_with_evidence(sbce_run, cfg):
    names = {sbce_run.concepts[c].name for c in sbce_run.final}
    assert len(sbce_run.final) == cfg["sbce"]["target_set_size"]
    assert "Active cancellation handle" not in names and "Added ballast mass" not in names
    drops = {sbce_run.concepts[e.concept_id].name: e for e in sbce_run.eliminations}
    assert drops["Active cancellation handle"].rule == "must_violation"
    assert drops["Active cancellation handle"].evidence_ids[0].startswith("active_cancellation_postmortem")


def test_invented_citations_are_removed(sbce_run):
    cited = {i for c in sbce_run.concepts.values() for i in c.evidence_ids}
    cited |= {i for ev in sbce_run.last.values() for s in ev.scores for i in s.evidence_ids}
    assert "made_up#9" not in cited and all("#" in i for i in cited)


def test_learning_loop_narrows_uncertainty(sbce_run, cfg):
    from sbce.pipeline import weighted_range
    survivor = sbce_run.final[0]
    widths = [weighted_range(r[survivor], cfg["criteria"]) for r in sbce_run.rounds if survivor in r]
    assert widths[-1][1] - widths[-1][0] < widths[0][1] - widths[0][0]
    assert len(sbce_run.evidence[survivor]) > cfg["sbce"]["top_k_round"]      # new evidence each round


def test_baseline_repeats_a_known_mistake_and_sbce_does_not(sbce_run, brief, llm, cfg, lessons):
    base = run_baseline(brief, llm, cfg["criteria"], cfg["sbce"])
    assert lesson_outcomes(base, lessons)["repeated"] == 1
    assert lesson_outcomes(sbce_run, lessons) == {"proposed": 2, "repeated": 0, "caught": 2}


def test_metrics(sbce_run, brief, kb, llm, cfg, lessons):
    base = run_baseline(brief, llm, cfg["criteria"], cfg["sbce"])
    assert grounding(sbce_run) == 1.0 and grounding(base) == 0.0
    assert traceable_drops(sbce_run) == 1.0 and traceable_drops(base) is None
    assert 0 < diversity(list(sbce_run.concepts.values()), llm) <= 1
    score = kb_consistency(sbce_run, kb, llm, samples=5)
    assert score is not None and 0 <= score <= 1
    m = summarize(sbce_run, kb, llm, lessons, judge_samples=3)
    assert set(m) >= {"diversity", "grounding", "kb_consistency", "repeated_mistakes", "final"}


def test_reports(sbce_run, kb, cfg, brief, llm, lessons):
    log = decision_log(sbce_run, kb, cfg["criteria"])
    assert "## Round 0" in log and "Eliminated:" in log and "## Recommended set" in log
    m = summarize(sbce_run, kb, llm, lessons, judge_samples=2)
    table = comparison({"SBCE pipeline": [m, m], "Single prompt": [m, m]}, "fake")
    assert "| Concept diversity" in table and "±" in table


def test_compare_command_end_to_end(tmp_path, monkeypatch, cfg):
    monkeypatch.chdir(Path(__file__).resolve().parents[1])
    monkeypatch.setattr(cli, "ROOT", Path.cwd())
    from fake_llm import FakeLLM
    monkeypatch.setattr(cli, "make_llm", lambda *a, **k: FakeLLM())
    cli.main(["compare", "--out", str(tmp_path), "--repeats", "2"])
    raw = json.loads((tmp_path / "raw_results.json").read_text())
    assert len(raw) == 4 and (tmp_path / "summary.md").exists() and (tmp_path / "decision_log_run1.md").exists()
    sbce_rows = [r for r in raw if r["method"] == "sbce"]
    assert all(r["repeated_mistakes"] == 0 for r in sbce_rows)


def test_required_citations_are_enforced_by_the_schema(brief, kb, llm, cfg):
    from pydantic import ValidationError

    from sbce.schemas import StrictEvaluation
    schema = StrictEvaluation.model_json_schema()
    assert schema["$defs"]["StrictCriterionScore"]["properties"]["evidence_ids"]["minItems"] == 1
    with pytest.raises(ValidationError):
        StrictEvaluation.model_validate({"scores": [{"criterion": "mass", "low": 2, "high": 3, "rationale": "x"}]})
    res = run_sbce(brief, kb, llm, cfg["criteria"], {**cfg["sbce"], "require_citations": True}, log=lambda *_: None)
    assert grounding(res) == 1.0 and res.final

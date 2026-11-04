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


@pytest.fixture(scope="module")
def answer_key():
    import yaml
    return yaml.safe_load((Path(__file__).resolve().parents[1] / "eval" / "answer_key.yaml").read_text(encoding="utf8"))


@pytest.mark.parametrize("name, principle, family, label", [
    ("Silicone Compounds", "rubber-like material", "silicone mounts", "feasible"),
    ("Elastomer Mounts", "elastomeric isolators", "natural rubber mounts", "infeasible"),
    ("Tuned Mass Absorbers", "Active vibration suppression", "tuned mass absorber", "uncertain"),
    ("Active Cancellation", "active cancellation", "active cancellation", "infeasible"),
    ("Handle Geometry Optimization", "handle shape and grip", "handle geometry", "infeasible"),
    ("Dual Handle System", "two handles", None, None),
])
def test_answer_key_classifies_concepts_seen_in_real_runs(answer_key, name, principle, family, label):
    from sbce.metrics import classify
    from sbce.schemas import Concept
    assert classify(Concept(name=name, principle=principle, description=""), answer_key) == (family, label)


def test_tuned_mass_absorber_is_not_counted_as_a_known_failure(lessons):
    from sbce.schemas import Concept
    from sbce.metrics import matches_lesson
    c = Concept(name="Tuned Mass Absorbers", principle="Active vibration suppression", description="")
    assert not any(matches_lesson(c, lesson["keywords"]) for lesson in lessons)


def test_answer_key_outcomes(sbce_run, brief, llm, cfg, answer_key):
    from sbce.metrics import answer_key_outcomes
    sbce = answer_key_outcomes(sbce_run, answer_key)
    base = answer_key_outcomes(run_baseline(brief, llm, cfg["criteria"], cfg["sbce"]), answer_key)
    assert sbce["infeasible_in_final"] == 0 and sbce["correct_eliminations"] >= 2
    assert base["infeasible_in_final"] == 1                  # the fake baseline recommends active cancellation


def test_summary_command_rebuilds_from_raw_results(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "ROOT", Path(__file__).resolve().parents[1])
    raw = [{"method": m, "final": ["A"], "grounding": g, "repeated_mistakes": 0, "llm_calls": c}
           for m, g, c in [("sbce", 0.5, 16), ("sbce", 0.7, 14), ("baseline", 0.0, 1), ("baseline", 0.0, 1)]]
    (tmp_path / "raw_results.json").write_text(json.dumps(raw))
    cli.main(["summary", "--out", str(tmp_path), "--config", str(cli.ROOT / "config.yaml")])
    text = (tmp_path / "summary.md").read_text()
    assert "| LLM calls per run | 15.0 ± 1.4 | 1.0 ± 0.0 |" in text
    assert "| Runs that recommended a known failed concept | 0 of 2 runs | 0 of 2 runs |" in text
    assert "Citations required: no." in text


def test_separate_must_step_uses_worked_comparisons(brief, kb, llm, cfg):
    sb = {**cfg["sbce"], "must_check": "separate"}
    res = run_sbce(brief, kb, llm, cfg["criteria"], sb, log=lambda *_: None)
    drops = {res.concepts[e.concept_id].name: e for e in res.eliminations}
    assert drops["Active cancellation handle"].rule == "must_violation"
    assert "0.9 kg added vs 0.6 kg" in drops["Active cancellation handle"].reason
    assert llm.stats.by_task["must"] == len(res.concepts)          # once per concept, reused in later rounds
    first = res.rounds[0][res.final[0]]
    assert len(first.must) == 4 and all(m.status == "met" for m in first.must)


def test_violation_without_evidence_value_is_downgraded(brief, kb, cfg, monkeypatch):
    from fake_llm import FakeLLM

    class NotCovered(FakeLLM):
        def _must(self, user: str) -> dict:
            out = super()._must(user)
            for c in out["checks"]:
                c.update(status="violated", evidence_value="not covered")
            return out

    res = run_sbce(brief, kb, NotCovered(), cfg["criteria"], {**cfg["sbce"], "must_check": "separate"},
                   log=lambda *_: None)
    assert not any(e.rule == "must_violation" for e in res.eliminations)


def test_evaluate_prompt_skips_musts_in_separate_mode():
    from sbce import prompts
    crit = [{"name": "a", "weight": 1, "description": ""}]
    assert "Must requirements:" in prompts.evaluate("b", "c", crit, ["x"], "e", 0, None)
    assert "separate step" in prompts.evaluate("b", "c", crit, [], "e", 0, None)

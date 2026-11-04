"""Command line.

    sbce run       one SBCE run, writes results/decision_log.md
    sbce compare   SBCE vs single-prompt baseline, several runs each, writes results/summary.md
    sbce check     checks that Ollama is running and the models are pulled
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import requests
import yaml

from .kb import KnowledgeBase, load_chunks
from .llm import Ollama
from .metrics import summarize
from .pipeline import run_baseline, run_sbce
from .report import comparison, decision_log

PROJECT = Path(__file__).resolve().parents[2]
# Run from the project folder, or from anywhere else: then the project's own config and data are used.
ROOT = Path.cwd() if (Path.cwd() / "config.yaml").exists() else PROJECT


def load_config(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf8"))


def make_llm(cfg: dict, seed: int | None = None, temperature: float | None = None) -> Ollama:
    c = cfg["llm"]
    return Ollama(c["host"], c["model"], c["embed_model"],
                  c["temperature"] if temperature is None else temperature, c.get("timeout_s", 600), seed=seed,
                  num_ctx=c.get("num_ctx", 8192), progress=c.get("progress", True))


def cmd_check(cfg: dict) -> None:
    host = cfg["llm"]["host"]
    try:
        tags = requests.get(f"{host}/api/tags", timeout=5).json()
    except requests.RequestException as e:
        raise SystemExit(f"Ollama is not reachable at {host}: {e}\nStart it with: ollama serve")
    have = {m["name"].split(":")[0] for m in tags.get("models", [])} | {m["name"] for m in tags.get("models", [])}
    for m in (cfg["llm"]["model"], cfg["llm"]["embed_model"]):
        ok = m in have or m.split(":")[0] in have
        print(f"{'ok     ' if ok else 'MISSING'} {m}" + ("" if ok else f"   -> ollama pull {m}"))


def cmd_run(cfg: dict, out: Path) -> None:
    llm = make_llm(cfg)
    kb = KnowledgeBase(load_chunks(ROOT / cfg["knowledge_dir"]), llm, cache_dir=out / "cache")
    brief = (ROOT / cfg["brief"]).read_text(encoding="utf8")
    res = run_sbce(brief, kb, llm, cfg["criteria"], cfg["sbce"])
    out.mkdir(parents=True, exist_ok=True)
    (out / "decision_log.md").write_text(decision_log(res, kb, cfg["criteria"]), encoding="utf8")
    print(f"\nRecommended set: {[res.concepts[c].name for c in res.final]}")
    print(f"LLM calls: {llm.stats.calls} ({llm.stats.by_task}), {llm.stats.seconds:.0f} s")
    print(f"Decision log: {out / 'decision_log.md'}")


def cmd_compare(cfg: dict, out: Path, repeats: int | None) -> None:
    repeats = repeats or cfg["experiment"]["repeats"]
    lessons = yaml.safe_load((ROOT / "eval" / "known_lessons.yaml").read_text(encoding="utf8"))
    brief = (ROOT / cfg["brief"]).read_text(encoding="utf8")
    judge = make_llm(cfg, seed=0, temperature=0.0)               # one fixed, deterministic judge
    kb = KnowledgeBase(load_chunks(ROOT / cfg["knowledge_dir"]), judge, cache_dir=out / "cache")
    runs: dict[str, list[dict]] = {"sbce": [], "baseline": []}
    raw = []
    out.mkdir(parents=True, exist_ok=True)
    for r in range(repeats):
        for method in ("baseline", "sbce"):
            llm = make_llm(cfg, seed=r)          # the knowledge base keeps the judge's embedder (same model)
            t0 = time.perf_counter()
            res = (run_sbce(brief, kb, llm, cfg["criteria"], cfg["sbce"], log=lambda *_: None) if method == "sbce"
                   else run_baseline(brief, llm, cfg["criteria"], cfg["sbce"]))
            seconds = round(time.perf_counter() - t0, 1)            # the method only, without judging
            m = summarize(res, kb, judge, lessons, cfg["experiment"]["judge_samples"], seed=r)
            m.update(llm_calls=llm.stats.calls, retries=llm.stats.retries, output_tokens=llm.stats.output_tokens,
                     seconds=seconds)
            runs[method].append(m)
            raw.append({"run": r, **m})
            if method == "sbce":
                (out / f"decision_log_run{r + 1}.md").write_text(decision_log(res, kb, cfg["criteria"]), encoding="utf8")
            print(f"run {r + 1}/{repeats} {method:8s}: final={m['final']} grounding={m['grounding']:.2f} "
                  f"repeated_mistakes={m['repeated_mistakes']} time={seconds:.0f}s calls={llm.stats.calls} "
                  f"retries={llm.stats.retries}")
    (out / "raw_results.json").write_text(json.dumps(raw, indent=1), encoding="utf8")
    summary = comparison({"SBCE pipeline": runs["sbce"], "Single prompt": runs["baseline"]}, cfg["llm"]["model"])
    (out / "summary.md").write_text(summary, encoding="utf8")
    print("\n" + summary)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="sbce", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["run", "compare", "check"])
    ap.add_argument("--config", type=Path, default=ROOT / "config.yaml")
    ap.add_argument("--out", type=Path, default=ROOT / "results")
    ap.add_argument("--repeats", type=int, help="override experiment.repeats")
    args = ap.parse_args(argv)
    cfg = load_config(args.config)
    if args.command == "check":
        cmd_check(cfg)
    elif args.command == "run":
        cmd_run(cfg, args.out)
    else:
        cmd_compare(cfg, args.out, args.repeats)


if __name__ == "__main__":
    main()

# SBCE Concept Explorer

![tests](https://github.com/suka1901/sbce_concept_explorer/actions/workflows/tests.yml/badge.svg)

Can a local LLM help an engineering team in **early product development** without making it repeat old
mistakes? This demonstrator combines retrieval from an engineering knowledge base with
**set-based concurrent engineering (SBCE)**: it keeps several concepts open, scores them with uncertainty ranges
and citations, and narrows the set only when evidence decides. It is compared with simply asking the LLM once.

Everything runs locally with [Ollama](https://ollama.com); no data leaves the computer.

## How it works

```
design brief ─▶ scout ─▶ generate a SET of concepts ─▶ evaluate (score ranges + citations + must checks)
                 │                                          │
           hybrid RAG over                                  ▼
           knowledge base  ◀── learning loop: targeted ── narrow the set ──▶ recommended set + decision log
           (BM25 + embeddings,   retrieval for each        (only on evidence:
            rank fusion)         concept's most            must violation with citation,
                                 uncertain criterion        or confident dominance)
```

1. **Scout**: the LLM writes search queries; hybrid retrieval (BM25 keywords + embeddings, merged with
   reciprocal rank fusion) collects evidence from the knowledge base.
2. **Generate**: several concepts with clearly different working principles; near-duplicates are removed by
   embedding similarity.
3. **Evaluate**: each concept gets a pessimistic and optimistic score per criterion, with cited chunk ids.
   Citations to chunks the model was not shown are removed.
4. **Must check**: every must requirement is checked against evidence retrieved for that concept *and that
   requirement*, as a worked comparison (value from the evidence, limit, comparison, verdict), so a wrong
   comparison is visible in the decision log. A violation needs a value from the evidence; missing evidence
   only gives "unclear".
5. **Narrow (SBCE)**: a concept is eliminated only if it violates a must requirement *and cites evidence for it*,
   or if its optimistic weighted score is below another concept's pessimistic score. Otherwise it stays.
6. **Learning loop**: for each surviving concept, new evidence aimed at its most uncertain criterion is retrieved
   and the concept is re-evaluated. Repeats until the target set size or the round limit.
7. **Output**: the recommended set and a decision log showing every score, elimination and the evidence behind it.

## The demo case

A generic design brief (`data/brief.md`): lower hand-arm vibration on a hand-held powered tool from 7.5 to
below 4.0 m/s², with limits on added mass, temperature range, dust and rain, and cost.

The knowledge base (`data/knowledge/`) is **written for the demo** and imitates what an engineering team keeps:
concept notes, test notes, a cold-weather field report, cost data, and **post-mortems of two stopped projects**
(active vibration cancellation and added ballast mass). Numbers are illustrative. Add your own Markdown files;
every `##` section becomes a retrievable chunk.

## Research questions

The demonstrator is improved step by step. Each question below is answered by a run that anyone can repeat
(see [Versions](#versions)), and the answers are updated as new results come in.

| # | Question | How it is measured | Status |
|---|---|---|---|
| Q1 | Does grounding concept evaluation in the team's knowledge base make it more traceable and more correct than a single prompt? | scores citing evidence; consistency with the knowledge base (LLM judge) | v1: yes, 0.55 vs 0.00 cited, 0.68 vs 0.52 consistent |
| Q2 | Does set-based narrowing stop the tool from repeating documented failures? | known failed concepts proposed / eliminated with a reason / recommended | v1: active cancellation eliminated with a cited post-mortem every time it was proposed; neither method recommended a known failure |
| Q3 | Is the final set feasible, and are the eliminations correct? | answer key: infeasible concepts in final set, correct and false eliminations | v1: **no better than the baseline** (1.0 infeasible concept per final set for both); 2 feasible concepts wrongly eliminated |
| Q4 | Does requiring a citation for every score raise grounding without making the scores less correct? | v2 vs v1: grounding and consistency | open |
| Q5 | Does a separate must-check step with worked comparisons remove false eliminations and infeasible survivors? | v3 vs v1: answer-key metrics | open |
| Q6 | Does a bigger local model fix the must-check errors, or does the method matter more than model size? | v3 with `qwen2.5:7b` vs `qwen2.5:14b`, and v1 with 14B if needed | open |
| Q7 | What does the structure cost? | LLM calls, retries, generated tokens and time per run | v1: about 16 calls per SBCE run vs 1; the single long baseline answer is slower per call and needs retries (re-measured from v3 on) |

## Optimisation log

| Date | Step | Observation that led to it | Change |
|---|---|---|---|
| 2026-11-04 | v0 | First run on a laptop CPU timed out while generating concepts | Streamed replies, explicit 8k context, `qwen2.5:3b` for CPU; experiments moved to a Colab T4 GPU with `qwen2.5:7b` |
| 2026-11-04 | v1 | First results (3 runs): grounding varied from 0.33 to 0.71 between runs | Kept as the reference version |
| 2026-11-04 | metrics fix | The known-failure check matched the bare word "active" ("tuned mass absorbers, active vibration suppression"); counts were summed instead of averaged; run time included judging | Phrase matching on name and principle only, per-run means, timing of the method alone, retries and tokens logged |
| 2026-11-04 | answer key | Decision logs showed infeasible concepts (natural rubber at -15 degC, handle geometry with 5-10 % reduction) in final sets, which no metric caught | `eval/answer_key.yaml` with feasible / infeasible / uncertain concept types and four new metrics |
| 2026-11-04 | v2 | Citations were optional and the model often left them out | `require_citations: true` enforces at least one citation per score in the output schema |
| 2026-11-04 | v3 | The model compared numbers wrongly ("0.25 kg is above the 0.6 kg limit") and never looked up evidence for some requirements | Separate must-check step: evidence per requirement and a worked comparison (value, limit, comparison, verdict); no violation without a value from the evidence |
| next | 14B | Q6 | Rerun v3 with `qwen2.5:14b` on the same Colab GPU |

## Versions

The method was improved in steps, and each step is a setting in `config.yaml`, so every version can be rerun:

| Version | `require_citations` | `must_check` | What changed |
|---|---|---|---|
| v1 | false | inline | first version: musts checked inside the evaluation |
| v2 | true | inline | every score must cite at least one chunk |
| v3 | true | separate | must requirements checked in their own step with worked comparisons |

v1 results showed why v3 was needed: the model compared numbers wrongly ("0.25 kg is above the 0.6 kg limit")
and never looked up the evidence behind some requirements, so concepts that fail in the cold stayed in the set.

## Evaluation

`sbce compare` runs both methods several times and reports:

| Metric | Meaning |
|---|---|
| Concept diversity | mean pairwise cosine distance of concept embeddings |
| Scores citing evidence | share of criterion scores that cite evidence the model was actually shown |
| Consistent with knowledge base | LLM-as-judge (temperature 0): is each score rationale supported by the knowledge base? Same procedure for both methods |
| Known failed concepts in final recommendation | does the method recommend a concept the post-mortems document as failed? (`eval/known_lessons.yaml`) |
| Known failed concepts eliminated with a reason | knowledge reuse: proposed, then dropped with evidence |
| Eliminations with reason and evidence | traceability of the narrowing |
| Feasible / infeasible concepts in final set | checked against `eval/answer_key.yaml`, a hand-written judgement of which concept types can meet the must requirements according to the knowledge base |
| Correct / false eliminations | infeasible concepts dropped / feasible concepts wrongly dropped (same answer key) |
| LLM calls and time | cost of the extra structure |

## Results

### v1 (`qwen2.5:7b`, Colab T4, 3 runs per method) - preliminary

Measured before the metric fixes; the answer-key rows were scored by hand from the decision logs.

| Metric | SBCE pipeline | Single prompt |
|---|---|---|
| Concept diversity | 0.29 ± 0.04 | 0.25 ± 0.02 |
| Scores citing evidence | 0.55 ± 0.20 | 0.00 |
| Consistent with knowledge base (LLM judge) | 0.68 ± 0.08 | 0.52 ± 0.03 |
| Runs that recommended a known failed concept | 0 of 3 | 0 of 3 |
| Infeasible concepts in final set (answer key, mean) | 1.0 | 1.0 |
| False eliminations (feasible dropped, total) | 2 | - |
| LLM calls per run | 16 | 1 |

### v3 and model size

_Pending: `sbce compare --out results_v3`, then the same with `qwen2.5:14b`._

## Run it

```bash
# 1. Ollama (https://ollama.com/download), then the models
ollama pull qwen2.5:7b          # on a laptop without GPU, qwen2.5:3b is faster (set it in config.yaml)
ollama pull nomic-embed-text

# 2. This project
python -m venv .venv
.venv\Scripts\activate           # Windows   (Linux/macOS: source .venv/bin/activate)
pip install -e .

sbce check                       # Ollama running, models present?
sbce run                         # one run -> results/decision_log.md
sbce compare --repeats 3         # both methods, 3 runs each -> results/summary.md
sbce summary --out results       # rebuild summary.md from results/raw_results.json
```

Settings (model, criteria and weights, number of concepts, rounds, set size) are in `config.yaml`.

## Tests

```bash
pip install -r requirements-dev.txt
pytest          # 45 tests, offline: a deterministic fake LLM replaces Ollama
pyright         # type check
```

The tests cover the retrieval (BM25, rank fusion, chunking), the SBCE narrowing rule (no elimination without
evidence or confident dominance, never below the minimum set size), removal of invented citations, required
citations, the separate must step, the learning loop narrowing uncertainty, the answer key and other metrics,
the reports, the Ollama client (streamed schema output, retries) and the full `compare` command. GitHub Actions runs them on every push.

## Limitations

- The knowledge base is small and written for the demo; real pre-development data is larger, messier and partly
  confidential, which is one reason this runs locally.
- Scores come from an LLM reading the evidence, not from engineering analysis or tests. The tool supports the
  team's discussion; it does not replace it.
- The LLM judge is itself an LLM. It is run deterministically and the same way for both methods, but it should be
  checked against engineers' judgement before conclusions are drawn.
- A 7B local model sometimes needs a retry to produce valid JSON; the client retries with the validation error.

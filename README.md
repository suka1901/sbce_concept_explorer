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
3. **Evaluate**: each concept gets a pessimistic and optimistic score per criterion, with cited chunk ids, and
   a check of every must requirement. Citations to chunks the model was not shown are removed.
4. **Narrow (SBCE)**: a concept is eliminated only if it violates a must requirement *and cites evidence for it*,
   or if its optimistic weighted score is below another concept's pessimistic score. Otherwise it stays.
5. **Learning loop**: for each surviving concept, new evidence aimed at its most uncertain criterion is retrieved
   and the concept is re-evaluated. Repeats until the target set size or the round limit.
6. **Output**: the recommended set and a decision log showing every score, elimination and the evidence behind it.

## The demo case

A generic design brief (`data/brief.md`): lower hand-arm vibration on a hand-held powered tool from 7.5 to
below 4.0 m/s², with limits on added mass, temperature range, dust and rain, and cost.

The knowledge base (`data/knowledge/`) is **written for the demo** and imitates what an engineering team keeps:
concept notes, test notes, a cold-weather field report, cost data, and **post-mortems of two stopped projects**
(active vibration cancellation and added ballast mass). Numbers are illustrative. Add your own Markdown files;
every `##` section becomes a retrievable chunk.

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
| LLM calls and time | cost of the extra structure |

## Results

<!-- Run `sbce compare` and paste results/summary.md here. -->
_Not run yet._

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
```

Settings (model, criteria and weights, number of concepts, rounds, set size) are in `config.yaml`.

## Tests

```bash
pip install -r requirements-dev.txt
pytest          # 32 tests, offline: a deterministic fake LLM replaces Ollama
pyright         # type check
```

The tests cover the retrieval (BM25, rank fusion, chunking), the SBCE narrowing rule (no elimination without
evidence or confident dominance, never below the minimum set size), removal of invented citations, the learning
loop narrowing uncertainty, the metrics, the reports, the Ollama client (schema output, retries) and the full
`compare` command. GitHub Actions runs them on every push.

## Limitations

- The knowledge base is small and written for the demo; real pre-development data is larger, messier and partly
  confidential, which is one reason this runs locally.
- Scores come from an LLM reading the evidence, not from engineering analysis or tests. The tool supports the
  team's discussion; it does not replace it.
- The LLM judge is itself an LLM. It is run deterministically and the same way for both methods, but it should be
  checked against engineers' judgement before conclusions are drawn.
- A 7B local model sometimes needs a retry to produce valid JSON; the client retries with the validation error.

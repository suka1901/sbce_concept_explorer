# Results

Model: `qwen2.5:7b` via Ollama, 3 runs per method.

| Metric | SBCE pipeline | Single prompt |
|---|---|---|
| Concept diversity (0-1, higher = broader) | 0.28 ± 0.01 | 0.24 ± 0.02 |
| Scores citing evidence | 1.00 ± 0.00 | 0.00 ± 0.00 |
| Consistent with knowledge base (LLM judge) | 0.68 ± 0.03 | 0.53 ± 0.03 |
| Known failed concepts proposed | 2 / 3 runs | 3 / 3 runs |
| Known failed concepts in final recommendation | 0 / 3 runs | 1 / 3 runs |
| Known failed concepts eliminated with a reason | 2 / 3 runs | 0 / 3 runs |
| Eliminations with reason and evidence | 1.00 ± 0.00 | - |
| LLM calls per run | 53 / 3 runs | 3 / 3 runs |
| Retries after invalid JSON per run | 0 / 3 runs | 0 / 3 runs |
| Generated tokens per run | 34953 / 3 runs | 5140 / 3 runs |
| Time per run, without judging (s) | 389.63 ± 67.44 | 55.10 ± 5.80 |

Final recommendations per run:

- SBCE pipeline run 1: C1 - Steel Spring Isolators, C6 - Passive Vibration Absorber
- SBCE pipeline run 2: C5, C1
- SBCE pipeline run 3: C1 - Handle Geometry Optimization, C2 - Elastomer Mounts
- Single prompt run 1: C1: Hand-Held Vibration Dampening System, C3: Dual Handle Vibration Cancelling System
- Single prompt run 2: C1: Mass Damper, C4: Handle Design Optimization
- Single prompt run 3: C2: Vibration Dampening Material, C6: Handle Design Optimization

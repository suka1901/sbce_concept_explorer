# Results

Model: `qwen2.5:7b` via Ollama, 3 runs per method.

| Metric | SBCE pipeline | Single prompt |
|---|---|---|
| Concept diversity (0-1, higher = broader) | 0.29 ± 0.02 | 0.24 ± 0.02 |
| Scores citing evidence | 0.80 ± 0.11 | 0.00 ± 0.00 |
| Consistent with knowledge base (LLM judge) | 0.63 ± 0.06 | 0.53 ± 0.03 |
| Known failed concepts proposed | 3 / 3 runs | 3 / 3 runs |
| Known failed concepts in final recommendation | 0 / 3 runs | 1 / 3 runs |
| Known failed concepts eliminated with a reason | 3 / 3 runs | 0 / 3 runs |
| Eliminations with reason and evidence | 1.00 ± 0.00 | - |
| LLM calls per run | 52 / 3 runs | 3 / 3 runs |
| Retries after invalid JSON per run | 0 / 3 runs | 0 / 3 runs |
| Generated tokens per run | 32805 / 3 runs | 5140 / 3 runs |
| Time per run, without judging (s) | 369.67 ± 44.67 | 55.77 ± 6.31 |

Final recommendations per run:

- SBCE pipeline run 1: C2 - Elastomer Isolators, C5 - Handle Geometry and Grip
- SBCE pipeline run 2: C4, C5
- SBCE pipeline run 3: C2 - Elastomer Mounts, C1 - Handle Geometry Optimization
- Single prompt run 1: C1: Hand-Held Vibration Dampening System, C3: Dual Handle Vibration Cancelling System
- Single prompt run 2: C1: Mass Damper, C4: Handle Design Optimization
- Single prompt run 3: C2: Vibration Dampening Material, C6: Handle Design Optimization

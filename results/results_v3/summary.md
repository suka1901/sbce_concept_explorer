# Results

Citations required: yes.

Model: `qwen2.5:7b` via Ollama, 3 runs per method.

| Metric | SBCE pipeline | Single prompt |
|---|---|---|
| Concept diversity (0-1, higher = broader) | 0.29 ± 0.04 | 0.25 ± 0.02 |
| Scores citing evidence | 0.99 ± 0.02 | 0.00 ± 0.00 |
| Consistent with knowledge base (LLM judge) | 0.68 ± 0.03 | 0.52 ± 0.03 |
| Runs that proposed a known failed concept | 2 of 3 runs | 1 of 3 runs |
| Runs that recommended a known failed concept | 0 of 3 runs | 0 of 3 runs |
| Runs that eliminated a known failed concept with a reason | 2 of 3 runs | 0 of 3 runs |
| Feasible concepts in final set (answer key) | 1.0 ± 1.0 | 0.0 ± 0.0 |
| Infeasible concepts in final set (answer key) | 0.0 ± 0.0 | 1.3 ± 0.6 |
| Unclassified concepts in final set | 0.0 ± 0.0 | 0.3 ± 0.6 |
| Correct eliminations (infeasible dropped) | 2.0 ± 1.0 | 0.0 ± 0.0 |
| False eliminations (feasible dropped) | 0.7 ± 1.2 | 0.0 ± 0.0 |
| Eliminations with reason and evidence | 1.00 ± 0.00 | - |
| LLM calls per run | 19.3 ± 4.6 | 1.0 ± 0.0 |
| Retries after invalid JSON per run | 0.0 ± 0.0 | 0.0 ± 0.0 |
| Generated tokens per run | 8546.3 ± 2233.6 | 1657.0 ± 119.5 |
| Time per run, without judging (s) | 293.13 ± 79.14 | 55.53 ± 6.66 |

Final recommendations per run:

- SBCE pipeline run 1: C5 - Parallel Linkage with Sealed Bushings, C2 - Silicone Compounds
- SBCE pipeline run 2: C1: Source Balancing, C5: Tuned Mass Absorbers
- SBCE pipeline run 3: C3 - Tuned Mass Absorber, C4 - Parallel Linkage with Sealed Bushings
- Single prompt run 1: C1: Hand-Held Vibration Dampening System, C2: Dual Handle System
- Single prompt run 2: C1: Mass Damper, C4: Handle Design Optimization
- Single prompt run 3: C2: Vibration Dampening Material, C6: Handle Design Optimization

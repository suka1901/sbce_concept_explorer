# Results

Model: `qwen2.5:7b` via Ollama, 3 runs per method.

| Metric | SBCE pipeline | Single prompt |
|---|---|---|
| Concept diversity (0-1, higher = broader) | 0.29 ± 0.04 | 0.25 ± 0.02 |
| Scores citing evidence | 0.55 ± 0.20 | 0.00 ± 0.00 |
| Consistent with knowledge base (LLM judge) | 0.68 ± 0.08 | 0.52 ± 0.03 |
| Known failed concepts proposed | 3 / 3 runs | 3 / 3 runs |
| Known failed concepts in final recommendation | 0 / 3 runs | 0 / 3 runs |
| Known failed concepts eliminated with a reason | 3 / 3 runs | 0 / 3 runs |
| Eliminations with reason and evidence | 1.00 ± 0.00 | - |
| LLM calls per run | 48 / 3 runs | 3 / 3 runs |
| LLM time per run (s) | 376.67 ± 44.70 | 112.17 ± 57.32 |

Final recommendations per run:

- SBCE pipeline run 1: C2 - Silicone Compounds, C5 - Parallel Linkage with Sealed Bushings
- SBCE pipeline run 2: C2: Natural Rubber Mounts, C3: Silicone Compounds
- SBCE pipeline run 3: C2 - Elastomer Mounts, C1 - Handle Geometry Optimization
- Single prompt run 1: C1: Hand-Held Vibration Dampening System, C2: Dual Handle System
- Single prompt run 2: C1: Mass Damper, C4: Handle Design Optimization
- Single prompt run 3: C2: Vibration Dampening Material, C6: Handle Design Optimization

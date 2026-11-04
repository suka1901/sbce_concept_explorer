# Decision log

## Scouting queries

- steel_spring_isolators#1
- vibration_absorbing_materials#2
- handle_design_for_vibration_reduction#3
- durability_tests_for_hand_tools#4
- cost_reduction_strategies_for_hand_tools#5

## Concepts

- **C1 C1 - Steel Spring Isolators** (Spring suspension): Steel spring handles with guide pins reduce vibration. Bench tests showed 40 to 60 percent lower handle vibration.
- **C2 C2 - Silicone Compounds** (Rubber-like material): Use of a silicone-based compound for vibration isolation, providing better low-temperature performance and cost increase of 3 to 5 percent.
- **C3 C3 - Tuned Mass Absorber** (Absorber): A tuned mass absorber reduces vibration at a specific frequency, though its effectiveness varies with operating conditions. Costs about 5 percent more.
- **C4 C4 - Source Balancing** (Drive train modification): Adjusting the drive train to reduce vibration at the source. High development effort and cost, but cost increases once in production are low.
- **C5 C5 - Parallel Linkage with Sealed Bushings** (Linkage system): Use of a parallel linkage with sealed bushings for vibration isolation. This concept is costlier, about 12 percent increase, but provides effective isolation.
- **C6 C6 - Active Cancellation** (Active cancellation): Implement active vibration cancellation, though this is expensive (35 percent cost increase) and requires solving power and sealing issues first.

## Round 0

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Steel Spring Isolators | 3.55 - 4.55 | unclear; met; unclear; unclear |
| C2 C2 - Silicone Compounds | 3.30 - 4.30 | met; met; met; met |
| C3 C3 - Tuned Mass Absorber | 2.75 - 3.75 | met; met; unclear; unclear |
| C4 C4 - Source Balancing | 2.80 - 3.80 | unclear; violated; unclear; unclear |
| C5 C5 - Parallel Linkage with Sealed Bushings | 3.75 - 4.55 | met; met; unclear; met |
| C6 C6 - Active Cancellation | 2.10 - 3.10 | met; violated; unclear; violated |

Eliminated:
- C6 C6 - Active Cancellation: violates 'Added mass at most 0.6 kg compared with today's tool.': Added 0.9 kg. vs 0.6 kg: 0.9 kg added is above the 0.6 kg limit. (evidence: `active_cancellation_postmortem#1`, `active_cancellation_postmortem#2`)
- C4 C4 - Source Balancing: violates 'Added mass at most 0.6 kg compared with today's tool.': 0.6 kg exceeded vs 0.6 kg: The added ballast mass concept was dropped due to operator complaints and exceeding the mass target by a wide margin. (evidence: `added_mass_postmortem#1`, `source_balancing#1`)

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Steel Spring Isolators | 2.85 - 3.85 | unclear; met; unclear; unclear |
| C2 C2 - Silicone Compounds | 3.30 - 4.22 | met; met; met; met |
| C3 C3 - Tuned Mass Absorber | 2.75 - 3.75 | met; met; unclear; unclear |
| C5 C5 - Parallel Linkage with Sealed Bushings | 3.75 - 4.32 | met; met; unclear; met |

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Steel Spring Isolators | 3.15 - 4.15 | unclear; met; unclear; unclear |
| C2 C2 - Silicone Compounds | 3.53 - 4.28 | met; met; met; met |
| C3 C3 - Tuned Mass Absorber | 3.05 - 4.05 | met; met; unclear; unclear |
| C5 C5 - Parallel Linkage with Sealed Bushings | 3.75 - 4.42 | met; met; unclear; met |

## Recommended set (kept open for detailed design)

### C5 C5 - Parallel Linkage with Sealed Bushings
- vibration_reduction: 4-5. Prototype tests showed 60 to 75% lower vibration, and the design is expected to reduce it to 4.0 m/s² or below, which is the target. Test-to-test spread is about plus or minus 0.5 m/s². (`decoupled_handle_linkage#1`, `decoupled_handle_linkage#0`, `test_method_notes#0`)
- mass: 4-4.5. The added mass is about 0.5 kg, which is close to the 0.6 kg limit. (`cost_data#1`)
- cost: 3-3.5. The unit cost increase is about 12%, which is close to the 15% limit, and is within the acceptable range. (`cost_data#0`)
- robustness: 4-4.5. Sealed bushings have been effective in preventing failures in dust tests, and the linkage has passed the full 500 h test. The design allows the tool to work from -15 °C to +40 °C without issues. (`dust_sealing_lessons#0`, `decoupled_handle_linkage#1`)
- development_effort: 3-3.5. The concept requires additional parts and tooling, indicating a moderate development effort compared to other concepts. (`decoupled_handle_linkage#1`)

### C2 C2 - Silicone Compounds
- vibration_reduction: 3.5-4.5. Silicone compounds can provide better performance in cold weather, and a 50 to 70 percent reduction from 7.5 m/s² is expected, but the exact reduction is not specified. (`cold_weather_field_report#1`, `elastomer_isolators#2`)
- mass: 3-3.5. Adding silicone mounts adds about 0.1 kg, which is close to the limit but not over it. (`elastomer_isolators#1`)
- cost: 3-4. The increase in cost is 3 to 5 percent, which is within the allowed limit of 15 percent increase. (`cost_data#0`)
- robustness: 4-4.5. Silicone mounts are expected to perform well in cold weather, and the tool is expected to survive dust and rain exposure. No exposed moving parts jam. (`cold_weather_field_report#1`, `elastomer_isolators#2`, `dust_sealing_lessons#0`)
- development_effort: 4.5-5. The concept does not require significant changes to the existing design, as the mounts fit in the existing handle interface. (`elastomer_isolators#1`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `added_mass_postmortem#0`: Post-mortem: added ballast mass in the housing (dropped concept) - What was tried
- `added_mass_postmortem#1`: Post-mortem: added ballast mass in the housing (dropped concept) - Result
- `added_mass_postmortem#2`: Post-mortem: added ballast mass in the housing (dropped concept) - Lesson
- `cold_weather_field_report#0`: Field report: handle isolators in Nordic winter - Observation
- `cold_weather_field_report#1`: Field report: handle isolators in Nordic winter - Fix
- `cost_data#0`: Indicative cost data for handle vibration solutions - Unit cost increase (approximate)
- `cost_data#1`: Indicative cost data for handle vibration solutions - Tooling
- `damping_materials#0`: Viscoelastic damping layers - Effect
- `decoupled_handle_linkage#0`: Decoupled handle on a parallel linkage - Principle and typical effect
- `decoupled_handle_linkage#1`: Decoupled handle on a parallel linkage - Design issues
- `dust_sealing_lessons#0`: Lessons on dust and rain sealing - Moving parts
- `elastomer_isolators#0`: Elastomer handle isolators - Principle and typical effect
- `elastomer_isolators#1`: Elastomer handle isolators - Mass, cost and packaging
- `elastomer_isolators#2`: Elastomer handle isolators - Temperature behaviour
- `handle_geometry#1`: Handle geometry and grip - Use
- `source_balancing#0`: Reducing vibration at the source - Principle and typical effect
- `source_balancing#1`: Reducing vibration at the source - Cost of change
- `steel_spring_isolators#0`: Steel spring handle suspension - Principle and typical effect
- `steel_spring_isolators#1`: Steel spring handle suspension - Design issues
- `test_method_notes#0`: Vibration test method notes - Measurement
- `tuned_mass_absorber#0`: Tuned mass absorber on the handle - Principle and typical effect
- `tuned_mass_absorber#1`: Tuned mass absorber on the handle - Limitations

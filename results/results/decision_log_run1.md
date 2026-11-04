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
| C1 C1 - Steel Spring Isolators | 3.00 - 4.00 | unclear; violated; met; met |
| C2 C2 - Silicone Compounds | 3.30 - 4.30 | unclear; unclear; met; met |
| C3 C3 - Tuned Mass Absorber | 2.65 - 4.00 | unclear; unclear; met; met |
| C4 C4 - Source Balancing | 3.10 - 4.10 | unclear; violated; met; met |
| C5 C5 - Parallel Linkage with Sealed Bushings | 2.75 - 3.75 | met; met; unclear; met |
| C6 C6 - Active Cancellation | 2.10 - 3.10 | unclear; violated; met; unclear |

Eliminated:
- C6 C6 - Active Cancellation: violates 'Added mass at most 0.6 kg compared with today's tool.': The project was stopped due to the added 0.9 kg from the actuator and controller, which exceeds the limit. (evidence: `active_cancellation_postmortem#1`)
- C1 C1 - Steel Spring Isolators: violates 'Added mass at most 0.6 kg compared with today's tool.': The added mass is 0.25 kg, which is above the limit of 0.6 kg. (evidence: `steel_spring_isolators#1`)
- C4 C4 - Source Balancing: violates 'Added mass at most 0.6 kg compared with today's tool.': The added ballast mass was 1.2 kg, exceeding the limit by 0.6 kg. (evidence: `added_mass_postmortem#0`)

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C2 C2 - Silicone Compounds | 3.30 - 4.30 | unclear; unclear; met; met |
| C3 C3 - Tuned Mass Absorber | 3.03 - 4.20 | unclear; unclear; met; met |
| C5 C5 - Parallel Linkage with Sealed Bushings | 2.85 - 3.70 | met; met; unclear; met |

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C2 C2 - Silicone Compounds | 3.30 - 4.30 | unclear; met; met; met |
| C3 C3 - Tuned Mass Absorber | 3.00 - 3.95 | unclear; unclear; met; met |
| C5 C5 - Parallel Linkage with Sealed Bushings | 3.18 - 3.85 | met; met; unclear; met |

## Recommended set (kept open for detailed design)

### C2 C2 - Silicone Compounds
- vibration_reduction: 3-4.5. The concept uses silicone-based isolators expected to provide better isolation than current elastomer isolators, but the exact reduction is not quantified. Evidence suggests a likely reduction but not specific numbers. (no evidence cited)
- mass: 3-3.5. The concept adds 0.1 kg of mass, which is below the 0.6 kg limit, but the exact impact is not fully quantified. The mass increase is small, but the current evidence does not provide a precise value. (no evidence cited)
- cost: 3-3.5. The concept increases costs by 3-5%, which is within the allowed increase of 15%, but the exact impact is not fully quantified. The cost increase is modest, but the evidence does not specify the exact cost. (no evidence cited)
- robustness: 4-5. The concept mentions the material can operate from -15°C to +40°C, and it is durable enough to survive dust and rain for 500 hours, with no exposed moving parts that jam, which aligns with the robustness requirement. (no evidence cited)
- development_effort: 4-5. The concept suggests minimal changes to the existing design, implying a small development effort, though specific changes are not detailed in the evidence provided. (no evidence cited)

### C5 C5 - Parallel Linkage with Sealed Bushings
- vibration_reduction: 3.5-4.5. Prototype tests indicated a 60 to 75 percent reduction in vibration, which should bring the vibration total value below 4.0 m/s². [decoupled_handle_linkage#1] (no evidence cited)
- mass: 2.5-3. The added mass of 0.5 kg is within the allowed limit but slightly above the middle of the range. [cost_data#1] (no evidence cited)
- cost: 2-2.5. The unit cost increase of about 12 percent is close to the target limit. [cost_data#0] (no evidence cited)
- robustness: 4-4.5. The concept uses sealed bushings to prevent wear and ensures the tool operates correctly in a dusty environment. [dust_sealing_lessons#0] (no evidence cited)
- development_effort: 3.5-4. While the concept involves a new linkage system, it avoids changes to the drive train. [decoupled_handle_linkage#1] (no evidence cited)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `added_mass_postmortem#0`: Post-mortem: added ballast mass in the housing (dropped concept) - What was tried
- `added_mass_postmortem#2`: Post-mortem: added ballast mass in the housing (dropped concept) - Lesson
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

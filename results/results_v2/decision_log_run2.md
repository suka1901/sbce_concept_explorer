# Decision log

## Scouting queries

- vibration reduction techniques for hand-held tools#2
- mass optimization methods for reducing vibration#3
- environmental durability tests for outdoor tools#4
- cost analysis of vibration isolation materials for tool handles#5
- handle design considerations for vibration reduction#6

## Concepts

- **C1 C1** (Steel springs): Steel spring handle suspension reduces vibration by isolating the handles from the tool’s vibration source. This approach uses minimal damping, requiring additional end stops and a small damper to prevent resonance.
- **C2 C2** (Source balancing): Reducing vibration at the source by balancing the rotating parts or adding a counter-rotating mass, which can be done without changing the drive train but requires significant development time.
- **C3 C3** (Natural-rubber mounts): Using natural-rubber mounts to dampen vibrations between the tool and the handle, offering a cost-effective solution with a slight increase in unit cost.
- **C4 C4** (Silicone-compound mounts): Silicone-compound mounts provide a moderate vibration reduction with a moderate increase in unit cost compared to natural-rubber mounts.
- **C5 C5** (Handle geometry and grip): Improving handle geometry and grip to enhance comfort and control, with minimal impact on vibration transmission, but slight improvement in handle feel.
- **C6 C6** (Active cancellation (not recommended)): Active vibration cancellation at the handle, which is not recommended due to high power, mass, and sealing requirements, but included for comparison.

## Round 0

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 | 3.20 - 4.20 | unclear; met; met; met |
| C2 C2 | 2.90 - 3.90 | met; unclear; unclear; unclear |
| C3 C3 | 3.45 - 4.00 | unclear; met; unclear; met |
| C4 C4 | 3.15 - 4.15 | unclear; met; unclear; met |
| C5 C5 | 3.85 - 4.65 | unclear; unclear; met; unclear |
| C6 C6 | 1.55 - 2.85 | unclear; violated; met; met |

Eliminated:
- C6 C6: violates 'Added mass at most 0.6 kg compared with today's tool.': The added mass of 0.9 kg exceeds the allowed limit of 0.6 kg. (evidence: `active_cancellation_postmortem#1`)

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 | 3.20 - 4.20 | unclear; met; met; met |
| C2 C2 | 2.55 - 3.55 | met; unclear; unclear; unclear |
| C3 C3 | 3.62 - 4.00 | unclear; met; unclear; met |
| C4 C4 | 3.15 - 4.50 | unclear; met; unclear; met |
| C5 C5 | 4.00 - 4.67 | unclear; unclear; met; unclear |

Eliminated:
- C2 C2: optimistic score 3.55 is below the pessimistic score 4.00 of C5

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 | 3.92 - 4.42 | unclear; met; met; met |
| C3 C3 | 3.45 - 4.00 | unclear; met; unclear; met |
| C4 C4 | 3.50 - 4.50 | unclear; met; unclear; met |
| C5 C5 | 4.00 - 4.67 | unclear; unclear; met; unclear |

## Recommended set (kept open for detailed design)

### C5 C5
- vibration_reduction: 3.5-4.5. Steel spring handle suspension is expected to reduce vibration by 40 to 60 percent, but the exact reduction is uncertain. (`steel_spring_isolators#0`)
- mass: 4-4.5. Adding steel spring isolators might add some mass, but the increase is expected to be within the allowed limit. (`handle_geometry#1`)
- cost: 4.5-5. The addition of steel spring isolators is a relatively simple modification, likely resulting in a negligible cost increase. (`handle_geometry#1`)
- robustness: 4.5-5. The steel spring isolators are designed to maintain their stiffness over a wide temperature range, supporting robustness. (`steel_spring_isolators#0`)
- development_effort: 4-4.5. Introducing steel spring isolators is a moderate change that avoids altering the drive train, keeping the development effort within a reasonable range. (`handle_geometry#1`)

### C1 C1
- vibration_reduction: 3.5-4. Based on bench tests, it is expected to achieve 40 to 60 percent lower vibration, which translates to a reduction to around 4.5 to 3.0 m/s², just below the target of 4.0 m/s². (`steel_spring_isolators#0`, `steel_spring_isolators#1`)
- mass: 4-4.5. Added mass is 0.25 kg, which is well below the 0.6 kg limit. (`steel_spring_isolators#1`)
- cost: 4-4.5. The unit cost increase is about 6 to 8 percent, which is within the allowed increase of 15 percent. (`cost_data#0`, `steel_spring_isolators#1`)
- robustness: 4.5-5. The design works over the temperature range and has a history of surviving dust and rain without issues. (`steel_spring_isolators#1`)
- development_effort: 4-4.5. While it introduces new components, it does not require a new drive train or electronics, making the change moderate in effort. (`steel_spring_isolators#1`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `cold_weather_field_report#0`: Field report: handle isolators in Nordic winter - Observation
- `cold_weather_field_report#1`: Field report: handle isolators in Nordic winter - Fix
- `cost_data#0`: Indicative cost data for handle vibration solutions - Unit cost increase (approximate)
- `damping_materials#0`: Viscoelastic damping layers - Effect
- `decoupled_handle_linkage#0`: Decoupled handle on a parallel linkage - Principle and typical effect
- `dust_sealing_lessons#0`: Lessons on dust and rain sealing - Moving parts
- `dust_sealing_lessons#1`: Lessons on dust and rain sealing - Electronics
- `elastomer_isolators#0`: Elastomer handle isolators - Principle and typical effect
- `elastomer_isolators#1`: Elastomer handle isolators - Mass, cost and packaging
- `elastomer_isolators#2`: Elastomer handle isolators - Temperature behaviour
- `handle_geometry#0`: Handle geometry and grip - Effect
- `handle_geometry#1`: Handle geometry and grip - Use
- `source_balancing#0`: Reducing vibration at the source - Principle and typical effect
- `source_balancing#1`: Reducing vibration at the source - Cost of change
- `steel_spring_isolators#0`: Steel spring handle suspension - Principle and typical effect
- `steel_spring_isolators#1`: Steel spring handle suspension - Design issues
- `test_method_notes#0`: Vibration test method notes - Measurement
- `tuned_mass_absorber#0`: Tuned mass absorber on the handle - Principle and typical effect
- `tuned_mass_absorber#1`: Tuned mass absorber on the handle - Limitations

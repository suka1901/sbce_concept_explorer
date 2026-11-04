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
| C1 C1 | 3.00 - 4.00 | unclear; met; met; met |
| C2 C2 | 3.10 - 4.10 | unclear; unclear; met; unclear |
| C3 C3 | 3.10 - 4.10 | unclear; met; unclear; met |
| C4 C4 | 2.85 - 4.20 | unclear; met; met; unclear |
| C5 C5 | 3.20 - 4.20 | unclear; unclear; met; unclear |
| C6 C6 | 1.75 - 2.75 | unclear; violated; met; unclear |

Eliminated:
- C6 C6: violates 'Added mass at most 0.6 kg compared with today's tool': The active cancellation added 0.9 kg, exceeding the allowed limit. (evidence: `active_cancellation_postmortem#1`)

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 | 3.17 - 4.17 | unclear; met; met; met |
| C2 C2 | 2.93 - 4.10 | unclear; unclear; met; unclear |
| C3 C3 | 3.35 - 4.12 | unclear; met; unclear; met |
| C4 C4 | 3.40 - 4.30 | unclear; met; met; unclear |
| C5 C5 | 3.10 - 4.10 | unclear; unclear; met; unclear |

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 | 3.00 - 4.17 | unclear; met; met; met |
| C2 C2 | 2.83 - 4.00 | unclear; unclear; met; unclear |
| C3 C3 | 3.35 - 4.12 | unclear; met; unclear; met |
| C4 C4 | 3.50 - 4.40 | unclear; met; met; unclear |
| C5 C5 | 3.26 - 4.26 | unclear; unclear; met; unclear |

## Recommended set (kept open for detailed design)

### C4 C4
- vibration_reduction: 3.5-4.5. The concept aims for moderate vibration reduction, and silicone-compound mounts typically reduce vibration by 30 to 50 percent, which is in the 3.0 to 4.0 m/s² range. (`elastomer_isolators#1`, `tuned_mass_absorber#0`, `test_method_notes#0`)
- mass: 4-4.5. The silicone-compound mounts add about 0.1 kg, which is within the 0.6 kg limit but close to the upper bound. (`elastomer_isolators#1`)
- cost: 2.5-3.5. The cost increase is moderate at about 3 to 5 percent, which is acceptable but near the limit. (`cost_data#0`)
- robustness: 4-5. The silicone compound maintains performance down to -30 °C, which covers -15 °C, and the concept is expected to survive the IP54 test. (`cold_weather_field_report#0`, `cold_weather_field_report#1`)
- development_effort: 3-4. The concept involves a moderate change to the existing design and does not specify if the drive train needs to be altered. (`handle_geometry#1`, `test_method_notes#0`)

### C5 C5
- vibration_reduction: 3.5-4.5. [handle_geometry#0], [handle_geometry#1], [steel_spring_isolators#0] (`handle_geometry#0`, `handle_geometry#1`, `steel_spring_isolators#0`)
- mass: 2.6-3.6. [steel_spring_isolators#0] (`steel_spring_isolators#0`)
- cost: 2.8-3.8. [steel_spring_isolators#0] (`steel_spring_isolators#0`)
- robustness: 4-5. [steel_spring_isolators#0] (`steel_spring_isolators#0`)
- development_effort: 3-4. [steel_spring_isolators#0] (`steel_spring_isolators#0`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `cold_weather_field_report#0`: Field report: handle isolators in Nordic winter - Observation
- `cold_weather_field_report#1`: Field report: handle isolators in Nordic winter - Fix
- `cost_data#0`: Indicative cost data for handle vibration solutions - Unit cost increase (approximate)
- `damping_materials#0`: Viscoelastic damping layers - Effect
- `decoupled_handle_linkage#0`: Decoupled handle on a parallel linkage - Principle and typical effect
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

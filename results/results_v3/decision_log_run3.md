# Decision log

## Scouting queries

- vibration reduction techniques for hand-held tools#2
- mass optimization for vibration reduction in tools#3
- survival of electronic components in dust and rain environments#4
- long-term durability of mechanical components under temperature extremes#5
- cost analysis of adding vibration isolators to hand tools#6

## Concepts

- **C1 C1 - Handle Geometry Optimization** (Handle shape and grip): Adjust the handle’s shape and grip to improve operator comfort and potentially reduce perceived vibration.
- **C2 C2 - Elastomer Mounts** (Elastomeric isolators): Use four natural-rubber isolators on the handle to absorb vibrations. They add minimal mass and cost.
- **C3 C3 - Tuned Mass Absorber** (Variable frequency isolation): Install a tuned mass absorber on the handle to isolate vibrations at the tool’s operating frequency. This could reduce vibration by 10-20% but may not be frequency-independent.
- **C4 C4 - Parallel Linkage with Sealed Bushings** (Mechanical damping and sealing): Implement a parallel linkage with sealed bushings and a damper to reduce vibrations. This concept is costlier but provides broad-band vibration reduction.
- **C5 C5 - Active Vibration Cancellation** (Active cancellation): Introduce active vibration cancellation, despite previous failure. This could reduce vibrations significantly but would be expensive and complex.
- **C6 C6 - Viscoelastic Damping Layers** (Broad-band vibration reduction): Apply viscoelastic damping layers on the handle tube or housing to reduce resonant peaks and provide broad-band vibration reduction. However, effectiveness may drop in cold conditions.

## Round 0

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Handle Geometry Optimization | 3.05 - 4.05 | unclear; unclear; unclear; unclear |
| C2 C2 - Elastomer Mounts | 3.00 - 4.30 | unclear; met; violated; unclear |
| C3 C3 - Tuned Mass Absorber | 3.40 - 4.20 | met; met; unclear; met |
| C4 C4 - Parallel Linkage with Sealed Bushings | 2.75 - 3.75 | met; met; unclear; met |
| C5 C5 - Active Vibration Cancellation | 1.90 - 2.90 | violated; violated; unclear; unclear |
| C6 C6 - Viscoelastic Damping Layers | 3.30 - 4.10 | unclear; unclear; unclear; unclear |

Eliminated:
- C5 C5 - Active Vibration Cancellation: violates 'Vibration total value at the rear handle at most 4.0 m/s² in the standard test': 70% reduction in lab test; original value 7.5 m/s², so 4.5 m/s² after reduction vs 4.0 m/s²: 4.5 m/s² is slightly above 4.0 m/s² (evidence: `test_method_notes#0`, `active_cancellation_postmortem#0`)
- C2 C2 - Elastomer Mounts: violates 'Works from -15 °C to +40 °C': Natural rubber stiffens below -10 °C, causing a 25% increase in handle vibration vs Works from -15 °C to +40 °C: Natural rubber will stiffen below -15 °C, causing a 25% increase in handle vibration, making it not meet the requirement over the full temperature range (evidence: `elastomer_isolators#2`, `cold_weather_field_report#0`)

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Handle Geometry Optimization | 3.05 - 4.05 | unclear; unclear; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 3.20 - 4.20 | met; met; unclear; met |
| C4 C4 - Parallel Linkage with Sealed Bushings | 3.15 - 4.15 | met; met; unclear; met |
| C6 C6 - Viscoelastic Damping Layers | 3.20 - 4.00 | unclear; unclear; unclear; unclear |

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Handle Geometry Optimization | 2.85 - 3.85 | unclear; unclear; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 3.77 - 4.50 | met; met; unclear; met |
| C4 C4 - Parallel Linkage with Sealed Bushings | 3.12 - 4.30 | met; met; unclear; met |
| C6 C6 - Viscoelastic Damping Layers | 2.65 - 3.62 | unclear; unclear; unclear; unclear |

Eliminated:
- C6 C6 - Viscoelastic Damping Layers: optimistic score 3.62 is below the pessimistic score 3.77 of C3

## Recommended set (kept open for detailed design)

### C3 C3 - Tuned Mass Absorber
- vibration_reduction: 3.5-4.5. The evidence states that the effect is narrow-band and the reduction away from the tuned frequency is limited to 10 to 20 percent, while a 50 to 70 percent reduction was measured on a test rig, indicating a moderate to good potential reduction, but the exact reduction is uncertain. (`tuned_mass_absorber#1`, `tuned_mass_absorber#0`)
- mass: 4-4.5. The added mass is usually 0.3 to 0.8 kg, which is within the allowed limit of 0.6 kg, and the reduction from 7.5 m/s² to 4.0 m/s² is significant, indicating a good mass reduction. (`tuned_mass_absorber#1`, `tuned_mass_absorber#0`)
- cost: 4-4.5. The cost increase is about 5 percent, which is within the allowed limit of 15 percent, and the reduction in vibration is significant, indicating a good cost reduction. (`tuned_mass_absorber#1`, `cost_data#0`)
- robustness: 4-4.5. The evidence does not provide specific information on the robustness of the tuned mass absorber, but it does not indicate any issues with temperature or environmental conditions, and proper sealing can ensure the tool survives dust and rain. (`tuned_mass_absorber#1`, `dust_sealing_lessons#0`)
- development_effort: 3.5-4.5. The concept may require changes to the tool design, as the evidence suggests the effect is narrow-band and limited, which may necessitate adjustments to the tool's operating parameters, but the reduction in vibration is significant, indicating a moderate development effort. (`tuned_mass_absorber#1`, `source_balancing#0`, `handle_geometry#1`)

### C4 C4 - Parallel Linkage with Sealed Bushings
- vibration_reduction: 3-4.5. Prototype tests showed a 60 to 75 percent reduction in vibration, which is within the requirement of a 4.0 m/s² vibration total value at the rear handle. This is near the high end of the requirement, but the exact reduction is uncertain. (`decoupled_handle_linkage#0`, `decoupled_handle_linkage#1`)
- mass: 3-4. The concept adds about 0.5 kg, which is close to the 0.6 kg limit. This is within the allowed range, but it is near the upper limit. (`decoupled_handle_linkage#1`)
- cost: 2.5-3.5. The cost increase is approximately 12 percent, which is close to the 15 percent limit. This is within the allowed range, but it is near the upper limit. (`cost_data#0`, `cost_data#1`)
- robustness: 4-5. Sealed bushings used in the concept will prevent moving parts from jamming and ensure the tool survives the 500-hour dust and rain test. This is well within the requirement. (`dust_sealing_lessons#0`, `dust_sealing_lessons#1`, `decoupled_handle_linkage#1`)
- development_effort: 3-4. The design involves adding a parallel linkage, increasing the number of parts and potentially development effort. While it is a significant change, it is not as large as a new drive train or electronics. (`decoupled_handle_linkage#1`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `cold_weather_field_report#0`: Field report: handle isolators in Nordic winter - Observation
- `cost_data#0`: Indicative cost data for handle vibration solutions - Unit cost increase (approximate)
- `cost_data#1`: Indicative cost data for handle vibration solutions - Tooling
- `damping_materials#0`: Viscoelastic damping layers - Effect
- `decoupled_handle_linkage#0`: Decoupled handle on a parallel linkage - Principle and typical effect
- `decoupled_handle_linkage#1`: Decoupled handle on a parallel linkage - Design issues
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
- `test_method_notes#0`: Vibration test method notes - Measurement
- `tuned_mass_absorber#0`: Tuned mass absorber on the handle - Principle and typical effect
- `tuned_mass_absorber#1`: Tuned mass absorber on the handle - Limitations

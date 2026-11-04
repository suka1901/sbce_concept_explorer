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
| C1 C1 - Handle Geometry Optimization | 3.50 - 4.30 | unclear; unclear; met; met |
| C2 C2 - Elastomer Mounts | 3.45 - 4.45 | unclear; met; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 3.50 - 3.85 | unclear; met; met; met |
| C4 C4 - Parallel Linkage with Sealed Bushings | 2.75 - 3.75 | unclear; unclear; met; met |
| C5 C5 - Active Vibration Cancellation | 1.75 - 2.75 | unclear; violated; met; unclear |
| C6 C6 - Viscoelastic Damping Layers | 3.20 - 3.85 | unclear; met; unclear; unclear |

Eliminated:
- C5 C5 - Active Vibration Cancellation: violates 'Added mass at most 0.6 kg compared with today's tool': Added 0.9 kg of mass, which is 0.3 kg over the allowed limit. (evidence: `active_cancellation_postmortem#2`)

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Handle Geometry Optimization | 3.65 - 4.60 | unclear; unclear; met; met |
| C2 C2 - Elastomer Mounts | 3.45 - 4.45 | unclear; met; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 3.50 - 3.85 | unclear; met; met; met |
| C4 C4 - Parallel Linkage with Sealed Bushings | 3.08 - 3.80 | unclear; unclear; met; met |
| C6 C6 - Viscoelastic Damping Layers | 3.00 - 3.65 | unclear; met; unclear; unclear |

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Handle Geometry Optimization | 3.20 - 3.88 | unclear; unclear; met; met |
| C2 C2 - Elastomer Mounts | 3.52 - 4.12 | unclear; met; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 3.10 - 3.50 | unclear; met; met; met |
| C4 C4 - Parallel Linkage with Sealed Bushings | 3.00 - 3.97 | met; met; unclear; met |
| C6 C6 - Viscoelastic Damping Layers | 2.80 - 3.45 | unclear; met; unclear; unclear |

Eliminated:
- C6 C6 - Viscoelastic Damping Layers: optimistic score 3.45 is below the pessimistic score 3.52 of C2
- C3 C3 - Tuned Mass Absorber: optimistic score 3.50 is below the pessimistic score 3.52 of C2

## Recommended set (kept open for detailed design)

### C2 C2 - Elastomer Mounts
- vibration_reduction: 3.5-4. The isolation effect of 30 to 50 percent is expected, but the exact value after applying the isolators is uncertain, especially considering the cold-weather performance. (`elastomer_isolators#0`, `elastomer_isolators#2`, `cold_weather_field_report#0`)
- mass: 4-4.5. The added mass of 0.1 kg is significantly below the 0.6 kg limit. (`elastomer_isolators#1`)
- cost: 4-4.5. The unit cost increase is expected to be small, around 2 to 4 percent, which is acceptable. (`elastomer_isolators#1`)
- robustness: 2.5-3.5. The isolators may not perform optimally below -10 °C, and the robustness against dust and rain is not explicitly mentioned, but it is a small change that might be manageable. (`elastomer_isolators#2`)
- development_effort: 4-4.5. Minor tooling changes are required, which is a small change to the design. (`elastomer_isolators#1`)

### C1 C1 - Handle Geometry Optimization
- vibration_reduction: 3-4. [handle_geometry#0, elastomer_isolators#0, tuned_mass_absorber#0] Handle geometry and grip alone reduce vibration by 5-10%, elastomer isolators reduce it by 30-50%, and tuned mass absorbers offer up to 70% reduction, but the combined effect is hard to predict and could range from 30-40%. (`handle_geometry#0`, `elastomer_isolators#0`, `tuned_mass_absorber#0`)
- mass: 3-3.5. [elastomer_isolators#0, tuned_mass_absorber#1] Adding elastomer isolators and tuned mass absorbers could add up to 0.7 kg, which is close to the 0.6 kg limit. (`elastomer_isolators#0`, `tuned_mass_absorber#1`)
- cost: 3-3.5. [elastomer_isolators#0, tuned_mass_absorber#1] The cost increase from elastomer isolators is about 0.6 kg, and the tuned mass absorber adds about 5% cost, but the overall cost impact is uncertain. (`elastomer_isolators#0`, `tuned_mass_absorber#1`)
- robustness: 4-4.5. No specific evidence contradicts this requirement, and it is a standard design consideration. (no evidence cited)
- development_effort: 3-3.5. [handle_geometry#1, tuned_mass_absorber#1] Handle geometry and grip changes are straightforward, but the effect on vibration needs to be verified. Tuned mass absorbers require additional development effort. (`handle_geometry#1`, `tuned_mass_absorber#1`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `added_mass_postmortem#2`: Post-mortem: added ballast mass in the housing (dropped concept) - Lesson
- `cold_weather_field_report#0`: Field report: handle isolators in Nordic winter - Observation
- `cold_weather_field_report#1`: Field report: handle isolators in Nordic winter - Fix
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
- `steel_spring_isolators#1`: Steel spring handle suspension - Design issues
- `test_method_notes#0`: Vibration test method notes - Measurement
- `tuned_mass_absorber#0`: Tuned mass absorber on the handle - Principle and typical effect
- `tuned_mass_absorber#1`: Tuned mass absorber on the handle - Limitations

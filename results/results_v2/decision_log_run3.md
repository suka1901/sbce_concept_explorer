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
| C1 C1 - Handle Geometry Optimization | 3.50 - 4.30 | unclear; unclear; met; unclear |
| C2 C2 - Elastomer Mounts | 3.30 - 4.30 | unclear; met; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 3.20 - 4.20 | unclear; met; unclear; unclear |
| C4 C4 - Parallel Linkage with Sealed Bushings | 2.75 - 3.75 | unclear; met; unclear; met |
| C5 C5 - Active Vibration Cancellation | 1.55 - 3.55 | unclear; violated; unclear; unclear |
| C6 C6 - Viscoelastic Damping Layers | 3.40 - 4.40 | unclear; unclear; met; unclear |

Eliminated:
- C5 C5 - Active Vibration Cancellation: violates 'Added mass at most 0.6 kg compared with today's tool.': Added 0.9 kg, which is 0.3 kg over the limit. (evidence: `active_cancellation_postmortem#1`)

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Handle Geometry Optimization | 3.70 - 4.47 | unclear; unclear; met; unclear |
| C2 C2 - Elastomer Mounts | 3.50 - 4.45 | unclear; met; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 2.90 - 3.57 | unclear; met; unclear; unclear |
| C4 C4 - Parallel Linkage with Sealed Bushings | 2.85 - 3.85 | unclear; met; unclear; met |
| C6 C6 - Viscoelastic Damping Layers | 2.55 - 3.55 | unclear; unclear; met; unclear |

Eliminated:
- C6 C6 - Viscoelastic Damping Layers: optimistic score 3.55 is below the pessimistic score 3.70 of C1
- C3 C3 - Tuned Mass Absorber: optimistic score 3.57 is below the pessimistic score 3.70 of C1

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Handle Geometry Optimization | 3.88 - 4.83 | unclear; unclear; met; unclear |
| C2 C2 - Elastomer Mounts | 3.32 - 4.45 | unclear; met; unclear; unclear |
| C4 C4 - Parallel Linkage with Sealed Bushings | 3.05 - 3.80 | unclear; met; unclear; met |

Eliminated:
- C4 C4 - Parallel Linkage with Sealed Bushings: optimistic score 3.80 is below the pessimistic score 3.88 of C1

## Recommended set (kept open for detailed design)

### C1 C1 - Handle Geometry Optimization
- vibration_reduction: 3-4.5. Handle geometry and elastomer isolators can provide some reduction, and a tuned mass absorber can significantly reduce vibration at its tuned frequency. (`handle_geometry#0`, `elastomer_isolators#0`, `tuned_mass_absorber#0`)
- mass: 4.5-5. While handle geometry optimization is cheap, the added mass is minimal, and the exact impact is uncertain. (`handle_geometry#1`)
- cost: 4.5-5. Handle geometry optimization is cheap, and elastomer isolators are likely to be cost-effective, but the overall cost impact is uncertain. (`handle_geometry#1`)
- robustness: 4-5. The test method does not provide specific evidence, but the design constraints suggest it should meet the requirements. (`test_method_notes#0`)
- development_effort: 4.5-5. Minor changes to handle design and the potential for elastomer isolators, which might be a small change. (`handle_geometry#1`)

### C2 C2 - Elastomer Mounts
- vibration_reduction: 3-4.5. Rubber mounts are expected to reduce vibrations by 30 to 50 percent, potentially bringing the vibration total value down to 4.0 m/s² or below. (`elastomer_isolators#0`)
- mass: 4.5-5. The added mass is 0.1 kg, well below the 0.6 kg limit, and the tool design can accommodate it with minor changes. (`elastomer_isolators#1`)
- cost: 3.5-4.5. The cost increase is estimated to be 2 to 4 percent, which is within the acceptable range but might be seen as high for a minor improvement. (`elastomer_isolators#1`)
- robustness: 2-3.5. Natural rubber stiffens below -10 °C, which might affect performance, but it's not clear how much. (`elastomer_isolators#2`)
- development_effort: 4.5-5. The design change is small, involving only minor tooling changes, and the drive train remains unchanged. (`elastomer_isolators#1`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
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
- `test_method_notes#0`: Vibration test method notes - Measurement
- `tuned_mass_absorber#0`: Tuned mass absorber on the handle - Principle and typical effect
- `tuned_mass_absorber#1`: Tuned mass absorber on the handle - Limitations

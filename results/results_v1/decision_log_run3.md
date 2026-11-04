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
| C1 C1 - Handle Geometry Optimization | 3.35 - 4.15 | unclear; met; met; met |
| C2 C2 - Elastomer Mounts | 3.45 - 4.45 | unclear; met; unclear; met |
| C3 C3 - Tuned Mass Absorber | 2.55 - 3.90 | unclear; unclear; unclear; unclear |
| C4 C4 - Parallel Linkage with Sealed Bushings | 2.85 - 3.95 | unclear; violated; met; met |
| C5 C5 - Active Vibration Cancellation | 1.75 - 2.75 | unclear; violated; unclear; violated |
| C6 C6 - Viscoelastic Damping Layers | 3.45 - 4.45 | unclear; met; unclear; unclear |

Eliminated:
- C5 C5 - Active Vibration Cancellation: violates 'Added mass at most 0.6 kg compared with today's tool': The added mass was 0.9 kg, which exceeds the 0.6 kg limit. (evidence: `active_cancellation_postmortem#1`)
- C4 C4 - Parallel Linkage with Sealed Bushings: violates 'Added mass at most 0.6 kg compared with today's tool': Added mass is about 0.5 kg, slightly above the limit, but not negligible (evidence: `decoupled_handle_linkage#1`)

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Handle Geometry Optimization | 3.35 - 4.15 | unclear; met; met; met |
| C2 C2 - Elastomer Mounts | 3.45 - 4.45 | unclear; met; unclear; met |
| C3 C3 - Tuned Mass Absorber | 2.75 - 3.65 | unclear; unclear; unclear; unclear |
| C6 C6 - Viscoelastic Damping Layers | 3.27 - 4.05 | unclear; met; unclear; unclear |

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Handle Geometry Optimization | 3.35 - 4.15 | unclear; met; met; met |
| C2 C2 - Elastomer Mounts | 3.45 - 4.45 | unclear; met; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 2.93 - 3.65 | unclear; unclear; unclear; unclear |
| C6 C6 - Viscoelastic Damping Layers | 3.00 - 3.82 | unclear; unclear; unclear; unclear |

## Recommended set (kept open for detailed design)

### C2 C2 - Elastomer Mounts
- vibration_reduction: 3-4. The expected reduction is 30 to 50 percent, but it is uncertain whether this will meet the 4.0 m/s² limit due to the natural rubber's stiffness at low temperatures. (`elastomer_isolators#0`, `elastomer_isolators#2`)
- mass: 4-5. The added mass is 0.1 kg, which is well below the limit. (`elastomer_isolators#1`)
- cost: 4-5. The unit cost increase is small, roughly 2 to 4 percent, which is below the limit. (`elastomer_isolators#1`)
- robustness: 3-4. The isolators work within the temperature range, but the performance at -15 °C and below is uncertain due to the natural rubber's stiffness. (`elastomer_isolators#2`)
- development_effort: 4-5. The change is small, requiring only minor tooling changes, and no new drive train is needed. (`elastomer_isolators#1`)

### C1 C1 - Handle Geometry Optimization
- vibration_reduction: 2-3. [handle_geometry#0, elastomer_isolators#0] Handle geometry alone reduces vibration by 5-10%, while isolators can further reduce it by 30-50%. Combined, the effect is likely to be in this range, but not sufficient to meet the target without additional measures. (`handle_geometry#0`, `elastomer_isolators#0`)
- mass: 4-5. [handle_geometry#1] The mass increase is expected to be within the limit as indicated by the evidence. (`handle_geometry#1`)
- cost: 3-4. [handle_geometry#1] The cost increase is expected to be low to moderate, but precise prediction is uncertain without detailed costing. The isolators might add a small cost but are within the acceptable range. (`handle_geometry#1`)
- robustness: 5-5. [handle_geometry#1] The changes do not introduce any new components that could fail under harsh conditions. The standard test conditions for dust and rain are well within the expected operational environment. (`handle_geometry#1`)
- development_effort: 4-5. [handle_geometry#1] The changes involve modifying the handle without altering the drive train or electronics. This is considered a small change. (`handle_geometry#1`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `cold_weather_field_report#0`: Field report: handle isolators in Nordic winter - Observation
- `cold_weather_field_report#1`: Field report: handle isolators in Nordic winter - Fix
- `cost_data#0`: Indicative cost data for handle vibration solutions - Unit cost increase (approximate)
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
- `test_method_notes#0`: Vibration test method notes - Measurement
- `tuned_mass_absorber#0`: Tuned mass absorber on the handle - Principle and typical effect
- `tuned_mass_absorber#1`: Tuned mass absorber on the handle - Limitations

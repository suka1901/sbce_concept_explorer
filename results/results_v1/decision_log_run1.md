# Decision log

## Scouting queries

- vibration reduction techniques for handheld tools#1
- mass optimization in handheld tool design#2
- environmental durability testing for construction tools#3
- cost analysis of vibration isolators for hand tools#4
- operator comfort and control in high-vibration tools#5

## Concepts

- **C1 C1 - Steel Spring Isolators** (Steel spring suspension): Steel spring isolators are used to reduce vibration, but require damping and guide pins to prevent resonance and wear.
- **C2 C2 - Elastomer Isolators** (Elastomer mounts): Elastomer mounts act as a low-pass filter, reducing vibration by 30 to 50 percent, but softer mounts may reduce control and feel loose.
- **C3 C3 - Tuned Mass Absorber** (Tuned mass damper): A tuned mass absorber is added to the tool to absorb specific vibration frequencies, but this concept has a high cost.
- **C4 C4 - Parallel Linkage with Sealed Bushings and Damper** (Parallel linkage dampening): A complex linkage with sealed bushings and a damper is used to reduce vibration, leading to a significant increase in cost.
- **C5 C5 - Handle Geometry and Grip** (Handle geometry): Improving the handle geometry and grip enhances comfort and control but has only a minor effect on reducing vibration.
- **C6 C6 - Active Vibration Cancellation** (Active vibration cancellation): Active vibration cancellation is considered, but the project was stopped due to unresolved issues with power, mass, and sealing.

## Round 0

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Steel Spring Isolators | 2.75 - 3.75 | unclear; met; met; met |
| C2 C2 - Elastomer Isolators | 2.80 - 3.80 | unclear; met; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 3.10 - 4.10 | unclear; unclear; met; met |
| C4 C4 - Parallel Linkage with Sealed Bushings and Damper | 2.95 - 3.95 | unclear; met; unclear; met |
| C5 C5 - Handle Geometry and Grip | 3.30 - 4.30 | unclear; met; unclear; unclear |
| C6 C6 - Active Vibration Cancellation | 1.75 - 2.75 | unclear; violated; met; met |

Eliminated:
- C6 C6 - Active Vibration Cancellation: violates 'Added mass at most 0.6 kg compared with today's tool.': The added mass was 0.9 kg, which exceeds the 0.6 kg limit. (evidence: `active_cancellation_postmortem#1`)

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Steel Spring Isolators | 2.98 - 3.65 | unclear; met; met; unclear |
| C2 C2 - Elastomer Isolators | 3.25 - 4.25 | unclear; met; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 3.25 - 4.05 | unclear; unclear; met; met |
| C4 C4 - Parallel Linkage with Sealed Bushings and Damper | 2.77 - 3.77 | unclear; met; unclear; met |
| C5 C5 - Handle Geometry and Grip | 3.10 - 3.95 | unclear; met; unclear; unclear |

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Steel Spring Isolators | 2.55 - 3.38 | unclear; met; met; unclear |
| C2 C2 - Elastomer Isolators | 3.07 - 4.08 | unclear; met; unclear; unclear |
| C3 C3 - Tuned Mass Absorber | 2.97 - 3.70 | unclear; unclear; met; met |
| C4 C4 - Parallel Linkage with Sealed Bushings and Damper | 2.92 - 3.82 | unclear; met; unclear; met |
| C5 C5 - Handle Geometry and Grip | 3.10 - 3.95 | unclear; met; unclear; unclear |

## Recommended set (kept open for detailed design)

### C2 C2 - Elastomer Isolators
- vibration_reduction: 3.5-4.5. [elastomer_isolators#0] Elastomer handle isolators - Principle and typical effect: Rubber mounts between the handle and the housing act as a low-pass filter. With the mount natural frequency well below the dominant excitation frequency, handle vibration typically drops by 30 to 50 percent. (`elastomer_isolators#0`)
- mass: 3-4. [elastomer_isolators#1] Elastomer handle isolators - Mass, cost and packaging: Four natural-rubber mounts add about 0.1 kg. Unit cost increase is small, roughly 2 to 4 percent. (`elastomer_isolators#1`)
- cost: 3-4. [elastomer_isolators#1] Elastomer handle isolators - Mass, cost and packaging: Four natural-rubber mounts add about 0.1 kg. Unit cost increase is small, roughly 2 to 4 percent. (`elastomer_isolators#1`)
- robustness: 2-3. [elastomer_isolators#2] Elastomer handle isolators - Temperature behaviour: Natural rubber stiffens below about -10 °C. Stiffer mounts raise the natural frequency and the isolation effect falls. See the cold-weather field report for what happened on the previous generation. (`elastomer_isolators#2`)
- development_effort: 4-5. [elastomer_isolators#1] Elastomer handle isolators - Mass, cost and packaging: Four natural-rubber mounts add about 0.1 kg. Unit cost increase is small, roughly 2 to 4 percent. They fit in the existing handle interface with minor tooling changes. (`elastomer_isolators#1`)

### C5 C5 - Handle Geometry and Grip
- vibration_reduction: 2-3.5. [decoupled_handle_linkage#0]: The decoupled handle mechanism can provide a significant reduction of 60-75%, but the exact impact on the current 7.5 m/s² is uncertain. (`decoupled_handle_linkage#0`)
- mass: 4-4.5. [elastomer_isolators#1]: Adding 0.1 kg is under the 0.6 kg limit, but it still represents a non-negligible increase in mass. (`elastomer_isolators#1`)
- cost: 4-4.5. [elastomer_isolators#1]: The cost increase is small, around 2-4%, which is within the acceptable range. (`elastomer_isolators#1`)
- robustness: 3-3.5. The concept does not explicitly address robustness in temperature or environmental conditions, but given the lack of evidence against it, it is considered robust. (no evidence cited)
- development_effort: 4-4.5. [elastomer_isolators#1], [decoupled_handle_linkage#0]: The use of elastomer isolators and a parallel linkage mechanism are relatively simple modifications, not requiring a new drive train or electronics. (`elastomer_isolators#1`, `decoupled_handle_linkage#0`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `added_mass_postmortem#1`: Post-mortem: added ballast mass in the housing (dropped concept) - Result
- `added_mass_postmortem#2`: Post-mortem: added ballast mass in the housing (dropped concept) - Lesson
- `cold_weather_field_report#0`: Field report: handle isolators in Nordic winter - Observation
- `cold_weather_field_report#1`: Field report: handle isolators in Nordic winter - Fix
- `cost_data#0`: Indicative cost data for handle vibration solutions - Unit cost increase (approximate)
- `cost_data#1`: Indicative cost data for handle vibration solutions - Tooling
- `damping_materials#0`: Viscoelastic damping layers - Effect
- `decoupled_handle_linkage#0`: Decoupled handle on a parallel linkage - Principle and typical effect
- `decoupled_handle_linkage#1`: Decoupled handle on a parallel linkage - Design issues
- `elastomer_isolators#0`: Elastomer handle isolators - Principle and typical effect
- `elastomer_isolators#1`: Elastomer handle isolators - Mass, cost and packaging
- `elastomer_isolators#2`: Elastomer handle isolators - Temperature behaviour
- `handle_geometry#0`: Handle geometry and grip - Effect
- `handle_geometry#1`: Handle geometry and grip - Use
- `source_balancing#0`: Reducing vibration at the source - Principle and typical effect
- `steel_spring_isolators#0`: Steel spring handle suspension - Principle and typical effect
- `steel_spring_isolators#1`: Steel spring handle suspension - Design issues
- `test_method_notes#0`: Vibration test method notes - Measurement
- `tuned_mass_absorber#0`: Tuned mass absorber on the handle - Principle and typical effect
- `tuned_mass_absorber#1`: Tuned mass absorber on the handle - Limitations

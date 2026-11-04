# Decision log

## Scouting queries

- vibration reduction techniques for handheld tools#1
- mass optimization in handheld tool design#2
- environmental durability testing for construction tools#3
- cost analysis of vibration isolators for hand tools#4
- operator comfort and control in high-vibration tools#5

## Concepts

- **C1 C1 - Steel Spring Isolators** (Steel spring suspension): Steel spring isolators are used to dampen vibrations, but they require end stops and a small damper to avoid resonance, and they add about 0.25 kg of mass.
- **C2 C2 - Elastomer Isolators** (Elastomer vibration isolation): Natural-rubber mounts act as a low-pass filter, reducing vibration by 30 to 50 percent, but they become stiff at low temperatures, affecting performance.
- **C3 C3 - Parallel Linkage with Sealed Bushings** (Parallel linkage dampening): A parallel linkage system with sealed bushings and a damper can significantly reduce vibration, but it is costly, adding about 12 percent to the unit cost.
- **C4 C4 - Tuned Mass Damper** (Tuned mass damper): A tuned mass damper could be integrated into the handle design to absorb vibrations, but it would add about 5 percent to the unit cost.
- **C5 C5 - Handle Geometry and Grip** (Handle design for comfort): Improving the handle geometry and grip can enhance comfort and control, but the vibration reduction at the handle is minimal, around 5 to 10 percent.
- **C6 C6 - Passive Vibration Absorber** (Passive vibration absorber): A passive vibration absorber can be added without significantly increasing the unit cost, but its effectiveness in reducing vibrations is limited.

## Round 0

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Steel Spring Isolators | 3.20 - 4.20 | unclear; met; unclear; met |
| C2 C2 - Elastomer Isolators | 3.10 - 4.10 | unclear; met; unclear; met |
| C3 C3 - Parallel Linkage with Sealed Bushings | 2.90 - 3.90 | unclear; met; unclear; met |
| C4 C4 - Tuned Mass Damper | 3.00 - 4.00 | met; unclear; met; met |
| C5 C5 - Handle Geometry and Grip | 3.30 - 4.30 | unclear; met; unclear; unclear |
| C6 C6 - Passive Vibration Absorber | 3.35 - 4.20 | unclear; met; unclear; unclear |

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Steel Spring Isolators | 3.75 - 4.33 | unclear; met; unclear; met |
| C2 C2 - Elastomer Isolators | 3.45 - 4.45 | unclear; met; unclear; met |
| C3 C3 - Parallel Linkage with Sealed Bushings | 2.95 - 3.88 | unclear; met; unclear; met |
| C4 C4 - Tuned Mass Damper | 3.00 - 4.00 | met; unclear; met; met |
| C5 C5 - Handle Geometry and Grip | 3.30 - 4.30 | unclear; met; unclear; unclear |
| C6 C6 - Passive Vibration Absorber | 3.82 - 4.42 | unclear; met; unclear; unclear |

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1 - Steel Spring Isolators | 3.75 - 4.33 | unclear; met; unclear; met |
| C2 C2 - Elastomer Isolators | 3.45 - 4.45 | unclear; met; unclear; met |
| C3 C3 - Parallel Linkage with Sealed Bushings | 3.17 - 4.05 | unclear; met; unclear; met |
| C4 C4 - Tuned Mass Damper | 3.15 - 4.10 | met; unclear; met; met |
| C5 C5 - Handle Geometry and Grip | 3.10 - 4.10 | unclear; met; unclear; unclear |
| C6 C6 - Passive Vibration Absorber | 3.65 - 4.42 | unclear; met; unclear; unclear |

## Recommended set (kept open for detailed design)

### C1 C1 - Steel Spring Isolators
- vibration_reduction: 3.5-4.5. Based on the field report and bench tests, the vibration reduction is expected to be 40 to 60 percent, and the steel spring isolators are designed to reduce vibrations by 40 to 60 percent. (`cold_weather_field_report#1`, `steel_spring_isolators#1`)
- mass: 4-4. The added mass of 0.25 kg is within the 0.6 kg limit, with a low risk of exceeding it. (`steel_spring_isolators#1`)
- cost: 3.5-4. The unit cost increase is estimated to be 6 to 8 percent, which is close to the 15 percent limit. (`steel_spring_isolators#1`)
- robustness: 4-4.5. The tool operates well in temperatures down to -30 °C and survives dust and rain, with no exposed moving parts that jam, and the temperature range is expected to cover -15 °C to +40 °C. (`cold_weather_field_report#1`, `steel_spring_isolators#1`)
- development_effort: 4-4.5. This concept requires additional components (dampers, end stops) but does not specify a new drive train or electronics, and other methods like tuned mass absorbers and decoupled handles could also provide significant reduction. (`steel_spring_isolators#1`, `tuned_mass_absorber#0`, `decoupled_handle_linkage#0`)

### C6 C6 - Passive Vibration Absorber
- vibration_reduction: 3-4.5. A tuned mass absorber can reduce vibrations by 50 to 70 percent, which is promising. However, the reduction may fall to 10 to 20 percent away from the tuned frequency. (`tuned_mass_absorber#0`, `tuned_mass_absorber#1`)
- mass: 4-4. The cost increase for the tuned mass absorber is about 5 percent, which is within the limit of 0.6 kg added mass. (`cost_data#0`)
- cost: 4-4. The cost increase for the tuned mass absorber is about 5 percent, which is within the limit of 15 percent. (`cost_data#0`)
- robustness: 4-5. The tool needs to operate in a wide temperature range and survive dust and rain, which the concept does not address directly but is within the design requirements. (`test_method_notes#0`, `cost_data#0`)
- development_effort: 4-4.5. The design brief suggests no change to the drive train if avoidable, and the cost data indicates a moderate cost increase, indicating a moderate development effort. (`cost_data#0`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#1`: Post-mortem: active vibration cancellation handle (stopped project) - Why it was stopped
- `added_mass_postmortem#0`: Post-mortem: added ballast mass in the housing (dropped concept) - What was tried
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

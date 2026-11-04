# Decision log

## Scouting queries

- vibration reduction techniques for hand-held tools#2
- mass optimization methods for reducing vibration#3
- environmental durability tests for outdoor tools#4
- cost analysis of vibration isolation materials for tool handles#5
- handle design considerations for vibration reduction#6

## Concepts

- **C1 C1: Source Balancing** (Reduce excitation): Improve the balancing of the rotating parts in the drive train, which will reduce the vibration by 20-40% and benefit both handles equally.
- **C2 C2: Natural Rubber Mounts** (Passive isolation): Use natural rubber mounts to isolate the vibration from the handle, with a cost increase of 2-4% and minimal impact on the drive train.
- **C3 C3: Silicone Compounds** (Passive isolation): Replace the existing mounts with silicone compounds, which will reduce the vibration by a similar effect to natural rubber with a slightly higher cost increase of 3-5%.
- **C4 C4: Steel Spring Isolators** (Passive isolation): Implement steel spring isolators with guide pins and rubber boots to reduce the vibration, but be aware of the potential for wear due to dust entry.
- **C5 C5: Tuned Mass Absorbers** (Active vibration suppression): Add tuned mass absorbers to the handles, which can reduce the vibration significantly but will increase the unit cost by about 5%.
- **C6 C6: Handle Geometry Optimization** (Improved grip): Enhance the handle's geometry and grip design, which will improve comfort and control but will have only a minor impact on vibration levels (5-10%).

## Round 0

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1: Source Balancing | 3.10 - 4.10 | met; unclear; met; met |
| C2 C2: Natural Rubber Mounts | 2.80 - 4.10 | unclear; met; unclear; unclear |
| C3 C3: Silicone Compounds | 3.65 - 4.65 | met; unclear; met; unclear |
| C4 C4: Steel Spring Isolators | 2.55 - 3.55 | unclear; met; unclear; unclear |
| C5 C5: Tuned Mass Absorbers | 2.75 - 3.75 | unclear; met; unclear; unclear |
| C6 C6: Handle Geometry Optimization | 3.85 - 4.65 | unclear; met; unclear; unclear |

Eliminated:
- C4 C4: Steel Spring Isolators: optimistic score 3.55 is below the pessimistic score 3.85 of C6
- C5 C5: Tuned Mass Absorbers: optimistic score 3.75 is below the pessimistic score 3.85 of C6

## Round 1

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1: Source Balancing | 3.10 - 4.10 | met; unclear; met; met |
| C2 C2: Natural Rubber Mounts | 2.95 - 3.95 | unclear; met; unclear; unclear |
| C3 C3: Silicone Compounds | 3.30 - 4.30 | met; met; met; unclear |
| C6 C6: Handle Geometry Optimization | 3.65 - 4.15 | unclear; met; unclear; unclear |

## Round 2

| Concept | Weighted score range | Must checks |
|---|---|---|
| C1 C1: Source Balancing | 2.55 - 3.72 | met; unclear; met; met |
| C2 C2: Natural Rubber Mounts | 3.55 - 4.23 | unclear; met; unclear; unclear |
| C3 C3: Silicone Compounds | 3.48 - 4.20 | met; met; met; unclear |
| C6 C6: Handle Geometry Optimization | 3.27 - 3.95 | unclear; met; unclear; unclear |

## Recommended set (kept open for detailed design)

### C2 C2: Natural Rubber Mounts
- vibration_reduction: 3.5-4.5. The concept aims for a 30 to 50 percent reduction in vibration, which is in line with the expected range. [elastomer_isolators#0] (no evidence cited)
- mass: 4-4. The added mass of 0.1 kg is below the 0.6 kg limit. [elastomer_isolators#1] (no evidence cited)
- cost: 3.5-4. The unit cost increase is estimated between 2 to 4 percent, which is close to the allowed limit. [cost_data#0] (no evidence cited)
- robustness: 3-4. The isolators are expected to work within the temperature range, but the exact behavior below -10 °C is uncertain. [elastomer_isolators#2] (no evidence cited)
- development_effort: 4-4.5. No change to the drive train is needed, and the design is within the existing handle interface. [elastomer_isolators#1] (no evidence cited)

### C3 C3: Silicone Compounds
- vibration_reduction: 4-4.5. The concept aims to achieve the required vibration reduction, and silicone compounds are expected to perform similarly to steel springs in reducing vibration. (`steel_spring_isolators#1`, `elastomer_isolators#2`)
- mass: 2.5-3. The added mass of 0.25 kg is within the 0.6 kg limit, but the concept may need to consider further optimization. (`steel_spring_isolators#1`)
- cost: 2.5-3.5. The cost increase is expected to be 3-5%, which is within the limit. (`cost_data#0`)
- robustness: 4-5. Silicone compounds are expected to perform well in the temperature range from -15 °C to +40 °C, and the concept does not involve exposed moving parts. (`cold_weather_field_report#1`)
- development_effort: 4-5. Replacing existing mounts with silicone compounds is a relatively small change. The concept avoids changes to the drive train. (no evidence cited)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `cold_weather_field_report#0`: Field report: handle isolators in Nordic winter - Observation
- `cold_weather_field_report#1`: Field report: handle isolators in Nordic winter - Fix
- `cost_data#0`: Indicative cost data for handle vibration solutions - Unit cost increase (approximate)
- `cost_data#1`: Indicative cost data for handle vibration solutions - Tooling
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

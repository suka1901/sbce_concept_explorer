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
| C1 C1: Source Balancing | 2.95 - 4.30 | met; unclear; unclear; unclear |
| C2 C2: Natural Rubber Mounts | 2.90 - 3.90 | unclear; met; violated; violated |
| C3 C3: Silicone Compounds | 3.65 - 4.65 | unclear; violated; met; met |
| C4 C4: Steel Spring Isolators | 2.55 - 3.55 | violated; met; unclear; unclear |
| C5 C5: Tuned Mass Absorbers | 3.10 - 4.10 | met; met; unclear; unclear |
| C6 C6: Handle Geometry Optimization | 3.70 - 4.30 | violated; met; unclear; unclear |

Eliminated:
- C4 C4: Steel Spring Isolators: violates 'Vibration total value at the rear handle at most 4.0 m/s² in the standard test.': 4.5 m/s² vs 4.0 m/s²: 4.5 m/s² is above the 4.0 m/s² limit. (evidence: `test_method_notes#0`, `cold_weather_field_report#0`)
- C2 C2: Natural Rubber Mounts: violates 'Works from -15 °C to +40 °C.': Natural rubber stiffens at about -10 °C, leading to higher vibration. vs Functionality at -15 °C to +40 °C: The natural rubber mounts may stiffen and lose their isolation effect at -15 °C, leading to higher vibration, which is a violation of the requirement. (evidence: `elastomer_isolators#2`, `cold_weather_field_report#0`)
- C6 C6: Handle Geometry Optimization: violates 'Vibration total value at the rear handle at most 4.0 m/s² in the standard test.': Typically 5 to 10 percent reduction, but vibration at the handle changes very little. vs 4.0 m/s²: A 5-10% reduction from 7.5 m/s² is 3.75-6.75 m/s², which is above the 4.0 m/s² limit. (evidence: `handle_geometry#0`, `test_method_notes#0`)
- C3 C3: Silicone Compounds: violates 'Added mass at most 0.6 kg compared with today's tool.': Added 1.2 kg steel ballast, which exceeded the target by a wide margin. vs 0.6 kg: 1.2 kg is significantly above the 0.6 kg limit. (evidence: `added_mass_postmortem#1`, `added_mass_postmortem#0`)

## Recommended set (kept open for detailed design)

### C1 C1: Source Balancing
- vibration_reduction: 2-4. Source balancing can reduce vibration by 20-40%, and a tuned mass absorber can reduce it by 50-70%. Combining both might achieve a reduction in the 40-70% range, but the exact value is uncertain. (`source_balancing#0`, `tuned_mass_absorber#0`)
- mass: 4-5. While the concept requires changes to the drive train, the added mass is within the limit, and the impact on unit cost is low once in production. (`source_balancing#1`)
- cost: 3-4. The cost impact is low once in production, but the engineering effort is high, which could affect the overall cost. (`source_balancing#1`)
- robustness: 4-5. The concept does not specify any changes to the robustness, and the current robustness requirements are met. (`source_balancing#0`)
- development_effort: 2-3. The concept involves changes to the drive train, indicating a moderate development effort. (`source_balancing#1`)

### C5 C5: Tuned Mass Absorbers
- vibration_reduction: 4-5. Tuned mass absorbers can achieve reductions of 50 to 70 percent on a test rig, but the exact reduction in the field is uncertain. (`tuned_mass_absorber#0`, `tuned_mass_absorber#1`)
- mass: 2-3. The added mass of 0.3 to 0.8 kg is significant and will impact the tool's balance and control, but it is below the 0.6 kg limit. (`tuned_mass_absorber#1`)
- cost: 2-3. The cost increase of about 5 percent for tuned mass absorbers is significant but within the allowed limit. (`cost_data#0`)
- robustness: 4-5. No specific robustness issues are mentioned for tuned mass absorbers, and they do not introduce any new moving parts that would affect the IP54 rating. (`tuned_mass_absorber#1`)
- development_effort: 2-3. The post-mortem indicates that active cancellation is complex and not recommended for site tools without significant improvements in power, mass, and sealing. (`active_cancellation_postmortem#2`)

## Evidence used

- `active_cancellation_postmortem#0`: Post-mortem: active vibration cancellation handle (stopped project) - What was tried
- `active_cancellation_postmortem#2`: Post-mortem: active vibration cancellation handle (stopped project) - Lesson
- `added_mass_postmortem#0`: Post-mortem: added ballast mass in the housing (dropped concept) - What was tried
- `added_mass_postmortem#1`: Post-mortem: added ballast mass in the housing (dropped concept) - Result
- `cold_weather_field_report#0`: Field report: handle isolators in Nordic winter - Observation
- `cold_weather_field_report#1`: Field report: handle isolators in Nordic winter - Fix
- `cost_data#0`: Indicative cost data for handle vibration solutions - Unit cost increase (approximate)
- `cost_data#1`: Indicative cost data for handle vibration solutions - Tooling
- `dust_sealing_lessons#0`: Lessons on dust and rain sealing - Moving parts
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

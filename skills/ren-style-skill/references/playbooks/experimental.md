# Playbook: `experimental`

## Functions
- `test_rig` — Architecture of the custom test rig / model switch, actuation mechanism, force/electrical sensors, and DAQ system.
- `specimen` — Contact pair geometry (`ball-shaped rider` vs `flat sample`), substrate/coating materials, surface roughness, and ultrasonic degreasing protocol.
- `procedure` — Four-wire measurement circuit, operating parameter matrix (`Table 1`), environmental control, and post-mortem SEM/EDX/3D profilometry setup.

## Quantitative Targets (S+A Train Weighted)
- **Paragraph length**: **92 words** median (IQR: `53–165` words), **4 sentences** per paragraph (`2–6` paragraphs per Experimental section).
- **Sentence length**: Median **19 words** — shortest in the corpus (IQR: `15–26` words, P90: `34` words; lint range P50 `13–28`, P90 `19–42`).
- **Voice & pronouns**: **71.9%** passive sentences — highest in the corpus (`3.66` passives/100w; lint range `0.40–0.95`); almost zero `we`/`our` (`0.41 / 1,000w`).
- **Tense mix**: **46.1%** Past (`was supplied`, `were degreased`, `was measured`) / **53.9%** Present (`consists of`, `is shown in`, `has a resolution of`). Keep tense consistent within each subsection.
- **Top connectives**: `In general,` (`6.3 / 100 paras`), `Thus,` (`1.28 / 100 sents`), `Then,` (`1.28`), `Therefore,` (`1.15`), `As shown in [FIG n],` (`0.64`).

## Move Order
1. **Move 1 (`test_rig`) — Test Rig Overview & Schematic Pointer (1 paragraph)**
   - Cite prior rig paper if applicable, refer to `[FIG 1]`, and list the main functional modules (`motion structure, measurement unit, and PC software`).
   - *Evidence*: `"The test apparatus used in these experiments is described in detail in [CIT], which contains a brief summary thereof."` (`P01`)
2. **Move 2 (`test_rig`) — Actuation, Sensors & Data Acquisition Specs (1–2 paragraphs)**
   - Detail how motion/force is generated and how contact voltage, current, force, and displacement are sensed and digitized, giving model numbers, ranges, and resolutions in parentheses.
   - *Evidence*: `"During the test, data was acquired using a personal computer with programmed software and a DAQ card (500 kHz)."` (`P01`)
3. **Move 3 (`specimen`) — Contact Pair Geometry, Material & Ultrasonic Cleaning (1 paragraph)**
   - Specify rider diameter/shape, flat coupon dimensions, substrate alloy, electroplated coating thickness, roughness, and the `acetone, alcohol, and distilled water` ultrasonic cleaning sequence.
   - *Evidence*: `"The contacts were a ball-shaped rider, with a diameter of 2 mm, on a flat sample..."` (`P01`)
4. **Move 4 (`procedure`) — Electrical Circuit, Test Conditions & Surface Analysis Tools (1 paragraph)**
   - Reference the four-wire circuit `[FIG n]` and conditions table (`Table 1`), state tested current/frequency/temperature levels, and list post-test characterization instruments (`SEM`, `EDX`, `CSLM`).
   - *Evidence*: `"By using the 4-wires method (shown in [FIG 2]), the contact resistance was continuously measured as a function of fretting cycles..."` (`P01`)

## Sentence Frames (Slot Templates)
1. `The test apparatus used in these experiments is described in detail in [CIT], which contains a brief summary thereof.`
2. `In general, the whole test rig consists of three main modules, including <motion structure>, <measurement unit>, and <control software>, as shown in [FIG n].`
3. `The relative motion between the contacts was provided by an electrodynamic shaker imposing controlled sinusoidal cyclic movements.`
4. `The normal contact force between the two electrodes was assessed using a <sensor type> (Type: <Model>), which has a measurement range of <X> and a resolution of <Y>.`
5. `All above signals including <signal 1>, <signal 2>, and <signal 3> are acquired by a commercial DAQ system (<Model, Maker>), which has a measurement resolution of <N> bits and a sampling frequency of <F> kHz.`
6. `The contacts were a ball-shaped rider, with a diameter of <D> mm, on a flat sample, both made of <copper alloy> and electroplated with <Au> with a thickness of <h> μm.`
7. `Prior to each test, the rider and flat specimens were degreased using acetone, alcohol, and distilled water in an ultrasonic cleaner, dried, and carefully mounted in the test rig.`
8. `The rider and flat contacts are mated in such a way as to create a point contact in "sphere-plane" geometry (shown in [FIG n]).`
9. `By using the four-wire method, the instantaneous value of contact voltage/resistance was continuously measured as a function of <fretting cycles / time> under <load conditions>.`
10. `Scanning electron microscopy (SEM) and energy dispersive X-ray analysis (EDX) were used to characterize the extent of <wear/oxidation> and elemental distribution across the contact zone.`

## Guardrails & Tier-S Precedence
- Always write `"our newly designed test rig"` (never `"our new designed test rig"`, `F18`).
- Never write objectless `"allows to observe"` (`F26`); write `"makes it possible to measure/observe..."` or `"allows in-situ observation of..."`.
- Keep sentences factual, passive, and hardware-grounded; do not insert speculative mechanism claims in `experimental`.

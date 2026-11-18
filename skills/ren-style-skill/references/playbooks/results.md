# Playbook: `results`

## Functions
- `waveform` — Time-domain or cycle-domain transient waveform analysis (contact voltage, current, dynamic force, resistance spikes), partitioned into lettered points (`A–B–C`) or numbered stages.
- `trend` — Parametric dependence of contact resistance, welding force, bounce duration, or normalized spreading resistance on load, frequency, amplitude, temperature, or geometry (`as a function of...`).
- `surface_analysis` — Post-mortem SEM, EDX/EDS elemental mapping, and 3D laser profilometry of worn/eroded/welded contact surfaces.

## Quantitative Targets (S+A Train Weighted)
- **Paragraph length**: **106 words** median (IQR: `68–171` words), **5 sentences** per paragraph.
- **Sentence length**: Median **22 words** (IQR: `16–29` words, P90: `37` words; lint range P50 `14–30`, P90 `21–45`).
- **Voice & pronouns**: **35.9%** passive sentences — lowest in the corpus (lint range `0.15–0.68`), driven by active figure-pointer sentences (`[FIG n] shows...`) + `3.79` `It is noted/shown that` per 100 sentences.
- **Tense mix**: **76.8%** Present — highest in the corpus / **22.9%** Past / **0.3%** Present Perfect.
- **Top connectives**: `However,` (`3.46 / 100 sents`), `As shown/seen in [FIG n],` (`2.13`), `Thus,` (`2.10`), `Therefore,` (`1.66`), `In addition,` (`1.14`), `Meanwhile,` (`0.66`).

## Move Order
1. **Move 1 — Figure-Driven Topic Opening (1 sentence)**
   - Open the paragraph by naming the figure (`[FIG n] shows/illustrates the variation in <Y> as a function of <X>...` or `The typical waveforms of <signals> are shown in [FIG n].`).
   - *Evidence*: `"[FIG 9] shows the results of illustrative calculations of the dependence of R* on..."` (`P22`)
2. **Move 2 — Stage-by-Stage or Parametric Trajectory Description (2–3 sentences)**
   - Walk through the curve quantitatively: divide into stages (`namely low and stable, slight rise, sharp increase, and severe fluctuation`) or trace points (`from point A to point B`), giving exact values, cycle counts, and slopes.
   - *Evidence*: `"When a/r is less than 0.01, R* decreases rapidly with increasing a/r, and then decreases slowly..."` (`P22`)
3. **Move 3 — Cross-Case Comparison (`However,` / `Comparing [FIG a] with [FIG b]`, 1–2 sentences)**
   - Contrast low vs high load/frequency/amplitude or analytical vs FEM/Holm predictions.
   - *Evidence*: `"Comparing [FIG 6] with [FIG 6], it can be seen there is much more damage to the contact..."` (`P03`)
4. **Move 4 — Immediate Physical Interpretation (`This is attributed to...` / `This indicates that...`, 1–2 sentences)**
   - Close the paragraph by linking the observed curve feature or SEM/EDX feature to its physical cause.
   - *Evidence*: `"This is attributed to severe oxidation wear and abrasive wear caused by the temperature rise..."` (`P03`)

## Sentence Frames (Slot Templates)
1. `[FIG n] shows/illustrates the variation in <metric> as a function of <fretting cycles / time / ratio> under different <conditions>.`
2. `As shown in [FIG n], the <contact resistance> behavior can be characterized by <N> distinct stages, namely <stage 1>, <stage 2>, and <stage 3>.`
3. `Within the initial <N> cycles, <metric> remains low and stable around <value>. Subsequently, a sharp rise to <value> occurs after the <M>th cycle.`
4. `With the increase of <parameter> from <X1> to <X2>, <metric> increases/decreases significantly from <Y1> to <Y2>.`
5. `However, in the case of <condition B>, <metric> fluctuates drastically, correlating closely with the variations in <secondary signal> shown in [FIG n].`
6. `Comparing [FIG a] with [FIG b], it can be seen that <comparative observation>.`
7. `It is noted/shown that the analytical results agree well with the FEM simulation results when <a/r ≤ 0.1>, whereas appreciable deviation appears for <a/r > 0.1>.`
8. `This phenomenon is mainly attributed to <physical factor A> and <physical factor B>.`
9. `[FIG n] shows the SEM surface morphology and EDX elemental distribution of the worn contact zone after <N> cycles under <condition>.`
10. `The elemental analysis performed by EDX reveals high concentrations of <Cu> (<X> at%) and <O> (<Y> at%) with a relatively small amount of <Au> (<Z> at%), suggesting that the wear debris is mainly <copper oxide>.`

## Guardrails & Tier-S Precedence
- **Tier S Precedence**: Always write `"As shown in [FIG n],"` or `"As seen in [FIG n],"` with the explicit figure reference; never write bare `"As shown, the..."` (which is a Tier B student habit, $z = -5.22$).
- Never write `"inversely proportion to"` (`F25`) or `"results into"` (`F17`); always write `"inversely proportional to"` and `"results in"`.

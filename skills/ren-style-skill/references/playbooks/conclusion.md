# Playbook: `conclusion`

## Functions
- `numbered` — Brief scope restatement followed by `The main findings are as follows:` and numbered conclusions `(1) ... (2) ... (3) ...` (preferred for experimental fretting/regime papers like `P01`, `P03`, `P14`).
- `summary` — Single cohesive summary paragraph opening with `This investigation/paper mainly aims to...` and `Our results indicate that...` (preferred for modeling/theoretical and IEEE TED/TCPMT papers like `P13`, `P22`).

## Quantitative Targets (S+A Train Weighted)
- **Paragraph length**: **107 words** median (IQR: `54–152` words; `120–220` words total across the Conclusion section).
- **Sentence length**: Median **23 words** (IQR: `16–30` words, P90: `39` words; lint range P50 `15–31`, P90 `21–45`).
- **Voice & pronouns**: **38.9%** passive sentences (lint range `0.15–0.72`); **highest possessive `our` rate in the corpus (`1.56 / 1,000w`)**: `"Our results indicate that..."`, `"our newly designed test rig"`.
- **Tense mix**: **69.5%** Present / **28.9%** Past / **1.5%** Present Perfect.
- **Top connectives**: `Meanwhile,` (**3.36 / 100 sents**), `Therefore,` (**3.36**), `Similarly,` (`2.24`), `Finally,` (`1.68`), `However,` (`1.12`), `Furthermore,` (`1.12`).

## Move Order
1. **Move 1 — Restatement of Aim, System & Method (1–2 sentences)**
   - Open with `"This investigation/paper mainly aims to (systematically) determine/investigate..."` or `"The <behavior> of <contacts> is investigated at various <loads/speeds> by using our newly designed test rig."`
   - *Evidence*: `"This investigation mainly aims to determine the electrical contact resistance of a circular constriction in a spherical contact..."` (`P13`)
2. **Move 2 — Core Quantitative & Regime Findings (`summary` or `numbered`, 3–5 sentences)**
   - *In `summary` mode*: Start sentence 2 with `"Our results indicate that..."`, add parallel findings with `"Meanwhile,..."` and `"Furthermore,..."`, and state quantitative validity thresholds (`wherever a/h > 1`, `for a/r ≤ 0.1`).
   - *In `numbered` mode*: End Move 1 with `"The main findings are as follows."` and present `(1) ... (2) ... (3) ...` covering regimes, parameter transitions (`Increasing <A> with fixed <B> results in... Similarly, increasing <B> causes...`), and mechanism.
   - *Evidence*: `"Our results indicate that the total contact resistance and the comprised spreading resistance... deviate appreciably..."` (`P13`)
3. **Move 3 — Fundamental Physical Attribution & Engineering Implication (1–2 sentences)**
   - Identify the root physical cause (`is not only the root reason for..., but also causes...` / `This difference is attributed to...`) and optionally state the design implication for relays/connectors/MEMS.
   - *Evidence*: `"The difference of electrical conductivity between substrate and coating is not only the root reason for the occurrence of resistance in transition zone, but causes..."` (`P13`)

## Sentence Frames (Slot Templates)
1. `This investigation/paper mainly aims to (systematically) determine/investigate the <property/behavior> of <contact system> under <operating conditions>.`
2. `The <fretting / switching / welding> behavior of <material> contacts is investigated at various <parameters>, namely <list>, with the use of our newly designed test rig.`
3. `Our results indicate that <primary finding> wherever <dimensionless threshold, e.g., a/h > 1>.`
4. `Meanwhile, <secondary metric> is significantly affected by <parameter>, which is attributed to <physical/geometric feature>.`
5. `The relationship between normalized <metric Y> and normalized <parameter X> conforms to <formula> well for <range>.`
6. `The main findings are as follows. (1) <Regime/Finding 1>. (2) <Parametric transition 2>. (3) <Mechanism 3>.`
7. `Increasing <parameter A> with fixed <parameter B> results in the transition from <Regime I> to <Regime II>. Similarly, increasing <parameter B> with fixed <parameter A> causes the identical transition.`
8. `Furthermore, the <conductive ability / welding strength> of <contacts> is determined by <factor A> and <factor B> comprehensively.`
9. `The <physical property mismatch> is not only the root reason for the occurrence of <phenomenon A>, but also causes <phenomenon B> to deviate from the classical Holm theory.`
10. `This is a positive and beneficial conclusion in engineering applications for electrical contacts, especially for the determination of contact structure in the design process.`

## Guardrails & Tier-S Precedence
- Never open a conclusion with AI clichés like `"In conclusion, this study has comprehensively elucidated..."` or `"To sum up, our work paves the way for..."`.
- In `balanced` mode, avoid ending with `"will be in schedule"` (`F35`); if mentioning future work, write `"In future work, <topic> will be investigated for comparison."`

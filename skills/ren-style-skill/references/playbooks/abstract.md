# Playbook: `abstract`

## Functions
- `full` — Complete single-paragraph abstract (5–7 sentences, 95–145 words).

## Quantitative Targets (S+A Train Weighted)
- **Paragraph length**: 1 paragraph, **115 words** median (IQR: `96–143` words), **5–6 sentences**.
- **Sentence length**: Median **21 words** (IQR: `17–24` words, P90: `29` words; lint range P50 `14–27`, P90 `20–38`).
- **Voice & pronouns**: **69.0%** passive sentences (lint range `0.35–0.90`); avoid `we` (`0.20 / 1,000w`); use `our` only in `"our newly designed test rig"`.
- **Tense mix**: **67.4%** Present / **29.5%** Past / **3.1%** Present Perfect.
- **Top connectives**: `Subsequently,` (`4.18 / 100 sents`), `Furthermore,` (`2.51`), `Finally,` (`2.51`), `In this paper,` (`2.51`), `Moreover,` (`1.67`).

## Move Order
1. **Move 1 — Engineering Context & Reliability Need (0–1 sentence)**
   - State where the contact/component is used and why reliability or failure is a key concern.
   - *Evidence*: `"Electrical contacts, which are used in aerospace engineering with high reliability requirements, are usually plated..."` (`P01`)
2. **Move 2 — Study Object & Method Statement (1 sentence)**
   - Introduce what is investigated and by what method (passive `"The <property> of <contact> is studied by..."` or `"In this paper, ... is investigated by introducing our newly designed test rig"`).
   - *Evidence*: `"The electrical contact resistance of cambered surface contact is systematically studied by analytical solution and finite-element simulation."` (`P22`)
3. **Move 3 — Model/Experimental Decomposition & Parameter Scope (1–2 sentences)**
   - Specify the configurations built (`namely <A> and <B>`), waveforms recorded (`explicitly`), or parameters evaluated (`over a large range of...`).
   - *Evidence*: `"Two representative cambered surface contacts, namely sphere-plane contact and cylinder-plane contact are built and... compared explicitly."` (`P22`)
4. **Move 4 — Core Finding & Physical Mechanism Attribution (2–3 sentences)**
   - Advance with `Subsequently,` or `Furthermore,`; report how the target metric responds to parameters and explain the underlying mechanism (`with reference to...`, `is attributed to...`, `It is shown/demonstrated that...`).
   - *Evidence*: `"Subsequently, the correlations of normalized spreading resistance, total contact resistance, and normalized contact radius are calculated..."` (`P13`)

## Sentence Frames (Slot Templates)
1. `<Components>, which are used in <engineering field> with high reliability requirements, are usually <surface-treated> in order to <purpose>.`
2. `<Contact materials> are widely used in <application> to meet the requirements of high quality and high reliability for <industry>.`
3. `The <electrical contact resistance / behavior> of <contact configuration> is (systematically) studied by using <analytical method> and <finite-element simulation>.`
4. `In this paper, the <phenomena> of <material> under <conditions> are investigated by introducing our newly designed test rig.`
5. `Two representative <configurations>, namely <type A> and <type B>, are built and the distributions of <field/waveform> are compared/recorded explicitly.`
6. `The effects of <param 1>, <param 2>, and <param 3> on <target metric> are evaluated over a large range of <aspect ratios / frequencies>.`
7. `The total <quantity> could comprise <N> components, that is, <component 1>, <component 2>, and <component 3>.`
8. `Subsequently, the correlations of <metric A> and <metric B> are calculated and compared with the classical Holm theory.`
9. `The results show that <target variable> is significantly influenced by <factor A>, as well as <factor B>.`
10. `It is shown/demonstrated that <key physical finding>, which is attributed to <physical mechanism>.`

## Guardrails & Tier-S Precedence
- **Never** write `"In this paper/study, we investigate/delve into..."` (AI baseline anti-pattern $z = -5.15$). Always use passive `"is studied / are investigated"` or `"This paper investigates..."`.
- **Never** use `"across a broad spectrum"` or `"across the interface"`; use `"over a large range of"` and `"within the fretted/contact zone"`.
- Place `explicitly` at most **once** in the abstract, always after the verb (`are recorded/compared/analyzed explicitly`).

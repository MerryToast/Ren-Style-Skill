# Playbook: `mechanism`

## Functions
- `explanation` — Physical and mathematical explanation of contact degradation, fretting wear/corrosion transition, thermoelastic instability (TEI), molten bridge rupture, or bounce-arc welding.

## Quantitative Targets (S+A Train Weighted)
- **Paragraph length**: **101 words** median (IQR: `62–147` words), **4 sentences** per paragraph.
- **Sentence length**: Median **21 words** (IQR: `17–30` words, P90: **51 words** — longest multi-clause causal sentences in the corpus; lint range P50 `15–32`, P90 `22–55`).
- **Voice & pronouns**: **47.2%** passive sentences (lint range `0.20–0.78`); **highest rate of `It is <VBN/ADJ> that` in the corpus (`5.19 / 100 sents`)** and **highest modal verb rate (`23.4 / 100 sents`: `could`, `would`, `may`, `will`)**.
- **Tense mix**: **69.9%** Present / **27.7%** Past / **2.4%** Present Perfect.
- **Top connectives**: `However,` (**6.06 / 100 sents** — highest in corpus), `Therefore,` (**4.76** — highest in corpus), `Thus,` (`2.38`), `In addition,` (`1.95`), `As shown in [FIG n],` (`1.95`), `Meanwhile,` (`1.73`), `Moreover,` (`1.30`).

## Move Order
1. **Move 1 — Coupled Process Framing or Existing Model Limitation (1 paragraph)**
   - Identify the competing or coupled physical processes (`conduction and friction`, `making bounce arc and breaking molten bridge`) or point out why a single-factor model is insufficient (`However, the two models mentioned above cannot explain...`).
   - *Evidence*: `"There are two coupled physical processes during the whole fretting wear of contacts, namely conduction and friction..."` (`P01`)
2. **Move 2 — Theoretical Equation Grounding & Stepwise Causal Chain (1–3 paragraphs)**
   - Anchor the mechanism in classical contact physics (Holm constriction + film resistance $R_c = R_s + R_f$ `[EQ]`, Kohlrausch softening/melting voltage, frictional heat input $q = \mu v P$ `[EQ]`), then trace the physical chain: **mechanical wear / current constriction → localized Joule/frictional heating → softening/melting/oxidation → conductive area evolution**.
   - *Evidence*: `"According to the classical electrical contact theory [CIT], contact resistance is composed of constriction resistance and film resistance, that is [EQ]."` (`P05`)
3. **Move 3 — Multi-Factor Synthesis & Regime Attribution (1 paragraph)**
   - Synthesize the governing factors using an inline numbered list `(1) ...; (2) ...; (3) ...` and deduce the macroscopic failure outcome (`Therefore, these factors account for...`).
   - *Evidence*: `"Three factors influencing the contact area and real conductive area during the dynamic process could be summarized as: (1)..."` (`P03`)

## Sentence Frames (Slot Templates)
1. `There are two coupled physical processes during the whole <degradation process> of contacts, namely <process A> and <process B> between two contacting surfaces.`
2. `According to the classical electrical contact theory [CIT], the contact resistance is composed of constriction resistance and film resistance, that is, [EQ].`
3. `For samples with intact gold coating, Rc is determined directly by <constriction term>. After the gold coating is worn out and detached from the substrate, oxidation of the copper alloy occurs and film resistance becomes the main component.`
4. `As a result of the decrease in conductive area, the current density increases significantly, which generates localized Joule heat to melt the contacting asperities.`
5. `When the contact voltage reaches the softening/melting voltage of <material> (<U> mV, corresponding to <T> °C), localized thermal softening/melting occurs within the contact zone.`
6. `This process is accompanied by <intermediate effect>, which in turn aggravates <secondary effect>, followed by <final state>.`
7. `However, the micro conduction patches and whole conduction area increase explicitly with the raised current load, which delays the deterioration process of contact resistance.`
8. `Three factors influencing the real conductive area during the dynamic process can be summarized as: (1) the increment of contact area induced by mechanical wear, which is relevant to the hardness of materials; (2) the reduction of conductive area caused by oxide debris accumulation; and (3) the decrement of contact area induced by thermoelastic instability.`
9. `It is demonstrated/determined that <factor A> plays a crucial/dominant role in the formation of <weld nugget / high contact resistance>.`
10. `Therefore, these combined factors account for the higher <metric> and accelerated failure under <condition>.`

## Guardrails & Tier-S Precedence
- Ground every mechanism explanation in **quantitative physical thresholds** (e.g., softening/melting temperature or voltage, critical sliding velocity, constriction radius ratio $a/h$, oxide resistivity $\sigma_f$) as practiced in Tier S (`P01`, `P03`, `P13`).
- Never write `"are resulted from"` (`F16`) or `"relevant with"` (`F22`) or `"harness"` (`F29`); always write `"result from"` / `"are caused by"`, `"relevant to"`, and `"hardness"`.

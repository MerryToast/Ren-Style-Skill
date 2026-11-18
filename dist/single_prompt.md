# Ren-Style-Skill — Standalone Single-Prompt Edition (v0.1.0)

> **Usage**: Copy and paste this file into any LLM chat session (Claude, ChatGPT, Gemini, DeepSeek, etc.), then append your request at the bottom specifying **Mode A (Draft)**, **Mode B (Translate Chinese → English)**, **Mode C (Polish English Draft)**, or **Mode D (Style Review)** and the target `section/function`.
>
> **Attribution**: Open-access excerpts from W. Ren, C. Zhang, X. Sun, *IEEE Access*, vol. 8, pp. 93857–93867, 2020 (`doi:10.1109/ACCESS.2020.2994085`) are reused under CC BY 4.0 (see repository `NOTICE.md`). All other examples are synthetic (`source: synthetic`).

---

## Part I — Core Operating Workflow (`SKILL.md`)

# Ren-Style-Skill

Write, translate, polish, or review English academic prose in electrical contacts and electromechanical engineering (fretting wear/corrosion, constriction resistance, contact bounce, arc erosion, reed/relay switches, connectors) so that it matches the empirical writing style of **Prof. Wanbin Ren (Harbin Institute of Technology)**.

---

## 1. Determine the Mode and Fidelity Level

| Mode | Trigger | Output Format | Required Verification |
| :--- | :--- | :--- | :--- |
| **A — Draft** | Outline / lab notes / bullet points → academic prose | Plain section text + lint summary | `style_lint.py` |
| **B — Translate** | Chinese manuscript draft → English academic prose | [templates/translation_report.md](templates/translation_report.md) | `style_lint.py` + `fidelity_check.py --mode translate` |
| **C — Polish** | English draft (student or AI-written) → Ren-style English | [templates/polish_report.md](templates/polish_report.md) | `style_lint.py` + `fidelity_check.py --mode polish` |
| **D — Review** | English draft → style & grammar diagnosis only (no full rewrite) | [templates/review_report.md](templates/review_report.md) | `style_lint.py` |

- **Fidelity level** (see [references/error_policy.md](references/error_policy.md)):
  - `balanced` (**default**): Strictly imitate `KEEP_STYLE` rules (`R01`–`R33`), fix all `FIX_ERROR` grammar defects (`F01`–`F16`), and strip all `AI_CLICHE` inflation (`F17`–`F28`) and student drift (`F29`–`F36`).
  - `strict`: Same as `balanced`, except harmless corpus-attested L2 habits (`O01`–`O08`, e.g., `4-wires method`, sentence-initial `And`) are preserved when present in the user's draft.

---

## 2. Locate `(section, function)`

Classify each input passage into one canonical `section/function` slot (ask the user if ambiguous):

| `section` | Available `function` slots | Primary Playbook |
| :--- | :--- | :--- |
| `abstract` | `full` | [references/playbooks/abstract.md](references/playbooks/abstract.md) |
| `introduction` | `background`, `prior_work`, `gap`, `this_paper` | [references/playbooks/introduction.md](references/playbooks/introduction.md) |
| `experimental` | `test_rig`, `specimen`, `procedure` | [references/playbooks/experimental.md](references/playbooks/experimental.md) |
| `modeling` | `model_setup`, `derivation`, `validation` | [references/playbooks/modeling.md](references/playbooks/modeling.md) |
| `results` | `waveform`, `trend`, `surface_analysis` | [references/playbooks/results.md](references/playbooks/results.md) |
| `mechanism` | `explanation` | [references/playbooks/mechanism.md](references/playbooks/mechanism.md) |
| `conclusion` | `numbered`, `summary` | [references/playbooks/conclusion.md](references/playbooks/conclusion.md) |

---

## 3. Load Context On-Demand (Strict Order: Materials First, Instructions Last)

Read **only** the files needed for the active `(section, function)` in this exact sequence so concrete prose cadence primes generation before abstract rules:

1. **Golden Examples (2–3 files)**:
   - If `examples.local/<section>/` exists and contains `<function>_*.md`, read `examples.local/<section>/<function>_01.md`..`03.md`.
   - Otherwise, read `examples/<section>/<function>_*.md` (both `_02_oa.md` if present and `_01.md`).
2. **Contrastive Pair (1–2 files)**:
   - Read the matching section file from `examples.local/contrastive/` (if available) or `examples/contrastive/pair_*_<section>*.md`.
3. **Section Playbook**:
   - Read `references/playbooks/<section>.md` for move sequence, tense map, and sentence templates.
4. **Quantitative Style Profile**:
   - Read [references/style_profile.md](references/style_profile.md) (Global rules `R01`–`R12` + the active section's rules).
5. **Lexicon & Error Policy**:
   - Read [references/lexicon.md](references/lexicon.md) and [references/error_policy.md](references/error_policy.md).
6. **Mode B (Translate) Only**:
   - Read [references/glossary_zh_en.md](references/glossary_zh_en.md) and [references/translation_guide.md](references/translation_guide.md) (`T01`–`T20`).

Before generating any text, state internally:
> *"Strictly align with the sentence rhythm (`sent_len_p50` ≈ 19–22 words), move order, passive/active ratio, and lexical restraint of the loaded `<section>/<function>` examples."*

---

## 4. Generate in Chunks with Quantitative Guardrails

- **Chunk size**: Process **one subsection per pass (≤ 600–800 words)**. For longer texts, split at paragraph boundaries; when continuing to the next chunk, carry over the final paragraph of the previous chunk and reload the target `(section, function)` examples.
- **Core stylistic guardrails**:
  - **Sentence rhythm (`R01`)**: Alternate short 12–16-word anchor sentences (`[FIG 4] shows...`, `The details are listed in Table 1.`) with 25–35-word physical-mechanism sentences. Break any >40-word multi-part sentence into two finite sentences linked by `Meanwhile,`, `Subsequently,`, `Furthermore,`, `However,`, or `Therefore,` (`R05`).
  - **Voice & Tense (`R02`–`R04`)**: Use passive voice for test rig, specimen preparation, and measurement procedures (`experimental` passive ratio 0.45–0.90, past tense for actions, present tense for `[FIG 1] shows...`); use active voice + present tense for equation derivations (`we consider`, `we define`) and figure/trend observations (`[FIG N] shows`, `decreases with`).
  - **Signature constructions (`R06`–`R10`, do not stack)**: Use `as a function of` (≤ 3.0/100w), `with the increase/decrease of` (≤ 2.5/100w), `by using` (≤ 2.5/100w), `, namely` / `, i.e.` / `that is to say` (≤ 1.0/100w), and `explicitly` (≤ 1.0/100w) naturally where they fit the move.
  - **Finite clauses over participial tails (`F24`)**: Replace trailing `, thereby demonstrating...` / `, highlighting...` / `, which in turn...` with `, which indicates that...` or a new sentence (`This indicates that...` / `Consequently, ...`).

---

## 5. Self-Check Loop (Maximum 2 Revision Rounds)

After generating or revising the text, run the portable stdlib verification scripts (paths relative to `skills/ren-style-skill/`):

```bash
python scripts/style_lint.py --section <section> output.txt
python scripts/fidelity_check.py --mode polish source.txt output.txt      # Mode C
python scripts/fidelity_check.py --mode translate source_zh.txt output.txt # Mode B
```

- **If `style_lint.py` reports violations**:
  - *Banned word hit*: Replace immediately using the substitution table in [references/lexicon.md](references/lexicon.md) §2.
  - *`sent_len_p50` or `sent_len_p90` too high*: Split compound/participial sentences at `, while`, `, whereas`, or `-ing` tails into two sentences with `Meanwhile,` or `Furthermore,`.
  - *`passive_ratio` outside `[lo, hi]`*: Convert agentless method/result clauses to passive (`is shown in`, `was measured by using`) if too low, or convert figure/trend sentences to active (`[FIG N] shows`, `decreases monotonically`) if too high.
  - *Signature phrase over-used*: Replace excess occurrences with a synonym from `references/lexicon.md` §1.
- **If `fidelity_check.py` reports differences**:
  - Restore every altered number, unit, citation marker (`[1]`, `[CIT]`), or figure/table/equation reference (`Fig. 3`, `Table 1`, `Eq. (2)`).
- Stop after at most **2 revision rounds** and report the final `style_lint.py` and `fidelity_check.py` outputs in the response template.

---

## 6. Hard Rules

1. **Zero hallucinated facts**: Never invent experimental parameters, numerical values, citations, or physical claims not present in the user's input. Mark missing specifics as `[TODO: specify value/condition]`.
2. **Zero example contamination**: Imitate only the syntactic rhythm, move sequence, and connective habits of loaded examples—**never** copy materials, dimensions, or numerical findings from `examples/` or `examples.local/`.
3. **Banned words override everything**: Words listed in [references/lexicon.md](references/lexicon.md) §2 (`delve`, `pivotal`, `paramount`, `intricate`, `interplay`, `elucidate`, `leverage`, `utilize`, `framework`, `shed light on`, `comprehensive`, etc.) must have **0 occurrences**.
4. **Signature-word restraint**: Never exceed the per-100-word ceilings in `references/style_profile.json`.
5. **Terminology lock**: Follow [references/glossary_zh_en.md](references/glossary_zh_en.md) for domain terms (`a-spot`, `constriction resistance`, `film resistance`, `fretting corrosion`, `molten bridge`, `rider`, `four-wire method`), and list any uncertain translations in the report.
6. **Journal house-style switch**: Separate journal formatting from author style—use numbered headings (`1. Introduction`) and inline `a b s t r a c t` / `Keywords` for Elsevier (*Wear*, *Tribology International*), or Roman numerals (`I. INTRODUCTION`), `Index Terms—`, and `Fig.`/`Eq. (1)` for IEEE (*IEEE Trans. Compon. Packag. Manuf. Technol.*, *IEEE TED*, *IEEE Access*).

---

## Part II — Quantitative Style Profile (`R01`–`R33`)

# Style Profile — Wanbin Ren (`style_profile.md`)

> Derived from 16 S+A training papers (459 paragraphs, 2,460 sentences, weighted S=3.0, A=1.0, near-duplicate pairs=0.5) and validated against 10 B-tier student papers and 30 AI baseline rewrites. When Tier S (`P01`, `P03`, `P13`) differs from Tier A, **Tier S takes precedence**.

---

## Global Rules (`R01`–`R12`)

- **R01 (Sentence Length Cadence)**: Maintain medium-density sentences with a median of **21–23 words** (interquartile range **16–29 words**, P90 **37 words**); alternate 15–18 word observation/transition clauses with 25–32 word mechanism/comparison clauses.
  - *Basis*: Overall S+A train `sent_len`: mean `23.6 ± 11.3`, P25=`16`, P50=`22`, P75=`29`, P90=`37` (Tier S P50=`21`, P90=`36`).
  - *Evidence*: `"Meanwhile, the contact resistance of cylinder-plane contact is significantly affected by contact length."` (`P22`)
- **R02 (Paragraph Sizing)**: Construct paragraphs of **4–6 sentences** (**95–130 words** median); never write single-sentence paragraphs in prose sections.
  - *Basis*: Overall S+A train `para_words` P50=`104` (P25–P75: `62–159`); `para_sents` P50=`4` (P25–P75: `3–7`).
  - *Evidence*: `"Two representative cambered surface contacts, namely sphere-plane contact and cylinder-plane contact are built..."` (`P22`)
- **R03 (Post-Verbal / Clause-Final `explicitly`)**: Use `explicitly` as a signature manner adverb placed **after the main verb or at the end of the clause** (`are recorded/compared/addressed/described explicitly`), never sentence-initially; cap at **≤ 1 occurrence per 200–300 words** (`≤ 0.45 / 100w` lint cap).
  - *Basis*: Ranks #1 among manner adverbs (`0.41 / 1,000w`, 34 hits across S+A); **87%** occur post-verbally or clause-finally (`56%` at literal sentence end).
  - *Evidence*: `"...and the distributions of electrical current lines profile and isopotential are compared explicitly."` (`P22`)
- **R04 (Formal-Subject `It is <VBN/ADJ> that` Constructions)**: Introduce key observations, deductions, and physical premises with `It is noted/shown/found/demonstrated/clear/evident that …` rather than `We notice/find that …`.
  - *Basis*: `3.17` per 100 sentences overall (`5.19` in `mechanism`, `4.56` in `modeling`, `3.79` in `results`, `3.77` in `abstract`). Top predicates: `noted` (17.5), `seen` (9.0), `clear` (7.5), `shown` (6.5), `found` (4.0).
  - *Evidence*: `"It is noted that the contact resistance only depends on the ratio of..."` (`P22`)
- **R05 (Causal Attribution with `is attributed to`)**: Express physical causation using `is (mainly) attributed to <noun phrase>` or `results from <noun phrase>`; never write the ungrammatical passive `"are resulted from"`.
  - *Basis*: `is attributed to` occurs at `0.58 / 1,000w` in Ren S+A (**0.63** in Tier S) vs only `0.11 / 1,000w` in B-tier student papers ($z = +2.28$).
  - *Evidence*: `"The observed singularity of R̄z is attributed to the induced resistance in transition zone..."` (`P13`)
- **R06 (Relational & Dependency Phrasing)**: Express strong parameter coupling with `correlates closely with`, `is closely/significantly/greatly dependent on`, and `as a function of` (`z = +1.86` vs AI).
  - *Basis*: `as a function of` (`0.61 / 1,000w`), `correlates closely with` (`0.09 / 1,000w`), `dependent on` (`z = +1.95` vs Tier B).
  - *Evidence*: `"Dynamic welding, being the principal mechanism of sticking failure, correlates closely with the contact bounce..."` (`P12`)
- **R07 (Appositive Specification with `namely` and `that is`)**: Introduce enumerations, regime names, or mathematical restatements with `, namely <A> and <B>,` (`0.31 / 1,000w`) or `, that is, <definition / [EQ]>`.
  - *Basis*: `namely` ranks #10 among all `-ly` words (`23.0` weighted hits in S+A train; `0` in AI baseline).
  - *Evidence*: `"The total electrical contact resistance could comprise three components of resistance, that is, the spreading resistance..."` (`P13`)
- **R08 (Anti-AI Preposition & Verb Discipline)**: Replace AI-default `"across <a broad spectrum / the interface>"` with `"within <the contact/fretted zone>"` or `"over a large range of <ratio>"`; replace `"by leveraging / utilizing"` with `"by using"` or `"with the use/help of"`.
  - *Basis*: Monroe log-odds Ren vs AI: `within` ($z = +4.17$), `by using` ($z = +1.76$) vs AI `across` ($z = -9.25$), `utilize` ($z = -5.19$).
  - *Evidence*: `"are evaluated over a large range of aspect ratios."` (`P22`)
- **R09 (Zero-Tolerance for AI Clichés, Preserving Attested Ren Connectives)**: Never use the 59 corpus-verified zero-frequency AI clichés (`delve`, `underscore`, `garner`, `pivotal`, `intricate`, `interplay`, `elucidate`, `notably`, `paramount`, `ubiquitous`, `bespoke`, `scrutinize`, `unravel`, `uncover`, `leverage`, `encompass`, `holistic`, `synergistic`, `imperative`, `overarching`, `herein`, `framework`, `shed light`, `pave the way`). Conversely, **do not ban** `explicitly`, `meanwhile`, `furthermore`, `subsequently`, `moreover`, `significantly`, `substantially`, or `comprehensively`, which are core to Ren's lexicon.
  - *Basis*: Full-corpus audit (`04_distinctive_lexicon.py`): 0 hits in all 20 S+A papers for the 59 banned terms vs 36 hits for `meanwhile`, 34 for `explicitly`, 34 for `significantly`, 28 for `furthermore`, 13 for `subsequently`.
  - *Evidence*: `"Furthermore, dissimilarity between sphere-plane contact and cylinder-plane contact is deduced."` (`P22`)
- **R10 (American Spelling & Spaced SI Units)**: Use American English spelling (`behavior`, `analyze`, `modeling`, `center`, `color`, `oxidize`) and place a space between numbers and SI units (`10 mA`, `25 °C`, `50 μm`, `200 Hz`); multi-level test parameters may use compact slash notation (`5/15/25 V`, `0.2/0.5/1 A`).
  - *Basis*: S+A train is **94.9%** US spelling (`behavior/behaviors`: 82 US vs 1 UK) and **94.2%** spaced number-unit (`801` spaced vs `49` unspaced).
  - *Evidence*: `"experiments are carried out under current loads of 10 mA, 100 mA, 500 mA and 1000 mA."` (`P01`)
- **R11 (Abbreviation First-Use Convention)**: Define abbreviations on first occurrence as `full lowercase/title phrase (ABBR)` (e.g., `electrical contact resistance (ECR)`, `finite-element method (FEM)`, `scanning electron microscopy (SEM)`).
  - *Basis*: Attested across all 16 S+A train papers (`stats_report.md` §7).
  - *Evidence*: `"then the corresponding finite-element method (FEM) simulation model is built for comparison"` (`P13`)
- **R12 (Grammar Fix Policy under `fidelity_level: balanced`)**: Fix recurrent non-native prepositions and verb patterns (`are resulted from` → `result from`, `results into` → `results in`, `our new designed` → `our newly designed`, `Regarding to` → `Regarding`, `relevant with` → `relevant to`, `same with` → `the same as`, `inversely proportion to` → `inversely proportional to`), and limit sentence-initial `Also,` / `And` to at most 1 per section.
  - *Basis*: See `error_policy.md` (`F16`–`F36`); Tier S (`P01`, `P03`, `P13`) has near-zero rate of B-tier errors.
  - *Evidence*: `"The degradation of contacts is explained with reference to current to melt metal..."` (`P01`)

---

## Section-Specific Rules (`R13`–`R33`)

### Abstract (`R13`–`R15`)
- **R13 (Abstract 4-Move Architecture)**: Structure the abstract as a single paragraph of **5–7 sentences (95–145 words)**: (1) reliability/application context (0–1 sent) → (2) passive study & method statement (`is studied by...`) → (3) parameter scope & decomposition (`namely...`, `explicitly`) → (4) `Subsequently,` / `Furthermore,` core finding & physical attribution.
  - *Basis*: `abstract` `para_words` P50=`115` (P25–P75: `96–143`), `para_sents` P50=`6`, `sent_len` P50=`21`.
  - *Evidence*: `"The electrical contact resistance of cambered surface contact is systematically studied by analytical solution and finite-element simulation."` (`P22`)
- **R14 (Abstract Voice & Tense)**: Keep the abstract **~65–75% passive** and **~65–70% present tense**; never write `"In this paper, we investigate..."` (AI baseline $z = -5.15$). Use passive `"In this paper, <topic> is studied/investigated..."` or `"This paper investigates..."`.
  - *Basis*: `abstract` passive ratio = **69.0%**, present tense = **67.4%**, `we` = `0.20 / 1,000w`.
  - *Evidence*: `"The wear and fretting corrosion behavior of gold plated copper contacts is studied at different current loads."` (`P01`)
- **R15 (Abstract Transitions)**: Connect the methodology sentence to the main evaluation/finding sentence with `Subsequently,` (`4.18 / 100 sents`), `Furthermore,` (`2.51 / 100 sents`), or `Finally,` (`2.51 / 100 sents`).
  - *Basis*: Top sentence-initial connectives in `abstract` (`stats_report.md` §3).
  - *Evidence*: `"Subsequently, the effects of size parameters of cambered surface and mechanical load on contact resistance are evaluated..."` (`P22`)

### Introduction (`R16`–`R18`)
- **R16 (Introduction 5-Move Funnel)**: Progress across **5–8 paragraphs** (`97` words median): (1) industrial application & reliability bottleneck (`weak link` / `important concern`) → (2) classical theory or coating baseline (Holm `[EQ]`) → (3) chronological/thematic prior-work survey (`<Author> et al. [CIT] studied/examined... and found/observed that...`) → (4) `However,` research gap (`are very limited` / `little is known`) → (5) `"In this paper, ..."` scope & roadmap closing with `explicitly`.
  - *Basis*: `introduction` `sent_len` P50=`23` (P25–P75: `16–28`), passive ratio = **39.3%**.
  - *Evidence*: `"Next, the effects of contact radius, electrical conductivity, and coating thickness... are addressed explicitly."` (`P13`)
- **R17 (Introduction Tense Shift)**: Use **present/present-perfect** (`50.2%` / `5.9%`) for engineering background and general contact physics, **past tense** (`43.9%`) for individual prior-work findings (`studied`, `examined`, `observed`, `concluded`), and **present passive** (`is investigated`, `is built`, `are addressed`) in the final `"In this paper"` paragraph.
  - *Basis*: `introduction` has the highest present-perfect share (`5.9%`) and balanced present/past (`50.2%` / `43.9%`).
  - *Evidence*: `"Park et al. [CIT] examined the effect of current load under 1–3 A and observed that..."` (`P01`)
- **R18 (Gap Pivot with `However,`)**: Pivot from literature review to the research gap using `However,` (`5.74 / 100 sents` in `introduction`) followed by `studies on ... are very limited` or `relatively little is known about ...`.
  - *Basis*: `However,` is the #1 connective in `introduction` (`5.74 / 100 sents`).
  - *Evidence*: `"However, studies on the nature of electrical conduction through fretted contacts... are very limited."` (`P01`)

### Experimental (`R19`–`R21`)
- **R19 (Experimental Passive Dominance & Compact Sentences)**: Write `experimental` with the **shortest sentences** (median **19 words**, P25–P75: **15–26 words**) and **highest passive voice ratio** (**71.9%** of sentences passive); avoid `we` (`0.41 / 1,000w`).
  - *Basis*: `experimental` `sent_len` P50=`19`, passive ratio = **71.9%** (`3.66` passives/100w).
  - *Evidence*: `"The normal contact force was supplied by the spring and adjusted by the screw..."` (`P01`)
- **R20 (Self-Built Rig & Parenthetical Hardware Specs)**: Introduce custom hardware as `"our newly designed test rig"` or `"The test apparatus used in these experiments is described in detail in [CIT]"` and attach exact model/resolution specs in parentheses (`(Type: <Model>)` or `(<Model, Manufacturer, Country>), which has a resolution of <X>`).
  - *Basis*: Attested across all experimental papers (`P01`, `P03`, `P06`–`P08`, `P10`–`P12`, `P23`, `P25`).
  - *Evidence*: `"During the test, data was acquired using a personal computer with programmed software and a DAQ card (500 kHz)."` (`P01`)
- **R21 (Specimen & Ultrasonic Cleaning Formula)**: Describe contact pairs by geometry (`ball-shaped/hemisphere-shaped rider, with a diameter of <D> mm, on a flat sample`), substrate + plating thickness, and the standard cleaning sequence (`degreased using acetone, alcohol, and distilled water in an ultrasonic cleaner, dried, and carefully mounted`).
  - *Basis*: Recurring verbatim template in `P01`, `P03`, `P04`, `P06`, `P07`, `P08`, `P10`, `P14`.
  - *Evidence*: `"The rider and flat specimens were degreased using alcohol and distilled water in an ultrasonic cleaner..."` (`P01`)

### Modeling (`R22`–`R24`)
- **R22 (Active Mathematical `we` in Modeling)**: Unlike `experimental`, use active first-person plural `we` (`We consider...`, `we set...`, `For simplicity, we define...`) at **~2.0–2.5 per 1,000 words** alongside present-tense passive (`is assumed as`, `can be expressed as`, `is given as`).
  - *Basis*: `modeling` has the corpus's highest `we` rate (**2.27 / 1,000w**), **75.9%** present tense, and **50.2%** passive ratio.
  - *Evidence*: `"For simplicity, we define g = ρ1/ρ2 and (∂V2/∂r)|r=r0 = f(θ)."` (`P13`)
- **R23 (Equation Lead-In & `where` Definition Frame)**: Introduce display equations with `is given as` / `can be expressed as` / `are taken as follows:` `[EQ]`, and immediately follow with a lower-case `where <sym1> and <sym2> are <def1> and <def2>, respectively.`
  - *Basis*: ` expressed as where` ranks in top Ren personal trigrams ($z = +1.90$); `respectively` is `0.91 / 1,000w`.
  - *Evidence*: `"Holm [CIT] has shown that the constriction resistance... can be expressed as [EQ] where ρ and a are..."` (`P13`)
- **R24 (FEM Mesh & Boundary Description)**: When presenting COMSOL/FEM models, state the software version, element type (`meshed with traditional triangular/tetrahedral elements`), radial mesh grading (`graded radially outward from the initial point of contact, with the densest mesh in the contact region`), minimum element size, and electrical boundary conditions (`top-most surface` prescribed voltage/current, `bottom-most surface` grounded, lateral surfaces `electrically insulated`).
  - *Basis*: Verbatim structure across `P02`, `P09`, `P13`, `P17`, `P22`, `P28`.
  - *Evidence*: `"The meshes, presented in [FIG 3], are graded radially outward from the initial point of contact..."` (`P13`)

### Results (`R25`–`R27`)
- **R25 (Active Figure-Pointer Openings & Present Tense Dominance)**: Open results paragraphs with `[FIG n] shows/illustrates the variation in <Y> as a function of <X>` or `As shown in [FIG n], ...` (always include `in [FIG n]`, never bare `As shown,` per Tier S precedence); maintain **~75% present tense** and **~35% passive voice**.
  - *Basis*: `results` present tense = **76.8%**, passive ratio = **35.9%**, `show` = **7.57 / 1,000w**, `increase` = **7.81 / 1,000w**.
  - *Evidence*: `"[FIG 9] shows the results of illustrative calculations of the dependence of R* on..."` (`P22`)
- **R26 (Stage-Wise Quantitative Trajectory)**: Partition waveforms and degradation curves into named or numbered stages/zones (`can be characterized by four stages, namely low and stable, slight rise, sharp increase and severe fluctuation`), citing exact threshold cycle numbers, slopes, and parameter ranges.
  - *Basis*: `sent_len` P50=`22` (P25–P75: `16–29`), `para_words` P50=`106`.
  - *Evidence*: `"The contact resistance behavior can be characterized by four stages, namely low and stable, slight rise..."` (`P01`)
- **R27 (Paragraph-Closing Local Attribution)**: Close results paragraphs with a 1–2 sentence physical interpretation using `This is (mainly) attributed to ...`, `This indicates that ...`, or `It is noted that ...`.
  - *Basis*: `indicate` (`2.03 / 1,000w`) and `attribute` (`1.14 / 1,000w`) peak in `results`.
  - *Evidence*: `"This is attributed to severe oxidation wear and abrasive wear caused by the temperature rise..."` (`P03`)

### Mechanism (`R28`–`R30`)
- **R28 (Coupled Multi-Process Framing)**: Frame mechanism sections around coupled physical processes (`There are two coupled physical processes during..., namely <A> and <B>`) and classical contact resistance decomposition ($R_c = R_s + R_f$, constriction + film resistance).
  - *Basis*: `mechanism` `sent_len` P50=`21`, P90=`51` (longest complex causal sentences), passive ratio = **47.2%**.
  - *Evidence*: `"There are two coupled physical processes during the whole fretting wear of contacts, namely conduction and friction..."` (`P01`)
- **R29 (High-Density `It is <VBN> that` & `However,` / `Therefore,` Chains)**: Use `However,` (`6.06 / 100 sents`) to rule out insufficient single-factor explanations, `Therefore,` (`4.76 / 100 sents`) to deduce interfacial consequences, and `It is demonstrated/considered that` (`5.19 / 100 sents`) to state governing mechanisms.
  - *Basis*: `mechanism` has the corpus's highest rates of `However,`, `Therefore,`, `It is <VBN> that`, and modals (`23.4 / 100 sents`).
  - *Evidence*: `"Therefore, these factors may account for the higher instantaneous contact resistance values..."` (`P05`)
- **R30 (Numbered Multi-Factor Mechanism Summary)**: When multiple competing physical factors govern contact area or resistance, synthesize them inline as `(1) the increment of ...; (2) the reduction of ...; and (3) the decrement of ...`.
  - *Basis*: Attested in `P03` (Tier S) and `P05` (Tier A).
  - *Evidence*: `"Three factors influencing the contact area and real conductive area... could be summarized as: (1)..."` (`P03`)

### Conclusion (`R31`–`R33`)
- **R31 (Conclusion Opening Formula)**: Open `conclusion` with `"This investigation/paper mainly aims to (systematically) determine/investigate the <target> of <contact system>..."` or `"The <behavior> of <contacts> is investigated at various <parameters>..."`.
  - *Basis*: Attested in `P01`, `P02`, `P03`, `P12`, `P13`, `P14`, `P22`.
  - *Evidence*: `"This investigation mainly aims to determine the electrical contact resistance of a circular constriction..."` (`P13`)
- **R32 (Two Valid Conclusion Formats — `summary` vs `numbered`)**:
  - For **modeling/theoretical papers** (`P13`, `P22`), write a single cohesive `summary` paragraph (`110–180` words) continuing immediately with `"Our results indicate that..."`, `"Meanwhile,..."`, and `"Furthermore,..."`.
  - For **experimental fretting/regime papers** (`P01`, `P03`), follow the scope summary with `"The main findings are as follows:"` and a `(1) ... (2) ... (3) ...` `numbered` list.
  - *Basis*: `conclusion` `our` rate = **1.56 / 1,000w** (highest in corpus), `Meanwhile` = `3.36 / 100 sents`, `Therefore` = `3.36 / 100 sents`.
  - *Evidence*: `"Our results indicate that mechanical load is a sensitive parameter to contact resistance of sphere-plane contact."` (`P22`)
- **R33 (Root-Reason Closing Statement)**: Close the conclusion by identifying the fundamental physical driver using `"<Factor> is not only the root reason for <effect A>, but also causes <effect B>..."` or stating its engineering design value.
  - *Basis*: Attested in `P13` (Tier S), `P22` (Tier A), `P23`.
  - *Evidence*: `"The difference of electrical conductivity between substrate and coating is not only the root reason..."` (`P13`)

---

## Part III — Distinctive Lexicon & Banned AI Clichés

# Lexicon — Wanbin Ren (`lexicon.md`)

> Derived from `data/processed/stats.json` and `data/processed/lexicon.json` (Monroe et al., 2008 z-scored log-odds across 20 Ren S+A papers, 10 B-tier student papers, and 30 AI baseline rewrites).

---

## 1. Signature Words & Phrases (with Density Caps)

| Phrase / Word | Typical Position & Function | Corpus Rate (S+A Train) | Max / 100w (Lint Cap) | Short Evidence (`paper_id`, ≤ 20w) |
|---|---|---:|---:|---|
| **`explicitly`** | Post-verbal / clause-final (87%): `are recorded / compared / addressed / described explicitly` | 0.41 / 1,000w (34 hits in S+A) | **0.65** (≤ 1 per 200w) | `"current lines profile and isopotential are compared explicitly."` (`P22`) |
| **`It is noted/shown/found/demonstrated/clear that`** | Sentence-initial formal-subject passive introducing a finding or deduction | 3.17 / 100 sents | **1.20** | `"It is noted that the contact resistance only depends on..."` (`P22`) |
| **`is (mainly) attributed to`** | Post-copular causal attribution in `results` / `mechanism` / `conclusion` | 0.58 / 1,000w ($z=+2.28$ vs B) | **0.80** | `"This difference is attributed to the specific conforming feature..."` (`P22`) |
| **`as a function of`** | Prepositional phrase linking plotted metric $Y$ to independent variable $X$ | 0.61 / 1,000w ($z=+1.86$ vs AI) | **1.00** | `"contact resistance was continuously measured as a function of fretting cycles"` (`P01`) |
| **`correlates closely with` / `closely correlates with`** | Expressing strong physical coupling between two variables | 0.09 / 1,000w | **0.40** | `"Dynamic welding... correlates closely with the contact bounce"` (`P12`) |
| **`is closely/significantly/greatly dependent on`** | Expressing governing parameter dependence | 0.20 / 1,000w ($z=+1.95$ vs B) | **0.50** | `"selection of a contact material is closely dependent on experimental verification."` (`P16`) |
| **`by introducing our newly designed test rig` / `using our designed model switch`** | Introducing custom experimental apparatus in `abstract` / `introduction` / `experimental` | 1 per experimental paper | **0.40** | `"studied by introducing our newly designed test rig."` (`P08`) |
| **`, namely <A> and <B>,`** | Appositive introduction of regimes, contact types, or parameter values | 0.31 / 1,000w | **0.60** | `"Two representative cambered surface contacts, namely sphere-plane contact and cylinder-plane contact"` (`P22`) |
| **`, that is,`** | Introducing mathematical definition or component breakdown | 0.25 / 1,000w | **0.50** | `"comprise three components of resistance, that is, the spreading resistance..."` (`P13`) |
| **`comprehensively` / `simultaneously` / `individually` / `separately`** | Clause-final manner adverbs (68–77% post-verbal/final) | 0.17–0.24 / 1,000w | **0.50** | `"determined by the feature of cambered surface and mechanical load comprehensively."` (`P22`) |
| **`This investigation/paper mainly aims to`** | Opening sentence of `conclusion` | 1 per conclusion | **0.40** | `"This investigation mainly aims to determine the electrical contact resistance..."` (`P13`) |
| **`Our results indicate that`** | Second sentence of `conclusion` (`summary` style) | 1.56 `our` / 1,000w in `conclusion` | **0.50** | `"Our results indicate that mechanical load is a sensitive parameter..."` (`P22`) |

---

## 2. Preferred Reporting & Research Verbs by Section

| Section | Primary Verbs (per 1,000w in S+A Train) | Typical Syntactic Voice |
|---|---|---|
| **`abstract`** | `study` (3.22), `investigate` (3.42), `present` (2.82), `compare` (2.82), `reveal` (2.61), `show` (2.41), `observe` (2.21), `measure` (2.21), `calculate` (2.01), `evaluate` (2.01) | Passive (`is studied`, `are evaluated`, `are compared explicitly`) |
| **`introduction`** | `increase` (3.84), `result` (2.87), `present` (2.75), `investigate` (2.64), `show` (2.40), `study` (2.25), `observe` (1.67), `find` (1.36), `propose` (1.01), `examine` / `evaluate` | Past active for literature (`studied`, `examined`, `found`); present passive for `"In this paper"` (`is investigated`, `are addressed`) |
| **`experimental`** | `measure` (6.40), `show` (5.00), `describe` (1.45), `introduce` (1.28), `calculate` (0.93), `obtain` (0.81), `define` (0.70), `supply`, `assess`, `degrease`, `mount`, `acquire`, `characterize` | Passive (`was supplied by`, `were degreased`, `was continuously measured`, `were assessed using`) |
| **`modeling`** | `show` (5.93), `define` (2.65), `assume` (1.77), `model` (1.77), `consider` (1.64), `describe` (1.64), `obtain` (1.26), `determine` (1.26), `express` (1.01), `mesh`, `grade` | Active `we` (`We consider`, `we define`, `we set`) + present passive (`can be expressed as`, `is assumed as`) |
| **`results`** | `increase` (7.81), `show` (7.57), `result` (4.93), `decrease` (2.21), `indicate` (2.03), `observe` (1.92), `attribute` (1.14), `reach` (1.00), `correlate` (0.91), `determine` (0.90), `illustrate` | Active figure subject (`[FIG n] shows/illustrates`) + `It is noted/shown that` + `is attributed to` |
| **`mechanism`** | `increase` (6.23), `show` (5.31), `result` (3.57), `model` (3.49), `lead` (1.91), `cause` (1.91), `decrease` (1.49), `indicate` (1.41), `propose` (1.33), `explain` (1.33), `summarize`, `account for` | Causal active/passive mix with modals (`could`, `would`, `may`) |
| **`conclusion`** | `result` (9.14), `increase` (7.10), `cause` (3.13), `study` (2.65), `show` (2.53), `decrease` (2.53), `measure` (2.17), `investigate` (1.80), `obtain` (1.68), `determine` (1.68), `indicate` | Active meta-subject (`This paper mainly aims to...`, `Our results indicate that...`) |

---

## 3. Preferred Connectives by Section

| Function | Preferred Connectives (with Section Affinity) | Usage Note |
|---|---|---|
| **Contrast / Gap Pivot** | `However,` (3.09 / 100 sents; **6.06** in `mechanism`, **5.74** in `introduction`), `Whereas`, `On the other hand,` | Primary contrast marker; prefer `However,` over `Nevertheless,` (only 1 hit in S+A) |
| **Sequential / Stepwise** | `Subsequently,` (**4.18** / 100 sents in `abstract`), `Then,` (1.82 in `modeling`), `Next,`, `Finally,` (2.51 in `abstract`) | Use `Subsequently,` in `abstract`/`introduction` roadmap; use `First,/Firstly, ... Next, ... Finally,` for 3-step roadmaps |
| **Additive / Reinforcement** | `Furthermore,` (2.51 in `abstract`, 1.52 in `modeling`), `In addition,` (1.40 / 100 paras paragraph-initially), `Moreover,` (1.67 in `abstract`), `Meanwhile,` (**3.36** in `conclusion`, 1.73 in `mechanism`) | `Meanwhile,` is heavily favored for parallel observations (`36` hits in S+A vs `0` in AI baseline) |
| **Causal / Deductive** | `Therefore,` (2.11 / 100 sents; **4.76** in `mechanism`), `Thus,` (1.77 / 100 sents; **3.65** in `modeling`), `As a result,` | Prefer `Therefore,` and `Thus,` over `Consequently,` (only 2 hits in S+A) |
| **Visual / Evidence Pointer** | `As shown in [FIG n],` (`z = +2.41`), `As seen in [FIG n],`, `Comparing [FIG a] with [FIG b],` | Always include `in [FIG n]` (never bare `As shown,` in `balanced` mode) |
| **Concession / Scope Framing** | `Admittedly,`, `In general,` (**6.3** / 100 paras in `experimental`), `Generally,`, `For simplicity,` (in `modeling`) | Natural paragraph openers in Ren's prose |

---

## 4. Replacement Table (`AI-Default → Ren-Preferred`)

| AI-Default Expression | Ren-Preferred Expression | Rule / Basis |
|---|---|---|
| `"In this study/paper/work, we comprehensively investigate..."` | `"In this paper, the <behavior> of <contact> is studied/investigated..."` or `"This paper investigates..."` | `R14` ($z = -5.15$ for `this paper we`) |
| `"across a broad spectrum of <parameters>"` | `"over a large range of <aspect ratios / frequencies>"` or `"under different <parameter> combinations"` | `R08` (`across` $z = -9.25$) |
| `"across the contact interface / worn scar"` | `"within the contact zone / within the fretted zone"` | `R08` (`within` $z = +4.17$) |
| `"by leveraging / utilizing a custom-built platform"` | `"by introducing our newly designed test rig"` or `"by using our designed model switch"` | `R08`, `R20` (`by using` $z = +1.76$) |
| `"utilize / utilized / utilizing"` | `"use / used / by using / with the use of"` | `R08` (`utilize` $z = -5.19$) |
| `"elucidate / unravel / shed light on the mechanism"` | `"explain / interpret / determine / understand the mechanism"` (`...are interpreted explicitly`) | `R03`, `R09` (`elucidate` = 0 in S+A) |
| `"underscore / highlight the pivotal role of <X>"` | `"confirm / show that <X> plays an important/crucial role in..."` | `R09` (`underscore`, `pivotal` = 0 in S+A) |
| `"stemming from / attributable to"` | `"which is (mainly) attributed to..."` or `"which results from..."` | `R05` (`is attributed to` $z = +2.28$) |
| `"exhibits a strong correlation with / is contingent upon"` | `"correlates closely with"` / `"is closely/significantly dependent on"` | `R06` (`F05`, `F06`) |
| `"versus / plotted against <variable>"` | `"as a function of <variable>"` | `R06` (`as a function of` $z = +1.86$) |
| `"Notably, / Importantly, our findings reveal that..."` | `"It is noted/shown/found that..."` or `"Our results indicate that..."` | `R04`, `R32` (`notably` = 0 in S+A) |
| `"Furthermore, a comprehensive framework is established"` | `"Furthermore, a universal mathematical / finite-element model is built/presented"` | `R09`, `R16` (`framework` = 0 in S+A) |
| `"Contacts subjected to varying current loads"` | `"Contacts under different/various current loads"` | `R08` (`subjected to` $z = -5.00$) |
| `"With the rise / escalation of <X>"` | `"With the increase of/in <X>"` | `R25` (`with the increase of` $z = +1.97$) |

---

## 5. Corpus-Verified Banned Words (`0` Hits in All 20 Ren S+A Papers)

### 5.1 Strictly Banned AI Clichés (`count = 0` in Ren S+A)
`augment`, `augmenting`, `bespoke`, `bolster`, `bolstering`, `cutting-edge`, `delve`, `delves`, `delving`, `elucidate`, `elucidated`, `elucidates`, `elucidating`, `encompass`, `encompasses`, `encompassing`, `facilitating`, `foster`, `fostering`, `framework`, `garner`, `garnered`, `garnering`, `groundbreaking`, `herein`, `holistic`, `imperative`, `importantly`, `in-depth`, `interplay`, `intricate`, `landscape`, `leverage`, `leveraged`, `leveraging`, `meticulously`, `multifaceted`, `notably`, `noteworthy`, `overarching`, `paramount`, `pave the way`, `pivotal`, `realm`, `scrutinize`, `scrutinized`, `shed light`, `synergistic`, `testament`, `ubiquitous`, `ubiquitously`, `uncover`, `uncovered`, `uncovers`, `underscore`, `underscores`, `underscoring`, `unravel`, `unraveling`.

### 5.2 Attested Words in Ren's Corpus — **Do NOT Ban**
- **Core High-Frequency Ren Words**: `meanwhile` (36 hits), `explicitly` (34 hits), `significantly` (34 hits), `furthermore` (28 hits), `subsequently` (13 hits), `moreover` (11 hits), `substantially` (9 hits), `comprehensively` (7 hits), `essential` (4 hits), `vital` (3 hits), `dramatically` (3 hits).
- **Rare in Ren (1–2 hits across 20 papers — avoid introducing, replace with preferred synonym)**:
  - `utilize / utilized` (2 hits → use `use` / `by using`)
  - `facilitate / facilitates` (2 hits → use `help` / `promote` / `allow`)
  - `comprehensive` (2 hits, adjective; note adverb `comprehensively` has 7 hits and is idiomatic in Ren!)
  - `consequently` (2 hits → prefer `therefore` / `thus`)
  - `nevertheless` (1 hit in S+A → prefer `however`)
  - `crucial` (1 hit in S+A → acceptable in `"plays a crucial role"`, or use `important` / `key`)

---

## Part IV — Style vs. Error Policy (`F01`–`F36`, `O01`–`O08`)

# Style vs. Error Policy (`error_policy.md`)

Decided policy (`docs/design_notes.md` §2.2 & §9): **imitate Wanbin Ren's rhetorical structure, sentence patterns, and signature vocabulary, while fixing grammatical errors** (`fidelity_level: balanced` by default).

| Class | Meaning | `fidelity_level: balanced` (default) | `fidelity_level: strict` |
|---|---|---|---|
| `KEEP_STYLE` | Characteristic, idiomatic choices that define Ren's voice | **Reproduce** (within P90 density cap) | **Reproduce** |
| `FIX_ERROR` | Grammatical, syntactic, or lexical errors | **Always correct** to the idiomatic form | **Always correct** |
| `OPTIONAL_NONNATIVE` | Harmless non-native habits attested in the corpus | **Use sparingly / prefer cleaner alternative** | **Reproduce** |

---

## 1. Master Feature Classification Table

| ID | Feature / Pattern | Class | Corrected / Idiomatic Form (when `FIX_ERROR` or `balanced`) | Corpus Evidence (`paper_id`, ≤ 20w) | Note |
|---|---|---|---|---|---|
| **F01** | Post-verbal / clause-final `explicitly` (`are recorded/addressed/compared explicitly`) | `KEEP_STYLE` | Keep as-is (cap ≤ 0.15 / 100w) | `"isopotential are compared explicitly."` (`P22`); `"are addressed explicitly."` (`P13`) | 87% post-verbal/final across 34 hits in S+A |
| **F02** | Formal-subject passive openings (`It is shown/found/noted/demonstrated/clear that …`) | `KEEP_STYLE` | Keep as-is | `"It is noted that the contact resistance only depends on..."` (`P22`) | 3.17 / 100 sentences in S+A train (5.19 in `mechanism`) |
| **F03** | Self-built apparatus introduction (`by introducing our newly designed test rig`, `using our designed model switch`) | `KEEP_STYLE` | Keep `"our newly designed test rig"` | `"studied by introducing our newly designed test rig."` (`P08`) | Signature experimental framing |
| **F04** | Causal attribution with `is (mainly) attributed to` | `KEEP_STYLE` | Keep as-is | `"This difference is attributed to the specific conforming feature..."` (`P22`) | 5× higher in Ren S+A (0.58/1kw) than students (0.11/1kw) |
| **F05** | Correlation phrasing `correlates closely with` / `closely correlates with` | `KEEP_STYLE` | Keep as-is | `"Dynamic welding... correlates closely with the contact bounce"` (`P12`) | Signature relational verb + adverb |
| **F06** | Dependency phrasing `is closely/greatly/significantly dependent on` | `KEEP_STYLE` | Keep as-is | `"is closely dependent on experimental verification."` (`P16`) | Preferred over AI `"hinges on"` / `"is contingent upon"` |
| **F07** | Functional dependence `as a function of <cycles/time/position>` | `KEEP_STYLE` | Keep as-is | `"continuously measured as a function of fretting cycles"` (`P01`) | 0.61 / 1,000w in S+A train |
| **F08** | Appositive enumeration with `namely` (`two typical contacts, namely A and B`) | `KEEP_STYLE` | Keep as-is | `"Two representative cambered surface contacts, namely sphere-plane contact and cylinder-plane contact"` (`P22`) | 0.31 / 1,000w in S+A train |
| **F09** | Equation bridge `that is, [EQ]` / `can be expressed as [EQ] where …` | `KEEP_STYLE` | Keep as-is | `"can be expressed as [EQ] where ρ and a are..."` (`P13`) | Canonical modeling transition |
| **F10** | Discourse progression `Subsequently, … Furthermore, … Meanwhile, …` | `KEEP_STYLE` | Keep as-is | `"Subsequently, the effects of size parameters... Furthermore, dissimilarity..."` (`P22`) | Core connective triad in abstracts & results |
| **F11** | Passive-heavy `abstract` (69.0%) and `experimental` (71.9%) vs active `we` in `modeling` (2.27/1kw) | `KEEP_STYLE` | Keep section-specific voice shift | `"We consider the simple situation of a hemispherical metal..."` (`P13`) | Distinguishes `modeling` from `experimental` |
| **F12** | Active figure-pointer openings (`[FIG n] shows/illustrates the variation in …`) | `KEEP_STYLE` | Keep as-is | `"[FIG 9] shows the results of illustrative calculations..."` (`P22`) | Drives 76.8% present tense in `results` |
| **F13** | Conclusion scope-restatement + `Our results indicate that …` | `KEEP_STYLE` | Keep as-is | `"This investigation mainly aims to determine... Our results indicate that..."` (`P13`) | Canonical S/A conclusion opening (`P13`, `P22`) |
| **F14** | Slash-separated multi-condition compact notation (`5/15/25 V`, `0.2/0.5/1 A`) | `KEEP_STYLE` | Keep as-is | `"in conditions of nonarc load (5/15/25 V and 0.2/0.5/1 A)"` (`P07`) | Concise test-condition listing |
| **F15** | Clause-final `comprehensively` / `simultaneously` / `individually` / `separately` | `KEEP_STYLE` | Keep as-is | `"determined by the feature of cambered surface and mechanical load comprehensively."` (`P22`) | Matches post-verbal adverb placement |
| **F16** | Passive of intransitive `result from`: `"is/are resulted from"` | `FIX_ERROR` | `"result(s) from"` or `"is/are caused by"` | `"molten bridge phenomena are resulted from the competition"` (`P08`) | `result` is intransitive; never passivize |
| **F17** | Wrong preposition after `result`: `"result(s) into"` | `FIX_ERROR` | `"result(s) in"` or `"lead(s) to"` | `"high bounce energy results into the increase"` (`P23`) | Always `result in`, never `result into` |
| **F18** | Adjective instead of adverb before participle: `"our new designed test rig"` | `FIX_ERROR` | `"our newly designed test rig"` | `"by introducing our new designed test rig."` (`P06`, `P10`) | `P08` uses the correct `"our newly designed test rig"` |
| **F19** | Misuse of `ever` for past literature: `"ever published results"` | `FIX_ERROR` | `"previously published results"` | `"Ever published research results have revealed that"` (`P23`) | Calque of 中文“已发表的研究结果” |
| **F20** | Transitive misuse of `reoccur`: `"reoccur(ring) the welding phenomenon"` | `FIX_ERROR` | `"reproduce / reproducing the welding phenomenon"` | `"method for reoccurring the welding phenomenon"` (`P26`) | `reoccur` is intransitive ("occur again") |
| **F21** | Non-standard topic prepositions: `"Regarding to"`, `"Regards to"`, `"In terms to"` | `FIX_ERROR` | `"Regarding"`, `"With regard to"`, `"In terms of"` | `"Regarding to the calculation formula of contact resistance"` (`P13`) | Very common preposition intrusion |
| **F22** | Wrong preposition with `relevant`: `"is relevant with"` | `FIX_ERROR` | `"is relevant to"` or `"is related to"` | `"introduce the plating factor, which is relevant with the ratio"` (`P13`) | Appears 6 times in `P03` and `P13` |
| **F23** | Wrong preposition with `same`: `"(the) same with"` | `FIX_ERROR` | `"the same as"` | `"which is almost the same with the no current case."` (`P07`) | Appears 6 times in `P06`, `P07`, `P11`, `P23` |
| **F24** | Redundant preposition after verb `equal`: `"equals to"` | `FIX_ERROR` | `"equals"` or `"is equal to"` | `"The M&B operation mode equals to the combination"` (`P23`) | Adjective `is equal to` is fine; verb `equals` takes direct object |
| **F25** | Noun instead of adjective in `"inversely proportion to"` | `FIX_ERROR` | `"inversely proportional to"` | `"which is inversely proportion to the contact resistance."` (`P23`) | Appears 4 times in `P23`, `P26` |
| **F26** | Objectless `allow`: `"allows to <verb>"` / `"allows <gerund>"` | `FIX_ERROR` | `"allows <NP> to <verb>"` or `"makes it possible to <verb>"` | `"allows to in situ observe the variations"` (`P23`) | Use `P06`'s `"makes it possible to measure"` |
| **F27** | Causative `make` followed by finite verb: `"make(s) <NP> decreases/is"` | `FIX_ERROR` | `"make(s) <NP> decrease/be"` or `"cause(s) <NP> to decrease"` | `"which make the local force of contact asperities decreases"` (`P16`) | Bare infinitive required after causative `make` |
| **F28** | Incomplete noun-clause after `due to / attributed to the fact that <NP>` | `FIX_ERROR` | `"attributed to <NP>"` or `"due to the fact that <clause with verb>"` | `"attributed to the fact that the specific conforming feature"` (`P22`) | Drop `the fact that` when followed only by a noun phrase |
| **F29** | Malapropism `"harness"` for `"hardness"` | `FIX_ERROR` | `"hardness"` | `"which is relevant to the harness of materials"` (`P03`, `P05`, `P10`) | Spelling error in material property |
| **F30** | Non-idiomatic adjectives `"challengeable"` / `"top-urgent"` | `FIX_ERROR` | `"challenging"` / `"urgent"` (or `"of great importance"`) | `"the calculation of tON is challengeable."` (`P15`) | `challengeable` means "open to dispute", not "difficult" |
| **F31** | Subject–verb agreement lapses (`This paper first present`, `the cracks distributes`) | `FIX_ERROR` | Match singular/plural verb (`This paper first presents`, `the cracks distribute`) | `"This paper first present a universal mathematical model"` (`P13`) | Always enforce standard agreement |
| **F32** | Sentence-initial `"Also,"` | `OPTIONAL_NONNATIVE` | In `balanced`: max 1 per section (prefer `Furthermore,` / `In addition,`); in `strict`: allow | `"Also, it is the key element in providing early warning"` (`P13`) | 26 hits in corpus; B-tier students overuse it (2× Ren) |
| **F33** | Sentence-initial `"And "` (`And the…`) | `OPTIONAL_NONNATIVE` | In `balanced`: replace with `Moreover,` / `Meanwhile,` or merge clause; in `strict`: allow | `"And the superiority of cylinder-plane contact would be performed"` (`P22`) | 75 hits in corpus (heaviest in `P02`, `P22`) |
| **F34** | Post-verbal / mid-clause `"firstly"` (`calculated ... firstly, and then ...`) | `OPTIONAL_NONNATIVE` | In `balanced`: use `"first"` mid-clause and `"First,"`/`"Firstly,"` sentence-initially | `"calculated under every corresponding load force condition... firstly"` (`P02`) | 12 hits in corpus |
| **F35** | Future-work idiom `"will be in schedule"` | `OPTIONAL_NONNATIVE` | In `balanced`: `"will be carried out in future work"`; in `strict`: allow | `"detailed works on the plastic deformation will be in schedule"` (`P22`) | Appears at the end of `P21`, `P22` conclusions |
| **F36** | Bare `"As shown, the…"` without `"in [FIG n]"` | `OPTIONAL_NONNATIVE` | In `balanced`: always write `"As shown in [FIG n], the…"` (Tier S standard) | `"As shown, the tangential force behaviors appear to be..."` (`P29`) | Characteristic of Tier B (`z = -5.22`); Tier S includes `[FIG n]` |

---

## 2. Top 10 Most Important `FIX_ERROR` Patterns (Must Never Appear in Output)

1. **`are/is resulted from`** → **`result(s) from`** or **`are/is caused by`** (`F16`)
2. **`result(s) into`** → **`result(s) in`** or **`lead(s) to`** (`F17`)
3. **`our new designed test rig`** → **`our newly designed test rig`** (`F18`)
4. **`Regarding to` / `Regards to` / `In terms to`** → **`Regarding` / `With regard to` / `In terms of`** (`F21`)
5. **`is relevant with`** → **`is relevant to`** or **`is related to`** (`F22`)
6. **`(the) same with`** → **`the same as`** (`F23`)
7. **`equals to`** → **`equals`** or **`is equal to`** (`F24`)
8. **`inversely proportion to`** → **`inversely proportional to`** (`F25`)
9. **`due to / attributed to the fact that <NP without verb>`** → **`attributed to <NP>`** (`F28`)
10. **`ever published results` / `reoccurring the phenomenon` / `is challengeable`** → **`previously published results` / `reproducing the phenomenon` / `is challenging`** (`F19`, `F20`, `F30`)

---

## Part V — Chinese-to-English Domain Glossary & Translation Guide (`T01`–`T20`)

# Glossary (Chinese → English) — Electrical Contacts (`glossary_zh_en.md`)

> Extracted from Wanbin Ren's 30 corpus papers (`P01`–`P30`). You can append additional group-internal Chinese terms at any time.

---

## 1. Contact Physics, Geometry & Resistance (电接触物理、几何与接触电阻)

| 中文术语 | English (Ren's Preferred Usage) | First-Use Abbrev. | Corpus Note & Papers |
|---|---|---|---|
| 电接触 | electrical contact | | Core domain term (`P01`–`P30`) |
| 接触电阻 / 电接触电阻 | contact resistance / electrical contact resistance | ECR (in connector/vibration papers `P19`) | Both used; `contact resistance` ($R_c$) is the default in `P01`, `P03`, `P13`, `P22` |
| 收缩电阻 | constriction resistance | $R_s$ | Classical Holm constriction (`P02`, `P09`, `P13`, `P22`) |
| 扩展电阻 | spreading resistance | $R_c$ / $\bar{R}_c$ | Distinguished from total constriction resistance in coated/cambered contacts (`P13`, `P22`) |
| 膜层电阻 / 表面膜电阻 | film resistance | $R_f$ | Oxide/contaminant film resistance (`P03`, `P04`, `P05`, `P13`) |
| 过渡区电阻 | transition resistance / resistance in transition zone | | Induced by substrate–coating resistivity mismatch (`P02`, `P13`) |
| 体电阻 / 基体体电阻 | bulk resistance (of the substrate) | | Third component alongside spreading & transition resistance (`P02`, `P13`) |
| 导电斑点 / $a$ 斑点 | contact a-spot / circular a-spot | | Always hyphenated `a-spot` / `a-spots` (`P07`, `P08`, `P10`, `P13`, `P17`, `P28`) |
| 真实接触面积 / 导电面积 | real contact area / conductive area | | `real contact area` (`P27`), `conductive area` / `conduction area` (`P01`, `P03`, `P05`) |
| 名义接触面积 | nominal contact area | | (`P11`, `P27`) |
| 微凸体 / 表面微凸体 | asperity / contact asperity | | Plural `asperities`; `elliptical asperity` (`P27`), `asperity interactions` (`P28`) |
| 微凸体峰点 | asperity-peak | SAP / NP | `single asperity-peak (SAP)`, `neighboring point (NP)` (`P27`) |
| 曲面触点 / 弧面触点 | cambered surface contact / contact bodies with cambered surface | | Covers sphere-plane & cylinder-plane (`P13`, `P22`) |
| 球-平面接触 | sphere-plane contact | | Always hyphenated (`P01`, `P13`, `P22`) |
| 柱-平面接触 | cylinder-plane contact | | Line/conforming contact (`P21`, `P22`) |
| 非共形接触 / 共形接触 | non-conforming contact / conforming contact | | (`P22`) |
| 电流线 / 等势线 | electrical current lines / isopotential (lines) | | Often `"distributions of electrical current lines profile and isopotential"` (`P13`, `P22`) |
| 电流拥挤效应 | current crowding (effect) | | (`P13`, `P17`, `P22`) |
| 镀层因子 | plating factor | | Williamson–Greenwood plating factor (`P13`) |
| 软化电压 / 熔化电压 | softening voltage / melting voltage | | e.g., Au softening `80 mV` (`100 °C`), melting `430 mV` (`1064 °C`) (`P01`, `P04`, `P10`) |
| 科尔劳施方程（电压-温度关系） | Kohlrausch's equation / temperature–voltage (T–V) relation | | Corrected with modified Lorenz coefficient $L^*$ (`P09`) |
| 洛伦兹系数 | Lorenz coefficient | $L$ | (`P01`, `P04`, `P09`) |

---

## 2. Fretting, Vibration & Wear Regimes (微动、振动与磨损机制)

| 中文术语 | English (Ren's Preferred Usage) | First-Use Abbrev. | Corpus Note & Papers |
|---|---|---|---|
| 微动 | fretting | | Defined as small-amplitude oscillatory micro-motion (< 100 μm) (`P01`, `P03`, `P04`, `P05`, `P14`) |
| 微动腐蚀 | fretting corrosion | | Primary degradation mechanism of plated copper alloy contacts (`P01`, `P03`, `P04`) |
| 微动磨损 / 微动疲劳 | fretting wear / fretting fatigue | | (`P01`, `P03`, `P05`, `P14`) |
| 微动区域图 / 微动状态图 | fretting regime map / fretting map | | Plotted over vibration amplitude and frequency combinations (`P03`, `P14`) |
| 粘着-部分滑移区（I 区） | stick / partial slip regime (Regime I) | | `infinite electrical contact life zone` (`P03`, `P14`) |
| 全滑移氧化磨损区（II 区） | gross slip regime with oxidation wear (Regime II) | | `oxidation-dominated failure zone` (`P03`, `P14`) |
| 瞬态不稳定导电失效区（III 区） | transient unstable conductivity dominated failure zone (Regime III) | | Driven by high sliding speed & thermoelastic instability (`P03`, `P05`, `P14`) |
| 磨痕 / 微动磨斑 | wear track / fretted scar / fretted zone | | `"within the fretted zone"`, `"four fretted scars"` (`P01`, `P03`, `P04`, `P14`) |
| 磨屑 / 氧化磨屑 | wear debris / oxide debris | | `"accumulation of oxide debris at the contact zone"` (`P01`, `P03`, `P04`, `P05`) |
| 分层剥落 / 剥落坑 | delamination / spalling crater | | (`P03`, `P04`, `P05`, `P14`, `P18`) |
| 犁沟 / 划痕 / 飞溅物 | furrow / scratches / splashes | | Five regions in `P01`: `scratches, particles, cracks, deposits, and splashes` |
| 瞬断 / 间歇性失效 | intermittence / short duration discontinuity / intermittent failure | | Rapid resistance spikes within micro- to milliseconds (`P04`, `P05`, `P14`) |
| 间歇率 / 失效时间比 | intermittency rate / failure time ratio | | (`P04`, `P05`, `P14`) |
| 热弹性不稳定性 | thermoelastic instability | TEI | Burton's localized thermal bulging model (`P03`, `P05`) |
| 切向摩擦力（有效值） | tangential force (RMS) | $F_{\text{RMS}}$ | (`P03`, `P05`) |
| 定频振动 / 扫频振动 | constant-frequency vibration / frequency sweep vibration | | (`P03`, `P14`, `P19`) |
| 传递路径 / 结构动力学模型 | excitation transmission path / structural dynamic model | | (`P19`) |

---

## 3. Switching, Contact Bounce, Arcing & Welding (开关过程、弹跳、电弧与触点熔焊)

| 中文术语 | English (Ren's Preferred Usage) | First-Use Abbrev. | Corpus Note & Papers |
|---|---|---|---|
| 闭合过程 / 分断过程 | contact-making process / contact-breaking process | | Also `MO (make only)`, `BO (break only)`, `M&B (make & break)` (`P16`, `P23`, `P30`) |
| 超低闭合/分断速度 | superlow (or super low) making/breaking velocity (or speed) | | `25–150 nm/s` (`P06`, `P07`, `P08`, `P10`, `P15`) |
| 冷切换 / 热切换（带电插拔） | cold switching / hot switching | | `cold switching` (`P11`), `hot switching` (`P23`, `P29`) |
| 触点弹跳 / 机械弹跳 | contact bounce (behavior) | | `first impact`, `bounce duration`, `last bounce` ($t_{\text{last}}$), `total bounce time` ($t_{\text{all}}$) (`P12`, `P15`, `P16`, `P23`) |
| 触点熔焊 / 动熔焊 / 静熔焊 | contact welding / dynamic welding / static welding | | (`P12`, `P16`, `P18`, `P23`, `P24`, `P25`, `P26`, `P30`) |
| 熔焊力 / 抗拉熔焊强度 | welding force / contact welding strength | | (`P12`, `P18`, `P23`, `P24`, `P25`, `P26`) |
| 起焊电流 / 阈值熔焊电流 | threshold welding current | $I_{\text{weld}}$ | (`P09`, `P24`, `P25`, `P26`) |
| 熔池 / 焊核 / 熔焊痕迹 | molten pool / weld nugget / welding trace | | (`P07`, `P10`, `P23`, `P24`, `P25`, `P26`) |
| 间歇性金属液桥 | intermittent molten bridge | | Divided into `static bridge` and `dynamic bridge` (`P06`, `P08`, `P10`, `P23`) |
| 弹跳电弧 / 分断电弧 / 重燃 | bounce arc / break (or breaking) arc / restrike | | `bounce energy`, `break arc energy`, `molten bridge energy` (`P16`, `P18`, `P23`, `P30`) |
| 间歇电弧 | intermittent arc | | (`P16`) |
| 冲击电流 / 浪涌电流 | inrush current | | Capacitive / lamp / overload inrush current (`P12`, `P16`, `P25`) |
| 电动斥力 | electrodynamic repulsion force | EDRF | Holm + Lorentz force on contact bridge (`P17`) |
| 表面粘附力 / 粘滞 | surface adhesion force / stiction | | $\mu\text{N}$-level adhesion (`P07`, `P11`) |
| 触点滑移 / 滚动与滑移 | contact sliding (distance) / rolling and sliding behavior | SD | Overtravel wiping action (`P20`, `P23`) |
| 超程 / 释放弹簧 / 柔性簧片 | overtravel / restoring spring / flexible spring component | | (`P12`, `P20`, `P23`, `P30`) |
| 动触点 / 静触点 / 常开触点 | movable contact / stationary (or fixed) contact / normally opened (N.O.) contact | | (`P12`, `P16`, `P20`, `P23`, `P30`) |
| 分断相位角（选相分断角） | point-on-wave (at break / make) | POW | AC relay switching (`P30`) |
| 电寿命试验 / 电耐久试验 | electrical endurance test (or experiment) / electrical lifetime test | | (`P12`, `P16`, `P18`, `P23`, `P30`) |

---

## 4. Materials, Specimens & Test Apparatus (材料、试样与测试装置)

| 中文术语 | English (Ren's Preferred Usage) | First-Use Abbrev. | Corpus Note & Papers |
|---|---|---|---|
| 镀金铜合金触点 | gold-plated (or Au-plated) copper alloy contacts | | Both `gold-plated` (`P01`, `P03`, `P04`, `P05`, `P07`, `P08`, `P14`) and `Au-plated` (`P06`, `P10`) are used |
| 银氧化锡 / 银氧化镉 / 银镍 | silver tin oxide ($\text{AgSnO}_2$) / silver cadmium oxide ($\text{AgCdO}$) / silver nickel ($\text{AgNi}$) | $\text{AgSnO}_2$ | (`P12`, `P16`, `P18`, `P23`, `P24`, `P25`, `P26`) |
| 铍青铜 | beryllium bronze | | Spring material (`P20`, `P23`) |
| 球形压头 / 球头动子 / 平面静子 | sphere indenter / ball-shaped (or hemisphere-shaped) rider / flat sample (or coupon) | | `rider` and `coupon` (or `flat sample`) is the standard pair (`P01`–`P10`, `P14`) |
| 圆柱与簧片触点 / TO-5 微型继电器 | rod and spring contacts / transistor outline package (TO-5) microelectromechanical relay | MEMS relay | (`P21`) |
| 插片与插孔（电连接器） | blade and receptacle pair / pin and socket | | (`P19`, `P29`) |
| 自研试验台 / 模型开关 | our newly designed test rig / our designed model switch | | Never write `"our new designed test rig"` in `balanced` mode (`P06`, `P08`, `P12`, `P23`) |
| 电动振动台 | electrodynamic shaker | | (`P01`, `P03`, `P04`, `P05`, `P14`, `P19`) |
| 压电促动器 / 光栅尺 | piezoelectric actuator / grating ruler | | Superlow-speed rig (`P06`, `P07`, `P08`, `P10`, `P15`) |
| 线性位移台 | linear translation stage | LTS | (`P11`, `P20`, `P23`, `P25`) |
| 压电力传感器 / 应变式力传感器 | piezoelectric force transducer / strain sensor (or load cell) | | (`P01`, `P05`, `P12`, `P23`, `P25`) |
| 四线法（开尔文测阻法） | four-wire method (or 4-wires method) | | (`P01`, `P03`, `P04`, `P05`, `P06`, `P10`, `P21`) |
| 扫描电子显微镜 / X 射线能谱分析 | scanning electron microscopy / energy dispersive X-ray analysis | SEM / EDX (or EDS) | `EDX` in `P01`, `P03`, `P04`, `P14`; `EDS` in `P18`, `P23` |
| 激光共聚焦扫描显微镜 | confocal scanning laser microscope (or confocal optical microscope) | CSLM | (`P06`, `P10`, `P12`, `P27`) |

# Translation Guide (Chinese → English, Mode B) (`translation_guide.md`)

> Authoritative rules for translating Chinese electrical-contact manuscripts into Wanbin Ren's English academic style (`fidelity_level: balanced` by default).

---

## 1. Sentence Restructuring & Cadence (`R01`, `R02`)

1. **Break Chinese Run-On Topic Chains**: Chinese technical sentences often chain 3–5 comma-separated clauses (`由于……，使得……，进而导致……，因此……`). Split them into **1–2 English sentences** targeting the section's median sentence length (**19–23 words**, IQR **16–29 words**, P90 **≤ 37 words**).
2. **Convert Topic-Comment to Passive or Formal-Subject Frames**:
   - 中文无主句 / 泛主语句（`本文研究了……` / `对……进行了实验研究`）→ Passive `"In this paper, the <behavior> of <contact> is studied/investigated..."` (`R14`) or third-person `"This paper investigates..."`, **never** AI-style `"In this paper, we comprehensively delve into..."`.
   - 中文判断/发现句（`结果表明……` / `值得注意的是……` / `研究发现……`）→ Formal-subject `"It is shown/noted/found/demonstrated that …"` (`R04`) or `"Our results indicate that …"` (in `conclusion`, `R32`).

---

## 2. Section-Specific Voice & Tense Mapping (`R13`–`R33`)

| Section | Target Passive Ratio | Target Tense Mix | Key Pronoun & Frame Rule |
|---|---:|---|---|
| **`abstract`** | **65–75%** | ~67% Present / ~30% Past | Avoid `we`; use `Subsequently,` and `Furthermore,`; place `explicitly` post-verbally (`R13`–`R15`) |
| **`introduction`** | **35–45%** | ~50% Present / ~44% Past / ~6% Pres. Perf. | Past tense for literature (`studied`, `examined`, `found`); `However,` for gap; passive in final `"In this paper"` paragraph (`R16`–`R18`) |
| **`experimental`** | **65–75%** | Consistent Past (`was supplied`, `were degreased`) or Present (`consists of`) | Shortest sentences (median 19w); attach hardware specs in parentheses `(Type: ...)` (`R19`–`R21`) |
| **`modeling`** | **45–55%** | ~76% Present | Use active `we` (`We consider...`, `For simplicity, we define...`) + `can be expressed as [EQ] where...` (`R22`–`R24`) |
| **`results`** | **30–45%** | ~77% Present | Open with `[FIG n] shows/illustrates...` or `As shown in [FIG n],`; close with `This is attributed to...` (`R25`–`R27`) |
| **`mechanism`** | **40–55%** | ~70% Present + Modals (`could`, `would`, `may`) | Frame around `two coupled physical processes, namely...`; synthesize factors as `(1)...; (2)...; (3)...` (`R28`–`R30`) |
| **`conclusion`** | **35–45%** | ~70% Present / ~29% Past | Open with `"This investigation/paper mainly aims to..."`; use `"Our results indicate that..."` or `"The main findings are as follows: (1)..."` (`R31`–`R33`) |

---

## 3. High-Frequency Chinese → Ren English Phrase Map

| 中文原句表达 | Ren 标志性英文译法 | 对应规则 |
|---|---|---|
| 在航空航天等高可靠性要求领域广泛应用 | `are widely used in aviation and aerospace engineering to meet the requirements of high quality and high reliability` | `R13`, `R16` |
| 是整个系统中的薄弱环节 / 重要关注点 | `often represent a weak link in the whole system` / `is a very important concern (or issue) to...` | `R16` |
| 利用自行研制的新型试验装置 / 模型开关 | `by introducing our newly designed test rig` / `by using our designed model switch` | `R03`, `R20`, `F03` |
| 明确记录 / 明确对比 / 明确探讨了…… | `are recorded / compared / addressed / described / interpreted explicitly` (句尾/动词后置) | `R03` |
| 随（周次 / 时间 / 位移）的变化规律 | `the variation in <Y> as a function of <fretting cycles / time / position>` | `R06`, `R25` |
| 与……密切相关 / 很大程度上取决于…… | `correlates closely with...` / `is closely (or significantly / greatly) dependent on...` | `R06` |
| 这主要归因于…… / 由……引起 | `This is (mainly) attributed to...` / `which results from...`（**严禁译为** `are resulted from`） | `R05`, `F16` |
| 分为三个阶段，即…… | `can be characterized by (or divided into) three distinct stages, namely <A>, <B>, and <C>` | `R07`, `R26` |
| 在大长径比/宽参数范围内进行了评估 | `are evaluated over a large range of aspect ratios (or under different <param> combinations)`（**不用** `across a broad spectrum`） | `R08` |
| 在微动区域内 / 在接触区内 | `within the fretted zone` / `within the contact region`（**不用** `across the interface`） | `R08` |
| 实验前将动子与静子试样在超声波清洗机中用丙酮、酒精和去离子水除油清洗并干燥 | `The rider and flat specimens were degreased using acetone, alcohol, and distilled water in an ultrasonic cleaner, dried, and carefully mounted in the test rig.` | `R21` |

---

## 4. Strict Fidelity & Hygiene Rules

1. **Terminology & Abbreviations (`R11`)**: Follow `glossary_zh_en.md` strictly. Define abbreviations at first mention in the section (`electrical contact resistance (ECR)`, `scanning electron microscopy (SEM)`).
2. **Numbers, Units & Equations (`R10`)**: Preserve every number, range, citation `[CIT]`, figure reference `[FIG n]`, and equation `[EQ]` with **zero modification** (verified by `scripts/fidelity_check.py --mode translate`). Always leave a space between value and unit (`10 mA`, `25 °C`, `50 μm`).
3. **Grammar & Anti-AI Hygiene (`R09`, `R12`)**: Never emit any word from the 59 banned AI clichés (`delve`, `underscore`, `pivotal`, `elucidate`, `interplay`, `leverage`, `utilize`, `herein`, `framework`, etc.) and never emit `FIX_ERROR` constructions (`are resulted from`, `results into`, `our new designed`, `Regarding to`, `relevant with`, `same with`, `inversely proportion to`).
4. **No Hallucinated Claims**: Do not add physical explanations, qualifiers, or literature comparisons absent from the Chinese source; if a source phrase is ambiguous, flag it in the translation report table.

---

## Part VI — Section Playbooks

### Playbook: `abstract`

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

### Playbook: `introduction`

# Playbook: `introduction`

## Functions
- `background` — Engineering application context, reliability bottleneck (`weak link`), and classical contact physics/theory baseline (Holm `[EQ]`).
- `prior_work` — Literature review organized as chronological/thematic `<Author> et al. [CIT] <past verb> ... and <past verb> that ...` chains.
- `gap` — Pivot with `However,` highlighting unexamined operating conditions, coupled processes, or coating/geometry effects (`are very limited` / `little is known`).
- `this_paper` — Final roadmap paragraph opening with `In this paper,` or `This paper first presents...` and closing with `explicitly`.

## Quantitative Targets (S+A Train Weighted)
- **Paragraph length**: **97 words** median (IQR: `64–140` words), **4 sentences** per paragraph (`5–9` paragraphs total for a full Introduction).
- **Sentence length**: Median **23 words** (IQR: `16–28` words, P90: `36` words; lint range P50 `15–30`, P90 `22–44`).
- **Voice & pronouns**: **39.3%** passive sentences (lint range `0.15–0.70`); low `we` (`0.81 / 1,000w`).
- **Tense mix**: **50.2%** Present (`background` & `this_paper`), **43.9%** Past (`prior_work`), **5.9%** Present Perfect (highest in corpus: `has been extensively investigated`, `have shown`).
- **Top connectives**: `However,` (`5.74 / 100 sents`), `Therefore,` (`3.01`), `Finally,` (`2.28`), `In this paper,` (`1.82`), `In addition,` (`1.64`), `Then,` (`1.28`), `Next,` (`1.00`).

## Move Order
1. **Move 1 (`background`) — Engineering Application & Reliability Bottleneck (1–2 paragraphs)**
   - Establish widespread use of relays/connectors/contacts and identify contact failure (`fretting`, `contact welding`, `contact resistance`) as a weak link.
   - *Evidence*: `"In terms of reliability, metal contacts present in electrical connectors often represent a weak link in the whole system..."` (`P01`)
2. **Move 2 (`background`) — Classical Theory or Material Baseline (1 paragraph)**
   - Introduce the governing physical definition or classical Holm/Sharvin/Kohlrausch equation `[EQ]` with `where` variable definitions, or contrast noble (Au) vs non-noble (Sn) coatings.
   - *Evidence*: `"Holm [CIT] has shown that the constriction resistance of a single circular a-spot in a bulk interface..."` (`P13`)
3. **Move 3 (`prior_work`) — Thematic Literature Survey (1–3 paragraphs)**
   - Open with a factor-listing sentence (`Many factors influence..., such as... [CIT]`), then chain 3–5 concrete author-verb sentences reporting exact experimental ranges and findings.
   - *Evidence*: `"Park et al. [CIT] examined the effect of current load under 1–3 A and observed that..."` (`P01`)
4. **Move 4 (`gap`) — Research Gap Statement (2–4 sentences, either closing `prior_work` or opening the final paragraph)**
   - Pivot with `However,`; point out that studies on the specific combined condition or physical mechanism are `very limited` or `remain absent`.
   - *Evidence*: `"However, studies on the nature of electrical conduction through fretted contacts... are very limited."` (`P01`)
5. **Move 5 (`this_paper`) — Scope & Stepwise Roadmap of This Paper (1 paragraph, 3–5 sentences)**
   - State the objective (`In this paper, ... is investigated...`) and walk through the paper's steps (`firstly... then... next... finally...`) using passive voice and closing with `explicitly`.
   - *Evidence*: `"Next, the effects of contact radius, electrical conductivity, and coating thickness... are addressed explicitly."` (`P13`)

## Sentence Frames (Slot Templates)
1. `With the increasing application of <system> in <industry>, more and more electromechanical devices with metal contacts, including <connectors, relays, and switches>, are used in <systems>.`
2. `The electrical contact resistance across an interface between two conductors is an important quantity in many electromechanical device measurements and design [CIT].`
3. `<Phenomenon>, which occurs at the interface of contacting metal materials subjected to <stimulus>, is caused by <micro-process> between contacting surfaces [CIT].`
4. `Holm [CIT] has shown that the constriction resistance of a single circular a-spot in a bulk interface can be expressed as [EQ] where <sym1> and <sym2> are <def1> and <def2>, respectively.`
5. `Many factors influence the <property> of contacts, such as <factor 1>, <factor 2>, <factor 3>, and <factor 4> [CIT].`
6. `<Author> et al. [CIT] investigated/examined the effect of <parameter> under <numeric range> and found/observed/concluded that <specific finding>.`
7. `However, studies on the nature of <process> and the influence of <parameter> on <failure mode> are very limited.`
8. `Relatively little is known about the <mechanism> of <material> used in <parameter> over the range of <A–B>.`
9. `In this paper, an attempt is made to explore the effect of various <parameters> on the change of <metric> of <contacts> by introducing our newly designed test rig.`
10. `This paper first presents a universal mathematical model of <contact> for <analysis>, and then the corresponding finite-element method (FEM) simulation model is built for comparison. Next, the effects of <parameters> on <target> are addressed explicitly.`

## Guardrails & Tier-S Precedence
- In `prior_work`, always report what each cited author **actually varied or measured** (e.g., `under 10 and 100 mA`, `in the frequency range of 1–100 Hz`), rather than vague summaries.
- In `this_paper`, follow Tier S (`P01`, `P03`, `P13`) by using passive constructions (`is investigated`, `is built`, `are analyzed`, `are addressed explicitly`) rather than `"In this paper, we..."`.

### Playbook: `experimental`

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

### Playbook: `modeling`

# Playbook: `modeling`

## Functions
- `model_setup` — Idealized contact geometry, coordinate system, symmetry assumptions, and finite-element (COMSOL) mesh/boundary setup.
- `derivation` — Governing differential/integral equations (`[EQ]`), boundary conditions, `where` symbol definitions, and analytical resistance/force derivation.
- `validation` — Comparison of analytical predictions with classical Holm/Hertz theory, FEM simulations, or experimental benchmark data.

## Quantitative Targets (S+A Train Weighted)
- **Paragraph length**: **127 words** median (IQR: `44–198` words), **5 sentences** per paragraph.
- **Sentence length**: Median **21 words** (IQR: `16–28` words, P90: `39` words; lint range P50 `14–30`, P90 `21–46`).
- **Voice & pronouns**: **50.2%** passive sentences (lint range `0.20–0.80`), combined with the **highest active `we` rate in the corpus (`2.27 / 1,000w`)**: `"We consider..."`, `"we set..."`, `"For simplicity, we define..."`.
- **Tense mix**: **75.9%** Present / **23.7%** Past / **0.4%** Present Perfect; `4.56` `It is <VBN> that` per 100 sentences.
- **Top connectives**: `Thus,` (`3.65 / 100 sents`), `Therefore,` (`1.82`), `Then,` (`1.82`), `As shown in [FIG n],` (`1.82`), `Furthermore,` (`1.52`), `For simplicity,` (`0.91`).

## Move Order
1. **Move 1 (`model_setup`) — Geometric Configuration & Symmetry Assumptions (1–2 paragraphs)**
   - Reference the schematic `[FIG n]`, define radii/thicknesses ($r_0, r_1, h, a$), and state symmetry assumptions using active `we` (`We consider the simple situation of...`).
   - *Evidence*: `"The system of interest and associated boundary conditions are described in relation to [FIG 2]."` (`P13`)
2. **Move 2 (`derivation`) — Governing Equation & Boundary Conditions (1–2 paragraphs)**
   - State the governing Laplace/heat/elastic equation `[EQ]`, list boundary conditions `as follows: [EQ]`, and define all symbols in a `where ... respectively` clause.
   - *Evidence*: `"The boundary conditions are taken as follows: [EQ] where ρ1 is the electrical resistivity of the substrate..."` (`P13`)
3. **Move 3 (`derivation`) — Dimensionless Ratios & Analytical Solution (1–3 paragraphs)**
   - Introduce dimensionless groups (`For simplicity, we define g = ρ1/ρ2...`), substitute boundary conditions (`Combining (3)–(5) yields [EQ]`), and decompose total resistance into spreading, transition, and bulk terms.
   - *Evidence*: `"For simplicity, we define g = ρ1/ρ2 and (∂V2/∂r)|r=r0 = f(θ)."` (`P13`)
4. **Move 4 (`model_setup` / `validation`) — FEM Simulation Setup & Validation (1–2 paragraphs)**
   - Specify COMSOL Multiphysics version, 2D axisymmetric / 3D geometry, radial mesh grading toward the contact constriction (`[FIG n]`), minimum mesh element size, and electrical/thermal boundary conditions; compare analytical vs FEM/Holm curves.
   - *Evidence*: `"The meshes, presented in [FIG 3], are graded radially outward from the initial point of contact..."` (`P13`)

## Sentence Frames (Slot Templates)
1. `The system of interest and associated size/boundary parameters are described schematically in relation to [FIG n].`
2. `We consider the simple situation of a <hemispherical/cambered> conductor of radius <r1> surrounded by a metal film of thickness <h>.`
3. `Assuming electrical current passes through the circular constriction of contact radius <a>, as shown in [FIG n], the model is symmetric about <axis>.`
4. `The equation describing the distribution of the electrical potential within the contact is [EQ].`
5. `The boundary conditions are taken as follows: [EQ] where <ρ1> and <ρ2> are the electrical resistivities of the substrate and coating, respectively.`
6. `For simplicity, we define <g = ρ1/ρ2> and normalize the contact resistance by the classical Holm constriction resistance.`
7. `Similar to the known distribution of electrical current in a semi-infinite solid [CIT], the current density distribution within the constriction is assumed as [EQ].`
8. `Substituting <Eq. A> into <Eq. B>, the total contact resistance between <surface A> and <surface B> can be expressed as [EQ].`
9. `To visualize the isopotential and electrical current line distributions, the commercial program COMSOL Multiphysics is used to perform simulations by solving electric field equations through FEM.`
10. `The meshes, presented in [FIG n], are graded radially outward from the initial point of contact, with the densest mesh in the contact region (minimal mesh size of <X> μm).`
11. `Electrically, a prescribed constant voltage of <V> is applied to the top-most surface, the bottom-most surface is electrically grounded, and the lateral surfaces are considered electrically insulated.`

## Guardrails & Tier-S Precedence
- Always follow `[EQ]` immediately with a lower-case `where <symbol> is ...` clause when new symbols appear in the equation.
- Keep algebraic derivations connected with explicit logical bridges (`Thus,`, `Therefore,`, `Then,`, `Furthermore,`, `Combining (X) and (Y) yields`).

### Playbook: `results`

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

### Playbook: `mechanism`

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

### Playbook: `conclusion`

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

---

## Part VII — Public Golden Examples (Open-Access `P22` + Synthetic)

### Example: `abstract/full_01.md`

---
section: abstract
function: full
source: synthetic
moves: [M1_method_framed_object, M2_parameter_matrix, M3_key_empirical_findings, M4_theoretical_significance]
rules: [R01, R03, R07, R13, R14, R15]
notes: "Fictitious study on rotational micro-slip fretting of PdNi-plated copper alloy connectors; demonstrates Move 1 passive method opening, Move 2 parameter sweep, Move 3 quantitative findings, and Move 4 practical implication."
---

The electrical contact resistance and tribological degradation of palladium-nickel-coated beryllium bronze contacts under rotational micro-slip are investigated by using a custom-built torsional fretting apparatus. The effects of angular slip amplitude, normal spring load, and direct current level on contact resistance stability and wear track morphology are evaluated over a wide range of operating conditions. Experimental results indicate that the evolution of contact resistance can be divided into three distinct stages: the initial running-in stage, the low-fluctuation plateau stage, and the rapid degradation stage. The threshold number of cycles prior to contact failure decreases markedly when the angular slip amplitude exceeds 0.35 deg, whereas increasing the normal load from 1.5 N to 6.0 N prolongs the electrical endurance by suppressing interfacial oxide accumulation. Furthermore, energy-dispersive X-ray analysis confirms that substrate copper diffusion and frictional oxidation dominate the sudden rise in contact resistance. These findings provide a quantitative reference for the anti-fretting design of rotary aerospace connectors.

### Example: `abstract/full_02_oa.md`

---
section: abstract
function: full
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
tier: A
para_idx: "0"
words: 77
rules: [R01, R03, R07, R13, R14, R15]
---

The electrical contact resistance of cambered surface contact is systematically studied by analytical solution and finite-element simulation. Two representative cambered surface contacts, namely sphere-plane contact and cylinder-plane contact are built and the distributions of electrical current lines profile and isopotential are compared explicitly. Subsequently, the effects of size parameters of cambered surface and mechanical load on contact resistance are evaluated over a large range of aspect ratios. Furthermore, dissimilarity between sphere-plane contact and cylinder-plane contact is deduced.

### Example: `conclusion/numbered_01.md`

---
section: conclusion
function: numbered
source: synthetic
moves: [M1_scope_and_methodology_recap, M2_numbered_or_transition_linked_findings]
rules: [R01, R05, R31, R32, R33]
notes: "Fictitious numbered conclusion for the rotational micro-slip study; demonstrates scope recap, (1)-(4) numbered findings, zero citations/figure pointers, and restrained closure."
---

The electrical contact resistance behavior and interfacial wear mechanism of gold-flashed palladium-nickel-coated beryllium bronze contacts under rotational micro-slip have been experimentally investigated and analyzed. Based on the experimental results and physical modeling, the main conclusions can be summarized as follows: (1) Under rotational micro-slip excitation, the evolution of electrical contact resistance with fretting cycles exhibits three distinct regimes: the initial running-in stage, the stable metallic-conduction plateau stage, and the rapid oxidation-induced degradation stage. (2) With the increase of angular slip amplitude from 0.15 deg to 0.80 deg, the contact interface transitions from partial torsional slip to gross rotational slip, and the threshold fretting lifetime decreases by more than 80%. Conversely, increasing the normal contact force from 1.5 N to 6.0 N enlarges the central stick zone radius and significantly delays contact failure. (3) Microstructural and elemental analyses confirm that wear-through of the noble PdNi coating initiates preferentially within the outer annular slip zone, where the linear radial velocity gradient is highest, before oxidized copper debris migrates inward toward the contact center. (4) Maintaining the angular oscillation amplitude below the critical partial-slip threshold of 0.25 deg and applying a normal load above 4.0 N are effective measures to prevent fretting corrosion failure in rotary aerospace connectors.

### Example: `conclusion/summary_01.md`

---
section: conclusion
function: summary
source: synthetic
moves: [M1_scope_and_methodology_recap, M2_numbered_or_transition_linked_findings, M3_practical_design_implication]
rules: [R01, R05, R07, R31, R32, R33]
notes: "Fictitious prose summary conclusion for the bilayer contact resistance modeling study; demonstrates 'This paper mainly aims to...', transition-linked findings ('Furthermore... Meanwhile...'), and practical design guidance."
---

This paper mainly aims to systematically investigate the electrical contact resistance of bilayer-coated spherical-planar contacts over a wide range of geometric aspect ratios and resistivity ratios. By solving the axisymmetric Laplace equation in cylindrical coordinates, explicit series expressions for the constriction resistance, the bilayer transition resistance, and the substrate bulk resistance are derived. The analytical calculations are compared with finite-element simulations performed in COMSOL Multiphysics software. The comparison results show that the analytical predictions agree well with the finite-element data, with a maximum relative deviation of 1.4%. Furthermore, when the normalized contact radius exceeds 0.15, the classical Holm formula significantly overestimates the constriction resistance because radial boundary confinement is neglected. Meanwhile, introducing a high-conductivity top flash over a harder intermediate barrier layer reduces the current density singularity near the contact edge. This reduction becomes particularly pronounced when the total coating thickness exceeds 20% of the contact spot radius. Consequently, the proposed dimensionless charts can be directly applied to select optimal coating thicknesses for high-reliability electrical contacts.

### Example: `conclusion/summary_02_oa.md`

---
section: conclusion
function: summary
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
tier: A
para_idx: "27"
words: 229
rules: [R01, R05, R07, R31, R32, R33]
---

This paper mainly aims to systematically investigate the similarity and difference between two typical cambered surface contacts, i.e. sphere-plane contact and cylinder-plane contact, under the elastic deformation based on the effects of size parameters and mechanical load on the contact resistance. Our results indicate that mechanical load is a sensitive parameter to contact resistance of sphere-plane contact. Meanwhile, the contact resistance of cylinder-plane contact is significantly affected by contact length. This difference is attributed to the fact that the specific conforming feature of cylinder-plane contact. The distributions of simulated constriction region show that the sphere-plane contact has a stronger current crowding ability. And the simplification of the Hertzian contact area for both sphere-and cylinder-plane contacts is limited with larger contact radius for a/r > 0.1. Furthermore, the conductive ability of non-conforming contact is determined by the feature of cambered surface and mechanical load comprehensively. And the superiority of cylinder-plane contact would be performed even under low mechanical load. This is a positive and beneficial conclusion in engineering applications for electrical contacts, especially for the determination of contact structure in the design process. And the dimensionless results of contact resistance could be instructive to the stable electrical contact for MEMS under smaller dimension and lower contact load. In future, the detailed works on the plastic deformation will be in schedule for comparison to the elastic deformation for different contact structures.

### Example: `experimental/procedure_01.md`

---
section: experimental
function: procedure
source: synthetic
moves: [M3_operating_conditions_and_4wire_protocol, M4_post_test_microstructural_characterization]
rules: [R01, R06, R10, R19, R20, R21]
notes: "Fictitious 4-wire measurement protocol and post-mortem SEM/EDX characterization; demonstrates 'By using the four-wire method...', uncertainty statement, Table 1 reference, and analytical instruments."
---

By using the four-wire Kelvin resistance measurement method (shown in [FIG 2]), the electrical contact resistance across the mated pair was continuously monitored as a function of torsional fretting cycles. A programmable constant-current source (Keithley 6220, USA) supplied a direct current load ranging from 20 mA to 200 mA, while the voltage drop across the contact interface was sampled by a nanovoltmeter (Keithley 2182A, USA) at a sampling frequency of 2 kHz. The measurement accuracies of the current source and the nanovoltmeter were ±0.1% and ±0.05%, respectively; thus, the overall uncertainty of the contact resistance measurement did not exceed 0.2%. All experiments were conducted in a temperature- and humidity-controlled cabinet maintained at 25 ± 1 °C and 55 ± 3% relative humidity. The detailed experimental parameters are listed in Table 1. Each test was run for up to 5 × 10^4 torsional cycles or terminated automatically once the contact resistance exceeded 1.0 Ω. After the endurance tests, the worn surface morphologies and three-dimensional wear depth profiles were examined by using a scanning electron microscope (Merlin Compact, Zeiss, Germany) and a laser confocal microscope. Energy-dispersive X-ray spectroscopy (EDX) area mapping and line scans were performed at an accelerating voltage of 15 kV to determine the elemental distribution across the annular wear region.

### Example: `experimental/specimen_01.md`

---
section: experimental
function: specimen
source: synthetic
moves: [M2_specimen_geometry_materials_and_surface_preparation]
rules: [R01, R10, R19, R21]
notes: "Fictitious duplex Au/PdNi-coated beryllium bronze contact specimen preparation; demonstrates geometry, coating thickness verification, roughness/hardness specs, and ultrasonic cleaning chain."
---

The mating contact pair consists of a hemispherical rider with a tip radius of 1.8 mm and a circular flat disk with a diameter of 12 mm. Both the rider and the flat disk were machined from C17200 beryllium bronze alloy. Prior to electroplating, the substrates were mechanically polished and barrel-plated with a 1.8 μm nickel underlayer. Subsequently, a 1.2 μm palladium-nickel (80 wt.% Pd–20 wt.% Ni) layer and a 0.15 μm hard gold top flash were deposited. After electroplating, the thickness of each layer was measured immediately by an X-ray fluorescence spectrometer (XAN250, Helmut Fischer, Germany). The initial surface roughness Ra of the coated flat disk was controlled below 0.12 μm over a central scan size of 100 μm × 100 μm, as evaluated by a laser confocal microscope (VK-X200, Keyence, Japan). The micro-hardness of the composite coating surface was approximately 245 HV (49 mN). Before each test, all specimens were degreased using acetone and anhydrous ethanol in an ultrasonic cleaner for 10 min, rinsed with deionized water, and dried in nitrogen. The rider and flat disk were then assembled in the fixture to form a hemisphere-on-disk point contact configuration.

### Example: `experimental/test_rig_01.md`

---
section: experimental
function: test_rig
source: synthetic
moves: [M1_test_rig_architecture_and_subsystems]
rules: [R01, R10, R19, R20]
notes: "Fictitious torsional fretting test rig description; demonstrates subsystem decomposition, closed-loop feedback description, and inline parenthetical transducer specs."
---

A schematic diagram of the custom-built torsional fretting test apparatus used in the present study is shown in [FIG 1]. The experimental system consists of four main functional modules: the rotary micro-displacement excitation unit, the normal dead-weight loading unit, the environmental chamber, and the real-time electrical and mechanical data acquisition unit. Controlled angular oscillations are generated by a closed-loop piezoelectric rotary stage (PI M-660, Physik Instrumente, Germany) with an angular resolution of 0.002 deg and an operating frequency range of 1–200 Hz. The rotary stage is bolted onto a rigid granite base to isolate external floor vibrations. A miniature reaction torque sensor (TFF400, Futek, USA, capacity 50 N·mm, accuracy ±0.2%) is mounted coaxially below the lower flat specimen holder to monitor the tangential friction torque throughout the test. Meanwhile, the upper hemispherical rider is fixed to a vertical precision guideway, and the normal contact load is applied through a calibrated dead-weight lever mechanism. An eddy-current angular displacement sensor is integrated into the rotary shaft to provide real-time feedback for closed-loop amplitude control.

### Example: `introduction/background_01.md`

---
section: introduction
function: background
source: synthetic
moves: [M1_engineering_importance_and_failure_context]
rules: [R01, R02, R08, R16, R17]
notes: "Fictitious background on separable high-speed backplane connectors in avionics racks; demonstrates domain anchor, component failure chain, and classic Holm textbook citation."
---

Separable pin-and-socket connectors are widely used in modular avionics racks to transmit low-voltage differential signals and DC power across printed circuit boards in airborne radar systems [CIT]. As the packaging density of airborne electronic equipment increases, these contact pairs experience multi-axis structural vibrations and ambient thermal cycling during flight missions [CIT]. Noble metal coatings such as hard gold or palladium-nickel alloys are routinely electroplated onto copper alloy substrates to prevent tarnishing. Nevertheless, micro-motion at the mating interface remains a critical weak link for long-term system reliability [CIT]. According to the classical theory established by Holm [CIT], electrical current transfers exclusively through discrete micro-asperity spots, known as a-spots, which causes current streamline constriction and constriction resistance. Once relative micro-slip occurs between the mating surfaces, wear debris generation and base metal oxidation progressively reduce the effective conducting area. Consequently, intermittent voltage drops or permanent open-circuit failures can occur in flight-critical control loops.

### Example: `introduction/background_02_oa.md`

---
section: introduction
function: background
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
tier: A
para_idx: "1"
words: 115
rules: [R01, R02, R08, R16, R17]
---

Electrical contact, namely a current transferring from one metal to another member through the interface, has always been an important part of the electro-mechanical devices, including but not limited to electromagnetic relays [CIT], automotive connectors [CIT], circuit-breakers [CIT], micro-electro-mechanical systems (MEMS) [CIT], thin-film devices [CIT], and switchgears [CIT]. The electrical current lines would be sharply distorted and bundle together to pass through the contact interface due to the limited contact region[CIT]. Thus, the additional resistance causing by the shrinking current lines is called constriction resistance, which is a main component of electrical contact resistance between mental contact pairs. Low and stable contact resistance is a fundamental requirement of any electrical and electronic engineering [CIT].

### Example: `introduction/gap_01.md`

---
section: introduction
function: gap
source: synthetic
moves: [M2_literature_review, M3_knowledge_gap_pivot]
rules: [R01, R06, R16, R17, R18]
notes: "Fictitious gap statement contrasting linear sinusoidal fretting with superimposed torsional micro-slip; demonstrates restrained 'However, relatively little is known...' pivot."
---

Previous investigations have provided valuable insights into the degradation mechanisms of coated electrical contacts under unidirectional linear fretting at constant frequency [CIT]. In actual aircraft harness assemblies, however, connector pins locked inside floating housings often experience small-angle torsional oscillations induced by cable harness twisting rather than pure translational sliding [CIT]. Under torsional excitation, the local slip amplitude varies linearly with radial distance from the contact center, which produces an annular micro-slip zone surrounding a central stick zone even at moderate angular displacements. However, relatively little is known about how radial slip gradients in torsional fretting affect the wear-through life of duplex palladium-nickel coatings and the subsequent transport of oxidized copper debris. Moreover, most existing analytical and empirical lifetime models were derived for uniform translational displacement fields and cannot directly predict the electrical contact resistance evolution when stick and slip zones coexist across a circular contact spot. Therefore, it is necessary to clarify the coupling between angular slip amplitude, normal force, and interfacial oxide distribution under rotational micro-slip conditions.

### Example: `introduction/prior_work_01.md`

---
section: introduction
function: prior_work
source: synthetic
moves: [M2_chronological_thematic_literature_review]
rules: [R01, R02, R11, R16, R17]
notes: "Fictitious literature review on ternary palladium alloy coatings and dual-frequency vibration testing; demonstrates author-led past-tense reporting verbs and mechanism contrast."
---

Over the past two decades, extensive experimental and numerical efforts have been devoted to clarifying the fretting corrosion behavior of noble-metal-coated electrical contacts. Antler and co-workers [CIT] systematically examined the sliding wear of electrodeposited palladium and gold-flashed palladium coatings, and concluded that frictional polymerization and loose wear debris govern the contact resistance stability under dry conditions. Subsequently, Fouvry et al. [CIT] introduced an dissipated-energy approach to quantify the transition between partial slip and gross slip regimes in noble metal coatings, demonstrating that coating endurance scales inversely with accumulated interfacial shear work. To improve wear resistance under elevated contact loads, duplex coatings consisting of a palladium-nickel intermediate layer and an ultrathin gold flash were developed and evaluated under linear reciprocating motion [CIT]. Furthermore, several investigators studied the influence of ambient relative humidity and current load on the oxidation rate of exposed copper substrates [CIT]. Their results revealed that Joule heating localized at constrictive a-spots accelerates oxide film growth once the protective noble layer is worn through.

### Example: `introduction/prior_work_02_oa.md`

---
section: introduction
function: prior_work
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
tier: A
para_idx: "5-6"
words: 265
rules: [R01, R02, R11, R16, R17]
---

In addition, the cambered surface contact also exactly exists between the rough surfaces. For the sake of simplicity, many researchers utilize the spherical contact to simulate the single asperity contact. Greenwood and Williamson [CIT] first presented the contact model for rough surfaces and assumed that all asperities whose heights conform to the Gaussian random distribution have identical curvature radius. And many meaningful works make the asperities equivalent to the spheres with different curvature radius to simulate accurately and analyze the contact situation [CIT]. However, there are not only spherical contact but also cylindrical contact in the real contact between rough surfaces according to other researches [CIT]. Therefore, it is necessary to investigate the effects of aspect ratios and mechanical load on spherical contact and cylindrical contact in the micro scale, which is also the basis of accurate equivalence for rough surface contact. In a previous paper by the present authors, variations in contact resistance as a function of contact load between rod and spring contacts are investigated explicitly [CIT]. There is also a remarkable transition stage from spherical contact to cylindrical contact before stable contact. And this could be attributed to the rough surfaces of contact pairs. If the problems mentioned above are solved, then the profile of asperities could be easily estimated in the contact process according to the relationship between contact resistance and contact load. In order to avoid the probable mixture of contact forms caused by the rough surfaces under low contact load, the theoretical solution and finite-element method are employed to further investigate the similarity and difference between cambered surface contacts.

### Example: `introduction/this_paper_01.md`

---
section: introduction
function: this_paper
source: synthetic
moves: [M4_objective_and_roadmap_of_this_paper]
rules: [R01, R03, R08, R16, R17]
notes: "Fictitious roadmap paragraph for a rotational fretting study; demonstrates 'In this paper...' opening, 'First... Subsequently... Finally...' sequence, and practical engineering closure."
---

In this paper, an attempt is made to systematically investigate the electrical contact resistance behavior and interfacial degradation mechanism of gold-flashed palladium-nickel coatings under controlled rotational micro-slip. First, a high-precision torsional fretting test apparatus equipped with a piezoelectric rotary actuator and a four-wire resistance measurement circuit is described in detail. Subsequently, the variations of contact resistance and friction torque with fretting cycles are measured under angular slip amplitudes from 0.10 deg to 0.80 deg and normal loads from 1.5 N to 6.0 N. Scanning electron microscopy (SEM), three-dimensional laser profilometry, and energy-dispersive X-ray spectroscopy (EDX) characterize the worn surface morphologies and elemental distributions across the annular wear tracks. Finally, we propose a physical degradation model that incorporates the radial slip gradient and interfacial debris transport to explain the transition from partial torsional slip to gross oxidation. The experimental results and physical model provide a practical basis for optimizing coating thickness in high-reliability rotary connectors.

### Example: `mechanism/explanation_01.md`

---
section: mechanism
function: explanation
source: synthetic
moves: [M1_macroscopic_phenomenon_restatement, M2_multi_stage_physical_model, M3_coupled_driving_forces, M4_theoretical_criterion_and_regime_boundary]
rules: [R01, R04, R05, R07, R28, R29, R30]
notes: "Fictitious 3-stage physical degradation model for annular torsional fretting corrosion; demonstrates schematic figure reference, stage-by-stage mechanism, Mindlin-type stick-slip criterion, and 'This may be attributed to...' causal hedging."
---

Based on the electrical contact resistance waveforms and post-test SEM/EDX observations, the interfacial degradation process of the duplex Au/PdNi coating under rotational micro-slip can be explained by a three-stage physical model, as illustrated in [FIG 10]. According to the Cattaneo–Mindlin tangential contact theory [CIT], when the applied torque T is below the limiting friction torque, the circular contact area splits into a central stick zone of radius c and an outer annular slip zone (c < r ≤ a). Within the outer annulus, the local slip amplitude increases linearly with the radial coordinate r. During Stage I ([FIG 10](a)), rotational micro-slip remains confined to the outer annulus. The thin gold flash is rapidly sheared off in this outer ring, whereas the central stick core maintains low-resistance metallic conduction. As cycling proceeds into Stage II ([FIG 10](b)), abrasive wear in the outer annulus penetrates the palladium-nickel layer and exposes the nickel underlayer and copper alloy substrate. Fine copper and nickel wear particles oxidize rapidly under frictional heating and form an insulating ring along the periphery. Consequently, current streamlines constrict toward the shrinking central stick zone. In Stage III ([FIG 10](c)), oxidized debris gradually migrates inward into the central core; this may be attributed to radial pumping under cyclic normal vibration. Once the insulating oxide film covers the central conducting a-spots, the contact resistance rises abruptly above 1.0 Ω.

### Example: `modeling/derivation_01.md`

---
section: modeling
function: derivation
source: synthetic
moves: [M2_governing_equations_boundary_conditions_and_dimensionless_groups]
rules: [R01, R04, R07, R22, R23]
notes: "Fictitious analytical derivation of potential distribution in a bilayer contact; demonstrates Laplace governing equation, boundary conditions, 'For simplicity, we define...' dimensionless groups, and component decomposition."
---

Under steady-state direct-current excitation, the electrostatic potential φi(r, z) in each conducting layer i (i = 1, 2, 3) satisfies the axisymmetric Laplace equation in cylindrical coordinates. The governing differential equation can be written as [EQ], where ρi denotes the electrical resistivity of layer i. At the metallurgical interfaces z = h1 and z = h1 + h2, both the electrical potential and the normal current density remain continuous. These physical requirements yield the interface continuity conditions [EQ]. Across the circular contact plane z = 0, the mixed boundary conditions are given by φ1(r, 0) = V0 for 0 ≤ r ≤ a and ∂φ1/∂z = 0 for a < r ≤ b. By applying the zero-order Hankel transform with respect to the radial coordinate r, the general solution of the potential in each layer can be expressed as [EQ]. Here, J0 denotes the zero-order Bessel function of the first kind, and Ak(ξ) and Bk(ξ) are layer coefficients determined by the boundary conditions. For simplicity, we define the normalized contact radius a* = a/b, the normalized coating thicknesses h1* = h1/a and h2* = h2/a, and the resistivity ratios κ1 = ρ1/ρ3 and κ2 = ρ2/ρ3. The total electrical contact resistance Rc can then be decomposed into three series components, namely the constriction resistance Rs, the bilayer transition resistance Rt, and the substrate bulk resistance Rb.

### Example: `modeling/derivation_02_oa.md`

---
section: modeling
function: derivation
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
tier: A
para_idx: "11-13"
words: 170
rules: [R01, R04, R07, R22, R23]
---

It is obvious that the electrical potential decreases sharply especially around the contact region for both two contact structural configurations, which means that the decreasing potential mainly concentrates around the interface. Then a local analysis is used to investigate the singularity in the partial derivative of voltage with respect to the vertical axis along the edge of contacts, which is arose due to the mixed boundary condition at (a, 0). To confirm that finite-element analysis captures the singularity behavior, log(∂V/∂z) against log[1/(a∗−x/r0)] with different normalized contact half-width a∗of 0.01, 0.1, 0.5 and 0.8 are plotted in [FIG 7]. When x/r0 is close to a∗from the negative direction, log(∂V/∂z) increases along the straight line asymptotically. This phenomenon conforms to the associated singularity behavior mentioned in Ref [CIT]. And this indicates that FEA correctly captures the singularity behavior at (a, 0). The normalized height is written by h∗= h/r to eliminate the influence of the curvature radius of cambered surface.

### Example: `modeling/model_setup_01.md`

---
section: modeling
function: model_setup
source: synthetic
moves: [M1_geometric_idealization_and_coordinate_setup, M3_fem_discretization_and_mesh_grading]
rules: [R01, R11, R22, R24]
notes: "Fictitious axisymmetric FEM setup for a bilayer-coated sphere-on-flat contact in COMSOL; demonstrates coordinate setup, boundary conditions, and graded mesh near singularity."
---

The system of interest and its geometric parameters are illustrated schematically in [FIG 1]. We consider an axisymmetric circular contact spot of radius a formed between a silver-alloy hemisphere of radius R and a flat copper substrate. The lower substrate carries a bilayer coating with layer thicknesses h1 and h2. Because the contact geometry and electric field distribution are rotationally symmetric about the vertical z-axis, the three-dimensional conduction problem reduces to a two-dimensional axisymmetric domain in cylindrical coordinates (r, z). To evaluate the constriction resistance and potential distribution over a wide range of coating thicknesses, a two-dimensional axisymmetric finite-element model is built in COMSOL Multiphysics software. In the simulation domain, the outer radial boundary at r = b is electrically insulated. Meanwhile, a uniform direct current I0 enters the top-most boundary of the upper hemisphere, and the bottom-most boundary of the lower substrate is electrically grounded (V = 0). The computational domain is meshed with six-node triangular elements. Furthermore, the mesh size is graded radially toward the contact edge (r = a) with a minimum element size of 2 × 10^-4 a to resolve the current density singularity accurately.

### Example: `modeling/model_setup_02_oa.md`

---
section: modeling
function: model_setup
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
tier: A
para_idx: "9b"
words: 178
rules: [R01, R11, R22, R24]
---

A series of mesh convergence studies are conducted and the maximal size of the mesh around the contact region is determined as 0.07µm. This means that the simulated contact resistance results are not affected with the size of the mesh further decreasing. And the contact surfaces are assumed smooth. Electrically, a prescribed constant current 10mA is applied to the top-most surface and the bottom-most surface is electrically grounded. Axis symmetry on the leftmost boundary results in electrical insulation. The lateral surfaces of both bodies are also considered electrically insulated. For better description, the Laplace equation and boundary conditions for sphere-plane and cylinder-plane contact are described with the cylindrical and Cartesian coordinates, respectively. The corresponding distribution of the potential ϕ for sphere-plane and cylinder-plane contact are written as [EQ] And the boundary conditions for sphere-plane and cylinder-plane contacts both could be described as follows [EQ] where the current density are J0 = I0/(πr2 0) and J0 = I0/(2r0L) for sphere-plane and cylinder-plane contacts, respectively, due to the circular and rectangular top-most surface.

### Example: `modeling/validation_01.md`

---
section: modeling
function: validation
source: synthetic
moves: [M4_analytical_fem_classical_theory_validation]
rules: [R01, R04, R08, R22, R24]
notes: "Fictitious model validation comparing analytical solution, COMSOL FEM, and classical Holm formula; demonstrates quantitative regime agreement and physical reason for divergence."
---

To verify the accuracy of the derived analytical solution, illustrative calculations of the normalized contact resistance Rc* = 2aRc/ρ3 as a function of the normalized contact radius a* are compared with the finite-element simulation results in [FIG 3]. The classical Holm formula is also plotted for reference. In the limiting case of an uncoated homogeneous contact (h1* = 0, κ1 = 1), the analytical expression is reduced to the classical single-spot constriction resistance formula Rc = (ρ1 + ρ3)/(4a) for small contact spots. As shown in [FIG 3], the analytical predictions agree well with the finite-element simulation data over the entire range of aspect ratios 0.01 ≤ a* ≤ 0.60. The maximum relative deviation between the two methods is less than 1.4%. Specifically, when a* ≤ 0.08, the analytical values, numerical results, and classical Holm curve practically coincide because the outer radial boundary has a negligible effect on current constriction near the a-spot. When a* exceeds 0.15, however, the contact resistance is increasingly overestimated by the classical Holm theory. By contrast, both the analytical model and the finite-element simulation capture the monotonic decrease of Rc* caused by radial boundary confinement, which confirms the validity of the analytical formulation.

### Example: `modeling/validation_02_oa.md`

---
section: modeling
function: validation
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
tier: A
para_idx: "10"
words: 243
rules: [R01, R04, R08, R22, R24]
---

The simulation results of isopotential maps and electrical current lines profile at 10mA electrical current load are shown in [FIG 4] and [FIG 5] for sphere-plane contact and cylinder-plane contact, respectively. As expected, the current lines are orthogonal to the potential lines and shrink uniformly radially toward the contact region. And the distribution of current lines are densest around the vicinity of the contact region. It is necessary to investigate the electrical potential distribution on the top-most surface in order to illustrate whether the half-sphere with limited height of r0 = 1mm in finite-element model has influence on the constriction of current lines. The height h is defined as the vertical distance from the horizontal line to the contact region. And the potential distribution on the horizontal lines with different heights from 0.5mm to 1mm are shown in [FIG 6]. It is noted that the electrical potential increases significantly from 8.25 µ V to 8.275 µ V along the horizontal line away from the vertical z-axis for h = 0.5mm. And the variations of electrical potential becomes smaller with the height h increasing until all potential are equal for h = 1mm corresponding to the top-most surface. This means that the top-most surface is an isopotential surface even under limited height. For better description, the isopotential lines corresponding to 90%U, 75%U, 50%U, 25%U and 10%U are drawn in [FIG 4] and [FIG 5], where U is the electrical potential of the top-most surface.

### Example: `results/surface_analysis_01.md`

---
section: results
function: surface_analysis
source: synthetic
moves: [M1_figure_pointer, M4_microstructural_and_elemental_evidence]
rules: [R01, R05, R07, R25, R27]
notes: "Fictitious SEM morphology and EDX elemental analysis of an annular torsional fretting scar; demonstrates central stick vs peripheral slip zone morphology and atomic-percent EDX evidence."
---

In order to clarify the physical origin of the contact resistance degradation in Stage III, the worn surface morphologies and EDX elemental profiles of the flat specimen after 1.5 × 10^4 cycles at θ = 0.45 deg and Fn = 2.5 N are shown in [FIG 8]. It can be clearly observed from the SEM micrograph in [FIG 8](a) that the circular contact scar has an outer diameter of approximately 165 μm. The worn surface exhibits a concentric ring structure. Specifically, a smooth central region (Region I, radius ~38 μm) is surrounded by a severely ploughed annular peripheral zone (Region II). Loose lamellar wear debris and dark oxide compacts are accumulated along the outer rim of Region II. As shown by the radial EDX line scan in [FIG 8](b), the atomic percentages of Pd and Au remain high (46.2 at.% Pd and 8.4 at.% Au) inside the central stick region. Meanwhile, oxygen and copper signals are barely detectable in Region I. Within the annular micro-slip zone (Region II), however, the Pd content drops below 7.5 at.%, whereas the atomic percentages of Cu, Ni, and O rise sharply to 38.6 at.%, 14.8 at.%, and 34.1 at.%, respectively. This elemental distribution indicates that both the gold flash and the palladium-nickel layer are worn through in the outer annulus, exposing the nickel barrier and copper alloy substrate to tribochemical oxidation.

### Example: `results/trend_01.md`

---
section: results
function: trend
source: synthetic
moves: [M1_figure_pointer_and_experimental_condition_anchor, M3_quantitative_contrast_across_parameters]
rules: [R01, R04, R05, R06, R25, R26, R27]
notes: "Fictitious parametric trend of electrical endurance cycles versus angular slip amplitude and normal load; demonstrates 'as a function of', 'With the increase of...', quantitative regimes, and 'That is to say' restatement."
---

The variations of the threshold fretting cycles Nf as a function of angular slip amplitude θ under different normal loads are presented in [FIG 6]. Here, Nf is defined as the cycle number at which the contact resistance first reaches 0.1 Ω. With the increase of the angular slip amplitude from 0.15 deg to 0.80 deg, the threshold fretting lifetime decreases monotonically for all four normal load levels. However, the rate of decrease depends strongly on the operating slip regime. Specifically, when the angular slip amplitude is below 0.25 deg, the contact interface operates within the partial torsional slip regime. In this regime, the contact resistance remains below 15 mΩ even after 5 × 10^4 cycles at a normal load of 4.0 N. As the angular slip amplitude increases from 0.30 deg to 0.65 deg, Nf drops sharply from 3.4 × 10^4 cycles to 6.8 × 10^3 cycles under a normal load of 2.0 N, which corresponds to a reduction of nearly 80%. By contrast, when the normal load is increased from 1.5 N to 6.0 N at a fixed slip amplitude of 0.50 deg, the threshold lifetime is extended from 4.9 × 10^3 cycles to 1.95 × 10^4 cycles. That is to say, a higher normal contact force enlarges the central stick zone radius and retards the inward propagation of the annular oxidation front.

### Example: `results/trend_02_oa.md`

---
section: results
function: trend
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
tier: A
para_idx: "23-24"
words: 200
rules: [R01, R04, R05, R06, R25, R26, R27]
---

The height distributions of various isopotential with 90%U, 75%U, 50%U, 25%U and 10%U with varied curvature radius r/L from 0.1 to 10 for sphere-plane contact and with varied normalized curvature radius of cambered surface r/L = 0.1, 1 and 10. cylinder-plane contact are shown in [FIG 17]. The normalized height h∗and the relative height of the constriction region 1h∗both decrease significantly with the normalized curvature radius increasing. For the fixed isopotential, the parameters h∗and 1h∗of sphere-plane contact are always lower than that of cylinder-plane contact, which indicates that the isopotential distribution of former is closer to the contact a-spot than the latter. So the crowding ability for electrical current of cylinder-plane is weaker than that of sphere-plane contact, and there would be a lower potential difference for cylinder-plane contact corresponding to a smaller contact resistance. However, the potential decreases significantly for cylinder-plane contact along the arc profile of cylinder, which causes a larger bulk resistance. And the bulk resistance would increase with the curvature radius of cylinder increasing. This is the root reason for a larger resistance for cylinder-plane contact with the curvature radius increasing than that of sphere-plane contact.

### Example: `results/waveform_01.md`

---
section: results
function: waveform
source: synthetic
moves: [M1_figure_pointer_and_experimental_condition_anchor, M2_multi_stage_or_regime_partition, M3_quantitative_contrast_across_parameters]
rules: [R01, R04, R06, R25, R26, R27]
notes: "Fictitious transient voltage and contact resistance waveform analysis during torsional fretting; demonstrates '[FIG 4] shows the typical waveforms...', Point A/B/C chronological walk-through, and quantitative cycle thresholds."
---

[FIG 4] shows the typical evolution of the electrical contact resistance and tangential friction torque as a function of torsional fretting cycles at an angular slip amplitude of 0.45 deg and a normal load of 2.5 N. As can be seen from [FIG 4], the variation curve of contact resistance over the entire test can be divided into three distinct stages: the initial running-in stage (Stage I), the stable low-resistance plateau stage (Stage II), and the rapid degradation stage (Stage III). At the beginning of the test (Point A, N = 1 cycle), the initial contact resistance is approximately 6.8 mΩ due to a thin adventitious film on the gold flash. Within the first 400 cycles (Stage I), the contact resistance drops slightly to 5.4 mΩ (Point B) as the superficial film is disrupted by micro-slip. Meanwhile, the friction torque increases from 4.2 N·mm to 6.5 N·mm. During Stage II (from 400 to 1.15 × 10^4 cycles), the contact resistance remains stable between 5.2 mΩ and 6.1 mΩ because metallic conduction is maintained by the palladium-nickel layer. Once the cycle count reaches Point C (1.18 × 10^4 cycles), however, sharp resistance spikes exceeding 180 mΩ appear intermittently. Finally, the contact resistance rises above the 1.0 Ω failure threshold at 1.42 × 10^4 cycles.

---

## Part VIII — Contrastive Pairs (`AI-default` vs `Ren`)

### Contrastive Pair: `pair_01_abstract.md`

---
section: abstract
function: full
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
rules: [R01, R03, R07, R13, R14, R15]
---

### AI-default

Understanding the electrical contact resistance of cambered surface contacts is crucial for ensuring reliable power and signal transmission across mechanical interfaces. In this study, we comprehensively explore the contact resistance behavior of cambered surfaces by leveraging both analytical modeling and finite-element simulations. Specifically, two representative configurations—sphere-plane contact and cylinder-plane contact—are established to elucidate the underlying current streamline and isopotential distributions. Furthermore, we systematically assess the interplay between geometric curvature parameters and mechanical load across a broad spectrum of aspect ratios. Ultimately, these findings shed light on the fundamental divergence between spherical and cylindrical contact geometries.

### Ren

The electrical contact resistance of cambered surface contact is systematically studied by analytical solution and finite-element simulation. Two representative cambered surface contacts, namely sphere-plane contact and cylinder-plane contact are built and the distributions of electrical current lines profile and isopotential are compared explicitly. Subsequently, the effects of size parameters of cambered surface and mechanical load on contact resistance are evaluated over a large range of aspect ratios. Furthermore, dissimilarity between sphere-plane contact and cylinder-plane contact is deduced.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `Understanding the electrical contact resistance ... is crucial for ensuring...` | `The electrical contact resistance of cambered surface contact is systematically studied by...` | `R03`, `R13`, `F25` | Ren opens Abstracts directly with the object of study and method in passive voice (`The <phenomenon> is studied by...`), never with a generic "Understanding X is crucial" hook. |
| `we comprehensively explore ... by leveraging` | `is systematically studied by analytical solution and finite-element simulation` | `R14`, `F17` | Avoids `we` in Abstracts (`R14`) and replaces AI buzzwords (`explore`, `leveraging`) with plain physical method nouns. |
| `two representative configurations—sphere-plane contact and cylinder-plane contact—are established to elucidate` | `Two representative cambered surface contacts, namely sphere-plane contact and cylinder-plane contact are built` | `R07`, `R22`, `F17` | Uses `, namely` for apposition (`R07`) instead of em-dashes, `are built` (`R22`) instead of `are established`, and avoids `elucidate` (`F17`). |
| `assess the interplay between ... across a broad spectrum of aspect ratios` | `the effects of ... are evaluated over a large range of aspect ratios` | `R13`, `F17` | Uses Ren's signature parameter-sweep template (`the effects of X, Y, and Z on W are evaluated over a large range of aspect ratios`). |
| `Ultimately, these findings shed light on the fundamental divergence` | `Furthermore, dissimilarity between ... is deduced.` | `R05`, `R15`, `F17` | Closes on a direct, uninflated statement of the deduced result without promotional meta-commentary (`shed light on`). |

### Contrastive Pair: `pair_02_introduction_gap.md`

---
section: introduction
function: gap
source: synthetic
rules: [R01, R06, R16, R17, R18]
---

### AI-default

While prior studies have yielded pivotal insights into the fretting degradation of coated electrical contacts under simple unidirectional vibration [CIT], real-world aerospace wiring harnesses present a far more intricate mechanical environment [CIT]. Specifically, connector pins housed within floating cavities frequently undergo complex small-angle torsional oscillations driven by cable bundle twisting, which fundamentally alters the interfacial kinematics by creating a radial slip gradient. Despite its critical practical importance, there remains a glaring gap in our comprehensive understanding of how radial slip gradients govern the wear-through durability of duplex palladium-nickel coatings. Furthermore, existing theoretical frameworks are predominantly tailored to uniform linear displacement fields and fail to capture the intricate interplay between coexisting stick and slip zones. Consequently, bridging this knowledge gap is imperative for advancing connector reliability.

### Ren

Previous investigations have provided valuable insights into the degradation mechanisms of coated electrical contacts under unidirectional linear fretting at constant frequency [CIT]. In actual aircraft harness assemblies, however, connector pins locked inside floating housings often experience small-angle torsional oscillations induced by cable harness twisting rather than pure translational sliding [CIT]. Under torsional excitation, the local slip amplitude varies linearly with radial distance from the contact center, which produces an annular micro-slip zone surrounding a central stick zone even at moderate angular displacements. However, relatively little is known about how radial slip gradients in torsional fretting affect the wear-through life of duplex palladium-nickel coatings and the subsequent transport of oxidized copper debris. Moreover, most existing analytical and empirical lifetime models were derived for uniform translational displacement fields and cannot directly predict the electrical contact resistance evolution when stick and slip zones coexist across a circular contact spot. Therefore, it is necessary to clarify the coupling between angular slip amplitude, normal force, and interfacial oxide distribution under rotational micro-slip conditions.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `yielded pivotal insights ... far more intricate mechanical environment` | `provided valuable insights ... actual aircraft harness assemblies` | `R12`, `F17`, `F26` | Replaces promotional intensifiers (`pivotal`, `far more intricate`) with concrete engineering hardware descriptions. |
| `Despite its critical practical importance, there remains a glaring gap in our comprehensive understanding of` | `However, relatively little is known about` | `R06`, `R18`, `F27` | Uses Ren's restrained gap pivot (`However, relatively little is known about...`) rather than dramatic "glaring gap" rhetoric. |
| `existing theoretical frameworks are predominantly tailored to ... and fail to capture the intricate interplay` | `most existing analytical and empirical lifetime models were derived for ... and cannot directly predict` | `R16`, `F17` | Avoids banned words (`framework`, `intricate`, `interplay`) and states the exact mathematical limitation of prior models. |
| `bridging this knowledge gap is imperative for advancing` | `Therefore, it is necessary to clarify the coupling between` | `R05`, `R08`, `F17` | Uses `Therefore, it is necessary to clarify...` (`R05`, `R08`) instead of AI cliché `imperative for advancing`. |

### Contrastive Pair: `pair_03_experimental_procedure.md`

---
section: experimental
function: procedure
source: synthetic
rules: [R01, R06, R10, R19, R20, R21]
---

### AI-default

To accurately track the evolution of electrical contact resistance throughout the torsional fretting tests, we employed a high-precision four-wire Kelvin sensing configuration, as depicted in [FIG 2]. A programmable Keithley 6220 current source was utilized to inject a stable DC current between 20 mA and 200 mA, while a Keithley 2182A nanovoltmeter captured the resulting interfacial voltage drop at a 2 kHz rate. Given the exceptional instrument tolerances of ±0.1% and ±0.05%, the overall measurement uncertainty was successfully constrained below 0.2%. All trials were executed inside an environmental chamber regulated at 25 ± 1 °C and 55 ± 3% RH, with full operating parameters summarized in Table 1. Following test termination at 5 × 10^4 cycles or 1.0 Ω, comprehensive post-mortem surface characterization was conducted by leveraging Zeiss SEM imaging, laser confocal profilometry, and 15 kV EDX elemental mapping to unravel the wear track chemistry.

### Ren

By using the four-wire Kelvin resistance measurement method (shown in [FIG 2]), the electrical contact resistance across the mated pair was continuously monitored as a function of torsional fretting cycles. A programmable constant-current source (Keithley 6220, USA) supplied a direct current load ranging from 20 mA to 200 mA, while the voltage drop across the contact interface was sampled by a nanovoltmeter (Keithley 2182A, USA) at a sampling frequency of 2 kHz. The measurement accuracies of the current source and the nanovoltmeter were ±0.1% and ±0.05%, respectively; thus, the overall uncertainty of the contact resistance measurement did not exceed 0.2%. All experiments were conducted in a temperature- and humidity-controlled cabinet maintained at 25 ± 1 °C and 55 ± 3% relative humidity. The detailed experimental parameters are listed in Table 1. Each test was run for up to 5 × 10^4 torsional cycles or terminated automatically once the contact resistance exceeded 1.0 Ω. After the endurance tests, the worn surface morphologies and three-dimensional wear depth profiles were examined by using a scanning electron microscope (Merlin Compact, Zeiss, Germany) and a laser confocal microscope. Energy-dispersive X-ray spectroscopy (EDX) area mapping and line scans were performed at an accelerating voltage of 15 kV to determine the elemental distribution across the annular wear region.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `To accurately track ... we employed a high-precision four-wire Kelvin sensing configuration` | `By using the four-wire Kelvin resistance measurement method (shown in [FIG 2]), the electrical contact resistance ... was continuously monitored as a function of` | `R06`, `R10`, `R19`, `R20` | Uses Ren's signature experimental opener (`By using the four-wire method (shown in [FIG N]), the contact resistance was continuously measured/monitored as a function of...`) in passive voice. |
| `a programmable Keithley 6220 current source was utilized` | `A programmable constant-current source (Keithley 6220, USA) supplied` | `R20`, `F17` | Formats instrument specifications in inline parentheses `(Model, Manufacturer, Country)` (`R20`) and avoids `utilized` (`F17`). |
| `Given the exceptional instrument tolerances ... was successfully constrained` | `The measurement accuracies ... were ±0.1% and ±0.05%, respectively; thus, the overall uncertainty ... did not exceed 0.2%.` | `R12`, `R20`, `F26` | States instrument accuracy and deduced measurement uncertainty without evaluative adjectives (`exceptional`, `successfully`). |
| `by leveraging Zeiss SEM imaging ... to unravel` | `were examined by using a scanning electron microscope (Merlin Compact, Zeiss, Germany) ... to determine` | `R10`, `R20`, `F17` | Uses instrument-passive (`were examined by using...`) and plain verbs (`determine`) instead of `leveraging` and `unravel`. |

### Contrastive Pair: `pair_04_modeling_validation.md`

---
section: modeling
function: validation
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
rules: [R01, R04, R08, R22, R24]
---

### AI-default

[FIG 4] and [FIG 5] illustrate the simulated isopotential contours and electric current streamline distributions under a 10 mA excitation for the sphere-plane and cylinder-plane contact configurations, respectively. Consistent with theoretical expectations, the current streamlines remain strictly orthogonal to the equipotential surfaces while converging radially toward the constriction zone, where the current density peaks sharply. To rigorously validate whether the finite hemisphere height of r0 = 1 mm in our finite-element setup introduces artificial boundary distortions, we examine the potential profile along the upper boundary. Specifically, [FIG 6] plots the potential variations across horizontal planes at elevations h ranging from 0.5 mm to 1.0 mm above the contact interface. At h = 0.5 mm, a noticeable radial potential gradient from 8.25 µV to 8.275 µV is observed; however, this variation progressively diminishes with increasing elevation until the potential becomes completely uniform at the top surface (h = 1 mm). This confirms that the upper boundary behaves as a true equipotential surface despite the truncated domain height.

### Ren

The simulation results of isopotential maps and electrical current lines profile at 10mA electrical current load are shown in [FIG 4] and [FIG 5] for sphere-plane contact and cylinder-plane contact, respectively. As expected, the current lines are orthogonal to the potential lines and shrink uniformly radially toward the contact region. And the distribution of current lines are densest around the vicinity of the contact region. It is necessary to investigate the electrical potential distribution on the top-most surface in order to illustrate whether the half-sphere with limited height of r0 = 1mm in finite-element model has influence on the constriction of current lines. The height h is defined as the vertical distance from the horizontal line to the contact region. And the potential distribution on the horizontal lines with different heights from 0.5mm to 1mm are shown in [FIG 6]. It is noted that the electrical potential increases significantly from 8.25 µ V to 8.275 µ V along the horizontal line away from the vertical z-axis for h = 0.5mm. And the variations of electrical potential becomes smaller with the height h increasing until all potential are equal for h = 1mm corresponding to the top-most surface. This means that the top-most surface is an isopotential surface even under limited height. For better description, the isopotential lines corresponding to 90%U, 75%U, 50%U, 25%U and 10%U are drawn in [FIG 4] and [FIG 5], where U is the electrical potential of the top-most surface.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `[FIG 4] and [FIG 5] illustrate the simulated isopotential contours` | `The simulation results of isopotential maps and electrical current lines profile ... are shown in [FIG 4] and [FIG 5]` | `R04`, `R22`, `R24` | Uses passive figure pointer (`are shown in [FIG N]`) and Ren's exact field terminology (`isopotential maps`, `electrical current lines profile`). |
| `To rigorously validate whether the finite hemisphere height ... introduces artificial boundary distortions, we examine` | `It is necessary to investigate the electrical potential distribution on the top-most surface in order to illustrate whether...` | `R08`, `R22`, `F26` | Uses `It is necessary to investigate...` (`R08`) and domain-specific boundary term `top-most surface` (`R22`) without `rigorously`. |
| `At h = 0.5 mm, a noticeable radial potential gradient ... is observed` | `It is noted that the electrical potential increases significantly from 8.25 µ V to 8.275 µ V ... for h = 0.5mm.` | `R08`, `R26` | Uses `It is noted that...` (`R08`) with exact numerical bounds (`from X to Y`). |
| `This confirms that the upper boundary behaves as a true equipotential surface` | `This means that the top-most surface is an isopotential surface even under limited height.` | `R07`, `R24` | Uses direct causal restatement (`This means that...`) to state the physical implication of the numerical check. |

### Contrastive Pair: `pair_05_results_waveform.md`

---
section: results
function: waveform
source: synthetic
rules: [R01, R04, R06, R25, R26, R27]
---

### AI-default

[FIG 4] depicts the temporal progression of electrical contact resistance alongside tangential friction torque over the course of torsional fretting cycling under a 0.45 deg slip amplitude and 2.5 N normal force. Inspection of the profile reveals a clear tri-phasic degradation trajectory comprising an initial run-in phase, an extended steady-state conduction plateau, and an eventual catastrophic failure phase. Initially (Point A, N = 1), native surface contaminants on the gold flash yield a baseline resistance of 6.8 mΩ. Over the first 400 cycles, interfacial wiping rapidly disrupts this superficial film, driving the resistance down to 5.4 mΩ (Point B) while concomitantly elevating the friction torque from 4.2 N·mm to 6.5 N·mm. Subsequently, robust metallic conduction through the palladium-nickel barrier sustains a remarkably stable resistance window (5.2–6.1 mΩ) up to 1.15 × 10^4 cycles. Beyond Point C (1.18 × 10^4 cycles), however, erratic resistance transients surpassing 180 mΩ emerge, culminating in complete electrical failure (>1.0 Ω) at 1.42 × 10^4 cycles.

### Ren

[FIG 4] shows the typical evolution of the electrical contact resistance and tangential friction torque as a function of torsional fretting cycles at an angular slip amplitude of 0.45 deg and a normal load of 2.5 N. As can be seen from [FIG 4], the variation curve of contact resistance over the entire test can be divided into three distinct stages: the initial running-in stage (Stage I), the stable low-resistance plateau stage (Stage II), and the rapid degradation stage (Stage III). At the beginning of the test (Point A, N = 1 cycle), the initial contact resistance is approximately 6.8 mΩ due to a thin adventitious film on the gold flash. Within the first 400 cycles (Stage I), the contact resistance drops slightly to 5.4 mΩ (Point B) as the superficial film is disrupted by micro-slip. Meanwhile, the friction torque increases from 4.2 N·mm to 6.5 N·mm. During Stage II (from 400 to 1.15 × 10^4 cycles), the contact resistance remains stable between 5.2 mΩ and 6.1 mΩ because metallic conduction is maintained by the palladium-nickel layer. Once the cycle count reaches Point C (1.18 × 10^4 cycles), however, sharp resistance spikes exceeding 180 mΩ appear intermittently. Finally, the contact resistance rises above the 1.0 Ω failure threshold at 1.42 × 10^4 cycles.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `[FIG 4] depicts the temporal progression of ... alongside` | `[FIG 4] shows the typical evolution of ... as a function of torsional fretting cycles` | `R04`, `R06`, `R25` | Uses `[FIG N] shows the typical...` (`R25`) and `as a function of` (`R06`) rather than `depicts the temporal progression`. |
| `Inspection of the profile reveals a clear tri-phasic degradation trajectory comprising` | `As can be seen from [FIG 4], the variation curve of contact resistance ... can be divided into three distinct stages:` | `R06`, `R25`, `R26` | Uses Ren's canonical stage-partitioning formula (`As can be seen from [FIG N], the variation curve ... can be divided into three distinct stages:`). |
| `while concomitantly elevating the friction torque` | `Meanwhile, the friction torque increases from 4.2 N·mm to 6.5 N·mm.` | `R01`, `R05`, `F24` | Splits a participial tail (`while concomitantly elevating...`) into an independent finite sentence opened by `Meanwhile,` (`R05`, `F24`). |
| `sustain a remarkably stable resistance window ... culminating in complete electrical failure` | `remains stable between 5.2 mΩ and 6.1 mΩ ... Finally, the contact resistance rises above the 1.0 Ω failure threshold` | `R12`, `R26`, `F26` | Replaces evaluative/dramatic phrasing (`remarkably`, `culminating in catastrophic failure`) with exact numerical bounds and threshold criteria. |

### Contrastive Pair: `pair_06_results_trend.md`

---
section: results
function: trend
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
rules: [R01, R04, R05, R06, R25, R26, R27]
---

### AI-default

[FIG 17] compares the vertical height distributions of the 90%U, 75%U, 50%U, 25%U, and 10%U equipotential contours across normalized curvature radii r/L spanning from 0.1 to 10 for both sphere-plane and cylinder-plane contacts. Notably, both the normalized height h* and the relative constriction zone height Δh* exhibit a pronounced downward trend as the normalized curvature radius increases. For any given equipotential level, the sphere-plane configuration consistently yields lower h* and Δh* values compared to its cylinder-plane counterpart, signifying that the potential drop is much more tightly localized around the spherical a-spot. Consequently, the cylinder-plane geometry experiences weaker current crowding and a correspondingly smaller constriction voltage drop. Nevertheless, a substantial potential drop develops along the extended cylindrical arc profile, which introduces a considerable bulk resistance component that escalates with increasing cylinder curvature radius. This competing bulk effect ultimately explains why the total resistance of the cylinder-plane contact surpasses that of the sphere-plane contact at larger curvature radii.

### Ren

The height distributions of various isopotential with 90%U, 75%U, 50%U, 25%U and 10%U with varied curvature radius r/L from 0.1 to 10 for sphere-plane contact and with varied normalized curvature radius of cambered surface r/L = 0.1, 1 and 10. cylinder-plane contact are shown in [FIG 17]. The normalized height h∗and the relative height of the constriction region 1h∗both decrease significantly with the normalized curvature radius increasing. For the fixed isopotential, the parameters h∗and 1h∗of sphere-plane contact are always lower than that of cylinder-plane contact, which indicates that the isopotential distribution of former is closer to the contact a-spot than the latter. So the crowding ability for electrical current of cylinder-plane is weaker than that of sphere-plane contact, and there would be a lower potential difference for cylinder-plane contact corresponding to a smaller contact resistance. However, the potential decreases significantly for cylinder-plane contact along the arc profile of cylinder, which causes a larger bulk resistance. And the bulk resistance would increase with the curvature radius of cylinder increasing. This is the root reason for a larger resistance for cylinder-plane contact with the curvature radius increasing than that of sphere-plane contact.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `[FIG 17] compares the vertical height distributions ... across normalized curvature radii` | `The height distributions of various isopotential ... are shown in [FIG 17].` | `R04`, `R25` | Uses passive figure pointer (`The distributions ... are shown in [FIG N]`) instead of anthropomorphizing the figure (`[FIG 17] compares...`). |
| `exhibit a pronounced downward trend as the normalized curvature radius increases` | `both decrease significantly with the normalized curvature radius increasing` | `R06`, `R26` | Uses direct trend verb (`decrease significantly`) + `with the <X> increasing` (`R06`). |
| `signifying that the potential drop is much more tightly localized` | `, which indicates that the isopotential distribution of former is closer to the contact a-spot than the latter.` | `R03`, `R27` | Uses finite `, which indicates that...` clause instead of participial `-ing` tail (`signifying that...`, `F24`). |
| `This competing bulk effect ultimately explains why` | `This is the root reason for a larger resistance for cylinder-plane contact...` | `R27`, `R29` | Uses direct causal summary (`This is the root reason for...`) to close the trend comparison. |

### Contrastive Pair: `pair_07_mechanism_explanation.md`

---
section: mechanism
function: explanation
source: synthetic
rules: [R01, R04, R05, R07, R28, R29, R30]
---

### AI-default

Synthesizing the electrical resistance transients with the post-mortem SEM/EDX evidence allows us to formulate a three-stage phenomenological degradation model for the duplex Au/PdNi coating under rotational micro-slip, as depicted in [FIG 10]. Grounded in Cattaneo–Mindlin torsional contact mechanics [CIT], applying a sub-limiting torque T partitions the circular interface into a central stick core (radius c) encircled by an annular micro-slip zone (c < r ≤ a) featuring a radially increasing slip amplitude. In Stage I ([FIG 10](a)), rotational micro-slip is restricted to the outer annulus, rapidly stripping the superficial gold flash while preserving pristine metallic conduction across the central core. Transitioning into Stage II ([FIG 10](b)), sustained annular abrasion breaches the palladium-nickel barrier, exposing the underlying nickel and copper alloy to frictional oxidation and forming an insulating peripheral oxide ring that constricts current flow toward the center. Finally, Stage III ([FIG 10](c)) is characterized by the inward migration of oxidized debris into the stick zone—driven by cyclic normal vibration pumping—which ultimately blankets the conducting a-spots and triggers a two-order-of-magnitude surge in contact resistance.

### Ren

Based on the electrical contact resistance waveforms and post-test SEM/EDX observations, the interfacial degradation process of the duplex Au/PdNi coating under rotational micro-slip can be explained by a three-stage physical model, as illustrated in [FIG 10]. According to the Cattaneo–Mindlin tangential contact theory [CIT], when the applied torque T is below the limiting friction torque, the circular contact area splits into a central stick zone of radius c and an outer annular slip zone (c < r ≤ a). Within the outer annulus, the local slip amplitude increases linearly with the radial coordinate r. During Stage I ([FIG 10](a)), rotational micro-slip remains confined to the outer annulus. The thin gold flash is rapidly sheared off in this outer ring, whereas the central stick core maintains low-resistance metallic conduction. As cycling proceeds into Stage II ([FIG 10](b)), abrasive wear in the outer annulus penetrates the palladium-nickel layer and exposes the nickel underlayer and copper alloy substrate. Fine copper and nickel wear particles oxidize rapidly under frictional heating and form an insulating ring along the periphery. Consequently, current streamlines constrict toward the shrinking central stick zone. In Stage III ([FIG 10](c)), oxidized debris gradually migrates inward into the central core; this may be attributed to radial pumping under cyclic normal vibration. Once the insulating oxide film covers the central conducting a-spots, the contact resistance rises abruptly above 1.0 Ω.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `Synthesizing the electrical resistance transients ... allows us to formulate` | `Based on the electrical contact resistance waveforms and post-test SEM/EDX observations, the interfacial degradation process ... can be explained by a three-stage physical model, as illustrated in [FIG 10].` | `R28`, `F24` | Opens the mechanism section with `Based on ..., the <process> can be explained by a three-stage physical model, as illustrated in [FIG N]` rather than a gerund opener (`Synthesizing...`). |
| `Grounded in Cattaneo–Mindlin torsional contact mechanics [CIT], applying...` | `According to the Cattaneo–Mindlin tangential contact theory [CIT], when the applied torque T is below...` | `R16`, `R30` | Uses `According to the <Name> theory [CIT], when...` instead of a dangling participial phrase (`Grounded in...`). |
| `forming an insulating peripheral oxide ring that constricts current flow` | `Fine copper and nickel wear particles oxidize rapidly ... and form an insulating ring along the periphery. Consequently, current streamlines constrict toward the shrinking central stick zone.` | `R01`, `R05`, `R28` | Breaks dense multi-clause chains into sequential physical steps linked by `Consequently,` (`R05`). |
| `—driven by cyclic normal vibration pumping—` | `; this may be attributed to radial pumping under cyclic normal vibration.` | `R07`, `R29`, `F24` | Avoids em-dash parentheticals and uses Ren's signature hedged causal attribution (`this may be attributed to...`, `R29`). |

### Contrastive Pair: `pair_08_conclusion_summary.md`

---
section: conclusion
function: summary
source: "P22 (IEEE Access 2020, doi:10.1109/ACCESS.2020.2994085, CC BY 4.0)"
rules: [R01, R05, R07, R31, R32, R33]
---

### AI-default

In summary, this work has presented a comprehensive comparative investigation of two canonical cambered contact configurations—sphere-plane and cylinder-plane contacts—under elastic deformation, focusing on how geometric dimensions and mechanical loading govern electrical contact resistance. Our findings demonstrate that mechanical load plays a dominant role in modulating the resistance of sphere-plane contacts, whereas cylinder-plane contacts are primarily governed by the axial contact length due to their line-conforming geometry. Furthermore, finite-element field analyses reveal stronger current crowding in spherical contacts and highlight that the classical Hertzian small-spot approximation breaks down once the normalized contact radius exceeds a/r = 0.1. Overall, cylinder-plane contacts offer superior electrical conductivity under low-load conditions, providing valuable design guidelines for next-generation MEMS switches. Future work will extend this framework to elasto-plastic contact regimes.

### Ren

This paper mainly aims to systematically investigate the similarity and difference between two typical cambered surface contacts, i.e. sphere-plane contact and cylinder-plane contact, under the elastic deformation based on the effects of size parameters and mechanical load on the contact resistance. Our results indicate that mechanical load is a sensitive parameter to contact resistance of sphere-plane contact. Meanwhile, the contact resistance of cylinder-plane contact is significantly affected by contact length. This difference is attributed to the fact that the specific conforming feature of cylinder-plane contact. The distributions of simulated constriction region show that the sphere-plane contact has a stronger current crowding ability. And the simplification of the Hertzian contact area for both sphere-and cylinder-plane contacts is limited with larger contact radius for a/r > 0.1. Furthermore, the conductive ability of non-conforming contact is determined by the feature of cambered surface and mechanical load comprehensively. And the superiority of cylinder-plane contact would be performed even under low mechanical load. This is a positive and beneficial conclusion in engineering applications for electrical contacts, especially for the determination of contact structure in the design process. And the dimensionless results of contact resistance could be instructive to the stable electrical contact for MEMS under smaller dimension and lower contact load. In future, the detailed works on the plastic deformation will be in schedule for comparison to the elastic deformation for different contact structures.

### Differences

| AI-default | Ren | Rule | Why |
| :--- | :--- | :--- | :--- |
| `In summary, this work has presented a comprehensive comparative investigation of two canonical cambered contact configurations—sphere-plane and cylinder-plane contacts—` | `This paper mainly aims to systematically investigate the similarity and difference between two typical cambered surface contacts, i.e. sphere-plane contact and cylinder-plane contact,` | `R07`, `R31`, `F17` | Opens prose conclusions with `This paper mainly aims to systematically investigate...` (`R31`) and uses `, i.e.` (`R07`) instead of em-dashes and `canonical`. |
| `mechanical load plays a dominant role in modulating ... whereas cylinder-plane contacts are primarily governed by` | `Our results indicate that mechanical load is a sensitive parameter to ... Meanwhile, the contact resistance of cylinder-plane contact is significantly affected by contact length.` | `R01`, `R05`, `R32` | Splits contrast into two crisp sentences linked by `Meanwhile,` (`R05`) and uses `is a sensitive parameter to` / `is significantly affected by`. |
| `providing valuable design guidelines for next-generation MEMS switches. Future work will extend this framework` | `And the dimensionless results of contact resistance could be instructive to the stable electrical contact for MEMS ... In future, the detailed works on the plastic deformation will be in schedule` | `R33`, `F17` | Avoids banned words (`framework`, `next-generation`) and states specific engineering applicability (`instructive to the stable electrical contact for MEMS`). |

---

## Part IX — Output Report Templates

### Mode B Template (`translation_report.md`)
```markdown
# Translation Report

**Section / function:** `<section>/<function>`  **Fidelity:** balanced

## English translation

<translation>

## Terminology

| 中文 | English used | Source (glossary / chosen) | Confidence |
|---|---|---|---|

## Uncertain points

- <source phrase> → <rendering> — <why uncertain>

## Checks

- style_lint: <pass / issues>
- fidelity_check (numbers, citations): <pass / issues>
```

### Mode C Template (`polish_report.md`)
```markdown
# Polish Report

**Section / function:** `<section>/<function>`  **Fidelity:** balanced

## Polished text

<polished text>

## Change log

| # | Original | Revised | Rule | Reason |
|---|---|---|---|---|
| 1 | | | R.. | |

## Checks

- style_lint: <pass / issues>
- fidelity_check: <pass / issues>
- Open items: `[TODO: ...]` list, if any
```

### Mode D Template (`review_report.md`)
```markdown
# Style Review Report

**Section / function:** `<section>/<function>`

## Summary

<2–3 sentences: overall distance from Ren's style, main issues>

## Findings

| # | Location (quote) | Issue | Rule | Suggested fix |
|---|---|---|---|---|
| 1 | | | R.. | |

## Metrics (style_lint)

| Metric | Value | Target range |
|---|---|---|
```

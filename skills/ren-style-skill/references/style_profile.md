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

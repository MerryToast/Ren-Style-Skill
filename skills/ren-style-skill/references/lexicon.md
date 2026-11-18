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

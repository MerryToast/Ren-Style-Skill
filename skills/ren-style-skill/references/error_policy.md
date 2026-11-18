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

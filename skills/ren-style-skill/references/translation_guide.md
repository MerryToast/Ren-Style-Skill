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

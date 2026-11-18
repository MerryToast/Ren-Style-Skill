---
name: ren-style-skill
description: >-
  Use this skill when the user asks to draft, translate (Chinese to English),
  polish, or style-check academic paper text on electrical contacts or electrical
  engineering in the writing style of Wanbin Ren (Harbin Institute of Technology).
  Covers abstract, introduction, experimental setup, modeling, results, mechanism
  analysis, and conclusion sections.
---

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

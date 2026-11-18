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

Write, translate, polish or review academic text so that it matches the writing style of
Wanbin Ren (electrical contacts: fretting, contact resistance, contact welding, arcs, connectors).

> Status: v0 skeleton. `references/` and `examples/` are filled by the build pipeline
> (see repository `docs/design_notes.md`). If a referenced file is still a placeholder,
> tell the user the style data has not been built yet.

## 1. Determine the mode

| Mode | Trigger | Output template |
|---|---|---|
| **A Draft** | notes / outline → prose | plain text |
| **B Translate** | Chinese text → English | [translation_report.md](templates/translation_report.md) |
| **C Polish** | English draft → improved English | [polish_report.md](templates/polish_report.md) |
| **D Review** | English draft → diagnosis only | [review_report.md](templates/review_report.md) |

Fidelity level: `balanced` (default) = imitate Ren's style, **fix grammar**.
`strict` = also keep harmless non-native habits. See [error_policy.md](references/error_policy.md).

## 2. Locate section and function

Classify the text into one `section/function` (ask the user if unclear):

| section | functions |
|---|---|
| abstract | full |
| introduction | background, prior_work, gap, this_paper |
| experimental | test_rig, specimen, procedure |
| modeling | model_setup, derivation, validation |
| results | waveform, trend, surface_analysis |
| mechanism | explanation |
| conclusion | numbered, summary |

## 3. Load context — materials first, instructions last

Read only what is needed, in this order:

1. Examples for this `section/function` (2–3 files):
   `examples.local/<section>/<function>_*.md` if that folder exists, otherwise `examples/<section>/<function>_*.md`.
2. 1–2 files from `examples/contrastive/` (prefer the same section).
3. `references/playbooks/<section>.md`.
4. `references/style_profile.md` (global rules + this section).
5. `references/lexicon.md` and `references/error_policy.md`.
6. Mode B only: `references/glossary_zh_en.md` and `references/translation_guide.md`.

Then, before writing, state to yourself: *"Strictly align with the sentence rhythm, move order and
lexical restraint of the loaded examples for `<section>/<function>`."*

## 4. Generate in chunks

- One subsection per pass, **≤ 800 words**. For longer input, split at paragraph boundaries; when
  continuing, include the last paragraph of the previous chunk and reload the same examples.
- Follow the move order of the playbook. Imitate rhythm and wording — **never copy example content**.

## 5. Self-check loop (max 2 revision rounds)

```bash
python scripts/style_lint.py --section <section> output.txt
python scripts/fidelity_check.py source.txt output.txt      # modes B and C only
```

- `style_lint.py`: banned words, sentence-length range, passive ratio, signature-word over-use.
- `fidelity_check.py`: numbers, units, citations, equation/figure references must be unchanged.
  (For mode B, compare numbers/citations only.)
- If scripts cannot run, perform the same checks manually and say so.

## 6. Hard rules

1. Never add claims, data, references or results that are not in the user's input; mark gaps as `[TODO: ...]`.
2. Never reuse specific content (materials, values, findings) from the examples.
3. Banned words in `lexicon.md` override everything else.
4. Signature words (e.g. sentence-final "explicitly") must stay within the density limits in `lexicon.md`.
5. Keep the user's technical terms; for mode B follow `glossary_zh_en.md`, list uncertain terms.
6. Formatting conventions (IEEE vs Elsevier headings, "Index Terms", etc.) follow the target journal the user names.

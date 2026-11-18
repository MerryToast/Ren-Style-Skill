# Prompt: Style vs. error classification (Phase 3)

<!-- Fill {FEATURES} (list of candidate features with evidence sentences). -->

## Materials

### Candidate features (from stylometry + move analysis), each with evidence sentences
{FEATURES}

## Task

Policy decided by the project owner: **imitate Ren's style, fix grammar** (`fidelity_level: balanced`).

Classify every feature into exactly one class:

| Class | Meaning | Skill behaviour (balanced) | Skill behaviour (strict) |
|---|---|---|---|
| `KEEP_STYLE` | Idiomatic, characteristic choice (e.g. sentence-final "explicitly", "It is shown that", "by introducing our newly designed test rig") | reproduce | reproduce |
| `FIX_ERROR` | Grammatical / lexical error (e.g. "are resulted from", "our new designed", "ever published results") | correct | correct |
| `OPTIONAL_NONNATIVE` | Non-native but harmless habit (e.g. frequent sentence-initial "Also,") | use sparingly | reproduce |

For each feature output a row: `id | feature | class | corrected/idiomatic form (if FIX_ERROR) | evidence (paper_id) | note`.

## Rules
- When unsure between KEEP_STYLE and OPTIONAL_NONNATIVE, choose OPTIONAL_NONNATIVE.
- Never classify a grammatical error as KEEP_STYLE.
- Output a single Markdown table, then a short list of the 10 most important FIX_ERROR patterns.

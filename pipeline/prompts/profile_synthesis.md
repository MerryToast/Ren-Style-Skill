# Prompt: Style profile synthesis (Phase 3)

<!-- Fill {STATS_REPORT}, {LEXICON}, {MOVE_ANALYSES}, {STYLE_VS_ERROR}. -->

## Materials
### Stylometry report
{STATS_REPORT}
### Distinctive lexicon (Ren vs AI baseline; Ren vs tier B)
{LEXICON}
### Move analyses (all sections)
{MOVE_ANALYSES}
### Style vs error table
{STYLE_VS_ERROR}

## Task

Produce the following files for `skills/ren-style-skill/references/`:

1. `style_profile.md` (≤ 1500 words): numbered rules `R01…`, grouped as Global / per section.
   Each rule: statement · quantitative basis (if any) · one short evidence quote (≤ 20 words, paper_id).
   Public repo: quotes must be short; prefer evidence from P22 (open access) when equivalent.
2. `style_profile.json`: lint thresholds per section, e.g.
   `{"global": {...}, "results": {"sent_len_p50": [lo, hi], "passive_ratio": [lo, hi], "signature_max_per_100w": {...}}}`
   Ranges = weighted P25–P75 of the corpus unless noted.
3. `lexicon.md`: signature words/phrases (with max density), preferred verbs & connectives,
   replacement table (AI-default → Ren-preferred), **corpus-verified** banned list.
4. `error_policy.md`: from the style-vs-error table, grouped by class.
5. `playbooks/<section>.md`: ordered moves with sentence frames and length guidance.

## Rules
- Every rule must be traceable to materials. No vague rules.
- If tier S conflicts with tier A, follow tier S and note it.
- Do not ban a word Ren actually uses.

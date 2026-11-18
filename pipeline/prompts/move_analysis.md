# Prompt: Rhetorical move analysis (Phase 3)

<!-- Fill {SECTION}, {STATS}, {PARAGRAPHS}. Materials first, instructions last. -->

## Materials

### Quantitative statistics for section `{SECTION}` (from data/processed/stats.json)
{STATS}

### Paragraphs from section `{SECTION}` (tier S first, then tier A; each tagged with paper_id and tier)
{PARAGRAPHS}

## Task

You are analysing the academic writing style of Wanbin Ren (electrical contacts, HIT).
For section `{SECTION}` only:

1. **Moves**: List the rhetorical moves (ordered) found across the paragraphs, e.g. for Introduction:
   application background → reliability requirement → prior work → gap → "In this paper" → contributions.
   For each move give: typical opening pattern(s), typical length (sentences), 2 short evidence quotes (≤ 20 words, with paper_id).
2. **Argument progression**: how paragraphs advance (general→specific? phenomenon→mechanism?).
3. **Stance**: how prior work is evaluated, how strongly own results are claimed, hedging habits.
4. **Recurring sentence frames** (≥ 8), written as templates with slots, e.g.
   `It is shown that <finding>, which results from <cause>.`
5. **Differences between tier S and tier A** if any (tier S wins conflicts).

## Rules
- Base every claim on the materials; quote evidence. Do not invent statistics — use only numbers from STATS.
- No vague rules such as "be clear and concise".
- Output Markdown with headings 1–5.

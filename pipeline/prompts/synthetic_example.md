# Prompt: Synthetic public example (Phase 4)

<!-- Fill {SECTION}, {FUNCTION}, {GOLDEN_EXCERPTS} (local only), {PLAYBOOK}, {RULES}. -->

## Materials
### Golden excerpts for `{SECTION}/{FUNCTION}` (local, copyrighted — do NOT copy content)
{GOLDEN_EXCERPTS}
### Playbook
{PLAYBOOK}
### Style rules
{RULES}

## Task
Write ONE new paragraph (150–250 words) for `{SECTION}/{FUNCTION}` in exactly this style
(sentence rhythm, move order, connectives, verb choices, restraint), about a **fictitious but plausible**
electrical-contact study (invent materials, parameters, and findings; keep physics plausible).

## Rules
- No sentence may share more than 5 consecutive words with any excerpt (except fixed technical terms).
- Apply `fidelity_level: balanced` (correct grammar).
- After the paragraph, list which rules (R-numbers) it demonstrates.
- Output frontmatter:
  ```
  ---
  section: {SECTION}
  function: {FUNCTION}
  source: synthetic
  rules: [R..]
  ---
  ```

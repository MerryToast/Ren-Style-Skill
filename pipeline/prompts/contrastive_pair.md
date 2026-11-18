# Prompt: Contrastive pair (Phase 4)

<!-- Fill {ORIGINAL} (Ren paragraph) and {RULES}. -->

## Materials
### Original paragraph (Ren)
{ORIGINAL}
### Style rules
{RULES}

## Task
1. Rewrite the original paragraph the way a default LLM would write it ("AI-default version"):
   same facts, but with your natural default tone and vocabulary. Do not exaggerate artificially.
2. Produce a table of differences: `AI-default phrase | Ren phrase | rule R-number | why`.

## Output format
```
---
section: <section>
function: <function>
source: <paper_id or synthetic>
---
### AI-default
...
### Ren
<original, unchanged>
### Differences
| AI-default | Ren | Rule | Why |
```
For the public layer, use a synthetic or open-access (P22) paragraph as the original.

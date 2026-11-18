# Prompt: Blind A/B Style Judge (Phase 6)

<!-- Fill {SECTION}, {REF_EXCERPTS}, {PASSAGE_A}, {PASSAGE_B}. Order of A/B is randomized by 06_evaluate.py. -->

## Reference Anchor (3 genuine train excerpts by Prof. Wanbin Ren for `{SECTION}`)
{REF_EXCERPTS}

## Candidate Passages (one is a heldout original by Prof. Wanbin Ren; one is a generated/rewritten passage)

### Passage A
{PASSAGE_A}

### Passage B
{PASSAGE_B}

## Task
Without relying on topic familiarity, judge which passage (**A** or **B**) is the genuine paragraph written by Prof. Wanbin Ren, based strictly on:
1. Sentence-length rhythm and clause structure (alternation of short 12–16-word anchor sentences and 25–35-word mechanism sentences; finite relative clauses vs participial `-ing` tails);
2. Section-appropriate voice and tense (passive setup/procedure vs active present-tense figure pointers and derivations);
3. Connective habits (`Meanwhile,`, `Furthermore,`, `Subsequently,`, `However,`, `Therefore,`) and lexical restraint (absence of LLM clichés such as `crucial`, `pivotal`, `intricate`, `interplay`, `elucidate`, `leverage`, `utilize`, `framework`);
4. Domain-specific phrasing (`as a function of`, `by using`, `with the increase of`, `, namely`, `may be attributed to`).

Output JSON:
```json
{
  "predicted_original": "A or B",
  "confidence": 0.0,
  "stylistic_cues": "..."
}
```

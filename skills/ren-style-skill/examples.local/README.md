# examples.local/ — private golden excerpts (gitignored)

Only this README is tracked. Everything else in this folder stays on your machine.

Put verbatim golden excerpts from publisher-copyrighted papers here (tiers S/A, `split: train` only),
same layout and frontmatter as `../examples/`:

```text
examples.local/<section>/<function>_NN.md
examples.local/contrastive/*.md
```

Rules (design_notes §6 Phase 4):
- 2–3 excerpts per section/function, 150–250 words each, **at least one from tier S** (P01/P03/P13).
- Spread across papers (≤ 2 per paper per function).
- Never use held-out (P05, P09, P16, P19) or tier-B papers.

`SKILL.md` loads this folder in preference to `../examples/` when it exists.

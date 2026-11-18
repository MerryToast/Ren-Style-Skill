# Build a writing-style skill for another author

The pipeline is author-agnostic. To build your own:

1. Fork this repository and rename `skills/ren-style-skill/` (and its `name:` frontmatter, lowercase-hyphenated).
2. `Copy-Item config.example.yaml config.yaml`, then edit:
   - `author`, `corpus_dir`
   - `papers`: one entry per PDF with `prefix` (leading filename number), `tier` (S/A/B), `split`, optional `dup_group`, `open_access`.
3. Run `pipeline/00_build_manifest.py` → check `data/corpus_meta.csv`.
4. Run `01` → `05`, then the Phase 3/4 prompts in `pipeline/prompts/` with your agent.
5. Fill `references/`, `examples/` (public: open-access + synthetic) and `examples.local/` (private).
6. Evaluate with `eval/` before publishing.

Tier guidance:
- **S**: 2–4 papers the author wrote alone or clearly led; strongest style anchors.
- **A**: other first-author papers.
- **B**: papers where the author is only corresponding / supervising author — useful to separate personal style from group style.

Copyright: never commit PDFs or full text; only distribute open-access excerpts with attribution and synthetic examples.

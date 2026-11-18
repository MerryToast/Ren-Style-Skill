# data/ (gitignored)

Everything in this folder is derived from copyrighted papers and must **never** be committed.

```text
data/
├── corpus_meta.csv        # 00_build_manifest.py
├── raw/<ID>.txt           # 01_extract_pdf.py   (per-paper extracted text)
├── raw/<ID>.blocks.json   # 01_extract_pdf.py   (layout blocks for debugging)
├── processed/paragraphs.jsonl   # 02_clean_segment.py
├── processed/stats.json         # 03_stylometry.py
├── processed/stats_report.md
├── processed/lexicon.json       # 04_distinctive_lexicon.py
├── baseline/ai_rewrites.jsonl   # AI-default baseline paragraphs (Phase 2)
└── candidates/<section>/<function>.jsonl   # 05_rank_candidates.py
```

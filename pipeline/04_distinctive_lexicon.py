"""Phase 2.2 — Distinctive lexicon via weighted log-odds (informative Dirichlet prior).

Three-way comparison (docs/design_notes.md §6 Phase 2):
  1. Ren (S+A, train)  vs  AI baseline (data/baseline/ai_rewrites.jsonl)  -> "anti-AI-tone" table
  2. Ren (S+A, train)  vs  tier B (students first-author)                  -> Ren-specific traits

TODO:
  - unigrams + bigrams + trigrams, lemmatized, placeholders ([EQ], [CIT], [FIG n]) removed
  - z-scored log-odds (Monroe et al., 2008); keep top/bottom 100 per comparison
  - banned-word candidates = common LLM words with Ren frequency ~ 0 (verify, never assume)
  Output: data/processed/lexicon.json

Usage:
    python pipeline/04_distinctive_lexicon.py
"""
from __future__ import annotations

import sys


def main() -> int:
    raise NotImplementedError("Phase 2: implement distinctive lexicon")


if __name__ == "__main__":
    sys.exit(main())

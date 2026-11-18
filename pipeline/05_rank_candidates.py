"""Phase 4.1 — Rank candidate golden excerpts by typicality.

TODO (docs/design_notes.md §6 Phase 4):
  - Assign each train paragraph (tiers S+A only) a function label within its section
    (taxonomy in config.yaml `sections`), via heuristics + LLM labelling.
  - Feature vector per paragraph (from 03_stylometry features); centroid per section/function.
  - typicality distance = distance to centroid; multiply by 0.7 for tier S (bonus).
  - Keep top 8 per section/function, 150–250 words, diverse papers (max 2 per paper).
  - NEVER include split heldout/secondary papers.
  Output: data/candidates/<section>/<function>.jsonl

Usage:
    python pipeline/05_rank_candidates.py
"""
from __future__ import annotations

import sys


def main() -> int:
    raise NotImplementedError("Phase 4: implement candidate ranking")


if __name__ == "__main__":
    sys.exit(main())

"""Phase 2.1 — Quantitative stylometry (weighted, per section).

Only tiers S+A with split == train are used for the profile; secondary (tier B) is
computed separately for comparison. Use ``common.effective_weight`` for weighting.

TODO (Phase 2, see docs/design_notes.md §6 Phase 2):
  Per section, weighted:
    - sentence length distribution (mean, P25/P50/P75/P90), paragraph length (sentences, words)
    - passive voice ratio (spaCy dep: nsubjpass / auxpass), "we"/"our" rate
    - formal-subject constructions: "It is shown/found/demonstrated/noted that ..."
    - tense ratios (present / past / present perfect) from main verbs
    - sentence- and paragraph-initial connectives ranking (However, Furthermore, Moreover, Subsequently, Also, ...)
    - reporting verbs ranking (investigate, present, propose, demonstrate, ...)
    - signature adverbs and their position (e.g. sentence-final "explicitly")
    - hedging / intensity words, semicolon / parenthesis / dash rates
    - US vs UK spelling, number+unit formatting ("0.2/0.5/1 A", "25∼150 nm/s"), abbreviation definitions
    - early (<=2015) vs late (>=2017) comparison
  Output: data/processed/stats.json, data/processed/stats_report.md
  Sanity check: "explicitly" should rank among signature words.

Usage:
    python pipeline/03_stylometry.py
"""
from __future__ import annotations

import sys


def main() -> int:
    raise NotImplementedError("Phase 2: implement stylometry")


if __name__ == "__main__":
    sys.exit(main())

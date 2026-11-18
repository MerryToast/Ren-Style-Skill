"""Phase 1.3 — Clean extracted text and segment into sections / paragraphs.

TODO (Phase 1, see docs/design_notes.md §2.3 / §3):
  Cleaning
    - Ligatures (ﬁ ﬂ ﬀ ﬃ) -> ASCII; de-hyphenate line breaks ("mea- suring" -> "measuring").
    - Elsevier letter-spaced labels ("a b s t r a c t", "a r t i c l e i n f o").
    - Broken symbols (e.g. "25\\u0001125 1C" -> "25–125 °C"); keep a fix-log per paper.
    - Drop-cap repair ("LECTROMECHANICAL" -> "ELECTROMECHANICAL"); one-word-per-line joins (P23).
    - Placeholders: equations -> [EQ], citations "[1-3]" / "(Smith, 2010)" -> [CIT], "Fig. 3" -> [FIG 3].
  Segmentation
    - Map headings (Roman numerals, "1. Introduction", "Abstract—", "SUMMARY") to canonical labels:
      abstract | introduction | experimental | modeling | results | mechanism | conclusion | other.
    - Use an LLM fallback only for ambiguous headings; log every mapping decision.
  Output
    - data/processed/paragraphs.jsonl, one record per paragraph:
      {paper_id, tier, weight, split, section, heading, para_idx, text, n_words}

Usage:
    python pipeline/02_clean_segment.py
"""
from __future__ import annotations

import sys

from common import load_config


def main() -> int:
    load_config()
    raise NotImplementedError("Phase 1: implement cleaning and section segmentation")


if __name__ == "__main__":
    sys.exit(main())

"""Phase 6 — Evaluation harness.

TODO (docs/design_notes.md §6 Phase 6):
  - back_translation : heldout paragraph -> zh -> mode B -> en ; style distance to Ren centroid vs no-skill baseline
  - de_styling       : heldout paragraph -> AI-default rewrite -> mode C ; distance + banned-word hits
  - personalness     : tier-B paragraph -> mode C ; should move toward Ren (S+A) centroid, away from tier-B centroid
  - blind_judge      : mix originals and outputs; judge accuracy (target ~50%)
  - fidelity         : skills/ren-style-skill/scripts/fidelity_check.py on every B/C output (target 0 diffs)
  - ablation         : without examples / profile / contrastive / examples.local
  - cross_model      : repeat back_translation with at least one non-Argon model
  Raw outputs -> eval/results/raw/ (gitignored); aggregated metrics -> eval/results/<date>_<tag>.md

Usage:
    python eval/run_eval.py --suite back_translation
"""
from __future__ import annotations

import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", default="all")
    ap.parse_args()
    raise NotImplementedError("Phase 6: implement evaluation suites")


if __name__ == "__main__":
    sys.exit(main())

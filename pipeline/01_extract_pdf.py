"""Phase 1.2 — Extract text from PDFs (layout-aware).

TODO (Phase 1, see docs/design_notes.md §2.3 / §6):
  - Use ``page.get_text("blocks")`` and sort blocks by column (x0 vs page mid-line) then y.
  - Drop publisher cover pages (``skip_pages`` in config, e.g. P12, P25).
  - Strip IEEE accepted-manuscript banners (``strip_banner``: P19, P23) and running headers/footers
    (blocks repeated on >50% of pages, page numbers, journal header lines).
  - Stop at "References" / "REFERENCES"; keep figure/table captions separately.
  - Output per paper: ``data/raw/<ID>.txt`` and ``data/raw/<ID>.blocks.json`` (for debugging).

Usage:
    python pipeline/01_extract_pdf.py [--only P01 P13]
"""
from __future__ import annotations

import argparse
import sys

from common import data_dir, load_config, resolve_papers


def extract_paper(paper, out_dir) -> None:
    raise NotImplementedError("Phase 1: implement layout-aware extraction")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="paper IDs to process")
    args = ap.parse_args()
    cfg = load_config()
    out_dir = data_dir(cfg) / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in resolve_papers(cfg):
        if args.only and p.id not in args.only:
            continue
        extract_paper(p, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())

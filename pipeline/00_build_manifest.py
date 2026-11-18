"""Phase 1.1 — Build the corpus manifest.

Reads the paper registry in config.yaml, matches each entry to a PDF in
``corpus_dir`` and writes ``data/corpus_meta.csv`` with a first-page title guess
so a human can verify tiers / splits before extraction.

Usage:
    python pipeline/00_build_manifest.py
"""
from __future__ import annotations

import csv
import sys

import pymupdf

from common import data_dir, effective_weight, load_config, resolve_papers


def first_page_head(pdf_path, n_chars: int = 160) -> str:
    with pymupdf.open(pdf_path) as doc:
        text = doc[0].get_text()
    return " ".join(text.split())[:n_chars]


def main() -> int:
    cfg = load_config()
    papers = resolve_papers(cfg)
    out = data_dir(cfg) / "corpus_meta.csv"
    missing = [p.id for p in papers if p.pdf is None]

    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["paper_id", "prefix", "tier", "split", "weight", "effective_weight",
                    "venue", "year", "open_access", "dup_group", "short", "pdf_file", "first_page_head"])
        for p in papers:
            w.writerow([
                p.id, p.prefix, p.tier, p.split, p.weight, round(effective_weight(p, cfg), 3),
                p.meta.get("venue"), p.meta.get("year"), p.meta.get("open_access", False),
                p.meta.get("dup_group", ""), p.meta.get("short"),
                p.pdf.name if p.pdf else "", first_page_head(p.pdf) if p.pdf else "",
            ])

    tiers = {t: sum(1 for p in papers if p.tier == t) for t in ("S", "A", "B")}
    splits = {s: sum(1 for p in papers if p.split == s) for s in ("train", "heldout", "secondary")}
    print(f"Wrote {out}")
    print(f"Tiers: {tiers}   Splits: {splits}")
    if missing:
        print(f"[error] No PDF matched for: {missing}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

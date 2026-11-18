"""Phase 1.1 — Build the corpus manifest.

Reads the paper registry in config.yaml, matches each entry to a PDF in
``corpus_dir``, extracts coordinate-sorted first-page text and DOI/year clues
from the PDF (skipping publisher cover pages if configured), and writes
``data/corpus_meta.csv`` for human verification before full extraction.

Usage:
    python pipeline/00_build_manifest.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import pymupdf

from common import Paper, data_dir, effective_weight, load_config, resolve_papers

DOI_RE = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)")


def inspect_pdf_first_page(paper: Paper, n_chars: int = 200) -> tuple[str, str, int]:
    """Return (coordinate-sorted first-page head, extracted DOI if any, page_count)."""
    if not paper.pdf or not paper.pdf.exists():
        return "", "", 0
    skip_pages = set(paper.meta.get("skip_pages") or [])
    with pymupdf.open(paper.pdf) as doc:
        n_pages = len(doc)
        first_idx = 0
        while (first_idx + 1) in skip_pages and (first_idx + 1) < n_pages:
            first_idx += 1
        page = doc[first_idx]
        # Sort blocks by vertical band (10pt) then horizontal x0 so blocks stored
        # out-of-order in the PDF content stream (e.g., P23 title/authors) appear first.
        blocks = sorted(page.get_text("blocks"), key=lambda b: (round(b[1] / 10.0), b[0]))
        full_text = " ".join(" ".join(b[4].split()) for b in blocks if b[4].strip())
        # Also search metadata + first page for DOI
        meta_str = " ".join(str(v) for v in (doc.metadata or {}).values() if v)
        m = DOI_RE.search(full_text) or DOI_RE.search(meta_str)
        doi = m.group(1).rstrip(".") if m else ""
    return full_text[:n_chars], doi, n_pages


def main() -> int:
    cfg = load_config()
    papers = resolve_papers(cfg)
    out = data_dir(cfg) / "corpus_meta.csv"
    missing = [p.id for p in papers if p.pdf is None]

    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow([
            "paper_id",
            "prefix",
            "title",
            "first_author",
            "authors",
            "venue",
            "year",
            "doi",
            "tier",
            "weight",
            "effective_weight",
            "split",
            "open_access",
            "dup_group",
            "pages",
            "pdf_file",
            "first_page_head",
        ])
        for p in papers:
            head, pdf_doi, n_pages = inspect_pdf_first_page(p)
            doi = p.meta.get("doi") or pdf_doi
            w.writerow([
                p.id,
                p.prefix,
                p.meta.get("title") or p.meta.get("short", ""),
                p.meta.get("first_author", ""),
                p.meta.get("authors", ""),
                p.meta.get("venue", ""),
                p.meta.get("year", ""),
                doi,
                p.tier,
                p.weight,
                round(effective_weight(p, cfg), 3),
                p.split,
                p.meta.get("open_access", False),
                p.meta.get("dup_group", ""),
                n_pages,
                p.pdf.name if p.pdf else "",
                head,
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

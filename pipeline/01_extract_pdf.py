"""Phase 1.2 — Extract text from PDFs (layout-aware).

Uses ``page.get_text("blocks")`` with coordinate-based column sorting:
  - Drops publisher cover pages (``skip_pages`` in config, e.g. P12, P25).
  - Strips IEEE accepted-manuscript banners (``strip_banner``: P19, P23), copyright
    lines, page-1 affiliation/manuscript footnotes, and running headers/footers.
  - Handles both two-column and single-column (P11, P24) layouts, preserving
    pre-Introduction full-width/boxed abstracts on page 1 before two-column body text.
  - Stops at References / Appendix / Acknowledgments.
  - Separates figure/table captions, figure/table internal labels, and display
    equation blocks from prose blocks.
  - Writes per paper: ``data/raw/<ID>.txt`` and ``data/raw/<ID>.blocks.json``.

Usage:
    python pipeline/01_extract_pdf.py [--only P01 P13]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pymupdf

from common import Paper, data_dir, load_config, resolve_papers

SINGLE_COLUMN_PAPERS = {"P11", "P24"}

# Lines that are always running headers, footers, copyright banners, or footnotes
STRIP_LINE_PATTERNS = [
    re.compile(r"^This article has been accepted for publication", re.I),
    re.compile(r"^Content may change prior to final publication", re.I),
    re.compile(r"^Transactions on (?:Components|Industrial|Electron)", re.I),
    re.compile(r"^Authorized licensed use limited to:", re.I),
    re.compile(r"^\d{4}-\d{4}\s*(?:\(c\)|©|/\$|\$)", re.I),
    re.compile(r"^&\s*201\d\s+Elsevier\s+Ltd\.\s+All\s+rights\s+reserved", re.I),
    re.compile(r"^Personal use is permitted, but republication", re.I),
    re.compile(r"^See http://www\.ieee\.org/publications_standards", re.I),
    re.compile(r"^(?:http://dx\.doi\.org/|https?://doi\.org/|Digital Object Identi|DOI\s*:?\s*10\.)", re.I),
    re.compile(r"^Color versions of one or more of the", re.I),
    re.compile(r"^online at http://ieeexplore\.ieee\.org", re.I),
    re.compile(r"^The associate editor coordinating the review", re.I),
    re.compile(r"^approving it for publication was\b", re.I),
    re.compile(r"^VOLUME\s+\d+,\s*20\d\d\b", re.I),
    re.compile(r"^This work is licensed under a Creative Commons", re.I),
    re.compile(r"^Materials\s+2020,\s*13,\s*3666", re.I),
    re.compile(r"^Materials Research Innovations$", re.I),
    re.compile(r"^SUPPL\s+\d+\s+S\d+-\d+$", re.I),
    re.compile(r"^VOL\s+\d+$", re.I),
    re.compile(r"^©\s*(?:W\.\s*S\.\s*Maney|20\d\d\s+(?:Taylor|Author|IEEE|Elsevier))", re.I),
    re.compile(r"^Copyright\s+c?\s*⃝?\s*20\d\d\s+The Institute of Electronics", re.I),
    re.compile(r"^Published (?:by Elsevier|under license by AIP|by AIP Publishing)", re.I),
    re.compile(r"^Reuse of AIP Publishing content is subject to the terms", re.I),
    re.compile(r"^Review of Scientific Instruments\s+ARTICLE", re.I),
    re.compile(r"^Rev\.\s*Sci\.\s*Instrum\.\s+\d+,\s*\d+\s*\(20\d\d\)", re.I),
    re.compile(r"^REVIEW OF SCIENTIFIC INSTRUMENTS\s+\d+,", re.I),
    re.compile(r"^Cite as:\s*Rev\.\s*Sci\.\s*Instrum\.", re.I),
    re.compile(r"^Submitted:\s*\d+\s+\w+\s+20\d\d", re.I),
    re.compile(r"^\(Received\s+\d+\s+\w+\s+20\d\d;\s*accepted", re.I),
    re.compile(r"^Received\s*:?\s*\d+\s+\w+\s+20\d\d\s*[;,]\s*(?:revised|accepted)", re.I),
    re.compile(r"^Article history:\s*Received", re.I),
    re.compile(r"^ARTICLE HISTORY\s*Received", re.I),
    re.compile(r"^Contents lists available at ScienceDirect$", re.I),
    re.compile(r"^journal homepage:\s*www\.elsevier\.com", re.I),
    re.compile(r"^(?:Tribology International|Wear)\s+\d+\s*\(20\d\d\)\s*\d+", re.I),
    re.compile(r"^W\.\s*Ren\s+et\s+al\.\s*/\s*(?:Tribology\s+International|Wear)\b", re.I),
    re.compile(r"^THE JOURNAL OF ADHESION\b", re.I),
    re.compile(r"^Plasma Science and Technology,\s*Vol\.", re.I),
    re.compile(r"^\d*\s*IEICE TRANS\.\s*ELECTRON\.", re.I),
    re.compile(r"^\d*\s*IEEE TRANSACTIONS ON\s+(?:COMPONENTS|ELECTRON|INDUSTRIAL)", re.I),
    re.compile(r"^2020 11th International Conference on Prognostics", re.I),
    re.compile(r"^2166-5656/20/", re.I),
    re.compile(r"^(?:REN(?:\s+Wanbin)?|ZHANG|ZHOU|W\.\s*Ren|C\.\s*Zhang|X\.\s*Zhang|Wanbin\s+Ren)\s+et al\.\s*:", re.I),
    re.compile(r"^Ren et al\.\s+Effects of frequency on the intermittent", re.I),
    re.compile(r"^Manuscript received\b", re.I),
    re.compile(r"^(?:\*|n|a\))\s*(?:Corresponding author|Author to whom correspondence|E-?mail)", re.I),
    re.compile(r"^Corresponding author:\s*Wanbin Ren", re.I),
    re.compile(r"^E-?mail(?: addresses)?:\s*renwanbin@hit\.edu\.cn", re.I),
    re.compile(r"^CONTACT\s+Wanbin Ren\s+renwanbin@hit\.edu\.cn", re.I),
    re.compile(r"^[†∗*]\s*(?:The authors are with|supported by National Natural Science)", re.I),
    re.compile(r"^The authors are with (?:the )?School of Electrical Engineering", re.I),
    re.compile(r"^This work was supported (?:in part )?by (?:the )?National Natural Science", re.I),
    re.compile(r"^\(Some (?:ﬁgures|figures) may appear in colour only", re.I),
    re.compile(r"^PACS:\s*\d", re.I),
    re.compile(r"^\d+\s+of\s+\d+$", re.I),
    re.compile(r"^\d+,\s*\d{6}-\d+$"),
    re.compile(r"^2016\s+13:42:18$"),
]

# Whole-block footnote patterns on the first content page
PAGE1_FOOTNOTE_BLOCK_RE = re.compile(
    r"(?:Manuscript received\b|"
    r"Date of publication\b|"
    r"Date of current version\b|"
    r"This work was supported (?:in part )?by\b|"
    r"The review of this paper was arranged by Editor\b|"
    r"The associate editor coordinating the review\b|"
    r"Corresponding (?:author|e-mail)\s*:\s*(?:Wanbin Ren|renwanbin)|"
    r"\(corresponding author:\s*Wanbin Ren\)|"
    r"are with (?:the )?School of Electrical Engineering and Automation|"
    r"is with (?:the )?(?:School of Electronics|Department of Electrical|State Grid|G&A Electronics)|"
    r"Harbin Institute of Technology,\s*Harbin(?:,\s*150001)?,\s*China\s*\((?:e-mail|Corresponding)|"
    r"^AFFILIATIONS\b|"
    r"^[1-3a-c†]*\s*School of Electrical Engineering and Automation|"
    r"^[123]\.\s*(?:School of|G&A Electronics|Chixi Technology|AVIC Beijing)|"
    r"^online at http://ieeexplore\.ieee\.org|"
    r"Elsevier Ltd\.\s*All rights reserved)",
    re.I,
)

# Stop markers (end of main body text)
STOP_HEADING_RE = re.compile(
    r"^(?:[IVX]+\.?\s+|[1-9]\.?\s+)?(?:REFERENCES|References|Literature|APPENDIX|Appendix|ACKNOWLEDGMENTS?|Acknowledgments?|Acknowledgements?)\b"
)

# Introduction heading marker
INTRO_HEADING_RE = re.compile(
    r"^(?:I\.?\s*INTRODUCTION|1\.?\s*Introduction|Introduction)\b"
)

# Valid section / subsection heading start
HEADING_START_RE = re.compile(
    r"^(?:[IVX]{1,4}\.?\s+[A-Z][A-Za-z]|[1-6](?:\.\d+)?\.?\s+[A-Z][A-Za-z]|[A-F]\.\s+[A-Z][A-Za-z]|"
    r"(?:Abstract|ABSTRACT|SUMMARY|a\s+b\s+s\s+t\s+r\s+a\s+c\s+t\s*s?|"
    r"Introduction|INTRODUCTION|Experimental\s+(?:details|setup|methods?)|"
    r"Results\s+and\s+(?:discussions?|analysis)|Conclusion|Conclusions|CONCLUSION|CONCLUSIONS)\b)"
)

# Figure / Table caption markers (excludes prose sentences like "Fig. 2 shows...", "Figure 5 illustrates...")
CAPTION_RE = re.compile(
    r"^(?:Fig(?:ure)?s?\.?\s*\d+|TABLE\s+[IVX\d]+|Table\s+[IVX\d]+)\b"
    r"(?!\s*(?:\([a-z]\)|[a-z])?(?:\s*(?:and|–|-|,)\s*(?:Fig(?:ure)?s?\.?\s*)?\d*(?:\([a-z]\)|[a-z])?)*"
    r"\s+(?:shows?|illustrates?|depicts?|presents?|plots?|gives?|compares?|demonstrates?|"
    r"indicates?|reveals?|lists?|summarizes?|describes?|is|are|can|has|have)\b)",
    re.I,
)
# P05 uses bare numbers for figure captions: "1 Experimental apparatus...", "6 Variation in..."
P05_CAPTION_RE = re.compile(
    r"^[1-8]\s+[A-Z][A-Za-z\s\-]+"
)


def is_noise_line(line: str, repeated_lines: set[str]) -> bool:
    s = " ".join(line.split()).strip()
    if not s:
        return True
    if s in repeated_lines:
        return True
    for pat in STRIP_LINE_PATTERNS:
        if pat.search(s):
            return True
    return False


def clean_block_lines(
    raw_text: str,
    page_idx: int,
    y0: float,
    y1: float,
    page_h: float,
    repeated_lines: set[str],
) -> str:
    """Strip running headers/footers/banners and page-1 footnote blocks."""
    flat_raw = " ".join(raw_text.split()).strip()
    if not flat_raw:
        return ""
    # Whole-block check for page-1 footnotes, affiliations, keywords, article info
    if page_idx == 0:
        if re.match(r"^(?:Keywords|Key\s*words|INDEX\s+TERMS|Index\s+Terms|a\s+r\s+t\s+i\s+c\s+l\s+e\s+i\s+n\s+f\s+o)\b", flat_raw, re.I):
            return ""
        if PAGE1_FOOTNOTE_BLOCK_RE.search(flat_raw) and not re.search(r"\b(?:Abstract|ABSTRACT|SUMMARY|INTRODUCTION|Introduction)\b", flat_raw):
            return ""
    if y0 > page_h * 0.72 and PAGE1_FOOTNOTE_BLOCK_RE.search(flat_raw):
        return ""
    if "Check the adjusted references" in flat_raw:
        return ""

    lines = [ln for ln in raw_text.splitlines() if ln.strip()]
    kept: list[str] = []
    for ln in lines:
        s = " ".join(ln.split()).strip()
        if not s:
            continue
        if len(lines) == 1 and (y0 < 65 or y1 > page_h - 65) and re.fullmatch(r"\d{1,4}", s):
            continue
        if is_noise_line(s, repeated_lines):
            continue
        kept.append(ln.rstrip())
    text = "\n".join(kept).strip()
    if not text:
        return ""
    flat = " ".join(text.split())
    if flat in ("Transactions on Industrial Electronics", "Transactions on Components, Packaging and Manufacturing Technology"):
        return ""
    return text


def classify_block_role(
    text: str,
    paper_id: str,
    page_idx: int,
    bbox: tuple[float, float, float, float],
    before_intro: bool,
    just_saw_intro: bool,
) -> str:
    """Classify a block into 'caption' | 'equation' | 'frontmatter' | 'body'."""
    flat = " ".join(text.split()).strip()
    if not flat:
        return "noise"
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0

    # Vertical rotated axis labels (e.g. "Contact resistance(ohm)", "Voltage drop(V)")
    if w < 22 and h > 20 and len(flat) > 2:
        return "caption"

    if CAPTION_RE.match(flat) or (paper_id == "P05" and P05_CAPTION_RE.match(flat)):
        return "caption"
    # Subfigure labels like "(a)", "(b)", "(a) Rider, (b) Coupon"
    if re.fullmatch(r"(?:\([a-f]\)\s*[A-Za-z0-9\s,./\-:()]*)+", flat) and len(flat) < 80:
        return "caption"

    if before_intro and page_idx == 0:
        if re.match(r"^(?:Abstract|ABSTRACT|SUMMARY|a\s+b\s+s\s+t\s+r\s+a\s+c\s+t\s*s?)\b", flat):
            return "body"
        n_words = len(re.findall(r"[A-Za-z]{2,}", flat))
        if n_words >= 45:
            return "body"
        return "frontmatter"

    # Drop-cap single uppercase letter right after I. INTRODUCTION on page 1
    if re.fullmatch(r"[A-Z]", flat):
        return "body" if (page_idx == 0 and just_saw_intro) else "caption"

    if HEADING_START_RE.match(flat):
        if not re.search(r"\b[2-9]\.\s+[A-Z]", flat[4:]) and not re.match(
            r"^\d+(?:\.\d+)?\s*(?:mm|μm|µm|nm|mA|kHz|MHz|V|A|N|Hz|%|shows|In\s+addition|In\s+the\s+case)\b",
            flat,
        ):
            return "body"

    alpha_words = re.findall(r"[A-Za-z]{3,}", flat)
    has_eq_num = bool(re.search(r"(?:\(\d+[a-z]?\)|ð\d+[a-z]?Þ|\(A-\d+\))\s*$", flat))
    has_eq_op = bool(re.search(r"[=¼\uf03d≈\uf0bb≤≥\uf0a3\uf0b9∑∫\uf0e5\uf0f2]", text))

    if has_eq_num and len(alpha_words) <= 8:
        return "equation"
    if has_eq_op and len(alpha_words) <= 4 and len(flat) < 140:
        return "equation"

    # Detect multi-line table / schematic callout blocks (short lines, no prose sentences)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if lines:
        max_line_len = max(len(ln) for ln in lines)
        avg_line_len = sum(len(ln) for ln in lines) / len(lines)
        has_sentence_verb = bool(re.search(
            r"\b(?:is|are|was|were|be|been|have|has|had|can|could|will|would|may|might|"
            r"shows?|shown|indicates?|demonstrates?|presents?|results?|increases?|decreases?|"
            r"occurs?|consists?|leads?|causes?|means?|appears?|remains?|becomes?|reaches?|"
            r"corresponds?|relates?|depends?|plays?|measured|calculated|obtained|observed|"
            r"investigated|analyzed|studied|used|applied|set|carried|found|determined)\b",
            flat,
            re.I,
        ))
        if not has_sentence_verb and max_line_len < 34 and avg_line_len < 24:
            return "caption"

    if len(alpha_words) <= 2 and not flat.endswith(".") and len(flat) < 50:
        return "caption"
    return "body"


def sort_page_blocks(
    blocks: list[tuple],
    page_w: float,
    is_first_content_page: bool,
    single_col: bool,
) -> tuple[list[tuple], float]:
    """Return (ordered blocks, y_intro)."""
    mid = page_w / 2.0
    if single_col:
        filtered = [
            b for b in blocks
            if not (is_first_content_page and b[0] > page_w * 0.62 and b[1] < 340)
        ]
        return sorted(filtered, key=lambda b: (round(b[1] / 6.0), b[0])), 0.0

    if is_first_content_page:
        y_intro = 9999.0
        for b in blocks:
            flat = " ".join(b[4].split()).strip()
            if INTRO_HEADING_RE.match(flat):
                y_intro = min(y_intro, b[1])
                break
        if y_intro < 9999.0:
            pre_intro = []
            left_col = []
            right_col = []
            for b in blocks:
                x0, y0, x1, y1 = b[0], b[1], b[2], b[3]
                if y0 < y_intro - 4 and x0 < mid - 25:
                    pre_intro.append(b)
                elif x0 < mid - 25 and x1 <= mid + 45:
                    left_col.append(b)
                elif x0 >= mid - 25:
                    if y0 < 200 and x0 < mid - 60:
                        pre_intro.append(b)
                    elif y0 < 195 and (x0 + x1) / 2.0 < mid + 30 and y_intro > 350:
                        pre_intro.append(b)
                    else:
                        right_col.append(b)
                else:
                    left_col.append(b)
            pre_intro.sort(key=lambda b: (round(b[1] / 8.0), b[0]))
            left_col.sort(key=lambda b: (b[1], b[0]))
            right_col.sort(key=lambda b: (b[1], b[0]))
            return pre_intro + left_col + right_col, y_intro

    def _is_right_col(b: tuple) -> bool:
        if "Reuse of AIP Publishing content" in b[4] and len(b[4].splitlines()) > 2:
            return True
        return (b[0] + b[2]) / 2.0 >= mid

    left = [b for b in blocks if not _is_right_col(b)]
    right = [b for b in blocks if _is_right_col(b)]
    left.sort(key=lambda b: (b[1], b[0]))
    right.sort(key=lambda b: (b[1], b[0]))
    return left + right, 0.0


def extract_paper(paper: Paper, out_dir: Path) -> dict[str, Any]:
    if not paper.pdf or not paper.pdf.exists():
        raise FileNotFoundError(f"Missing PDF for {paper.id}")

    skip_pages = set(paper.meta.get("skip_pages") or [])
    single_col = paper.id in SINGLE_COLUMN_PAPERS

    with pymupdf.open(paper.pdf) as doc:
        content_page_indices = [
            i for i in range(len(doc))
            if (i + 1) not in skip_pages
        ]
        line_counts: Counter[str] = Counter()
        for idx in content_page_indices:
            seen_on_page: set[str] = set()
            for b in doc[idx].get_text("blocks"):
                if b[6] != 0:
                    continue
                for ln in b[4].splitlines():
                    s = " ".join(ln.split()).strip()
                    if 3 <= len(s) <= 120:
                        seen_on_page.add(s)
            for s in seen_on_page:
                line_counts[s] += 1
        min_repeat = max(3, len(content_page_indices) // 2)
        repeated_lines = {
            s for s, c in line_counts.items()
            if c >= min_repeat and not re.match(r"^(?:[IVX]+\.|[1-9]\.|Fig|Table|Abstract|Introduction|Conclusion)", s, re.I)
        }

        extracted_blocks: list[dict[str, Any]] = []
        captions: list[dict[str, Any]] = []
        stop_reached = False

        for rel_idx, page_idx in enumerate(content_page_indices):
            if stop_reached:
                break
            page = doc[page_idx]
            page_w, page_h = page.rect.width, page.rect.height
            raw_blocks = [b for b in page.get_text("blocks") if b[6] == 0 and b[4].strip()]
            ordered, y_intro = sort_page_blocks(
                raw_blocks,
                page_w=page_w,
                is_first_content_page=(rel_idx == 0),
                single_col=single_col,
            )

            seen_intro_on_page0 = False
            just_saw_intro = False
            for b in ordered:
                x0, y0, x1, y1, raw_txt = b[0], b[1], b[2], b[3], b[4]
                cleaned = clean_block_lines(raw_txt, rel_idx, y0, y1, page_h, repeated_lines)
                if not cleaned:
                    continue

                kept_lines: list[str] = []
                for ln in cleaned.splitlines():
                    s_ln = " ".join(ln.split()).strip()
                    if rel_idx >= 1 and STOP_HEADING_RE.match(s_ln) and len(s_ln) < 45:
                        stop_reached = True
                        break
                    kept_lines.append(ln)
                cleaned = "\n".join(kept_lines).strip()
                if not cleaned:
                    if stop_reached:
                        break
                    continue

                flat = " ".join(cleaned.split()).strip()
                if rel_idx == 0 and INTRO_HEADING_RE.match(flat):
                    seen_intro_on_page0 = True
                    just_saw_intro = True
                    before_intro = False
                else:
                    before_intro = (rel_idx == 0) and (not seen_intro_on_page0) and (y0 < y_intro - 4 if y_intro else True)

                role = classify_block_role(
                    cleaned,
                    paper.id,
                    rel_idx,
                    (x0, y0, x1, y1),
                    before_intro,
                    just_saw_intro,
                )
                if not INTRO_HEADING_RE.match(flat) and not re.fullmatch(r"[A-Z]", flat):
                    just_saw_intro = False

                col = 0 if single_col or (x0 + x1) / 2.0 < page_w / 2.0 else 1
                rec = {
                    "page": page_idx + 1,
                    "col": col,
                    "bbox": [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)],
                    "role": role,
                    "text": cleaned,
                }
                if role == "caption":
                    captions.append(rec)
                elif role in ("body", "equation", "frontmatter"):
                    extracted_blocks.append(rec)

                if stop_reached:
                    break

    payload = {
        "paper_id": paper.id,
        "pdf_file": paper.pdf.name,
        "single_column": single_col,
        "blocks": extracted_blocks,
        "captions": captions,
    }
    json_path = out_dir / f"{paper.id}.blocks.json"
    txt_path = out_dir / f"{paper.id}.txt"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    txt_parts: list[str] = []
    for blk in extracted_blocks:
        if blk["role"] == "frontmatter":
            continue
        if blk["role"] == "equation":
            if not txt_parts or txt_parts[-1] != "[EQ]":
                txt_parts.append("[EQ]")
        else:
            txt_parts.append(blk["text"])
    txt_path.write_text("\n\n".join(txt_parts) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="paper IDs to process")
    args = ap.parse_args()
    cfg = load_config()
    out_dir = data_dir(cfg) / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    papers = resolve_papers(cfg)
    for p in papers:
        if args.only and p.id not in args.only:
            continue
        payload = extract_paper(p, out_dir)
        n_body = sum(1 for b in payload["blocks"] if b["role"] == "body")
        n_eq = sum(1 for b in payload["blocks"] if b["role"] == "equation")
        n_cap = len(payload["captions"])
        print(f"{p.id}: body_blocks={n_body:3d}  eq_blocks={n_eq:2d}  captions={n_cap:2d} -> {out_dir / (p.id + '.txt')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

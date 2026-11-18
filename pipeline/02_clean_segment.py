"""Phase 1.3 — Clean extracted text and segment into sections / paragraphs.

Fixes all extraction issues listed in docs/design_notes.md §2.3:
  1. Elsevier letter-spaced headings ("a b s t r a c t", "a r t i c l e i n f o")
  2. Corrupted symbols ("25\\u0001125 1C" -> "25–125 °C", "71 1C" -> "±1 °C",
     "accuracy of 71%" -> "accuracy of ±1%", Elsevier math font ¼/þ/ð/Þ,
     Windows Symbol PUA \\uf020-\\uf0ff, P29 subset-font cipher, middle-dot decimals)
  3. Ligatures (ﬁ ﬂ ﬀ ﬃ ﬄ) and line-end hyphenated word breaks ("mea- suring" -> "measuring")
  4. Publisher cover pages (handled in 01_extract_pdf.py)
  5. IEEE accepted-manuscript banners & running headers/footers
  6. Drop-caps ("LECTROMECHANICAL" -> "Electromechanical", etc.) & one-word-per-line blocks
  7. Two-column ordering, figure/table separation, and placeholders:
     equations -> [EQ], citations -> [CIT], figure refs -> [FIG n]

Outputs:
  - ``data/processed/paragraphs.jsonl``:
    {paper_id, tier, weight, effective_weight, split, section, heading, para_idx, text, n_words}
  - ``data/processed/fix_log.json``: per-paper log of repairs and section mappings.

Usage:
    python pipeline/02_clean_segment.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from common import Paper, data_dir, effective_weight, load_config, resolve_papers

# 1. Ligature replacements
LIGATURES = {
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb03": "ffi",
    "\ufb04": "ffl",
    "\u00ad": "",  # soft hyphen
    "\u200b": "",  # zero-width space
    "\ufeff": "",  # BOM
}

# 2. Windows Symbol PUA (0xF000..0xF0FF) -> Unicode
PUA_MAP = {
    "\uf020": " ",
    "\uf026": "&",
    "\uf02b": "+",
    "\uf02d": "−",
    "\uf03d": "=",
    "\uf044": "Δ",
    "\uf047": "γ",
    "\uf057": "Ω",
    "\uf061": "α",
    "\uf062": "β",
    "\uf064": "δ",
    "\uf067": "γ",
    "\uf06a": "φ",
    "\uf06c": "•",
    "\uf06d": "μ",
    "\uf070": "π",
    "\uf072": "ρ",
    "\uf077": "ω",
    "\uf0a3": "≤",
    "\uf0a5": "∞",
    "\uf0b4": "×",
    "\uf0b6": "∂",
    "\uf0b9": "≠",
    "\uf0bb": "≈",
    "\uf0d7": "⋅",
    "\uf0e5": "∑",
    "\uf0f2": "∫",
}

# 3. P29 page 4 subset-font cipher replacements
P29_CIPHER_FIXES = [
    (
        "betwee\x08\t \x06\n\x0b\x0c\x07\t \r\x08\x0e\t \x06\n\x0b\x0f\x0c\x07\n\t \x10\x11\t \x11\x12\x13\x14\x08\t \x15\x08\t \x16\x15\x17\n\x0f\x18\t \x19\x12\x1a\t \x1b\x1c\x1a\r\x1d\t",
        "between 1.5 mΩ and 1.57 mΩ. As shown in Fig. 7, the clear ",
    ),
    (
        "T\x12\x1a\x1d\x1a\t \x15\x11\t \x11\x0c\r\x1c\x1c\t \x1e\x1c\x1f\x1b\x19\x1f\r\x19\x15\x13\x08\t !\x1a\x19\x14\x1a\x1a\x08\t \x06\n\"\x05\x0c\x07\t \r\x08\x0e\t\n\x06\n\x0b\x0f\x0c\x07\t\x15\x08\t\x1b\x13\x08\x19\r\x1b\x19\t\x1d\x1a\x11\x15\x11\x19\r\x08\x1b\x1a",
        "There is small fluctuation between 1.48 mΩ and 1.57 mΩ in contact resistance.",
    ),
    (
        "In Zone #\x18\t\x19\x12\x1a\t\x1e\x1d\x1a$\x1f\x1a\x08\x19\t\x1e\x1c\x1f\x1b\x19\x1f\r\x19\x15\x13\x08\x11\t\x13\x1b\x1b\x1f\x1d\x11\t\x15\x08",
        "In Zone III, the frequent fluctuations occur in",
    ),
    ("19\x02\x03\x042\x02", "19 °C ± 2 °C"),
]

# 4. Drop-cap word repairs (when initial capital letter was separated or lost)
DROP_CAP_FIXES = [
    (re.compile(r"^(?:N\s+)?OWADAYS\b"), "Nowadays"),
    (re.compile(r"^(?:E\s+)?LECTRICAL\b"), "Electrical"),
    (re.compile(r"^(?:T\s+)?HE\s+ELECTRICAL\b"), "The electrical"),
    (re.compile(r"^(?:T\s+)?HE\s+electrical\b"), "The electrical"),
    (re.compile(r"^(?:I\s+)?NTEREST\b"), "Interest"),
    (re.compile(r"^(?:M\s+)?ICROELECTROMECHANICAL\b"), "Microelectromechanical"),
    (re.compile(r"^(?:L\s+)?ONG\b"), "Long"),
    (re.compile(r"^(?:E\s+)?LECTRODYNAMIC\b"), "Electrodynamic"),
    (re.compile(r"^(?:A\s+)?T\s+PRESENT\b"), "At present"),
    (re.compile(r"^(?:E\s+)?LECTROMECHANICAL\b"), "Electromechanical"),
]

# 5. Compound prefixes/words that should KEEP their hyphen when broken at end of line
ALWAYS_HYPHENATED = {
    "in-situ", "real-time", "steady-state", "open-circuit", "closed-loop", "solid-state",
    "three-dimensional", "two-dimensional", "one-dimensional", "cross-section",
    "cross-sectional", "well-known", "so-called", "high-frequency", "high-speed",
    "high-reliability", "high-current", "low-cost", "low-current", "low-profile",
    "long-term", "long-life", "long-lifetime", "short-term", "short-time", "short-duration",
    "non-conforming", "non-welding", "self-designed", "self-healing", "self-leveling",
    "finite-element", "four-wire", "four-wires", "over-travel", "switch-on", "switch-off",
    "off-isolation", "re-open", "re-melt", "re-separation", "inter-molecular",
    "micro-motion", "micro-adhesion", "nano-scale", "semi-infinite", "semi-melting",
    "quasi-static", "stick-slip", "point-on", "run-to", "above-mentioned", "built-in",
    "zoomed-in", "curve-fit", "bow-type", "flake-like", "dust-tight", "gas-insulated",
    "single-contact", "two-contact", "multiple-contact", "single-asperity", "single-point",
    "general-purpose", "general-purposed", "current-carrying", "contact-making",
    "contact-breaking", "slow-making", "sweeping-frequency", "energy-dispersive",
    "solid-liquid", "voltage-drop", "voltage-temperature", "oxidation-dominated",
    "vibration-control", "anti-welding", "nearest-neighboring", "Sub-bridges", "sub-bridges",
}
KEEP_HYPHEN_PREFIXES = {
    "self", "non", "anti", "semi", "multi", "micro", "macro", "nano", "super",
    "ultra", "cross", "quasi", "well", "ill", "high", "low", "long",
    "short", "single", "double", "triple", "two", "three", "four", "one", "first",
    "second", "third", "all", "over", "under", "up", "down",
    "out", "off", "on", "by", "counter", "time", "size", "load", "current",
    "voltage", "contact", "gold", "silver", "copper", "tin", "nickel", "metal",
    "oxide", "surface", "spring", "rod", "ball", "sphere", "flat", "line", "point",
    "finite", "thermo", "mechano", "elasto", "plastic", "piezo", "steady",
    "open", "closed", "make", "stitch", "step", "run", "real", "full",
    "half", "hand", "base", "end", "side", "top", "bottom", "left", "right", "axis",
    "x", "y", "z", "a", "b", "c", "dc", "ac", "rf", "fe", "fem", "3d", "2d",
}
KEEP_HYPHEN_SUFFIXES = {
    "based", "plated", "coated", "shaped", "sized", "type", "like", "free", "induced",
    "driven", "controlled", "dependent", "independent", "related", "oriented", "scale",
    "level", "order", "stage", "phase", "mode", "spot", "spots", "making",
    "carrying", "loading", "unloading", "sliding", "rolling", "heating", "cooling",
    "melting", "welding", "opening", "closing", "coupled", "dimensional", "element",
    "section", "sectional", "state", "term", "time", "hand", "situ", "isolation",
    "on", "off", "up", "down", "in", "out", "to", "peak", "peaks", "drop", "plane",
    "most", "width", "circuit", "ray", "rays",
}


def dehyphenate(text: str, fixes: Counter[str], corpus_vocab: set[str]) -> str:
    """Repair line-end hyphenated word breaks ('mea-\\nsuring' or 'mea- suring')."""
    def _join_match(m: re.Match) -> str:
        w1, w2 = m.group(1), m.group(2)
        p1, p2 = w1.lower(), w2.lower()
        hyphenated = f"{p1}-{p2}"
        joined = f"{p1}{p2}"
        if not w1.isalpha() or (w1[0].isupper() and w1.isupper()):
            return f"{w1}-{w2}"
        if hyphenated in ALWAYS_HYPHENATED:
            return f"{w1}-{w2}"
        # If the unhyphenated word is attested in the corpus vocabulary, join it
        if joined in corpus_vocab and p1 not in ("a", "b", "c", "x", "y", "z", "non", "self"):
            fixes["dehyphenated"] += 1
            return f"{w1}{w2}"
        if p1 in KEEP_HYPHEN_PREFIXES or p2 in KEEP_HYPHEN_SUFFIXES:
            return f"{w1}-{w2}"
        fixes["dehyphenated"] += 1
        return f"{w1}{w2}"

    # Across newline first
    text = re.sub(r"\b([A-Za-z]{2,})-\s*\n\s*([a-z]{2,})\b", _join_match, text)
    # Also intra-line "<frag>- <frag>" caused by PDF justification
    text = re.sub(r"\b([A-Za-z]{2,})-\s+([a-z]{2,})\b", _join_match, text)
    # Also inline broken words without spaces where joined form is standard
    text = re.sub(r"\bcon-focal\b", "confocal", text, flags=re.I)
    return text


def clean_symbols(text: str, paper_id: str, fixes: Counter[str]) -> str:
    """Repair ligatures, broken symbols, Elsevier math font chars, and PUA glyphs."""
    if paper_id == "P29":
        for bad, good in P29_CIPHER_FIXES:
            if bad in text:
                text = text.replace(bad, good)
                fixes["p29_cipher"] += 1

    for k, v in LIGATURES.items():
        if k in text:
            cnt = text.count(k)
            text = text.replace(k, v)
            fixes["ligatures"] += cnt

    for k, v in PUA_MAP.items():
        if k in text:
            cnt = text.count(k)
            text = text.replace(k, v)
            fixes["pua_symbols"] += cnt

    # Remove remaining PUA box-drawing / brace pieces (\uf0e6..\uf8ff)
    text, n_pua = re.subn(r"[\ue000-\uf8ff]", " ", text)
    if n_pua:
        fixes["pua_stripped"] += n_pua

    # Elsevier & IEEE broken symbol patterns (design_notes §2.3)
    # e.g., "25\x01125 1C" -> "25–125 °C", "71 1C" -> "±1 °C", "accuracy of 71%" -> "accuracy of ±1%"
    text, n = re.subn(r"\b71\s*1C\b", "±1 °C", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"(accuracy\s+of\s+)71%", r"\1±1%", text, flags=re.I)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"\b6172%", "61±2%", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"\b8000\s+10,000,", "8000, 10,000,", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"(\d)\s*\x01\s*(\d)", r"\1–\2", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"(?<=\d)\s*1C\b", " °C", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"(\d+)\s*m[\x02\t]\b", r"\1 mΩ", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"(\d+(?:\s*[×x]\s*10[−-]?\d+)?)\s*[\x05\x08]m\b", r"\1 Ω·m", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"10[\x02\x05](\d+)", r"10−\1", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"(\d+(?:[:.]\d+)?(?:\s*(?:μm|µm|mm|nm|cm|m))?)\s*[\x03\x04]\s*(\d)", r"\1 × \2", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"[\x02\x03\x07]t\b", "Δt", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"\x07T\b", "ΔT", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"[‘']\x02[’']", "‘×’", text)
    fixes["broken_symbols"] += n
    text, n = re.subn(r"^\s*[\x03•]\s+", "• ", text, flags=re.M)
    fixes["broken_symbols"] += n

    # Elsevier math font in inline text: ¼ -> =, þ -> +, ð -> (, Þ -> ), 16:5 -> 16.5
    if "¼" in text or "ð" in text or "Þ" in text or "þ" in text:
        text = text.replace("¼", " = ").replace("þ", " + ").replace("ð", "(").replace("Þ", ")")
        text = re.sub(r"(?<=\d):(?=\d)", ".", text)
        fixes["elsevier_math_chars"] += 1

    # Maney (P05) British middle-dot decimal point: 12·5 -> 12.5
    if paper_id == "P05":
        text, n = re.subn(r"(?<=\d)·(?=\d)", ".", text)
        fixes["middle_dot_decimal"] += n

    # Strip any remaining ASCII control chars (< 32 except \n, \t)
    text, n_ctrl = re.subn(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", text)
    if n_ctrl:
        fixes["ctrl_stripped"] += n_ctrl

    return text


def apply_placeholders(text: str, paper_id: str, fixes: Counter[str]) -> str:
    """Replace citations with [CIT], figure refs with [FIG n], and inline corrupted math with [EQ]."""
    # 1. Figure references: "Figs. 3 and 4", "Fig. 3(a)", "Figure 3a", "Fig.3"
    def _fig_pair(m: re.Match) -> str:
        fixes["fig_placeholders"] += 2
        return f"[FIG {m.group(1)}] and [FIG {m.group(2)}]"

    text = re.sub(
        r"\bFig(?:ure)?s?\.?\s*(\d+)(?:\([a-z]\)|[a-z])?\s+and\s+\(?(\d+)(?:\([a-z]\)|[a-z])?\)?",
        _fig_pair,
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\bFig(?:ure)?s?\.?\s*(\d+)\s*\(?[a-f]\)?\s+and\s+\(?[a-f]\)?",
        lambda m: f"[FIG {m.group(1)}]",
        text,
        flags=re.I,
    )

    def _fig_single(m: re.Match) -> str:
        fixes["fig_placeholders"] += 1
        return f"[FIG {m.group(1)}]"

    text = re.sub(
        r"\bFig(?:ure)?s?\.?\s*\(?(\d+)\)?(?:\s*\([a-f]\)|[a-f]\b)?",
        _fig_single,
        text,
        flags=re.I,
    )

    # 2. Bracketed citations: "[1]", "[1, 2]", "[1–3]", "[1]-[3]"
    text, n_cit = re.subn(
        r"\[(?:\d+\s*(?:[–\-−,]\s*\d+\s*)*)\](?:\s*[–\-−,]\s*\[(?:\d+\s*(?:[–\-−,]\s*\d+\s*)*)\])*",
        "[CIT]",
        text,
    )
    fixes["cit_placeholders"] += n_cit

    # 3. Superscript citations in P05, P12, P25:
    #    - attached to punctuation after a word/paren (never after a digit, so "0.15 N" is untouched):
    #      "discontinuities.2", "extent.11,12", "Hz.4–10", "bounce,6,9–13"
    if paper_id in ("P05", "P12", "P25"):
        text, n_sup1 = re.subn(
            r"(?<=[A-Za-z)])([.,;])(\d{1,2}(?:[–\-−,]\d{1,2})*)(?=\s+[A-Z]|\s*$)",
            r"\1 [CIT]",
            text,
        )
        fixes["cit_placeholders"] += n_sup1
        #    - attached to author name / "et al." before a reporting verb
        text, n_sup2 = re.subn(
            r"\b(et\s+al\.|[A-Z][a-zA-Z\-]{2,})(\d{1,2}(?:[–\-−,]\d{1,2})*)"
            r"(?=\s+(?:investigated|researched|found|recorded|evaluated|proposed|presented|"
            r"reported|studied|examined|showed|concluded|stated|suggested|observed|analyzed|"
            r"calculated|developed|had|have|has|and\b))",
            r"\1 [CIT]",
            text,
        )
        fixes["cit_placeholders"] += n_sup2

    # Ensure space after sentence-ending period before Capitalized word (e.g. "Hz.In" -> "Hz. In")
    text = re.sub(r"([a-z\d])\.(?=[A-Z][a-z])", r"\1. ", text)

    # Collapse repeated [CIT]
    text = re.sub(r"\[CIT\](?:\s*[,–\-]\s*\[CIT\])+", "[CIT]", text)
    text = re.sub(r"(\[EQ\])(?:\s*\[EQ\])+", r"\1", text)
    return text


# Heading detection & canonical section mapping (design_notes §3)
SPLIT_NUM_HEADING_RE = re.compile(
    r"^(?P<num>[IVX]{1,4}\.|[1-6](?:\.\d+)?\.?)\s*\n+\s*(?P<title>[A-Z][A-Za-z0-9\s,&/\-–()]{2,80})$"
)

INLINE_HEADING_PATTERNS = [
    # Abstract—..., ABSTRACT ..., SUMMARY ...
    re.compile(r"^(?P<head>Abstract|ABSTRACT|SUMMARY)\s*(?:[—–\-:]|\s+)\s*(?P<body>[A-Z].+)$", re.S),
    # I. INTRODUCTION\n..., II. EXPERIMENTAL DETAILS\nA. TEST RIG\n..., V. CONCLUSION\n...
    re.compile(
        r"^(?P<head>(?:[IVX]{1,4}\.|[1-6](?:\.\d+)?\.?|[A-F]\.)\s+[A-Z][A-Z0-9\s,&/\-–()]{2,75}?)\s*\n+\s*(?P<body>.+)$",
        re.S,
    ),
]

STANDALONE_HEADING_RE = re.compile(
    r"^(?:"
    r"a\s+b\s+s\s+t\s+r\s+a\s+c\s+t\s*s?|"
    r"Abstract|ABSTRACT|SUMMARY|"
    r"(?:[IVX]{1,4}\.?\s+|[1-6](?:\.\d+)?\.?\s+|[A-F]\.\s+)"
    r"[A-Z][A-Za-z0-9\s,&/\-–()]{2,90}|"
    r"Introduction|INTRODUCTION|"
    r"Experimental\s+(?:details|setup|methods?)|"
    r"Results\s+and\s+(?:discussions?|analysis)|"
    r"Conclusions?|CONCLUSIONS?"
    r")$"
)


def is_subsection_heading(heading: str) -> bool:
    h = " ".join(heading.split()).strip()
    return bool(re.match(r"^(?:[1-6]\.\d+\.?|[A-F]\.)\s+", h))


def classify_heading(heading: str, current_section: str | None, top_section: str | None) -> tuple[str, str | None]:
    """Map a section or subsection heading to one of the 7 canonical section labels.

    Returns (new_current_section, new_top_section).
    """
    h = " ".join(heading.split()).strip()
    low = h.lower()
    is_sub = is_subsection_heading(h)

    if re.match(r"^(?:a\s*b\s*s\s*t\s*r\s*a\s*c\s*t\s*s?|abstract|summary)\b", low):
        return "abstract", "abstract"
    if "introduction" in low:
        return "introduction", "introduction"
    if any(k in low for k in ("conclusion", "conclusions", "summary and conclusion")):
        return "conclusion", "conclusion"

    # Explicit mechanism keywords (apply to both top-level and subsection headings)
    if any(k in low for k in (
        "failure mechanism", "physical mechanism", "wear mechanism", "mechanism analysis",
        "discussion of failure", "capillary force of molten bridge",
        "dominant roles in different operation", "role of bounce arc",
        "role of molten bridge", "multiple roles of bounce",
    )):
        return "mechanism", (top_section if is_sub else "mechanism")

    # Explicit experimental keywords
    if any(k in low for k in (
        "experimental details", "experimental setup", "experimental method",
        "experiment methods", "experimental condition", "test rig",
        "description of the test rig", "description of the new test rig",
        "description of general-purpose relay", "flexible spring components description",
        "measurement of welding force",
    )):
        return "experimental", (top_section if is_sub else "experimental")

    # If this is a subsection under an already-established top_section:
    if is_sub and top_section:
        if top_section in ("modeling", "experimental") and any(k in low for k in (
            "experimental results", "validity of", "evaluation of", "reconstruction of",
            "relationship between contact sliding", "discussion of ecr",
        )):
            return "results", top_section
        return top_section, top_section

    if any(k in low for k in (
        "theoretical", "analytical", "mathematical model", "simulation model",
        "finite element", "finite-element", "fem ", "modeling", "modelling",
        "structural dynamic model", "contact model", "heat conduction model",
        "determination of elliptical asperity",
    )):
        return "modeling", "modeling"

    if any(k in low for k in (
        "result", "discussion", "switching characteristics", "degradation",
        "fretting regime", "effects of", "effect of", "influence factors",
        "contact welding phenomena", "model validation",
    )):
        return "results", "results"

    fallback = top_section or current_section or "results"
    return fallback, (top_section or fallback)


def normalize_multiline_headings(text: str) -> str:
    """Join split number + title lines or 2-line ALL-CAPS headings at the top of a block."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ""
    # e.g. ["I.", "INTRODUCTION", ...] or ["3", "Results and discussion"]
    if len(lines) >= 2 and re.fullmatch(r"(?:[IVX]{1,4}\.?|[1-6](?:\.\d+)?\.?|[A-F]\.)", lines[0]):
        if re.match(r"^[A-Z][A-Za-z]", lines[1]) and len(lines[1]) < 80:
            lines = [f"{lines[0].rstrip('.')}. {lines[1]}"] + lines[2:]
    # Merge wrapped 2-line uppercase section headings (e.g. "III. FINITE ELEMENT MODELING FOR\nELECTRICAL FIELD ANALYSIS")
    if len(lines) >= 2 and re.match(r"^(?:[IVX]{1,4}\.|[1-6](?:\.\d+)?\.?)\s+[A-Z\s,&/\-–()]{4,}$", lines[0]):
        if re.fullmatch(r"[A-Z0-9\s,&/\-–()]{3,60}", lines[1]) and not re.match(r"^(?:[A-F]\.|[IVX]+\.)", lines[1]):
            lines = [f"{lines[0]} {lines[1]}"] + lines[2:]
    return "\n".join(lines)


def split_heading_and_body(text: str, fixes: Counter[str]) -> tuple[list[str], str]:
    """Extract one or more leading headings from a block and return (headings, remaining_body)."""
    text = normalize_multiline_headings(text)
    flat = " ".join(text.split()).strip()
    if re.fullmatch(r"a\s+b\s+s\s+t\s+r\s+a\s+c\s+t\s*s?", flat, re.I):
        fixes["elsevier_spaced_abstract"] += 1
        return ["Abstract"], ""

    headings: list[str] = []
    cur = text.strip()
    while cur:
        one_line = " ".join(cur.split()).strip()
        # Check if the entire remaining text is a standalone heading
        if len(one_line) <= 95 and STANDALONE_HEADING_RE.match(one_line) and not one_line.endswith("."):
            if not re.match(r"^\d+\s+(?:mm|μm|µm|nm|V|A|N|Hz|shows)\b", one_line):
                headings.append(one_line)
                cur = ""
                break
        # Check inline heading patterns (e.g. "Abstract—...", "I. INTRODUCTION\n...")
        matched = False
        for pat in INLINE_HEADING_PATTERNS:
            m = pat.match(cur)
            if m:
                h = " ".join(m.group("head").split()).strip()
                b = m.group("body").strip()
                if len(h) <= 90:
                    headings.append(h)
                    cur = b
                    matched = True
                    break
        if not matched:
            break
    return headings, cur


def build_corpus_vocab(papers: list[Paper], raw_dir: Path) -> set[str]:
    """Collect all unhyphenated lowercase words (>=4 chars) attested in the corpus."""
    counts: Counter[str] = Counter()
    for p in papers:
        bp = raw_dir / f"{p.id}.blocks.json"
        if not bp.exists():
            continue
        data = json.loads(bp.read_text(encoding="utf-8"))
        for b in data.get("blocks", []):
            txt = b.get("text", "")
            for k, v in LIGATURES.items():
                txt = txt.replace(k, v)
            for m in re.finditer(r"(?<![A-Za-z\-])[A-Za-z]{4,}(?![A-Za-z\-])", txt):
                counts[m.group(0).lower()] += 1
    return {w for w, c in counts.items() if c >= 1}


def process_paper(
    paper: Paper,
    raw_dir: Path,
    cfg: dict[str, Any],
    corpus_vocab: set[str],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    blocks_path = raw_dir / f"{paper.id}.blocks.json"
    payload = json.loads(blocks_path.read_text(encoding="utf-8"))
    raw_blocks = payload["blocks"]
    fixes: Counter[str] = Counter()
    section_log: list[dict[str, str]] = []

    # Step 1: Repair drop-cap split across blocks (e.g. "I. INTRODUCTION\nT" + "HE..." or "E" + "LECTROMECHANICAL...")
    blocks: list[dict[str, Any]] = []
    i = 0
    while i < len(raw_blocks):
        b = dict(raw_blocks[i])
        if b["role"] == "frontmatter":
            i += 1
            continue
        txt = b["text"].strip()
        # Case A: trailing single capital letter on heading block ("I. INTRODUCTION\nT")
        m_trail = re.search(r"^(.*?\bINTRODUCTION)\s*\n\s*([A-Z])\s*$", txt, re.S)
        if m_trail and (i + 1) < len(raw_blocks) and raw_blocks[i + 1]["role"] == "body":
            b["text"] = m_trail.group(1).strip()
            raw_blocks[i + 1] = dict(raw_blocks[i + 1])
            raw_blocks[i + 1]["text"] = m_trail.group(2) + raw_blocks[i + 1]["text"].lstrip()
            fixes["drop_cap_repaired"] += 1
            blocks.append(b)
            i += 1
            continue
        # Case B: standalone single capital letter block ("E" in P23)
        if re.fullmatch(r"[A-Z]", txt) and (i + 1) < len(raw_blocks) and raw_blocks[i + 1]["role"] == "body":
            raw_blocks[i + 1] = dict(raw_blocks[i + 1])
            raw_blocks[i + 1]["text"] = txt + raw_blocks[i + 1]["text"].lstrip()
            fixes["drop_cap_repaired"] += 1
            i += 1
            continue
        blocks.append(b)
        i += 1

    # Step 2: Walk blocks, extract headings, clean text, attach [EQ], and segment into raw paragraphs
    raw_paras: list[dict[str, Any]] = []
    current_section: str | None = None
    top_section: str | None = None
    current_heading: str = ""

    for b in blocks:
        if b["role"] == "equation":
            if raw_paras:
                if not raw_paras[-1]["text"].endswith("[EQ]"):
                    raw_paras[-1]["text"] = raw_paras[-1]["text"].rstrip() + " [EQ]"
                    fixes["eq_placeholders"] += 1
            continue

        txt = clean_symbols(b["text"], paper.id, fixes)
        txt = dehyphenate(txt, fixes, corpus_vocab)
        headings, body = split_heading_and_body(txt, fixes)
        for h in headings:
            new_sec, top_section = classify_heading(h, current_section, top_section)
            current_section = new_sec
            current_heading = h
            section_log.append({"heading": h, "section": new_sec})

        if not body:
            continue

        # Apply drop-cap word case normalization (e.g. "ELECTROMECHANICAL" -> "Electromechanical")
        for pat, repl in DROP_CAP_FIXES:
            if pat.search(body):
                body = pat.sub(repl, body, count=1)
                fixes["drop_cap_word_normalized"] += 1

        # Flatten one-word-per-line / multi-line wrapping within paragraph
        flat_body = " ".join(body.split()).strip()
        if not flat_body:
            continue

        # Unlabeled abstract before Introduction on Page 1 (P05, P12)
        if current_section is None:
            current_section = "abstract"
            top_section = "abstract"
            current_heading = "Abstract"
            section_log.append({"heading": "(unlabeled abstract)", "section": "abstract"})

        flat_body = apply_placeholders(flat_body, paper.id, fixes)
        flat_body = " ".join(flat_body.split()).strip()

        raw_paras.append({
            "section": current_section,
            "heading": current_heading,
            "text": flat_body,
        })

    # Step 3: Merge paragraphs that were split mid-sentence across columns, pages, or equations
    merged_paras: list[dict[str, Any]] = []
    for p in raw_paras:
        if not merged_paras:
            merged_paras.append(p)
            continue
        prev = merged_paras[-1]
        prev_txt = prev["text"].rstrip()
        cur_txt = p["text"].lstrip()
        same_sec = prev["section"] == p["section"]
        prev_incomplete = not bool(re.search(r"[.?!:;]\s*(?:\[CIT\]\s*)?$", prev_txt))
        starts_lower_or_where = bool(re.match(r"^[a-z]|^(?:where|in which|and|or)\b", cur_txt))
        if same_sec and (prev_incomplete or (prev_txt.endswith("[EQ]") and starts_lower_or_where)):
            prev["text"] = f"{prev_txt} {cur_txt}"
            fixes["merged_split_paragraphs"] += 1
        else:
            merged_paras.append(p)

    # Step 4: Build final paragraph records (filtering tiny non-prose fragments < 12 words)
    eff_w = round(effective_weight(paper, cfg), 3)
    records: list[dict[str, Any]] = []
    para_idx = 0
    for p in merged_paras:
        txt = re.sub(r"(\[EQ\]\s*){2,}", "[EQ] ", p["text"]).strip()
        words = re.findall(r"[A-Za-z0-9]+(?:[.\-'][A-Za-z0-9]+)*", txt)
        n_words = len(words)
        if n_words < 12 and p["section"] != "abstract":
            continue
        records.append({
            "paper_id": paper.id,
            "tier": paper.tier,
            "weight": paper.weight,
            "effective_weight": eff_w,
            "split": paper.split,
            "section": p["section"],
            "heading": p["heading"],
            "para_idx": para_idx,
            "text": txt,
            "n_words": n_words,
        })
        para_idx += 1

    log_entry = {
        "paper_id": paper.id,
        "n_paragraphs": len(records),
        "sections_found": list(dict.fromkeys(r["section"] for r in records)),
        "section_counts": dict(Counter(r["section"] for r in records)),
        "headings_mapped": section_log,
        "fixes": dict(fixes),
    }
    return records, log_entry


def main() -> int:
    cfg = load_config()
    raw_dir = data_dir(cfg) / "raw"
    proc_dir = data_dir(cfg) / "processed"
    proc_dir.mkdir(parents=True, exist_ok=True)

    papers = resolve_papers(cfg)
    corpus_vocab = build_corpus_vocab(papers, raw_dir)
    all_records: list[dict[str, Any]] = []
    fix_logs: dict[str, Any] = {}

    for paper in papers:
        records, log_entry = process_paper(paper, raw_dir, cfg, corpus_vocab)
        all_records.extend(records)
        fix_logs[paper.id] = log_entry
        secs = ", ".join(f"{k}:{v}" for k, v in log_entry["section_counts"].items())
        print(f"{paper.id} ({paper.tier}/{paper.split:9s}): {len(records):2d} paras | [{secs}]")

    out_jsonl = proc_dir / "paragraphs.jsonl"
    with open(out_jsonl, "w", encoding="utf-8") as f:
        for rec in all_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    out_log = proc_dir / "fix_log.json"
    out_log.write_text(json.dumps(fix_logs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {len(all_records)} paragraphs to {out_jsonl}")
    print(f"Wrote fix log to {out_log}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

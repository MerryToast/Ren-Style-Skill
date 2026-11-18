#!/usr/bin/env python3
"""Style lint for Ren-Style-Skill outputs (stdlib only, so the skill stays portable).

Checks a text against thresholds in ../references/style_profile.json:
  - banned words / phrases                 (global.banned_words)
  - sentence-length median and P90         (<section>.sent_len_p50, <section>.sent_len_p90)  -> [lo, hi]
  - passive-voice ratio (heuristic)        (<section>.passive_ratio)                         -> [lo, hi]
  - signature-phrase over-use              (global.signature_max_per_100w)                   -> {phrase: max}

Usage:
    python scripts/style_lint.py --section results output.txt
    type output.txt | python scripts/style_lint.py --section results -
Exit code: 0 = pass, 1 = violations found, 2 = usage / profile error.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

PROFILE = Path(__file__).resolve().parent.parent / "references" / "style_profile.json"

ABBREV = r"(?:Fig|Figs|Eq|Eqs|Ref|Refs|e\.g|i\.e|et al|vs|No|Vol|approx)\."
PASSIVE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(?:\w+ed|\w+en|built|made|shown|found|known|set|put|held|done)\b",
    re.IGNORECASE,
)


def split_sentences(text: str) -> list[str]:
    protected = re.sub(ABBREV, lambda m: m.group(0).replace(".", "<DOT>"), text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\[(])", protected)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def words(s: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z\-']*|\d+(?:\.\d+)?", s)


def percentile(values: list[int], q: float) -> float:
    if not values:
        return 0.0
    v = sorted(values)
    k = (len(v) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def in_range(x: float, rng) -> bool:
    return rng is None or (rng[0] <= x <= rng[1])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", required=True)
    ap.add_argument("file", help="text file, or - for stdin")
    args = ap.parse_args()

    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    text = re.sub(r"\A---\r?\n.*?\r?\n---\r?\n*", "", text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()
    m_ren = re.search(r"^###\s+Ren\s*\r?\n(.*?)(?=^###\s+|\Z)", text, flags=re.MULTILINE | re.DOTALL)
    if m_ren:
        text = m_ren.group(1).strip()
    try:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"[error] cannot read {PROFILE}: {e}")
        return 2
    if str(profile.get("_status", "")).startswith("placeholder"):
        print("[warn] style_profile.json is still a placeholder; only basic metrics are reported.")

    g = profile.get("global", {})
    sec = profile.get(args.section, {})
    sents = split_sentences(text)
    lens = [len(words(s)) for s in sents]
    n_words = sum(lens)
    issues: list[str] = []

    lower = text.lower()
    for w in g.get("banned_words", []):
        hits = len(re.findall(rf"\b{re.escape(w.lower())}\b", lower))
        if hits:
            issues.append(f"banned word '{w}' x{hits}")

    for phrase, mx in g.get("signature_max_per_100w", {}).items():
        hits = len(re.findall(rf"\b{re.escape(phrase.lower())}\b", lower))
        density = hits / max(n_words, 1) * 100
        if density > mx:
            issues.append(f"signature '{phrase}' over-used: {density:.2f}/100w > {mx}")

    p50 = statistics.median(lens) if lens else 0
    p90 = percentile(lens, 0.9)
    passive = sum(1 for s in sents if PASSIVE.search(s)) / max(len(sents), 1)
    for name, val in (("sent_len_p50", p50), ("sent_len_p90", p90), ("passive_ratio", passive)):
        if not in_range(val, sec.get(name)):
            issues.append(f"{name}={val:.2f} outside {sec.get(name)}")

    print(f"section={args.section} sentences={len(sents)} words={n_words} "
          f"sent_len_p50={p50:.1f} sent_len_p90={p90:.1f} passive_ratio={passive:.2f}")
    if issues:
        print("VIOLATIONS:")
        for i in issues:
            print(f"  - {i}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

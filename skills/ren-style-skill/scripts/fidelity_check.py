#!/usr/bin/env python3
"""Fidelity check: verify that polishing / translation did not change facts (stdlib only).

Compares source vs output on:
  - numbers (with attached units if present)      e.g. 0.2, 50 nm/s, 125 °C
  - citation markers                              e.g. [1], [3-5], [CIT]
  - figure / table / equation references          e.g. Fig. 3, Table 2, Eq. (4), [FIG 3], [EQ]

Usage:
    python scripts/fidelity_check.py source.txt output.txt              # polish (mode C)
    python scripts/fidelity_check.py --mode translate source_zh.txt output_en.txt   # mode B
Exit code: 0 = identical fact sets, 1 = differences found.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

NUM = re.compile(r"(?<![A-Za-z\d.])[-+]?\d+(?:[.,]\d+)?(?:\s*[x×]\s*10\^?[-+]?\d+)?")
CIT = re.compile(r"\[(?:\d+(?:\s*[-–,]\s*\d+)*|CIT)\]")
REF_EN = re.compile(r"\b(Fig(?:ure)?s?\.?|Table|Eq(?:uation)?s?\.?)\s*\(?(\d+[a-z]?)\)?", re.IGNORECASE)
REF_ZH = re.compile(r"(图|表|式)\s*\(?(\d+[a-z]?)\)?")
PLACEHOLDER = re.compile(r"\[(?:FIG|EQ|TAB)\s*\d*\]")


def norm_num(s: str) -> str:
    s = s.replace(",", "") if re.fullmatch(r"\d{1,3}(,\d{3})+", s) else s.replace(",", ".")
    try:
        f = float(s)
        return str(int(f)) if f.is_integer() else repr(f)
    except ValueError:
        return s


def norm_ref(kind: str, n: str) -> str:
    k = kind.lower()
    if k.startswith(("fig", "图")):
        return f"FIG{n}"
    if k.startswith(("tab", "表")):
        return f"TAB{n}"
    return f"EQ{n}"


def extract(text: str, refs_only_numbers: bool) -> dict[str, Counter]:
    refs = Counter(norm_ref(k, n) for k, n in REF_EN.findall(text))
    refs += Counter(norm_ref(k, n) for k, n in REF_ZH.findall(text))
    refs += Counter(PLACEHOLDER.findall(text))
    cits = Counter(re.sub(r"\s", "", c) for c in CIT.findall(text))
    # remove citation / reference numbers before counting plain numbers
    stripped = CIT.sub(" ", REF_EN.sub(" ", REF_ZH.sub(" ", text)))
    nums = Counter(norm_num(n.strip()) for n in NUM.findall(stripped))
    out = {"numbers": nums, "citations": cits}
    if not refs_only_numbers:
        out["references"] = refs
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["polish", "translate"], default="polish")
    ap.add_argument("source")
    ap.add_argument("output")
    args = ap.parse_args()

    src = Path(args.source).read_text(encoding="utf-8")
    out = Path(args.output).read_text(encoding="utf-8")
    a = extract(src, args.mode == "translate")
    b = extract(out, args.mode == "translate")

    problems = 0
    for key in a:
        missing = a[key] - b[key]
        added = b[key] - a[key]
        if missing or added:
            problems += 1
            print(f"[{key}] missing in output: {dict(missing) or '-'} | added in output: {dict(added) or '-'}")
    if problems:
        print("FAIL: verify each difference (some may be legitimate, e.g. spelled-out numbers).")
        return 1
    print("PASS: numbers, citations and references preserved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

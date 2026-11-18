"""Shared helpers for the build pipeline.

All scripts run from the repository root, e.g. ``python pipeline/00_build_manifest.py``.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "ren-style-skill"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load config.yaml (falls back to config.example.yaml with a warning)."""
    cfg_path = Path(path) if path else REPO_ROOT / "config.yaml"
    if not cfg_path.exists():
        cfg_path = REPO_ROOT / "config.example.yaml"
        print(f"[warn] config.yaml not found, using {cfg_path.name}", file=sys.stderr)
    with open(cfg_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def data_dir(cfg: dict[str, Any]) -> Path:
    d = REPO_ROOT / cfg.get("data_dir", "data")
    d.mkdir(parents=True, exist_ok=True)
    return d


@dataclass
class Paper:
    id: str
    prefix: str
    tier: str
    split: str
    weight: float
    pdf: Path | None
    meta: dict[str, Any] = field(default_factory=dict)


def resolve_papers(cfg: dict[str, Any]) -> list[Paper]:
    """Match each registry entry to a PDF in corpus_dir by its leading number prefix."""
    corpus = Path(cfg["corpus_dir"])
    pdfs = sorted(corpus.glob("*.pdf"))
    by_prefix: dict[str, Path] = {}
    for p in pdfs:
        m = re.match(r"^(\d+)", p.name)
        if m:
            by_prefix[m.group(1).zfill(2)] = p
    weights = cfg["tier_weights"]
    papers = []
    for entry in cfg["papers"]:
        prefix = str(entry["prefix"]).zfill(2)
        papers.append(
            Paper(
                id=entry["id"],
                prefix=prefix,
                tier=entry["tier"],
                split=entry["split"],
                weight=float(weights[entry["tier"]]),
                pdf=by_prefix.get(prefix),
                meta=entry,
            )
        )
    return papers


def effective_weight(paper: Paper, cfg: dict[str, Any]) -> float:
    """Tier weight, halved for each paper in a near-duplicate group (design_notes §1)."""
    group = paper.meta.get("dup_group")
    if not group:
        return paper.weight
    n = sum(1 for e in cfg["papers"] if e.get("dup_group") == group)
    return paper.weight / max(n, 1)

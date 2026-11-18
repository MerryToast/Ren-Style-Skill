"""Phase 7 — Pack a standalone single-file prompt (`dist/single_prompt.md`) for chat models without Skill support.

Strictly reads from the public skill layer (`skills/ren-style-skill/` excluding `examples.local/`)
so that `dist/single_prompt.md` is 100% redistributable under MIT + CC BY 4.0 attribution.

Usage:
    python pipeline/07_pack_single_prompt.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from common import REPO_ROOT, SKILL_DIR


def _read_clean(path: Path) -> str:
    txt = path.read_text(encoding="utf-8")
    return re.sub(r"\A---\r?\n.*?\r?\n---\r?\n*", "", txt, flags=re.DOTALL).strip()


def main() -> int:
    dist_dir = REPO_ROOT / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    out_path = dist_dir / "single_prompt.md"

    ref_dir = SKILL_DIR / "references"
    pb_dir = ref_dir / "playbooks"
    ex_dir = SKILL_DIR / "examples"
    tpl_dir = SKILL_DIR / "templates"

    sections: list[str] = [
        "# Ren-Style-Skill — Standalone Single-Prompt Edition (v0.1.0)",
        "",
        "> **Usage**: Copy and paste this file into any LLM chat session (Claude, ChatGPT, Gemini, DeepSeek, etc.), "
        "then append your request at the bottom specifying **Mode A (Draft)**, **Mode B (Translate Chinese → English)**, "
        "**Mode C (Polish English Draft)**, or **Mode D (Style Review)** and the target `section/function`.",
        ">",
        "> **Attribution**: Open-access excerpts from W. Ren, C. Zhang, X. Sun, *IEEE Access*, vol. 8, pp. 93857–93867, "
        "2020 (`doi:10.1109/ACCESS.2020.2994085`) are reused under CC BY 4.0 (see repository `NOTICE.md`). "
        "All other examples are synthetic (`source: synthetic`).",
        "",
        "---",
        "",
        "## Part I — Core Operating Workflow (`SKILL.md`)",
        "",
        _read_clean(SKILL_DIR / "SKILL.md"),
        "",
        "---",
        "",
        "## Part II — Quantitative Style Profile (`R01`–`R33`)",
        "",
        _read_clean(ref_dir / "style_profile.md"),
        "",
        "---",
        "",
        "## Part III — Distinctive Lexicon & Banned AI Clichés",
        "",
        _read_clean(ref_dir / "lexicon.md"),
        "",
        "---",
        "",
        "## Part IV — Style vs. Error Policy (`F01`–`F36`, `O01`–`O08`)",
        "",
        _read_clean(ref_dir / "error_policy.md"),
        "",
        "---",
        "",
        "## Part V — Chinese-to-English Domain Glossary & Translation Guide (`T01`–`T20`)",
        "",
        _read_clean(ref_dir / "glossary_zh_en.md"),
        "",
        _read_clean(ref_dir / "translation_guide.md"),
        "",
        "---",
        "",
        "## Part VI — Section Playbooks",
        "",
    ]

    for sec_name in ("abstract", "introduction", "experimental", "modeling", "results", "mechanism", "conclusion"):
        pb_file = pb_dir / f"{sec_name}.md"
        sections.extend([
            f"### Playbook: `{sec_name}`",
            "",
            _read_clean(pb_file),
            "",
        ])

    sections.extend([
        "---",
        "",
        "## Part VII — Public Golden Examples (Open-Access `P22` + Synthetic)",
        "",
    ])

    for ex_file in sorted(ex_dir.rglob("*.md")):
        if ex_file.name == "README.md" or ex_file.parent.name == "contrastive":
            continue
        rel = ex_file.relative_to(ex_dir).as_posix()
        sections.extend([
            f"### Example: `{rel}`",
            "",
            ex_file.read_text(encoding="utf-8").strip(),
            "",
        ])

    sections.extend([
        "---",
        "",
        "## Part VIII — Contrastive Pairs (`AI-default` vs `Ren`)",
        "",
    ])
    for cp_file in sorted((ex_dir / "contrastive").glob("pair_*.md")):
        sections.extend([
            f"### Contrastive Pair: `{cp_file.name}`",
            "",
            cp_file.read_text(encoding="utf-8").strip(),
            "",
        ])

    sections.extend([
        "---",
        "",
        "## Part IX — Output Report Templates",
        "",
        "### Mode B Template (`translation_report.md`)",
        "```markdown",
        (tpl_dir / "translation_report.md").read_text(encoding="utf-8").strip(),
        "```",
        "",
        "### Mode C Template (`polish_report.md`)",
        "```markdown",
        (tpl_dir / "polish_report.md").read_text(encoding="utf-8").strip(),
        "```",
        "",
        "### Mode D Template (`review_report.md`)",
        "```markdown",
        (tpl_dir / "review_report.md").read_text(encoding="utf-8").strip(),
        "```",
        "",
    ])

    full_text = "\n".join(sections)
    out_path.write_text(full_text, encoding="utf-8")
    n_lines = len(full_text.splitlines())
    n_words = len(re.findall(r"\S+", full_text))
    print(f"Packed standalone prompt to {out_path} ({n_lines} lines, {n_words} words)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Ren-Style-Skill

> An agent **Skill** for academic writing in the style of **Prof. Wanbin Ren** (Harbin Institute of Technology), focused on **electrical contacts / electrical engineering** papers.
>
> 中文说明见 [README.zh-CN.md](README.zh-CN.md)。

> [!NOTE]
> **Status: under construction (v0.0.x).** The repository skeleton is in place; style rules and examples are produced by the build pipeline. See [docs/design_notes.md](docs/design_notes.md).

## What it does

| Mode | Input | Output |
|---|---|---|
| **A. Draft** | Notes / bullet points for one subsection | Paragraphs in Ren's style |
| **B. Translate** | Chinese manuscript text | English text in Ren's style + uncertain-term list |
| **C. Polish** | English draft | Polished text + change log citing style rules |
| **D. Review** | English draft | List of style deviations and suggested fixes (no rewrite) |

Default policy (`fidelity_level: balanced`): imitate Ren's rhetorical structure, sentence patterns and signature wording, **but fix grammar** so the output is journal-ready.

## Install the skill

Copy the self-contained folder [`skills/ren-style-skill/`](skills/ren-style-skill/) into your agent's skills directory, e.g.

- Antigravity (workspace): `<project>/.agents/skills/ren-style-skill/`
- Antigravity (global): `~/.gemini/config/skills/ren-style-skill/`
- Other agents that support `SKILL.md` skills: their skills directory.

For chat models without skill support, use `dist/single_prompt.md` (generated in Phase 7).

## Usage examples

```text
Use ren-style-skill, mode B: translate the following Introduction "gap" paragraph into English.
<中文段落>
```

```text
Use ren-style-skill, mode C: polish this Results paragraph describing contact-resistance waveforms.
<English paragraph>
```

Work **one subsection at a time (≤ 800 words)** for best style consistency.

## Repository layout

```text
pipeline/              build-time tooling: PDF -> paragraphs -> stylometry -> style profile & examples
skills/ren-style-skill the deliverable skill (self-contained)
eval/                  held-out evaluation
docs/                  design notes, build-your-own guide
```

## Build the skill yourself

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
Copy-Item config.example.yaml config.yaml   # edit corpus_dir
python pipeline/00_build_manifest.py
python pipeline/01_extract_pdf.py
python pipeline/02_clean_segment.py
python pipeline/03_stylometry.py
python pipeline/04_distinctive_lexicon.py
python pipeline/05_rank_candidates.py
```

See [docs/build_your_own.md](docs/build_your_own.md) to build a style skill for another author.

## Copyright & ethics

- No papers or full texts are distributed. Excerpts from copyrighted papers stay in the local, gitignored `examples.local/`. Open-access excerpts are attributed in [NOTICE.md](NOTICE.md).
- Prof. Ren has been informed of and agreed to this project.
- Intended to **assist writing and polishing** by the author's group. Do not use it for ghost-writing, impersonation or any form of academic misconduct.

## License

Code and original docs: [MIT](LICENSE). Quoted excerpts: see [NOTICE.md](NOTICE.md).

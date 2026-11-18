# Ren-Style-Skill (`v0.1.0`)

> A portable AI Agent **Skill** for drafting, translating (Chinese → English), polishing, and reviewing academic papers in the empirical writing style of **Prof. Wanbin Ren** (Harbin Institute of Technology, electrical contacts & electromechanical engineering).
>
> 中文说明见 **[README.zh-CN.md](README.zh-CN.md)**。

---

## 1. Overview & Supported Modes

`Ren-Style-Skill` models the rhetoric, sentence-length cadence, section-dependent voice/tense switching, and lexical restraint distilled from 30 electrical-contact papers (`P01`–`P30`: Tier S anchor papers, Tier A first-author papers, and Tier B student-led papers used as a negative contrast set).

| Mode | Trigger / Input | Output Format | Automated Verification |
| :--- | :--- | :--- | :--- |
| **A — Draft** | Experimental notes, bullet points, or outline for one subsection | Publication-ready prose in Ren's style | `style_lint.py` |
| **B — Translate** | Chinese academic draft (`中文手稿`) | English translation + terminology & uncertainty table ([translation_report.md](skills/ren-style-skill/templates/translation_report.md)) | `style_lint.py` + `fidelity_check.py --mode translate` |
| **C — Polish** | English draft (AI-flavoured or student draft) | Polished text + rule-cited change log ([polish_report.md](skills/ren-style-skill/templates/polish_report.md)) | `style_lint.py` + `fidelity_check.py --mode polish` |
| **D — Review** | English draft | Diagnostic report citing `R01`–`R33` / `F01`–`F36` without rewriting ([review_report.md](skills/ren-style-skill/templates/review_report.md)) | `style_lint.py` |

- **Default Fidelity Policy (`fidelity_level: balanced`)**: Preserves Prof. Ren's authentic stylistic choices (`KEEP_STYLE` rules `R01`–`R33`), fixes L2 grammatical errors (`FIX_ERROR` rules `F01`–`F16`), and strips both LLM clichés (`AI_CLICHE` rules `F17`–`F28`) and student-draft drift (`F29`–`F36`).
- **Optional Strict Mode (`fidelity_level: strict`)**: Also retains harmless corpus-attested L2 expressions (`O01`–`O08`) when present in the user's draft.

---

## 2. Installation

### Option A — Agent Skill Directory (Antigravity, Claude Code, Gemini CLI, Cursor)

Copy the self-contained [`skills/ren-style-skill/`](skills/ren-style-skill/) directory (zero third-party runtime dependencies; verification scripts use Python stdlib only) into your agent's skill path:

- **Google Antigravity (Workspace)**: `<project>/.agents/skills/ren-style-skill/`
- **Google Antigravity (Global)**: `~/.gemini/config/skills/ren-style-skill/`
- **Claude Code**: `<project>/.claude/skills/ren-style-skill/` or `~/.claude/skills/ren-style-skill/`
- **Gemini CLI / Other `SKILL.md`-compatible agents**: copy into the configured skills folder.

### Option B — Standalone Single-Prompt File (Web Chat Interfaces)

For chat models that do not support multi-file Skills (e.g., web ChatGPT, Claude, DeepSeek, or Gemini), copy and paste **[dist/single_prompt.md](dist/single_prompt.md)** into your conversation, followed by your task prompt.

---

## 3. Usage Examples (4 Modes)

> **Best Practice**: Process **one subsection at a time (≤ 600–800 words)** and name the target `section/function` slot (`abstract/full`, `introduction/{background,prior_work,gap,this_paper}`, `experimental/{test_rig,specimen,procedure}`, `modeling/{model_setup,derivation,validation}`, `results/{waveform,trend,surface_analysis}`, `mechanism/explanation`, `conclusion/{numbered,summary}`).

### Mode A — Draft from Experimental Notes
```text
Use ren-style-skill (Mode A, section: results/waveform):
Draft a paragraph from these lab notes:
- [FIG 5]: contact resistance and tangential friction force vs. fretting cycles (slip amplitude 25 μm, frequency 100 Hz, normal load 2.0 N).
- Three stages: Stage I running-in (0–600 cycles, 8.5 mΩ drops to 6.2 mΩ, friction rises 0.45 N -> 0.78 N); Stage II plateau (600–8.5e3 cycles, 6.0–7.4 mΩ); Stage III rapid degradation (>8.8e3 cycles spikes >150 mΩ, reaches 0.5 Ω failure threshold at 1.12e4 cycles).
```

### Mode B — Translate Chinese Manuscript to English
```text
Use ren-style-skill (Mode B, section: experimental/procedure, fidelity: balanced):
Translate the following Chinese paragraph into English:
法向接触力设定为 3 N，负载电流为 10 mA。动触头为直径 2 mm 的球形骑子（rider），静电极为平面试样。基体材料采用铜合金，表面镀覆厚度为 1 μm 的纯金镀层。采用四线法实时记录接触电阻的瞬态值，测量原理由 [FIG 1] 给出……
```

### Mode C — Polish an AI-Flavoured or Student English Draft
```text
Use ren-style-skill (Mode C, section: introduction/gap, fidelity: balanced):
Polish the following paragraph into Prof. Ren's style and provide the rule-cited change log:
"Despite its critical practical importance, there remains a glaring gap in our comprehensive understanding of how radial slip gradients govern the wear-through durability of duplex palladium-nickel coatings. Furthermore, existing theoretical frameworks fail to capture the intricate interplay between stick and slip zones..."
```

### Mode D — Diagnostic Style Review Only
```text
Use ren-style-skill (Mode D, section: introduction/background):
Review this draft paragraph for deviations from Prof. Ren's style (do not rewrite the paragraph):
"It is top-urgent to understand and determine the failure mechanisms of silver tin oxide composite material used in switching devices. Ever published research results have determined that..."
```

---

## 4. Quantitative Evaluation on Heldout Split (`[P05, P09, P16, P19]`)

All evaluations are reproducible via `python pipeline/06_evaluate.py` on the strictly unseen **heldout split** (`P05`, `P09`, `P16`, `P19` across all 7 sections) and the **Tier B student split** (`P17`, `P18`, `P20`, `P23`, `P24`):

### 4.1 Back-Translation & Component Ablation (`Heldout → Chinese → Mode B English`)

| Configuration | Mean Stylometric Distance $d(\cdot, \mu_{\text{Ren S+A}})$ ↓ | `style_lint.py` Pass Rate ↑ | Banned AI Cliché Hits ↓ | `fidelity_check.py` Pass Rate ↑ |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline (No Skill)** | `1.2367` | `0.0%` | `16` | `100.0%` |
| **Ablation: `-Profile/Lexicon` (Examples only)** | `1.2869` | `25.0%` | `0` | `100.0%` |
| **Ablation: `-Examples` (Profile + Playbook only)** | `1.6819` | `25.0%` | `0` | `100.0%` |
| **Ablation: `-Contrastive Pairs`** | `0.7077` | `75.0%` | `0` | `100.0%` |
| **Skill Mode B (Public Layer `examples/` only)** | **`0.6913`** | **`100.0%`** | **`0`** | **`100.0%`** |
| **Skill Mode B (Full: Private `examples.local/` + Public)** | **`0.6639`** | **`100.0%`** | **`0`** | **`100.0%`** |

- **Public vs. Private Layer Effectiveness**: The redistributable public layer (`P22` OA excerpts + synthetic examples + contrastive pairs + rules) achieves **`95.2%`** of the private layer's stylometric distance reduction on back-translation and **`88.5%`** on Mode C de-stylized polishing (exceeding the ≥80% design target).

### 4.2 Personal Style vs. Student Drift (`Tier B Drafts → Mode C Polish`)

| Metric | Before Polish (Tier B Original) | After Mode C Polish | Result |
| :--- | :---: | :---: | :--- |
| **Distance to Ren (`S+A`) Centroid $d(\cdot, \mu_{\text{Ren S+A}})$** | `1.3999` | **`0.5071`** | **Moves `-63.8%` closer to Ren's personal centroid** |
| **Distance to Student (`B`) Centroid $d(\cdot, \mu_{\text{Student B}})$** | `0.9095` | **`1.1601`** | **Moves `+27.6%` away from student-drift centroid** |
| **Student-Drift Markers (`F29`–`F36`)** | `10` | **`0`** | `100%` eliminated (`0` factual alterations) |

### 4.3 Three-Way Blind A/B Discrimination (`16 Heldout Pairs/Arm`, Ideal = `50.0%`)

- **`Original vs. Baseline (No Skill)`**: **`92.2%`** mean discriminator accuracy (baseline easily spotted).
- **`Original vs. Skill (Public Layer)`**: **`39.1%`** mean discriminator accuracy.
- **`Original vs. Skill (Full Private Layer)`**: **`40.6%`** mean discriminator accuracy (indistinguishable from genuine Ren prose; slightly below 50% because Skill outputs sit closer to the S-tier centroid than noisy single heldout paragraphs).

---

## 5. Repository Structure & Reproducible Build Pipeline

```text
Ren-Style-Skill/
├── config.example.yaml                 # Corpus & split configuration template
├── NOTICE.md                           # CC BY 4.0 attribution for open-access excerpts (P22)
├── dist/
│   └── single_prompt.md                # Standalone single-file prompt for chat UIs
├── docs/
│   ├── design_notes.md                 # Architecture, corpus audit, and phase specifications
│   └── build_your_own.md               # Guide to building a style skill for another author
├── pipeline/
│   ├── 00_build_manifest.py            # Step 0: Corpus registry & split assignment
│   ├── 01_extract_pdf.py               # Step 1: Two-column layout-aware PDF extraction
│   ├── 02_clean_segment.py             # Step 2: Ligature/regex cleaning & section segmentation
│   ├── 03_stylometry.py                # Step 3: Weighted per-section stylometric statistics
│   ├── 04_distinctive_lexicon.py       # Step 4: Three-way log-odds lexicon (Ren S+A vs AI vs Tier B)
│   ├── 05_rank_candidates.py           # Step 5: Typicality ranking & public/private excerpt export
│   ├── 06_evaluate.py                  # Step 6: Heldout back-translation, polish, ablation & blind eval
│   └── 07_pack_single_prompt.py        # Step 7: Compile dist/single_prompt.md
└── skills/ren-style-skill/             # Self-contained deliverable Skill
    ├── SKILL.md                        # Main skill entry point (<200 lines)
    ├── references/                     # style_profile.md/.json, lexicon.md, error_policy.md,
    │                                   # glossary_zh_en.md, translation_guide.md, playbooks/*.md
    ├── examples/                       # Public layer (P22 OA + synthetic + contrastive pairs)
    ├── examples.local/                 # Private layer (gitignored, copyrighted train excerpts)
    ├── scripts/                        # stdlib-only style_lint.py and fidelity_check.py
    └── templates/                      # Markdown output templates for Modes B, C, D
```

To rebuild from the local PDF corpus:
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item config.example.yaml config.yaml   # set corpus_dir to your local PDF folder
python pipeline/00_build_manifest.py
python pipeline/01_extract_pdf.py
python pipeline/02_clean_segment.py
python pipeline/03_stylometry.py
python pipeline/04_distinctive_lexicon.py
python pipeline/05_rank_candidates.py
python pipeline/06_evaluate.py
python pipeline/07_pack_single_prompt.py
```

---

## 6. Limitations, Copyright & Ethics

- **Domain Scope**: Calibrated specifically for electrical contacts, switching apparatus, tribology of conductive coatings, and finite-element contact modeling. Do not apply to unrelated disciplines without rebuilding the domain lexicon and playbooks (see [docs/build_your_own.md](docs/build_your_own.md)).
- **Two-Layer Copyright Separation**:
  - **Zero full-text PDFs or copyrighted excerpts** are tracked in Git. Verbatim excerpts from publisher-copyrighted papers reside strictly inside the local, gitignored `skills/ren-style-skill/examples.local/` directory.
  - The public `skills/ren-style-skill/examples/` directory contains only open-access excerpts from `P22` (*IEEE Access* 2020, CC BY 4.0, attributed in [NOTICE.md](NOTICE.md)) and synthetic examples (`source: synthetic`).
- **Author Consent & Academic Integrity**: Prof. Wanbin Ren (Harbin Institute of Technology) has been informed of and agreed to this project. This tool is designed to assist manuscript drafting, translation, and language polishing within the research group; users remain fully responsible for the scientific validity, factual accuracy, and originality of their publications.

## License

Code, statistical rules, and synthetic examples: [MIT License](LICENSE). Open-access excerpts: CC BY 4.0 as listed in [NOTICE.md](NOTICE.md).

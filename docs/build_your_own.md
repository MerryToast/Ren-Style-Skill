# Build a Scientific Writing-Style Skill for Another Author (`build_your_own.md`)

The `Ren-Style-Skill` build pipeline (`pipeline/00_build_manifest.py` through `07_pack_single_prompt.py`) is **author- and domain-agnostic**. You can use it to model the English academic writing style of any researcher from 15–40 PDF papers while keeping publisher-copyrighted text strictly local.

---

## 1. Corpus Preparation & Three-Tier Stratification

Gather 15–40 PDF papers from your target author/group and classify each paper into one of three tiers in `config.yaml`:

| Tier | Authorship Role | Weight (`tier_weights`) | Purpose in Pipeline |
| :--- | :--- | :---: | :--- |
| **Tier S** | Sole-authored or flagship first-author papers in top journals (2–5 papers) | `3.0` | **Primary style anchors**: Resolve conflicts between tiers; provide at least 1 golden excerpt per `(section, function)` slot. |
| **Tier A** | Other first-author papers by the target author (10–25 papers) | `1.5` | **Statistical backbone**: Provide sufficient sample size across all 7 canonical sections (`train` vs `heldout`). |
| **Tier B** | Student first-author papers where the target author is corresponding/supervising author (5–15 papers) | `0.5` | **Negative contrast (`split: secondary`)**: Used in `04_distinctive_lexicon.py` and `06_evaluate.py` to separate the PI's personal voice from student-draft habits (`F29`–`F36`). |

### Handling Near-Duplicate Pairs & Splits
- **Near-duplicate pairs (`dup_group`)**: If the corpus contains conference-to-journal extensions or companion papers sharing >25% of paragraphs, assign them the same `dup_group` label in `config.yaml`. The pipeline automatically halves their effective weight (`× 0.5`) so shared passages do not skew stylometric means, and keeps both members in the same split (`train`) to prevent heldout data leakage.
- **Heldout split (`split: heldout`)**: Reserve 3–5 Tier A papers spanning experimental and modeling topics for Phase 6 blind and quantitative evaluation. **Never** include `heldout` or `secondary` (Tier B) papers in stylometric profiling (`03`) or golden excerpt selection (`05`).

---

## 2. Step-by-Step Build Pipeline

### Step 0 — Configure & Build the Corpus Manifest
1. Fork this repository, rename `skills/ren-style-skill/` to `skills/<your-skill-name>/`, and update `SKILL_DIR` in `pipeline/common.py`.
2. Copy `config.example.yaml` to `config.yaml` (gitignored) and fill in `author`, `corpus_dir`, `sections`, and `papers`.
3. Run:
   ```powershell
   python pipeline/00_build_manifest.py
   ```
4. Inspect `data/corpus_meta.csv` and verify every paper's first author, venue, year, `tier`, `split`, and `open_access` license status.

### Step 1 — Layout-Aware PDF Extraction & Cleaning
Run the two-column extractor and section segmenter:
```powershell
python pipeline/01_extract_pdf.py
python pipeline/02_clean_segment.py
```
- `01_extract_pdf.py` detects single-column vs. two-column body layouts per page, strips running headers/footers, watermarks, proofreader boxes, display equations (`[EQ]`), figure captions, and tables (`[TAB]`).
- `02_clean_segment.py` repairs ligatures (`ﬁ`, `ﬂ`), control characters (`0x01`–`0x1f`), private-use glyphs, inline citation markers (`[1]`, superscript citations → `[CIT]`), figure references (`Fig. 3` → `[FIG 3]`), and maps headings into the 7 canonical sections (`abstract`, `introduction`, `experimental`, `modeling`, `results`, `mechanism`, `conclusion`).
- **Quality gate**: Spot-check 15 random paragraphs in `data/processed/paragraphs.jsonl` and verify every paper has `abstract`, `introduction`, `conclusion`, and 2–4 body sections.

### Step 2 — Weighted Per-Section Stylometry & Three-Way Lexicon
```powershell
python pipeline/03_stylometry.py
python pipeline/04_distinctive_lexicon.py
```
- `03_stylometry.py` computes weighted per-section sentence-length distributions (mean, SD, median, IQR, P10, P90), passive voice ratio, tense ratios, initial connectives, reporting verbs, adverb placement (`explicitly`, `respectively`), and signature constructions (`data/processed/stats_report.md`).
- Generate 25–30 default-LLM abstract rewrites in `data/baseline/ai_rewrites.jsonl` using `pipeline/prompts/ai_baseline_rewrite.md`, then run `04_distinctive_lexicon.py` to compute Monroe's Dirichlet-smoothed log-odds z-scores for:
  1. `Author (S+A) vs. AI Baseline` → populates the preferred lexicon and banned AI cliché list;
  2. `Author (S+A) vs. Student (Tier B)` → isolates personal signature phrases from student drift.

### Step 3 — Synthesize the Style Profile, Error Policy & Playbooks
Using the prompt templates in `pipeline/prompts/{move_analysis,style_vs_error,profile_synthesis}.md`:
1. Classify every quantitative and qualitative pattern into `KEEP_STYLE` (`R01`–`R33`), `FIX_ERROR` (`F01`–`F16`), `AI_CLICHE` (`F17`–`F28`), `STUDENT_DRIFT` (`F29`–`F36`), or `OPTIONAL` (`O01`–`O08`).
2. Populate:
   - `skills/<skill>/references/style_profile.md` and machine-readable thresholds in `style_profile.json`
   - `skills/<skill>/references/lexicon.md` and `error_policy.md`
   - `skills/<skill>/references/glossary_zh_en.md` and `translation_guide.md`
   - Per-section playbooks in `skills/<skill>/references/playbooks/*.md`

### Step 4 — Rank Candidates & Populate the Two-Layer Example Store
```powershell
python pipeline/05_rank_candidates.py
```
- Ranks `train` S+A paragraphs by standardized Euclidean distance to each `(section, function)` centroid (applying a `× 0.7` distance bonus to Tier S paragraphs).
- Exports verbatim copyrighted golden excerpts **only** to `skills/<skill>/examples.local/` (gitignored).
- Exports open-access excerpts (e.g., CC BY 4.0 papers, attributed in `NOTICE.md`) to `skills/<skill>/examples/`, and guides the creation of 1 synthetic example per `(section, function)` (`pipeline/prompts/synthetic_example.md`) plus 6–8 contrastive pairs (`pipeline/prompts/contrastive_pair.md`).
- Verify that every public example in `examples/` passes `python skills/<skill>/scripts/style_lint.py`.

### Step 5 & Step 6 — Assemble `SKILL.md` & Run Heldout Evaluation
```powershell
python pipeline/06_evaluate.py
python pipeline/07_pack_single_prompt.py
```
- Verify on your heldout split (`data/eval_report.md`):
  1. Back-translation (`Heldout → Chinese → Mode B`) and de-stylized polishing (`Heldout → AI rewrite → Mode C`) significantly reduce stylometric distance to the S+A centroid and pass `style_lint.py` at 100%;
  2. `fidelity_check.py` reports **0 altered numbers, units, citations, or references**;
  3. The public layer achieves ≥80% of the private layer's stylometric improvement;
  4. Tier B student drafts polished with Mode C move closer to the `S+A` centroid and farther from the `Tier B` centroid.

---

## 3. Pre-Release Checklist

Before pushing to GitHub or tagging a release:
1. Run `git status --ignored` and `git ls-files` to confirm that **zero** `*.pdf`, `data/*` (except `data/README.md`), `config.yaml`, or `examples.local/*` (except `README.md`) files are tracked.
2. Verify every open-access excerpt in `examples/` and `dist/single_prompt.md` is attributed with full citation, DOI, and license in `NOTICE.md`.

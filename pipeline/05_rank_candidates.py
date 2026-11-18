"""Phase 4.1 — Rank candidate golden excerpts by typicality.

Assigns each train paragraph/window (tiers S+A with ``split == "train"`` ONLY;
never heldout or tier B) to one or more canonical ``(section, function)`` slots,
computes a standardized stylometric feature vector per candidate, measures
Euclidean distance to the weighted section/function centroid, applies the
Tier-S bonus (``distance * 0.7`` per docs/design_notes.md §6 Phase 4), and
writes the top 8 diverse candidates (max 2 per paper) to:
  ``data/candidates/<section>/<function>.jsonl``

Usage:
    python pipeline/05_rank_candidates.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from common import SKILL_DIR, data_dir, load_config, resolve_papers

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from importlib import import_module
import statistics

stylo = import_module("03_stylometry")
style_lint = import_module("style_lint")
STYLE_PROFILE = json.loads((SKILL_DIR / "references" / "style_profile.json").read_text(encoding="utf-8"))


def passes_style_lint(text: str, section: str) -> bool:
    """Return True iff text passes skills/ren-style-skill/scripts/style_lint.py for section."""
    g = STYLE_PROFILE.get("global", {})
    sec = STYLE_PROFILE.get(section, {})
    sents = style_lint.split_sentences(text)
    lens = [len(style_lint.words(s)) for s in sents]
    if not lens:
        return False
    n_words = sum(lens)
    lower = text.lower()
    for w in g.get("banned_words", []):
        if re.search(rf"\b{re.escape(w.lower())}\b", lower):
            return False
    for phrase, mx in g.get("signature_max_per_100w", {}).items():
        hits = len(re.findall(rf"\b{re.escape(phrase.lower())}\b", lower))
        if hits / max(n_words, 1) * 100 > mx:
            return False
    p50 = statistics.median(lens)
    p90 = style_lint.percentile(lens, 0.9)
    passive = sum(1 for s in sents if style_lint.PASSIVE.search(s)) / max(len(sents), 1)
    for name, val in (("sent_len_p50", p50), ("sent_len_p90", p90), ("passive_ratio", passive)):
        if not style_lint.in_range(val, sec.get(name)):
            return False
    return True

RULE_MAP = {
    ("abstract", "full"): "[R01, R03, R07, R13, R14, R15]",
    ("introduction", "background"): "[R01, R02, R08, R16, R17]",
    ("introduction", "prior_work"): "[R01, R02, R11, R16, R17]",
    ("introduction", "gap"): "[R01, R06, R16, R17, R18]",
    ("introduction", "this_paper"): "[R01, R03, R08, R16, R17]",
    ("experimental", "test_rig"): "[R01, R10, R19, R20]",
    ("experimental", "specimen"): "[R01, R10, R19, R21]",
    ("experimental", "procedure"): "[R01, R06, R10, R19, R20, R21]",
    ("modeling", "model_setup"): "[R01, R11, R22, R24]",
    ("modeling", "derivation"): "[R01, R04, R07, R22, R23]",
    ("modeling", "validation"): "[R01, R04, R08, R22, R24]",
    ("results", "waveform"): "[R01, R04, R06, R25, R26, R27]",
    ("results", "trend"): "[R01, R04, R05, R06, R25, R26, R27]",
    ("results", "surface_analysis"): "[R01, R05, R07, R25, R27]",
    ("mechanism", "explanation"): "[R01, R04, R05, R07, R28, R29, R30]",
    ("conclusion", "numbered"): "[R01, R05, R31, R32, R33]",
    ("conclusion", "summary"): "[R01, R05, R07, R31, R32, R33]",
}


def build_candidate_windows(train_paras: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return single paragraphs plus merged 2-3 consecutive paragraph windows (130-260 words)."""
    by_paper_sec: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for p in train_paras:
        by_paper_sec[(p["paper_id"], p["section"])].append(p)

    candidates: list[dict[str, Any]] = []
    for (pid, sec), plist in by_paper_sec.items():
        plist.sort(key=lambda x: x["para_idx"])
        # Single paragraphs
        for p in plist:
            if sec == "abstract" or 85 <= p["n_words"] <= 280:
                candidates.append(dict(p))
            elif p["n_words"] > 280:
                # Split very long paragraphs (>280w) into two sentence-aligned halves
                sents = stylo.split_sentences(p["text"])
                if len(sents) >= 4:
                    mid = len(sents) // 2
                    for suffix, chunk in (("a", sents[:mid]), ("b", sents[mid:])):
                        txt_half = " ".join(chunk)
                        nw_half = len(stylo.tokenize_words(txt_half))
                        if 110 <= nw_half <= 265:
                            half_p = dict(p)
                            half_p["para_idx"] = f"{p['para_idx']}{suffix}"
                            half_p["text"] = txt_half
                            half_p["n_words"] = nw_half
                            candidates.append(half_p)
        # Consecutive 2- or 3-paragraph windows when individual paragraphs are short/medium
        n = len(plist)
        for i in range(n):
            acc_txt = [plist[i]["text"]]
            acc_words = plist[i]["n_words"]
            for j in range(i + 1, min(i + 4, n)):
                acc_txt.append(plist[j]["text"])
                acc_words += plist[j]["n_words"]
                if 120 <= acc_words <= 265:
                    merged = dict(plist[i])
                    merged["para_idx"] = f"{plist[i]['para_idx']}-{plist[j]['para_idx']}"
                    merged["text"] = " ".join(acc_txt)
                    merged["n_words"] = acc_words
                    candidates.append(merged)
    return candidates


def _base_idx(para_idx: Any) -> int:
    m = re.match(r"(\d+)", str(para_idx))
    return int(m.group(1)) if m else 0


def classify_functions(cand: dict[str, Any], max_idx_in_sec: int) -> list[str]:
    """Return one or more function labels within ``cand['section']``."""
    sec = cand["section"]
    txt = cand["text"]
    low = txt.lower()
    head = cand.get("heading", "").lower()
    first_idx = _base_idx(cand["para_idx"])

    if sec == "abstract":
        return ["full"]

    if sec == "introduction":
        funcs: list[str] = []
        if re.search(
            r"\b(?:in this paper|in this study|in this work|this paper first|an attempt is made|"
            r"the main motivation|the objective of this|the purpose of this)\b",
            low,
        ):
            funcs.append("this_paper")
        if re.search(
            r"\b(?:however,\s+(?:studies|little|to the best|there is little|ever published)|"
            r"relatively little is known|are very limited|remains? absent|remains? unexamined|"
            r"cannot explain|challengeable to)\b",
            low,
        ):
            funcs.append("gap")
        if "[CIT]" in txt and re.search(
            r"\b(?:et al\.|studied|investigated|examined|evaluated|reported|proposed|"
            r"observed|concluded|reviewed|argued|stated|found that)\b",
            low,
        ):
            funcs.append("prior_work")
        if first_idx <= 3 or re.search(
            r"\b(?:widely used|increasing application|weak link|important concern|"
            r"important issue|important quantity|defined as|holm\b)\b",
            low,
        ):
            funcs.append("background")
        return funcs or ["background"]

    if sec == "experimental":
        funcs = []
        if "test rig" in head or re.search(
            r"\b(?:test rig|test apparatus|schematic|consists of|three main modules|"
            r"shaker|piezoelectric actuator|linear translation|force transducer|load cell|"
            r"daq|sampling rate|sampling frequency|labview)\b",
            low,
        ):
            funcs.append("test_rig")
        if re.search(
            r"\b(?:ball-shaped|hemisphere-shaped|flat sample|flat specimen|coupon|"
            r"diameter of|electroplated with|thickness of|degreased|ultrasonic cleaner|"
            r"acetone|distilled water|surface roughness|hardness of)\b",
            low,
        ):
            funcs.append("specimen")
        if "method" in head or "condition" in head or re.search(
            r"\b(?:four-wire|4-wires|table 1|experimental conditions|current loads? of|"
            r"scanning electron|sem\b|edx\b|x-ray|endurance test|operation mode)\b",
            low,
        ):
            funcs.append("procedure")
        return funcs or ["procedure"]

    if sec == "modeling":
        funcs = []
        if "fem" in head or "finite" in head or re.search(
            r"\b(?:system of interest|we consider|symmetric about|comsol|multiphysics|"
            r"meshed with|graded radially|top-most|bottom-most|electrically grounded|"
            r"electrically insulated)\b",
            low,
        ):
            funcs.append("model_setup")
        if "[EQ]" in txt or re.search(
            r"\b(?:boundary conditions|can be expressed as|is given as|is written as|"
            r"for simplicity, we define|substituting|combining|legendre|laplace|potential)\b",
            low,
        ):
            funcs.append("derivation")
        if "valid" in head or re.search(
            r"\b(?:compared with|comparison|agree well|deviate|classical holm|hertz|"
            r"validity|accuracy of|illustrative calculations|isopotential)\b",
            low,
        ):
            funcs.append("validation")
        return funcs or ["derivation"]

    if sec == "results":
        funcs = []
        if "waveform" in head or "intermittent" in head or re.search(
            r"\b(?:waveform|waveforms|as a function of the time|as a function of time|"
            r"point a\b|point b\b|bounce|molten bridge|oscillat|hump|intermittenc|"
            r"discontinuit|transient)\b",
            low,
        ):
            funcs.append("waveform")
        if "surface" in head or "sem" in head or "wear track" in head or re.search(
            r"\b(?:sem\b|edx\b|eds\b|morphology|morphologies|micro-topography|"
            r"microtopography|fretted scar|wear track|debris|at%|delamination|ablation|"
            r"splashes|scratches|3d profile)\b",
            low,
        ):
            funcs.append("surface_analysis")
        if re.search(
            r"\b(?:as a function of|with the increase|increases with|decreases with|"
            r"regime map|fretting map|dependence of|normalized|threshold|effect of)\b",
            low,
        ):
            funcs.append("trend")
        return funcs or ["trend"]

    if sec == "mechanism":
        return ["explanation"]

    if sec == "conclusion":
        if re.search(r"(?:^|\s)(?:\([1-4]\)|\([I-IV]+\)|as follows|following features)", txt):
            return ["numbered"]
        return ["summary"]

    return []


def compute_feature_vector(text: str) -> list[float]:
    """Compute a 10-dimensional stylometric feature vector for typicality ranking."""
    sents = stylo.split_sentences(text)
    if not sents:
        return [0.0] * 10
    s_lens = [len(stylo.tokenize_words(s)) for s in sents if stylo.tokenize_words(s)]
    if not s_lens:
        return [0.0] * 10
    n_sents = len(s_lens)
    n_words = max(sum(s_lens), 1)
    mean_len = sum(s_lens) / n_sents
    std_len = math.sqrt(sum((x - mean_len) ** 2 for x in s_lens) / n_sents)
    passive_ratio = sum(1 for s in sents if stylo.PASSIVE_RE.search(s)) / n_sents

    tc: Counter[str] = Counter()
    conn_hits = 0
    it_hits = 0
    for s in sents:
        tc.update(stylo.analyze_sentence_tenses(s))
        if stylo.detect_initial_connective(s):
            conn_hits += 1
        if stylo.IT_PASSIVE_RE.search(s):
            it_hits += 1
    tot_tense = max(tc["present"] + tc["past"] + tc["present_perfect"], 1)
    pres_ratio = tc["present"] / tot_tense
    past_ratio = tc["past"] / tot_tense

    clean = stylo.PLACEHOLDER_RE.sub(" ", text)
    we_our = len(re.findall(r"\b(?:we|our|us)\b", clean, re.I)) / n_words * 100.0
    rep_verbs = sum(len(pat.findall(clean)) for pat in stylo.VERB_PATTERNS.values()) / n_words * 100.0
    sig_hits = sum(len(pat.findall(clean)) for pat in stylo.SIGNATURE_CONSTRUCTIONS.values()) / n_words * 100.0

    return [
        mean_len,
        std_len,
        passive_ratio * 100.0,
        pres_ratio * 100.0,
        past_ratio * 100.0,
        (conn_hits / n_sents) * 100.0,
        (it_hits / n_sents) * 100.0,
        we_our,
        rep_verbs,
        sig_hits,
    ]


def rank_for_slot(
    slot_cands: list[dict[str, Any]],
    target_min_w: int = 135,
    target_max_w: int = 255,
    top_k: int = 8,
) -> list[dict[str, Any]]:
    if not slot_cands:
        return []

    vecs = [compute_feature_vector(c["text"]) for c in slot_cands]
    weights = [float(c["effective_weight"]) for c in slot_cands]
    tot_w = sum(weights) or 1.0
    dim = len(vecs[0])

    # Weighted centroid & per-dimension SD for z-standardization
    centroid = [sum(vecs[i][d] * weights[i] for i in range(len(slot_cands))) / tot_w for d in range(dim)]
    sds = []
    for d in range(dim):
        var = sum(weights[i] * ((vecs[i][d] - centroid[d]) ** 2) for i in range(len(slot_cands))) / tot_w
        sds.append(max(math.sqrt(var), 1.0))

    scored: list[dict[str, Any]] = []
    for c, v in zip(slot_cands, vecs):
        dist = math.sqrt(sum(((v[d] - centroid[d]) / sds[d]) ** 2 for d in range(dim)) / dim)
        # Word-count window penalty outside [target_min_w, target_max_w]
        nw = c["n_words"]
        if nw < target_min_w:
            dist += (target_min_w - nw) / 80.0
        elif nw > target_max_w:
            dist += (nw - target_max_w) / 80.0
        # Penalize paragraphs containing known FIX_ERROR strings or inline table artifacts
        if re.search(r"\b(?:are resulted from|results into|our new designed|relevant with|same with|inversely proportion to|harness)\b", c["text"], re.I):
            dist += 0.5
        if re.search(r"Amplitude\s*\(μm\)\s*4,\s*7", c["text"]):
            dist += 1.5
        # Tier S bonus: multiply distance by 0.7 (docs/design_notes.md §6 Phase 4)
        final_score = dist * 0.7 if c["tier"] == "S" else dist
        rec = dict(c)
        rec["raw_centroid_distance"] = round(dist, 4)
        rec["typicality_distance"] = round(final_score, 4)
        scored.append(rec)

    scored.sort(key=lambda x: x["typicality_distance"])

    # Select top_k with diversity (max 2 per paper, no overlapping para_idx from same paper)
    selected: list[dict[str, Any]] = []
    paper_counts: Counter[str] = Counter()
    used_spans: set[tuple[str, str]] = set()

    for item in scored:
        pid = item["paper_id"]
        if paper_counts[pid] >= 2:
            continue
        pidx_str = str(item["para_idx"])
        if pidx_str.endswith(("a", "b")):
            span_keys = {(pid, pidx_str), (pid, pidx_str[:-1])}
        else:
            span_parts = [_base_idx(x) for x in pidx_str.split("-")]
            span_keys = {(pid, str(idx)) for idx in range(span_parts[0], span_parts[-1] + 1)} | {
                (pid, f"{idx}a") for idx in range(span_parts[0], span_parts[-1] + 1)
            } | {
                (pid, f"{idx}b") for idx in range(span_parts[0], span_parts[-1] + 1)
            }
        if any(k in used_spans for k in span_keys):
            continue
        selected.append(item)
        paper_counts[pid] += 1
        used_spans.update(span_keys)
        if len(selected) >= top_k:
            break

    # Ensure at least 2 Tier S candidates (if available in scored) appear in top_k
    s_in_sel = sum(1 for x in selected if x["tier"] == "S")
    if s_in_sel < 2:
        for item in scored:
            if item["tier"] != "S" or item in selected:
                continue
            pid = item["paper_id"]
            pidx_str = str(item["para_idx"])
            if pidx_str.endswith(("a", "b")):
                span_keys = {(pid, pidx_str), (pid, pidx_str[:-1])}
            else:
                span_parts = [_base_idx(x) for x in pidx_str.split("-")]
                span_keys = {(pid, str(idx)) for idx in range(span_parts[0], span_parts[-1] + 1)}
            if any(k in used_spans for k in span_keys):
                continue
            # Replace the last non-S item in selected
            for rev_i in range(len(selected) - 1, -1, -1):
                if selected[rev_i]["tier"] != "S":
                    selected[rev_i] = item
                    used_spans.update(span_keys)
                    s_in_sel += 1
                    break
            if s_in_sel >= 2:
                break
        selected.sort(key=lambda x: x["typicality_distance"])

    return selected


def main() -> int:
    cfg = load_config()
    d_dir = data_dir(cfg)
    paras_path = d_dir / "processed" / "paragraphs.jsonl"
    cand_root = d_dir / "candidates"
    cand_root.mkdir(parents=True, exist_ok=True)

    papers_by_id = {p.id: p for p in resolve_papers(cfg)}
    all_paras = [json.loads(line) for line in open(paras_path, encoding="utf-8")]

    # STRICT FILTER: only tiers S and A with split == "train"
    train_sa = [
        p for p in all_paras
        if p["tier"] in ("S", "A") and p["split"] == "train"
    ]
    for p in train_sa:
        meta = papers_by_id[p["paper_id"]].meta
        p["doi"] = meta.get("doi", "")
        p["venue"] = meta.get("venue", "")
        p["year"] = meta.get("year", "")
        p["open_access"] = bool(meta.get("open_access", False))

    windows = build_candidate_windows(train_sa)
    max_idx = defaultdict(int)
    for p in train_sa:
        max_idx[(p["paper_id"], p["section"])] = max(max_idx[(p["paper_id"], p["section"])], int(p["para_idx"]))

    # Also allow mechanism-rich paragraphs from P01/P13 results if needed for mechanism/explanation
    by_slot: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for w in windows:
        funcs = classify_functions(w, max_idx[(w["paper_id"], w["section"])])
        for fn in funcs:
            by_slot[(w["section"], fn)].append(w)
        # In P13 (S), "A. Validity of Analytical Model" is placed under IV. RESULTS AND DISCUSSION
        if w["section"] == "results" and "validity of" in w.get("heading", "").lower():
            by_slot[("modeling", "validation")].append(w)

    sections_taxonomy: dict[str, list[str]] = cfg["sections"]
    local_root = SKILL_DIR / "examples.local"
    pub_root = SKILL_DIR / "examples"
    n_local_written = 0
    n_oa_written = 0

    for sec, fn_list in sections_taxonomy.items():
        sec_dir = cand_root / sec
        sec_dir.mkdir(parents=True, exist_ok=True)
        local_sec_dir = local_root / sec
        local_sec_dir.mkdir(parents=True, exist_ok=True)
        pub_sec_dir = pub_root / sec
        pub_sec_dir.mkdir(parents=True, exist_ok=True)
        sec_used_local: set[tuple[str, str]] = set()
        sec_used_oa: set[tuple[str, str]] = set()

        for fn in fn_list:
            cands = by_slot[(sec, fn)]
            min_w = 90 if sec == "abstract" else 130
            ranked = rank_for_slot(cands, target_min_w=min_w, target_max_w=255, top_k=8)
            out_file = sec_dir / f"{fn}.jsonl"
            with open(out_file, "w", encoding="utf-8") as f:
                for rank_idx, r in enumerate(ranked, 1):
                    r["rank"] = rank_idx
                    r["function"] = fn
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")

            # Export 2-3 private golden excerpts to examples.local/<sec>/<fn>_0{1,2,3}.md
            # Guarantee at least 1 Tier S excerpt first, then distinct papers, preferring paragraphs not yet exported in this section
            s_rows = [r for r in ranked if r["tier"] == "S"]
            other_rows = [r for r in ranked if r["tier"] != "S"]
            chosen: list[dict[str, Any]] = []
            used_pids: set[str] = set()
            if s_rows:
                s_unused = [r for r in s_rows if (r["paper_id"], str(r["para_idx"])) not in sec_used_local]
                pick_s = s_unused[0] if s_unused else s_rows[0]
                chosen.append(pick_s)
                used_pids.add(pick_s["paper_id"])
            pool_rest = [r for r in (s_rows + other_rows) if (r["paper_id"], str(r["para_idx"])) not in sec_used_local] + (s_rows + other_rows)
            for r in pool_rest:
                if r["paper_id"] not in used_pids:
                    chosen.append(r)
                    used_pids.add(r["paper_id"])
                if len(chosen) >= 3:
                    break
            for c in chosen:
                sec_used_local.add((c["paper_id"], str(c["para_idx"])))

            rules = RULE_MAP.get((sec, fn), "[R01, R02]")
            for idx_ex, c in enumerate(chosen, 1):
                assert c["split"] == "train" and c["tier"] in ("S", "A")
                doi_str = f", doi:{c['doi']}" if c.get("doi") else ""
                src_str = f"{c['paper_id']} ({c.get('venue', '')}, {c.get('year', '')}{doi_str})"
                md = (
                    f"---\n"
                    f"section: {sec}\n"
                    f"function: {fn}\n"
                    f"source: \"{src_str}\"\n"
                    f"tier: {c['tier']}\n"
                    f"para_idx: \"{c['para_idx']}\"\n"
                    f"words: {c['n_words']}\n"
                    f"typicality_distance: {c['typicality_distance']}\n"
                    f"rules: {rules}\n"
                    f"---\n\n"
                    f"{c['text']}\n"
                )
                (local_sec_dir / f"{fn}_0{idx_ex}.md").write_text(md, encoding="utf-8")
                n_local_written += 1

            # Also export open-access P22 excerpt to public examples/<sec>/<fn>_02_oa.md if available in slot
            oa_cands = [
                r for r in cands
                if r.get("open_access") and r["paper_id"] == "P22" and passes_style_lint(r["text"], sec)
            ]
            oa_cands.sort(key=lambda r: abs(r["n_words"] - 190))
            oa_unused = [r for r in oa_cands if (r["paper_id"], str(r["para_idx"])) not in sec_used_oa]
            if oa_unused:
                c_oa = oa_unused[0]
                sec_used_oa.add((c_oa["paper_id"], str(c_oa["para_idx"])))
                src_oa = f"P22 (IEEE Access 2020, doi:{c_oa['doi']}, CC BY 4.0)"
                md_oa = (
                    f"---\n"
                    f"section: {sec}\n"
                    f"function: {fn}\n"
                    f"source: \"{src_oa}\"\n"
                    f"tier: {c_oa['tier']}\n"
                    f"para_idx: \"{c_oa['para_idx']}\"\n"
                    f"words: {c_oa['n_words']}\n"
                    f"rules: {rules}\n"
                    f"---\n\n"
                    f"{c_oa['text']}\n"
                )
                (pub_sec_dir / f"{fn}_02_oa.md").write_text(md_oa, encoding="utf-8")
                n_oa_written += 1
            elif (pub_sec_dir / f"{fn}_02_oa.md").exists():
                (pub_sec_dir / f"{fn}_02_oa.md").unlink()

            s_cnt = sum(1 for r in ranked if r["tier"] == "S")
            oa_cnt = len(oa_cands)
            top_pids = [f"{r['paper_id']}({r['tier']},{r['n_words']}w,d={r['typicality_distance']:.2f})" for r in ranked[:4]]
            print(f"{sec:12s}/{fn:16s}: {len(ranked):2d} ranked (S={s_cnt}, OA={oa_cnt}) | local={len(chosen)} | top: {', '.join(top_pids)}")

    print(f"\nExported {n_local_written} private golden excerpts to {local_root}")
    print(f"Exported {n_oa_written} open-access (P22) excerpts to {pub_root}")
    export_local_contrastive_pairs(local_root)
    return 0


def _strip_frontmatter(md_text: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = {}
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n*(.*)\Z", md_text, flags=re.DOTALL)
    if not m:
        return meta, md_text.strip()
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, m.group(2).strip()


def export_local_contrastive_pairs(local_root: Path) -> None:
    """Export 8 private Tier-S contrastive pairs to examples.local/contrastive/."""
    c_dir = local_root / "contrastive"
    c_dir.mkdir(parents=True, exist_ok=True)
    specs = [
        (
            "pair_01_abstract.md",
            "abstract/full_01.md",
            "Surface coatings are ubiquitously employed on spherical electrical contacts to enhance interfacial durability, making the accurate prediction of electrical contact resistance imperative for connector design. In this study, we comprehensively investigate the contact resistance of coated spherical contacts by leveraging both analytical modeling and finite-element simulations. Specifically, we systematically evaluate the interplay among contact radius, coating thickness, and the substrate-to-coating resistivity ratio across an extensive spectrum of geometric aspect ratios. Our formulation decomposes the overall contact resistance into three distinct physical contributions—spreading resistance, transition resistance, and bulk resistance—and benchmarks the normalized resistance trends against classical Holm theory.",
            [
                ("Surface coatings are ubiquitously employed ... making the accurate prediction ... imperative", "The electrical contact resistance of two spherical contacts with coating is studied by using...", "R03, R13, F25", "Opens directly with the object of study and method in passive voice rather than a generic importance hook."),
                ("we comprehensively investigate ... by leveraging", "is studied by using analytical method and finite-element method simulation software", "R10, R14, F17", "Avoids 'we' in Abstracts (R14) and uses 'by using' (R10) instead of 'leveraging' (F17)."),
                ("three distinct physical contributions—spreading resistance, transition resistance, and bulk resistance—", "three components of resistance, that is, the spreading resistance, the transition resistance, and the bulk resistance.", "R07, F17", "Uses ', that is,' (R07) for appositive enumeration instead of em-dashes."),
            ],
        ),
        (
            "pair_02_introduction_prior_work.md",
            "introduction/prior_work_01.md",
            "Elucidating the failure mechanisms of gold-plated electrical contacts subjected to high-frequency, high-acceleration fretting vibration is of paramount importance for aerospace reliability. As dictated by sinusoidal kinematics in Eqs. (1)–(3), peak acceleration is governed by the coupled interplay of vibration frequency and displacement amplitude. Numerous researchers have previously explored fretting degradation across varying kinematic regimes. Notably, Braunovic et al. [CIT] conducted a comprehensive review of slip amplitude effects across diverse contact metallurgy, demonstrating that larger slip amplitudes consistently accelerate contact resistance degradation, whereas smaller amplitudes restrict the oxidized contact area and prolong electrical life. Similarly, Hannel et al. [CIT] established that exceeding a critical amplitude threshold triggers gross slip, which rapidly strips the noble coating. Conversely, Park et al. [CIT] observed in tin-plated copper contacts that a 5 μm track reached the 0.1 Ω failure threshold faster than a 25 μm track, attributing this counterintuitive trend to earlier oxide percolation within a tightly confined wear zone.",
            [
                ("Elucidating the failure mechanisms ... is of paramount importance", "It is becoming increasingly important to understand and determine the failure mechanism...", "R08, R16, F17", "Uses preparatory 'It is...' frame (R08) and plain verbs ('understand and determine') instead of 'Elucidating' and 'paramount'."),
                ("is governed by the coupled interplay of", "is synthetically decided by both frequency and amplitude, based on...", "R16, F17", "Avoids banned AI cliché 'interplay' (F17)."),
                ("attributing this counterintuitive trend to earlier oxide percolation", "This paper argued that within a confined oxidation area the percolation limit ... reach earlier", "R01, R11, F24", "Uses a separate finite sentence with reporting verb 'argued that' (R11) instead of a trailing participial '-ing' clause (F24)."),
            ],
        ),
        (
            "pair_03_experimental_procedure.md",
            "experimental/procedure_01.md",
            "Immediately following the electroplating process, fretting endurance trials were initiated. Prior to mounting, both the hemispherical rider and flat coupon were thoroughly degreased via ultrasonic agitation in alcohol and distilled water, dried, and precisely aligned to establish a sphere-on-plane point contact configuration. To continuously track interfacial resistance evolution across fretting cycles under a 10 mA DC load, we utilized a four-wire Kelvin sensing setup ([FIG 3]). Concurrently, normal and tangential contact forces were monitored via a strain gauge and a piezoelectric dynamic sensor, while a high-resolution laser displacement transducer (ILD2220, Epsilon, Germany, 30 nm resolution) ensured constant relative slip amplitude. High-speed data acquisition was orchestrated using a PC-based DAQ card operating at 500 kHz. Post-test microstructural characterization was conducted by leveraging SEM, EDX, X-ray line mapping, and confocal laser scanning microscopy to unravel wear damage, oxidation severity, and 3D scar topography.",
            [
                ("To continuously track interfacial resistance evolution ... we utilized a four-wire Kelvin sensing setup ([FIG 3]).", "By using the 4-wires method (shown in [FIG 3], the contact resistance was continuously measured as a function of fretting cycles under current loads of 10 mA.", "R06, R10, R19, R20", "Uses Ren's signature experimental opener 'By using the 4-wires method (shown in [FIG N]), the contact resistance was continuously measured as a function of...'."),
                ("while a high-resolution laser displacement transducer ... ensured", "A laser displacement transducer (ILD2220, Epsilon, Germany), which has the resolution of 30 nm, was introduced to further ensure that...", "R03, R20", "Uses passive 'was introduced to further ensure' and inline parenthetical vendor specs (R20)."),
                ("Post-test microstructural characterization was conducted by leveraging SEM ... to unravel", "Scanning electron microscopy (SEM), energy dispersive analysis of X-rays (EDX) and X-ray line mapping were used to characterize the extent of...", "R10, R21, F17", "Places analytical instruments as passive grammatical subjects ('SEM, EDX ... were used to characterize the extent of...') and avoids 'leveraging'/'unravel'."),
            ],
        ),
        (
            "pair_04_modeling_validation.md",
            "modeling/validation_01.md",
            "[FIG 9] illustrates the dependence of the spreading resistance Rc—derived from analytical expression (14) alongside COMSOL Multiphysics finite-element simulations—on the normalized constriction radius a/h. The results clearly demonstrate a monotonic decline in spreading resistance with increasing a/h, while remaining virtually insensitive to variations in the conductivity ratio g within the small-spot regime (a/h < 1). Consistent with the trends observed in [FIG 8], the numerical simulations exhibit remarkable agreement with our analytical predictions for a/h < 1, yielding a maximum discrepancy of merely 0.108 mΩ. At larger aspect ratios (a/h = 10, g = 100), however, the divergence between the two approaches expands to 0.365 mΩ. In this plot, the continuous curve represents analytical relation (13) whereas the cross markers denote COMSOL simulation data obtained at a fixed coating thickness of h = 1 μm across contact radii spanning 0.01–10 μm.",
            [
                ("[FIG 9] illustrates the dependence of ... on the normalized constriction radius a/h.", "[FIG 9] shows the variations of the spreading resistance Rc as described by (14) and COMSOL Multiphysics software simulation, with the normalized constriction radius a/h.", "R04, R22, R24", "Uses '[FIG 9] shows the variations of...' (R04, R25) and explicit software naming 'COMSOL Multiphysics software simulation' (R22)."),
                ("exhibit remarkable agreement with our analytical predictions ... yielding a maximum discrepancy", "the simulations are in excellent agreement with the analytical calculations when a/h < 1. And the corresponding maximum deviation of Rc is only 0.108 m .", "R01, R24, F24", "Splits the agreement statement and the quantitative maximum deviation into two finite sentences instead of a participial tail ('yielding...', F24)."),
            ],
        ),
        (
            "pair_05_results_waveform.md",
            "results/waveform_01.md",
            "The contact resistance evolution observed at a large slip amplitude of 62 μm diverges markedly from that recorded at 15 μm. Specifically, the premature and pronounced surge in contact resistance is tightly coupled to the elevated sliding amplitude and interfacial velocity. Amplifying the fretting amplitude accelerates noble gold coating wear-through, which directly triggers a rapid escalation in contact resistance. Concurrently, the steady, low-fluctuation upward drift in resistance reflects a progressive shrinkage of the effective metallic conducting area across the mated wear scar. Throughout each fretting trial, transient tangential force waveforms were continuously captured, and the cycle-level root-mean-square tangential force FRMS was quantified via [EQ].",
            [
                ("diverges markedly from that recorded at 15 μm", "is apparently different from the 15 μm case.", "R12, R26", "Uses plain comparative adjective ('is apparently different from the 15 μm case') rather than 'diverges markedly'."),
                ("Amplifying the fretting amplitude accelerates noble gold coating wear-through, which directly triggers", "With the increase of fretting amplitude, the wear on the gold coating increases, which results in the rapid increment of contact resistance.", "R06, R26", "Uses Ren's signature prepositional trend opener 'With the increase of <X>, the <Y> increases, which results in...' (R06)."),
                ("Concurrently, the steady, low-fluctuation upward drift", "In the meantime, the continued increase of resistance without high fluctuation corresponds to...", "R05, R26", "Uses 'In the meantime,' (R05) and 'corresponds to' (R26)."),
            ],
        ),
        (
            "pair_06_results_surface_analysis.md",
            "results/surface_analysis_01.md",
            "[FIG 5] depicts the evolution of the RMS tangential force across fretting cycles at 200 Hz for slip amplitudes of 4 μm, 15 μm, and 62 μm. Across all three amplitude regimes, the tangential force remains minimal during the initial 3500 cycles before undergoing a sharp upward transition and diverging into distinct post-transition trajectories. Specifically, at 4 μm, the RMS force stabilizes around 1.7 N for the remainder of the test, whereas both the 15 μm and 62 μm profiles exhibit two-stage decay behavior. Notably, the 15 μm condition attains a higher peak force of 3.75 N accompanied by pronounced cyclic fluctuations, mirroring the erratic contact resistance spikes observed in [FIG 5]. Fundamentally, interfacial friction is governed by the interplay among surface chemistry [CIT], third-body wear debris accumulation [CIT], and oxide film mechanics [CIT]: while an intact gold layer stabilizes friction and trapped third-body debris elevates tangential force under gross slip [CIT], subsequent copper substrate oxidation acts as a solid lubricant that reduces friction [CIT].",
            [
                ("[FIG 5] depicts the evolution of the RMS tangential force across fretting cycles", "The obtained RMS value of tangential force, as a function of fretting cycles for ..., is shown in [FIG 5].", "R04, R06, R25", "Uses passive data-pointer opener ('The obtained <Y>, as a function of <X>, is shown in [FIG N]') instead of '[FIG 5] depicts'."),
                ("mirroring the erratic contact resistance spikes", "This is consistent with the little change and sharp fluctuation of contact resistance shown in [FIG 5].", "R01, R27, F24", "Uses a separate finite sentence ('This is consistent with...') rather than a participial '-ing' clause ('mirroring...', F24)."),
                ("Fundamentally, interfacial friction is governed by the interplay among", "Friction is mainly determined by the nature of the contact interface [CIT], accumulation of wear debris [CIT] and mechanical properties of oxidative films [CIT]", "R28, F17", "Uses 'is mainly determined by' and avoids banned word 'interplay' (F17)."),
            ],
        ),
        (
            "pair_07_mechanism_explanation.md",
            "mechanism/explanation_01.md",
            "Evaluating the thermoelastic instability (TEI) criterion for copper (λ = 394 W/(m·K), E = 115 GPa, α = 16.5 × 10^-6 K^-1, μ = 0.2, and κ = π/120 rad/μm derived from the 200 Hz / 62 μm wear profile) via Eq. (5) yields a critical sliding velocity of Vn = 54.36 m/s. Given that the actual peak sliding velocity in our experiments never exceeds 0.08 m/s, standalone TEI effects cannot account for the dramatic contact area reduction and Regime III electrical failure, rendering a purely thermoelastic explanation inadequate. Instead, neglecting electrical film heating, the interfacial frictional heat flux is governed by [EQ], which upon substituting the sinusoidal kinematics of Eq. (1) and tangential force relation [EQ] transforms into [EQ]. As revealed by Eq. (8), peak frictional heating scales directly with fretting frequency, slip amplitude, and tangential force, implying that elevated frequencies and amplitudes drive substantial interfacial temperature rises and severe oxidative degradation.",
            [
                ("Given that the actual peak sliding velocity ... standalone TEI effects cannot account for ... rendering a purely thermoelastic explanation inadequate.", "However, the actual maximum sliding speed is no more than 0.08 m/s ... The single TEI model and explanations could not result in such a substantial change ... The analysis is therefore incomplete.", "R01, R05, R30, F24", "Breaks the quantitative refutation of an alternative hypothesis into three short, crisp declarative sentences ending with 'The analysis is therefore incomplete.'"),
                ("As revealed by Eq. (8), peak frictional heating scales directly with ... implying that", "As can be seen in Eq. (8), the frictional heat source maximum is proportional to ... An increase of fretting frequency and/or amplitude corresponds to a rise in contact temperature", "R06, R26, R28", "Uses 'As can be seen in Eq. (8), ... is proportional to ...' and a separate sentence with 'corresponds to'."),
            ],
        ),
        (
            "pair_08_conclusion_numbered.md",
            "conclusion/numbered_01.md",
            "In summary, the electrical contact resistance trajectory during fretting progresses through four characteristic phases—initial stability, gradual elevation, rapid escalation, and severe instability—driven sequentially by noble gold wear-through, copper substrate exposure and oxidation, and third-body debris sliding. Varying the applied DC current load introduces three key phenomena: (I) elevated current loads prolong the fretting lifetime prior to reaching the resistance threshold; (II) lower current loads yield systematically higher contact resistance values; and (III) resistance fluctuations intensify at lower currents. These current-dependent behaviors stem from the capacity of higher currents to breakdown insulating films and enlarge conducting a-spot patches, a mechanism corroborated by oxide particle size distributions and EDX line profiles. Finally, morphological inspection reveals five distinct microstructural zones—scratches, particles, cracks, deposits, and splashes—whose heterogeneous conductivity distributions govern the observed resistance instability.",
            [
                ("four characteristic phases—initial stability, gradual elevation, rapid escalation, and severe instability—driven sequentially by", "four stages, namely low and stable, slight rise, sharp increase and severe fluctuation, which results from...", "R07, R31", "Uses ', namely' (R07) instead of em-dashes and names the four stages with plain descriptive adjectives."),
                ("Varying the applied DC current load introduces three key phenomena: (I)...", "The effects of variation in current loads can be shown as following features: (I)...", "R31, R32", "Uses numbered inline points (I), (II), (III) with direct comparative clauses ('increases as the current loads increase')."),
                ("five distinct microstructural zones—scratches, particles, cracks, deposits, and splashes—whose heterogeneous conductivity", "five typical regions that are shared by the four fretted scars, namely the scratches, the particles, the cracks, the deposits and the splashes, which have different conductivities.", "R03, R07, R32", "Uses ', namely' + 'which have different conductivities. Therefore...' instead of em-dashes and 'heterogeneous'."),
            ],
        ),
    ]

    for out_name, src_rel, ai_text, diffs in specs:
        src_path = local_root / src_rel
        meta, ren_text = _strip_frontmatter(src_path.read_text(encoding="utf-8"))
        rows = "\n".join(f"| `{a}` | `{r}` | `{rl}` | {w} |" for a, r, rl, w in diffs)
        md = (
            f"---\n"
            f"section: {meta.get('section', '')}\n"
            f"function: {meta.get('function', '')}\n"
            f"source: \"{meta.get('source', '')}\"\n"
            f"tier: {meta.get('tier', 'S')}\n"
            f"rules: {meta.get('rules', '[R01]')}\n"
            f"---\n\n"
            f"### AI-default\n\n"
            f"{ai_text}\n\n"
            f"### Ren\n\n"
            f"{ren_text}\n\n"
            f"### Differences\n\n"
            f"| AI-default | Ren | Rule | Why |\n"
            f"| :--- | :--- | :--- | :--- |\n"
            f"{rows}\n"
        )
        (c_dir / out_name).write_text(md, encoding="utf-8")
    print(f"Exported {len(specs)} private Tier-S contrastive pairs to {c_dir}")


if __name__ == "__main__":
    sys.exit(main())

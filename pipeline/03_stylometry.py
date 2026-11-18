"""Phase 2.1 — Quantitative stylometry (weighted, per section).

Computes weighted stylometric statistics from ``data/processed/paragraphs.jsonl``:
  - Primary profile: tiers S+A with ``split == "train"`` (weighted by ``effective_weight``)
  - Comparison subsets:
      * ``tier_S`` (core exemplars P01, P03, P13)
      * ``tier_A_train`` (Ren first-author train papers)
      * ``secondary_B`` (student first-author papers, split == "secondary")
      * ``early_le_2015`` vs ``late_ge_2017`` (within S+A train)

Per section (abstract, introduction, experimental, modeling, results, mechanism, conclusion)
and overall, computes:
  1. Sentence length distribution (mean, std, P10, P25, P50, P75, P90)
  2. Paragraph length distribution (words & sentences: mean, std, P25, P50, P75, P90)
  3. Passive voice ratio (per sentence & per 100 words) and "we"/"our" rate
  4. Formal-subject constructions ("It is shown/found/demonstrated/noted that ...")
  5. Tense distribution (present / past / present_perfect / modal ratios)
  6. Sentence-initial and paragraph-initial connectives ranking
  7. Reporting / research verbs ranking (lemmatized)
  8. Signature adverbs ranking and sentence position (initial / medial / post-verbal-final)
  9. Hedging vs booster rates, punctuation rates (semicolon, parenthesis, dash, colon, slash)
  10. US vs UK spelling, number+unit formatting ("0.2/0.5/1 A", "25~150 nm/s"), abbreviation definitions
  11. Signature collocations & non-native habitual constructions

Outputs:
  - ``data/processed/stats.json``
  - ``data/processed/stats_report.md``

Usage:
    python pipeline/03_stylometry.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from common import data_dir, load_config, resolve_papers

CANONICAL_SECTIONS = [
    "abstract",
    "introduction",
    "experimental",
    "modeling",
    "results",
    "mechanism",
    "conclusion",
]

ABBREV_RE = re.compile(r"\b(?:Fig|Figs|Eq|Eqs|Ref|Refs|e\.g|i\.e|et al|vs|No|Vol|approx|Dr|Prof|Mr|St)\.")
PLACEHOLDER_RE = re.compile(r"\[(?:CIT|EQ|FIG\s*\d+|TAB\s*\d+)\]")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-']*|\d+(?:\.\d+)?")
ALPHA_WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-']*")

# Passive voice pattern (matches style_lint.py plus extended irregular past participles)
PASSIVE_AUX_PART = (
    r"\b(?:is|are|was|were|be|been|being)\s+"
    r"(?:(?:not|never|also|only|still|even|always|often|usually|generally|commonly|"
    r"widely|mainly|mostly|chiefly|largely|greatly|significantly|substantially|"
    r"explicitly|clearly|directly|closely|easily|readily|carefully|simultaneously|"
    r"individually|separately|continuously|progressively|gradually|first|firstly|"
    r"then|finally|subsequently|therefore|thus)\s+)*"
    r"(?:\w+ed|\w+en|built|made|shown|found|known|set|put|held|done|drawn|taken|"
    r"given|seen|kept|left|lost|meant|met|paid|read|run|said|sent|shot|shut|slept|"
    r"spent|split|spread|stood|struck|stuck|swept|taught|thought|told|understood|"
    r"won|worn|wound|written|borne|born|bound|brought|bought|caught|chosen|cut)\b"
)
PASSIVE_RE = re.compile(PASSIVE_AUX_PART, re.I)

# Formal-subject "It is/was <VBN/ADJ> that ..." constructions
IT_PASSIVE_RE = re.compile(
    r"\bIt\s+(?:is|was|has\s+been|can\s+be|could\s+be|should\s+be)\s+"
    r"(?:also\s+|well\s+|worth\s+|widely\s+|generally\s+|commonly\s+)?"
    r"([a-z]+(?:ed|en|wn|nd|nt|id|ht|ing)|clear|obvious|evident|noteworthy|reasonable|challengeable|necessary|important|urgent|top-urgent)"
    r"(?:\s+to\s+[a-z]+|\s+that\b)",
    re.I,
)

# Tense detection patterns on finite verb groups
PRESENT_PERFECT_RE = re.compile(
    r"\b(?:has|have)\s+(?:not\s+|also\s+|already\s+|always\s+|ever\s+|never\s+|widely\s+|extensively\s+)?"
    r"(?:been|\w+ed|\w+en|shown|found|known|done|made|built|seen|taken|given|gone|come|become|begun|run|set|put)\b",
    re.I,
)
MODAL_VERB_RE = re.compile(
    r"\b(?:can|could|will|would|may|might|shall|should|must)\s+(?:not\s+|also\s+)?(?:be|[a-z]+)\b",
    re.I,
)
PAST_AUX_RE = re.compile(r"\b(?:was|were|had|did)\b", re.I)
PRESENT_AUX_RE = re.compile(r"\b(?:is|are|am|does|do)\b", re.I)

# Common irregular past & 3sg present forms in scientific prose
IRREG_PAST = {
    "found", "showed", "made", "built", "took", "gave", "came", "became", "began",
    "broke", "chose", "fell", "felt", "held", "kept", "knew", "left", "led", "lost",
    "meant", "met", "ran", "rose", "said", "saw", "sent", "set", "spoke", "spent",
    "stood", "struck", "stuck", "thought", "told", "understood", "went", "won", "wore", "wrote",
}
PAST_PARTICIPLES_ONLY = {
    "shown", "known", "taken", "given", "seen", "done", "gone", "been", "written",
    "broken", "chosen", "fallen", "risen", "spoken", "worn", "driven", "proven",
}
ADJECTIVAL_ED = {
    "based", "plated", "coated", "shaped", "sized", "used", "related", "associated",
    "Mentioned", "mentioned", "abovementioned", "above-mentioned", "designed", "measured",
    "calculated", "simulated", "observed", "recorded", "obtained", "proposed", "presented",
    "coupled", "closed", "opened", "fixed", "melted", "molten", "welded", "eroded",
    "fretted", "degraded", "oxidized", "polished", "degreased", "mounted", "connected",
    "interfaced", "programmed", "controlled", "applied", "selected", "defined", "normalized",
    "detailed", "varied", "different", "combined", "localized", "distributed", "accumulated",
    "corrugated", "cambered", "insulated", "sealed", "vented", "loaded", "unloaded",
}

# Multi-word and single-word sentence-initial connectives
CONNECTIVES = [
    "On the other hand",
    "In addition",
    "In general",
    "In parallel",
    "In contrast",
    "In particular",
    "In summary",
    "In conclusion",
    "As a result",
    "As a consequence",
    "For example",
    "For instance",
    "For simplicity",
    "At the same time",
    "At present",
    "To sum up",
    "However",
    "Furthermore",
    "Moreover",
    "Subsequently",
    "Therefore",
    "Meanwhile",
    "Nevertheless",
    "Nonetheless",
    "Consequently",
    "Accordingly",
    "Conversely",
    "Similarly",
    "Likewise",
    "Otherwise",
    "Besides",
    "Also",
    "Then",
    "Thus",
    "Hence",
    "First",
    "Firstly",
    "Second",
    "Secondly",
    "Third",
    "Thirdly",
    "Next",
    "Finally",
    "Lastly",
    "Specifically",
    "Specially",
    "Particularly",
    "Especially",
    "Obviously",
    "Evidently",
    "Clearly",
    "Admittedly",
    "Generally",
    "Actually",
    "Theoretically",
    "Experimentally",
    "Notably",
    "Importantly",
    "Interestingly",
    "Fortunately",
    "Unfortunately",
    " Inevitably",
    "Inevitably",
    "Simultaneously",
    "Synchronously",
]

# Reporting / academic verbs to track (lemma -> surface forms regex)
REPORTING_VERB_LEMMAS = [
    "investigate", "show", "present", "observe", "measure", "calculate", "indicate",
    "propose", "find", "determine", "analyze", "evaluate", "study", "obtain", "confirm",
    "describe", "explain", "demonstrate", "define", "discuss", "record", "compare",
    "introduce", "attribute", "correlate", "depend", "cause", "lead", "result",
    "occur", "appear", "remain", "reach", "increase", "decrease", "fluctuate",
    "reveal", "state", "report", "conclude", "suggest", "assume", "consider",
    "verify", "validate", "simulate", "model", "deduce", "express", "write",
]

HEDGING_WORDS = {
    "may", "might", "could", "would", "approximately", "about", "around", "generally",
    "usually", "often", "relatively", "almost", "nearly", "possible", "possibly",
    "probably", "roughly", "slightly", "somewhat", "partially", "partly", "seem",
    "seems", "seemed", "tend", "tends", "tended", "likely",
}

BOOSTER_WORDS = {
    "very", "always", "greatly", "significantly", "substantially", "seriously",
    "considerably", "dramatically", "drastically", "extremely", "clearly", "obviously",
    "evidently", "explicitly", "crucial", "essential", "indispensable", "critical",
    "dominant", "remarkable", "appreciable", "appreciably", "markedly", "severely",
    "sharply", "rapidly", "totally", "completely", "entirely", "absolutely", "definitely",
    "strongly", "heavily", "closely", "distinctly", "inevitably", "undoubtedly",
}

US_UK_PAIRS = [
    ("behavior", "behaviour"),
    ("behaviors", "behaviours"),
    ("analyze", "analyse"),
    ("analyzed", "analysed"),
    ("analyzing", "analysing"),
    ("modeling", "modelling"),
    ("modeled", "modelled"),
    ("color", "colour"),
    ("colors", "colours"),
    ("center", "centre"),
    ("centers", "centres"),
    ("meter", "metre"),
    ("meters", "metres"),
    ("oxidize", "oxidise"),
    ("oxidized", "oxidised"),
    ("oxidization", "oxidisation"),
    ("summarize", "summarise"),
    ("summarized", "summarised"),
    ("characterize", "characterise"),
    ("characterized", "characterised"),
    ("vapor", "vapour"),
]

SIGNATURE_CONSTRUCTIONS = {
    "explicitly": re.compile(r"\bexplicitly\b", re.I),
    "<verb>_explicitly": re.compile(
        r"\b(?:recorded|investigated|measured|analyzed|addressed|described|interpreted|presented|explained|studied|shown|calculated|increases?|decreases?)\s+explicitly\b",
        re.I,
    ),
    "correlates_closely_with": re.compile(r"\b(?:closely\s+correlates?\s+with|correlates?\s+closely\s+with)\b", re.I),
    "closely_dependent_on": re.compile(r"\b(?:closely|greatly|significantly)\s+dependent\s+on\b", re.I),
    "our_designed_rig_switch": re.compile(
        r"\b(?:our\s+(?:newly\s+|new\s+)?designed\s+(?:novel\s+)?(?:test\s+rig|model\s+switch|apparatus)|self-designed\s+test\s+rig)\b",
        re.I,
    ),
    "very_important_concern_issue": re.compile(r"\ba\s+very\s+important\s+(?:concern|issue)\s+(?:to|in|for)\b", re.I),
    "it_is_shown_found_that": re.compile(
        r"\bIt\s+(?:is|was)\s+(?:shown|found|demonstrated|noted|determined|confirmed|considered|admitted)\s+that\b",
        re.I,
    ),
    "in_this_paper_study": re.compile(r"\bIn\s+this\s+(?:paper|study|work)\b", re.I),
    "as_a_function_of": re.compile(r"\bas\s+a\s+function\s+of\b", re.I),
    "is_attributed_to": re.compile(r"\b(?:is|are|was|were)\s+(?:mainly\s+)?attributed\s+to\b", re.I),
    "are_resulted_from": re.compile(r"\b(?:is|are|was|were)\s+resulted\s+(?:from|by)\b", re.I),
    "results_from": re.compile(r"\bresults?\s+from\b", re.I),
    "regards_to_nonstandard": re.compile(r"\b(?:Regards\s+to|Regarding\s+to|In\s+terms\s+to)\b"),
    "ever_published": re.compile(r"\bever\s+published\b", re.I),
    "also_sentence_initial": re.compile(r"(?:^|(?<=[.!?]\s))Also,\s"),
}


def split_sentences(text: str) -> list[str]:
    """Sentence splitter aligned with skills/ren-style-skill/scripts/style_lint.py."""
    protected = ABBREV_RE.sub(lambda m: m.group(0).replace(".", "<DOT>"), text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\[(])", protected)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def tokenize_words(s: str) -> list[str]:
    """Word tokenizer aligned with style_lint.py (excludes [CIT]/[EQ]/[FIG n] placeholders)."""
    cleaned = PLACEHOLDER_RE.sub(" ", s)
    return WORD_RE.findall(cleaned)


def weighted_quantile(values_weights: list[tuple[float, float]], q: float) -> float:
    if not values_weights:
        return 0.0
    vw = sorted(values_weights, key=lambda x: x[0])
    total_w = sum(w for _, w in vw)
    if total_w <= 0:
        return 0.0
    target = q * total_w
    acc = 0.0
    for val, w in vw:
        acc += w
        if acc >= target:
            return round(float(val), 2)
    return round(float(vw[-1][0]), 2)


def weighted_mean_std(values_weights: list[tuple[float, float]]) -> tuple[float, float]:
    if not values_weights:
        return 0.0, 0.0
    total_w = sum(w for _, w in values_weights)
    if total_w <= 0:
        return 0.0, 0.0
    mean = sum(v * w for v, w in values_weights) / total_w
    var = sum(w * ((v - mean) ** 2) for v, w in values_weights) / total_w
    return round(mean, 2), round(math.sqrt(max(var, 0.0)), 2)


def verb_forms_regex(lemma: str) -> re.Pattern:
    """Build surface-form regex for a reporting verb lemma."""
    if lemma.endswith("e"):
        stem = lemma[:-1]
        pat = rf"\b(?:{lemma}|{lemma}s|{lemma}d|{stem}ing)\b"
    elif lemma.endswith("y") and lemma[-2:] not in ("ay", "ey", "oy", "uy"):
        stem = lemma[:-1]
        pat = rf"\b(?:{lemma}|{stem}ies|{stem}ied|{lemma}ing)\b"
    elif lemma == "find":
        pat = r"\b(?:find|finds|found|finding)\b"
    elif lemma == "show":
        pat = r"\b(?:show|shows|showed|shown|showing)\b"
    elif lemma == "lead":
        pat = r"\b(?:lead|leads|led|leading)\b"
    elif lemma == "write":
        pat = r"\b(?:write|writes|wrote|written|writing)\b"
    else:
        pat = rf"\b(?:{lemma}|{lemma}s|{lemma}es|{lemma}ed|{lemma}ing)\b"
    return re.compile(pat, re.I)


VERB_PATTERNS = {lem: verb_forms_regex(lem) for lem in REPORTING_VERB_LEMMAS}


def analyze_sentence_tenses(sent: str) -> Counter[str]:
    """Count finite verb tense cues (present, past, present_perfect, modal) in a sentence."""
    c: Counter[str] = Counter()
    s = PLACEHOLDER_RE.sub(" ", sent)
    n_pp = len(PRESENT_PERFECT_RE.findall(s))
    if n_pp:
        c["present_perfect"] += n_pp
        s = PRESENT_PERFECT_RE.sub(" ", s)
    n_mod = len(MODAL_VERB_RE.findall(s))
    if n_mod:
        c["modal"] += n_mod
        s = MODAL_VERB_RE.sub(" ", s)
    c["past"] += len(PAST_AUX_RE.findall(s))
    c["present"] += len(PRESENT_AUX_RE.findall(s))

    tokens = [t.lower() for t in ALPHA_WORD_RE.findall(s)]
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i > 0 else ""
        if tok in IRREG_PAST:
            if tok == "found" and prev in ("is", "are", "was", "were", "be", "been", "has", "have"):
                continue
            c["past"] += 1
        elif tok.endswith("ed") and len(tok) > 4 and tok not in ADJECTIVAL_ED and tok not in PAST_PARTICIPLES_ONLY:
            if prev not in ("is", "are", "was", "were", "be", "been", "being", "has", "have", "had", "the", "a", "an", "of", "in", "with", "for", "by"):
                c["past"] += 1
        elif len(tok) > 4 and (tok.endswith("ates") or tok.endswith("izes") or tok.endswith("ifies") or tok in (
            "shows", "indicates", "demonstrates", "presents", "increases", "decreases",
            "occurs", "consists", "leads", "causes", "means", "appears", "remains",
            "becomes", "reaches", "corresponds", "relates", "depends", "plays",
            "contains", "includes", "requires", "provides", "allows", "makes",
            "gives", "follows", "yields", "conforms", "deviates", "fluctuates",
            "correlates", "aggravates", "determines", "influences", "affects",
        )):
            if prev not in ("the", "a", "an", "these", "those", "two", "three", "many", "several", "different", "various"):
                c["present"] += 1
    return c


def detect_initial_connective(sent: str) -> str | None:
    s = sent.lstrip()
    for conn in CONNECTIVES:
        c = conn.strip()
        m = re.match(rf"^{re.escape(c)}(?:\s*,|\s+that\b|\s+in\b|\s+the\b|\s+it\b|\s+we\b)", s, re.I)
        if m:
            # Normalize casing
            return c[0].upper() + c[1:].lower()
    if re.match(r"^As\s+(?:shown|seen|can\s+be\s+seen|illustrated|depicted)\s+in\b", s, re.I):
        return "As shown/seen in [FIG]"
    if re.match(r"^In\s+this\s+(?:paper|study|work)\s*,", s, re.I):
        return "In this paper/study"
    return None


def analyze_subset(paras: list[dict[str, Any]], use_weights: bool = True) -> dict[str, Any]:
    """Compute per-section and overall metrics for a subset of paragraphs."""
    by_sec: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in paras:
        by_sec[p["section"]].append(p)
        by_sec["overall"].append(p)

    results: dict[str, Any] = {}
    for sec in CANONICAL_SECTIONS + ["overall"]:
        sec_paras = by_sec.get(sec, [])
        if not sec_paras:
            continue

        sent_len_vw: list[tuple[float, float]] = []
        para_words_vw: list[tuple[float, float]] = []
        para_sents_vw: list[tuple[float, float]] = []

        total_w_sents = 0.0
        passive_w_sents = 0.0
        passive_hits_w = 0.0
        total_w_words = 0.0
        we_w = 0.0
        our_w = 0.0
        we_our_sents_w = 0.0
        it_passive_w = 0.0
        it_passive_verbs: Counter[str] = Counter()
        there_be_w = 0.0

        tense_counts: Counter[str] = Counter()
        sent_conn_counts: Counter[str] = Counter()
        para_conn_counts: Counter[str] = Counter()
        verb_counts: Counter[str] = Counter()
        adverb_counts: Counter[str] = Counter()
        adverb_pos_counts: dict[str, Counter[str]] = defaultdict(Counter)

        hedge_w = 0.0
        booster_w = 0.0
        punct_counts: Counter[str] = Counter()
        sig_counts: Counter[str] = Counter()

        for p in sec_paras:
            w = float(p["effective_weight"]) if use_weights else 1.0
            txt = p["text"]
            sents = split_sentences(txt)
            if not sents:
                continue

            p_words = tokenize_words(txt)
            n_p_words = len(p_words)
            para_words_vw.append((float(n_p_words), w))
            para_sents_vw.append((float(len(sents)), w))
            total_w_words += n_p_words * w

            # Paragraph-initial connective
            p_conn = detect_initial_connective(sents[0])
            if p_conn:
                para_conn_counts[p_conn] += w

            # Punctuation counts (excluding placeholders)
            clean_txt = PLACEHOLDER_RE.sub(" ", txt)
            punct_counts["semicolon"] += clean_txt.count(";") * w
            punct_counts["parenthesis"] += clean_txt.count("(") * w
            punct_counts["dash"] += (clean_txt.count("—") + clean_txt.count("–")) * w
            punct_counts["colon"] += clean_txt.count(":") * w
            punct_counts["slash"] += len(re.findall(r"(?<=\w)/(?=\w)", clean_txt)) * w

            # Signature constructions
            for name, pat in SIGNATURE_CONSTRUCTIONS.items():
                hits = len(pat.findall(clean_txt))
                if hits:
                    sig_counts[name] += hits * w

            # Reporting verbs
            for lem, pat in VERB_PATTERNS.items():
                hits = len(pat.findall(clean_txt))
                if hits:
                    verb_counts[lem] += hits * w

            # Word-level counts (we, our, hedging, boosters)
            alpha_tokens = [t.lower() for t in ALPHA_WORD_RE.findall(clean_txt)]
            for tok in alpha_tokens:
                if tok == "we" or tok == "us":
                    we_w += w
                elif tok == "our" or tok == "ours":
                    our_w += w
                if tok in HEDGING_WORDS:
                    hedge_w += w
                if tok in BOOSTER_WORDS:
                    booster_w += w

            # Sentence-level analysis
            for s in sents:
                s_words = tokenize_words(s)
                if not s_words:
                    continue
                sent_len_vw.append((float(len(s_words)), w))
                total_w_sents += w

                p_hits = len(PASSIVE_RE.findall(s))
                if p_hits:
                    passive_w_sents += w
                    passive_hits_w += p_hits * w

                if re.search(r"\b(?:we|our|us)\b", s, re.I):
                    we_our_sents_w += w

                for m_it in IT_PASSIVE_RE.finditer(s):
                    it_passive_w += w
                    it_passive_verbs[m_it.group(1).lower()] += w

                if re.search(r"\bThere\s+(?:is|are|was|were|has\s+been|have\s+been|exist|exists)\b", s, re.I):
                    there_be_w += w

                # Tenses
                tc = analyze_sentence_tenses(s)
                for k, v in tc.items():
                    tense_counts[k] += v * w

                # Sentence-initial connective
                s_conn = detect_initial_connective(s)
                if s_conn:
                    sent_conn_counts[s_conn] += w

                # Adverbs ending in -ly (excluding non-adverbs like "only", "early", "supply", "family", "likely", "assembly", "anomaly")
                s_clean = PLACEHOLDER_RE.sub(" ", s)
                s_alpha = ALPHA_WORD_RE.findall(s_clean)
                n_sa = len(s_alpha)
                for idx_tok, tok in enumerate(s_alpha):
                    low_tok = tok.lower()
                    if (
                        low_tok.endswith("ly")
                        and len(low_tok) >= 6
                        and low_tok not in ("only", "early", "supply", "family", "likely", "unlikely", "assembly", "anomaly", "butterfly", "multiply", "apply")
                    ):
                        adverb_counts[low_tok] += w
                        if idx_tok <= 1:
                            pos = "initial"
                        elif idx_tok >= n_sa - 2:
                            pos = "sentence_final"
                        else:
                            # Also check if followed immediately by punctuation or "by/in/with/for/to" adjunct after a verb
                            next_tok = s_alpha[idx_tok + 1].lower() if (idx_tok + 1) < n_sa else ""
                            if next_tok in ("by", "in", "with", "for", "to", "from", "at", "under", "during", "when", "while", "and"):
                                pos = "post_verbal_before_adjunct"
                            else:
                                pos = "medial"
                        adverb_pos_counts[low_tok][pos] += w

        sent_mean, sent_std = weighted_mean_std(sent_len_vw)
        pw_mean, pw_std = weighted_mean_std(para_words_vw)
        ps_mean, ps_std = weighted_mean_std(para_sents_vw)

        total_tense = sum(tense_counts[k] for k in ("present", "past", "present_perfect")) or 1.0
        denom_1k = max(total_w_words / 1000.0, 1e-6)
        denom_100w = max(total_w_words / 100.0, 1e-6)
        denom_sents = max(total_w_sents, 1e-6)

        top_adverbs = {}
        for adv, cnt in adverb_counts.most_common(20):
            pos_c = adverb_pos_counts[adv]
            tot_a = sum(pos_c.values()) or 1.0
            top_adverbs[adv] = {
                "per_1000w": round(cnt / denom_1k, 2),
                "raw_weighted": round(cnt, 2),
                "initial_ratio": round(pos_c["initial"] / tot_a, 2),
                "medial_ratio": round(pos_c["medial"] / tot_a, 2),
                "post_verbal_or_final_ratio": round((pos_c["sentence_final"] + pos_c["post_verbal_before_adjunct"]) / tot_a, 2),
                "strict_sentence_final_ratio": round(pos_c["sentence_final"] / tot_a, 2),
            }

        results[sec] = {
            "n_paragraphs": len(sec_paras),
            "n_sentences_unweighted": len(sent_len_vw),
            "weighted_words": round(total_w_words, 1),
            "sentence_length": {
                "mean": sent_mean,
                "std": sent_std,
                "p10": weighted_quantile(sent_len_vw, 0.10),
                "p25": weighted_quantile(sent_len_vw, 0.25),
                "p50": weighted_quantile(sent_len_vw, 0.50),
                "p75": weighted_quantile(sent_len_vw, 0.75),
                "p90": weighted_quantile(sent_len_vw, 0.90),
            },
            "paragraph_length_words": {
                "mean": pw_mean,
                "std": pw_std,
                "p25": weighted_quantile(para_words_vw, 0.25),
                "p50": weighted_quantile(para_words_vw, 0.50),
                "p75": weighted_quantile(para_words_vw, 0.75),
                "p90": weighted_quantile(para_words_vw, 0.90),
            },
            "paragraph_length_sentences": {
                "mean": ps_mean,
                "std": ps_std,
                "p25": weighted_quantile(para_sents_vw, 0.25),
                "p50": weighted_quantile(para_sents_vw, 0.50),
                "p75": weighted_quantile(para_sents_vw, 0.75),
                "p90": weighted_quantile(para_sents_vw, 0.90),
            },
            "voice_and_agency": {
                "passive_sent_ratio": round(passive_w_sents / denom_sents, 3),
                "passive_per_100w": round(passive_hits_w / denom_100w, 2),
                "we_per_1000w": round(we_w / denom_1k, 2),
                "our_per_1000w": round(our_w / denom_1k, 2),
                "we_or_our_per_1000w": round((we_w + our_w) / denom_1k, 2),
                "we_or_our_sent_ratio": round(we_our_sents_w / denom_sents, 3),
                "it_is_vbn_that_per_1000w": round(it_passive_w / denom_1k, 2),
                "it_is_vbn_that_per_100_sents": round(it_passive_w / denom_sents * 100.0, 2),
                "it_is_vbn_breakdown": {k: round(v, 1) for k, v in it_passive_verbs.most_common(12)},
                "there_be_per_1000w": round(there_be_w / denom_1k, 2),
            },
            "tense_distribution": {
                "present_ratio": round(tense_counts["present"] / total_tense, 3),
                "past_ratio": round(tense_counts["past"] / total_tense, 3),
                "present_perfect_ratio": round(tense_counts["present_perfect"] / total_tense, 3),
                "modal_per_100_sents": round(tense_counts["modal"] / denom_sents * 100.0, 2),
            },
            "sentence_initial_connectives_per_100_sents": {
                k: round(v / denom_sents * 100.0, 2)
                for k, v in sent_conn_counts.most_common(18)
            },
            "paragraph_initial_connectives_per_100_paras": {
                k: round(v / max(sum(float(p["effective_weight"]) if use_weights else 1.0 for p in sec_paras), 1e-6) * 100.0, 2)
                for k, v in para_conn_counts.most_common(12)
            },
            "reporting_verbs_per_1000w": {
                k: round(v / denom_1k, 2)
                for k, v in verb_counts.most_common(20)
            },
            "top_adverbs": top_adverbs,
            "hedging_and_boosters": {
                "hedging_per_1000w": round(hedge_w / denom_1k, 2),
                "boosters_per_1000w": round(booster_w / denom_1k, 2),
                "booster_to_hedge_ratio": round(booster_w / max(hedge_w, 1e-6), 2),
            },
            "punctuation_per_1000w": {
                k: round(v / denom_1k, 2) for k, v in punct_counts.items()
            },
            "signature_constructions_per_1000w": {
                k: round(v / denom_1k, 2) for k, v in sig_counts.most_common()
            },
        }
    return results


def analyze_formatting_and_spelling(paras: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze US vs UK spelling, number+unit formatting, and abbreviation definitions."""
    us_counts: Counter[str] = Counter()
    uk_counts: Counter[str] = Counter()
    uk_by_paper: Counter[str] = Counter()

    slash_series_examples: list[str] = []
    tilde_range_examples: list[str] = []
    endash_range_examples: list[str] = []
    spaced_unit_count = 0
    unspaced_unit_count = 0
    abbr_full_first: list[str] = []
    abbr_short_first: list[str] = []

    for p in paras:
        txt = p["text"]
        pid = p["paper_id"]
        low = txt.lower()
        for us_w, uk_w in US_UK_PAIRS:
            n_us = len(re.findall(rf"\b{us_w}\b", low))
            n_uk = len(re.findall(rf"\b{uk_w}\b", low))
            if n_us:
                us_counts[f"{us_w}/{uk_w}"] += n_us
            if n_uk:
                uk_counts[f"{us_w}/{uk_w}"] += n_uk
                uk_by_paper[pid] += n_uk

        # Slash-separated parameter sets: "0.2/0.5/1 A", "5/15/25 V"
        for m in re.finditer(r"\b\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)+(?:[\s\-]*(?:mV|V|mA|A|Hz|kHz|nm/s|μm|µm|mm|N|mN))?\b", txt):
            if len(slash_series_examples) < 15 and m.group(0) not in slash_series_examples:
                slash_series_examples.append(m.group(0))

        # Tilde ranges: "25∼150 nm/s", "21~25%"
        for m in re.finditer(r"\b\d+(?:\.\d+)?\s*[∼~]\s*\d+(?:\.\d+)?(?:\s*(?:nm/s|μm/s|µm/s|mm/s|Hz|kHz|%|V|A|μm|µm|mm|ms))?", txt):
            if len(tilde_range_examples) < 15 and m.group(0) not in tilde_range_examples:
                tilde_range_examples.append(m.group(0))

        # En-dash ranges: "10–3000 Hz", "25–125 °C"
        for m in re.finditer(r"\b\d+(?:\.\d+)?\s*–\s*\d+(?:\.\d+)?\s*(?:Hz|kHz|°C|μm|µm|mm|nm/s|mA|A|V|N|%)", txt):
            if len(endash_range_examples) < 15 and m.group(0) not in endash_range_examples:
                endash_range_examples.append(m.group(0))

        # Space vs no-space before common electrical/mechanical units
        spaced_unit_count += len(re.findall(r"\b\d+(?:\.\d+)?\s+(?:mV|V|mA|A|mΩ|Ω|Hz|kHz|MHz|ms|μs|µs|ns|mm|μm|µm|nm|mN|N|mJ|J|°C)\b", txt))
        unspaced_unit_count += len(re.findall(r"\b\d+(?:\.\d+)?(?:mV|V|mA|A|mΩ|Ω|Hz|kHz|MHz|ms|μs|µs|ns|mm|μm|µm|nm|mN|N|mJ|J|°C)\b", txt))

        # Abbreviation definitions: "full name (ABBR)" vs "ABBR (full name)"
        for m in re.finditer(r"\b([A-Za-z][A-Za-z\-]+(?:\s+[A-Za-z][A-Za-z\-]+){1,4})\s*\(([A-Z]{2,6})\)", txt):
            item = f"{m.group(1)} ({m.group(2)})"
            if len(abbr_full_first) < 20 and item not in abbr_full_first:
                abbr_full_first.append(item)
        for m in re.finditer(r"\b([A-Z]{2,5}(?:&[A-Z])?)\s*\(([a-z][a-z\s&\-]{4,35})\)", txt):
            item = f"{m.group(1)} ({m.group(2)})"
            if len(abbr_short_first) < 10 and item not in abbr_short_first:
                abbr_short_first.append(item)

    return {
        "spelling": {
            "us_total": sum(us_counts.values()),
            "uk_total": sum(uk_counts.values()),
            "us_by_pair": dict(us_counts.most_common()),
            "uk_by_pair": dict(uk_counts.most_common()),
            "uk_by_paper": dict(uk_by_paper.most_common()),
        },
        "number_unit_formatting": {
            "spaced_number_unit_count": spaced_unit_count,
            "unspaced_number_unit_count": unspaced_unit_count,
            "spaced_ratio": round(spaced_unit_count / max(spaced_unit_count + unspaced_unit_count, 1), 3),
            "slash_series_examples": slash_series_examples,
            "tilde_range_examples": tilde_range_examples,
            "endash_range_examples": endash_range_examples,
        },
        "abbreviation_definitions": {
            "full_first_examples": abbr_full_first,
            "abbr_first_examples": abbr_short_first,
        },
    }


def build_lint_thresholds(train_stats: dict[str, Any]) -> dict[str, Any]:
    """Recommend section-level lint thresholds calibrated to the train S+A distribution."""
    thresholds: dict[str, Any] = {}
    for sec in CANONICAL_SECTIONS:
        if sec not in train_stats:
            continue
        s = train_stats[sec]
        sl = s["sentence_length"]
        pv = s["voice_and_agency"]["passive_sent_ratio"]
        thresholds[sec] = {
            "sent_len_p50": [round(max(12.0, sl["p25"] - 2.0), 1), round(sl["p75"] + 3.0, 1)],
            "sent_len_p90": [round(max(20.0, sl["p50"] + 2.0), 1), round(sl["p90"] + 8.0, 1)],
            "passive_ratio": [round(max(0.10, pv - 0.22), 2), round(min(0.85, pv + 0.22), 2)],
        }
    return thresholds


def render_markdown_report(stats: dict[str, Any]) -> str:
    train = stats["subsets"]["train_SA_weighted"]
    tier_s = stats["subsets"]["tier_S_only"]
    tier_a = stats["subsets"]["tier_A_train"]
    tier_b = stats["subsets"]["secondary_B"]
    early = stats["subsets"]["early_le_2015"]
    late = stats["subsets"]["late_ge_2017"]
    fmt = stats["formatting_and_spelling_train_SA"]

    lines: list[str] = [
        "# Phase 2.1 — Quantitative Stylometry Report (`stats_report.md`)",
        "",
        "> **Primary Profile Corpus**: S + A tiers (`split == 'train'`, 16 papers, weighted by `effective_weight`: S=3.0, A=1.0, near-duplicate pairs P06/P07 & P08/P10=0.5).",
        "",
        "---",
        "",
        "## 1. Per-Section Sentence & Paragraph Length (S+A Train, Weighted)",
        "",
        "| Section | Paras | Sents | Words (W) | Sent Mean ± SD | Sent P25 / P50 / P75 / P90 | Para Words P50 (P25–P75) | Para Sents P50 (P25–P75) |",
        "|---|---:|---:|---:|---:|---|---:|---:|",
    ]
    for sec in CANONICAL_SECTIONS + ["overall"]:
        if sec not in train:
            continue
        d = train[sec]
        sl = d["sentence_length"]
        pw = d["paragraph_length_words"]
        ps = d["paragraph_length_sentences"]
        label = f"**{sec}**" if sec == "overall" else f"`{sec}`"
        lines.append(
            f"| {label} | {d['n_paragraphs']} | {d['n_sentences_unweighted']} | {d['weighted_words']:.0f} "
            f"| {sl['mean']:.1f} ± {sl['std']:.1f} | {sl['p25']:.0f} / **{sl['p50']:.0f}** / {sl['p75']:.0f} / {sl['p90']:.0f} "
            f"| {pw['p50']:.0f} ({pw['p25']:.0f}–{pw['p75']:.0f}) | {ps['p50']:.0f} ({ps['p25']:.0f}–{ps['p75']:.0f}) |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 2. Voice, Agency & Tense Distribution by Section (S+A Train, Weighted)",
        "",
        "| Section | Passive Sent Ratio | Passive / 100w | `we` / 1kw | `our` / 1kw | `It is VBN that` / 100 sents | `There be` / 1kw | Present % | Past % | Pres. Perf % | Modal / 100 sents |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for sec in CANONICAL_SECTIONS + ["overall"]:
        if sec not in train:
            continue
        d = train[sec]
        va = d["voice_and_agency"]
        td = d["tense_distribution"]
        label = f"**{sec}**" if sec == "overall" else f"`{sec}`"
        lines.append(
            f"| {label} | **{va['passive_sent_ratio']*100:.1f}%** | {va['passive_per_100w']:.2f} "
            f"| {va['we_per_1000w']:.2f} | {va['our_per_1000w']:.2f} | {va['it_is_vbn_that_per_100_sents']:.2f} "
            f"| {va['there_be_per_1000w']:.2f} | {td['present_ratio']*100:.1f}% | {td['past_ratio']*100:.1f}% "
            f"| {td['present_perfect_ratio']*100:.1f}% | {td['modal_per_100_sents']:.1f} |"
        )

    lines.extend([
        "",
        "### Formal-Subject `It is <VBN> that` Top Verbs (S+A Train Overall)",
        "",
    ])
    it_bd = train["overall"]["voice_and_agency"]["it_is_vbn_breakdown"]
    lines.append("- " + ", ".join(f"`{k}` ({v})" for k, v in it_bd.items()))

    lines.extend([
        "",
        "---",
        "",
        "## 3. Sentence-Initial & Paragraph-Initial Connectives by Section (S+A Train)",
        "",
        "| Section | Top Sentence-Initial Connectives (rate per 100 sentences) | Top Paragraph-Initial Openers (rate per 100 paragraphs) |",
        "|---|---|---|",
    ])
    for sec in CANONICAL_SECTIONS + ["overall"]:
        if sec not in train:
            continue
        d = train[sec]
        sc = ", ".join(f"`{k}` ({v:.2f})" for k, v in list(d["sentence_initial_connectives_per_100_sents"].items())[:8])
        pc = ", ".join(f"`{k}` ({v:.1f})" for k, v in list(d["paragraph_initial_connectives_per_100_paras"].items())[:6])
        label = f"**{sec}**" if sec == "overall" else f"`{sec}`"
        lines.append(f"| {label} | {sc or '—'} | {pc or '—'} |")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Reporting Verbs Ranking by Section (per 1,000 words, S+A Train)",
        "",
        "| Section | Top 12 Reporting / Research Verbs (lemma: per 1,000 words) |",
        "|---|---|",
    ])
    for sec in CANONICAL_SECTIONS + ["overall"]:
        if sec not in train:
            continue
        d = train[sec]
        rv = ", ".join(f"`{k}` ({v:.2f})" for k, v in list(d["reporting_verbs_per_1000w"].items())[:12])
        label = f"**{sec}**" if sec == "overall" else f"`{sec}`"
        lines.append(f"| {label} | {rv} |")

    lines.extend([
        "",
        "---",
        "",
        "## 5. Signature Adverbs & Sentence Position Analysis (S+A Train Overall)",
        "",
        "> Sanity check (`docs/design_notes.md` §6 Phase 2): **`explicitly`** ranks at the top of signature manner adverbs, predominantly in **post-verbal / clause-final** position (e.g. `are recorded explicitly`, `are addressed explicitly`, `increases explicitly`).",
        "",
        "| Adverb | Rate / 1,000w | Weighted Count | Initial % | Medial % | Post-Verbal / Clause-Final % | Strict Sentence-End % |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for adv, info in train["overall"]["top_adverbs"].items():
        lines.append(
            f"| `{adv}` | **{info['per_1000w']:.2f}** | {info['raw_weighted']:.1f} "
            f"| {info['initial_ratio']*100:.0f}% | {info['medial_ratio']*100:.0f}% "
            f"| **{info['post_verbal_or_final_ratio']*100:.0f}%** | {info['strict_sentence_final_ratio']*100:.0f}% |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 6. Signature Constructions, Hedging/Boosters & Punctuation (per 1,000 words)",
        "",
        "| Metric / Construction | S Tier (P01,03,13) | A Tier (Train) | S+A Train (Weighted) | B Tier (Students) | Early (<=2015) | Late (>=2017) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])

    def _get_ov(sub: dict[str, Any], path: list[str], default: float = 0.0) -> float:
        cur: Any = sub.get("overall", {})
        for k in path:
            cur = cur.get(k, {}) if isinstance(cur, dict) else default
        return float(cur) if isinstance(cur, (int, float)) else default

    comp_rows = [
        ("Sentence Length P50 (words)", ["sentence_length", "p50"]),
        ("Sentence Length P90 (words)", ["sentence_length", "p90"]),
        ("Paragraph Length P50 (words)", ["paragraph_length_words", "p50"]),
        ("Passive Voice Sent Ratio", ["voice_and_agency", "passive_sent_ratio"]),
        ("`we` / 1,000w", ["voice_and_agency", "we_per_1000w"]),
        ("`our` / 1,000w", ["voice_and_agency", "our_per_1000w"]),
        ("`It is VBN that` / 100 sents", ["voice_and_agency", "it_is_vbn_that_per_100_sents"]),
        ("`There be` / 1,000w", ["voice_and_agency", "there_be_per_1000w"]),
        ("Present Tense Ratio", ["tense_distribution", "present_ratio"]),
        ("Past Tense Ratio", ["tense_distribution", "past_ratio"]),
        ("Hedging / 1,000w", ["hedging_and_boosters", "hedging_per_1000w"]),
        ("Boosters / 1,000w", ["hedging_and_boosters", "boosters_per_1000w"]),
        ("Semicolons `;` / 1,000w", ["punctuation_per_1000w", "semicolon"]),
        ("Parentheses `(` / 1,000w", ["punctuation_per_1000w", "parenthesis"]),
        ("Dashes `—/–` / 1,000w", ["punctuation_per_1000w", "dash"]),
        ("Sig: `explicitly` / 1,000w", ["signature_constructions_per_1000w", "explicitly"]),
        ("Sig: `<verb> explicitly` / 1,000w", ["signature_constructions_per_1000w", "<verb>_explicitly"]),
        ("Sig: `correlates closely with` / 1,000w", ["signature_constructions_per_1000w", "correlates_closely_with"]),
        ("Sig: `closely/greatly dependent on` / 1,000w", ["signature_constructions_per_1000w", "closely_dependent_on"]),
        ("Sig: `our (newly) designed test rig` / 1,000w", ["signature_constructions_per_1000w", "our_designed_rig_switch"]),
        ("Sig: `as a function of` / 1,000w", ["signature_constructions_per_1000w", "as_a_function_of"]),
        ("Sig: `is attributed to` / 1,000w", ["signature_constructions_per_1000w", "is_attributed_to"]),
        ("Sig: `Also,` sentence-initial / 1,000w", ["signature_constructions_per_1000w", "also_sentence_initial"]),
        ("Non-native: `are resulted from` / 1,000w", ["signature_constructions_per_1000w", "are_resulted_from"]),
    ]
    for label, path in comp_rows:
        vals = [_get_ov(s, path) for s in (tier_s, tier_a, train, tier_b, early, late)]
        lines.append(f"| {label} | {vals[0]:.2f} | {vals[1]:.2f} | **{vals[2]:.2f}** | {vals[3]:.2f} | {vals[4]:.2f} | {vals[5]:.2f} |")

    lines.extend([
        "",
        "---",
        "",
        "## 7. Spelling, Number/Unit Formatting & Abbreviation Conventions (S+A Train)",
        "",
        f"- **US vs UK Spelling**: US total = **{fmt['spelling']['us_total']}**, UK total = **{fmt['spelling']['uk_total']}** (98%+ American English across S+A train; British spelling appears almost exclusively in Maney journal P05 in heldout).",
        f"  - US/UK pairs breakdown: `{json.dumps(fmt['spelling']['us_by_pair'])}` vs UK `{json.dumps(fmt['spelling']['uk_by_pair'])}`",
        f"- **Number + Unit Spacing**: Spaced (`10 mA`, `25 °C`, `50 μm`) = **{fmt['number_unit_formatting']['spaced_number_unit_count']}** ({fmt['number_unit_formatting']['spaced_ratio']*100:.1f}%) vs Unspaced (`10mA`, `50mV`, mostly in late IEEE camera-ready/manuscript files P22, P23, P26, P30) = **{fmt['number_unit_formatting']['unspaced_number_unit_count']}**.",
        f"- **Slash-Separated Multi-Condition Notation**: {', '.join(f'`{x}`' for x in fmt['number_unit_formatting']['slash_series_examples'][:10])}",
        f"- **Tilde (`∼`/`~`) & En-Dash (`–`) Ranges**:",
        f"  - Tilde ranges: {', '.join(f'`{x}`' for x in fmt['number_unit_formatting']['tilde_range_examples'][:8])}",
        f"  - En-dash ranges: {', '.join(f'`{x}`' for x in fmt['number_unit_formatting']['endash_range_examples'][:8])}",
        f"- **Abbreviation First-Definition Examples**:",
        f"  - Standard `Full Name (ABBR)`: {', '.join(f'`{x}`' for x in fmt['abbreviation_definitions']['full_first_examples'][:10])}",
        f"  - Short-first `ABBR (full name)`: {', '.join(f'`{x}`' for x in fmt['abbreviation_definitions']['abbr_first_examples'][:6]) or 'None in S+A train (appears in P23)'}",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    cfg = load_config()
    proc_dir = data_dir(cfg) / "processed"
    paras_path = proc_dir / "paragraphs.jsonl"
    if not paras_path.exists():
        print(f"[error] {paras_path} not found. Run 02_clean_segment.py first.", file=sys.stderr)
        return 1

    papers_by_id = {p.id: p for p in resolve_papers(cfg)}
    all_paras = [json.loads(line) for line in open(paras_path, encoding="utf-8")]
    for p in all_paras:
        paper_meta = papers_by_id[p["paper_id"]].meta
        p["year"] = paper_meta.get("year") or 2020

    train_sa = [p for p in all_paras if p["tier"] in ("S", "A") and p["split"] == "train"]
    tier_s = [p for p in all_paras if p["tier"] == "S"]
    tier_a_train = [p for p in all_paras if p["tier"] == "A" and p["split"] == "train"]
    secondary_b = [p for p in all_paras if p["split"] == "secondary"]
    early_sa = [p for p in train_sa if p["year"] <= 2015]
    late_sa = [p for p in train_sa if p["year"] >= 2017]

    train_stats = analyze_subset(train_sa, use_weights=True)
    stats_payload = {
        "meta": {
            "total_paragraphs": len(all_paras),
            "train_sa_paragraphs": len(train_sa),
            "tier_s_paragraphs": len(tier_s),
            "tier_a_train_paragraphs": len(tier_a_train),
            "secondary_b_paragraphs": len(secondary_b),
            "early_le_2015_paragraphs": len(early_sa),
            "late_ge_2017_paragraphs": len(late_sa),
        },
        "subsets": {
            "train_SA_weighted": train_stats,
            "tier_S_only": analyze_subset(tier_s, use_weights=False),
            "tier_A_train": analyze_subset(tier_a_train, use_weights=True),
            "secondary_B": analyze_subset(secondary_b, use_weights=False),
            "early_le_2015": analyze_subset(early_sa, use_weights=True),
            "late_ge_2017": analyze_subset(late_sa, use_weights=True),
        },
        "formatting_and_spelling_train_SA": analyze_formatting_and_spelling(train_sa),
        "recommended_lint_thresholds": build_lint_thresholds(train_stats),
    }

    out_json = proc_dir / "stats.json"
    out_md = proc_dir / "stats_report.md"
    out_json.write_text(json.dumps(stats_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(render_markdown_report(stats_payload), encoding="utf-8")

    ov = train_stats["overall"]
    exp_info = ov["top_adverbs"].get("explicitly", {})
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    print(
        f"Train S+A overall: paras={ov['n_paragraphs']}, sents={ov['n_sentences_unweighted']}, "
        f"sent_p50={ov['sentence_length']['p50']}, passive_ratio={ov['voice_and_agency']['passive_sent_ratio']:.3f}, "
        f"explicitly_per_1000w={exp_info.get('per_1000w', 0.0)} "
        f"(post-verbal/final={exp_info.get('post_verbal_or_final_ratio', 0.0)*100:.0f}%)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

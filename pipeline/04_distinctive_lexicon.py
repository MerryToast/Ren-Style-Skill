"""Phase 2.2 — Distinctive lexicon via weighted log-odds (informative Dirichlet prior).

Implements Monroe, Colaresi & Quinn (2008) z-scored log-odds ratio with an
informative Dirichlet prior for three comparisons (docs/design_notes.md §6 Phase 2):
  1. Ren (S+A, train)  vs  AI baseline (data/baseline/ai_rewrites.jsonl)  -> "anti-AI-tone" table
  2. Ren (S+A, train)  vs  tier B (students first-author, secondary)      -> Ren-specific traits
  3. Tier S (core 3)   vs  Tier A (train)                                 -> S-tier anchor traits

Features:
  - Extracts lemmatized unigrams, surface unigrams, bigrams, and trigrams with
    placeholders ([EQ], [CIT], [FIG n], [TAB n]) removed.
  - Separates pure rhetorical/stylistic n-grams (excluding physical/domain nouns
    like "fretting", "contact", "resistance", "welding", "arc", "gold") from
    domain+style n-grams so that academic framing, verbs, adverbs, and transitions
    emerge cleanly without topic confounding.
  - Verifies a comprehensive list of common LLM/AI words against all 20 Ren
    first-author papers (S + A_train + A_heldout) and 10 Tier B papers.

Outputs:
  - ``data/processed/lexicon.json``
  - ``data/processed/lexicon_report.md``

Usage:
    python pipeline/04_distinctive_lexicon.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from common import data_dir, load_config

PLACEHOLDER_RE = re.compile(r"\[(?:CIT|EQ|FIG\s*\d+|TAB\s*\d+)\]")
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z\-']*[a-zA-Z]|[A-Za-z]{2,}")

# Pure grammar/function words excluded from unigram content rankings (but KEPT in bigrams/trigrams!)
UNIGRAM_STOPWORDS = {
    "the", "of", "and", "in", "to", "is", "are", "was", "were", "be", "been", "being",
    "for", "with", "on", "at", "by", "from", "as", "that", "this", "these", "those",
    "it", "its", "an", "or", "into", "than", "then", "when", "where", "which",
    "who", "whom", "whose", "while", "during", "after", "before", "between", "through",
    "under", "over", "above", "below", "up", "down", "out", "off", "about", "around",
    "can", "could", "will", "would", "may", "might", "shall", "should", "must", "have",
    "has", "had", "do", "does", "did", "not", "no", "nor", "only", "same", "other",
    "another", "each", "every", "all", "both", "some", "any", "such", "more", "most",
    "less", "least", "very", "much", "many", "few", "several", "one", "two", "three",
    "four", "five", "six", "seven", "eight", "nine", "ten", "fig", "table", "eq", "eqs",
    "section", "ii", "iii", "iv",
}

# Comprehensive physical/domain nouns & technical adjectives excluded in the pure-rhetorical view
DOMAIN_TOPIC_WORDS = {
    "contact", "contacts", "resistance", "resistances", "fretting", "fretted", "fret",
    "wear", "worn", "corrosion", "corrosive", "current", "currents", "voltage", "voltages",
    "force", "forces", "load", "loads", "loading", "unloading", "amplitude", "amplitudes",
    "frequency", "frequencies", "cycle", "cycles", "cycling", "temperature", "temperatures",
    "time", "times", "duration", "durations", "speed", "speeds", "velocity", "velocities",
    "radius", "radii", "diameter", "thickness", "length", "width", "height", "depth",
    "size", "sizes", "distance", "gap", "area", "areas", "volume", "volumes", "mass",
    "surface", "surfaces", "zone", "zones", "region", "regions", "site", "sites",
    "spot", "spots", "a-spot", "a-spots", "patch", "patches", "asperity", "asperities",
    "asperity-peak", "asperity-peaks", "summit", "summits", "sphere", "spheres", "spherical",
    "hemisphere", "hemispherical", "cylinder", "cylindrical", "planar", "plane", "flat",
    "cambered", "rough", "roughness", "smooth", "topography", "morphology", "morphologies",
    "micro-topography", "microtopography", "profile", "profiles", "contour",
    "gold", "gold-plated", "gold-coated", "au", "au-plated", "silver", "ag", "copper", "cu",
    "tin", "tin-plated", "sn", "nickel", "ni", "cobalt", "palladium", "oxide", "oxides",
    "oxidation", "oxidized", "agsno2", "agsno", "agni", "agcdo", "agzno", "agmgni",
    "beryllium", "bronze", "brass", "metal", "metals", "metallic", "alloy", "alloys",
    "material", "materials", "coating", "coatings", "plated", "plating", "coated",
    "substrate", "substrates", "bulk", "film", "films", "layer", "layers", "insulator",
    "insulation", "debris", "particle", "particles", "nanoparticles", "scar", "scars",
    "track", "tracks", "pit", "pits", "pip", "crack", "cracks", "splash", "splashes",
    "splashing", "delamination", "ablation", "carbon", "carbonization",
    "bridge", "bridges", "sub-bridges", "molten", "melt", "melting", "melted", "meltdown",
    "pool", "solid", "liquid", "solid-liquid", "solidification", "soften", "softening",
    "weld", "welds", "welding", "welded", "nugget", "strength", "tensile", "breakaway",
    "bounce", "bounces", "bouncing", "rebound", "impact", "arc", "arcs", "arcing",
    "restrike", "re-striked", "ignition", "ignite", "ignites", "ignited", "extinguish",
    "anode", "cathode", "cathodic", "erosion", "eroded", "transfer",
    "adhesion", "adhesive", "stiction", "stick", "sticking", "repulsion", "lorentz",
    "lorenz", "kohlrausch", "holm", "sharvin", "hertz", "hertzian", "greenwood",
    "williamson", "timsit", "braunovic", "burton", "utsumi", "malucci", "skinner",
    "rieder", "neuhaus", "morin", "jemaa", "carvou", "fouvry", "schoepf", "slade",
    "friction", "frictional", "tangential", "normal", "axial", "vertical", "horizontal",
    "radial", "lateral", "mechanical", "electrical", "electrically", "thermal", "thermally",
    "electro-thermal", "thermal-mechanical", "thermo-mechanical", "electromechanical",
    "microelectromechanical", "electromagnetic", "electrostatic", "piezoelectric", "piezo",
    "elastic", "plastic", "elasto-plastic", "hardness", "modulus", "stress", "shearing",
    "strain", "deformation", "deflection", "bending", "displacement", "vibration",
    "vibrational", "oscillation", "oscillatory", "sinusoidal", "sine", "sweep", "sweeping",
    "acceleration", "sliding", "slip", "slipping", "gross", "stick-slip", "rolling",
    "wiping", "overtravel", "over-travel", "stroke", "insertion", "extraction", "withdrawal",
    "making", "breaking", "make", "break", "opening", "closing", "open", "closed",
    "switching", "switch", "switches", "Switch", "relay", "relays", "connector",
    "connectors", "interconnection", "interconnections", "contactors", "breaker", "breakers",
    "indenter", "indenters", "rivet", "rivets", "spring", "springs", "leaf", "rod", "rods",
    "blade", "blades", "receptacle", "receptacles", "pin", "socket", "rider", "coupon",
    "sample", "samples", "specimen", "specimens", "electrode", "electrodes", "conductor",
    "conductors", "interface", "interfaces", "interfacial", "circuit", "circuits",
    "capacitive", "capacitance", "capacitor", "resistive", "resistor", "inductive",
    "inductance", "inrush", "pulsed", "pulse", "dc", "ac", "vac", "vdc", "power", "supply",
    "energy", "heat", "heating", "joule", "calorific", "convection", "conduction",
    "conductive", "conductivity", "resistivity", "potential", "potentials", "isopotential",
    "isopotentials", "field", "constriction", "restriction", "spreading", "transition",
    "fem", "fe", "finite-element", "comsol", "multiphysics", "mesh", "meshes", "element",
    "elements", "sem", "edx", "eds", "x-ray", "x-rays", "daq", "labview", "sensor",
    "transducer", "shaker", "actuator", "slider", "motor", "camera", "ccd", "microscope",
    "confocal", "laser", "ultrasonic", "alcohol", "acetone", "water", "air", "ambient",
    "room", "humidity", "aerospace", "aviation", "automotive", "vehicle", "vehicles",
    "industrial", "appliance", "equipment", "device", "devices", "component", "components",
    "apparatus", "system", "systems", "structure", "structures", "configuration",
    "ecr", "tei", "sd", "edrf", "pow", "mo", "bo", "to-5", "mems", "ssr", "rms",
    "khz", "mhz", "hz", "mv", "ma", "ms", "nm", "mm", "mω", "kω", "mpa", "gpa", "mn", "mj",
}

# Candidate AI/LLM cliché words & phrases to verify against Ren's actual corpus
AI_CLICHE_CANDIDATES = [
    "delve", "delves", "delving",
    "underscore", "underscores", "underscoring",
    "garner", "garnered", "garnering",
    "pivotal",
    "intricate",
    "interplay",
    "elucidate", "elucidates", "elucidated", "elucidating",
    "notably",
    "importantly",
    "meticulously",
    "paramount",
    "ubiquitous", "ubiquitously",
    "bespoke",
    "scrutinize", "scrutinized",
    "unravel", "unraveling",
    "uncover", "uncovers", "uncovered",
    "foster", "fostering",
    "bolster", "bolstering",
    "augment", "augmenting",
    "harnessing",
    "leverage", "leveraging", "leveraged",
    "facilitating",
    "encompass", "encompasses", "encompassing",
    "holistic",
    "synergistic",
    "realm",
    "landscape",
    "testament",
    "imperative",
    "overarching",
    "multifaceted",
    "noteworthy",
    "groundbreaking",
    "cutting-edge",
    "shed light",
    "pave the way",
    "in-depth",
    "herein",
    # Words attested in Ren's corpus that generic AI lists often wrongly ban
    "explicitly",
    "meanwhile",
    "significantly",
    "furthermore",
    "subsequently",
    "moreover",
    "substantially",
    "comprehensively",
    "nevertheless",
    "consequently",
    "crucial",
    "vital",
    "essential",
    "indispensable",
    "dramatically",
    "drastically",
    "appreciably",
    "utilize", "utilized",
    "comprehensive",
    "facilitate", "facilitates",
    "harness",
    "framework",
]

IRREGULAR_LEMMAS = {
    "are": "be", "is": "be", "was": "be", "were": "be", "been": "be", "being": "be",
    "has": "have", "had": "have", "having": "have",
    "does": "do", "did": "do", "done": "do", "doing": "do",
    "shows": "show", "showed": "show", "shown": "show", "showing": "show",
    "finds": "find", "found": "find", "finding": "find",
    "leads": "lead", "led": "lead", "leading": "lead",
    "makes": "make", "made": "make", "making": "make",
    "builds": "build", "built": "build", "building": "build",
    "takes": "take", "took": "take", "taken": "take", "taking": "take",
    "gives": "give", "gave": "give", "given": "give", "giving": "give",
    "comes": "come", "came": "come", "coming": "come",
    "becomes": "become", "became": "become", "becoming": "become",
    "begins": "begin", "began": "begin", "begun": "begin", "beginning": "begin",
    "breaks": "break", "broke": "break", "broken": "break", "breaking": "break",
    "chooses": "choose", "chose": "choose", "chosen": "choose", "choosing": "choose",
    "falls": "fall", "fell": "fall", "fallen": "fall", "falling": "fall",
    "holds": "hold", "held": "hold", "holding": "hold",
    "keeps": "keep", "kept": "keep", "keeping": "keep",
    "knows": "know", "knew": "know", "known": "know", "knowing": "know",
    "leaves": "leave", "left": "leave", "leaving": "leave",
    "loses": "lose", "lost": "lose", "losing": "lose",
    "means": "mean", "meant": "mean", "meaning": "mean",
    "meets": "meet", "met": "meet", "meeting": "meet",
    "rises": "rise", "rose": "rise", "risen": "rise", "rising": "rise",
    "runs": "run", "ran": "run", "running": "run",
    "says": "say", "said": "say", "saying": "say",
    "sees": "see", "saw": "see", "seen": "see", "seeing": "see",
    "sets": "set", "setting": "set",
    "puts": "put", "putting": "put",
    "stands": "stand", "stood": "stand", "standing": "stand",
    "strikes": "strike", "struck": "strike", "striking": "strike",
    "sticks": "stick", "stuck": "stick", "sticking": "stick",
    "understands": "understand", "understood": "understand", "understanding": "understand",
    "wears": "wear", "wore": "wear", "worn": "wear", "wearing": "wear",
    "writes": "write", "wrote": "write", "written": "write", "writing": "write",
    "studies": "study", "studied": "study", "studying": "study",
    "carries": "carry", "carried": "carry", "carrying": "carry",
    "varies": "vary", "varied": "vary", "varying": "vary",
    "applies": "apply", "applied": "apply", "applying": "apply",
    "implies": "imply", "implied": "imply", "implying": "imply",
    "relies": "rely", "relied": "rely", "relying": "rely",
    "satisfies": "satisfy", "satisfied": "satisfy",
    "identifies": "identify", "identified": "identify",
    "clarifies": "clarify", "clarified": "clarify",
    "verifies": "verify", "verified": "verify",
    "modifies": "modify", "modified": "modify",
    "specifies": "specify", "specified": "specify",
    "classifies": "classify", "classified": "classify",
    "accompanies": "accompany", "accompanied": "accompany",
    "analyses": "analysis", "phenomena": "phenomenon", "criteria": "criterion",
    "radii": "radius", "formulas": "formula", "formulae": "formula",
}

DO_NOT_STEM = {
    "series", "species", "means", "always", "whereas", "besides", "towards", "status",
    "radius", "modulus", "apparatus", "campus", "focus", "gas", "glass", "mass", "loss",
    "pass", "cross", "gross", "stress", "process", "access", "success", "excess", "less",
    "unless", "needless", "regardless", "previous", "various", "obvious", "serious",
    "continuous", "simultaneous", "instantaneous", "homogeneous", "spontaneous",
    "synchronous", "numerous", "rigorous", "analogous", "monotonous", "porous", "viscous",
    "basis", "analysis", "synthesis", "hypothesis", "emphasis", "thesis", "axis", "crisis",
    "this", "thus", "plus", "minus", "bias", "atlas", "canvas", "alias",
    "bed", "red", "led", "fed", "shed", "sped", "wed", "hundred", "thousand",
    "ring", "spring", "string", "thing", "wing", "king", "bring", "sing", "cling", "swing",
    "ceiling", "feeling", "meaning", "morning", "evening", "warning", "bearing", "coating",
    "plating", "housing", "spacing", "wiping", "damping", "setting", "fitting",
}


def lemmatize_token(tok: str) -> str:
    """Deterministic lightweight lemmatizer for academic English."""
    w = tok.lower()
    if w in IRREGULAR_LEMMAS:
        return IRREGULAR_LEMMAS[w]
    if w in DO_NOT_STEM or len(w) <= 3 or w.endswith("ly") or "-" in w:
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith(("ches", "shes", "xes", "zes", "sses")) and len(w) > 5:
        return w[:-2]
    if w.endswith("ied") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("ed") and len(w) > 5 and not w.endswith(("eed", "ied")):
        base = w[:-2]
        if base in (
            "measur", "observ", "describ", "compar", "introduc", "propos", "increas",
            "decreas", "caus", "produc", "reduc", "induc", "deduc", "assum", "consum",
            "defin", "combin", "examin", "determin", "declin", "requir", "acquir",
            "ensur", "achiev", "believ", "receiv", "conclud", "includ", "exclud",
            "provid", "divid", "decid", "coincid", "correl", "calcul", "simulat",
            "evaluat", "investigat", "demonstrat", "indicat", "illustr", "estimat",
            "generat", "operat", "separat", "accelerat", "aggravat", "dissipat",
            "fluctuat", "oscillat", "dominat", "initiat", "terminat", "originat",
            "associat", "locat", "relat", "rotat", "vibrat", "penetrat", "concentrat",
            "propagat", "mitigat", "facilitat", "necessitat", "incorporat", "delineat",
            "formul", "accumul", "nucleat", "degrad", "erod", "plat", "coat", "analyz",
            "analys", "characteriz", "summariz", "normaliz", "oxidiz", "carboniz",
            "miniaturiz", "stabiliz", "utiliz", "scrutiniz", "elucidat", "leverag",
            "underscor", "delv", "coupl", "slid", "bounc", "wip", "attribut", "ascrib",
        ):
            return base + "e"
        if len(base) >= 3 and base[-1] == base[-2] and base[-1] in "bdgmnprt":
            return base[:-1]
        return base
    if w.endswith("ing") and len(w) > 5:
        base = w[:-3]
        if base in (
            "measur", "observ", "describ", "compar", "introduc", "propos", "increas",
            "decreas", "caus", "produc", "reduc", "induc", "deduc", "assum", "defin",
            "combin", "examin", "determin", "declin", "requir", "acquir", "ensur",
            "achiev", "receiv", "conclud", "includ", "exclud", "provid", "divid",
            "decid", "correl", "calcul", "simulat", "evaluat", "investigat",
            "demonstrat", "indicat", "illustr", "estimat", "generat", "operat",
            "separat", "accelerat", "aggravat", "dissipat", "fluctuat", "oscillat",
            "dominat", "initiat", "terminat", "originat", "associat", "locat",
            "relat", "rotat", "vibrat", "penetrat", "concentrat", "propagat",
            "mitigat", "facilitat", "necessitat", "incorporat", "delineat", "formul",
            "accumul", "nucleat", "degrad", "erod", "analyz", "analys", "characteriz",
            "summariz", "normaliz", "oxidiz", "carboniz", "miniaturiz", "stabiliz",
            "utiliz", "scrutiniz", "elucidat", "leverag", "underscor", "delv",
            "coupl", "slid", "bounc", "wip", "attribut", "ascrib",
        ):
            return base + "e"
        if len(base) >= 3 and base[-1] == base[-2] and base[-1] in "bdgmnprt":
            return base[:-1]
        return base
    if w.endswith("s") and not w.endswith(("ss", "us", "is", "os", "as")) and len(w) > 4:
        return w[:-1]
    return w


def is_topic_word(w: str) -> bool:
    return w in DOMAIN_TOPIC_WORDS or lemmatize_token(w) in DOMAIN_TOPIC_WORDS


def extract_ngrams(
    records: list[dict[str, Any]],
    weighted: bool = True,
    filter_topic_words: bool = False,
) -> dict[str, Counter[str]]:
    """Extract weighted counts of unigrams (surface & lemma), bigrams, and trigrams."""
    uni_surf: Counter[str] = Counter()
    uni_lemma: Counter[str] = Counter()
    bigrams: Counter[str] = Counter()
    trigrams: Counter[str] = Counter()

    for rec in records:
        w = float(rec.get("effective_weight", 1.0)) if weighted else 1.0
        txt = PLACEHOLDER_RE.sub(" ", rec["text"])
        clauses = re.split(r"[.!?;:()]+", txt)
        for cl in clauses:
            toks = [t.lower() for t in TOKEN_RE.findall(cl)]
            if not toks:
                continue
            for t in toks:
                if t in UNIGRAM_STOPWORDS or len(t) <= 2:
                    continue
                if filter_topic_words and is_topic_word(t):
                    continue
                uni_surf[t] += w
                uni_lemma[lemmatize_token(t)] += w

            for i in range(len(toks) - 1):
                t1, t2 = toks[i], toks[i + 1]
                if t1 in UNIGRAM_STOPWORDS and t2 in UNIGRAM_STOPWORDS:
                    continue
                if filter_topic_words and (is_topic_word(t1) or is_topic_word(t2)):
                    continue
                bigrams[f"{t1} {t2}"] += w

            for i in range(len(toks) - 2):
                t1, t2, t3 = toks[i], toks[i + 1], toks[i + 2]
                if t1 in UNIGRAM_STOPWORDS and t2 in UNIGRAM_STOPWORDS and t3 in UNIGRAM_STOPWORDS:
                    continue
                if filter_topic_words and (is_topic_word(t1) or is_topic_word(t2) or is_topic_word(t3)):
                    continue
                trigrams[f"{t1} {t2} {t3}"] += w

    return {
        "unigram_lemma": uni_lemma,
        "unigram_surface": uni_surf,
        "bigram": bigrams,
        "trigram": trigrams,
    }


def monroe_log_odds(
    counts_a: Counter[str],
    counts_b: Counter[str],
    prior_strength: float = 500.0,
    min_count: float = 2.0,
    top_k: int = 100,
    normalize_scale: float | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Compute Monroe et al. (2008) z-scored log-odds with informative Dirichlet prior."""
    tot_a_raw = sum(counts_a.values()) or 1.0
    tot_b_raw = sum(counts_b.values()) or 1.0

    scale_a = (normalize_scale / tot_a_raw) if normalize_scale is not None else 1.0
    scale_b = (normalize_scale / tot_b_raw) if normalize_scale is not None else 1.0

    vocab = {
        w for w in (set(counts_a) | set(counts_b))
        if counts_a[w] >= min_count or counts_b[w] >= min_count
    }

    ca = {w: counts_a[w] * scale_a for w in vocab}
    cb = {w: counts_b[w] * scale_b for w in vocab}
    na = sum(ca.values()) or 1.0
    nb = sum(cb.values()) or 1.0

    alpha: dict[str, float] = {}
    for w in vocab:
        p_pool = (ca[w] + cb[w]) / (na + nb)
        alpha[w] = max(prior_strength * p_pool, 0.01)
    alpha_0 = sum(alpha.values()) or 1.0

    scored: list[dict[str, Any]] = []
    for w in vocab:
        ya = ca[w] + alpha[w]
        yb = cb[w] + alpha[w]
        da = na + alpha_0 - ya
        db = nb + alpha_0 - yb
        if da <= 0 or db <= 0:
            continue
        delta = math.log(ya / da) - math.log(yb / db)
        var = (1.0 / ya) + (1.0 / yb)
        z = delta / math.sqrt(var)
        scored.append({
            "term": w,
            "z_score": round(z, 3),
            "log_odds": round(delta, 3),
            "count_a_weighted": round(counts_a[w], 2),
            "count_b_weighted": round(counts_b[w], 2),
            "rate_a_per_10kw": round(counts_a[w] / tot_a_raw * 10000.0, 2),
            "rate_b_per_10kw": round(counts_b[w] / tot_b_raw * 10000.0, 2),
        })

    scored.sort(key=lambda x: x["z_score"], reverse=True)
    return {
        "top_positive_A": [x for x in scored if x["z_score"] > 0][:top_k],
        "top_negative_B": [x for x in reversed(scored) if x["z_score"] < 0][:top_k],
    }


def verify_ai_cliches(
    train_sa: list[dict[str, Any]],
    all_ren_sa: list[dict[str, Any]],
    tier_s: list[dict[str, Any]],
    tier_b: list[dict[str, Any]],
    ai_paras: list[dict[str, Any]],
) -> dict[str, Any]:
    """Verify exact counts of candidate AI clichés across Ren S, S+A train, all S+A, Student B, and AI baseline."""
    def _concat(recs: list[dict[str, Any]]) -> tuple[str, int]:
        texts = [PLACEHOLDER_RE.sub(" ", r["text"]) for r in recs]
        joined = "\n".join(texts).lower()
        n_w = sum(len(TOKEN_RE.findall(t)) for t in texts)
        return joined, max(n_w, 1)

    txt_sa_tr, nw_sa_tr = _concat(train_sa)
    txt_sa_all, nw_sa_all = _concat(all_ren_sa)
    txt_s, _ = _concat(tier_s)
    txt_b, _ = _concat(tier_b)
    txt_ai, nw_ai = _concat(ai_paras)

    verified_banned: list[dict[str, Any]] = []
    verified_allowed_or_signature: list[dict[str, Any]] = []

    for term in AI_CLICHE_CANDIDATES:
        pat = re.compile(rf"\b{re.escape(term.lower())}\b")
        c_s = len(pat.findall(txt_s))
        c_sa_tr = len(pat.findall(txt_sa_tr))
        c_sa_all = len(pat.findall(txt_sa_all))
        c_b = len(pat.findall(txt_b))
        c_ai = len(pat.findall(txt_ai))
        entry = {
            "term": term,
            "count_S": c_s,
            "count_SA_train": c_sa_tr,
            "count_SA_all20": c_sa_all,
            "count_B_students": c_b,
            "count_AI_baseline": c_ai,
            "rate_SA_all_per_10kw": round(c_sa_all / nw_sa_all * 10000.0, 2),
            "rate_AI_per_10kw": round(c_ai / nw_ai * 10000.0, 2),
        }
        if c_sa_all == 0:
            entry["status"] = "BANNED (0 hits in all 20 Ren S+A papers)"
            verified_banned.append(entry)
        else:
            entry["status"] = "USED_BY_REN (do NOT ban)" if c_sa_all >= 3 else "RARE_IN_REN (caution, <=2 hits)"
            verified_allowed_or_signature.append(entry)

    return {
        "confirmed_banned_zero_in_ren": verified_banned,
        "attested_in_ren_do_not_blindly_ban": sorted(
            verified_allowed_or_signature,
            key=lambda x: x["count_SA_all20"],
            reverse=True,
        ),
    }


def render_lexicon_report(payload: dict[str, Any]) -> str:
    r_ai = payload["comparisons"]["ren_SA_vs_AI_baseline_style"]
    r_b = payload["comparisons"]["ren_SA_vs_tier_B_style"]
    r_b_all = payload["comparisons"]["ren_SA_vs_tier_B_all"]
    cliches = payload["ai_cliche_verification"]

    lines: list[str] = [
        "# Phase 2.2 — Distinctive Lexicon Report (`lexicon_report.md`)",
        "",
        "> **Method**: Monroe, Colaresi & Quinn (2008) z-scored log-odds ratio with informative Dirichlet prior.",
        "> **Three-Way Comparison**:",
        "> 1. **Ren (S+A, train)** vs **AI Baseline** (`data/baseline/ai_rewrites.jsonl`, 30 topic-matched rewrites) → Anti-AI-Tone Table",
        "> 2. **Ren (S+A, train)** vs **Tier B (student first-author papers, 10 papers)** → Ren Personal Style vs Group Average",
        "",
        "---",
        "",
        "## 1. Ren (S+A Train) vs AI Baseline — Pure Rhetorical & Style Vocabulary",
        "",
        "### 1.1 Top Distinctive Ren Rhetorical Words & Frames ($z > 0$, Preferred by Ren over AI)",
        "",
        "| Rank | Unigram (Lemma) | $z$ | Ren /10kw | AI /10kw | Surface Unigram | $z$ | Rhetorical Bigram | $z$ | Rhetorical Trigram | $z$ |",
        "|---:|---|---:|---:|---:|---|---:|---|---:|---|---:|",
    ]
    ul_pos = r_ai["unigram_lemma"]["top_positive_A"][:25]
    us_pos = r_ai["unigram_surface"]["top_positive_A"][:25]
    bi_pos = r_ai["bigram"]["top_positive_A"][:25]
    tri_pos = r_ai["trigram"]["top_positive_A"][:25]
    for i in range(25):
        u1 = ul_pos[i] if i < len(ul_pos) else {"term": "—", "z_score": 0, "rate_a_per_10kw": 0, "rate_b_per_10kw": 0}
        u2 = us_pos[i] if i < len(us_pos) else {"term": "—", "z_score": 0}
        b = bi_pos[i] if i < len(bi_pos) else {"term": "—", "z_score": 0}
        t = tri_pos[i] if i < len(tri_pos) else {"term": "—", "z_score": 0}
        lines.append(
            f"| {i+1} | `{u1['term']}` | +{u1['z_score']:.2f} | {u1['rate_a_per_10kw']:.1f} | {u1['rate_b_per_10kw']:.1f} "
            f"| `{u2['term']}` | +{u2['z_score']:.2f} | `{b['term']}` | +{b['z_score']:.2f} | `{t['term']}` | +{t['z_score']:.2f} |"
        )

    lines.extend([
        "",
        "### 1.2 Top Distinctive AI-Baseline Words & Frames ($z < 0$, AI Clichés to Avoid)",
        "",
        "| Rank | AI Unigram (Lemma) | $z$ | Ren /10kw | AI /10kw | AI Surface Unigram | $z$ | AI Bigram | $z$ | AI Trigram | $z$ |",
        "|---:|---|---:|---:|---:|---|---:|---|---:|---|---:|",
    ])
    ul_neg = r_ai["unigram_lemma"]["top_negative_B"][:25]
    us_neg = r_ai["unigram_surface"]["top_negative_B"][:25]
    bi_neg = r_ai["bigram"]["top_negative_B"][:25]
    tri_neg = r_ai["trigram"]["top_negative_B"][:25]
    for i in range(25):
        u1 = ul_neg[i] if i < len(ul_neg) else {"term": "—", "z_score": 0, "rate_a_per_10kw": 0, "rate_b_per_10kw": 0}
        u2 = us_neg[i] if i < len(us_neg) else {"term": "—", "z_score": 0}
        b = bi_neg[i] if i < len(bi_neg) else {"term": "—", "z_score": 0}
        t = tri_neg[i] if i < len(tri_neg) else {"term": "—", "z_score": 0}
        lines.append(
            f"| {i+1} | `{u1['term']}` | {u1['z_score']:.2f} | {u1['rate_a_per_10kw']:.1f} | {u1['rate_b_per_10kw']:.1f} "
            f"| `{u2['term']}` | {u2['z_score']:.2f} | `{b['term']}` | {b['z_score']:.2f} | `{t['term']}` | {t['z_score']:.2f} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 2. Ren (S+A Train) vs Tier B (Student First-Author Papers)",
        "",
        "### 2.1 Top Ren-Personal Rhetorical Markers ($z > 0$, More Frequent in Ren than Students)",
        "",
        "| Rank | Style Unigram (Surface) | $z$ | Ren /10kw | B /10kw | Rhetorical Bigram | $z$ | Rhetorical Trigram | $z$ | All-Vocab Bigram | $z$ |",
        "|---:|---|---:|---:|---:|---|---:|---|---:|---|---:|",
    ])
    rb_u = r_b["unigram_surface"]["top_positive_A"][:25]
    rb_b = r_b["bigram"]["top_positive_A"][:25]
    rb_t = r_b["trigram"]["top_positive_A"][:25]
    rba_b = r_b_all["bigram"]["top_positive_A"][:25]
    for i in range(25):
        u = rb_u[i] if i < len(rb_u) else {"term": "—", "z_score": 0, "rate_a_per_10kw": 0, "rate_b_per_10kw": 0}
        b = rb_b[i] if i < len(rb_b) else {"term": "—", "z_score": 0}
        t = rb_t[i] if i < len(rb_t) else {"term": "—", "z_score": 0}
        ab = rba_b[i] if i < len(rba_b) else {"term": "—", "z_score": 0}
        lines.append(
            f"| {i+1} | `{u['term']}` | +{u['z_score']:.2f} | {u['rate_a_per_10kw']:.1f} | {u['rate_b_per_10kw']:.1f} "
            f"| `{b['term']}` | +{b['z_score']:.2f} | `{t['term']}` | +{t['z_score']:.2f} | `{ab['term']}` | +{ab['z_score']:.2f} |"
        )

    lines.extend([
        "",
        "### 2.2 Top Student (Tier B) Rhetorical Markers ($z < 0$, More Frequent in Students than Ren)",
        "",
        "| Rank | Student Unigram (Surface) | $z$ | Ren /10kw | B /10kw | Student Rhetorical Bigram | $z$ | Student Rhetorical Trigram | $z$ |",
        "|---:|---|---:|---:|---:|---|---:|---|---:|",
    ])
    sb_u = r_b["unigram_surface"]["top_negative_B"][:20]
    sb_b = r_b["bigram"]["top_negative_B"][:20]
    sb_t = r_b["trigram"]["top_negative_B"][:20]
    for i in range(20):
        u = sb_u[i] if i < len(sb_u) else {"term": "—", "z_score": 0, "rate_a_per_10kw": 0, "rate_b_per_10kw": 0}
        b = sb_b[i] if i < len(sb_b) else {"term": "—", "z_score": 0}
        t = sb_t[i] if i < len(sb_t) else {"term": "—", "z_score": 0}
        lines.append(
            f"| {i+1} | `{u['term']}` | {u['z_score']:.2f} | {u['rate_a_per_10kw']:.1f} | {u['rate_b_per_10kw']:.1f} "
            f"| `{b['term']}` | {b['z_score']:.2f} | `{t['term']}` | {t['z_score']:.2f} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Corpus-Verified AI Cliché Audit (Verify, Never Assume)",
        "",
        "### 3.1 Confirmed Banned Words (`0` occurrences across all 20 Ren S+A papers)",
        "",
        "| Term / Phrase | S Count | S+A Train Count | S+A All (20) Count | B (Students) Count | AI Baseline Count | Status |",
        "|---|---:|---:|---:|---:|---:|---|",
    ])
    for item in cliches["confirmed_banned_zero_in_ren"]:
        lines.append(
            f"| `{item['term']}` | {item['count_S']} | {item['count_SA_train']} | **{item['count_SA_all20']}** "
            f"| {item['count_B_students']} | {item['count_AI_baseline']} | {item['status']} |"
        )

    lines.extend([
        "",
        "### 3.2 Words Attested in Ren's Corpus (Do NOT Blindly Ban!)",
        "",
        "> Many generic 'anti-AI word lists' ban words like `furthermore`, `moreover`, `subsequently`, `meanwhile`, `significantly`, `substantially`, `nevertheless`, `crucial`, or `comprehensive`. Corpus verification proves Ren actively uses these (and `explicitly` is a core personal signature!).",
        "",
        "| Term / Phrase | S Count | S+A Train Count | S+A All (20) Count | S+A / 10kw | B (Students) Count | AI Baseline Count | Policy |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ])
    for item in cliches["attested_in_ren_do_not_blindly_ban"]:
        lines.append(
            f"| `{item['term']}` | {item['count_S']} | {item['count_SA_train']} | **{item['count_SA_all20']}** "
            f"| {item['rate_SA_all_per_10kw']:.2f} | {item['count_B_students']} | {item['count_AI_baseline']} | {item['status']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    cfg = load_config()
    d_dir = data_dir(cfg)
    proc_dir = d_dir / "processed"
    paras_path = proc_dir / "paragraphs.jsonl"
    ai_path = d_dir / "baseline" / "ai_rewrites.jsonl"

    if not paras_path.exists():
        print(f"[error] {paras_path} not found. Run 02_clean_segment.py first.", file=sys.stderr)
        return 1
    if not ai_path.exists():
        print(f"[error] {ai_path} not found.", file=sys.stderr)
        return 1

    all_paras = [json.loads(line) for line in open(paras_path, encoding="utf-8")]
    ai_paras = [json.loads(line) for line in open(ai_path, encoding="utf-8")]

    train_sa = [p for p in all_paras if p["tier"] in ("S", "A") and p["split"] == "train"]
    all_ren_sa = [p for p in all_paras if p["tier"] in ("S", "A")]
    train_sa_abs_intro = [p for p in train_sa if p["section"] in ("abstract", "introduction", "conclusion")]
    all_ren_abs = [p for p in all_paras if p["tier"] in ("S", "A") and p["section"] == "abstract"]
    tier_s = [p for p in all_paras if p["tier"] == "S"]
    tier_a_train = [p for p in all_paras if p["tier"] == "A" and p["split"] == "train"]
    tier_b = [p for p in all_paras if p["split"] == "secondary"]

    ng_sa_style = extract_ngrams(train_sa, weighted=True, filter_topic_words=True)
    ng_sa_all = extract_ngrams(train_sa, weighted=True, filter_topic_words=False)
    ng_ai_style = extract_ngrams(ai_paras, weighted=False, filter_topic_words=True)
    ng_ai_all = extract_ngrams(ai_paras, weighted=False, filter_topic_words=False)

    ng_abs_ren = extract_ngrams(all_ren_abs + train_sa_abs_intro, weighted=True, filter_topic_words=True)
    ng_b_style = extract_ngrams(tier_b, weighted=False, filter_topic_words=True)
    ng_b_all = extract_ngrams(tier_b, weighted=False, filter_topic_words=False)

    ng_s_style = extract_ngrams(tier_s, weighted=False, filter_topic_words=True)
    ng_a_style = extract_ngrams(tier_a_train, weighted=True, filter_topic_words=True)

    comparisons: dict[str, Any] = {
        "ren_SA_vs_AI_baseline_style": {},
        "ren_SA_vs_AI_baseline_all": {},
        "ren_abstracts_vs_AI_abstracts_style": {},
        "ren_SA_vs_tier_B_style": {},
        "ren_SA_vs_tier_B_all": {},
        "tier_S_vs_tier_A_style": {},
    }

    for level in ("unigram_lemma", "unigram_surface", "bigram", "trigram"):
        min_c_ai = 1.0 if level != "unigram_lemma" else 2.0
        comparisons["ren_SA_vs_AI_baseline_style"][level] = monroe_log_odds(
            ng_sa_style[level], ng_ai_style[level], prior_strength=150.0, min_count=min_c_ai, top_k=100, normalize_scale=12000.0
        )
        comparisons["ren_SA_vs_AI_baseline_all"][level] = monroe_log_odds(
            ng_sa_all[level], ng_ai_all[level], prior_strength=200.0, min_count=min_c_ai, top_k=100, normalize_scale=15000.0
        )
        comparisons["ren_abstracts_vs_AI_abstracts_style"][level] = monroe_log_odds(
            ng_abs_ren[level], ng_ai_style[level], prior_strength=120.0, min_count=1.0, top_k=60, normalize_scale=8000.0
        )
        comparisons["ren_SA_vs_tier_B_style"][level] = monroe_log_odds(
            ng_sa_style[level], ng_b_style[level], prior_strength=300.0, min_count=2.0, top_k=100, normalize_scale=25000.0
        )
        comparisons["ren_SA_vs_tier_B_all"][level] = monroe_log_odds(
            ng_sa_all[level], ng_b_all[level], prior_strength=400.0, min_count=2.0, top_k=100, normalize_scale=30000.0
        )
        comparisons["tier_S_vs_tier_A_style"][level] = monroe_log_odds(
            ng_s_style[level], ng_a_style[level], prior_strength=200.0, min_count=2.0, top_k=60, normalize_scale=12000.0
        )

    cliches = verify_ai_cliches(train_sa, all_ren_sa, tier_s, tier_b, ai_paras)

    payload = {
        "meta": {
            "train_sa_paragraphs": len(train_sa),
            "all_ren_sa_paragraphs": len(all_ren_sa),
            "tier_b_paragraphs": len(tier_b),
            "ai_baseline_paragraphs": len(ai_paras),
        },
        "ai_cliche_verification": cliches,
        "comparisons": comparisons,
    }

    out_json = proc_dir / "lexicon.json"
    out_md = proc_dir / "lexicon_report.md"
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(render_lexicon_report(payload), encoding="utf-8")

    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    print(f"Confirmed zero-frequency banned AI clichés: {len(cliches['confirmed_banned_zero_in_ren'])}")
    print(f"Attested in Ren (do not ban): {len(cliches['attested_in_ren_do_not_blindly_ban'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

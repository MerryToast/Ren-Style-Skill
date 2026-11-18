<!-- PARTIAL — completed in Phase 3 via pipeline/prompts/style_vs_error.md -->
# Error Policy

Decided policy: **imitate style, fix grammar** — default `fidelity_level: balanced`.

| Class | balanced (default) | strict |
|---|---|---|
| `KEEP_STYLE` — characteristic, idiomatic choices | reproduce | reproduce |
| `FIX_ERROR` — grammatical / lexical errors | correct | correct |
| `OPTIONAL_NONNATIVE` — harmless non-native habits | use sparingly | reproduce |

## KEEP_STYLE

## FIX_ERROR

Seed examples observed in abstracts (to be confirmed):

| Observed | Correct form |
|---|---|
| "are resulted from" | "result from" |
| "our new designed test rig" | "our newly designed test rig" |
| "ever published results have shown" | "previously published results have shown" |
| "reoccurring the welding phenomenon" | "reproducing the welding phenomenon" |

## OPTIONAL_NONNATIVE

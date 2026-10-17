# Field evidence

What happened when panels or persona roles were tested on real work, against a
plain single-model baseline. The research corpus (`docs/research/`) says what
other people found; this file says what happened here. Read it at the evidence
gate (`evidence-gate.md`) and before proposing any panel.

## How to use it

- Before a gate decision, find rows in the same task family.
- A family whose most recent row says the panel or role did WORSE than the
  baseline on the deciding criterion drops one confidence level until a newer
  row reverses it (see `evidence-gate.md`, "Field override").
- Mixed results (better on one criterion, worse on another) do not change the
  level, but the gate names the weaker criterion as a required evaluation
  signal for any new role in that family.

## How to add a row

Add one row after every trial run, work sample, or Stage 11 review that
compared a panel or role against a baseline. One row per comparison. Summary
level only (this repo is public): no confidential or client-identifying detail. Ask the user before
writing (same consent rule as the roster).

| Field | What to write |
|---|---|
| Date | YYYY-MM-DD |
| Task | one line, generalized |
| Family | one of the families in `evidence-gate.md` |
| Compared | what ran against what (seats, models, baseline) |
| Judged by | blind judge / user / both; criteria |
| Result | per criterion: panel better / same / worse, with numbers if any |
| What fixed it | any non-persona step that changed the result |
| Source | path to the report |

## Rows

### 2026-08-26: literature-search coverage audit
- Family: General critique or analytical judgment
- Compared: 4 isolated persona lenses + adversarial verifier (all Claude) vs the stock single-model coverage script, same corpus
- Judged by: author review of both gap lists
- Result: breadth (scope checklist items caught): panel WORSE. Depth (base rates, effect sizes, definitions): panel BETTER. False positives: panel better (verifier removed one). Cost: panel worse. One seat (policy lens) produced zero usable gaps on a non-policy topic.
- What fixed it: a cheap single-model checklist pass BEFORE the panel, its gaps exempt from the panel's cap (now the "Coverage review" recipe row).
- Source: deep-research-squad skill build notes (local, not in this repo)

### 2026-09-16: deck hook writing from a source document
- Family: Creative divergence (hook writing), output bound to a source
- Compared: 3-lens persona hook panel vs a ~300-word single-writer prompt vs the full Narrative Engine, 4 sources, blind judge (gpt-6-astra)
- Judged by: blind judge on hook, chain, fidelity to source, naturalness
- Result: fidelity: panel WORSE (3.3 vs 7.3 on 10). The judge's verdict: persona panels at the hook stage are refuted for this use.
- What fixed it: a separate evidence reviewer holding the source (fidelity 9.5 on re-test, 2026-09-23). Now the SOURCE CHECK in `hard-rules.md`.
- Source: Narrative Engine ablation report and 2026-09-23 re-test (local, not in this repo)

# Synthesis modes

How you combine lens outputs is a first-order lever. Naive mean-blending of
quality-mixed lenses reliably flattens them back toward the average and discards the
standout view. Two rules always apply:

1. **De-duplicate BEFORE combining when the set is large (8 or more items).**
   Collapse near-identical items so the combiner is not flooded with the same view
   stated four ways. For a normal panel of 3-6 long lens outputs, skip this: the
   combiner reads them all, and the claim coverage check below catches losses.
2. **Never naive-mean-blend.** Pick a mode below; the default is Reconcile.

## Reconcile / dissent-carrying synthesis — DEFAULT

Produce the majority view PLUS explicitly labeled minority and dissenting views and
unique findings. This is the judicial "majority opinion with published dissents"
template. Use it for analytical judgment, creative direction, strategy, and normative
work — anywhere the value is an emergent combined answer that no single lens held.

Exact synthesis prompt:

```
You are combining several independent lenses on one question. Do NOT average them
into a bland consensus. Produce:
1. Majority view — where most lenses converge, and why.
2. Minority / dissenting views — each labeled with which lens holds it and the
   strongest case for it. Do not drop a view just because it is outnumbered.
3. Unique findings — points only one lens raised that the others missed.
4. Unified recommendation — your best synthesis, explicitly noting which dissent
   must survive into the decision.
Answer the underlying questions: Where do they agree? Where do they conflict? What
is the unified recommendation, and what dissent must survive?
```

## Concatenate

Append each lens output under its own heading, no merging. Use ONLY for genuinely
independent items that should not be reconciled (e.g. a set of distinct options meant
to stay separate). Apparent independence is often false when lenses came from one
model — prefer Reconcile when unsure.

## Vote

Count agreement across lenses, surface the majority answer, and flag disagreements.
For recoverable-answer tasks where a single answer is expected.

Paste-ready prompt:

```
You are tallying N independent lens answers to one question. Count agreement per
distinct answer. Output: (1) the majority answer with its count, (2) every
minority answer with its count and which lens held it, (3) a flag if any lens's
reasoning suggests the majority may be wrong. Do not blend answers.
```

## Selection

A judge picks the single best lens output. Better-evidenced than blending for tasks
with a recoverable best answer AND a competent judge — but it **cannot exceed the
best single candidate**, so never use it when you want an emergent combined answer.
For open-ended lens synthesis, use Reconcile instead.

Paste-ready judge prompt (recoverable-answer tasks only):

```
You are selecting the single best of N candidate outputs against the stated
goal. Rank all N with one-line justifications, name the winner, and list what
the winner MISSES that losing candidates contained (so the caller can graft).
Do not merge candidates.
```

On creative rows the selector is the HUMAN per hard-rules.md #Guardrails switch
by mode — never this judge prompt.

## Tight formats (word limits, fixed structure)

When the user's format cannot hold a majority view plus dissents (a 70-90 word
block, a one-line verdict):
- `synthesis.md` keeps the full combine (majority, labeled dissent, unique
  findings). The claim coverage check scores THIS file.
- The same synthesizer subagent cuts `deliverable.md` from it in the user's
  format. The SOURCE CHECK, the format check and any blind judging use THIS
  file, against the baseline in the same format.
- Report kept dissent to the user in one line outside the deliverable.

## Union (Coverage review row)

List every distinct gap or finding once. Checklist-pass items first, all of
them, outside any cap. Then lens findings, de-duplicated against the checklist
and each other, severity-ranked, capped at 8 unless the user set a cap. Each
item names who raised it. The verifier's refutations remove items; log what
was removed and why. Union needs no dissent section; the refutation log takes
its place. The checklist pass writes `checklist.md`, opening with the scope it
walked (the user's scope, else the standard practice list for the domain).

## Diversity-preserving set / variance-aware aggregate

Diversity-preserving (creative option sets, scenarios): emit the full
de-duplicated SET — no winner, no merging; the human selects.
Variance-aware aggregate (forecasting): report the center AND the spread AND the
minority tail — never the mean alone.

---

## Claim coverage check (after every synthesis)

The question that matters is whether each lens's distinct points survived into
what the user receives. Word overlap cannot answer it: two lenses can share
words and disagree, or differ in words and agree. So the check is a model
judgment, scored by a script.

1. A fresh checker (not the synthesizer) gets every lens output and the
   synthesis, and the CLAIM COVERAGE PROMPT below. It writes
   `run-<timestamp>/coverage.json`.
2. Run `python3 <skill-dir>/scripts/coverage_report.py run-<timestamp>/coverage.json`.
   It prints "Kept K of N distinct points", lists what was dropped or
   contradicted, and exits 1 when a lens was silenced (nothing of it kept).
3. A silenced lens or a dropped point that a lens marked as its "Dissent I would
   defend" means the synthesis flattened the panel: re-run the synthesis once
   with the dropped points named, then report the final count.
4. For dissent-carrying modes, also confirm the labeled minority/dissent section
   exists (its absence is a FAIL). Vote and Selection outputs legitimately have
   none.

For SET outputs (creative options, scenarios) the same check runs with
"kept" meaning "still present as its own option in the delivered set".

`diversity.py` remains an optional extra for set-spread. Without an embeddings
key it measures word overlap only; report it as such or leave it out.

CLAIM COVERAGE PROMPT:

```
You check whether a synthesis kept what each lens said. You see N lens outputs
and one synthesis. For each lens:
1. List its distinct points: claims, recommendations, objections, and its
   "Dissent I would defend". Merge restatements; keep at most 8 per lens.
2. For each point, mark kept (the synthesis states it, or plainly attributes it),
   dropped (absent), or contradicted (the synthesis says otherwise without
   labeling it as a dissent).
Return JSON only:
{"lenses": [{"lens": "<name>", "claims": [{"claim": "<short>", "status": "kept|dropped|contradicted"}]}]}
```

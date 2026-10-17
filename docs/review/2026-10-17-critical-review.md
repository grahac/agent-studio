# Agent Studio: critical review

Date: 17 Oct 2026. Reviewer: Claude (Opus 5.5), desk review for NR before Kata emir#8k7a.
Scope: `SKILL.md`, `methodologies/kernel.md`, all 15 files in `references/`, the scripts, and the tests (50 of 50 pass), read against the five research documents in `docs/research/` and two later field tests that used the skill's panels.
Method: reading only. No panels were run for this review.

## Summary

The skill follows its research closely on how to run a panel: isolated generation, a critic, no averaging, dissent kept. Its weak points are elsewhere:

1. It has never been tested on outcomes. Both later field tests found panels weaker than expected, and neither result was fed back into the skill.
2. It has no rule for work that must stay true to sources (briefings, reports, decks). That is where both field tests found the damage.
3. Its measurement tools do not work in a normal session (no API keys), and the main one measures word overlap, not difference in argument.
4. It is very heavy for most real uses: 11 stages, two Do-It engagements, about 1,800 lines of instructions.

## The field evidence the skill does not yet know about

| Test | What was compared | Result |
|---|---|---|
| Narrative Engine hook panel, 16 Sep 2026 (`~/Projects/family-office/agent-studio-out/ablation/REPORT.md`) | 3-lens persona panel writing deck hooks vs a ~300-word single-writer prompt, blind judge | Panel made fidelity to the source worse (3.3 vs 7.3 on 10). Fidelity recovered only when a separate evidence reviewer holding the source was added (re-test 23 Sep: 9.5). |
| deep-research-squad, 26 Aug 2026 (memory `project_deep_research_squad_skill`) | 4-persona coverage panel + verifier vs the stock single-model coverage script | Not strictly better. Single model won on checklist breadth and cost; panel won on depth and removed one false positive. The fix was a hybrid: cheap single-model checklist pass first, panel second. One seat (Cicero, policy) produced 0 usable gaps. |

Both point the same way: panels add depth and angles, they lose breadth and source fidelity, and the fix in both cases was a non-persona step around the panel.

## Findings, ranked by impact

### 1. No source-fidelity rule (HIGH)

The evidence gate has eight task families. None covers "write from sources" (briefings, reports, summaries, decks). Such work would land in "General critique or analytical judgment" (a blind work sample is owed) or "Creative divergence" (direct hire, no test). The second path is the one the hook panel took, and it hurt fidelity.

The research says this too. Persona construction bible section 3: constructed personas "invent unsupported detail" (MirageBench, 35-49% over-inference, via news). Ensembles bible section 1: personas change substance, not only tone.

Fix: add a hard rule. Any seat whose output makes claims about source material gets a separate source-holding verifier (not the critic, not a persona) that checks each figure and claim against the source. Add a ninth family, "Source-bound writing", that maps to "Promising, but experimental", so a blind sample is owed, with fidelity as a required evaluation signal.

### 2. No outcome evidence, and no loop to collect it (HIGH)

The repo lists behavioral QC, population metrics and report regression tests as deferred. The playbook (section 7) says the panel design "has zero direct evidence". Since then two field tests ran, and the skill still cites only the August corpus.

Fix:
- Add `references/field-evidence.md`: one row per real comparison (task, family, panel vs baseline, result, source path). Seed it with the two tests above and add emir#8k7a when it reports.
- Have the evidence gate read it. A family with a field result against panels drops one confidence level until a newer test reverses it.

### 3. The one-off panel door has no baseline (HIGH)

Door 4 runs the panel and ends with a self-assessed performance review. The user never sees what a single strong pass would have produced. So every run "works", and the skill learns nothing. The research asks for "cost-adjusted quality vs a self-consistency baseline" (playbook section 5; ensembles bible section 6).

Fix: by default, run one single-model pass on the same brief alongside the panel (cost: one more subagent). Show the panel's unique contributions next to it ("what the panel found that one pass did not"), and log the pair to `field-evidence.md`. Allow skipping when the user says so.

### 4. Breadth needs a single-model pass, not a panel (MED)

The squad test found panels skip the obvious. Personas focus attention, so they also narrow it (playbook section 0: "Personas focus attention, they do not add capability").

Fix: add a hybrid recipe row ("Coverage or review with a checklist: single-model checklist pass, then panel for depth; checklist gaps do not compete with panel gaps for the cap"). Point the artifact/skill review row at it.

### 5. The measurement tools do not run in a normal session (MED)

`diversity.py` needs `OPENAI_API_KEY`. Without it, it falls back to TF-IDF word overlap, labelled "degraded". `exemplar_find.py find` needs `EXA_API_KEY` and exits 20 without it. Neither key is set in the shell Claude Code runs in today. So every panel's "coverage note" is a word-overlap score.

Even with embeddings, the measure is weak. Synthesis bible section 4: "two lenses can be embedding-close yet argumentatively opposite." The flattening test (synthesis farther from the outlier lens) is the skill's own invention, with no source.

Fix: replace the score with a claim-level coverage check, which the synthesis bible names as the missing benchmark (section 5). A cheap model pass lists each lens's distinct claims, then marks each one kept, dropped or contradicted in the synthesis. Report "kept 11 of 14 distinct points; dropped: ...". Keep `diversity.py` as an optional extra. Load keys from a known env file, or say plainly that the score is lexical.

### 6. Same-model panels are the weak case, and the skill nearly always runs them (MED)

The strongest evidence for value-diverse panels used different models per seat (Sela 2026: consensus concentration 70.9% to 46.1%). Same-model agents "are low-variance and collude quickly" (ensembles bible section 3). The skill only "offers" other model families for high-stakes normative panels. In practice every seat is Claude.

A second family is already available here: Codex via fresheyes (`FRESHEYES_MODEL`).

Fix: run the critic, or one generating seat, on Codex by default for judgment panels. That is the cheapest structural step toward real independence.

### 7. Famous names are the default hire, but the evidence for them is the weakest (MED)

The August voice redesign made "lean toward widely recognizable real people" the default. The construction bible ranks named exemplars low as standalone drivers ("act mainly as multipliers", section 1). It also documents caricature (emulations too consistent: loadings 0.87-0.95 vs human 0.52-0.65), name-memorization inflating fidelity scores, and anthropomorphic names raising over-trust (Brookings). The main pro-names source (MIT/UCSD) came via news only.

The persona file is still stance-first, and a caricature probe exists, so this is not broken. The risk is that the user picks on the name while the stance does the work.

Fix: keep names for the user experience. In the slate, lead each candidate with the stance they bring and treat the name as shorthand for it. Run the blind work sample on the anonymous prototype (already the rule), and say in the slate that the name is not what was tested.

### 8. The process is heavy for most asks (MED)

There are 11 stages, two Do-It engagements, a charter, a manifest and a validator, spread over about 1,800 lines the agent must read. Most real uses (the squad, the hook panel, 8k7a) are door 3 or door 4. The durability gate already keeps the heaviest parts off light runs, but the agent still loads all of it.

Fix: move the door 4 path and the gate summary into a short core `SKILL.md`. Load the full-lifecycle files only when door 1 or 2 is chosen. Target: under 150 lines for the core file.

### 9. Smaller items (LOW)

- Value-laden deliberation maps to "Research supports trying this" (direct hire, no test). Its best evidence is the different-model setup (finding 6). With same-model seats, it should owe a work sample.
- "De-duplicate by embedding before combining" adds little for 3-5 long lens outputs. It matters for large candidate sets. Scope it to sets of 8 or more.
- The critic is one more same-model judge. Correlated judge errors ("Nine Judges, Two Effective Votes", unverified) cap its value. Finding 6 also covers this.
- `agent-studio-out/` sits inside the repo, against the skill's own "never this repo" rule (left over from an August run).
- The Playbook points to "Companion files on Desktop". The files now live in `docs/research/`.
- Memory `reference_agent_studio_skill_repo` says the installed skill is an rsync copy. It is a symlink to this repo, so edits go live at once. Commit before editing.

## What is solid and should stay

- Isolation per lens, critic after the lenses, one debate round at most, no averaging, labelled dissent. These follow the strongest evidence in the corpus.
- In-house by default, and "a successful run may create no persona". The squad and hook results support this.
- The blind work sample on an anonymous prototype. It is the right test, and it should be used more (findings 1, 3, 9).
- Mode-switched guardrails (stereotype check for judgment work, cliché check for creative work).
- Harm reported separately from no-lift.

## Proposed order of work

1. Findings 1, 2 and 3 together: source-fidelity rule, field-evidence file, door 4 baseline. About 45 min. Highest value, mostly reference-file edits.
2. Findings 5 and 6: claim-coverage check and a Codex seat. About 60 min, including a script change and tests.
3. Finding 4: hybrid recipe row. About 15 min.
4. Finding 7: slate wording. About 15 min.
5. Finding 8: split SKILL.md. About 60 min. Do it last, after the content settles.

## Bearing on emir#8k7a

Under today's rules, a sector-briefing panel would probably be classed as creative divergence and hired with no test. With finding 1 in place, it owes a blind sample with fidelity as a required signal, plus a source-holding verifier. That is close to what 8k7a already plans (same validators, blind side-by-side, figure accuracy checked by hand). 8k7a can serve as the first entry in `field-evidence.md` and the first real test of the revised skill.

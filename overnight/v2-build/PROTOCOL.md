# PROTOCOL — floodApp v2 Overnight Build Campaign

## North-star goal
Advance the Historic Flood Recovery Tool from v1 to v2 per `/Users/becca/Code/floodAPp/V2_PLAN.md`,
building everything that is **autonomously achievable** overnight, with every increment
**validated by an automated acceptance test** and **critiqued** before and after it is built.

Scope this campaign to P0–P2 (external-dependency-free work):
- **P0** — Security + credibility: remove the leaked Groq key from client code; make chat strictly
  user-key; add a secret-scan guard; add source citations to existing hardcoded guidance.
- **P1** — The NLP authoring pipeline: a reproducible Python pipeline that compiles **structured,
  cited** guidance from `docs/`, plus a real first `content-bundle.json` whose every citation is
  programmatically verified against source text. This is the headline deliverable.
- **P2** — PWA + i18n scaffold: installable, offline-capable app shell; string externalization +
  a language switcher + Spanish for at least the homeowner flow.

Explicitly **out of scope** (hard external dependencies — document, don't build):
- Backend proxy deployment, Netlify redeploy (needs Becca's hosting/secrets).
- P3 computer vision (needs Esri partnership + models/compute).
- P4 SHPO aggregation backend (needs infra) — may scaffold a data schema only.

## Metric (this is a BUILD loop, not an optimization loop)
`readiness = (# deliverables with a PASSING automated acceptance test) / (# deliverables defined)`.
A deliverable counts ONLY when its acceptance test passes and the test is recorded in the round file.
Track the raw ledger in `LEDGER.md`. No partial credit; no "probably works."

## Hard safety rails
1. **Never mutate source data.** `docs/`, `simeonResources/`, the source PDFs, and the two
   `.docx` vision notes are READ-ONLY. All new artifacts live under `overnight/v2-build/`.
2. **App-source edits are allowed but additive & reversible.** `floodapp.html`, `build-kb.py`,
   and new `pipeline/` files may be edited/created (that IS the build), but: keep a copy of any
   file before first edit in `overnight/v2-build/artifacts/originals/`; never delete user content;
   never commit or push (Becca commits).
3. **Evidence before claims.** A deliverable is "done" only with a re-run acceptance test in the
   round file. Log the actual command + output.
4. **No silent error sinks.** Full tracebacks to the round file. Never fabricate a metric or a
   citation. A failed round is a valid round.
5. **Citations must be real.** Every guidance citation must resolve to actual text in a `docs/`
   source (verified by `verify_citations`). A citation that can't be verified is a bug, not a note.
6. **Secrets.** Never write a real API key into any file. The leaked key must be REMOVED from
   working files; only Becca can revoke it — flag that at the top of every report.

## Budget / limit handling
- No paid external LLM calls are available (no key in env) — synthesis is done by in-loop Claude
  subagents; deterministic validation is free Python. So $-budget is ~0; the real limit is the
  session usage window.
- If a rate/usage limit is hit: finish writing the current round file + STATE.json + LEDGER.md,
  then `ScheduleWakeup` for the reset window and resume. State on disk must be sufficient to
  reconstruct the campaign with zero context.

## Round contract (each round)
MEASURE → HYPOTHESIZE (Opus gate: 3 structurally-diverse next-move critiques, ≥1 challenging
whether we're building the right thing) → SELECT → EXECUTE (additive) → VERIFY (acceptance test)
→ LOG+PERSIST (round file, LEDGER.md, HYPOTHESES.json write-back, STATE.json) → SCHEDULE.

## Stop conditions (any one)
- All P0–P2 deliverables in the ledger have passing acceptance tests.
- Frontier empty / all families exhausted or dead (nothing autonomously buildable remains).
- Usage limit hit → checkpoint + schedule resume (not a true stop).
- 3 consecutive rounds with no new passing deliverable AND no viable new hypothesis.

## Handoff note for Becca (kept current in FINAL_REPORT.md)
What was built, what passed, what needs her (revoke key, deploy proxy, commit), and how to run it.

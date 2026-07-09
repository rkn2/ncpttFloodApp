# Round 01 — P0 security containment

## MEASURE
- Start metric: 0/11 deliverables passing.
- Confirmed live leak: `gsk_rfyOhRY9…56se` hardcoded at floodapp.html:2109 and deploy/index.html:2109,
  used as default by `getGroqKey()`. Present in git commit 5b8f922; repo pushed to public
  github.com/rkn2/ncpttFloodApp (per memory). Env has NO ANTHROPIC/GROQ/OPENAI key.

## HYPOTHESIZE (Opus gate)
Gate proposed 3 diverse moves: (A) P0 security containment; (B) CHALLENGE — build the citation
validator before ANY content, since content built without it is unfalsifiable; (C) retrofit
citations to existing guidance. Gate ranked **B first** (highest-information, load-bearing rail),
then A, then C. Gate flags for later: (1) PDF extraction fidelity is the "silent killer" — validate
per-PDF before trusting the validator; (2) lock the citation SCHEMA now; (3) git history still leaks
the key — human must scrub history + revoke (loop must not rewrite pushed history unattended).

## SELECT (deviation from gate, recorded)
Chose **A this round**, not B. Rationale: the key is leaking on a *public* repo right now; the code
half of the fix is cheap, fully independent, and unambiguously correct — leaving it another round is
irresponsible. The gate itself said "do that half early." B becomes Round 2's sole focus, and I adopt
all three of the gate's forward-looking flags into Round 2's plan.
**Schema decision locked (per gate flag #2):** quote-match anchoring — each citation =
`{source_file, quote (verbatim substring), page?}`; verification = normalized substring match against
extracted source text. Chosen over char-offset anchoring because extraction offsets aren't stable
(OCR/pdftotext), and storing the actual quoted text is the most defensible provenance record.

## EXECUTE (additive)
- Removed `GROQ_DEFAULT_KEY` from floodapp.html + deploy/index.html; `getGroqKey()` now returns only
  the localStorage value (`|| ''`). Added a security comment.
- **Bonus fix (surfaced by the change):** reordered `sendChat()` so the offline passage-retrieval
  branch runs BEFORE the key check. Without a default key, an offline user (the core post-flood case)
  would otherwise have been blocked by a key prompt and unable to use offline search.
- Created `pipeline/scan_secrets.py` — dependency-free credential scanner (Groq/OpenAI/Anthropic/AWS/
  Google/Slack/PEM patterns), self-test mode, git pre-commit-hook-ready. Skips overnight/, binaries.
- Redacted the real key from my own pre-edit backups under overnight/…/originals/.

## VERIFY (acceptance tests — all commands re-run, output captured)
- **D0.1 PASS** — `grep -rn gsk_rfyOhRY9 . --exclude-dir=.git` → no match. Real key absent from entire
  working tree (remains only in git history — flagged for human).
- **D0.2 PASS** — `getGroqKey()` in both files = `localStorage.getItem(LS_GROQ_KEY) || ''`, no fallback.
- **D0.2b PASS** (bonus) — offline-first ordering comment present in both files ahead of key check.
- **D0.3 PASS** — `scan_secrets.py --self-test` → SELF-TEST PASS (exit 0); catches planted key, no
  false positive on clean localStorage code or the words "api key". Full-tree scan → CLEAN (exit 0).

## Metric delta
0/11 → 3/11 passing (D0.1, D0.2, D0.3). D0.2b is a bonus improvement (not a separate ledger row).

## CRITIQUE / carry-forward
- The code fix does NOT close the leak: the key is in pushed git history. **Becca must (1) revoke the
  key in the Groq console and (2) scrub git history (git filter-repo / BFG) + force-push.** Top of
  every report until confirmed.
- Chat is now non-functional online until a user enters their own key. That's correct for security,
  but means the "ask" feature is effectively off by default. Real fix = backend proxy (P0 external,
  out of scope tonight) — documented for handoff.
- Round 2 = the gate's B: citation validator + per-PDF extraction-fidelity precheck, using the locked
  quote-match schema.

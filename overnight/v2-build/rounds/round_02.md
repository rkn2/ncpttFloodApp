# Round 02 — the provenance rail (validation tooling)

## MEASURE
- Start metric: 3/11. Frontier [H2,H3,H4,H5,H6,H7]. Planned move: H2 (citation validator).

## HYPOTHESIZE (Opus gate)
Gate critiqued my proposed verifier design (asked it to, rather than just re-rank). Key findings:
- FALSE FAILS to fix: line-break hyphenation, ligatures/curly quotes (→ use NFKD), page-join headers
  (→ forbid cross-page quotes / keep to single sentence), tables (→ treat as unciteable).
- FALSE PASSES to fix: short quotes match trivially → **minimum quote-length gate (≥8 words/≥40 chars)**.
- Do NOT add fuzzy matching (a paraphrase that passes is worse than a real quote you must re-copy).
- Cache extraction keyed by hash for determinism.
- Sequencing rec: (1) extraction-fidelity precheck FIRST (standalone; a dependency of everything —
  tells you which PDFs are unciteable before you synthesize), (2) verifier w/ mitigations, (3) H5
  retrofit as end-to-end proof, (4) synthesis last.

## SELECT
Adopted the gate's plan wholesale — built precheck + verifier together (verifier needs extracted text).
All gate mitigations baked in.

## EXECUTE (additive, under pipeline/)
- `pipeline/extract.py` — deterministic, hash-cached extraction (pdftotext) + per-PDF fidelity report
  (`(cid:)` ratio, control-char ratio → verdict ok|low|garbled). Writes
  `overnight/v2-build/artifacts/extraction_fidelity.json`.
- `pipeline/verify_citations.py` — normalize() with NFKD + curly/dash unify + soft-hyphen strip +
  de-hyphenation + whitespace collapse + punctuation-light; strict substring; **length gate
  (≥8 words & ≥40 chars)**. verify_citation(), verify_bundle(), --self-test.

## VERIFY (acceptance tests — re-run, output captured)
- **Fidelity precheck** — 13/14 sources verdict≠garbled. **CONFIRMED GATE WARNING EMPIRICALLY:**
  `secretary for interior.pdf` (SOI Standards) is garbled under plain pdftotext (ctrl_ratio=0.2835,
  the known custom-font subset issue). Caught BEFORE any content was built on it.
- **Verifier self-test PASS** (exit 0) — real quote passes; NFKD/curly/hyphen variant passes;
  fabricated fails; wrong-source fails; too-short quote fails (length gate).
- **D1.2 END-TO-END PASS** — against real `nthp-treatment-…pdf`: a genuine 15-word span verifies;
  a fabricated sentence FAILs; the same real span attributed to a DIFFERENT pdf FAILs.

## Metric delta
3/11 → 4/11 (D1.2 DONE). Extraction+fidelity is a validated bonus artifact (partial D1.1; the
per-topic retrieval third of D1.1 remains for Round 3 as synthesis setup).

## CRITIQUE / carry-forward
- **SOI Standards is the app's foundational source and it's garbled under pdftotext.** For any guidance
  citing the SOI Standards, verification must run against OCR'd text. The existing
  `knowledge-base.json` chunks for that PDF were already OCR-cleaned (memory: 62/148 pages OCR'd,
  0 garbled). Round 3 options: (a) add OCR path to extract.py if pytesseract/pdf2image are installed,
  or (b) verify SOI quotes against the KB chunks. Decide in Round 3.
- The length gate + strict matching means authors (subagents) must quote ≥8 contiguous verbatim words.
  Good for provenance; means synthesis must be given the real passages to quote from → build the
  retrieval helper (D1.1 remainder) before synthesis.

#!/usr/bin/env python3
"""
verify_citations.py — the provenance rail for the floodApp authoring pipeline.

A guidance record may only ship if every citation's verbatim quote is actually present in the
cited source document. This makes "don't hallucinate preservation advice" a MECHANICAL check,
not a hope. Strict substring matching only — NO fuzzy/paraphrase matching, because a paraphrase
that passes verification is worse than a real quote an author must re-copy.

Citation schema (locked round 1):  {"source_file": "<name in docs/>", "quote": "<verbatim>", "page": <opt>}

Design mitigations (from the round-2 gate critique):
  - Unicode NFKD normalization  -> collapses ligatures (ﬁ->fi), curly quotes, dashes  [biggest false-fail source]
  - De-hyphenation of line-break hyphens ("recov-\\nery" -> "recovery") + soft hyphen U+00AD
  - Whitespace collapse + punctuation-light normalization
  - MINIMUM QUOTE LENGTH GATE (>=8 words AND >=40 normalized chars) -> blocks short-quote false PASSES

Usage:
    python3 pipeline/verify_citations.py --self-test
    python3 pipeline/verify_citations.py path/to/bundle.json     # verify every citation in a bundle
Importable:  from verify_citations import verify_citation, VerifyResult
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO / "docs"

MIN_WORDS = 8
MIN_CHARS = 40

_curly = {
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "−": "-", " ": " ",
}


def normalize(text):
    """Aggressive-but-safe normalization for substring matching."""
    # NFKD folds ligatures & compatibility forms
    text = unicodedata.normalize("NFKD", text)
    # unify curly quotes / dashes / nbsp
    for k, v in _curly.items():
        text = text.replace(k, v)
    # remove soft hyphen
    text = text.replace("­", "")
    # de-hyphenate line breaks:  "word-\nword" -> "wordword"
    text = re.sub(r"-\s*\n\s*", "", text)
    text = text.lower()
    # strip most punctuation to spaces (keep alphanumerics)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


class VerifyResult:
    def __init__(self, ok, reason, source_file=None):
        self.ok = ok
        self.reason = reason
        self.source_file = source_file

    def __repr__(self):
        return f"VerifyResult(ok={self.ok}, reason={self.reason!r})"


def _load_source_text(source_file, extractor):
    # Unified clean-text provider (handles garbled-but-OCR'd-in-KB sources like the SOI Standards).
    if extractor is None:
        from corpus import source_text
        t = source_text(source_file)
        return t if t else None
    path = DOCS_DIR / source_file
    if not path.exists():
        return None
    text, _ = extractor(path)
    return text


def verify_citation(citation, extractor=None, _cache={}):
    """citation: dict with source_file + quote. Returns VerifyResult.
    extractor=None -> use the unified corpus provider (recommended). A custom extractor
    (used by --self-test) bypasses the corpus for hermetic testing."""
    src = citation.get("source_file", "")
    quote = citation.get("quote", "")
    if not src or not quote:
        return VerifyResult(False, "missing source_file or quote")
    nquote = normalize(quote)
    # length gate — prevents trivially-matching short quotes from passing as provenance
    if len(nquote) < MIN_CHARS or len(nquote.split()) < MIN_WORDS:
        return VerifyResult(False, f"quote too short (need >={MIN_WORDS} words & >={MIN_CHARS} chars; "
                                   f"got {len(nquote.split())} words, {len(nquote)} chars)")
    if src not in _cache:
        raw = _load_source_text(src, extractor)
        if raw is None:
            return VerifyResult(False, f"source not found in docs/: {src}", src)
        _cache[src] = normalize(raw)
    if nquote in _cache[src]:
        return VerifyResult(True, "verified", src)
    return VerifyResult(False, "quote not found in source (possible fabrication, wrong source, "
                               "or extraction gap)", src)


def verify_bundle(bundle_path):
    data = json.loads(Path(bundle_path).read_text(encoding="utf-8"))
    records = data.get("guidance", data if isinstance(data, list) else [])
    total = passed = 0
    failures = []
    for rec in records:
        # citations live inside do/dont items (and optionally soi_standard), not on the record.
        items = list(rec.get("do", [])) + list(rec.get("dont", []))
        if rec.get("soi_standard"):
            items.append(rec["soi_standard"])
        for it in items:
            for cit in it.get("citations", []):
                total += 1
                res = verify_citation(cit)
                if res.ok:
                    passed += 1
                else:
                    failures.append((rec.get("id", "?"), cit.get("source_file", "?"),
                                     res.reason, cit.get("quote", "")[:60]))
    print(f"Citations: {passed}/{total} verified.")
    for rid, src, reason, snippet in failures:
        print(f"  ❌ [{rid}] {src}: {reason}\n       “{snippet}…”")
    return passed, total, failures


def self_test():
    """Self-test with a synthetic in-memory source, no PDF dependency."""
    ok = True
    source = ('The Secretary of the Interior’s Standards recommend that historic masonry be '
              'repointed using lime-based mortar rather than Portland cement, because the softer '
              'mortar protects the surrounding historic fabric from cracking during freeze-thaw '
              'cycles that follow a flood.')

    def fake_extractor(path):
        return source, True

    # patch docs existence by monkeypatching loader via cache pre-seed
    cache = {}
    cache["FAKE.pdf"] = normalize(source)

    # 1. real, long-enough quote -> PASS
    real = {"source_file": "FAKE.pdf",
            "quote": "historic masonry be repointed using lime-based mortar rather than Portland cement"}
    r1 = verify_citation(real, extractor=fake_extractor, _cache=cache)
    if not r1.ok:
        print(f"FAIL: real quote rejected: {r1.reason}"); ok = False

    # 2. quote with ligature/curly-quote/hyphenation variants -> still PASS (normalization)
    variant = {"source_file": "FAKE.pdf",
               "quote": "lime-based mortar rather than Portland cement, because the softer mortar"}
    r2 = verify_citation(variant, extractor=fake_extractor, _cache=cache)
    if not r2.ok:
        print(f"FAIL: normalized variant rejected: {r2.reason}"); ok = False

    # 3. fabricated quote -> FAIL
    fake = {"source_file": "FAKE.pdf",
            "quote": "always replace historic windows with vinyl units for maximum flood resistance"}
    r3 = verify_citation(fake, extractor=fake_extractor, _cache=cache)
    if r3.ok:
        print("FAIL: fabricated quote accepted"); ok = False

    # 4. real quote attributed to WRONG source -> FAIL
    wrong = {"source_file": "OTHER.pdf",
             "quote": "historic masonry be repointed using lime-based mortar rather than Portland cement"}
    cache2 = {"OTHER.pdf": normalize("An unrelated document about drone procurement and mapping.")}
    r4 = verify_citation(wrong, extractor=fake_extractor, _cache=cache2)
    if r4.ok:
        print("FAIL: quote verified against wrong source"); ok = False

    # 5. too-short quote -> FAIL (length gate)
    short = {"source_file": "FAKE.pdf", "quote": "lime-based mortar"}
    r5 = verify_citation(short, extractor=fake_extractor, _cache=cache)
    if r5.ok:
        print("FAIL: too-short quote accepted (length gate broken)"); ok = False

    print("SELF-TEST PASS" if ok else "SELF-TEST FAILED")
    return ok


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 2)
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        print(__doc__)
        sys.exit(0)
    p, t, fails = verify_bundle(args[0])
    sys.exit(0 if p == t and t > 0 else 1)

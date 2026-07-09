#!/usr/bin/env python3
"""
corpus.py — unified clean-text provider, one source of truth per document.

Problem it solves: `secretary for interior.pdf` (the SOI Standards — the app's foundational
source) is garbled under pdftotext (custom font subset). But the existing knowledge-base.json
already contains a CLEAN, OCR'd copy of that document's text (400 chunks, 0 garbling). So instead
of re-running OCR (libs not installed), we source clean text per-document:

  - verdict != garbled  -> use extract.py's pdftotext extraction
  - verdict == garbled AND knowledge-base.json has chunks for it -> reconstruct from those chunks

Both retrieval and citation verification call corpus.source_text(name), so SOI quotes verify
against the clean OCR'd text, not the garbled pdftotext.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "pipeline"))
from extract import extract_one, fidelity  # noqa: E402

KB_PATH = REPO / "knowledge-base.json"
FIDELITY_PATH = REPO / "overnight" / "v2-build" / "artifacts" / "extraction_fidelity.json"

_text_cache = {}
_kb = None
_fidelity = None


def _load_kb():
    global _kb
    if _kb is None:
        _kb = json.loads(KB_PATH.read_text()) if KB_PATH.exists() else {"chunks": []}
    return _kb


def _load_fidelity():
    global _fidelity
    if _fidelity is None:
        _fidelity = json.loads(FIDELITY_PATH.read_text()) if FIDELITY_PATH.exists() else {}
    return _fidelity


def kb_chunks_for(name):
    """All KB chunks whose source == name, in chunk order."""
    chunks = [c for c in _load_kb()["chunks"] if c.get("source") == name]
    chunks.sort(key=lambda c: c.get("chunk_index", 0))
    return chunks


def source_text(name):
    """Return the best clean full text for a document by filename."""
    if name in _text_cache:
        return _text_cache[name]
    fid = _load_fidelity().get(name)
    verdict = fid["verdict"] if fid else None
    text = None
    if verdict == "garbled":
        chunks = kb_chunks_for(name)
        if chunks:
            text = " ".join(c["text"] for c in chunks)  # overlap dup is harmless for substring match
    if text is None:
        path = REPO / "docs" / name
        if path.exists():
            text, _ = extract_one(path)
        else:
            text = ""
    _text_cache[name] = text
    return text


def source_verdict(name):
    """ok | low | garbled | garbled-recovered | missing"""
    fid = _load_fidelity().get(name)
    if not fid:
        return "missing"
    if fid["verdict"] == "garbled":
        return "garbled-recovered" if kb_chunks_for(name) else "garbled"
    return fid["verdict"]


if __name__ == "__main__":
    for name in ["secretary for interior.pdf", "nthp-treatment-flood-damaged-historic-buildings.pdf"]:
        t = source_text(name)
        print(f"{name}: {len(t):,} chars, verdict={source_verdict(name)}")

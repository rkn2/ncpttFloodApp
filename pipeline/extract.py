#!/usr/bin/env python3
"""
extract.py — deterministic, cached text extraction + per-PDF fidelity report.

Part of the floodApp NLP authoring pipeline. This is the FIRST rail: before any guidance
is synthesized from a source, we must know whether that source extracted cleanly. A PDF whose
text is garbled (custom font subsets, failed OCR) cannot be cited reliably, so we flag it and
keep guidance off it.

- Extracts each docs/*.pdf (and .txt/.md) to a cached plain-text file under EXTRACT_DIR.
- Cache key = (path, size, mtime) hash, so re-runs are instant and deterministic.
- Emits extraction_fidelity.json: per-source (cid:) ratio, control-char ratio, char count,
  and a trust verdict (ok | low | garbled).

Deps: pdftotext (poppler). OCR is intentionally NOT required here — if a page is garbled,
that is a signal to report, not to silently paper over.

Usage:
    python3 pipeline/extract.py                # extract all docs/, write fidelity report
    python3 pipeline/extract.py --report       # print fidelity report only (uses cache)
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO / "docs"
EXTRACT_DIR = REPO / "overnight" / "v2-build" / "extracted"
FIDELITY_OUT = REPO / "overnight" / "v2-build" / "artifacts" / "extraction_fidelity.json"

CID_GARBLED = 0.03   # >3% (cid:) sequences -> garbled
CTRL_GARBLED = 0.03  # >3% control chars -> garbled
LOW_TRUST = 0.005    # >0.5% either -> low trust (citeable but review)


def _cache_key(path):
    st = path.stat()
    h = hashlib.sha256(f"{path.name}|{st.st_size}|{int(st.st_mtime)}".encode()).hexdigest()[:16]
    return h


def _pdftotext(path):
    try:
        r = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, check=True)
        return r.stdout
    except FileNotFoundError:
        print("  [error] pdftotext not found — brew install poppler", file=sys.stderr)
        return ""
    except subprocess.CalledProcessError as e:
        print(f"  [error] pdftotext {path.name}: {e.stderr.strip()}", file=sys.stderr)
        return ""


def extract_one(path):
    """Return (text, from_cache: bool). Caches to EXTRACT_DIR/<stem>.<key>.txt."""
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    key = _cache_key(path)
    cache_file = EXTRACT_DIR / f"{path.stem}.{key}.txt"
    if cache_file.exists():
        return cache_file.read_text(encoding="utf-8"), True
    # remove any stale cache files for this stem (different key)
    for old in EXTRACT_DIR.glob(f"{path.stem}.*.txt"):
        old.unlink()
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text = _pdftotext(path)
    else:
        text = path.read_text(encoding="utf-8", errors="ignore")
    cache_file.write_text(text, encoding="utf-8")
    return text, False


def fidelity(text):
    n = max(len(text), 1)
    cid = text.count("(cid:") / n
    ctrl = sum(1 for c in text if ord(c) < 32 and c not in "\t\n\r\x0c") / n
    if cid > CID_GARBLED or ctrl > CTRL_GARBLED:
        verdict = "garbled"
    elif cid > LOW_TRUST or ctrl > LOW_TRUST:
        verdict = "low"
    else:
        verdict = "ok"
    return {
        "chars": len(text),
        "cid_ratio": round(cid, 5),
        "ctrl_ratio": round(ctrl, 5),
        "verdict": verdict,
    }


def build_report():
    if not DOCS_DIR.exists():
        print("no docs/ dir", file=sys.stderr)
        return {}
    docs = sorted(f for f in DOCS_DIR.iterdir() if f.suffix.lower() in {".pdf", ".txt", ".md"})
    report = {}
    for path in docs:
        text, cached = extract_one(path)
        fid = fidelity(text)
        fid["cached"] = cached
        report[path.name] = fid
        flag = {"ok": "✅", "low": "⚠️ ", "garbled": "❌"}[fid["verdict"]]
        print(f"  {flag} {path.name}: {fid['chars']:>8,} chars  "
              f"cid={fid['cid_ratio']:.4f} ctrl={fid['ctrl_ratio']:.4f}  "
              f"{'(cache)' if cached else '(fresh)'}")
    FIDELITY_OUT.parent.mkdir(parents=True, exist_ok=True)
    FIDELITY_OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    citeable = sum(1 for v in report.values() if v["verdict"] != "garbled")
    print(f"\n  {citeable}/{len(report)} sources citeable (verdict != garbled). "
          f"Report -> {FIDELITY_OUT.relative_to(REPO)}")
    return report


if __name__ == "__main__":
    if "--report" in sys.argv and FIDELITY_OUT.exists():
        print(FIDELITY_OUT.read_text())
    else:
        build_report()

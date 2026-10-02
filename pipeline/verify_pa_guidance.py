#!/usr/bin/env python3
"""
verify_pa_guidance.py — provenance rail for pa-guidance.json (+ its Spanish mirror).

pa-guidance.json uses the content-bundle record shape (guidance[] -> do/dont -> citations), plus a
top-level `notes` map of single cited items. This script runs, for every citation:

  1. verify_citations.verify_citation  — verbatim quote present in the cited docs/ source
                                         (same normalization + length gate as the bundle check)
  2. PAGE CHECK                         — the quote is on the cited PRINTED page. Each PDF page's
                                         printed number is read from its footer (the last line that
                                         ends in a number), so variable offsets (IAPPG) are handled.
                                         Substring matching alone can't catch a wrong page.
  3. guidance_schema.validate_record    — shape + "every actionable item has a citation"
  4. directive_lint.lint_item           — warns when an absolute/numeric word in the item text is
                                         not in its quotes (warning only, needs a human look)
  5. ES mirror check (--es FILE)        — same record ids, same item counts, identical citations
                                         per item (quotes stay English verbatim), text translated.

Usage:
    python3 pipeline/verify_pa_guidance.py pa-guidance.json --es pa-guidance.es.json
    python3 pipeline/verify_pa_guidance.py pa-guidance.json --es pa-guidance.es.json --write-counts
Exit code 0 only if every citation verifies on its page and the ES mirror matches.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_citations import normalize, verify_citation  # noqa: E402
from guidance_schema import validate_record  # noqa: E402
from directive_lint import lint_item  # noqa: E402

REPO = HERE.parent
DOCS = REPO / "docs"

_page_cache = {}


def _pdf_pages(source_file):
    """Return {printed_page_number: normalized_text} for a PDF (reads each page's footer)."""
    if source_file in _page_cache:
        return _page_cache[source_file]
    path = DOCS / source_file
    info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True).stdout
    n = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    pages = {}
    for i in range(1, n + 1):
        txt = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), str(path), "-"],
                             capture_output=True, text=True).stdout
        lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
        printed = None
        for ln in reversed(lines[-4:]):
            m = re.search(r"(\d{1,4})\s*$", ln)
            if m:
                printed = int(m.group(1))
                break
        if printed is None:
            continue
        # keep the first PDF page carrying a given printed number, but join duplicates
        pages[printed] = pages.get(printed, "") + " " + normalize(txt)
    _page_cache[source_file] = pages
    return pages


def page_check(cit):
    page = cit.get("page")
    if page is None:
        return False, "no page given"
    pages = _pdf_pages(cit["source_file"])
    nq = normalize(cit["quote"])
    if nq in pages.get(page, ""):
        return True, "on page"
    found = sorted(p for p, t in pages.items() if nq in t)
    return False, f"not on printed p.{page}; found on {found or 'no single page'}"


def _items(data):
    """Yield (where, item_dict) for every cited item: guidance do/dont + notes."""
    for rec in data.get("guidance", []):
        for sec in ("do", "dont"):
            for i, it in enumerate(rec.get(sec, [])):
                yield f"{rec['id']}.{sec}[{i}]", it
    for k, it in (data.get("notes") or {}).items():
        yield f"notes.{k}", it


def verify(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    total = ok = page_ok = 0
    fails, warns, schema_errs = [], [], []
    for rec in data.get("guidance", []):
        schema_errs += validate_record(rec)
    for where, it in _items(data):
        if not it.get("citations"):
            schema_errs.append(f"{where}: no citation")
        quotes = " ".join(c.get("quote", "") for c in it.get("citations", []))
        for w in lint_item(it.get("text", ""), quotes):
            warns.append(f"{where}: {w}")
        for cit in it.get("citations", []):
            total += 1
            r = verify_citation(cit)
            if r.ok:
                ok += 1
            else:
                fails.append(f"{where}: VERBATIM FAIL ({r.reason}) “{cit.get('quote','')[:70]}”")
                continue
            pok, why = page_check(cit)
            if pok:
                page_ok += 1
            else:
                fails.append(f"{where}: PAGE FAIL ({why}) “{cit['quote'][:70]}”")
    n_items = sum(1 for _ in _items(data))
    print(f"{path}: {ok}/{total} quotes verbatim, {page_ok}/{total} on the cited page, {n_items} items")
    for e in schema_errs:
        print("  SCHEMA:", e)
    for f in fails:
        print("  FAIL:", f)
    for w in warns:
        print("  lint (review):", w)
    return data, total, ok, page_ok, n_items, fails + schema_errs


def mirror_check(en, es):
    errs = []
    en_items = list(_items(en))
    es_items = list(_items(es))
    if [w for w, _ in en_items] != [w for w, _ in es_items]:
        errs.append("ES item structure differs from EN (ids/sections/counts)")
    for (w, a), (_, b) in zip(en_items, es_items):
        if a.get("citations") != b.get("citations"):
            errs.append(f"{w}: ES citations differ from EN")
        if a.get("owners") != b.get("owners"):
            errs.append(f"{w}: ES owners differ from EN")
        if a.get("text") == b.get("text"):
            errs.append(f"{w}: ES text identical to EN (untranslated?)")
    for ra, rb in zip(en.get("guidance", []), es.get("guidance", [])):
        for k in ("id", "owners", "audience"):
            if ra.get(k) != rb.get(k):
                errs.append(f"{ra.get('id')}: ES {k} differs")
    print(f"ES mirror: {'OK' if not errs else str(len(errs)) + ' problem(s)'}")
    for e in errs:
        print("  MIRROR:", e)
    return errs


def main():
    args = sys.argv[1:]
    write = "--write-counts" in args
    es_path = args[args.index("--es") + 1] if "--es" in args else None
    paths = [a for a in args if not a.startswith("--") and a != es_path]
    en_path = paths[0] if paths else str(REPO / "pa-guidance.json")
    en, total, ok, page_ok, n_items, errs = verify(en_path)
    bad = bool(errs) or ok != total or page_ok != total or total == 0
    targets = [(en_path, en)]
    if es_path:
        es, t2, ok2, p2, n2, errs2 = verify(es_path)
        bad = bad or bool(errs2) or bool(mirror_check(en, es))
        targets.append((es_path, es))
    if write and not bad:
        for p, d in targets:
            d["verification"].update(citations_verified=ok, citations_total=total,
                                     pages_verified=page_ok, items=n_items)
            Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("verification counts written")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

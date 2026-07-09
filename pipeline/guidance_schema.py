#!/usr/bin/env python3
"""
guidance_schema.py — the structured shape of a compiled guidance record + a validator.

This is the contract the authoring pipeline emits and the app consumes. Every ACTIONABLE
statement (a do, a dont, the SOI-standard tie-in) must carry >=1 citation, so provenance is
structural, not optional. `validate_record` checks shape AND the citation requirement; it does
NOT check that citations resolve to source text — that's verify_citations.py's job (run both).

A record:
{
  "id": "structural",
  "label": "Structural / Foundation",
  "audience": ["homeowner", "assessor"],
  "summary": "One-paragraph plain-language overview.",
  "do":   [ {"text": "...", "citations": [ {"source_file": "...", "quote": "...", "page": 12} ]} ],
  "dont": [ {"text": "...", "citations": [ ... ]} ],
  "call_a_pro": "optional string",
  "soi_standard": {"text": "...", "citations": [ ... ]},          # optional but recommended
  "severity_notes": {"minor": "...", "moderate": "...", "severe": "..."}   # optional
}
"""
AUDIENCES = {"homeowner", "assessor"}


def _validate_citation(cit, where, errors):
    if not isinstance(cit, dict):
        errors.append(f"{where}: citation is not an object"); return
    if not cit.get("source_file"):
        errors.append(f"{where}: citation missing source_file")
    if not cit.get("quote"):
        errors.append(f"{where}: citation missing quote")


def _validate_item(item, where, errors, require_citation=True):
    if not isinstance(item, dict):
        errors.append(f"{where}: item is not an object"); return
    if not item.get("text"):
        errors.append(f"{where}: missing text")
    cits = item.get("citations", [])
    if require_citation and not cits:
        errors.append(f"{where}: actionable item has NO citation (provenance required)")
    for i, c in enumerate(cits):
        _validate_citation(c, f"{where}.citations[{i}]", errors)


def validate_record(rec):
    """Return a list of error strings ([] == valid)."""
    errors = []
    if not isinstance(rec, dict):
        return ["record is not an object"]
    rid = rec.get("id", "<no-id>")
    # needs_human_authoring stubs (safety-critical categories held back from the runtime bundle)
    # carry only id/label/audience + retrieved passages; no summary/do/dont yet.
    if rec.get("status") == "needs_human_authoring":
        for req in ("id", "label"):
            if not rec.get(req):
                errors.append(f"[{rid}] stub missing required field: {req}")
        return errors
    for req in ("id", "label", "summary"):
        if not rec.get(req):
            errors.append(f"[{rid}] missing required field: {req}")
    aud = rec.get("audience", [])
    if not aud or not isinstance(aud, list) or not set(aud) <= AUDIENCES:
        errors.append(f"[{rid}] audience must be a non-empty subset of {sorted(AUDIENCES)}")
    do, dont = rec.get("do", []), rec.get("dont", [])
    if not do and not dont:
        errors.append(f"[{rid}] record has neither 'do' nor 'dont' items")
    for i, it in enumerate(do):
        _validate_item(it, f"[{rid}].do[{i}]", errors)
    for i, it in enumerate(dont):
        _validate_item(it, f"[{rid}].dont[{i}]", errors)
    if "soi_standard" in rec and rec["soi_standard"]:
        _validate_item(rec["soi_standard"], f"[{rid}].soi_standard", errors)
    return errors


def validate_bundle(bundle):
    records = bundle.get("guidance", []) if isinstance(bundle, dict) else bundle
    all_errors = []
    for rec in records:
        all_errors.extend(validate_record(rec))
    return all_errors


def self_test():
    ok = True
    good = {
        "id": "structural", "label": "Structural / Foundation",
        "audience": ["homeowner", "assessor"], "summary": "Overview.",
        "do": [{"text": "Wait for groundwater to equalize before pumping.",
                "citations": [{"source_file": "nthp-treatment-flood-damaged-historic-buildings.pdf",
                               "quote": "groundwater pressure is high, foundation walls may collapse"}]}],
        "dont": [{"text": "Do not use Portland cement on historic masonry.",
                  "citations": [{"source_file": "x.pdf", "quote": "some verbatim quote here"}]}],
    }
    if validate_record(good):
        print("FAIL: valid record rejected:", validate_record(good)); ok = False
    missing_cit = {**good, "do": [{"text": "Do a thing with no citation.", "citations": []}]}
    if not validate_record(missing_cit):
        print("FAIL: uncited actionable item accepted"); ok = False
    bad_aud = {**good, "audience": ["martians"]}
    if not validate_record(bad_aud):
        print("FAIL: bad audience accepted"); ok = False
    print("SELF-TEST PASS" if ok else "SELF-TEST FAILED")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if self_test() else 2)

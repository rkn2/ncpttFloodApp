#!/usr/bin/env python3
"""
directive_lint.py — deterministic scope-creep detector for guidance items.

Catches the failure mode quote-match can't: a verbatim citation wrapped in an over-claiming
directive. If an item's text uses an ABSOLUTE (always/never/all), a SAFETY verb, or a NUMERIC
threshold, the cited passage must itself contain matching modality — otherwise the directive
claims more than the source licenses. This is a lint (warns), and feeds the human-review flag;
it does not by itself pass/fail a record.
"""
import re

ABSOLUTES = re.compile(r"\b(always|never|all|every|none|must|cannot|guaranteed|completely|entirely)\b", re.I)
SAFETY = re.compile(r"\b(turn off|shut off|de-?energize|enter|evacuate|disconnect|gas|electrocut|"
                    r"asbestos|lead paint|carbon monoxide|collapse|structural failure)\b", re.I)
NUMERIC = re.compile(r"\b\d+(\.\d+)?\s*(%|percent|psi|volt|amp|feet|foot|ft|inch|inches|"
                     r"hours?|days?|degrees?|gallons?|cup|cups)\b", re.I)


def _norm(t):
    return re.sub(r"\s+", " ", t.lower())


def lint_item(text, passage):
    """Return list of scope-warnings for one item given its cited passage text."""
    warns = []
    p = _norm(passage)
    for name, pat in (("absolute", ABSOLUTES), ("safety-directive", SAFETY), ("numeric-threshold", NUMERIC)):
        for m in set(x.group(0).lower() for x in pat.finditer(text)):
            # token(s) of the match should appear in the passage's modality, else it's unlicensed
            key = m.split()[0]
            if key not in p:
                warns.append(f"{name} '{m}' not grounded in cited passage")
    return warns


def lint_record(rec, passage_lookup):
    """passage_lookup(citation)->passage text. Returns {item_text: [warnings]}."""
    out = {}
    for section in ("do", "dont"):
        for it in rec.get(section, []):
            passages = " ".join(passage_lookup(c) or "" for c in it.get("citations", []))
            w = lint_item(it.get("text", ""), passages)
            if w:
                out[it.get("text", "")[:60]] = w
    return out


def self_test():
    ok = True
    # over-claim: "never" not in passage
    w = lint_item("Never use Portland cement on historic masonry.",
                  "Lime-based mortar is softer and protects historic brick.")
    if not w:
        print("FAIL: unlicensed 'never' not flagged"); ok = False
    # grounded: "never" IS in passage
    w2 = lint_item("Never use Portland cement.", "You should never use Portland cement on soft brick.")
    if w2:
        print("FAIL: grounded 'never' wrongly flagged:", w2); ok = False
    print("SELF-TEST PASS" if ok else "SELF-TEST FAILED")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if self_test() else 2)

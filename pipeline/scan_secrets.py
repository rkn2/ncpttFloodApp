#!/usr/bin/env python3
"""
scan_secrets.py — fail the build/commit if a credential-shaped literal is present.

Why: a live Groq key (gsk_...) was committed to this repo's client JS and pushed to a
public GitHub. This guard makes that class of mistake loud and mechanical.

Usage:
    python3 pipeline/scan_secrets.py                 # scan the working tree
    python3 pipeline/scan_secrets.py path/to/file    # scan specific paths
    python3 pipeline/scan_secrets.py --self-test     # verify the scanner itself

Exit code 0 = clean, 1 = secret(s) found, 2 = self-test failed.

Install as a git pre-commit hook:
    ln -sf ../../pipeline/scan_secrets.py .git/hooks/pre-commit   # (or call it from one)
"""
import re
import sys
from pathlib import Path

# (name, compiled pattern). Patterns target *shaped* credentials, not the word "key".
PATTERNS = [
    ("Groq API key",        re.compile(r"gsk_[A-Za-z0-9]{20,}")),
    ("OpenAI API key",      re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("Anthropic API key",   re.compile(r"sk-ant-[A-Za-z0-9\-]{20,}")),
    ("AWS access key id",   re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Google API key",      re.compile(r"AIza[0-9A-Za-z\-_]{35}")),
    ("Slack token",         re.compile(r"xox[baprs]-[0-9A-Za-z\-]{10,}")),
    ("Generic bearer/PEM",  re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----")),
]

# Directories never worth scanning.
SKIP_DIRS = {".git", "node_modules", "overnight", "__pycache__", ".dual-graph"}
# Extensions that are binary / source PDFs / build artifacts — skip to avoid false positives.
SKIP_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".docx", ".doc", ".zip",
            ".woff", ".woff2", ".ttf", ".ico", ".DS_Store"}
# knowledge-base.json is a large generated artifact of source text — scan it anyway (cheap enough)
# but allow opting out via size guard.
MAX_BYTES = 20 * 1024 * 1024


def iter_files(roots):
    for root in roots:
        p = Path(root)
        if p.is_file():
            yield p
            continue
        for f in p.rglob("*"):
            if not f.is_file():
                continue
            if any(part in SKIP_DIRS for part in f.parts):
                continue
            if f.suffix in SKIP_EXT:
                continue
            # don't scan this scanner (it contains the patterns) or its own docs
            if f.name == "scan_secrets.py":
                continue
            try:
                if f.stat().st_size > MAX_BYTES:
                    continue
            except OSError:
                continue
            yield f


def scan_text(text):
    """Return list of (secret_name, matched_snippet)."""
    hits = []
    for name, pat in PATTERNS:
        for m in pat.finditer(text):
            snippet = m.group(0)
            redacted = snippet[:6] + "…" + snippet[-3:]
            hits.append((name, redacted))
    return hits


def scan_paths(roots):
    findings = []
    for f in iter_files(roots):
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, redacted in scan_text(text):
            findings.append((str(f), name, redacted))
    return findings


def self_test():
    ok = True
    planted = "const K = 'gsk_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';"
    if not scan_text(planted):
        print("SELF-TEST FAIL: did not catch a planted gsk_ key"); ok = False
    clean = "function getGroqKey() { return localStorage.getItem(LS_GROQ_KEY) || ''; }"
    if scan_text(clean):
        print("SELF-TEST FAIL: false positive on clean localStorage code"); ok = False
    if scan_text("the api key is user-supplied"):
        print("SELF-TEST FAIL: false positive on the words 'api key'"); ok = False
    print("SELF-TEST PASS" if ok else "SELF-TEST FAILED")
    return ok


def main(argv):
    if "--self-test" in argv:
        sys.exit(0 if self_test() else 2)
    roots = [a for a in argv[1:] if not a.startswith("-")] or ["."]
    findings = scan_paths(roots)
    if findings:
        print(f"❌ {len(findings)} potential secret(s) found:")
        for path, name, redacted in findings:
            print(f"   {path}: {name} ({redacted})")
        print("\nRemove the secret and (if it was ever committed/pushed) REVOKE it at the provider.")
        sys.exit(1)
    print("✅ No credential-shaped literals found.")
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)

#!/usr/bin/env python3
"""
retrieve.py — per-topic passage retrieval (BM25) over the knowledge base.

Feeds the synthesis step: given a guidance topic query, return the top-k source passages an
author (human or LLM subagent) may quote from. Reuses knowledge-base.json's chunks + IDF table
so retrieval is consistent with what the app itself searches at runtime.

Usage:
    python3 pipeline/retrieve.py "repoint historic masonry lime mortar" [k]
Importable:
    from retrieve import retrieve  ->  [{source, text, score, chunk_index}]
"""
import json
import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
KB_PATH = REPO / "knowledge-base.json"

K1, B = 1.5, 0.75
_index = None
_avgdl = 150.0
_idf = {}


def _tokenize(text):
    return [t for t in re.sub(r"[^a-z0-9\s]", " ", text.lower()).split() if len(t) > 2]


def _build_index():
    global _index, _avgdl, _idf
    kb = json.loads(KB_PATH.read_text())
    _idf = kb.get("idf", {})
    _avgdl = kb.get("avg_chunk_len", 150.0)
    _index = []
    for c in kb["chunks"]:
        toks = _tokenize(c["text"])
        tf = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        _index.append((c, tf, len(toks)))
    return _index


def retrieve(query, k=6, source=None):
    """Top-k passages for query. Optional source= restricts to one document."""
    if _index is None:
        _build_index()
    q = set(_tokenize(query))
    scored = []
    for c, tf, ln in _index:
        if source and c.get("source") != source:
            continue
        s = 0.0
        for t in q:
            f = tf.get(t, 0)
            if not f:
                continue
            idf = _idf.get(t, math.log(2))
            s += idf * (f * (K1 + 1)) / (f + K1 * (1 - B + B * ln / _avgdl))
        if s > 0:
            scored.append({"source": c.get("source"), "text": c["text"],
                           "score": round(s, 3), "chunk_index": c.get("chunk_index")})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        print(__doc__); sys.exit(0)
    query = args[0]
    k = int(args[1]) if len(args) > 1 else 6
    for r in retrieve(query, k):
        print(f"[{r['score']:.2f}] {r['source']} #{r['chunk_index']}")
        print("   " + r["text"][:200].replace("\n", " ") + "…\n")

#!/usr/bin/env python3
"""
build-kb.py — Build the knowledge base for the Historic Flood Recovery Tool chatbot.

Usage:
    pip install pdfplumber python-docx
    python build-kb.py

Reads all .pdf, .txt, .docx, .md files from docs/,
chunks them, and writes knowledge-base.json.

Re-run this script whenever you add or update documents in docs/.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

DOCS_DIR   = Path('docs')
OUTPUT     = Path('knowledge-base.json')
CHUNK_SIZE = 800   # characters
OVERLAP    = 150   # characters of overlap between chunks


def extract_pdf(path):
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return '\n'.join(page.extract_text() or '' for page in pdf.pages)
    except ImportError:
        print(f"  [skip] pdfplumber not installed — run: pip install pdfplumber")
        return ''
    except Exception as e:
        print(f"  [error] {path.name}: {e}")
        return ''


def extract_docx(path):
    try:
        from docx import Document
        return '\n'.join(p.text for p in Document(path).paragraphs)
    except ImportError:
        print(f"  [skip] python-docx not installed — run: pip install python-docx")
        return ''
    except Exception as e:
        print(f"  [error] {path.name}: {e}")
        return ''


def extract_text(path):
    return path.read_text(encoding='utf-8', errors='ignore')


def chunk(text):
    chunks, start = [], 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        if end < len(text):
            for sep in ['. ', '.\n', '\n\n', '\n']:
                idx = text.rfind(sep, start + CHUNK_SIZE // 2, end)
                if idx != -1:
                    end = idx + len(sep)
                    break
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        start = end - OVERLAP
    return chunks


def main():
    if not DOCS_DIR.exists():
        DOCS_DIR.mkdir()
        print(f"Created {DOCS_DIR}/  — add your grant documents (.pdf, .txt, .docx) there, then re-run.")
        sys.exit(0)

    docs = sorted(f for f in DOCS_DIR.iterdir() if f.suffix.lower() in {'.pdf', '.txt', '.docx', '.md'})

    if not docs:
        print(f"No documents found in {DOCS_DIR}/. Add .pdf, .txt, or .docx files and re-run.")
        sys.exit(0)

    chunks = []
    for path in docs:
        print(f"  {path.name} ...", end=' ', flush=True)
        suffix = path.suffix.lower()
        if suffix == '.pdf':
            text = extract_pdf(path)
        elif suffix == '.docx':
            text = extract_docx(path)
        else:
            text = extract_text(path)

        if not text.strip():
            print("no text extracted")
            continue

        file_chunks = chunk(text)
        for i, c in enumerate(file_chunks):
            chunks.append({'id': f"{path.stem}-{i}", 'source': path.name, 'chunk_index': i, 'text': c})
        print(f"{len(file_chunks)} chunks")

    kb = {
        'built_at':    datetime.now().isoformat(),
        'doc_count':   len(docs),
        'chunk_count': len(chunks),
        'chunks':      chunks,
    }
    OUTPUT.write_text(json.dumps(kb, indent=2, ensure_ascii=False))
    print(f"\nWrote {OUTPUT}  ({len(chunks)} chunks from {len(docs)} documents)")


if __name__ == '__main__':
    main()

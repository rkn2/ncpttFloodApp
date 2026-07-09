#!/usr/bin/env python3
"""
build-kb.py — Build the knowledge base for the Historic Flood Recovery Tool chatbot.

Usage:
    brew install poppler tesseract   # provides pdftotext + OCR engine
    pip install python-docx pytesseract pdf2image
    python build-kb.py

Reads all .pdf, .txt, .docx, .md files from docs/,
chunks them, and writes knowledge-base.json.

Re-run this script whenever you add or update documents in docs/.
"""

import json
import math
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DOCS_DIR        = Path('docs')
OUTPUT          = Path('knowledge-base.json')
CHUNK_SIZE      = 800   # characters
OVERLAP         = 150   # characters of overlap between chunks
CID_THRESHOLD   = 0.03  # fraction of (cid:…) sequences that triggers OCR fallback


def _pdftotext(path, first_page=None, last_page=None):
    cmd = ['pdftotext']
    if first_page is not None:
        cmd += ['-f', str(first_page)]
    if last_page is not None:
        cmd += ['-l', str(last_page)]
    cmd += [str(path), '-']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except FileNotFoundError:
        print(f"\n  [skip] pdftotext not found — run: brew install poppler", end='')
        return ''
    except subprocess.CalledProcessError as e:
        print(f"\n  [error] pdftotext: {e.stderr.strip()}", end='')
        return ''


def _pdf_page_count(path):
    try:
        result = subprocess.run(['pdfinfo', str(path)], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if line.startswith('Pages:'):
                return int(line.split(':')[1].strip())
    except Exception:
        pass
    return 0


def _is_garbled(text):
    if not text or not text.strip():
        return True
    n = len(text)
    if text.count('(cid:') / n > CID_THRESHOLD:
        return True
    # \x0c is pdftotext's page-separator — exclude it; other control chars signal garbled font
    ctrl = sum(1 for c in text if ord(c) < 32 and c not in '\t\n\r\x0c')
    return ctrl / n > CID_THRESHOLD


def _ocr_page(path, page_num):
    try:
        from pdf2image import convert_from_path
        import pytesseract
        images = convert_from_path(str(path), dpi=300, first_page=page_num, last_page=page_num)
        return pytesseract.image_to_string(images[0]) if images else ''
    except ImportError as e:
        print(f"\n  [skip OCR] {e} — pip install pytesseract pdf2image", end='')
        return ''


def extract_pdf(path):
    page_count = _pdf_page_count(path)
    if page_count == 0:
        return _pdftotext(path)

    pages_text, ocr_count = [], 0
    for i in range(1, page_count + 1):
        text = _pdftotext(path, first_page=i, last_page=i)
        if _is_garbled(text):
            text = _ocr_page(path, i)
            ocr_count += 1
        pages_text.append(text)

    if ocr_count:
        print(f"(OCR: {ocr_count}/{page_count} pages)", end=' ', flush=True)
    return '\n\n'.join(pages_text)


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


def tokenize(text):
    return [t for t in re.sub(r'[^a-z0-9\s]', ' ', text.lower()).split() if len(t) > 2]


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
        if end >= len(text):
            break
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

    # Build BM25 IDF table
    N = len(chunks)
    idf, avg_chunk_len = {}, 0
    if N > 0:
        df = {}
        lens = []
        for c in chunks:
            toks = tokenize(c['text'])
            lens.append(len(toks))
            for t in set(toks):
                df[t] = df.get(t, 0) + 1
        idf = {t: round(math.log((N - freq + 0.5) / (freq + 0.5) + 1), 4)
               for t, freq in df.items()}
        avg_chunk_len = round(sum(lens) / len(lens), 1)

    kb = {
        'built_at':      datetime.now().isoformat(),
        'doc_count':     len(docs),
        'chunk_count':   len(chunks),
        'avg_chunk_len': avg_chunk_len,
        'idf':           idf,
        'chunks':        chunks,
    }
    OUTPUT.write_text(json.dumps(kb, indent=2, ensure_ascii=False))
    print(f"\nWrote {OUTPUT}  ({len(chunks)} chunks from {len(docs)} documents, {len(idf)} IDF terms)")


if __name__ == '__main__':
    main()

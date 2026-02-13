#!/usr/bin/env python3
"""
read_docx.py — Extract text content from a .docx file.

Usage: python3 scripts/read_docx.py <filepath>

Outputs the full text content of the document, preserving paragraph breaks.
Used by the skill to read brand research dossiers from GitHub.
"""

import sys

def read_docx(filepath: str) -> str:
    try:
        from docx import Document
    except ImportError:
        import subprocess
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "python-docx", "--break-system-packages", "-q"
        ])
        from docx import Document

    doc = Document(filepath)
    text_parts = []
    for para in doc.paragraphs:
        text_parts.append(para.text)
    return "\n".join(text_parts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 read_docx.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    print(read_docx(filepath))

#!/usr/bin/env python3
"""
extract_profile.py — PDF Resume Text Extractor

Extracts plain text from existing PDF CVs dropped into `my_profile/old_cv/`.
Enables AI agents to read the text and scaffold `my_profile/candidate_profile.md` automatically.
"""

import sys
import os
import glob
import subprocess

# Ensure safe console output across all platforms
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def extract_with_pypdf(pdf_path):
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        text = []
        for i, page in enumerate(reader.pages):
            text.append(f"--- [Page {i+1}] ---\n" + (page.extract_text() or ""))
        return "\n".join(text)
    except ImportError:
        return None

def extract_with_pdfplumber(pdf_path):
    try:
        import pdfplumber
        text = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text.append(f"--- [Page {i+1}] ---\n" + (page.extract_text() or ""))
        return "\n".join(text)
    except ImportError:
        return None

def extract_with_pdftotext(pdf_path):
    import shutil
    if shutil.which("pdftotext"):
        try:
            res = subprocess.run(["pdftotext", pdf_path, "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return res.stdout
        except Exception:
            pass
    return None

def extract_text_from_pdf(pdf_path):
    # Try pypdf first
    txt = extract_with_pypdf(pdf_path)
    if txt:
        return txt

    # Try pdfplumber
    txt = extract_with_pdfplumber(pdf_path)
    if txt:
        return txt

    # Try system pdftotext
    txt = extract_with_pdftotext(pdf_path)
    if txt:
        return txt

    return None

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    old_cv_dir = os.path.join(repo_root, "my_profile", "old_cv")
    
    if len(sys.argv) > 1:
        target_files = [sys.argv[1]]
    else:
        target_files = glob.glob(os.path.join(old_cv_dir, "*.pdf"))

    if not target_files:
        print(f"[!] No PDF resumes found in: {old_cv_dir}")
        print("    Drop your old CV (e.g., 'resume.pdf') into 'my_profile/old_cv/' and re-run.")
        sys.exit(1)

    for pdf in target_files:
        print(f"[*] Processing: {os.path.basename(pdf)}")
        text = extract_text_from_pdf(pdf)
        if text:
            print("\n" + "="*70)
            print(f" EXTRACTED TEXT FROM: {os.path.basename(pdf)}")
            print("="*70)
            print(text)
            print("="*70 + "\n")
            out_txt = os.path.splitext(pdf)[0] + "_extracted.txt"
            with open(out_txt, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[✓] Saved extracted text to: {out_txt}")
        else:
            print(f"[!] Could not extract text from {pdf}.")
            print("    To enable Python PDF extraction, install pypdf:")
            print("    pip install pypdf")
            sys.exit(1)

if __name__ == "__main__":
    main()

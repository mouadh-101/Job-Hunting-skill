#!/usr/bin/env python3
"""
compile_latex.py — LaTeX Compilation and ATS Single-Page Validator

Compiles .tex files into clean PDFs, automatically cleans auxiliary files (.aux, .log, .out),
and validates that the generated CV or cover letter satisfies the strict 1-page ATS budget.
"""

import sys
import os
import shutil
import subprocess
import re

# Ensure safe console output across all platforms
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def count_pdf_pages(pdf_path):
    """Estimate or count pages in a PDF file without external heavy dependencies."""
    try:
        with open(pdf_path, 'rb') as f:
            content = f.read()
        # Look for /Type /Pages /Count N
        count_match = re.search(rb"/Type\s*/Pages.*?/Count\s+(\d+)", content, re.DOTALL)
        if count_match:
            return int(count_match.group(1))
        # Fallback to counting /Type /Page objects (excluding /Pages)
        matches = re.findall(rb"/Type\s*/Page[^s]", content)
        if matches:
            return len(matches)
    except Exception:
        pass
    return None

def compile_document(tex_path):
    if not os.path.exists(tex_path):
        print(f"[!] Error: File '{tex_path}' not found.")
        return False

    abs_tex = os.path.abspath(tex_path)
    work_dir = os.path.dirname(abs_tex)
    filename = os.path.basename(abs_tex)
    basename = os.path.splitext(filename)[0]
    pdf_file = os.path.join(work_dir, f"{basename}.pdf")

    # Detect compiler
    compiler = None
    if shutil.which("pdflatex"):
        compiler = "pdflatex"
    elif shutil.which("tectonic"):
        compiler = "tectonic"
    elif shutil.which("xelatex"):
        compiler = "xelatex"

    if not compiler:
        print("[!] No LaTeX compiler found on your system.")
        tools_dir = os.path.dirname(os.path.abspath(__file__))
        setup_script = os.path.join(tools_dir, "setup_latex.py")
        if os.path.exists(setup_script):
            subprocess.run([sys.executable, setup_script], check=False)
        return False

    print(f"[*] Compiling '{filename}' using {compiler}...")

    try:
        if compiler == "pdflatex":
            cmd = ["pdflatex", "-interaction=nonstopmode", filename]
            # Run twice to ensure cross-references and geometry calculate correctly
            subprocess.run(cmd, cwd=work_dir, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
            subprocess.run(cmd, cwd=work_dir, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
        elif compiler == "tectonic":
            cmd = ["tectonic", filename]
            subprocess.run(cmd, cwd=work_dir, check=True)
        elif compiler == "xelatex":
            cmd = ["xelatex", "-interaction=nonstopmode", filename]
            subprocess.run(cmd, cwd=work_dir, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

        print(f"[✓] Successfully generated: {pdf_file}")

        # Clean auxiliary files
        for ext in [".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk"]:
            aux_path = os.path.join(work_dir, f"{basename}{ext}")
            if os.path.exists(aux_path):
                try:
                    os.remove(aux_path)
                except OSError:
                    pass

        # Page Count Verification
        pages = count_pdf_pages(pdf_file)
        if pages is not None:
            if pages == 1:
                print(f"[✓] Page Budget Check PASSED: Exactly 1 page ({pages} page).")
            else:
                print(f"[⚠️ WARNING] Document is {pages} pages long!")
                print("    Modern ATS and recruiters require a STRICT 1-PAGE budget.")
                print("    Recommendation: Adjust \\vspace or condense 1-2 bullet points.")

        return True

    except subprocess.CalledProcessError as e:
        print(f"[!] Compilation failed. Check syntax in '{tex_path}'.")
        log_file = os.path.join(work_dir, f"{basename}.log")
        if os.path.exists(log_file):
            print(f"[*] Inspecting log file '{log_file}' for errors:")
            with open(log_file, "r", encoding="latin-1", errors="ignore") as f:
                lines = f.readlines()
                errors = [line.strip() for line in lines if line.startswith("!") or "Error" in line]
                for err in errors[:5]:
                    print(f"    {err}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python compile_latex.py <path_to_tex_file>")
        sys.exit(1)

    tex_file = sys.argv[1]
    success = compile_document(tex_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

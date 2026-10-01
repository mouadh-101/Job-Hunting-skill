#!/usr/bin/env python3
"""
setup_latex.py — Automated LaTeX Environment Detector and Installer

Checks for an existing LaTeX compiler (pdflatex, tectonic, xelatex).
If missing:
- Attempts automated installation if the platform allows it (winget/choco on Windows, apt/dnf on Linux, brew on macOS).
- If installation requires elevated rights or the platform does not allow it (e.g. restricted container or cloud sandbox),
  it informs the user with exact commands, Docker one-liners, and web compiler alternatives.
"""

import sys
import shutil
import subprocess
import platform
import os

# Ensure safe console output across all platforms (including Windows cp1252)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def check_latex_installed():
    compilers = ["pdflatex", "tectonic", "xelatex", "lualatex"]
    for comp in compilers:
        path = shutil.which(comp)
        if path:
            return comp, path
    return None, None

def check_docker():
    return shutil.which("docker") is not None

def print_manual_instructions(system):
    print("\n" + "="*70)
    print(" ℹ️  HOW TO GET LATEX FOR ZERO-ERROR PDF COMPILATION")
    print("="*70)
    
    if system == "Windows":
        print("""
Option 1: Windows Package Manager (Recommended)
  Open PowerShell as Administrator and run:
    winget install MiKTeX.MiKTeX
  or (super lightweight compiler):
    winget install Tectonic.Tectonic

Option 2: Chocolatey
    choco install miktex
""")
    elif system == "Darwin":
        print("""
Option 1: Homebrew (macOS)
    brew install --cask mactex-no-gui
  or (super lightweight compiler):
    brew install tectonic
""")
    else:  # Linux
        print("""
Option 1: Debian / Ubuntu
    sudo apt-get update
    sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra
  or (super lightweight compiler):
    sudo apt-get install -y tectonic

Option 2: Fedora / RHEL
    sudo dnf install texlive-scheme-medium
""")

    print("""Option 2: Docker (Zero-install if Docker is installed)
    docker run --rm -v "${PWD}:/data" dxjoke/tectonic tectonic document.tex

Option 3: Free Web Compilers (No installation needed)
  If your platform or corporate environment does not allow installing software:
  1. Open https://www.overleaf.com/ (Free, instant LaTeX compiler)
  2. Create a 'Blank Project' and paste the generated .tex file content.
  3. Click 'Recompile' and download your ATS PDF in 5 seconds!
""")
    print("="*70 + "\n")

def try_auto_install(system):
    print(f"[*] Attempting automated installation on {system}...")

    if system == "Windows":
        if shutil.which("winget"):
            print("[*] Found 'winget'. Installing Tectonic (lightweight LaTeX compiler)...")
            cmd = ["winget", "install", "--id", "Tectonic.Tectonic", "-e", "--accept-source-agreements", "--accept-package-agreements"]
            try:
                res = subprocess.run(cmd, check=False)
                if res.returncode == 0:
                    print("[✓] Tectonic installed successfully! Please restart your terminal if not found in PATH.")
                    return True
            except Exception as e:
                print(f"[!] Winget installation encountered: {e}")

        if shutil.which("choco"):
            print("[*] Found 'choco'. Attempting MiKTeX installation...")
            try:
                res = subprocess.run(["choco", "install", "miktex", "-y"], check=False)
                if res.returncode == 0:
                    print("[✓] MiKTeX installed successfully!")
                    return True
            except Exception as e:
                print(f"[!] Choco installation encountered: {e}")

    elif system == "Darwin":
        if shutil.which("brew"):
            print("[*] Found 'brew'. Installing tectonic...")
            try:
                res = subprocess.run(["brew", "install", "tectonic"], check=False)
                if res.returncode == 0:
                    print("[✓] Tectonic installed successfully!")
                    return True
            except Exception as e:
                print(f"[!] Brew installation encountered: {e}")

    elif system == "Linux":
        if shutil.which("apt-get"):
            print("[*] Attempting apt-get install (may require sudo privileges)...")
            try:
                cmd = ["apt-get", "install", "-y", "tectonic"]
                if os.geteuid() != 0:
                    cmd = ["sudo"] + cmd
                res = subprocess.run(cmd, check=False)
                if res.returncode == 0:
                    print("[✓] Tectonic installed successfully!")
                    return True
            except Exception as e:
                print(f"[!] Apt installation encountered: {e}")

    return False

def main():
    auto_install = "--auto-install" in sys.argv
    compiler, path = check_latex_installed()
    
    if compiler:
        print(f"[✓] LaTeX compiler found: {compiler} ({path})")
        return 0

    print("[!] No local LaTeX compiler (pdflatex, tectonic, xelatex) detected.")
    system = platform.system()
    
    installed = False
    if auto_install:
        installed = try_auto_install(system)
        if installed:
            compiler, path = check_latex_installed()
            if compiler:
                print(f"[✓] Verification succeeded: {compiler} is ready.")
                return 0

    print_manual_instructions(system)
    return 1

if __name__ == "__main__":
    sys.exit(main())

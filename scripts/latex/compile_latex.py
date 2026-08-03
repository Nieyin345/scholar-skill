#!/usr/bin/env python3
"""Compile a .tex file to PDF using a local LaTeX engine (cross-platform).

Usage:
    python compile_latex.py <input.tex> [--engine pdflatex|xelatex|lualatex|tectonic]
                             [--latexmk] [--output-dir DIR] [--verbose]

Behaviour:
  - Engine auto-detection: reads the .tex for ctex/xeCJK/fontspec -> xelatex,
    otherwise falls back to detect_engine.py's default.
  - Runs multiple passes (and bibtex when a .bib file is referenced).
  - Parses the .log for errors/warnings and prints a JSON summary.
  - Exits 0 when the PDF was produced, 1 otherwise.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DETECT = os.path.join(SCRIPT_DIR, "detect_engine.py")

ERROR_MARKS = [
    "LaTeX Error",
    "! LaTeX Error",
    "Undefined control sequence",
    "Undefined reference",
    "Citation '",          # undefined citation
    "Runaway argument",
    "Missing $",
    "Extra alignment tab",
    "Emergency stop",
]
WARNING_MARKS = [
    "Overfull",
    "Underfull",
    "There were undefined references",
    "undefined references",
    "Citation .* undefined",
    "multiply defined",
    "Float too large",
    "Package .* Warning",
    "Font shape .* undefined",
]


def detect_engine(preferred):
    try:
        out = subprocess.run(
            [sys.executable, DETECT, "--quiet"],
            capture_output=True, text=True, timeout=20,
        )
        available = out.stdout.strip().split(" | ") if out.returncode == 0 else []
    except Exception:
        available = []
    if preferred and preferred in available:
        return preferred
    if "xelatex" in available:
        return "xelatex"
    return available[0] if available else None


def guess_engine_from_source(tex_path):
    try:
        with open(tex_path, "r", encoding="utf-8", errors="ignore") as fh:
            head = fh.read(4000)
    except OSError:
        return None
    if any(mark in head for mark in ("\\usepackage{ctex}", "xeCJK", "\\usepackage{fontspec}")):
        return "xelatex"
    return None


def find_bib(tex_path):
    try:
        with open(tex_path, "r", encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
    except OSError:
        return None
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("\\bibliography{") or line.startswith("\\addbibresource{"):
            base = line.split("{", 1)[1].rsplit("}", 1)[0].split(",")[0].strip()
            return base + ".bib"
    return None


def collect_issues(log_path):
    errors, warnings = [], []
    if not log_path or not os.path.exists(log_path):
        return errors, warnings
    with open(log_path, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            line = line.rstrip()
            if not line.strip():
                continue
            if line.startswith("! ") or any(m in line for m in ERROR_MARKS):
                errors.append(line.strip()[:300])
            elif any(m in line for m in WARNING_MARKS):
                warnings.append(line.strip()[:300])
    # de-duplicate preserving order
    seen = set()
    errors = [e for e in errors if not (e in seen or seen.add(e))]
    seen = set()
    warnings = [w for w in warnings if not (w in seen or seen.add(w))]
    return errors[:40], warnings[:40]


def main():
    parser = argparse.ArgumentParser(description="Compile LaTeX to PDF")
    parser.add_argument("tex", help="path to input .tex file")
    parser.add_argument("--engine", default=None, help="pdflatex|xelatex|lualatex|tectonic")
    parser.add_argument("--latexmk", action="store_true", help="use latexmk backend")
    parser.add_argument("--output-dir", default=None, help="output directory (default: tex dir)")
    parser.add_argument("--verbose", action="store_true", help="show full compile output")
    args = parser.parse_args()

    tex_path = os.path.abspath(args.tex)
    if not os.path.exists(tex_path):
        print(json.dumps({"success": False, "error": "tex file not found: " + tex_path}))
        sys.exit(1)

    work_dir = os.path.dirname(tex_path)
    out_dir = os.path.abspath(args.output_dir) if args.output_dir else work_dir
    os.makedirs(out_dir, exist_ok=True)

    src_engine = guess_engine_from_source(tex_path)
    engine = detect_engine(args.engine or src_engine)
    if not engine:
        print(json.dumps({
            "success": False,
            "error": "no LaTeX engine found; install TeX Live or MiKTeX",
            "hint": "https://tug.org/texlive/ or https://miktex.org/",
        }))
        sys.exit(1)

    base = os.path.splitext(os.path.basename(tex_path))[0]
    log_path = os.path.join(out_dir, base + ".log")
    pdf_path = os.path.join(out_dir, base + ".pdf")

    def run(cmd):
        if args.verbose:
            subprocess.run(cmd, cwd=out_dir, check=False)
        else:
            subprocess.run(cmd, cwd=out_dir, capture_output=True, text=True, check=False)

    if args.latexmk and shutil.which("latexmk"):
        latexmk_cmd = ["latexmk", "-pdf", "-interaction=nonstopmode"]
        if engine == "xelatex":
            latexmk_cmd.append("-xelatex")
        elif engine == "lualatex":
            latexmk_cmd.append("-lualatex")
        latexmk_cmd.append(os.path.basename(tex_path))
        run(latexmk_cmd)
    else:
        run([engine, "-interaction=nonstopmode", os.path.basename(tex_path)])
        bib = find_bib(tex_path)
        if bib and shutil.which("bibtex"):
            run(["bibtex", base])
        run([engine, "-interaction=nonstopmode", os.path.basename(tex_path)])
        run([engine, "-interaction=nonstopmode", os.path.basename(tex_path)])

    errors, warnings = collect_issues(log_path)
    success = os.path.exists(pdf_path)
    result = {
        "success": success,
        "engine": engine,
        "pdf": pdf_path if success else None,
        "log": log_path if os.path.exists(log_path) else None,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

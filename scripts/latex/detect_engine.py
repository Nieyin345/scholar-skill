#!/usr/bin/env python3
"""Detect local LaTeX engines on PATH (cross-platform).

Usage:
    python detect_engine.py            # JSON summary
    python detect_engine.py --quiet    # plain text

Exits 0 if at least one engine is available, 1 otherwise.
"""
import json
import os
import shutil
import subprocess
import sys

ENGINES = ["pdflatex", "xelatex", "lualatex", "tectonic"]
HELPERS = ["latexmk", "bibtex", "biber"]


def _run_version(cmd):
    try:
        out = subprocess.run(
            [cmd, "--version"], capture_output=True, text=True, timeout=15
        )
        line = (out.stdout or out.stderr).splitlines()
        return line[0].strip() if line else "found"
    except Exception:
        return None


def detect():
    found = {}
    for name in ENGINES + HELPERS:
        exe = shutil.which(name)
        if exe:
            version = _run_version(name)
            found[name] = {"path": exe, "version": version}
    return found


def main():
    quiet = "--quiet" in sys.argv
    result = detect()
    engines = [e for e in ENGINES if e in result]
    latexmk = "latexmk" in result

    if quiet:
        if engines:
            print(" | ".join(engines))
        else:
            print("none")
        sys.exit(0 if engines else 1)

    payload = {
        "engines": engines,
        "latexmk": latexmk,
        "helpers": [h for h in HELPERS if h in result],
        "details": result,
        "default_engine": "xelatex" if "xelatex" in engines else (engines[0] if engines else None),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(0 if engines else 1)


if __name__ == "__main__":
    main()

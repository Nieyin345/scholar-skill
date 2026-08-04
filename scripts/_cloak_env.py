#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CloakBrowser 依赖解释器探测（institutional_login / institutional_download 共用）。

cloakbrowser 包可能只装在某个 Python 解释器里（例如 C:\\Python313\\python.exe），
而脚本被调用的默认解释器不一定有它。本模块负责自动探测「能 import cloakbrowser
的解释器」，避免出现误导性的「请先安装 cloakbrowser」报错。
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CLOAK_HINT = """未找到能 import cloakbrowser 的 Python 解释器（已探测: {tried}）。
解决方式（任选其一）：
  1) 设置环境变量指向已装 cloakbrowser 的解释器（推荐，脚本会自动使用）：
       PowerShell:  $env:CLOAKBROWSER_PYTHON = 'C:\\Python313\\python.exe'
       CMD:         set CLOAKBROWSER_PYTHON=C:\\Python313\\python.exe
  2) 直接用该解释器运行本脚本，例如：
       & 'C:\\Python313\\python.exe' scripts\\institutional_download.py --dois <清单> --out <目录> [--headful]
  3) 在任意 Python 上安装依赖后再试：
       python -m pip install -U cloakbrowser
"""


def _candidate_pythons() -> list[str]:
    """按优先级收集候选解释器（去重）。"""
    cands: list[str] = []
    env = os.environ.get("CLOAKBROWSER_PYTHON", "").strip()
    if env:
        cands.append(env)
    for ver in ("313", "312", "311", "310", "39"):
        p = rf"C:\Python{ver}\python.exe"
        if os.path.isfile(p):
            cands.append(p)
    try:
        r = subprocess.run(["py", "-0p"], capture_output=True, text=True, timeout=15)
        for line in r.stdout.splitlines():
            m = re.search(r"([A-Za-z]:\\[^\s]+python\.exe)", line)
            if m:
                cands.append(m.group(1).rstrip("*").strip())
    except Exception:
        pass
    for name in ("python", "python3", "python.exe"):
        w = shutil.which(name)
        if w:
            cands.append(w)
    cands.append(sys.executable)
    seen: set[str] = set()
    out: list[str] = []
    for c in cands:
        if not c:
            continue
        try:
            key = os.path.normcase(os.path.realpath(c))
        except Exception:
            key = os.path.normcase(c)
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def resolve_cloak_python() -> tuple[str | None, list[str]]:
    """返回 (能 import cloakbrowser 的解释器 | None, 已探测过的候选列表)。"""
    tried: list[str] = []
    for c in _candidate_pythons():
        if not (os.path.isfile(c) or shutil.which(c)):
            continue
        tried.append(c)
        try:
            r = subprocess.run(
                [c, "-c", "import cloakbrowser"],
                capture_output=True,
                timeout=20,
            )
            if r.returncode == 0:
                return c, tried
        except Exception:
            continue
    return None, tried

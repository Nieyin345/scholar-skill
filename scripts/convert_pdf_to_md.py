#!/usr/bin/env python3
"""PDF -> Markdown 转换（MinerU Open API CLI 封装）。

使用 MinerU Open API CLI 将 PDF 转换为 Markdown。
CLI 安装方式（跟随本 skill 一起下载）：
  - 内置安装脚本：scripts/mineru/install.ps1（Windows 官方安装器）
  - 或在线安装：irm https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1 | iex

两种转换模式：
  - flash （默认，免认证）：mineru-open-api flash-extract，快速 Markdown 提取；
    限制：文件 <= 10MB 且 <= 20 页；Markdown only（图片/表格/公式为占位）。
  - extract（需认证）：mineru-open-api extract，精提取（布局保留 + 全部资产），
    需先执行 mineru-open-api auth 配置 API Token。

用法：
  python convert_pdf_to_md.py <pdf路径> --out <输出文件夹> [--mode flash|extract] [--language en] [--timeout 300]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
BUNDLED_INSTALLER = SKILL_DIR / "scripts" / "mineru" / "install.ps1"


def _default_bin() -> str:
    candidates = []
    env_bin = os.environ.get("MINERU_BIN", "").strip()
    if env_bin:
        candidates.append(env_bin)
    home = str(Path.home())
    candidates.append(str(Path(home) / ".mineru" / "bin" / "mineru-open-api.exe"))
    which = shutil.which("mineru-open-api")
    if which:
        candidates.append(which)
    for c in candidates:
        if c and Path(c).exists():
            return c
    return candidates[0] if candidates else "mineru-open-api"


def _env_value(key: str) -> str:
    env_file = SKILL_DIR / ".env"
    if not env_file.exists():
        return ""
    for line in env_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line.startswith(key + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def ensure_bin(bin_path: str) -> str:
    """确保 mineru-open-api 可用；缺失时尝试用打包的安装脚本安装。"""
    if Path(bin_path).exists() or shutil.which(bin_path):
        return bin_path
    if os.name == "nt" and BUNDLED_INSTALLER.exists():
        print(
            f"[convert] mineru-open-api 未找到，尝试运行内置安装脚本: {BUNDLED_INSTALLER}",
            file=sys.stderr,
        )
        pwsh = shutil.which("pwsh") or shutil.which("powershell")
        if pwsh:
            proc = subprocess.run(
                [pwsh, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(BUNDLED_INSTALLER)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=600,
            )
            if proc.returncode != 0:
                raise RuntimeError(
                    "MinerU CLI 安装失败:\n"
                    + proc.stdout
                    + "\n"
                    + proc.stderr
                    + "\n请手动运行安装命令后再试。"
                )
            installed = str(Path.home() / ".mineru" / "bin" / "mineru-open-api.exe")
            if Path(installed).exists():
                return installed
    raise RuntimeError(
        "未找到 mineru-open-api。请先安装：\n"
        "  Windows: irm https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1 | iex\n"
        "  或运行本 skill 内置安装脚本: scripts/mineru/install.ps1\n"
        "  安装完成后如命令仍不可用，请重启终端或设置 MINERU_BIN 环境变量指向可执行文件。"
    )


def convert(pdf: Path, out_dir: Path, mode: str, language: str, timeout: int, bin_path: str) -> dict:
    if not pdf.exists():
        raise FileNotFoundError(f"PDF 不存在: {pdf}")
    out_dir.mkdir(parents=True, exist_ok=True)

    token = os.environ.get("MINERU_TOKEN", "").strip() or _env_value("MINERU_TOKEN")
    cmd = [bin_path]
    if mode == "extract":
        if not token:
            return {
                "ok": False,
                "pdf": str(pdf),
                "error": "extract 模式需要 MinerU API Token：请先运行 mineru-open-api auth，或保存密钥（python scripts/manage_keys.py set MINERU_TOKEN <token>）",
            }
        cmd += ["extract", str(pdf), "-o", str(out_dir), "-f", "md", "--language", language, "--timeout", str(timeout), "--token", token]
    else:
        cmd += ["flash-extract", str(pdf), "-o", str(out_dir), "--language", language, "--timeout", str(timeout)]

    shown = [c if "token" not in c.lower() else "***" for c in cmd]
    print(f"[convert] 运行: {' '.join(shown)}", file=sys.stderr)
    # 硬超时兜底：CLI 的 --timeout 未必覆盖上传/轮询挂死（如到阿里云 OSS
    # 上传端点网络超时），外层必须加一道保险，超时后杀掉进程并返回可重试错误。
    hard_timeout = timeout + 120
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=hard_timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"[convert] 转换超时（>{hard_timeout}s），已终止进程: {pdf}", file=sys.stderr)
        return {
            "ok": False,
            "pdf": str(pdf),
            "error": (
                f"转换超时（超过 {hard_timeout}s）：MinerU CLI 无响应。"
                "常见原因：PDF 过大或网络到 MinerU 云端不稳定（上传/轮询挂起）。"
                "请重试一次；大文件可改用 --mode flash（限 10MB/20 页）或检查网络。"
            ),
        }
    if proc.returncode != 0:
        return {
            "ok": False,
            "pdf": str(pdf),
            "error": proc.stderr.strip() or proc.stdout.strip() or f"exit code {proc.returncode}",
        }

    # 定位生成的 markdown，并统一命名为 <pdf文件名>.md
    produced = list(out_dir.glob("*.md"))
    if not produced:
        return {
            "ok": False,
            "pdf": str(pdf),
            "error": "转换完成但未在输出目录找到 .md 文件",
        }
    produced.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    target = out_dir / (pdf.stem + ".md")
    if produced[0].resolve() != target.resolve():
        shutil.move(str(produced[0]), str(target))
    return {
        "ok": True,
        "pdf": str(pdf),
        "md": str(target),
        "mode": mode,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="PDF -> Markdown（MinerU Open API CLI 封装）")
    ap.add_argument("pdf", help="PDF 文件路径")
    ap.add_argument("--out", default=".", help="输出文件夹（论文文件夹）")
    ap.add_argument(
        "--mode", choices=["flash", "extract"], default="flash",
        help="flash=免认证快速提取（默认）；extract=精提取（需 token）",
    )
    ap.add_argument("--language", default="en", help="文档语言，默认 en")
    ap.add_argument("--timeout", type=int, default=300, help="CLI 内部超时秒数（默认 300）；外层硬超时为其 +120s，超时自动终止并报错")
    ap.add_argument("--bin", default="", help="mineru-open-api 可执行文件路径（默认自动查找）")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    try:
        bin_path = args.bin or _default_bin()
        bin_path = ensure_bin(bin_path)
        result = convert(Path(args.pdf), Path(args.out), args.mode, args.language, args.timeout, bin_path)
    except Exception as e:  # noqa: BLE001
        result = {"ok": False, "pdf": args.pdf, "error": str(e)}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())

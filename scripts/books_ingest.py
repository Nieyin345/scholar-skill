#!/usr/bin/env python3
"""书籍库摄取与维护（书籍库管理工具配套脚本）。

管理 scholar 书籍库（Books/）的三级结构：
  Books/<方向>/<教材名>/<教材名>.pdf + <教材名>.md + (图床/)

命令：
  ensure-skeleton       创建书籍库骨架 + 00_索引.md（触发时动作，不扫描）
  list-orphan-pdfs      列出游离 PDF（不在第三级教材文件夹内的 pdf）
  ingest                归类 + 移动 + 转换 + 登记索引（维护步骤 2-4）

用法示例：
  python books_ingest.py ensure-skeleton
  python books_ingest.py list-orphan-pdfs
  python books_ingest.py ingest --pdf "D:/.../深度学习.pdf" --category 机器学习 --title 深度学习
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

DEFAULT_ROOT = Path.home() / "OB_database" / "Books"
INDEX_NAME = "00_索引.md"
SKILL_DIR = Path(__file__).resolve().parent.parent
CONVERT = SKILL_DIR / "scripts" / "convert_pdf_to_md.py"

INDEX_HEADER = """# 书籍库索引

> 本索引由「书籍库管理」工具维护（只增不删）。结构：Books/<方向>/<教材名>/（pdf + md + 图床）。

| 教材名 | 方向 | PDF | MD | 转换日期 | 状态 |
|--------|------|-----|----|----------|------|
"""


def _is_orphan(pdf: Path, root: Path) -> bool:
    """游离 = pdf 的直接父目录是 Books 根，或是方向目录（其父目录是 Books 根）。"""
    parent = pdf.parent
    if parent == root:
        return True
    return parent.parent == root


def ensure_skeleton(root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    index = root / INDEX_NAME
    created_index = False
    if not index.exists():
        index.write_text(INDEX_HEADER, encoding="utf-8")
        created_index = True
    return {"ok": True, "root": str(root), "index": str(index), "created_index": created_index}


def list_orphan_pdfs(root: Path) -> dict:
    if not root.exists():
        return {"ok": True, "orphans": [], "note": f"书籍库不存在（{root}），先运行 ensure-skeleton"}
    orphans = []
    for pdf in sorted(root.rglob("*.pdf")):
        if _is_orphan(pdf, root):
            orphans.append(str(pdf))
    return {"ok": True, "orphans": orphans}


def ingest(pdf: Path, category: str, title: str, mode: str, root: Path) -> dict:
    if not pdf.exists():
        return {"ok": False, "error": f"PDF 不存在: {pdf}"}
    target_dir = root / category / title
    target_dir.mkdir(parents=True, exist_ok=True)
    target_pdf = target_dir / pdf.name

    moved = False
    if pdf.resolve() != target_pdf.resolve():
        import shutil
        shutil.move(str(pdf), str(target_pdf))
        moved = True
    pdf = target_pdf

    # 转换（复用 convert_pdf_to_md.py，输出到教材文件夹）
    result = {"ok": False, "pdf": str(pdf), "error": "", "md": ""}
    if not CONVERT.exists():
        result["error"] = f"未找到转换脚本: {CONVERT}"
        _append_index(root, title, category, pdf, None, result)
        return result
    proc = subprocess.run(
        [sys.executable, str(CONVERT), str(pdf), "--out", str(target_dir), "--mode", mode],
        capture_output=True, text=True,
    )
    try:
        conv = json.loads(proc.stdout)
    except json.JSONDecodeError:
        result["error"] = (proc.stderr or proc.stdout or f"exit {proc.returncode}").strip()
        _append_index(root, title, category, pdf, None, result)
        return result
    if not conv.get("ok"):
        result["error"] = conv.get("error", "转换失败")
        _append_index(root, title, category, pdf, None, result)
        return result
    result.update(ok=True, md=conv.get("md", ""), mode=mode, moved=moved)
    _append_index(root, title, category, pdf, result.get("md"), result)
    return result


def _append_index(root: Path, title: str, category: str, pdf: Path, md: str | None, result: dict) -> None:
    index = root / INDEX_NAME
    if not index.exists():
        index.write_text(INDEX_HEADER, encoding="utf-8")
    status = "✅ 已转换" if result.get("ok") else "⛔ 转换失败"
    if md is None and not result.get("ok"):
        status = f"⛔ 转换失败：{result.get('error', '')[:40]}"
    row = f"| {title} | {category} | `{pdf.name}` | " + (f"`{Path(md).name}`" if md else "—") + f" | {date.today().isoformat()} | {status} |\n"
    lines = index.read_text(encoding="utf-8").splitlines()
    # 在表格行区（以 | 开头的连续行）末尾插入，避免插到表头前面
    insert_at = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip().startswith("|") and not lines[i].strip().startswith("|--------"):
            insert_at = i + 1
            break
    lines.insert(insert_at, row.rstrip("\n"))
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="书籍库摄取与维护（书籍库管理工具）")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=str(DEFAULT_ROOT), help=f"书籍库根目录（默认 {DEFAULT_ROOT}）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_skel = sub.add_parser("ensure-skeleton", parents=[common], help="创建骨架 + 00_索引.md（不扫描）")
    p_skel.set_defaults(fn=ensure_skeleton)

    p_list = sub.add_parser("list-orphan-pdfs", parents=[common], help="列出游离 PDF")
    p_list.set_defaults(fn=list_orphan_pdfs)

    p_ing = sub.add_parser("ingest", parents=[common], help="归类 + 移动 + 转换 + 登记索引")
    p_ing.add_argument("--pdf", required=True, help="游离 PDF 路径")
    p_ing.add_argument("--category", required=True, help="二级方向（如 通信 / 机器学习）")
    p_ing.add_argument("--title", required=True, help="三级教材名（教材文件夹名）")
    p_ing.add_argument("--mode", choices=["flash", "extract"], default="flash", help="转换模式（默认 flash）")
    p_ing.set_defaults(fn=ingest)

    args = ap.parse_args()
    root = Path(args.root)
    try:
        if args.cmd == "ensure-skeleton":
            result = args.fn(root)
        elif args.cmd == "list-orphan-pdfs":
            result = args.fn(root)
        else:
            result = args.fn(Path(args.pdf), args.category, args.title, args.mode, root)
    except Exception as e:  # noqa: BLE001
        result = {"ok": False, "error": str(e)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())


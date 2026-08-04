#!/usr/bin/env python3
"""scholar 三库文件系统初始化（首次触发时自动执行，不询问路径）。

在当前工作目录（cwd，即当前项目）创建三个并行的子文件夹：
  论文/   ← 论文库：研究方向文件夹建在论文库下（论文/<主题>/）
  笔记/   ← 学习笔记库：Sources/Papers、Knowledge 等（可直接作为 Obsidian vault 打开）
  书籍/   ← 教材库：<方向>/<教材名>/（pdf + md + 图床）

命令：
  init                  创建三库骨架 + 论文/00_索引.md + 笔记/00-导航.md + 书籍/00_索引.md（幂等，不扫描）
  add-topic <主题>      在论文库下创建研究方向文件夹：论文/<主题>/ + 00_项目导航.md + 登记论文/00_索引.md
  list-topics           列出论文库已登记的研究方向
  cleanup-tmp           清空 .scholar_tmp/（会话结束时调用；只删该目录内容，不删其他文件）

用法示例：
  python scripts/init_workspace.py init --project "D:/path/to/project"
  python scripts/init_workspace.py add-topic "GNN强化学习网络资源调度" --project "D:/path/to/project"
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
NAV_TEMPLATE = SKILL_DIR / "references" / "project-navigation-template.md"

PAPERS_DIR = "论文"
NOTES_DIR = "笔记"
BOOKS_DIR = "书籍"
TMP_DIR = ".scholar_tmp"

PAPERS_INDEX_HEADER = """# 论文库索引

> 本索引由 scholar 主流程维护（只增不删）。结构：论文/<主题>/（研究方向文件夹，内含 00_项目导航.md 与各类产出）。
> 登记时机：流程0 产出方向文档 / 流程一创建主题文件夹时追加一行；方向文档变化时更新状态列。

| 主题 | 研究方向（一句话） | 创建日期 | 最近更新 | 状态 |
|------|--------------------|----------|----------|------|
"""

NOTES_NAV_HEADER = """# 00-导航

> 本文件是 scholar「学习笔记工具」在当前项目中的**笔记库导航**（学习笔记库结构与位置的唯一事实来源）。本目录可直接作为 Obsidian vault 打开（Obsidian → Open folder as vault → 选择 <项目>/笔记）。
> 规则：**触发学习笔记工具时检查/生成；只有文件发生变动才更新**（新增/删除/重命名/移动笔记；详见 tools/学习笔记.md 与 SKILL.md）。

## 1. 项目信息

| 项 | 内容 |
|----|------|
| 项目根目录 | <项目>/笔记/ |
| 创建日期 | YYYY-MM-DD |
| 最近更新 | YYYY-MM-DD |
| 对应论文库 | <项目>/论文/ |

## 2. 文件结构（目录总表，唯一事实来源）

```
<项目>/笔记/
├── 00-导航.md               ← 本文件（入口，文件变动时更新）
├── 02-Index.md             ← 知识索引（人读导航，新增/提炼时更新）
├── Sources/
│   └── Papers/             ← 论文源笔记（每篇一个，slug = 一作姓-年-短名）
├── Knowledge/              ← 知识笔记（概念/方法/结论/争议/工具，synthesis-centered）
├── Maps/                   ← 知识图谱（可选，Mermaid / canvas）
└── _system/
    └── registry.md         ← 笔记注册表（每篇新增登记，只增不删）
```

> 论文转换稿（源）在论文库 <项目>/论文/<主题>/<论文短名-年>.md，本库只放**提炼后的笔记**（frontmatter source 指回源），不复制论文/PDF。

## 6. 当前状态

- 当前任务：
- 已提炼论文：
- 知识笔记数：
- 下一步：
- 阻塞 / 待用户决定：

## 7. 更新记录

| 日期 | 触发 | 变更内容 |
|------|------|----------|
| YYYY-MM-DD | 首次触发 | 生成笔记库骨架与导航文件 |

## 8. 维护铁律（本文件固定章节，勿删）

1. **本导航是笔记库结构的唯一事实来源**：任何笔记/目录以本导航为准，导航与实际不符时先改导航再动文件；
2. **新笔记先登记再创建**：新增论文笔记/知识笔记前，先登记位置，再创建；
3. **移动/重命名必须同步**：笔记被移动/重命名时同步更新本导航、_system/registry.md 与 02-Index.md——不允许「文件在但导航没更新」；
4. **文件变动时才更新**：新增/删除/重命名/移动笔记等文件变动发生后，才更新本导航（只增不删）；无文件变动的轮次不重写；
5. **源 vs 提炼不混淆**：Sources/Papers/ 是提炼后的源笔记，论文转换稿在论文库 论文/<主题>/；本库不复制 PDF/转换稿；
6. **每条笔记至少一个入口**：要么登记在 02-Index.md，要么被其他笔记链接，避免孤立笔记；
7. **wiki 链接优先**：库内互链一律用双中括号笔记名；重命名笔记后依赖 Obsidian 自动更新链接，仍须检查反向链接；
8. **只增不删**：历史保留在更新记录与版本存档中，不删除历史。
"""

TMP_README = """# .scholar_tmp（临时工作区，可随时清空）

> 本目录存放 scholar 会话过程中的临时脚本与中间产物（搜索缓存、临时 py/json/txt 等）。
> 纪律：
> 1. 临时脚本/中间产物一律放这里，**禁止散落在项目根目录**；
> 2. 会话结束（或工作流阶段门禁通过）时调用 `python scripts/init_workspace.py cleanup-tmp` 清空；
> 3. 本目录以 `.` 开头，Obsidian 默认隐藏；不登记进任何导航文档。
"""

BOOKS_INDEX_HEADER = """# 书籍库索引

> 本索引由「书籍库管理」工具维护（只增不删）。结构：书籍/<方向>/<教材名>/（pdf + md + 图床）。

| 教材名 | 方向 | PDF | MD | 转换日期 | 状态 |
|--------|------|-----|----|----------|------|
"""


def _ensure_papers_index(papers: Path) -> Path:
    index = papers / "00_索引.md"
    if not index.exists():
        index.write_text(PAPERS_INDEX_HEADER, encoding="utf-8")
    return index


def _append_topic_index(index: Path, topic: str) -> None:
    today = date.today().isoformat()
    row = f"| {topic} | — | {today} | {today} | 待生成 |"
    lines = index.read_text(encoding="utf-8").splitlines()
    insert_at = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip().startswith("|") and not lines[i].strip().startswith("|--------"):
            insert_at = i + 1
            break
    lines.insert(insert_at, row)
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")


def init(project: Path) -> dict:
    papers = project / PAPERS_DIR
    notes = project / NOTES_DIR
    books = project / BOOKS_DIR
    papers.mkdir(parents=True, exist_ok=True)
    notes.mkdir(parents=True, exist_ok=True)
    books.mkdir(parents=True, exist_ok=True)

    (notes / "Sources").mkdir(exist_ok=True)
    (notes / "Sources" / "Papers").mkdir(exist_ok=True)
    (notes / "Knowledge").mkdir(exist_ok=True)
    (notes / "Maps").mkdir(exist_ok=True)
    (notes / "_system").mkdir(exist_ok=True)

    tmp_dir = project / TMP_DIR
    tmp_dir.mkdir(exist_ok=True)
    tmp_readme = tmp_dir / "README.md"
    if not tmp_readme.exists():
        tmp_readme.write_text(TMP_README, encoding="utf-8")

    papers_index = _ensure_papers_index(papers)

    notes_nav = notes / "00-导航.md"
    created_notes = False
    if not notes_nav.exists():
        notes_nav.write_text(NOTES_NAV_HEADER, encoding="utf-8")
        created_notes = True

    books_index = books / "00_索引.md"
    created_books = False
    if not books_index.exists():
        books_index.write_text(BOOKS_INDEX_HEADER, encoding="utf-8")
        created_books = True

    return {
        "ok": True,
        "project": str(project),
        "papers": str(papers),
        "notes": str(notes),
        "books": str(books),
        "papers_index": str(papers_index),
        "notes_nav_created": created_notes,
        "books_index_created": created_books,
        "tmp_dir": str(tmp_dir),
    }


def add_topic(topic: str, project: Path) -> dict:
    if not topic or topic.strip() in {".", ".."}:
        return {"ok": False, "error": "主题名不能为空或路径分隔符"}
    papers = project / PAPERS_DIR
    papers.mkdir(parents=True, exist_ok=True)
    topic_dir = papers / topic.strip()
    topic_dir.mkdir(parents=True, exist_ok=True)

    nav = topic_dir / "00_项目导航.md"
    created_nav = False
    if not nav.exists():
        if NAV_TEMPLATE.exists():
            shutil.copyfile(NAV_TEMPLATE, nav)
        else:
            nav.write_text("# 00_项目导航\n\n> 模板缺失，请按 references/project-navigation-template.md 生成。\n", encoding="utf-8")
        created_nav = True

    index = _ensure_papers_index(papers)
    _append_topic_index(index, topic.strip())

    return {
        "ok": True,
        "topic": topic.strip(),
        "topic_dir": str(topic_dir),
        "nav": str(nav),
        "created_nav": created_nav,
        "papers_index": str(index),
    }


def list_topics(project: Path) -> dict:
    papers = project / PAPERS_DIR
    index = papers / "00_索引.md"
    topics = []
    if index.exists():
        for line in index.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("|") and not line.startswith("| 主题") and not line.startswith("|---"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells:
                    topics.append(cells[0])
    return {"ok": True, "topics": topics, "papers_index": str(index)}



def cleanup_tmp(project: Path) -> dict:
    tmp_dir = project / TMP_DIR
    if not tmp_dir.exists():
        return {"ok": True, "tmp_dir": str(tmp_dir), "removed": [], "note": "临时目录不存在，无需清理"}
    removed = []
    for item in sorted(tmp_dir.iterdir()):
        if item.name == "README.md":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
        removed.append(item.name)
    return {"ok": True, "tmp_dir": str(tmp_dir), "removed": removed}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="scholar 三库文件系统初始化")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--project", default=str(Path.cwd()), help="项目根目录（默认当前工作目录 cwd）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", parents=[common], help="创建三库骨架（幂等，不扫描）")
    p_init.set_defaults(fn=init)

    p_add = sub.add_parser("add-topic", parents=[common], help="在论文库下创建研究方向文件夹")
    p_add.add_argument("topic", help="研究方向名称")
    p_add.set_defaults(fn=add_topic)

    p_list = sub.add_parser("list-topics", parents=[common], help="列出论文库已登记的研究方向")
    p_list.set_defaults(fn=list_topics)

    p_clean = sub.add_parser("cleanup-tmp", parents=[common], help="清空 .scholar_tmp/（只删该目录内容）")
    p_clean.set_defaults(fn=cleanup_tmp)

    args = ap.parse_args()
    project = Path(args.project).expanduser().resolve()
    try:
        if args.cmd == "init":
            result = args.fn(project)
        elif args.cmd == "add-topic":
            result = args.fn(args.topic, project)
        else:
            result = args.fn(project)
    except Exception as e:  # noqa: BLE001
        result = {"ok": False, "error": str(e)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())

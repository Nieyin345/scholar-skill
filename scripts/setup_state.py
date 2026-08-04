#!/usr/bin/env python3
"""scholar 状态管理：记录初始化时间与本地路径覆盖（<skill_dir>/state.json）。

用法：
  python setup_state.py status                        # 查看当前状态（初始化时间 / 路径覆盖）
  python setup_state.py set-path <key> <value>        # 记录本地路径覆盖（可选：obsidian_vault / books_root / zotero_root）
  python setup_state.py complete                      # 标记三库骨架初始化完成（信息性，不 gate 任何流程）
  python setup_state.py reset                         # 重置初始化记录

说明：state.json 位于 <skill_dir>/state.json，已被 .gitignore 排除，不会上传 GitHub。
scholar 不设「先配置再使用」的首次触发门禁：state.json 不作为任何流程的前置条件，
仅记录首次/最近触发时间与路径覆盖（paths）。三库（论文/笔记/书籍）骨架缺失时自动创建；
密钥按需获取（见 SKILL.md「密钥获取与保存规则」），不在本状态中记录。
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path(__file__).resolve().parent.parent / "state.json"
SCHEMA_VERSION = 1
PATH_KEYS = ("obsidian_vault", "books_root", "zotero_root")


def default_state() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "setup_complete": False,
        "first_trigger_at": None,
        "last_trigger_at": None,
        "paths": {k: None for k in PATH_KEYS},
    }


def load() -> dict:
    if not STATE_FILE.exists():
        return default_state()
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return default_state()
    state = default_state()
    for k in state:
        if k in data:
            state[k] = data[k]
    state["paths"] = {**default_state()["paths"], **data.get("paths", {})}
    return state


def save(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def cmd_status(args) -> None:
    state = load()
    first = not state.get("setup_complete")
    print(json.dumps({"first_trigger": first, **state}, ensure_ascii=False, indent=2))


def cmd_set_path(args) -> None:
    state = load()
    state["paths"][args.key] = args.value
    state["last_trigger_at"] = now()
    save(state)
    print(f"OK: paths.{args.key} = {args.value}")


def cmd_complete(args) -> None:
    state = load()
    if state.get("first_trigger_at") is None:
        state["first_trigger_at"] = now()
    state["setup_complete"] = True
    state["last_trigger_at"] = now()
    save(state)
    print("OK: setup_complete = true")


def cmd_reset(args) -> None:
    save(default_state())
    print("OK: reset to first-trigger state")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.strip())
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="查看当前状态")
    sp = sub.add_parser("set-path", help="记录本地路径")
    sp.add_argument("key", choices=PATH_KEYS)
    sp.add_argument("value")
    sub.add_parser("complete", help="标记三库骨架初始化完成（信息性）")
    sub.add_parser("reset", help="重置为首次触发状态")
    args = parser.parse_args()
    handlers = {"status": cmd_status, "set-path": cmd_set_path, "complete": cmd_complete, "reset": cmd_reset}
    handlers[args.cmd](args)


if __name__ == "__main__":
    main()

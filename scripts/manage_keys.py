#!/usr/bin/env python3
"""密钥管理：保存/读取 scholar 本地密钥（<skill_dir>/.env）。

用法：
  python manage_keys.py set ANYSEARCH_API_KEY <value>   # 保存密钥
  python manage_keys.py get ANYSEARCH_API_KEY            # 读取密钥
  python manage_keys.py list                             # 列出已保存的密钥名
  python manage_keys.py delete ANYSEARCH_API_KEY         # 删除密钥

说明：密钥文件为 <skill_dir>/.env，已被 .gitignore 排除，不会上传到 GitHub。
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def load() -> dict:
    """读取 .env，返回 {KEY: VALUE}。"""
    data = {}
    if not ENV_FILE.exists():
        return data
    for line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def save(data: dict) -> None:
    ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{k}={v}" for k, v in sorted(data.items())]
    ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Windows 下避免被误读为需要解除锁定的下载文件
    try:
        import ctypes
        ctypes.windll.kernel32.SetFileAttributesW(str(ENV_FILE), 0x80)  # FILE_ATTRIBUTE_NORMAL
    except Exception:
        pass


def set_key(key: str, value: str) -> None:
    data = load()
    data[key.upper()] = value
    save(data)


def get_key(key: str) -> str | None:
    return load().get(key.upper())


def delete_key(key: str) -> None:
    data = load()
    data.pop(key.upper(), None)
    save(data)


def main() -> int:
    ap = argparse.ArgumentParser(description="scholar 密钥管理")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_set = sub.add_parser("set", help="保存密钥")
    p_set.add_argument("key")
    p_set.add_argument("value")
    p_get = sub.add_parser("get", help="读取密钥")
    p_get.add_argument("key")
    sub.add_parser("list", help="列出密钥名")
    p_del = sub.add_parser("delete", help="删除密钥")
    p_del.add_argument("key")
    args = ap.parse_args()

    if args.cmd == "set":
        set_key(args.key, args.value)
        print(f"saved {args.key.upper()} -> {ENV_FILE}")
    elif args.cmd == "get":
        v = get_key(args.key)
        print(v if v is not None else "")
        return 0 if v is not None else 1
    elif args.cmd == "list":
        for k in load():
            print(k)
    elif args.cmd == "delete":
        delete_key(args.key)
        print(f"deleted {args.key.upper()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

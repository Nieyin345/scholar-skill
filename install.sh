#!/usr/bin/env bash
# Scholar Skill 一键安装脚本（Linux / macOS / Git Bash）
# 用法:
#   bash install.sh --agent auto
#   bash install.sh --agent codex
#   bash install.sh --agent custom --target /path/to/skills
#   bash install.sh --repo https://github.com/<user>/<repo>.git --agent auto
set -euo pipefail

REPO_URL="https://github.com/Nieyin345/scholar-skill.git"
AGENT="auto"
TARGET_DIR=""
SKILL_NAME="scholar"

usage() {
  echo "Usage: install.sh [--agent auto|codex|claude|cursor|custom] [--target DIR] [--repo URL]"
  echo "  --agent  auto(default)/codex/claude/cursor/custom  ; auto = install to every detected agent"
  echo "  --target DIR   custom target dir (requires --agent custom)"
  echo "  --repo URL     custom repo source (default: $REPO_URL)"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent) AGENT="$2"; shift 2 ;;
    --target) TARGET_DIR="$2"; shift 2 ;;
    --repo) REPO_URL="$2"; shift 2 ;;
    *) usage ;;
  esac
done

command -v git >/dev/null 2>&1 || { echo "ERROR: git is required."; exit 1; }

install_to() {
  local dest="$1"
  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  git clone --depth 1 "$REPO_URL" "$dest"
  if [[ ! -f "$dest/SKILL.md" ]]; then
    echo "ERROR: no SKILL.md found in $dest"; exit 1
  fi
  echo ">> Installed scholar -> $dest (git repo; git pull 即可更新)"
}

if [[ "$AGENT" == "custom" ]]; then
  [[ -n "$TARGET_DIR" ]] || { echo "ERROR: --agent custom requires --target DIR"; exit 1; }
  install_to "$TARGET_DIR/$SKILL_NAME"
  exit 0
fi

installed=0
if [[ "$AGENT" == "auto" || "$AGENT" == "codex" ]] && [[ -d "$HOME/.codex" ]]; then
  install_to "$HOME/.codex/skills/$SKILL_NAME"; installed=1
fi
if [[ "$AGENT" == "auto" || "$AGENT" == "claude" ]] && [[ -d "$HOME/.claude" ]]; then
  install_to "$HOME/.claude/skills/$SKILL_NAME"; installed=1
fi
if [[ "$AGENT" == "auto" || "$AGENT" == "cursor" ]] && [[ -d "$HOME/.cursor" ]]; then
  install_to "$HOME/.cursor/skills/$SKILL_NAME"; installed=1
fi
if [[ $installed -eq 0 ]]; then
  case "$AGENT" in
    codex)  install_to "$HOME/.codex/skills/$SKILL_NAME"; installed=1 ;;
    claude) install_to "$HOME/.claude/skills/$SKILL_NAME"; installed=1 ;;
    cursor) install_to "$HOME/.cursor/skills/$SKILL_NAME"; installed=1 ;;
  esac
fi

if [[ $installed -eq 0 ]]; then
  echo ">> No supported agent detected. Install manually:"
  echo "   git clone --depth 1 $REPO_URL <your-skills-dir>/$SKILL_NAME"
  echo "   or run: install.sh --agent custom --target <your-skills-dir>"
  exit 1
fi
echo ">> Done. Restart your agent to load the scholar skill."

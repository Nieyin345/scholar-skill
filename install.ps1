# Scholar Skill 一键安装/更新脚本（Windows PowerShell 5.1+ / 7+）
# 用法:
#   .\install.ps1 -Agent auto
#   .\install.ps1 -Agent codex
#   .\install.ps1 -Agent custom -TargetDir D:\path\to\skills
#   .\install.ps1 -RepoUrl https://github.com/<user>/<repo>.git -Agent auto
#
# 本地配置保留：.env（密钥）与 state.json（首次配置状态）是本机文件，更新/重装都会自动保留。
param(
  [string]$Agent = "auto",        # auto / codex / claude / cursor / custom
  [string]$TargetDir = "",
  [string]$RepoUrl = "https://github.com/Nieyin345/scholar-skill.git",
  [switch]$Force
)
$ErrorActionPreference = "Stop"
$SkillName = "scholar"
$LocalFiles = @(".env", "state.json")

function Install-To([string]$Dest) {
  New-Item -ItemType Directory -Path (Split-Path $Dest -Parent) -Force | Out-Null

  # 已安装且是 git 仓库：保留本地配置，直接更新
  if (Test-Path (Join-Path $Dest ".git")) {
    Push-Location $Dest
    try {
      git remote set-url origin $RepoUrl | Out-Null
      git fetch --depth 1 origin main | Out-Null
      git reset --hard origin/main | Out-Null
    } finally {
      Pop-Location
    }
    if (-not (Test-Path (Join-Path $Dest "SKILL.md"))) {
      throw "ERROR: no SKILL.md found in $Dest"
    }
    Write-Output ">> Updated scholar -> $Dest (本地 .env / state.json 已保留)"
    return
  }

  # 全新安装：先备份本地配置（若有），重装后恢复
  $tmpBak = Join-Path $env:TEMP ("scholar-local-" + [guid]::NewGuid().ToString("N"))
  $found = @($LocalFiles | Where-Object { Test-Path (Join-Path $Dest $_) })
  if ($found.Count -gt 0) {
    New-Item -ItemType Directory -Path $tmpBak | Out-Null
    foreach ($f in $found) { Copy-Item (Join-Path $Dest $f) $tmpBak }
  }
  if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
  git clone --depth 1 $RepoUrl $Dest | Out-Null
  if (-not (Test-Path (Join-Path $Dest "SKILL.md"))) {
    throw "ERROR: no SKILL.md found in $Dest"
  }
  if ($found.Count -gt 0) {
    foreach ($f in $found) { Copy-Item (Join-Path $tmpBak $f) $Dest }
    Remove-Item -Recurse -Force $tmpBak
  }
  Write-Output ">> Installed scholar -> $Dest (本地 .env / state.json 已保留)"
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "ERROR: git is required."
}

if ($Agent -eq "custom") {
  if ([string]::IsNullOrWhiteSpace($TargetDir)) { throw "ERROR: -Agent custom requires -TargetDir" }
  Install-To (Join-Path $TargetDir $SkillName)
  exit 0
}

$installed = $false
if (($Agent -eq "auto" -or $Agent -eq "codex") -and (Test-Path "$env:USERPROFILE\.codex")) {
  Install-To "$env:USERPROFILE\.codex\skills\$SkillName"; $installed = $true
}
if (($Agent -eq "auto" -or $Agent -eq "claude") -and (Test-Path "$env:USERPROFILE\.claude")) {
  Install-To "$env:USERPROFILE\.claude\skills\$SkillName"; $installed = $true
}
if (($Agent -eq "auto" -or $Agent -eq "cursor") -and (Test-Path "$env:USERPROFILE\.cursor")) {
  Install-To "$env:USERPROFILE\.cursor\skills\$SkillName"; $installed = $true
}
if (-not $installed) {
  switch ($Agent) {
    "codex"  { Install-To "$env:USERPROFILE\.codex\skills\$SkillName"; $installed = $true }
    "claude" { Install-To "$env:USERPROFILE\.claude\skills\$SkillName"; $installed = $true }
    "cursor" { Install-To "$env:USERPROFILE\.cursor\skills\$SkillName"; $installed = $true }
  }
}
if (-not $installed) {
  Write-Output ">> No supported agent detected. Install manually:"
  Write-Output "   git clone --depth 1 $RepoUrl <your-skills-dir>\$SkillName"
  Write-Output "   or run: install.ps1 -Agent custom -TargetDir <your-skills-dir>"
  exit 1
}
Write-Output ">> Done. Restart your agent to load the scholar skill."

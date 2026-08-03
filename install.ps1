# Scholar Skill 一键安装脚本（Windows PowerShell 5.1+ / 7+）
# 用法:
#   .\install.ps1 -Agent auto
#   .\install.ps1 -Agent codex
#   .\install.ps1 -Agent custom -TargetDir D:\path\to\skills
#   .\install.ps1 -RepoUrl https://github.com/<user>/<repo>.git -Agent auto
param(
  [string]$Agent = "auto",        # auto / codex / claude / cursor / custom
  [string]$TargetDir = "",
  [string]$RepoUrl = "https://github.com/Nieyin345/scholar-skill.git",
  [switch]$Force
)
$ErrorActionPreference = "Stop"
$SkillName = "scholar"

function Install-To([string]$Dest) {
  if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
  New-Item -ItemType Directory -Path (Split-Path $Dest -Parent) -Force | Out-Null
  Copy-Item -Recurse -Force (Join-Path $Tmp $SkillName) $Dest
  Write-Output ">> Installed scholar -> $Dest"
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "ERROR: git is required."
}

$Tmp = Join-Path $env:TEMP ("scholar-install-" + [guid]::NewGuid().ToString("N"))
try {
  Write-Output ">> Cloning $RepoUrl ..."
  git clone --depth 1 $RepoUrl (Join-Path $Tmp $SkillName)
  if (-not (Test-Path (Join-Path $Tmp "$SkillName\SKILL.md"))) {
    throw "ERROR: no SKILL.md found in cloned repo root."
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
}
finally {
  if (Test-Path $Tmp) { Remove-Item -Recurse -Force $Tmp }
}

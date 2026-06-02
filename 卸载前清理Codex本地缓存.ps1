#Requires -Version 5.1
[CmdletBinding()]
param(
    [switch]$SkipUninstall,
    [switch]$NoPause
)

$ErrorActionPreference = 'Continue'

$ProjectRoot = 'F:\CodexSharedCockpit'
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupRoot = Join-Path $ProjectRoot "_reinstall_handoff_backup\$timestamp"

if (-not (Test-Path -LiteralPath $ProjectRoot)) {
    throw "Project folder not found: $ProjectRoot"
}

New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null

$handoffFiles = @(
    'CURRENT_WORKING_STATE.md',
    '项目笔记本.txt',
    '重装后恢复提示.md'
)

foreach ($name in $handoffFiles) {
    $src = Join-Path $ProjectRoot $name
    if (Test-Path -LiteralPath $src) {
        Copy-Item -LiteralPath $src -Destination $backupRoot -Force
    }
}

$resumePrompt = @'
Use $slow-chat-handoff. Read CURRENT_WORKING_STATE.md and 项目笔记本.txt if present. Then inspect episodes\season_01\episode_01\第一集_OP13-OP16_废站关键帧_宫格分镜表_V1.md, production\online\AI漫剧分镜管理器.html, prompts\角色锁.md, prompts\提示词模板.md, and episodes\season_01\episode_01\keyframes\op13_op16_废站_v1. Continue from the recorded next step: verify OP14-2 through OP16-3, update the storyboard table and manager references, resolve whether the abstract 小夏回声 workaround is acceptable, finish OP16-4 through OP16-6, then run checks.
'@

$resumeFile = Join-Path $backupRoot '重装后粘贴到Codex的新对话.txt'
Set-Content -LiteralPath $resumeFile -Value $resumePrompt -Encoding UTF8
Set-Clipboard -Value $resumePrompt

Write-Host "已备份交接文件到：$backupRoot"
Write-Host "已把重装后的恢复提示复制到剪贴板。"
Write-Host ""

if (-not $SkipUninstall) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "尝试通过 winget 卸载名称为 Codex 的应用。如果 winget 找不到，会继续清理本地缓存。"
        & $winget.Source uninstall '--name' 'Codex' '--accept-source-agreements'
        Write-Host ""
    }
    else {
        Write-Host "未检测到 winget。请在 Windows 设置 > 应用 中手动卸载 Codex，然后继续看本脚本的缓存清理结果。"
        Write-Host ""
    }

    $npm = Get-Command npm -ErrorAction SilentlyContinue
    if ($npm) {
        $npmGlobal = & $npm.Source 'ls' '-g' '--depth=0' 2>$null
        if ($npmGlobal -match '@openai/codex') {
            Write-Host "检测到全局 npm 包 @openai/codex，正在卸载。"
            & $npm.Source 'uninstall' '-g' '@openai/codex'
            Write-Host ""
        }
    }
}

function Remove-CodexPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return
    }

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $projectFullPath = [System.IO.Path]::GetFullPath($ProjectRoot)
    $leaf = Split-Path -Leaf $fullPath

    $allowedLeafNames = @(
        '.codex',
        'Codex',
        'codex',
        'codex-updater'
    )

    $allowed = $allowedLeafNames -contains $leaf
    $allowed = $allowed -or ($fullPath -match '\\OpenAI\\Codex$')

    if ($fullPath.Equals($projectFullPath, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove project folder: $fullPath"
    }

    if (-not $allowed) {
        Write-Warning "跳过可疑路径，未删除：$fullPath"
        return
    }

    if (Test-Path -LiteralPath $fullPath) {
        Write-Host "删除 Codex 本地数据：$fullPath"
        Remove-Item -LiteralPath $fullPath -Recurse -Force -ErrorAction Continue
    }
}

$codexPaths = @(
    (Join-Path $env:USERPROFILE '.codex'),
    (Join-Path $env:APPDATA 'Codex'),
    (Join-Path $env:APPDATA 'codex'),
    (Join-Path $env:APPDATA 'OpenAI\Codex'),
    (Join-Path $env:LOCALAPPDATA 'Codex'),
    (Join-Path $env:LOCALAPPDATA 'codex'),
    (Join-Path $env:LOCALAPPDATA 'OpenAI\Codex'),
    (Join-Path $env:LOCALAPPDATA 'codex-updater')
)

foreach ($path in $codexPaths) {
    Remove-CodexPath -Path $path
}

$tempRoot = [System.IO.Path]::GetFullPath($env:TEMP)
if (Test-Path -LiteralPath $tempRoot) {
    Get-ChildItem -LiteralPath $tempRoot -Force -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -match '^(codex|openai-codex)[-_]' -or
            $_.Name -match '^Codex'
        } |
        ForEach-Object {
            $tempItem = [System.IO.Path]::GetFullPath($_.FullName)
            if ($tempItem.StartsWith($tempRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
                Write-Host "删除 Codex 临时文件：$tempItem"
                Remove-Item -LiteralPath $tempItem -Recurse -Force -ErrorAction Continue
            }
        }
}

Write-Host ""
Write-Host "清理完成。项目目录保留在：$ProjectRoot"
Write-Host "重装 Codex 后，进入项目目录并粘贴剪贴板里的恢复提示即可。"

if (-not $NoPause) {
    Read-Host "按回车退出" | Out-Null
}

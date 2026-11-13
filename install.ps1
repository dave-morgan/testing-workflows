param(
    [string]$CodexSkills = (Join-Path $env:USERPROFILE '.agents/skills'),
    [string]$ClaudeSkills = (Join-Path $env:USERPROFILE '.claude/skills'),
    [ValidateSet('goal-gated','goal-continuous','goal-observe','goal-steer','goal-hybrid','goal-adaptive','goal-hybrid-lean','goal-hybrid-lean-plus')]
    [string[]]$SkillNames = @('goal-gated', 'goal-continuous', 'goal-observe', 'goal-steer')
)

$ErrorActionPreference = 'Stop'
$selectedSkills = $SkillNames

# Check every target before copying; existing installations are never replaced.
foreach ($skillName in $selectedSkills) {
    $sourcePath = Join-Path $PSScriptRoot "skills/$skillName"
    if (-not (Test-Path -LiteralPath (Join-Path $sourcePath 'scripts/runlog.py'))) {
        throw "Package is incomplete: run python tools/package.py first."
    }
    foreach ($skillsRoot in @($CodexSkills, $ClaudeSkills)) {
        $targetPath = Join-Path $skillsRoot $skillName
        if (Test-Path -LiteralPath $targetPath) {
            throw "Skill already exists; refusing to overwrite: $targetPath"
        }
    }
}

foreach ($skillsRoot in @($CodexSkills, $ClaudeSkills)) {
    New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null
}
foreach ($skillName in $selectedSkills) {
    $sourcePath = Join-Path $PSScriptRoot "skills/$skillName"
    $canonicalPath = Join-Path $CodexSkills $skillName
    Copy-Item -LiteralPath $sourcePath -Destination $canonicalPath -Recurse
    $claudePath = Join-Path $ClaudeSkills $skillName
    New-Item -ItemType Junction -Path $claudePath -Target $canonicalPath | Out-Null
    Write-Output "$skillName -> $canonicalPath (Claude junction: $claudePath)"
}

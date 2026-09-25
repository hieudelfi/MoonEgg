# Registers the Supabase keep-alive as a Windows scheduled task.
#
# Written as a script, not as a list of clicks, so the machine can be rebuilt the same way
# twice. Run it once per machine, from an elevated or a normal PowerShell 7 prompt:
#
#   pwsh -File tools/ops/register-ping-task.ps1
#
# Remove it again with:
#
#   Unregister-ScheduledTask -TaskName 'MoonEgg keep-alive ping' -Confirm:$false
#
# The task runs every 3 days. -StartWhenAvailable means a run missed because the machine
# was off happens at the next start-up instead of being skipped. A ping three hours late
# still beats a project that slept for a week.

[CmdletBinding()]
param(
    [string]$TaskName = 'MoonEgg keep-alive ping',
    [string]$BashPath = 'C:\Program Files\Git\bin\bash.exe',
    [int]$DaysInterval = 3,
    [string]$At = '09:00'
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$script = Join-Path $repoRoot 'tools\ops\ping-supabase.sh'

if (-not (Test-Path $script)) {
    throw "ping script not found at $script"
}

if (-not (Test-Path $BashPath)) {
    throw "bash not found at $BashPath. Pass -BashPath with the real location."
}

# bash wants a POSIX path for its own argument
$posixScript = 'tools/ops/ping-supabase.sh'

$action = New-ScheduledTaskAction `
    -Execute $BashPath `
    -Argument "-lc `"$posixScript`"" `
    -WorkingDirectory $repoRoot

$trigger = New-ScheduledTaskTrigger -Daily -DaysInterval $DaysInterval -At $At

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Output "removed the previous task so this run replaces it"
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description 'Reads one row from Supabase so the free project does not pause. Task P.2.' | Out-Null

Write-Output "registered: $TaskName"
Write-Output "  runs     : every $DaysInterval days at $At, and at start-up if a run was missed"
Write-Output "  command  : $BashPath -lc `"$posixScript`""
Write-Output "  in       : $repoRoot"
Write-Output ""
Write-Output "Run it once now to prove it fires:"
Write-Output "  Start-ScheduledTask -TaskName '$TaskName'"
Write-Output "Then check the log gained a line:"
Write-Output "  Get-Content tools/ops/ping-supabase.log -Tail 3"

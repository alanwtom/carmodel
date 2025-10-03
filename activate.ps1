$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $scriptPath
& "$scriptPath\venv\Scripts\Activate.ps1"
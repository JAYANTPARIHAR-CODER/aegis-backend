# Start the AEGIS backend (PowerShell helper)
# Usage: ./start_backend.ps1

# If you have a virtual environment in .venv, activate it
if (Test-Path -Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating .venv"
    . .\.venv\Scripts\Activate.ps1
}

# Start uvicorn
uvicorn main:app --reload --host 127.0.0.1 --port 8000

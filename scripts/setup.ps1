param(
    [string]$DbUser = "postgres",
    [string]$DbName = "careercraft_ai",
    [string]$DbHost = "localhost",
    [int]$DbPort = 5432
)

Write-Host "CareerCraft AI setup starting..." -ForegroundColor Cyan

if (-not $env:PGPASSWORD) {
    $secure = Read-Host "Enter PostgreSQL password for user '$DbUser'" -AsSecureString
    $ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    $env:PGPASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
}

$root = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root "backend"
$sqlFile = Join-Path $root "sql.txt"
$seedScript = Join-Path $backend "scripts\seed_catalog.py"

Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
pip install -r (Join-Path $backend "requirements.txt")

Write-Host "Ensuring database exists..." -ForegroundColor Cyan
psql -U $DbUser -h $DbHost -p $DbPort -c "CREATE DATABASE $DbName;" 2>$null

Write-Host "Applying schema..." -ForegroundColor Cyan
psql -U $DbUser -h $DbHost -p $DbPort -d $DbName -f $sqlFile

Write-Host "Seeding catalog..." -ForegroundColor Cyan
python $seedScript

Write-Host "Setup complete." -ForegroundColor Green
Write-Host "Start backend: python `"$backend\app.py`""
Write-Host "Open frontend: $root\frontend\index.html"

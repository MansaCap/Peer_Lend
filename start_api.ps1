# ============================
#  Winston's One‑Click API Start
# ============================

Write-Host "🔧 Activating virtual environment..."
.\.venv\Scripts\Activate

Write-Host "🔐 Setting database environment variables..."
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "root"
$env:DB_NAME = "fintech"

Write-Host "🛑 Checking for old uvicorn processes..."
$ports = @(8001, 8003, 8011)
foreach ($p in $ports) {
    $conn = Get-NetTCPConnection -State Listen -LocalPort $p -ErrorAction SilentlyContinue
    if ($conn) {
        Write-Host "⚠️ Port $p is in use. Killing process $($conn.OwningProcess)..."
        Stop-Process -Id $conn.OwningProcess -Force
    }
}

Write-Host "🚀 Starting API on port 8011..."
uvicorn Pulse.risk_api:app --host 127.0.0.1 --port 8011

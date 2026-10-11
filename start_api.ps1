# Set environment variables
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="root"
$env:DB_NAME="fintech"

# Run Uvicorn server
python -m uvicorn ancla_api.app.main:app --reload --host 127.0.0.1 --port 8001
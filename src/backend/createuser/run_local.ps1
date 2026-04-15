$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
$env:DB_USER="myuser"
$env:DB_PASS="mypass"
$env:DB_NAME="userdb"

Write-Host "Starting CreateUser Service locally connected to local MySQL Docker..."
#run this in background
python createuser_service.py &

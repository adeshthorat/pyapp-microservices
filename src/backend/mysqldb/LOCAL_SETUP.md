# MySQL Docker Setup Walkthrough

I have set up a local MySQL Docker container and configured it to be accessible for your `createuser_service`.

## Changes Made
1.  **Fixed `init.sql`**: Corrected the `INSERT` statements in `src/backend/mysqldb/init.sql` to properly initialize the database with valid data.
2.  **Created `docker-compose.yaml`**: Added a `docker-compose.yaml` in `src/backend/mysqldb` to manage the MySQL container easily.
3.  **Started Database**: The MySQL container is now running and exposed on port `3306`.
4.  **Local Run Script**: Created `src/backend/createuser/run_local.ps1` to easily run your service locally with the correct environment variables.

## How to use

### Validate Database is Running
The database should be running. You can check with:
```powershell
docker ps
```
If it's not running, you can start it with:
```powershell
cd src/backend/mysqldb
docker-compose up -d
```

### Run `createuser_service` Locally
To run your python service and connect to the local docker database, use the helper script:

```powershell
cd src/backend/createuser
.\run_local.ps1
```

This script sets `DB_HOST=127.0.0.1` and other necessary credentials before launching the python script.

### Database Credentials
- **Host**: `127.0.0.1` (when running locally) or `mysqldb` (inside docker network)
- **Port**: `3306`
- **User**: `myuser`
- **Password**: `mypass`
- **Database**: `userdb`

# Database Connection Error Fix Guide

## Issue: psycopg2.ProgrammingError - invalid connection option "statement_timeout"

### Root Cause:
The error occurs because PostgreSQL connection strings don't support `statement_timeout` and `command_timeout` parameters in the way they were being added to the connection string. These parameters need to be handled differently.

### Solution Applied:
1. Removed unsupported `statement_timeout` and `command_timeout` from the connection string in `backend/src/database/connection.py`
2. Kept only the supported `sslmode=require` parameter for Neon database connections
3. Removed these unsupported parameters from the connect_args as well

### What Was Changed:
- Removed `&options=--statement_timeout%3D30000ms` from the connection string
- Removed `"statement_timeout": 30000` and `"command_timeout": 30000` from connect_args
- Kept only supported PostgreSQL connection parameters

### How to Prevent Similar Issues:
When using PostgreSQL with Neon or other services, only use supported connection parameters in the connection string:
- sslmode
- sslcert
- sslkey
- sslrootcert
- connect_timeout
- application_name

Parameters like `statement_timeout` should be set per-query or in the database configuration, not in the connection string.

### Next Steps:
1. Redeploy your backend after these changes
2. The database connection should now work without the ProgrammingError
3. Authentication and other database-dependent features should work properly
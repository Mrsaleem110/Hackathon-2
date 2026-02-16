# Database Tables Creation Fix Guide

## Issue: UndefinedTable - relation "user" does not exist

### Root Cause:
The database tables (including the "user" table) have not been created in your database. This happens when:
1. Database migrations haven't been run
2. The initial table creation scripts haven't executed
3. The database is fresh and empty

### Solution Steps:

#### 1. Check Your Alembic Migrations
Look for migration files in `backend/alembic/versions/` directory. These should contain the table creation scripts.

#### 2. Database Initialization
The application should automatically create tables on startup. In `backend/src/api/main.py`, there should be a startup event like:

```python
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    try:
        from sqlmodel import SQLModel
        engine = get_engine()
        SQLModel.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully!")
    except Exception as e:
        logger.error(f"Error initializing database tables: {e}")
```

#### 3. Manual Table Creation (if needed)
If the automatic creation isn't working, you may need to run the database migrations manually:

```bash
# Navigate to backend directory
cd backend

# Run alembic migrations
alembic upgrade head
```

#### 4. Environment-Specific Considerations
For serverless environments like Vercel, table creation might need to happen differently since the application starts fresh on each deployment.

### Quick Fix for Vercel Deployment:

1. Make sure your `backend/src/database/connection.py` and `backend/src/api/main.py` have the proper table creation logic
2. Redeploy your backend after ensuring the table creation code is present
3. The tables should be created automatically on the first deployment

### Alternative Approach (for immediate fix):
If the automatic creation isn't working, you can create a simple initialization script that runs once to create all tables.
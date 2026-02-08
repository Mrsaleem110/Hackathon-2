# Neon Database Setup Guide

This guide explains how to set up and configure your application to use Neon as the PostgreSQL database.

## Step 1: Create a Neon Project

1. Go to [Neon Console](https://console.neon.tech/)
2. Sign up or log in to your account
3. Click "New Project"
4. Choose your region and click "Create Project"
5. Neon will create a PostgreSQL database for you automatically

## Step 2: Get Your Connection String

1. In the Neon Console, select your project
2. Go to the "Connection Details" section
3. Copy the connection string in the format:
   ```
   postgresql://username:password@endpoint.region.neon.tech/dbname
   ```

## Step 3: Update Environment Variables

Replace the placeholder in `backend.env` with your actual Neon connection string:

```env
NEON_DATABASE_URL=postgresql://username:password@endpoint.region.neon.tech/dbname
```

## Step 4: Configure Vercel Environment Variables

If deploying to Vercel, add the `NEON_DATABASE_URL` as an environment variable:

```bash
vercel env add NEON_DATABASE_URL
```

## Step 5: Verify Database Connection

You can test the database connection by running:

```bash
python test_db_connection.py
```

## Important Notes

- The application is already configured to prioritize `NEON_DATABASE_URL` over `DATABASE_URL`
- SSL is automatically configured for Neon connections
- Connection pooling is optimized for serverless environments
- The fallback remains SQLite for local development

## Troubleshooting

If you encounter connection issues:

1. Verify your connection string format
2. Ensure your Neon project allows connections from your deployment environment
3. Check that SSL parameters are correctly configured (handled automatically in the connection file)
4. Confirm that your Neon database is not in idle suspend mode

## Manual Steps Required in Neon Dashboard

After setting up the connection string:

1. **Set up database schemas and extensions** (if needed)
2. **Configure connection pooling settings** in the Neon dashboard for optimal performance
3. **Set up branch management** (Neon supports branching your database like Git)
4. **Configure IAM/users** if you need multiple access levels
5. **Set up monitoring/alerting** in the Neon dashboard
6. **Configure backup settings** if needed (Neon provides automatic backups by default)
7. **Review security settings** and IP allowlists if restricting access
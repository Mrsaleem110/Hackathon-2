# FastAPI Backend for Hackathon-2 - Vercel Deployment

This is a FastAPI backend application with user authentication, item management, and JWT-based security, configured for deployment on Vercel.

## Features

- User registration and authentication
- JWT token-based authentication
- CRUD operations for items
- SQLModel-based database models
- PostgreSQL support for production
- SQLite support for development

## Deployment on Vercel

This application is configured for deployment on Vercel. To deploy:

1. Install the Vercel CLI: `npm install -g vercel`
2. Navigate to the project root directory
3. Run `vercel` and follow the prompts
4. Set the following environment variables in Vercel:
   - `DATABASE_URL`: Your PostgreSQL database URL
   - `SECRET_KEY`: A secure random secret key for JWT tokens
   - `ALGORITHM`: JWT algorithm (default: HS256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## Alternative Deployment (GitHub Integration)

1. Push this repository to GitHub
2. Go to https://vercel.com and connect your GitHub account
3. Import your project
4. In the configuration:
   - Framework: None (or select appropriate option)
   - Root Directory: `/`
   - Build Command: Leave empty or `echo "Build not required for Python"`
   - Install Command: `cd backend && pip install -r requirements.txt`
   - Output Directory: Leave empty

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/token` - User login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/items/` - Create item
- `GET /api/v1/items/` - Get all items
- `GET /api/v1/items/{id}` - Get specific item
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{id}` - Get specific user

## Environment Variables

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for JWT tokens
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration in minutes (default: 30)
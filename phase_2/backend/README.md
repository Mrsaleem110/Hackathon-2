# FastAPI Backend for Hackathon-2

This is a FastAPI backend application with user authentication, item management, and JWT-based security.

## Features

- User registration and authentication
- JWT token-based authentication
- CRUD operations for items
- SQLModel-based database models
- PostgreSQL support for production
- SQLite support for development

## Deployment on Railway

This application is configured for deployment on Railway. To deploy:

1. Connect your GitHub repository to Railway
2. Select this backend directory for deployment
3. Set the following environment variables in Railway:
   - `DATABASE_URL`: Your PostgreSQL database URL (Railway will provide this)
   - `SECRET_KEY`: A secure random secret key for JWT tokens
   - `ALGORITHM`: JWT algorithm (default: HS256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

4. The build and deploy process will automatically use the Procfile

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
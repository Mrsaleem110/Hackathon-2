# FastAPI Backend for Todo AI Chatbot

This is the backend component of the Todo AI Chatbot application, built with FastAPI and deployed on Vercel. It integrates with Neon Database and supports Better Auth for authentication.

## Features

- 🔐 **Authentication**: Dual authentication system supporting both custom JWT and Better Auth
- 🗄️ **Database**: PostgreSQL with Neon Database integration
- 🤖 **AI Integration**: OpenAI API support for AI-powered features
- ⚡ **Serverless Ready**: Optimized for Vercel deployment
- 🌐 **CORS Support**: Comprehensive CORS configuration for frontend integration

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Authentication**: Custom JWT + Better Auth support
- **Deployment**: Vercel Serverless Functions

## Prerequisites

Before deploying, ensure you have:

1. **Node.js** and **npm** installed for Vercel CLI
2. **Vercel account** and CLI installed (`npm install -g vercel`)
3. **Neon Database** account and connection string
4. **OpenAI API key** (optional, for AI features)

## Environment Variables

Create a `.env` file with the following variables:

```bash
# Database Configuration
NEON_DATABASE_URL=postgresql://username:password@ep-summer-band-ah5itt8i-pooler.c-3.us-east-1.aws.neon.tech/neondb
DATABASE_URL=postgresql://username:password@ep-summer-band-ah5itt8i-pooler.c-3.us-east-1.aws.neon.tech/neondb

# Authentication Secrets (must be at least 32 characters)
SECRET_KEY=your-very-long-secret-key-for-jwt-tokens-at-least-32-chars-long
BETTER_AUTH_SECRET=your-very-long-better-auth-secret-key-at-least-32-chars-long

# Better Auth Configuration
BETTER_AUTH_URL=https://your-backend-domain.vercel.app
FRONTEND_URL=https://your-frontend-domain.vercel.app

# API Keys (optional)
OPENAI_API_KEY=your-openai-api-key-here

# Server Configuration
DEBUG=false
```

## Deployment to Vercel

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Set Environment Variables in Vercel Dashboard

Go to your Vercel project dashboard and set the following environment variables:

- `NEON_DATABASE_URL` - Your Neon Database connection string
- `SECRET_KEY` - At least 32 characters long
- `BETTER_AUTH_SECRET` - At least 32 characters long
- `BETTER_AUTH_URL` - Your Vercel backend URL
- `FRONTEND_URL` - Your frontend URL
- `OPENAI_API_KEY` (optional) - For AI features

### 3. Deploy

```bash
# For preview deployment
vercel

# For production deployment
vercel --prod
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/me` - Get current user info
- `GET /auth/test` - Test authentication system

### Other Endpoints
- `GET /health` - Health check
- `GET /debug/routes` - List all registered routes
- `/tasks/*` - Task management endpoints
- `/chat/*` - Chat endpoints
- `/dashboard/*` - Dashboard endpoints
- `/analysis/*` - Analytics endpoints

## Better Auth Integration

This backend is designed to work alongside Better Auth. You can:

1. Use the existing JWT authentication system
2. Integrate with Better Auth by configuring the `BETTER_AUTH_SECRET` and `BETTER_AUTH_URL`
3. The system can validate both custom JWT tokens and Better Auth tokens

## Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
cd backend
uvicorn src.api.main:app --reload --port 8000
```

## Troubleshooting

### Common Issues:

1. **Environment Variables**: Ensure all required environment variables are set
2. **Secret Length**: Make sure `SECRET_KEY` and `BETTER_AUTH_SECRET` are at least 32 characters
3. **Database Connection**: Verify your Neon Database URL is correct and accessible
4. **CORS Issues**: Check that `FRONTEND_URL` is properly set

### Debugging:

- Check the `/debug/routes` endpoint to see all available routes
- Use `/debug/cors` to verify CORS configuration
- Check the `/health` endpoint for basic connectivity

## Security Best Practices

- ✅ Use strong, random secrets (at least 32 characters)
- ✅ Enable SSL for database connections
- ✅ Use environment variables for sensitive data
- ✅ Validate all inputs and handle errors properly
- ✅ Regularly rotate secrets in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT
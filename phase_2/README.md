# Next.js/FastAPI Todo Application

Welcome to the Next.js/FastAPI Todo application! This is a full-stack application built with modern technologies that provides a complete todo management system with authentication.

## Overview

This full-stack Todo application provides:
- A modern web interface built with Next.js 14 and TypeScript
- FastAPI backend with automatic API documentation
- PostgreSQL database via Neon DB with SQLModel ORM
- Complete authentication system with user registration and login
- Responsive design that works on desktop and mobile devices

## Features

- **Full-stack application**: Next.js frontend with FastAPI backend
- **Authentication**: User registration and login system with JWT tokens
- **Todo management**: Create, read, update, and delete todos
- **Responsive design**: Works on desktop and mobile devices
- **Dark mode support**: Automatic dark/light mode based on system preference
- **Clean architecture**: Well-structured code with clear separation of concerns

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI with automatic API documentation
- **Database**: PostgreSQL via Neon DB with SQLModel ORM
- **Authentication**: JWT-based authentication system
- **ORM**: SQLModel for database interactions

## Project Structure

```
frontend/
├── app/                 # Next.js 14 app directory
│   ├── todo/           # Todo application pages
│   ├── page.tsx        # Home page
│   └── layout.tsx      # Root layout
└── package.json        # Frontend dependencies

backend/
├── app/
│   ├── api/           # API routes (v1)
│   │   └── v1/
│   │       ├── users.py
│   │       ├── items.py  # Todo items API
│   │       └── auth.py   # Authentication API
│   ├── models/        # Database models
│   ├── schemas/       # Pydantic schemas
│   ├── database.py    # Database configuration
│   └── config.py      # Configuration settings
└── main.py            # FastAPI application entry point
```

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- PostgreSQL (or Neon DB account)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file in the frontend directory with the following content:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory with your database configuration:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at http://localhost:8000

## API Endpoints

### Authentication
- `POST /api/v1/auth/token` - Login and get access token
- `POST /api/v1/auth/register` - Register a new user
- `GET /api/v1/auth/me` - Get current user info

### Items (Todos)
- `GET /api/v1/items/` - Get all items
- `GET /api/v1/items/{item_id}` - Get a specific item
- `POST /api/v1/items/` - Create a new item
- `PUT /api/v1/items/{item_id}` - Update an item
- `DELETE /api/v1/items/{item_id}` - Delete an item

## Usage

1. Visit the frontend at http://localhost:3000
2. You will be automatically redirected to the Todo application
3. Register a new account or log in if you already have one
4. Start adding, editing, and managing your todos!

## Development

### Running Tests

Frontend tests:
```bash
npm run test
```

Backend tests:
```bash
pytest
```

### API Documentation

FastAPI automatically generates API documentation at:
- http://localhost:8000/docs - Interactive API documentation (Swagger UI)
- http://localhost:8000/redoc - Alternative API documentation (ReDoc)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please open an issue in the repository.
#!/bin/bash

# Deployment script for AI Todo Chatbot (Frontend and Backend)

echo "🚀 AI Todo Chatbot Deployment Script"
echo "====================================="

# Function to check if vercel CLI is installed
check_vercel_cli() {
    if ! command -v vercel &> /dev/null; then
        echo "❌ Vercel CLI is not installed."
        echo "Please install it with: npm install -g vercel"
        exit 1
    fi
    echo "✅ Vercel CLI is installed"
}

# Function to login to vercel
login_to_vercel() {
    echo ""
    echo "🔐 Logging in to Vercel..."
    vercel login
    if [ $? -ne 0 ]; then
        echo "❌ Failed to login to Vercel"
        exit 1
    fi
    echo "✅ Successfully logged in to Vercel"
}

# Function to deploy backend
deploy_backend() {
    echo ""
    echo "📦 Deploying Backend..."
    cd backend

    # Check if vercel project is linked
    if [ ! -f .vercel/project.json ]; then
        echo "🔗 Linking backend to Vercel project..."
        vercel
    else
        echo "🔗 Backend already linked to Vercel project"
    fi

    # Deploy to production
    echo "📤 Deploying backend to production..."
    vercel --prod --confirm

    if [ $? -eq 0 ]; then
        echo "✅ Backend deployed successfully!"
        BACKEND_URL=$(vercel --scope production --token $VERCEL_TOKEN 2>/dev/null | grep -o 'https://[^ ]*.vercel.app' | head -n 1)
        if [ ! -z "$BACKEND_URL" ]; then
            echo "🌐 Backend URL: $BACKEND_URL"
        fi
    else
        echo "❌ Backend deployment failed!"
        exit 1
    fi

    cd ..
}

# Function to deploy frontend
deploy_frontend() {
    echo ""
    echo "📦 Deploying Frontend..."
    cd frontend

    # Check if vercel project is linked
    if [ ! -f .vercel/project.json ]; then
        echo "🔗 Linking frontend to Vercel project..."
        vercel
    else
        echo "🔗 Frontend already linked to Vercel project"
    fi

    # Deploy to production
    echo "📤 Deploying frontend to production..."
    vercel --prod --confirm

    if [ $? -eq 0 ]; then
        echo "✅ Frontend deployed successfully!"
        FRONTEND_URL=$(vercel --scope production --token $VERCEL_TOKEN 2>/dev/null | grep -o 'https://[^ ]*.vercel.app' | head -n 1)
        if [ ! -z "$FRONTEND_URL" ]; then
            echo "🌐 Frontend URL: $FRONTEND_URL"
        fi
    else
        echo "❌ Frontend deployment failed!"
        exit 1
    fi

    cd ..
}

# Main deployment process
main() {
    echo "Starting deployment process..."

    check_vercel_cli
    login_to_vercel

    echo ""
    read -p "Do you want to deploy the backend first? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        deploy_backend
    fi

    echo ""
    read -p "Do you want to deploy the frontend? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        deploy_frontend
    fi

    echo ""
    echo "🎉 Deployment process completed!"
    echo "Remember to:"
    echo "1. Add all required environment variables to both projects"
    echo "2. Update CORS settings in backend if needed"
    echo "3. Test your deployed application"
}

# Run the main function
main "$@"
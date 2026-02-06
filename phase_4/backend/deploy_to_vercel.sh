#!/bin/bash

# Deployment script for Vercel backend
# This script helps verify configuration before deploying to Vercel

echo "🔍 Verifying backend configuration for Vercel deployment..."

# Check if we're in the backend directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Please run this script from the backend directory."
    exit 1
fi

echo "✅ Found vercel.json configuration"

# Check Python dependencies
if [ ! -f "requirements-vercel.txt" ]; then
    echo "❌ Error: requirements-vercel.txt not found."
    exit 1
fi

echo "✅ Found requirements-vercel.txt"

# Check environment validation
echo "🧪 Testing environment variable validation..."
python -c "
import os
from src.utils.env_validator import validate_environment
print('Testing environment validation...')
try:
    validate_environment()
    print('✅ Environment validation passed')
except SystemExit as e:
    if e.code != 0:
        print('❌ Environment validation failed')
        exit(1)
    else:
        print('✅ Environment validation passed')
"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "⚠️  Warning: Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo "✅ Vercel CLI is available"

# Display important environment variables status
echo ""
echo "📋 Current environment variable status:"
echo "   DATABASE_URL: $(if [ -n \"$DATABASE_URL\" ]; then echo "SET"; else echo "NOT SET (will use fallback in serverless)"; fi)"
echo "   SECRET_KEY: $(if [ -n \"$SECRET_KEY\" ]; then echo "SET ($(echo -n $SECRET_KEY | wc -c) chars)"; else echo "NOT SET (will use fallback in serverless)"; fi)"
echo "   BETTER_AUTH_SECRET: $(if [ -n \"$BETTER_AUTH_SECRET\" ]; then echo "SET ($(echo -n $BETTER_AUTH_SECRET | wc -c) chars)"; else echo "NOT SET (will use fallback in serverless)"; fi)"

echo ""
echo "💡 Remember: For production deployment, ensure all secrets are at least 32 characters long."

# Check if there are any pending git changes
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "⚠️  Warning: You have uncommitted changes. Consider committing before deployment:"
    echo "   git add ."
    echo "   git commit -m \"Prepare for Vercel deployment\""
fi

echo ""
echo "🚀 To deploy to Vercel, run:"
echo "   vercel --prod"
echo ""
echo "📝 For more details, see VERCEL_DEPLOYMENT_CHECKLIST.md"
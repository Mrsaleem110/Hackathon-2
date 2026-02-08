#!/bin/bash
# Deployment script for FastAPI backend to Vercel
# This script prepares the backend for deployment and provides instructions

echo "🚀 Preparing FastAPI backend for Vercel deployment..."

# Check if we're in the backend directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the backend directory."
    exit 1
fi

echo "✅ Backend directory confirmed"

# Check for required files
REQUIRED_FILES=("app.py" "requirements-vercel.txt" "vercel.json" "src/")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ] && [ ! -d "$file" ]; then
        echo "❌ Error: $file not found"
        exit 1
    fi
done

echo "✅ All required files found"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Vercel CLI. Please install it manually with: npm install -g vercel"
        exit 1
    fi
fi

echo "✅ Vercel CLI is available"

# Validate environment variables
echo "🔍 Checking environment variables..."

ENV_VARS=("NEON_DATABASE_URL" "SECRET_KEY" "BETTER_AUTH_SECRET" "BETTER_AUTH_URL")
MISSING_VARS=()

for var in "${ENV_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo "⚠️  Warning: The following environment variables are not set:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "📝 Please set these variables in your Vercel dashboard:"
    echo "   1. Go to your Vercel project dashboard"
    echo "   2. Navigate to Settings > Environment Variables"
    echo "   3. Add the missing variables listed above"
    echo "   4. See .env.example for guidance on required values"
    echo ""
fi

# Show deployment commands
echo "📋 Deployment Commands:"
echo "   To deploy to preview: vercel"
echo "   To deploy to production: vercel --prod"
echo "   To link to existing project: vercel link"
echo ""

# Run environment validation
echo "🧪 Testing environment configuration..."
python -c "
try:
    from src.utils.env_validator import validate_environment
    print('✅ Environment validation completed')
except Exception as e:
    print(f'❌ Environment validation failed: {e}')
"

echo ""
echo "🎉 Backend is ready for Vercel deployment!"
echo ""
echo "📝 Next Steps:"
echo "   1. Ensure all required environment variables are set in Vercel dashboard"
echo "   2. Run 'vercel' to deploy to preview environment"
echo "   3. Run 'vercel --prod' to deploy to production"
echo "   4. Test the deployment using the provided URL"
echo ""
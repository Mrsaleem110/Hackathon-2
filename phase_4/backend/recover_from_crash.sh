#!/bin/bash
# Emergency crash fix deployment script with static handling
# Use this when your Vercel backend has crashed (especially for 500 errors on favicon.ico)

echo "🚨 EMERGENCY: Starting crash recovery procedure..."

# Check if we're in the right directory
if [ ! -f "app_static_handling.py" ]; then
    echo "❌ Error: app_static_handling.py not found in current directory"
    exit 1
fi

echo "✅ Static-handling app file found"

# Verify vercel.json is updated
if grep -q "app_static_handling.py" vercel.json; then
    echo "✅ Vercel configuration updated to handle static files and prevent 500 errors"
else
    echo "❌ Error: vercel.json not updated to use static-handling app"
    exit 1
fi

# Check if vercel CLI is available
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo "✅ Vercel CLI is available"

# Deploy the static-handling fix
echo "🚀 Deploying static-handling crash fix to Vercel..."
vercel --prod

if [ $? -eq 0 ]; then
    echo "✅ Static-handling crash fix deployed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Visit your Vercel app URL to verify it's working"
    echo "   2. Check the /health endpoint: https://your-app.vercel.app/health"
    echo "   3. The favicon.ico 500 error should now be resolved"
    echo "   4. Verify environment variables in Vercel dashboard"
    echo "   5. Once stable, consider migrating back to full-featured app"
    echo ""
    echo "💡 Tip: The static-handling version prevents 500 errors for static files like favicon.ico"
    echo "💡 Check Vercel logs if issues persist"
else
    echo "❌ Deployment failed. Check the errors above."
    exit 1
fi
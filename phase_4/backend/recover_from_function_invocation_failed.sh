#!/bin/bash
# Recovery script specifically for FUNCTION_INVOCATION_FAILED error
# Use this when Vercel shows: "This Serverless Function has crashed."

echo "🚨 CRITICAL FIX: Resolving FUNCTION_INVOCATION_FAILED error..."

# Check if we're in the right directory
if [ ! -f "app_serverless_crash_fix.py" ]; then
    echo "❌ Error: app_serverless_crash_fix.py not found in current directory"
    exit 1
fi

echo "✅ Crash-proof handler file found"

# Verify vercel.json is updated for function invocation fix
if grep -q "app_serverless_crash_fix.py" vercel.json; then
    echo "✅ Vercel configuration updated for crash protection"
else
    echo "❌ Error: vercel.json not updated properly"
    exit 1
fi

# Check if vercel CLI is available
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo "✅ Vercel CLI is available"

# Show the error ID if available in the environment
if [ ! -z "$VERCEL_ERROR_ID" ]; then
    echo "📋 Previous error ID: $VERCEL_ERROR_ID"
fi

echo "🚀 Deploying FUNCTION_INVOCATION_FAILED fix to Vercel..."
echo "🔧 This fix uses minimal initialization to prevent serverless crashes..."

vercel --prod

if [ $? -eq 0 ]; then
    echo "✅ FUNCTION_INVOCATION_FAILED fix deployed successfully!"
    echo ""
    echo "📋 Verification Steps:"
    echo "   1. Visit: https://your-app.vercel.app/health"
    echo "   2. Check: https://your-app.vercel.app/ (should return 200)"
    echo "   3. Test: https://your-app.vercel.app/favicon.ico (should not 500)"
    echo ""
    echo "💡 This fix prevents FUNCTION_INVOCATION_FAILED by:"
    echo "   - Using lightweight initialization"
    echo "   - Implementing multiple crash protection layers"
    echo "   - Handling static files properly"
    echo "   - Reducing memory usage (512MB)"
    echo "   - Shorter timeout (10s) for faster recovery"
    echo ""
    echo "🔄 The server should now be stable. Monitor the logs for any remaining issues."
else
    echo "❌ Deployment failed. Check the errors above."
    echo "📋 If problems persist:"
    echo "   1. Verify environment variables in Vercel dashboard"
    echo "   2. Check Vercel logs for specific error details"
    echo "   3. Ensure SECRET_KEY and DATABASE_URL are properly set"
    exit 1
fi
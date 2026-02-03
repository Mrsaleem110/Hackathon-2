#!/bin/bash
# Emergency crash fix deployment script
# Use this when your Vercel backend has crashed

echo "🚨 EMERGENCY: Starting crash recovery procedure..."

# Check if we're in the right directory
if [ ! -f "app_crash_fix.py" ]; then
    echo "❌ Error: app_crash_fix.py not found in current directory"
    exit 1
fi

echo "✅ Crash fix file found"

# Verify vercel.json is updated
if grep -q "app_crash_fix.py" vercel.json; then
    echo "✅ Vercel configuration updated to use crash fix"
else
    echo "❌ Error: vercel.json not updated to use crash fix"
    exit 1
fi

# Check if vercel CLI is available
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

echo "✅ Vercel CLI is available"

# Deploy the crash fix
echo "🚀 Deploying crash fix to Vercel..."
vercel --prod

if [ $? -eq 0 ]; then
    echo "✅ Crash fix deployed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Visit your Vercel app URL to verify it's working"
    echo "   2. Check the /health endpoint to confirm operation"
    echo "   3. Verify environment variables in Vercel dashboard"
    echo "   4. Once stable, consider migrating back to full-featured app"
    echo ""
    echo "💡 Tip: Check Vercel logs if issues persist"
else
    echo "❌ Deployment failed. Check the errors above."
    exit 1
fi
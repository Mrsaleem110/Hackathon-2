# Vercel Configuration Fix

## Issue Resolved

The error "The `functions` property cannot be used in conjunction with the `builds` property. Please remove one of them." has been fixed.

## Changes Made

### 1. Updated `vercel.json`
The configuration has been updated from the deprecated `builds` format to the modern `functions` format:

**Old (deprecated):**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/app.py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.11",
        "installCommand": "pip install -r backend/requirements-vercel.txt"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend/app.py"
    }
  ]
}
```

**New (current - fixed):**
```json
{
  "version": 2,
  "functions": {
    "backend/app.py": {
      "runtime": "python3.11",
      "memory": 1024,
      "maxDuration": 10
    }
  },
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend/app.py"
    }
  ]
}
```

### 2. Key Improvements
- Removed conflicting `builds` property
- Added `functions` property with proper configuration
- Included memory allocation (1024MB) for better performance
- Set max duration to 10 seconds for longer-running operations
- Dependencies are now automatically handled via `requirements.txt`

### 3. Requirements File
- Both `requirements.txt` and `requirements-vercel.txt` exist in the backend folder
- Vercel will automatically use `requirements.txt` for dependency installation

## Deployment Steps

Now you can deploy without the configuration error:

```bash
cd backend
vercel --prod
```

Or use the deployment helper:
```bash
python ../deploy_backend.py
```

## Benefits of the New Configuration

1. **Modern Vercel Standard**: Uses current best practices
2. **Better Performance**: Explicit memory allocation
3. **Longer Execution Time**: 10-second timeout for complex operations
4. **Cleaner Syntax**: Simpler and more maintainable
5. **Automatic Dependency Installation**: No need for custom install commands

The configuration is now fully compatible with Vercel's current platform requirements.
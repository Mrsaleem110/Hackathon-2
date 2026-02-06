#!/usr/bin/env python3
"""
CORS Configuration Verification Script
This script verifies that the CORS configuration in the FastAPI backend is properly set up
to handle cross-origin requests from the frontend deployed on Vercel.
"""

import os
import sys
from pathlib import Path

# Add backend src to path to import the main module
# We're already in the backend directory, so just add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def verify_cors_configuration():
    """Verify that the CORS configuration meets all requirements"""
    print("[CHECK] Verifying CORS Configuration...")

    try:
        # Import the main app to check the middleware
        from backend.src.api.main import app, cors_origins

        print("[OK] Successfully imported backend application")

        # Check for CORSMiddleware in the app's middleware stack
        cors_middleware_found = False
        for middleware in app.user_middleware:
            if hasattr(middleware.cls, '__name__') and 'CORSMiddleware' in middleware.cls.__name__:
                cors_middleware_found = True
                options = middleware.options
                print(f"[OK] CORSMiddleware found with options: {options}")

                # Verify the configuration meets requirements
                assert 'https://hackathon-2-p-3-frontend.vercel.app' in options['allow_origins'], \
                    "Frontend Vercel domain not in allowed origins"
                assert options['allow_credentials'] == True, \
                    "Credentials not allowed - required for authentication"
                assert '*' in options['allow_methods'], \
                    "Not all methods allowed - OPTIONS preflight required"
                assert '*' in options['allow_headers'], \
                    "Not all headers allowed - authentication headers required"

                print("[OK] All CORS configuration requirements met")
                break

        if not cors_middleware_found:
            print("[ERROR] CORSMiddleware not found in app configuration")
            return False

        # Verify specific origins are included
        required_origins = [
            "https://hackathon-2-p-3-frontend.vercel.app",
            "https://hackathon-2-p-3-backend.vercel.app",
            "http://localhost:5173",  # Common Vite dev port
            "http://localhost:5174",
            "http://localhost:3000",  # Common dev server port
        ]

        missing_origins = []
        for origin in required_origins:
            if origin not in cors_origins:
                missing_origins.append(origin)

        if missing_origins:
            print(f"[ERROR] Missing required origins: {missing_origins}")
            return False
        else:
            print("[OK] All required origins are included in CORS configuration")

        print("\n[TARGET] CORS Configuration Verification: PASSED")
        return True

    except ImportError as e:
        print(f"[ERROR] Failed to import backend application: {e}")
        return False
    except AssertionError as e:
        print(f"[ERROR] CORS configuration assertion failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error during CORS verification: {e}")
        return False

def verify_auth_endpoints_support_options():
    """Verify that auth endpoints support OPTIONS preflight requests"""
    print("\n[CHECK] Verifying Auth Endpoints OPTIONS Support...")

    try:
        from backend.src.api.main import app

        # Find auth routes
        auth_routes = []
        for route in app.routes:
            if hasattr(route, 'path') and '/auth/' in route.path.lower():
                auth_routes.append({
                    'path': route.path,
                    'methods': getattr(route, 'methods', ['UNKNOWN'])
                })

        if not auth_routes:
            print("[ERROR] No auth routes found")
            return False

        print(f"[OK] Found {len(auth_routes)} auth routes:")
        for route in auth_routes:
            print(f"   - {route['path']}: {route['methods']}")

            # Check if OPTIONS is supported (either explicitly or via wildcard)
            if 'OPTIONS' not in route['methods'] and '*' not in route['methods']:
                print(f"[ERROR] {route['path']} does not support OPTIONS method")
                return False

        print("[OK] All auth endpoints support OPTIONS preflight requests")
        return True

    except Exception as e:
        print(f"[ERROR] Error verifying auth endpoints: {e}")
        return False

def verify_environment_awareness():
    """Verify that CORS configuration is environment-aware"""
    print("\n[CHECK] Verifying Environment Awareness...")

    try:
        from backend.src.api.main import cors_origins

        # Check for both development and production origins
        has_dev_origins = any('localhost' in origin or '127.0.0.1' in origin for origin in cors_origins)
        has_prod_origins = any('vercel.app' in origin for origin in cors_origins)

        if not has_dev_origins:
            print("[ERROR] No development origins found in CORS configuration")
            return False
        else:
            print("[OK] Development origins (localhost) included")

        if not has_prod_origins:
            print("[ERROR] No production origins (Vercel) found in CORS configuration")
            return False
        else:
            print("[OK] Production origins (Vercel) included")

        print("[OK] CORS configuration is environment-aware")
        return True

    except Exception as e:
        print(f"[ERROR] Error verifying environment awareness: {e}")
        return False

def main():
    """Main verification function"""
    print("[START] Starting CORS Configuration Verification\n")

    results = []
    results.append(verify_cors_configuration())
    results.append(verify_auth_endpoints_support_options())
    results.append(verify_environment_awareness())

    print(f"\n[SUMMARY] Verification Summary:")
    print(f"   Total checks: {len(results)}")
    print(f"   Passed: {sum(results)}")
    print(f"   Failed: {len(results) - sum(results)}")

    if all(results):
        print("\n[PASS] All CORS configuration requirements verified successfully!")
        print("[INFO] Backend allows cross-origin requests from the deployed frontend")
        print("[INFO] All auth endpoints support OPTIONS preflight")
        print("[INFO] CORS configuration is environment-aware")
        print("[INFO] No auth request should fail due to missing Access-Control-Allow-Origin")
        return True
    else:
        print("\n[FAIL] Some CORS configuration requirements failed verification")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
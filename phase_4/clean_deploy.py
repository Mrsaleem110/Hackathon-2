#!/usr/bin/env python3
"""
Clean deployment script for Vercel backend
Resets all Vercel configuration and performs a fresh deployment
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def clean_vercel_config():
    """Remove existing Vercel configuration"""
    print("🧹 Cleaning existing Vercel configuration...")

    backend_dir = Path("backend")

    # Remove .vercel directory if it exists
    vercel_dir = backend_dir / ".vercel"
    if vercel_dir.exists():
        print(f"  Removing {vercel_dir}")
        shutil.rmtree(vercel_dir, ignore_errors=True)

    # Remove .env.local if it exists
    env_local = backend_dir / ".env.local"
    if env_local.exists():
        print(f"  Removing {env_local}")
        env_local.unlink()

    print("  ✓ Vercel configuration cleaned")

def verify_vercel_json():
    """Verify the vercel.json is properly configured"""
    print("🔍 Verifying vercel.json configuration...")

    vercel_json_path = Path("backend/vercel.json")

    if not vercel_json_path.exists():
        print(f"  ✗ {vercel_json_path} does not exist")
        return False

    # Read and validate the content
    try:
        import json
        with open(vercel_json_path, 'r') as f:
            config = json.load(f)

        # Check for conflicting properties
        if 'builds' in config and 'functions' in config:
            print("  ✗ Found both 'builds' and 'functions' properties - this causes conflicts")
            return False

        if 'functions' not in config:
            print("  ✗ 'functions' property not found in vercel.json")
            return False

        print("  ✓ vercel.json is properly configured")
        return True

    except Exception as e:
        print(f"  ✗ Error reading vercel.json: {e}")
        return False

def verify_app_file():
    """Verify the main app.py file exists"""
    print("🔍 Verifying app.py exists...")

    app_path = Path("backend/app.py")
    if not app_path.exists():
        print(f"  ✗ {app_path} does not exist")
        return False

    print("  ✓ app.py exists and is accessible")
    return True

def verify_requirements():
    """Verify requirements.txt exists"""
    print("🔍 Verifying requirements.txt exists...")

    req_path = Path("backend/requirements.txt")
    if not req_path.exists():
        print(f"  ✗ {req_path} does not exist")
        return False

    print("  ✓ requirements.txt exists")
    return True

def deploy_clean():
    """Perform a clean deployment"""
    print("🚀 Starting clean deployment...")

    try:
        # Change to backend directory
        os.chdir("backend")

        # Run vercel deploy with fresh configuration
        print("  Running: vercel --prod --force --confirm")
        result = subprocess.run([
            "vercel",
            "--prod",
            "--force",  # Force a new deployment
            "--confirm"  # Auto-confirm prompts
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout

        if result.returncode == 0:
            print("  ✓ Deployment successful!")
            print(result.stdout)

            # Extract and show the deployment URL
            lines = result.stdout.split('\n')
            for line in lines:
                if 'https://' in line and ('vercel.app' in line or 'now.sh' in line):
                    print(f"\n🌐 Your deployment URL: {line.strip()}")
                    break

            return True
        else:
            print(f"  ✗ Deployment failed with code {result.returncode}")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("  ✗ Deployment timed out")
        return False
    except Exception as e:
        print(f"  ✗ Deployment error: {e}")
        return False
    finally:
        # Return to original directory
        os.chdir("..")

def main():
    """Main deployment function"""
    print("🔄 Clean Vercel Deployment Script")
    print("=" * 40)

    print("\nStep 1: Cleaning existing configuration...")
    clean_vercel_config()

    print("\nStep 2: Verifying configuration files...")
    if not verify_vercel_json():
        print("\n❌ vercel.json verification failed. Please fix the configuration.")
        print("Make sure it only has 'functions' property, not 'builds'.")
        return False

    if not verify_app_file():
        print("\n❌ app.py verification failed.")
        return False

    if not verify_requirements():
        print("\n❌ requirements.txt verification failed.")
        return False

    print("\nStep 3: Performing clean deployment...")
    success = deploy_clean()

    if success:
        print("\n🎉 Deployment completed successfully!")
        print("\nNext steps:")
        print("1. Check your Vercel dashboard for the deployment URL")
        print("2. Add your environment variables in the Vercel dashboard")
        print("3. Test the /health endpoint to verify everything works")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        print("\nTroubleshooting tips:")
        print("- Make sure you have a Vercel account and are logged in")
        print("- Check that your vercel.json is properly formatted")
        print("- Verify all required files exist in the backend directory")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
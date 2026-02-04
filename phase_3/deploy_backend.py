#!/usr/bin/env python3
"""
Deployment helper script for AI-Powered Todo Chatbot backend
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required tools are installed"""
    print("Checking dependencies...")

    # Check if Python is available
    try:
        import sys
        print(f"✓ Python {sys.version} found")
    except:
        print("✗ Python not found")
        return False

    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"],
                      capture_output=True, check=True)
        print("✓ pip found")
    except:
        print("✗ pip not found")
        return False

    # Check if Vercel CLI is available
    try:
        result = subprocess.run(["vercel", "--version"],
                               capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Vercel CLI found: {result.stdout.strip()}")
        else:
            print("? Vercel CLI not found (will need to install)")
    except FileNotFoundError:
        print("? Vercel CLI not found (will need to install)")

    return True

def validate_environment():
    """Validate environment variables for deployment"""
    print("\nValidating environment variables...")

    required_vars = [
        'DATABASE_URL',
        'NEON_DATABASE_URL',
        'SECRET_KEY',
        'BETTER_AUTH_SECRET'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"✗ Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease set these variables before deploying.")
        return False
    else:
        print("✓ All required environment variables are set")
        return True

def install_vercel_cli():
    """Install Vercel CLI if not present"""
    print("\nInstalling Vercel CLI...")

    try:
        # Install Vercel CLI globally using npm
        result = subprocess.run([
            "npm", "install", "-g", "vercel"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Vercel CLI installed successfully")
            return True
        else:
            print(f"✗ Failed to install Vercel CLI: {result.stderr}")
            return False
    except FileNotFoundError:
        print("✗ npm not found. Please install Node.js first.")
        print("Visit https://nodejs.org/ to install Node.js and npm")
        return False

def deploy_to_vercel():
    """Deploy the backend to Vercel"""
    print("\nDeploying to Vercel...")

    # Change to the backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print(f"✗ Backend directory not found: {backend_dir}")
        return False

    original_dir = os.getcwd()
    try:
        os.chdir(backend_dir)

        # Run vercel deploy command
        result = subprocess.run([
            "vercel", "--prod"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Deployment successful!")
            print(result.stdout)
            return True
        else:
            print(f"✗ Deployment failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"✗ Deployment error: {str(e)}")
        return False
    finally:
        os.chdir(original_dir)

def main():
    """Main deployment function"""
    print("AI-Powered Todo Chatbot Backend Deployment Helper")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        print("\n✗ Dependencies check failed. Please install required tools.")
        sys.exit(1)

    # Validate environment (optional - just warn if missing)
    env_valid = validate_environment()
    if not env_valid:
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Deployment cancelled.")
            sys.exit(0)

    # Check if Vercel CLI is available, install if not
    vercel_available = False
    try:
        subprocess.run(["vercel", "--version"],
                      capture_output=True, check=True)
        vercel_available = True
    except FileNotFoundError:
        print("\nVercel CLI needs to be installed.")
        response = input("Install Vercel CLI? (Y/n): ")
        if response.lower() != 'n':
            if not install_vercel_cli():
                print("\n✗ Cannot proceed without Vercel CLI.")
                sys.exit(1)
            vercel_available = True
        else:
            print("\n✗ Cannot deploy without Vercel CLI.")
            sys.exit(1)

    # Proceed with deployment
    print(f"\nReady to deploy from: {os.getcwd()}/backend")
    response = input("Start deployment? (Y/n): ")

    if response.lower() != 'n':
        if deploy_to_vercel():
            print("\n🎉 Deployment completed successfully!")
            print("\nNext steps:")
            print("1. Visit your deployment URL to verify the backend is working")
            print("2. Update your frontend to use the new backend URL")
            print("3. Test the /health endpoint to confirm everything is operational")
        else:
            print("\n❌ Deployment failed. Check the error messages above.")
            sys.exit(1)
    else:
        print("\nDeployment cancelled.")
        sys.exit(0)

if __name__ == "__main__":
    main()
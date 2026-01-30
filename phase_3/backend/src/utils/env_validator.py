"""
Environment variable validator for the AI-Powered Todo Chatbot backend.
Ensures all required environment variables are set before startup.
"""

import os
import sys
from typing import List, Dict, Any


class EnvValidator:
    """Validate required environment variables for the application."""

    # Required environment variables for production
    REQUIRED_VARS = {
        "SECRET_KEY": {
            "description": "Secret key for JWT token signing",
            "validation": lambda x: len(x) >= 32 if x else False
        },
        "DATABASE_URL": {
            "description": "Database connection URL",
            "validation": lambda x: x is not None and x.startswith(('postgresql://', 'postgresql+asyncpg://', 'sqlite:///'))
        }
    }

    # Optional environment variables with defaults
    OPTIONAL_VARS = {
        "ALGORITHM": {
            "default": "HS256",
            "validation": lambda x: x in ["HS256", "HS512", "RS256"]
        },
        "ACCESS_TOKEN_EXPIRE_MINUTES": {
            "default": "30",
            "validation": lambda x: x.isdigit() and int(x) > 0
        },
        "BETTER_AUTH_SECRET": {
            "default": "your-default-secret-key-change-in-production",
            "validation": lambda x: len(x) >= 16
        }
    }

    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """
        Validate all environment variables and return status.

        Returns:
            Dictionary with validation results
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "details": {}
        }

        # Validate required variables
        for var_name, config in cls.REQUIRED_VARS.items():
            value = os.getenv(var_name)

            if value is None:
                results["valid"] = False
                error_msg = f"Missing required environment variable: {var_name} - {config['description']}"
                results["errors"].append(error_msg)
                results["details"][var_name] = {
                    "value": None,
                    "required": True,
                    "valid": False,
                    "error": "Variable not set"
                }
            elif not config["validation"](value):
                results["valid"] = False
                error_msg = f"Invalid value for required environment variable: {var_name} - {config['description']}"
                results["errors"].append(error_msg)
                results["details"][var_name] = {
                    "value": value,
                    "required": True,
                    "valid": False,
                    "error": "Value does not meet validation criteria"
                }
            else:
                results["details"][var_name] = {
                    "value": value[:10] + "..." if len(str(value)) > 10 else value,
                    "required": True,
                    "valid": True
                }

        # Validate optional variables
        for var_name, config in cls.OPTIONAL_VARS.items():
            value = os.getenv(var_name, config["default"])

            if not config["validation"](value):
                results["valid"] = False
                error_msg = f"Invalid value for environment variable: {var_name}"
                results["errors"].append(error_msg)
                results["details"][var_name] = {
                    "value": value[:10] + "..." if len(str(value)) > 10 else value,
                    "required": False,
                    "valid": False,
                    "error": "Value does not meet validation criteria"
                }
            else:
                results["details"][var_name] = {
                    "value": value[:10] + "..." if len(str(value)) > 10 else value,
                    "required": False,
                    "valid": True
                }

        # Check for common misconfigurations
        secret_key = os.getenv("SECRET_KEY", "")
        if secret_key == "your-default-secret-key-change-in-production":
            results["warnings"].append("Using default SECRET_KEY - this is insecure for production")

        better_secret = os.getenv("BETTER_AUTH_SECRET", "")
        if better_secret == "your-default-secret-key-change-in-production":
            results["warnings"].append("Using default BETTER_AUTH_SECRET - this is insecure for production")

        return results

    @classmethod
    def validate_and_exit(cls):
        """Validate environment variables and exit if validation fails."""
        results = cls.validate()

        if not results["valid"]:
            print("❌ Environment validation failed:", file=sys.stderr)
            for error in results["errors"]:
                print(f"  - {error}", file=sys.stderr)
            print("\nPlease set the required environment variables and try again.", file=sys.stderr)
            sys.exit(1)

        if results["warnings"]:
            print("⚠️  Environment validation warnings:")
            for warning in results["warnings"]:
                print(f"  - {warning}")

        print("✅ Environment validation passed")
        return results


# Convenience function for application startup
def validate_environment():
    """Validate environment variables at application startup."""
    return EnvValidator.validate_and_exit()


if __name__ == "__main__":
    # Run validation when script is executed directly
    validate_environment()
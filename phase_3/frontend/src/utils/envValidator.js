/**
 * Environment variable validator for the AI-Powered Todo Chatbot frontend.
 * Ensures all required environment variables are set before app initialization.
 */

class FrontendEnvValidator {
  /**
   * Validate required environment variables for frontend
   * @returns {Object} Validation results with errors and warnings
   */
  static validate() {
    const results = {
      valid: true,
      errors: [],
      warnings: [],
      details: {}
    };

    // Check for required environment variables
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

    if (!apiBaseUrl) {
      results.valid = false;
      results.errors.push(
        "Missing required environment variable: VITE_API_BASE_URL - API base URL for backend communication"
      );
      results.details.VITE_API_BASE_URL = {
        value: undefined,
        required: true,
        valid: false,
        error: "Variable not set"
      };
    } else {
      results.details.VITE_API_BASE_URL = {
        value: apiBaseUrl,
        required: true,
        valid: true
      };
    }

    // Check for common misconfigurations
    if (apiBaseUrl && apiBaseUrl.endsWith('/')) {
      results.warnings.push(
        "VITE_API_BASE_URL ends with a trailing slash, which may cause issues with API endpoint construction"
      );
    }

    if (apiBaseUrl && !apiBaseUrl.startsWith('http')) {
      results.warnings.push(
        "VITE_API_BASE_URL does not start with http:// or https://, which may cause connection issues"
      );
    }

    return results;
  }

  /**
   * Validate environment variables and log results
   * @returns {boolean} Whether validation passed
   */
  static validateAndLog() {
    const results = this.validate();

    if (!results.valid) {
      console.error('❌ Frontend environment validation failed:');
      results.errors.forEach(error => {
        console.error(`  - ${error}`);
      });
      console.error('\nPlease set the required environment variables and restart the application.\n');
    }

    if (results.warnings.length > 0) {
      console.warn('⚠️  Frontend environment validation warnings:');
      results.warnings.forEach(warning => {
        console.warn(`  - ${warning}`);
      });
      console.warn('');
    }

    if (results.valid && results.warnings.length === 0) {
      console.log('✅ Frontend environment validation passed');
    } else if (results.valid && results.warnings.length > 0) {
      console.log('✅ Frontend environment validation passed with warnings');
    }

    return results.valid;
  }

  /**
   * Get the API base URL with fallbacks
   * @returns {string} The API base URL
   */
  static getApiBaseUrl() {
    // Use VITE_API_BASE_URL if available, otherwise use relative paths for production
    const envBaseUrl = import.meta.env.VITE_API_BASE_URL;

    // In development, prefer the environment variable
    if (import.meta.env.DEV && envBaseUrl) {
      return envBaseUrl;
    }

    // In production, use environment variable if available, otherwise relative path
    if (!import.meta.env.DEV && envBaseUrl) {
      return envBaseUrl;
    }

    // Default to relative path for production builds
    return '';
  }
}

export default FrontendEnvValidator;
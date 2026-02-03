const { betterAuth } = require('better-auth');

// Initialize Better Auth with proper configuration for Vercel
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'fallback-better-auth-secret-change-in-production',
  baseURL: process.env.BETTER_AUTH_URL || 'https://your-domain.vercel.app', // Replace with your actual domain
  trustHost: true,
  origin: [
    process.env.FRONTEND_URL || 'https://your-frontend.vercel.app',
    'http://localhost:5173',
    'http://localhost:3000',
    'http://localhost:3001',
    'https://*.vercel.app'  // Allow all Vercel preview deployments
  ],
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Disable for testing
    password: {
      enabled: true,
      minPasswordLength: 8,
      requireSpecialChar: false
    }
  },
  database: {
    url: process.env.DATABASE_URL || process.env.NEON_DATABASE_URL || 'sqlite:///./better_auth_local.db',
    type: process.env.DATABASE_URL?.includes('postgresql') ? 'postgresql' : 'sqlite'
  }
});

// Export the auth handler for Vercel
module.exports = auth.handler;

// Also export the auth object for use in other parts of the application
module.exports.auth = auth;
import http from 'http';
import { betterAuth } from 'better-auth';
import url from 'url';

// Initialize Better Auth with email password provider
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || '$@!eem1234', // Use the secret from .env
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3000',
  trustHost: true,
  origin: [
    'http://localhost', 
    'http://localhost:80',
    'http://localhost:5173', 
    'http://localhost:3000', 
    'http://localhost:3001',
    'http://todo-frontend',
    'http://todo-frontend:80'
  ], // Allow Vite dev server and other origins
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Don't require email verification for testing
    password: {
      enabled: true,
    }
  }
});

// Create HTTP server
const server = http.createServer(async (req, res) => {
  // Add CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Access-Control-Allow-Credentials', 'true');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // Parse the URL
  const parsedUrl = url.parse(req.url, true);

  // Health check endpoint
  if (parsedUrl.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', service: 'auth-server' }));
    return;
  }

  // Handle Better Auth requests
  try {
    const response = await auth.handler(req);
    
    // If Better Auth returns a response, send it
    if (response) {
      res.writeHead(response.status || 200, {
        'Content-Type': 'application/json',
        ...response.headers
      });
      
      if (response.body) {
        res.end(JSON.stringify(response.body));
      } else {
        res.end();
      }
    } else {
      // No response from Better Auth, return 404
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Not Found' }));
    }
  } catch (error) {
    console.error('Auth handler error:', error);
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
      error: 'Internal Server Error',
      message: error.message 
    }));
  }
});

const PORT = process.env.PORT || 3001;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`Better Auth server listening on http://0.0.0.0:${PORT}`);
  console.log(`Base URL: ${process.env.BETTER_AUTH_URL || 'http://localhost:3001'}`);
});

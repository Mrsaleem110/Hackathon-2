import http from 'http';
import { betterAuth } from 'better-auth';
import { URL } from 'url'; // Import URL from 'url'
// Do not import url from 'url' here.

// Initialize Better Auth with email password provider
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || '$@!eem1234', // Use the secret from .env
  baseURL: process.env.BETTER_AUTH_URL || `http://localhost:${process.env.PORT || 3001}/api/auth`, // Use the actual server port for baseURL and include /api/auth
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
  const origin = req.headers.origin;
  if (auth.options.origin.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }
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
  const parsedUrl = new URL(req.url, `http://${req.headers.host}`); // Use new URL for robust parsing

  // Health check endpoint
  if (parsedUrl.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', service: 'auth-server' }));
    return;
  }

  // Handle Better Auth requests
  if (parsedUrl.pathname.startsWith('/api/auth')) { // Only process /api/auth paths with better-auth
    try {
      let body = '';
      if (req.method === 'POST' || req.method === 'PUT' || req.method === 'PATCH') {
        for await (const chunk of req) {
          body += chunk.toString();
        }
      }

      // Construct a Request object suitable for better-auth
      const request = new Request(parsedUrl.toString(), {
        method: req.method,
        headers: req.headers,
        body: body || undefined,
      });

      const response = await auth.handler(request);
      
      // Set response status and headers
      res.writeHead(response.status, Object.fromEntries(response.headers.entries()));

      if (response.body) {
        const responseBody = await response.text();
        res.end(responseBody);
      } else {
        res.end();
      }
    } catch (error) {
      console.error('Auth handler error:', error);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ 
        error: 'Internal Server Error',
        message: error.message 
      }));
    }
  } else {
    // Handle unknown routes outside of /api/auth
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

const PORT = process.env.PORT || 3001;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`Better Auth server listening on http://0.0.0.0:${PORT}`);
  console.log(`Base URL: ${process.env.BETTER_AUTH_URL || `http://localhost:${PORT}`}`);
});

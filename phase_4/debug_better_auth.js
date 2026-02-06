const http = require('http');
const { betterAuth } = require('better-auth');
const url = require('url');

// Initialize Better Auth with email password provider
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || '$@!eem1234', // Using the secret from .env
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3000',
  trustHost: true,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Don't require email verification for testing
  }
});

console.log('Better Auth initialized with email/password enabled');

// Create HTTP server
const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);

  console.log(`Received request: ${req.method} ${req.url}`);

  // Handle CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    console.log('Handling OPTIONS request');
    res.writeHead(200);
    res.end();
    return;
  }

  // Handle Better Auth routes
  if (req.url.startsWith('/api/auth')) {
    try {
      console.log(`Processing Better Auth request: ${req.method} ${req.url}`);

      // Better Auth expects the full path including /api/auth
      const internalUrl = `http://localhost:${server.address().port}${req.url}`;
      console.log(`Creating Request with URL: ${internalUrl}`);

      // Create a Request object for Better Auth
      let body = '';
      if (req.method === 'POST' || req.method === 'PUT') {
        for await (const chunk of req) {
          body += chunk.toString();
        }
        console.log(`Request body: ${body}`);
      }

      const request = new Request(internalUrl, {
        method: req.method,
        headers: req.headers,
        body: body || undefined
      });

      console.log('Calling auth.handler...');
      // Call Better Auth handler
      const response = await auth.handler(request);
      console.log(`Better Auth response status: ${response.status}`);

      // Set response status and headers
      res.statusCode = response.status;
      for (const [key, value] of response.headers) {
        res.setHeader(key, value);
      }

      if (response.body) {
        const responseBody = await response.text();
        console.log(`Response body length: ${responseBody.length}, first 200 chars: ${responseBody.substring(0, 200)}`);
        res.end(responseBody);
      } else {
        console.log('No response body from Better Auth');
        res.end();
      }
    } catch (error) {
      console.error('Better Auth Error:', error);
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Internal Server Error', details: error.message }));
    }
  }
  // Handle health check
  else if (parsedUrl.pathname === '/health') {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({
      status: 'ok',
      timestamp: new Date().toISOString(),
      message: 'Better Auth server is running'
    }));
  }
  // Handle unknown routes
  else {
    console.log(`Unknown route: ${req.url}`);
    res.statusCode = 404;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

// Start the server on port 10080 for consistent frontend connection
const PORT = process.env.PORT || 10080;
server.listen(PORT, 'localhost', () => {
  console.log(`Better Auth server running on port ${PORT}`);
  console.log(`Better Auth endpoints available at http://localhost:${PORT}/api/auth`);
  console.log('Ready to accept requests...');
});
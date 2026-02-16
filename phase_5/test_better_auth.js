const http = require('http');
const { betterAuth } = require('better-auth');
const url = require('url');

// Initialize Better Auth with email password provider
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'your-secret-key-change-in-production',
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3000',
  trustHost: true,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Don't require email verification for testing
  }
});

console.log("Available auth endpoints:", Object.keys(auth));

// Create HTTP server
const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);

  // Handle CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // Handle Better Auth routes
  if (req.url.startsWith('/api/auth')) {
    try {
      console.log(`Processing request: ${req.method} ${req.url}`);

      // Extract the path after /api/auth
      let internalPath = req.url.replace('/api/auth', '');
      if (internalPath === '') internalPath = '/';

      // Construct the URL that Better Auth expects
      const internalUrl = `http://localhost:${server.address().port}${internalPath}`;
      console.log(`Internal path: ${internalPath}, Internal URL: ${internalUrl}`);

      // Create a Request object for Better Auth
      let body = '';
      if (req.method === 'POST' || req.method === 'PUT') {
        for await (const chunk of req) {
          body += chunk.toString();
        }
      }

      const request = new Request(internalUrl, {
        method: req.method,
        headers: req.headers,
        body: body || undefined
      });

      console.log(`Calling auth.handler with path: ${internalPath}`);

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
        console.log(`Response body: ${responseBody.substring(0, 200)}...`); // Log first 200 chars
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
      message: 'Better Auth server is running',
      availableEndpoints: Object.keys(auth)
    }));
  }
  // Handle unknown routes
  else {
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
});
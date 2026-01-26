const http = require('http');
const { betterAuth } = require('better-auth');

// Initialize Better Auth with email password provider
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'your-secret-key-change-in-production',
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:0',
  trustHost: true,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  }
});

// Create HTTP server - let's try to handle the route matching differently
const server = http.createServer(async (req, res) => {
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

  // For all requests that start with /api/auth, forward everything after /api/auth
  // to Better Auth as if it were the root path
  if (req.url.startsWith('/api/auth')) {
    try {
      // Extract the path after /api/auth
      let internalPath = req.url.replace('/api/auth', '');
      if (internalPath === '') internalPath = '/';

      // Construct the URL that Better Auth expects
      const internalUrl = `http://localhost:${server.address().port}${internalPath}`;

      console.log(`Forwarding: ${req.method} ${req.url} -> ${internalUrl}`);

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

      // Call Better Auth handler
      const response = await auth.handler(request);

      console.log(`Better Auth responded with status: ${response.status}`);

      // Set response status and headers
      res.statusCode = response.status;
      for (const [key, value] of response.headers) {
        res.setHeader(key, value);
      }

      if (response.body) {
        const responseBody = await response.text();
        res.end(responseBody);
      } else {
        res.end();
      }
    } catch (error) {
      console.error('Better Auth Error:', error);
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Internal Server Error', details: error.message }));
    }
  } else {
    // For other routes, return 404
    res.statusCode = 404;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

// Start the server with a random port
server.listen(0, 'localhost', () => {
  const port = server.address().port;
  console.log(`Better Auth server running on port ${port}`);
  console.log(`Better Auth endpoints available at http://localhost:${port}/api/auth`);
  console.log('Try:');
  console.log(`  Register: curl -X POST http://localhost:${port}/api/auth/sign-up -H "Content-Type: application/json" -d \'{"email":"test@example.com", "password":"password123", "name":"Test User"}\'`);
  console.log(`  Login: curl -X POST http://localhost:${port}/api/auth/sign-in/email -H "Content-Type: application/json" -d \'{"email":"test@example.com", "password":"password123"}\'`);
});
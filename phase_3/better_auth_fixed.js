const http = require('http');
const { betterAuth } = require('better-auth');
const url = require('url');

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
  if (parsedUrl.pathname.startsWith('/api/auth')) {
    try {
      // Extract the actual auth route part by removing the /api/auth prefix
      const authPath = parsedUrl.pathname.replace(/^\/api\/auth/, '');
      const fullUrl = `http://localhost:${server.address().port}${req.url}`;

      // Create a new URL to manipulate the pathname
      const originalUrl = new URL(fullUrl);
      const newUrl = new URL(authPath || '/', originalUrl.origin);

      // Create a Request object with the corrected path
      let body = '';
      if (req.method === 'POST' || req.method === 'PUT') {
        for await (const chunk of req) {
          body += chunk.toString();
        }
      }

      const request = new Request(newUrl.toString(), {
        method: req.method,
        headers: req.headers,
        body: body || undefined
      });

      // Call Better Auth handler
      const response = await auth.handler(request);

      // Extract status, headers, and body from Better Auth response
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
    res.statusCode = 404;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

// Start the server with a random port
const serverInstance = server.listen(0, 'localhost', () => {
  const port = server.address().port;
  console.log(`Better Auth server running on port ${port}`);
  console.log(`Better Auth endpoints available at http://localhost:${port}/api/auth`);
});
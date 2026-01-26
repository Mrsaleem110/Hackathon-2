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

  console.log(`Incoming request: ${req.method} ${req.url}`);
  console.log(`Path starts with /api/auth: ${parsedUrl.pathname.startsWith('/api/auth')}`);

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
  if (parsedUrl.pathname.startsWith('/api/auth')) {
    try {
      // Build the full URL
      const hostname = req.headers.host ? req.headers.host.split(':')[0] : 'localhost';
      const port = server.address() ? server.address().port : (req.headers.host ? req.headers.host.split(':')[1] : '0');
      const protocol = 'http';
      const fullUrl = `${protocol}://${hostname}:${port}${req.url}`;

      console.log(`Full URL: ${fullUrl}`);

      // Create a Request object from the incoming request
      let body = '';
      if (req.method === 'POST' || req.method === 'PUT') {
        for await (const chunk of req) {
          body += chunk.toString();
        }
      }

      console.log(`Request body: ${body}`);

      const request = new Request(fullUrl, {
        method: req.method,
        headers: req.headers,
        body: body || undefined
      });

      console.log(`Calling Better Auth handler for: ${request.url}, method: ${request.method}`);

      // Call Better Auth handler
      const response = await auth.handler(request);

      console.log(`Better Auth response status: ${response.status}`);
      console.log(`Better Auth response headers:`, [...response.headers]);

      // Extract status, headers, and body from Better Auth response
      res.statusCode = response.status;
      for (const [key, value] of response.headers) {
        res.setHeader(key, value);
      }

      if (response.body) {
        const responseBody = await response.text();
        console.log(`Better Auth response body: ${responseBody.substring(0, 200)}...`);
        res.end(responseBody);
      } else {
        console.log('No response body from Better Auth');
        res.end();
      }
    } catch (error) {
      console.error('Better Auth Error:', error);
      console.error('Error stack:', error.stack);
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

// Start the server with a random port
const serverInstance = server.listen(0, 'localhost', () => {
  const port = server.address().port;
  console.log(`Better Auth server running on port ${port}`);
  console.log(`Better Auth endpoints available at http://localhost:${port}/api/auth`);
});
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

  console.log(`\n=== INCOMING REQUEST ===`);
  console.log(`Method: ${req.method}`);
  console.log(`URL: ${req.url}`);
  console.log(`Parsed Pathname: ${parsedUrl.pathname}`);
  console.log(`Full Path: ${req.url}`);

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

  // Log what API methods are available
  console.log(`Available API methods:`, Object.keys(auth.api));

  // Handle Better Auth routes
  if (parsedUrl.pathname.startsWith('/api/auth')) {
    try {
      // Extract the actual auth route part (remove /api/auth prefix)
      const authPath = parsedUrl.pathname.replace('/api/auth', '');
      const fullUrl = `http://localhost:${server.address().port}${req.url}`;

      console.log(`Auth path extracted: ${authPath}`);
      console.log(`Full URL constructed: ${fullUrl}`);

      // Create a Request object from the incoming request
      let body = '';
      if (req.method === 'POST' || req.method === 'PUT') {
        for await (const chunk of req) {
          body += chunk.toString();
        }
      }

      console.log(`Request body: ${body || '(empty)'}`);

      // Create the Request object
      const request = new Request(fullUrl, {
        method: req.method,
        headers: req.headers,
        body: body || undefined
      });

      console.log(`Created Request object - URL: ${request.url}, Method: ${request.method}`);

      // Call Better Auth handler
      console.log(`Calling auth.handler...`);
      const response = await auth.handler(request);
      console.log(`Received response - Status: ${response.status}`);

      // Extract status, headers, and body from Better Auth response
      res.statusCode = response.status;
      for (const [key, value] of response.headers) {
        res.setHeader(key, value);
      }

      if (response.body) {
        const responseBody = await response.text();
        console.log(`Response body: ${responseBody}`);
        res.end(responseBody);
      } else {
        console.log(`No response body`);
        res.end();
      }
    } catch (error) {
      console.error('Better Auth Error:', error.message);
      console.error('Error stack:', error.stack);
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Internal Server Error', details: error.message }));
    }
  } else {
    console.log(`Path does not start with /api/auth`);
    res.statusCode = 404;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

// Start the server with a random port
const serverInstance = server.listen(0, 'localhost', () => {
  const port = server.address().port;
  console.log(`\n=== SERVER STARTED ===`);
  console.log(`Better Auth server running on port ${port}`);
  console.log(`Better Auth endpoints available at http://localhost:${port}/api/auth`);
  console.log(`Available API methods:`, Object.keys(auth.api));
});
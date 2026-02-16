const http = require('http');
const { betterAuth } = require('better-auth');
const url = require('url');

// Initialize Better Auth with email password provider
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || '$@!eem1234',
  baseURL: process.env.BETTER_AUTH_URL || `http://localhost:${process.env.PORT || 3001}`,
  trustHost: true,
  origin: ['http://localhost:5173', 'http://localhost:3000', 'http://localhost:3001'],
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
    password: {
      enabled: true,
    }
  }
});

// Allowed origins for CORS
const ALLOWED_ORIGINS = [
  'http://localhost:3000',
  'http://localhost:5173',
  'http://localhost:3001'
];

// Create HTTP server
const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);
  
  // Get the origin from the request
  const origin = req.headers.origin;
  
  // Handle CORS - use specific origin instead of wildcard when credentials are needed
  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Access-Control-Allow-Credentials', 'true');
  }
  
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
      const requestUrl = new URL(req.url, `http://localhost:${process.env.PORT || 3001}`);

      let body = '';
      if (req.method === 'POST' || req.method === 'PUT') {
        for await (const chunk of req) {
          body += chunk.toString();
        }
      }

      const request = new Request(requestUrl.toString(), {
        method: req.method,
        headers: req.headers,
        body: body || undefined
      });

      const response = await auth.handler(request);

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

const PORT = process.env.PORT || 3001;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`Better Auth server running on port ${PORT}`);
  console.log(`Better Auth endpoints available at http://localhost:${PORT}/api/auth`);
});

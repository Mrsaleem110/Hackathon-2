const express = require('express');
const { betterAuth } = require('better-auth');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3001;

// Initialize Better Auth
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || '$@!eem1234',
  baseURL: process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : 'http://localhost:3000',
  origin: process.env.VERCEL_URL ? [`https://${process.env.VERCEL_URL}`] : ['http://localhost:5173', 'http://localhost:3000', 'http://localhost:3001'],
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
    password: {
      enabled: true,
    }
  }
});

app.use(cors({
  origin: auth.origin,
  credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// All auth routes are handled by the auth.handler
app.all('/api/auth/*', async (req, res) => {
  try {
    const response = await auth.handler(req);
    res.status(response.status);
    response.headers.forEach((value, key) => {
      res.setHeader(key, value);
    });
    if (response.body) {
      const body = await response.text();
      res.send(body);
    } else {
      res.end();
    }
  } catch (error) {
    console.error('Better Auth Error:', error);
    res.status(500).json({ error: 'Internal Server Error', details: error.message });
  }
});

app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    message: 'Better Auth server is running'
  });
});

// Catch all other routes
app.all('*', (req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

if (require.main === module) {
  app.listen(port, () => {
    console.log(`Better Auth server running on port ${port}`);
  });
}

module.exports = app;

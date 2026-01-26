const express = require('express');
const cors = require('cors');
const { betterAuth } = require('better-auth');
const { toNodeHandler } = require('better-auth/node');

// Initialize Better Auth with email password provider
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'your-secret-key-change-in-production',
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3000',
  trustHost: true,
  emailAndPassword: {
    enabled: true,
  }
});

const app = express();

// Enable CORS for communication with Next.js and FastAPI
app.use(cors({
  origin: [
    'http://localhost:3000',  // Node.js server
    'http://localhost:5173',  // Vite dev server
    'http://localhost:8000',  // FastAPI server
    'http://localhost:8001',  // Alternative FastAPI port
    'http://127.0.0.1:8000',  // Alternative FastAPI address
    'http://127.0.0.1:8001',  // Alternative FastAPI address
  ],
  credentials: true
}));

app.use(express.json());

// Mount Better Auth routes using the Node.js handler
app.use('/api/auth', toNodeHandler(auth));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Better Auth server running on port ${PORT}`);
  console.log(`Better Auth endpoints available at http://localhost:${PORT}/api/auth`);
});
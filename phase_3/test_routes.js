const { betterAuth } = require('better-auth');
const { toNodeHandler } = require('better-auth/node');
const express = require('express');

// Initialize Better Auth
const auth = betterAuth({
  secret: 'test-secret-for-debugging-purposes-only',
  emailAndPassword: {
    enabled: true
  }
});

console.log("Available API endpoints:");
console.log(Object.keys(auth.api));

// Create a simple Express app to test the handler
const app = express();
app.use(express.json());

// Mount the Better Auth handler
const nodeHandler = toNodeHandler(auth);
app.use('/api/auth', nodeHandler);

// Start server on a different port to test
const PORT = 4000;
app.listen(PORT, () => {
  console.log(`Test server running on port ${PORT}`);
  console.log(`Available routes will be accessible at http://localhost:${PORT}/api/auth`);

  // Give some time to see what happens
  setTimeout(() => {
    console.log("\nNow you can test the endpoints:");
    console.log("- POST http://localhost:4000/api/auth/sign-up");
    console.log("- POST http://localhost:4000/api/auth/sign-in/email");
    console.log("- GET http://localhost:4000/api/auth/session");
  }, 1000);
});
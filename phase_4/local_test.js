// This script will help debug the serverless function locally.

const request = require('supertest');
const app = require('./better_auth_debug.js'); // Import your express app

// Vercel environment variables mock
process.env.VERCEL_URL = 'localhost:3001';
process.env.BETTER_AUTH_SECRET = 'a-long-secret-key-that-is-at-least-32-characters-long';


console.log('Starting local test...');

request(app)
  .get('/health') // We'll make a request to the health check endpoint first
  .expect(200)
  .end(function(err, res) {
    if (err) {
      console.error('Error during local test:');
      console.error(err);
      throw err;
    }
    console.log('Local test successful!');
    console.log('Response:', res.body);
  });

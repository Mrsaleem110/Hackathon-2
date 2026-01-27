import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    rollupOptions: {
      // Additional rollup options if needed
    }
  },
  // Handle client-side routing for SPA deployment
  server: {
    host: true,
    proxy: {
      // Proxy Better Auth requests to the Better Auth server (most specific first)
      '/api/auth/': {
        target: 'http://localhost:10080',
        changeOrigin: true,
        secure: false,
        // Preserve cookies and other headers that Better Auth might need
        cookieDomainRewrite: 'localhost',
        cookiePathRewrite: '/',
      },
      // Proxy other specific API requests to the FastAPI backend
      '/tasks': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      },
      '/chat': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      },
      // Proxy all other /api requests to the FastAPI backend (most general last)
      '/api/': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  // This helps with handling client-side routing in production
  appType: 'spa', // Single Page Application
});
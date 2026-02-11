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
      '/api/auth': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        secure: false,
        // Preserve all headers to ensure Better Auth gets full request context
        autoRewrite: true,
        ws: true,
      },
      // Proxy other specific API requests to the FastAPI backend
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/tasks': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/chat': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      // Proxy all other /api requests to the FastAPI backend (most general last)
      '/api/': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  // This helps with handling client-side routing in production
  appType: 'spa', // Single Page Application
});
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
      // Only proxy actual API endpoints, not React Router pages
      '/auth/': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      },
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
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  // This helps with handling client-side routing in production
  appType: 'spa', // Single Page Application
});
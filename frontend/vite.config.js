// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // Force all React imports to use the same instance
      'react': path.resolve('./node_modules/react'),
      'react-dom': path.resolve('./node_modules/react-dom'),
    },
  },
  optimizeDeps: {
    // Ensure React is pre-bundled correctly
    include: ['react', 'react-dom'],
    force: true, // Force re-optimization
  },
  build: {
    outDir: 'dist',
  },
  server: {
    host: true, // Allow external connections
    allowedHosts: [
      'partle.rubenayla.xyz',
      '91.98.68.236',
      'localhost',
      '127.0.0.1'
    ],
    historyApiFallback: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});

// vite.config.js
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig(({ mode }) => {
  // Load env vars from parent directory
  loadEnv(mode, '../', 'VITE_');
  
  return {
    envDir: '../', // Tell Vite to look for .env files in parent directory
    plugins: [react()],
    resolve: {
      alias: {
        // Force all React imports to use the same instance
        'react': path.resolve('./node_modules/react'),
        'react-dom': path.resolve('./node_modules/react-dom'),
      },
    },
    optimizeDeps: {
      // Force ESM resolution for React
      include: ['react', 'react-dom', 'react/jsx-runtime'],
      force: true,
      esbuildOptions: {
        // Ensure proper ESM transformation
        format: 'esm',
        target: 'esnext'
      }
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
  };
});
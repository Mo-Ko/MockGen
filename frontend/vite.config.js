// File: frontend/vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ command }) => {
  // Base configuration for both dev and build
  const config = {
    plugins: [vue()],
  };

  if (command === 'serve') {
    // This is for local development (`npm run dev`)
    return {
      ...config,
      server: {
        port: 5173,
        // The proxy tells Vite to forward API requests to your local backend
        proxy: {
          '/generate': 'http://127.0.0.1:8000',
          '/health': 'http://127.0.0.1:8000',
          '/history': 'http://127.0.0.1:8000',
        }
      }
    };
  } else {
    // This is for production build (`npm run build`)
    return {
      ...config,
      base: '/static/', // This is the setting for Docker
    };
  }
});
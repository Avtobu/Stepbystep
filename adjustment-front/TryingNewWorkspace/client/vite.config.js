import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // @ → src/ (so "@/api" resolves to "src/api")
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      // All /api/* requests → Flask on port 5000
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})

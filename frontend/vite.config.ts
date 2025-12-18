import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  root: '.',
  publicDir: 'public',
  plugins: [react()],
  base: '/Sistema-de-Escalas-para-Equipes-de-Volunt-rios/',
  server: {
    port: 5173,
    host: '0.0.0.0',
    strictPort: false,
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
})

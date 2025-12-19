import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig(({ command }) => ({
  root: '.',
  publicDir: 'public',
  plugins: [react()],
  // Em dev, base='/' | Em build (GitHub Pages), base='/<repo>/'
  base: command === 'build'
    ? '/Sistema-de-Escalas-para-Equipes-de-Volunt-rios/'
    : '/',
  server: {
    port: 5173,
    host: '0.0.0.0',
    strictPort: false,
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
}))

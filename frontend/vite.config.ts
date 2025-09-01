import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import eslint from 'vite-plugin-eslint';
import { ViteWebfontDownload } from 'vite-plugin-webfont-dl';

// https://vitejs.dev/config/
// biome-ignore lint/style/noDefaultExport: Expected
export default defineConfig({
  plugins: [
    react(),
    eslint(),
    ViteWebfontDownload([
      'https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700;1000&display=swap',
    ]),
  ],
  resolve: {
    alias: {
      '@base': '/src',
      '@shared': '/src/shared-components',
      '@clients': '/src/clients',
      '@labour': '/src/pages/Labour',
      '@subscription': '/src/pages/Subscription',
      '@subscribe': '/src/pages/Subscribe',
      '@subscriptions': '/src/pages/Subscriptions',
    },
  },
  build: {
    chunkSizeWarningLimit: 1000,
    target: 'esnext',
    minify: 'esbuild',
    sourcemap: true,
  },
});

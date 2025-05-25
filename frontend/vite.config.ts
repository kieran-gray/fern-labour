import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import eslint from 'vite-plugin-eslint';

// https://vitejs.dev/config/
// biome-ignore lint/style/noDefaultExport: Expected
export default defineConfig({
  plugins: [react(), eslint()],
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
});

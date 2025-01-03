import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/
// biome-ignore lint/style/noDefaultExport: Expected
export default defineConfig({plugins: [react()]})

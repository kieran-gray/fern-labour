import react from '@vitejs/plugin-react';
import { type UserConfigExport, defineConfig, loadEnv } from 'vite';

// https://vitejs.dev/config/
// biome-ignore lint/style/noDefaultExport: Expected
export default defineConfig(({ command, mode }) => {

  const commonConfig: UserConfigExport = {
    plugins: [react()],
    base: '/'
  };

  // command === 'build'
  return {
    ...commonConfig
  };
});

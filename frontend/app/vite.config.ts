import * as path from 'node:path';
import vue from '@vitejs/plugin-vue';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const envPrefix = 'CONSTRUCTOR_';
  const env = loadEnv(mode, '.', envPrefix);
  const base = env.CONSTRUCTOR_APP_PREFIX || '/';

  return {
    envPrefix,
    base,
    server: {
      port: +env.CONSTRUCTOR_DEV_PORT,
      headers: {
        'Service-Worker-Allowed': '/',
      },
      proxy: {
        '/api': {
          target: env.CONSTRUCTOR_APP_URL,
          changeOrigin: true,
        },
      },
    },
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve('src'),
      },
    },
  };
});

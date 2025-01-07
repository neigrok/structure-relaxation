import { createPinia } from 'pinia';
import type { App, Plugin } from 'vue';

export const pinia: Plugin = {
  install(app: App) {
    createPinia().install(app);
  },
};

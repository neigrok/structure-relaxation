import {
  createGoFormPlugin,
  createGoBasePlugin,
  createGoColorSchemeProviderPlugin,
} from '@constructor/ui';
import type { App, Plugin } from 'vue';
import { generateMessage } from '@/services/veeValidate';

export const baseUi: Plugin = {
  install(app: App) {
    createGoBasePlugin().install(app);
    createGoFormPlugin({ generateMessage }).install(app);
    createGoColorSchemeProviderPlugin().install(app);
  },
};

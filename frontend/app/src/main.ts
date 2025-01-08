import '@/assets/styles/index.pcss';
import { createApp } from 'vue';
import { pinia } from '@/plugins/pinia';
import { router } from '@/router/router';
import App from './App.vue';

createApp(App).use(pinia).use(router).mount('#app');

import '@/assets/styles/index.pcss';
import { createApp } from 'vue';
import { pinia } from '@/plugins/pinia';
import { router } from '@/router/router';
import App from './App.vue';
import Toast from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-sugar.css';

createApp(App).use(pinia).use(router).use(Toast).mount('#app');

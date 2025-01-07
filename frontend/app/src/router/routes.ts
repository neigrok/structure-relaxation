import type { RouteRecordRaw } from 'vue-router';

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'structures',
    component: () => import('@/modules/structure/views/Structures.vue'),
    children: [
      {
        path: ':structureId',
        name: 'structure',
        component: () => import('@/modules/structure//views/Structure.vue'),
      },
    ],
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/',
  },
];

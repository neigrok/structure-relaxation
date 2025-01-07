import { getFileTypes, recommended } from '@constructor/configs/eslintConfig';

export default [
  ...recommended({
    restrictedZones: true,
  }),
  {
    files: getFileTypes().all,
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: ['@constructor/ui/src/*'],
              message: 'Please use import from @constructor/ui',
            },
            // TODO: webstorm bug https://youtrack.jetbrains.com/issue/WEB-61927/vue3-auto-imports-from-vue-dist-vue-on-paste
            {
              group: ['vue/dist/vue'],
              message: 'Please use import from vue',
            },
          ],
        },
      ],
    },
  },
];

const getFileTypes = () => ({
  all: ['*.js', '*.ts', '*.vue'],
});

const recommended = () => [
  {
    files: getFileTypes().all,
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: ['src/*'],
              message: 'Please use import from the appropriate module',
            },
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
              group: ['src/*'],
              message: 'Please use import from the appropriate module',
            },
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

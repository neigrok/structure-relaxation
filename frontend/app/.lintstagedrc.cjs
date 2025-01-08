module.exports = {
  '*.{vue,ts,mts,cts,js,mjs,cjs,css,pcss,html,yml,yaml}': ['prettier --write'],
  '*.{vue,ts,mts,cts,js,mjs,cjs}|package.json': ['eslint --fix'],
  '*.vue': ['stylelint --fix'],
  '*.{pcss,css}': ['stylelint --fix'],
};

const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/generated',
  timeout: 30000,
  retries: 0,
  use: {
    baseURL: 'http://localhost:3000',
    headless: true,
    screenshot: 'only-on-failure',
  },
  reporter: [['html'], ['json', { outputFile: 'data/results/test-results.json' }]],
});

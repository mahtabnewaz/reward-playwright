import { test, expect } from '@playwright/test';

test('should display the correct page title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle('Sample App');
});
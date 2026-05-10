import { test, expect } from '@playwright/test';

test('should show login page by default', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByTestId('login-title')).toBeVisible();
});
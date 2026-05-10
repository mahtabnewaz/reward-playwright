import { test, expect } from '@playwright/test';

test('page loads within 3 seconds', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByTestId('nav-login')).toBeVisible({ timeout: 3000 });
});
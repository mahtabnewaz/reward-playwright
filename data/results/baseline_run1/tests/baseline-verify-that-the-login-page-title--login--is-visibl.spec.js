import { test, expect } from '@playwright/test';

test('should display login page title when page loads', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await expect(page.getByTestId('login-title')).toBeVisible();
  await expect(page.getByTestId('login-title')).toContainText('Login');
});
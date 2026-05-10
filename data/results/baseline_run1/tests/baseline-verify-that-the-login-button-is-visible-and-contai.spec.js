import { test, expect } from '@playwright/test';

test('should display login button with text Login', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  const loginButton = page.getByTestId('login-button');
  await expect(loginButton).toBeVisible();
  await expect(loginButton).toContainText('Login');
});
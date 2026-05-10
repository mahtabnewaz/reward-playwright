import { test, expect } from '@playwright/test';

test('should show error message for invalid credentials', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await page.getByTestId('username-input').fill('invalid-username');
  await page.getByTestId('password-input').fill('invalid-password');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-error')).toContainText('Invalid username or password');
});
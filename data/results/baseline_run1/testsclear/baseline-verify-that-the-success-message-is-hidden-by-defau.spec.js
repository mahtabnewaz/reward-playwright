import { test, expect } from '@playwright/test';

test('should hide success message by default and show after successful login', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await expect(page.getByTestId('login-success')).not.toBeVisible();
  await page.getByTestId('username-input').fill('username');
  await page.getByTestId('password-input').fill('password');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-success')).toBeVisible();
});
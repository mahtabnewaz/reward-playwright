import { test, expect } from '@playwright/test';

test('login error message disappears on retry', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await page.getByTestId('username-input').fill('invalid-username');
  await page.getByTestId('password-input').fill('invalid-password');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-error')).toBeVisible();
  await page.getByTestId('username-input').fill('valid-username');
  await page.getByTestId('password-input').fill('valid-password');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-error')).not.toBeVisible();
});
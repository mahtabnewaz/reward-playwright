import { test, expect } from '@playwright/test';

test('should show success message after valid login', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await page.getByTestId('username-input').fill('admin');
  await page.getByTestId('password-input').fill('password123');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-success')).toBeVisible();
});
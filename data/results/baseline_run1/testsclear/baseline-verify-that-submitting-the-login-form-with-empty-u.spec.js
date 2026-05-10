import { test, expect } from '@playwright/test';

test('should show error when submitting login form with empty fields', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-error')).toContainText('Please fill in all fields');
});
import { test, expect } from '@playwright/test';

test('should show fill-all-fields error when only username is entered', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await page.getByTestId('username-input').fill('testuser');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-error')).toContainText('Please fill all fields');
});
import { test, expect } from '@playwright/test';

test('should have password input field of type password', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  const passwordInput = await page.getByTestId('password-input');
  await expect(passwordInput).toBeVisible();
  const inputType = await passwordInput.getAttribute('type');
  await expect(inputType).toBe('password');
});
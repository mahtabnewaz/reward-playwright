import { test, expect } from '@playwright/test';

test('password field masks input characters', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  const passwordInput = page.getByTestId('password-input');
  await passwordInput.click();
  await passwordInput.type('password123');
  const inputType = await passwordInput.getAttribute('type');
  expect(inputType).toBe('password');
});
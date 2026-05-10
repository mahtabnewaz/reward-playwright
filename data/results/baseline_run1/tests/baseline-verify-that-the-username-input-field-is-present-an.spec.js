import { test, expect } from '@playwright/test';

test('should have username input field with placeholder', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  const usernameInput = page.getByTestId('username-input');
  await expect(usernameInput).toBeVisible();
  const placeholder = await usernameInput.getAttribute('placeholder');
  await expect(placeholder).toBe('Enter username');
});
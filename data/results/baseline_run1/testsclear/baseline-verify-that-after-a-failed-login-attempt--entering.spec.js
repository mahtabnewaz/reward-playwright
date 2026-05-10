import { test, expect } from '@playwright/test';

test('successful login after failed attempt', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await page.getByTestId('username-input').fill('wrong-username');
  await page.getByTestId('password-input').fill('wrong-password');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-error')).toBeVisible();
  await expect(page.getByTestId('login-success')).not.toBeVisible();
  await page.getByTestId('username-input').fill('correct-username');
  await page.getByTestId('password-input').fill('correct-password');
  await page.getByTestId('login-button').click();
  await expect(page.getByTestId('login-error')).not.toBeVisible();
  await expect(page.getByTestId('login-success')).toBeVisible();
});
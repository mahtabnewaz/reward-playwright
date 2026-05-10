import { test, expect } from '@playwright/test';

test('should show Todo page and hide Login page when clicking Todo nav link', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await expect(page.getByTestId('login-title')).toBeVisible();
  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toBeVisible();
  await expect(page.getByTestId('login-title')).not.toBeVisible();
});
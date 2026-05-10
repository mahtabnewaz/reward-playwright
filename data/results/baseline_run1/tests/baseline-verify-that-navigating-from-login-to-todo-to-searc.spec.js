import { test, expect } from '@playwright/test';

test('should navigate between pages correctly', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await expect(page.getByTestId('login-title')).toBeVisible();

  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toBeVisible();

  await page.getByTestId('nav-search').click();
  await expect(page.getByTestId('search-title')).toBeVisible();

  await page.getByTestId('nav-login').click();
  await expect(page.getByTestId('login-title')).toBeVisible();
});
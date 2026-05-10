import { test, expect } from '@playwright/test';

test('should display title on each page', async ({ page }) => {
  await page.goto('/');

  // Navigate to login page and verify title
  await page.getByTestId('nav-login').click();
  await expect(page.getByTestId('login-title')).toBeVisible();

  // Navigate to todo page and verify title
  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toBeVisible();

  // Navigate to search page and verify title
  await page.getByTestId('nav-search').click();
  await expect(page.getByTestId('search-title')).toBeVisible();
});
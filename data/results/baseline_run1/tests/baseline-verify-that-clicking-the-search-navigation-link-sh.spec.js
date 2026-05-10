import { test, expect } from '@playwright/test';

test('should show Search page and hide other pages when clicking Search navigation link', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();

  await expect(page.getByTestId('search-title')).toBeVisible();
  await expect(page.getByTestId('search-input')).toBeVisible();
  await expect(page.getByTestId('search-results')).toBeVisible();

  await expect(page.getByTestId('login-title')).not.toBeVisible();
  await expect(page.getByTestId('username-input')).not.toBeVisible();
  await expect(page.getByTestId('password-input')).not.toBeVisible();
  await expect(page.getByTestId('login-button')).not.toBeVisible();

  await expect(page.getByTestId('todo-title')).not.toBeVisible();
  await expect(page.getByTestId('todo-input')).not.toBeVisible();
  await expect(page.getByTestId('add-todo-button')).not.toBeVisible();
  await expect(page.getByTestId('todo-list')).not.toBeVisible();
});
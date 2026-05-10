import { test, expect } from '@playwright/test';

test('should persist todo item after navigating away and back', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toBeVisible();
  await page.getByTestId('todo-input').fill('New task');
  await page.getByTestId('add-todo-button').click();
  await expect(page.getByTestId('todo-count')).toContainText('1');
  await expect(page.getByTestId('todo-list')).toContainText('New task');

  await page.getByTestId('nav-search').click();
  await expect(page.getByTestId('search-title')).toBeVisible();

  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toBeVisible();
  await expect(page.getByTestId('todo-count')).toContainText('1');
  await expect(page.getByTestId('todo-list')).toContainText('New task');
});
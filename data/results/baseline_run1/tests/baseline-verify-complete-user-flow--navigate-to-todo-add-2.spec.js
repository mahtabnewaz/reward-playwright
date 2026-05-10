import { test, expect } from '@playwright/test';

test('complete user flow', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toBeVisible();
  await page.getByTestId('todo-input').fill('Task 1');
  await page.getByTestId('add-todo-button').click();
  await page.getByTestId('todo-input').fill('Task 2');
  await page.getByTestId('add-todo-button').click();
  await expect(page.getByTestId('todo-count')).toContainText('2');
  await expect(page.getByTestId('todo-list')).toContainText('Task 1');
  await expect(page.getByTestId('todo-list')).toContainText('Task 2');
  await page.getByTestId('nav-search').click();
  await expect(page.getByTestId('search-title')).toBeVisible();
  await page.getByTestId('search-input').fill('Task 1');
  await page.getByTestId('search-results').waitFor();
  await expect(page.getByTestId('search-count')).toContainText('1');
  await expect(page.getByTestId('search-result-item')).toContainText('Task 1');
  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toBeVisible();
  await expect(page.getByTestId('todo-count')).toContainText('2');
  await expect(page.getByTestId('todo-list')).toContainText('Task 1');
  await expect(page.getByTestId('todo-list')).toContainText('Task 2');
});
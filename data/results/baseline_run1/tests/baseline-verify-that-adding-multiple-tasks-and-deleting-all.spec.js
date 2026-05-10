import { test, expect } from '@playwright/test';

test('should have empty list and 0 tasks count after adding and deleting multiple tasks', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();

  await page.getByTestId('todo-input').fill('Task 1');
  await page.getByTestId('add-todo-button').click();

  await page.getByTestId('todo-input').fill('Task 2');
  await page.getByTestId('add-todo-button').click();

  await page.getByTestId('todo-input').fill('Task 3');
  await page.getByTestId('add-todo-button').click();

  const todoList = page.getByTestId('todo-list');
  const todoCount = page.getByTestId('todo-count');

  await todoList.locator('li').first().getByRole('button').click();
  await todoList.locator('li').first().getByRole('button').click();
  await todoList.locator('li').first().getByRole('button').click();

  await expect(todoList).toBeEmpty();
  await expect(todoCount).toContainText('0');
});
import { test, expect } from '@playwright/test';

test('should not add task with empty input', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await page.getByTestId('add-todo-button').click();
  const todoCountBefore = await page.getByTestId('todo-count').textContent();
  await page.getByTestId('add-todo-button').click();
  const todoCountAfter = await page.getByTestId('todo-count').textContent();
  expect(todoCountBefore).toBe(todoCountAfter);
  const todoListItems = await page.getByTestId('todo-list').$$('li');
  expect(todoListItems.length).toBe(0);
});
import { test, expect } from '@playwright/test';

test('each added todo item has a unique data-testid attribute', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await page.getByTestId('todo-input').fill('Todo item 1');
  await page.getByTestId('add-todo-button').click();
  await page.getByTestId('todo-input').fill('Todo item 2');
  await page.getByTestId('add-todo-button').click();
  const todoItems = await page.getByTestId('todo-list').$$('li');
  const dataTestIds = await Promise.all(todoItems.map(async (item) => await item.getAttribute('data-testid')));
  expect(dataTestIds).toEqual(expect.arrayContaining(dataTestIds));
  expect(new Set(dataTestIds).size).toBe(dataTestIds.length);
});
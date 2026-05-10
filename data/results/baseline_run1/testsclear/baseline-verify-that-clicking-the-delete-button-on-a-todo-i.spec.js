import { test, expect } from '@playwright/test';

test('should remove todo item from list when delete button is clicked', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await page.getByTestId('todo-title').waitFor();
  await page.getByTestId('todo-input').fill('New Todo Item');
  await page.getByTestId('add-todo-button').click();
  await page.getByTestId('todo-list').waitFor();
  const initialTodoCount = await page.getByTestId('todo-count').textContent();
  const todoItem = (await page.getByTestId('todo-list').locator('li')).first();
  await todoItem.locator('button', { hasText: 'Delete' }).click();
  const updatedTodoCount = await page.getByTestId('todo-count').textContent();
  expect(parseInt(updatedTodoCount)).toBe(parseInt(initialTodoCount) - 1);
  expect(await page.getByTestId('todo-list').locator('li').count()).toBe(parseInt(initialTodoCount) - 1);
});
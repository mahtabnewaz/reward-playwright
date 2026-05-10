import { test, expect } from '@playwright/test';

test('unchecking a previously checked todo removes strikethrough decoration', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await page.getByTestId('todo-input').fill('New Todo');
  await page.getByTestId('add-todo-button').click();
  const todoItem = (await page.getByTestId('todo-list').locator('li')).first();
  await todoItem.click();
  await expect(todoItem).toHaveClass(/checked/);
  await expect(todoItem).toHaveCSS('textDecoration', 'line-through');
  await todoItem.click();
  await expect(todoItem).not.toHaveClass(/checked/);
  await expect(todoItem).not.toHaveCSS('textDecoration', 'line-through');
});
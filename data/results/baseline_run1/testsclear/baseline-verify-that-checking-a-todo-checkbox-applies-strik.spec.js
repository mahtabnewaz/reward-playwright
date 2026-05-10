import { test, expect } from '@playwright/test';

test('should apply strikethrough text decoration to task text when checkbox is checked', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await page.getByTestId('todo-input').fill('New task');
  await page.getByTestId('add-todo-button').click();
  const todoItem = page.getByTestId('todo-list').getByText('New task');
  await todoItem.locator('input[type="checkbox"]').check();
  await expect(todoItem).toHaveCSS('text-decoration', 'line-through');
});
import { test, expect } from '@playwright/test';

test('should display Todo List title', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toContainText('Todo List');
});
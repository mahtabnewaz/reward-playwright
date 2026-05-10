import { test, expect } from '@playwright/test';

test('should have placeholder text in todo input field', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  const todoInput = page.getByTestId('todo-input');
  await expect(todoInput).toHaveAttribute('placeholder', 'Add a new task...');
});
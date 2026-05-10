import { test, expect } from '@playwright/test';

test('should have Add Task button with correct text', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  const addTodoButton = page.getByTestId('add-todo-button');
  await expect(addTodoButton).toBeVisible();
  const buttonText = await addTodoButton.textContent();
  await expect(buttonText).toBe('Add Task');
});
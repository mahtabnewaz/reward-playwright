import { test, expect } from '@playwright/test';

test('should clear todo input field after adding a task', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await page.waitForSelector('[data-testid="todo-input"]');
  const todoInput = page.getByTestId('todo-input');
  await todoInput.fill('New task');
  await page.getByTestId('add-todo-button').click();
  await page.waitForTimeout(100);
  expect(await todoInput.inputValue()).toBe('');
});
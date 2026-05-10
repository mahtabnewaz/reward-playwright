import { test, expect } from '@playwright/test';

test('task count badge updates correctly when a task is added', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  const initialCount = await page.getByTestId('todo-count').textContent();
  expect(initialCount).not.toBeNull();
  const initialCountNumber = parseInt(initialCount);
  await page.getByTestId('todo-input').fill('New task');
  await page.getByTestId('add-todo-button').click();
  const updatedCount = await page.getByTestId('todo-count').textContent();
  expect(updatedCount).not.toBeNull();
  const updatedCountNumber = parseInt(updatedCount);
  expect(updatedCountNumber).toBe(initialCountNumber + 1);
});
import { test, expect } from '@playwright/test';

test('verify task count updates after adding and deleting tasks', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await page.getByTestId('todo-input').fill('Task 1');
  await page.getByTestId('add-todo-button').click();
  await page.getByTestId('todo-input').fill('Task 2');
  await page.getByTestId('add-todo-button').click();
  await page.getByTestId('todo-input').fill('Task 3');
  await page.getByTestId('add-todo-button').click();
  await expect(page.getByTestId('todo-count')).toHaveText('3 tasks');
  await page.getByTestId('todo-delete-1').click();
  await expect(page.getByTestId('todo-count')).toHaveText('2 tasks');
});
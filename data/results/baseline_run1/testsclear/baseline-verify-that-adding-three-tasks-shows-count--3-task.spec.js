import { test, expect } from '@playwright/test';

test('should update task count when adding and deleting tasks', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toBeVisible();

  await page.getByTestId('todo-input').fill('Task 1');
  await page.getByTestId('add-todo-button').click();
  await page.getByTestId('todo-input').fill('Task 2');
  await page.getByTestId('add-todo-button').click();
  await page.getByTestId('todo-input').fill('Task 3');
  await page.getByTestId('add-todo-button').click();

  await expect(page.getByTestId('todo-count')).toContainText('3 tasks');

  const todoList = page.getByTestId('todo-list');
  const firstTodo = (await todoList.$$('*'))[0];
  await firstTodo.click();

  await expect(page.getByTestId('todo-count')).toContainText('2 tasks');
});
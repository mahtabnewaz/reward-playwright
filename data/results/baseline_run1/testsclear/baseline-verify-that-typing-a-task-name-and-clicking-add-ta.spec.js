import { test, expect } from '@playwright/test';

test('should add task to todo list', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('todo-title')).toBeVisible();
  const todoInput = page.getByTestId('todo-input');
  const addTodoButton = page.getByTestId('add-todo-button');
  const todoList = page.getByTestId('todo-list');
  await todoInput.fill('New task');
  await addTodoButton.click();
  await expect(todoList).toContainText('New task');
  const todoCount = await page.getByTestId('todo-count').textContent();
  expect(todoCount).toBe('1');
});
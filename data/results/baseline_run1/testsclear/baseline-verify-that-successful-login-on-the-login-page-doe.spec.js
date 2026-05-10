import { test, expect } from '@playwright/test';

test('successful login does not affect todo list', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await page.getByTestId('username-input').fill('username');
  await page.getByTestId('password-input').fill('password');
  await page.getByTestId('login-button').click();
  await page.waitForSelector(() => page.getByTestId('login-success'), { state: 'visible' });
  await page.getByTestId('nav-todo').click();
  const todoList = await page.getByTestId('todo-list');
  const todoCount = await page.getByTestId('todo-count');
  expect(await todoList.count()).toBe(0);
  expect(await todoCount.textContent()).toBe('0');
});
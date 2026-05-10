import { test, expect } from '@playwright/test';

test('should display navigation bar with three links', async ({ page }) => {
  await page.goto('/');
  const navLogin = page.getByTestId('nav-login');
  const navTodo = page.getByTestId('nav-todo');
  const navSearch = page.getByTestId('nav-search');

  await expect(navLogin).toBeVisible();
  await expect(navTodo).toBeVisible();
  await expect(navSearch).toBeVisible();

  const navLoginText = await navLogin.textContent();
  const navTodoText = await navTodo.textContent();
  const navSearchText = await navSearch.textContent();

  await expect(navLoginText).toBe('Login');
  await expect(navTodoText).toBe('Todo');
  await expect(navSearchText).toBe('Search');
});
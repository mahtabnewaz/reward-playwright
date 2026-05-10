import { test, expect } from '@playwright/test';

test('should have active CSS class on active navigation link', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  await expect(page.getByTestId('nav-login')).toHaveClass('active');
  await expect(page.getByTestId('nav-todo')).not.toHaveClass('active');
  await expect(page.getByTestId('nav-search')).not.toHaveClass('active');

  await page.getByTestId('nav-todo').click();
  await expect(page.getByTestId('nav-login')).not.toHaveClass('active');
  await expect(page.getByTestId('nav-todo')).toHaveClass('active');
  await expect(page.getByTestId('nav-search')).not.toHaveClass('active');

  await page.getByTestId('nav-search').click();
  await expect(page.getByTestId('nav-login')).not.toHaveClass('active');
  await expect(page.getByTestId('nav-todo')).not.toHaveClass('active');
  await expect(page.getByTestId('nav-search')).toHaveClass('active');
});
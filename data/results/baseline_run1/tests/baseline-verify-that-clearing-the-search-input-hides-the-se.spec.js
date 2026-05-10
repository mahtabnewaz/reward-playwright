import { test, expect } from '@playwright/test';

test('should hide search results dropdown when clearing search input', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  await page.getByTestId('search-input').fill('test');
  await expect(page.getByTestId('search-results')).toBeVisible();
  await page.getByTestId('search-input').fill('');
  await expect(page.getByTestId('search-results')).not.toBeVisible();
});
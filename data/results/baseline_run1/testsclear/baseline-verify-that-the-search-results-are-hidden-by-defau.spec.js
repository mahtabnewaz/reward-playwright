import { test, expect } from '@playwright/test';

test('search results are hidden by default', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  const searchResults = page.getByTestId('search-results');
  await expect(searchResults).not.toBeVisible();
});
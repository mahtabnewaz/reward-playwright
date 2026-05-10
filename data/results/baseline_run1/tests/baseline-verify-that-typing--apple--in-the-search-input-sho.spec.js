import { test, expect } from '@playwright/test';

test('should show search results when typing in search input', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  await page.getByTestId('search-input').fill('apple');
  await page.waitForTimeout(1000); // wait for search results to load
  const searchResult = page.getByTestId('search-result-item');
  await expect(searchResult).toContainText('Apple');
});
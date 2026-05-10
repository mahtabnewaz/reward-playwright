import { test, expect } from '@playwright/test';

test('should display correct search results count', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  await page.getByTestId('search-input').fill('test');
  await page.getByTestId('search-input').press('Enter');
  const searchCount = await page.getByTestId('search-count').textContent();
  const searchResults = await page.getAllByTestId('search-result-item');
  expect(searchCount).toContain(searchResults.length.toString());
});
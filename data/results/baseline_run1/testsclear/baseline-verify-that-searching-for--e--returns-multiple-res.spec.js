import { test, expect } from '@playwright/test';

test('searching for e returns multiple results and correct count', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  await page.getByTestId('search-input').fill('e');
  await page.getByTestId('search-input').press('Enter');
  const searchCount = await page.getByTestId('search-count').textContent();
  const searchResults = await page.getAllByTestId('search-result-item');
  expect(searchResults.length).toBeGreaterThan(1);
  expect(parseInt(searchCount)).toBe(searchResults.length);
});
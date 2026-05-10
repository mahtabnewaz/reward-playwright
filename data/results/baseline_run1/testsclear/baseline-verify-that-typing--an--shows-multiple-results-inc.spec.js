import { test, expect } from '@playwright/test';

test('should show multiple search results for query "an"', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  await page.getByTestId('search-input').fill('an');
  await page.waitForTimeout(1000); // wait for search results to load
  const searchResults = page.getByTestId('search-result-item');
  const resultTexts = await searchResults.allTextContents();
  expect(resultTexts).toContain('Banana');
  expect(resultTexts).toContain('Mango');
  expect(resultTexts.length).toBeGreaterThan(1);
});
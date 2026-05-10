import { test, expect } from '@playwright/test';

test('should fill search input with selected value when search result item is clicked', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  await page.getByTestId('search-input').fill('test');
  await page.waitForTimeout(1000); // wait for search results to load
  const searchResultItem = page.getByTestId('search-result-item');
  await expect(searchResultItem).toBeVisible();
  const inputValueBeforeClick = await page.getByTestId('search-input').inputValue();
  await searchResultItem.click();
  const inputValueAfterClick = await page.getByTestId('search-input').inputValue();
  expect(inputValueAfterClick).not.toEqual(inputValueBeforeClick);
});
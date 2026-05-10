import { test, expect } from '@playwright/test';

test('search results dropdown disappears after selecting a result', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  await page.getByTestId('search-input').fill('test');
  await page.getByTestId('search-input').press('Enter');
  await expect(page.getByTestId('search-results')).toBeVisible();
  await page.getByTestId('search-result-item').first().click();
  await expect(page.getByTestId('search-results')).not.toBeVisible();
});
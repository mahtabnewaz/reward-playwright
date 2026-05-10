import { test, expect } from '@playwright/test';

test('should show no results dropdown and display 0 results found when searching with no matches', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  await page.getByTestId('search-input').fill('non-existent-query');
  await page.getByTestId('search-input').press('Enter');
  await expect(page.getByTestId('search-results')).not.toBeVisible();
  await expect(page.getByTestId('search-count')).toContainText('0 results found');
});
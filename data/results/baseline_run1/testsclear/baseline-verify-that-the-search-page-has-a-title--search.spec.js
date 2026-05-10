import { test, expect } from '@playwright/test';

test('should display Search title on Search page', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  await expect(page.getByTestId('search-title')).toContainText('Search');
});
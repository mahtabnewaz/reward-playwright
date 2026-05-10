import { test, expect } from '@playwright/test';

test('should have search input field with placeholder text', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-search').click();
  const searchInput = page.getByTestId('search-input');
  await expect(searchInput).toHaveAttribute('placeholder', 'Search...');
});
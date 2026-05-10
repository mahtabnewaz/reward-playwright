import { test, expect } from '@playwright/test';

test('login button changes appearance on hover', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('nav-login').click();
  const loginButton = page.getByTestId('login-button');
  const initialStyles = await loginButton.evaluate((element) => {
    return {
      backgroundColor: element.style.backgroundColor,
      color: element.style.color,
    };
  });
  await loginButton.hover();
  const hoverStyles = await loginButton.evaluate((element) => {
    return {
      backgroundColor: element.style.backgroundColor,
      color: element.style.color,
    };
  });
  expect(initialStyles).not.toEqual(hoverStyles);
});
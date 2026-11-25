import re

import allure
from playwright.sync_api import Page, expect


@allure.feature("Playwright website")
class TestPlaywrightSite:

    @allure.title("Home page has the correct title")
    def test_home_page_title(self, page: Page):
        with allure.step("Open playwright.dev"):
            page.goto("https://playwright.dev/")
        with allure.step("Check page title"):
            expect(page).to_have_title(re.compile("Playwright"))

    @allure.title("'Get started' link opens the Installation page")
    def test_get_started_link(self, page: Page):
        with allure.step("Open playwright.dev"):
            page.goto("https://playwright.dev/")
        with allure.step("Click 'Get started'"):
            page.get_by_role("link", name="Get started").click()
        with allure.step("Check Installation heading is visible"):
            expect(page.get_by_role("heading", name="Installation")).to_be_visible()

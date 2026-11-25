import allure
from playwright.sync_api import Page, expect

URL = "https://www.saucedemo.com/"


@allure.feature("Login")
class TestLogin:

    @allure.title("User can log in with valid credentials")
    def test_valid_login(self, page: Page):
        with allure.step("Open login page"):
            page.goto(URL)
        with allure.step("Fill in valid credentials and submit"):
            page.locator("#user-name").fill("standard_user")
            page.locator("#password").fill("secret_sauce")
            page.locator("#login-button").click()
        with allure.step("Check products page is shown"):
            expect(page).to_have_url(URL + "inventory.html")
            expect(page.locator(".title")).to_have_text("Products")

    @allure.title("Error is shown for wrong password")
    def test_invalid_login(self, page: Page):
        with allure.step("Open login page"):
            page.goto(URL)
        with allure.step("Fill in a wrong password and submit"):
            page.locator("#user-name").fill("standard_user")
            page.locator("#password").fill("wrong_password")
            page.locator("#login-button").click()
        with allure.step("Check error message"):
            expect(page.locator("[data-test='error']")).to_contain_text(
                "Username and password do not match"
            )

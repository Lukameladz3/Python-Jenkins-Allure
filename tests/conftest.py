import allure
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure report when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )

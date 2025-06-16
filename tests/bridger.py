
from playwright.sync_api import Page


def test_example(page: Page ) -> None:
    page.goto("Application URL")
    page.get_by_text("Search", exact=True).click()
    page.get_by_role("link", name="test", exact=True).click()

    page.get_by_label("First Name").dblclick()
    page.get_by_label("First Name").click()
    page.get_by_label("First Name").fill("charles")

    page.get_by_label("Last Name").click()
    page.get_by_label("Last Name").fill("taylor")

    page.locator("#toolbarSubmit").click()
    page.get_by_text("False Positive Name").click()
    page.get_by_role("button", name="Apply").click()
    page.get_by_text("False Positive Name was").click()

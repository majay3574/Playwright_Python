import allure
import pytest
from playwright.sync_api import Page
from utils.data_helper import DataHelper
import csv


class DataHelper:
    @staticmethod
    def read_form_data_from_csv(file_path):
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]


@pytest.mark.parametrize("data", DataHelper.read_form_data_from_csv("data/sample_form_data.csv"))
@allure.title("Form automation with data: {data[first_name]} {data[last_name]}")
def test_example(page: Page, data) -> None:
    with allure.step("Navigate to Application"):
        page.goto("https://your-app-url.com")  # Replace with actual URL

    with allure.step("Click on Search"):
        page.get_by_text("Search", exact=True).click()

    with allure.step("Click on test link"):
        page.get_by_role("link", name="test", exact=True).click()

    with allure.step(f"Fill First Name: {data['first_name']}"):
        page.get_by_label("First Name").dblclick()
        page.get_by_label("First Name").click()
        page.get_by_label("First Name").fill(data["first_name"])

    with allure.step(f"Fill Last Name: {data['last_name']}"):
        page.get_by_label("Last Name").click()
        page.get_by_label("Last Name").fill(data["last_name"])

    with allure.step("Click Submit"):
        page.locator("#toolbarSubmit").click()

    with allure.step("Click False Positive Name"):
        page.get_by_text("False Positive Name").click()

    with allure.step("Click Apply"):
        page.get_by_role("button", name="Apply").click()

    with allure.step("Click False Positive confirmation"):
        page.get_by_text("False Positive Name was").click()

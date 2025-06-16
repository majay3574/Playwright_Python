# tests/test_form.py

import allure
import pytest
import csv
from playwright.sync_api import Page


class DataHelper:
    @staticmethod
    def read_form_data_from_csv(file_path):
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]


@pytest.mark.parametrize("data", DataHelper.read_form_data_from_csv("data/sample_form_data.csv"))
@allure.title("Form submission test for {data[first_name]} {data[last_name]}")
def test_example(page: Page, data) -> None:
    with allure.step("Navigate to Practice Form"):
        page.goto("https://demoqa.com/automation-practice-form")

    with allure.step(f"Fill First Name: {data['first_name']}"):
        page.get_by_role("textbox", name="First Name").fill(data["first_name"])

    with allure.step(f"Fill Last Name: {data['last_name']}"):
        page.get_by_role("textbox", name="Last Name").fill(data["last_name"])

    with allure.step(f"Fill Email: {data['email']}"):
        page.get_by_role("textbox", name="name@example.com").click()
        page.get_by_role("textbox", name="name@example.com").fill(data["email"])

    with allure.step(f"Select Gender: {data['gender']}"):
        page.get_by_text(data["gender"], exact=True).click()

    with allure.step(f"Fill Mobile Number: {data['mobile']}"):
        page.get_by_role("textbox", name="Mobile Number").fill(data["mobile"])

    with allure.step(f"Fill Subject: {data['subject']}"):
        page.locator("#subjectsInput").fill(data["subject"])

    with allure.step(f"Fill Address: {data['address']}"):
        page.get_by_role("textbox", name="Current Address").fill(data["address"])

    with allure.step("Click Submit Button"):
        page.get_by_role("button", name="Submit").click()

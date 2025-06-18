from playwright.sync_api import Page
import pytest
import csv
from utils.data_helper import DataHelper
from utils.logger import setup_logger

logger = setup_logger()

class DataHelper:
    @staticmethod
    def read_form_data_from_csv(file_path):
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]


@pytest.mark.parametrize("data", DataHelper.read_form_data_from_csv("data/sample_form_data.csv"))
def test_example(page: Page, data) -> None:
    try:
        logger.info("Navigating to the application URL")
        page.goto("https://your-app-url.com")

        logger.info("Clicking on 'Search'")
        page.get_by_text("Search", exact=True).click()

        logger.info("Clicking on 'test' link")
        page.get_by_role("link", name="test", exact=True).click()

        logger.info(f"Filling First Name: {data['first_name']}")
        page.get_by_label("First Name").dblclick()
        page.get_by_label("First Name").click()
        page.get_by_label("First Name").fill(data["first_name"])

        logger.info(f"Filling Last Name: {data['last_name']}")
        page.get_by_label("Last Name").click()
        page.get_by_label("Last Name").fill(data["last_name"])

        logger.info("Clicking on Submit")
        page.locator("#toolbarSubmit").click()

        logger.info("Clicking on 'False Positive Name'")
        page.get_by_text("False Positive Name").click()

        logger.info("Clicking on Apply")
        page.get_by_role("button", name="Apply").click()

        logger.info("Confirming 'False Positive Name was'")
        page.get_by_text("False Positive Name was").click()

    except Exception as e:
        logger.error(f"Test failed due to: {e}")
        pytest.fail(f"Test failed due to: {e}")

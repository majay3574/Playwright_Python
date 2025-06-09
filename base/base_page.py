import logging
import allure
import configparser
from playwright.sync_api import Page, expect

class BasePage:
    """Base class for all page objects with common methods"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)
        self.timeout = self._read_timeout()
        self.page.set_default_timeout(self.timeout)

    def _read_timeout(self) -> int:
        config = configparser.ConfigParser()
        config.read("config.properties")
        return int(config.get("default", "action.timeout", fallback="30000"))

    def navigate(self, url: str):
        with allure.step(f"Navigate to URL: {url}"):
            self.logger.info(f"Navigating to: {url}")
            self.page.goto(url)

    def click(self, selector: str):
        with allure.step(f"Click on element: {selector}"):
            self.logger.info(f"Clicking element: {selector}")
            try:
                self.page.click(selector)
            except Exception as e:
                self.logger.error(f"Failed to click element {selector}: {str(e)}")
                raise

    def fill_text(self, selector: str, text: str):
        with allure.step(f"Fill text '{text}' into: {selector}"):
            self.logger.info(f"Filling text in element {selector}: {text}")
            try:
                self.page.fill(selector, text)
            except Exception as e:
                self.logger.error(f"Failed to fill text in element {selector}: {str(e)}")
                raise

    def get_text(self, selector: str) -> str:
        with allure.step(f"Get text from element: {selector}"):
            try:
                text = self.page.text_content(selector)
                self.logger.info(f"Got text from element {selector}: {text}")
                return text
            except Exception as e:
                self.logger.error(f"Failed to get text from element {selector}: {str(e)}")
                raise

    def select_option(self, selector: str, option: str):
        with allure.step(f"Select option '{option}' from dropdown: {selector}"):
            self.logger.info(f"Selecting option {option} from dropdown {selector}")
            try:
                self.page.select_option(selector, option)
            except Exception as e:
                self.logger.error(f"Failed to select option {option} from dropdown {selector}: {str(e)}")
                raise

    def is_visible(self, selector: str) -> bool:
        with allure.step(f"Check visibility of element: {selector}"):
            try:
                self.wait_for_element(selector)
                is_visible = self.page.is_visible(selector)
                self.logger.info(f"Element {selector} visibility: {is_visible}")
                return is_visible
            except Exception as e:
                self.logger.error(f"Failed to check visibility of element {selector}: {str(e)}")
                return False

    def wait_for_element(self, selector: str, timeout: int = None):
        final_timeout = timeout if timeout is not None else self.timeout
        with allure.step(f"Wait for element {selector} (timeout={final_timeout}ms)"):
            self.logger.info(f"Waiting for element: {selector}")
            try:
                self.page.wait_for_selector(selector, timeout=final_timeout)
            except Exception as e:
                self.logger.error(f"Element {selector} did not appear within {final_timeout}ms: {str(e)}")
                raise

    def assert_element_visible(self, selector: str):
        with allure.step(f"Assert element is visible: {selector}"):
            self.logger.info(f"Asserting element is visible: {selector}")
            expect(self.page.locator(selector)).to_be_visible()

    def assert_text(self, selector: str, expected_text: str):
        with allure.step(f"Assert element {selector} contains text: '{expected_text}'"):
            self.logger.info(f"Asserting element {selector} contains text: {expected_text}")
            expect(self.page.locator(selector)).to_contain_text(expected_text)

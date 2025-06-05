"""
Base Page module containing common functionality for all page objects
"""
import logging
from playwright.sync_api import Page, expect

class BasePage:
    """Base class for all page objects with common methods"""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)
        
    def navigate(self, url: str):
        """Navigate to the specified URL"""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
        
    def click(self, selector: str):
        """Click on the element with the given selector"""
        self.logger.info(f"Clicking element: {selector}")
        try:
            self.page.click(selector)
        except Exception as e:
            self.logger.error(f"Failed to click element {selector}: {str(e)}")
            raise
            
    def fill_text(self, selector: str, text: str):
        """Fill text in the element with the given selector"""
        self.logger.info(f"Filling text in element {selector}: {text}")
        try:
            self.page.fill(selector, text)
        except Exception as e:
            self.logger.error(f"Failed to fill text in element {selector}: {str(e)}")
            raise
            
    def get_text(self, selector: str) -> str:
        """Get text from the element with the given selector"""
        try:
            text = self.page.text_content(selector)
            self.logger.info(f"Got text from element {selector}: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from element {selector}: {str(e)}")
            raise
            
    def select_option(self, selector: str, option: str):
        """Select an option from a dropdown"""
        self.logger.info(f"Selecting option {option} from dropdown {selector}")
        try:
            self.page.select_option(selector, option)
        except Exception as e:
            self.logger.error(f"Failed to select option {option} from dropdown {selector}: {str(e)}")
            raise
            
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        try:
            is_visible = self.page.is_visible(selector)
            self.logger.info(f"Element {selector} visibility: {is_visible}")
            return is_visible
        except Exception as e:
            self.logger.error(f"Failed to check visibility of element {selector}: {str(e)}")
            return False
            
    def wait_for_element(self, selector: str, timeout: int = 30000):
        """Wait for element to be visible"""
        self.logger.info(f"Waiting for element: {selector}")
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
        except Exception as e:
            self.logger.error(f"Element {selector} did not appear within {timeout}ms: {str(e)}")
            raise
            
    def assert_element_visible(self, selector: str):
        """Assert that element is visible"""
        self.logger.info(f"Asserting element is visible: {selector}")
        expect(self.page.locator(selector)).to_be_visible()
    
    def assert_text(self, selector: str, expected_text: str):
        """Assert that element contains expected text"""
        self.logger.info(f"Asserting element {selector} contains text: {expected_text}")
        expect(self.page.locator(selector)).to_contain_text(expected_text)
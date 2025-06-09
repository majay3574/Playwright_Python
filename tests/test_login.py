"""
Test module for login functionality
"""
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage

class TestLogin:
    """Test class for login functionality"""
    
    def test_valid_login(self, page, test_data):
        """Test login with valid credentials"""
        # Create page objects
        login_page = LoginPage(page)
        
        # Navigate to login page
        login_page.navigate_to_login()
        
        # Perform login
        login_page.perform_login(
            test_data["valid_user"]["username"],
            test_data["valid_user"]["password"]
        )
        
    
    def test_invalid_login(self, page, test_data):
        """Test login with invalid credentials"""
        # Create login page object
        login_page = LoginPage(page)
        
        # Navigate to login page
        login_page.navigate_to_login()
        
        # Perform login with invalid credentials
        login_page.perform_login(
            test_data["invalid_user"]["username"],
            test_data["invalid_user"]["password"]
        )
        
        # Verify error message is displayed
        assert login_page.is_error_displayed(), "Error message not displayed for invalid login"
        
        # Verify error message contains expected text
        error_message = login_page.get_error_message().lower()
        assert "user not found" in error_message, f"'User not found' not in error message: {error_message}"
        

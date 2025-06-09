from base.base_page import BasePage
"""
Login Page module with login page elements and actions
"""

class LoginPage(BasePage):
    """Login page class with methods and selectors for the login page"""
    
    # Page URL
    URL = "http://leaftaps.com/opentaps/control/login"
    
    # Selectors
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = ".decorativeSubmit"
    ERROR_MESSAGE = "//p[contains(text(),'User not found')]"
      
    def __init__(self, page):
        super().__init__(page)
    
    def navigate_to_login(self):
        """Navigate to the login page"""
        self.navigate(self.URL)
        self.assert_element_visible(self.USERNAME_INPUT)
    
    def enter_username(self, username):
        """Enter username in the username field"""
        self.fill_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password):
        """Enter password in the password field"""
        self.fill_text(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        """Click the login button"""
        self.click(self.LOGIN_BUTTON)

    
    def perform_login(self, username, password):
        """Perform full login process"""
        self.logger.info(f"Performing login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    
    def is_error_displayed(self):
        """Check if login error is displayed"""
        return self.is_visible(self.ERROR_MESSAGE)
    
    def get_error_message(self):
        """Get the error message text"""
        return self.get_text(self.ERROR_MESSAGE)
from base.base_page import BasePage

"""
Home Page module with home page elements and actions
"""


class HomePage(BasePage):
    """Home page class with methods and selectors for the home page"""
    
    # Selectors
    LOGOUT_BUTTON = "a.decorativeSubmit"
    CRMSFA="//a[contains(text(),'CRM/SFA')]"  
    
    def __init__(self, page):
        super().__init__(page)
    
    def click_crm_sfa_link(self):
        """Click on the CRM/SFA link"""
        self.click(self.CRMSFA)
    
    def logout(self):
        """Log out from the application"""
        self.click(self.LOGOUT_BUTTON)
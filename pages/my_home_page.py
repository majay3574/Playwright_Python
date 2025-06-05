from base.base_page import BasePage
"""
My Home Page module with elements and actions
"""

class MyHomePage(BasePage):
    """My Home page class with methods and selectors"""
    
    # Selectors
    LEADS_LINK = "//a[text()='Leads']"
    ACCOUNTS_LINK = "//a[text()='Accounts']"
    CONTACTS_LINK = "//a[text()='Contacts']"
    OPPORTUNITIES_LINK = "//a[text()='Opportunities']"
    
    def __init__(self, page):
        super().__init__(page)
    
    def click_leads_tab(self):
        """Click on the Leads tab"""
        self.click(self.LEADS_LINK)
    
    def click_accounts_tab(self):
        """Click on the Accounts tab"""
        self.click(self.ACCOUNTS_LINK)
    
    def click_contacts_tab(self):
        """Click on the Contacts tab"""
        self.click(self.CONTACTS_LINK)
    
    def click_opportunities_tab(self):
        """Click on the Opportunities tab"""
        self.click(self.OPPORTUNITIES_LINK)
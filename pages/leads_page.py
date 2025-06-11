from base.base_page import BasePage
"""
Leads Page module with elements and actions
"""
from asyncio import timeout


class LeadsPage(BasePage):
    """Leads page class with methods and selectors"""
    
    # Selectors
    CREATE_LEAD_LINK = "//a[text()='Create Lead']"
    FIND_LEADS_LINK = "//a[text()='Find Leads']"
    MERGE_LEADS_LINK = "//a[text()='Merge Leads']"
    FIND_LEAD_BUTTON = "//button[text()='Find Leads']"
    FIRST_NAME_INPUT = "//input[@name='firstName']"
    
    # Lead list table selectors
    LEADS_TABLE = "div.x-grid3-body"
    LEAD_ROWS = "//div[@class='x-grid3-body']//tr"
    
    def __init__(self, page):
        super().__init__(page)
    
    def click_create_lead(self):
        """Click on the Create Lead link"""
        self.click(self.CREATE_LEAD_LINK)
    
    def click_find_leads(self):
        """Click on the Find Leads link"""
        self.click(self.FIND_LEADS_LINK)
            
    def click_merge_leads(self):
        """Click on the Merge Leads link"""
        self.click(self.MERGE_LEADS_LINK)
    
    def verify_leads_page_loaded(self):
        """Verify the leads page is loaded"""
        return self.is_visible(self.CREATE_LEAD_LINK) 
    
    def search_created_lead(self, lead_name):
        """Search for a created lead by name"""
        self.fill(self.FIRST_NAME_INPUT, lead_name)
        self.click(self.FIND_LEAD_BUTTON)
    

from base.base_page import BasePage
"""
View Lead Page module with elements and actions
"""


class ViewLeadPage(BasePage):
    """View Lead page class with methods and selectors"""
    
    # Selectors
    LEAD_ID = "#viewLead_generalProfId_sp"
    FIRST_NAME = "#viewLead_firstName_sp"
    LAST_NAME = "#viewLead_lastName_sp"
    COMPANY_NAME = "#viewLead_companyName_sp"
    
    # Action buttons
    EDIT_BUTTON = "a.subMenuButton:has-text('Edit')"
    DELETE_BUTTON = "a.subMenuButton:has-text('Delete')"
    DUPLICATE_BUTTON = "a.subMenuButton:has-text('Duplicate Lead')"
    
    def __init__(self, page):
        super().__init__(page)
    
    def get_lead_id(self):
        """Get the lead ID"""
        return self.get_text(self.LEAD_ID)
    
    def get_lead_name(self):
        """Get the lead's full name"""
        first_name = self.get_text(self.FIRST_NAME)
        last_name = self.get_text(self.LAST_NAME)
        return f"{first_name} {last_name}"
    
    def get_company_name(self):
        """Get the company name"""
        return self.get_text(self.COMPANY_NAME)
    
    def click_edit(self):
        """Click the Edit button"""
        self.click(self.EDIT_BUTTON)
    
    def click_delete(self):
        """Click the Delete button"""
        self.click(self.DELETE_BUTTON)
    
    def click_duplicate(self):
        """Click the Duplicate Lead button"""
        self.click(self.DUPLICATE_BUTTON)
    
   
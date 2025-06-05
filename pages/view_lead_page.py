"""
View Lead Page module with elements and actions
"""
from .base_page import BasePage

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
    
    def verify_lead_details(self, lead_data):
        """
        Verify the lead details match the expected data
        
        Args:
            lead_data: Dictionary containing expected lead information
        
        Returns:
            bool: True if all details match, False otherwise
        """
        self.logger.info(f"Verifying lead details for: {lead_data.get('firstName')} {lead_data.get('lastName')}")
        
        first_name = self.get_text(self.FIRST_NAME)
        last_name = self.get_text(self.LAST_NAME)
        company_name = self.get_text(self.COMPANY_NAME)
        
        all_match = True
        
        if first_name != lead_data.get("firstName"):
            self.logger.error(f"First name mismatch. Expected: {lead_data.get('firstName')}, Actual: {first_name}")
            all_match = False
        
        if last_name != lead_data.get("lastName"):
            self.logger.error(f"Last name mismatch. Expected: {lead_data.get('lastName')}, Actual: {last_name}")
            all_match = False
        
        if company_name != lead_data.get("companyName"):
            self.logger.error(f"Company name mismatch. Expected: {lead_data.get('companyName')}, Actual: {company_name}")
            all_match = False
        
        return all_match
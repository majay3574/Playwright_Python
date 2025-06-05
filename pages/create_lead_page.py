"""
Create Lead Page module with elements and actions
"""

from base.base_page import BasePage
class CreateLeadPage(BasePage):
    """Create Lead page class with methods and selectors"""
    
    # Selectors
    COMPANY_NAME_INPUT = "#createLeadForm_companyName"
    FIRST_NAME_INPUT = "#createLeadForm_firstName"
    LAST_NAME_INPUT = "#createLeadForm_lastName"
    SOURCE_DROPDOWN = "#createLeadForm_dataSourceId"
    MARKETING_CAMPAIGN_DROPDOWN = "#createLeadForm_marketingCampaignId"
    INDUSTRY_DROPDOWN = "#createLeadForm_industryEnumId"
    PHONE_INPUT = "#createLeadForm_primaryPhoneNumber"
    EMAIL_INPUT = "#createLeadForm_primaryEmail"
    CREATE_LEAD_BUTTON = "input[name='submitButton']"
    
    def __init__(self, page):
        super().__init__(page)
    
    def enter_company_name(self, company_name):
        """Enter company name"""
        self.fill_text(self.COMPANY_NAME_INPUT, company_name)
    
    def enter_first_name(self, first_name):
        """Enter first name"""
        self.fill_text(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name):
        """Enter last name"""
        self.fill_text(self.LAST_NAME_INPUT, last_name)
    
    def select_source(self, source):
        """Select lead source from dropdown"""
        self.select_option(self.SOURCE_DROPDOWN, source)
    
    def select_marketing_campaign(self, campaign):
        """Select marketing campaign from dropdown"""
        self.select_option(self.MARKETING_CAMPAIGN_DROPDOWN, campaign)
    
    def select_industry(self, industry):
        """Select industry from dropdown"""
        self.select_option(self.INDUSTRY_DROPDOWN, industry)
    
    def enter_phone(self, phone):
        """Enter phone number"""
        self.fill_text(self.PHONE_INPUT, phone)
    
    def enter_email(self, email):
        """Enter email address"""
        self.fill_text(self.EMAIL_INPUT, email)
    
    def click_create_lead(self):
        """Click create lead button"""
        self.click(self.CREATE_LEAD_BUTTON)
    
    def create_new_lead(self, lead_data):
        """
        Create a new lead with the provided lead data
        
        Args:
            lead_data: Dictionary containing lead information
        """
        self.logger.info(f"Creating new lead: {lead_data.get('firstName')} {lead_data.get('lastName')}")
        
        self.enter_company_name(lead_data.get("companyName"))
        self.enter_first_name(lead_data.get("firstName"))
        self.enter_last_name(lead_data.get("lastName"))
        
        if lead_data.get("source"):
            self.select_source(lead_data.get("source"))
        
        if lead_data.get("marketingCampaign"):
            self.select_marketing_campaign(lead_data.get("marketingCampaign"))
        
        if lead_data.get("industry"):
            self.select_industry(lead_data.get("industry"))
        
        if lead_data.get("phone"):
            self.enter_phone(lead_data.get("phone"))
        
        if lead_data.get("email"):
            self.enter_email(lead_data.get("email"))
        
        self.click_create_lead()
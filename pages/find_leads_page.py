"""
Find Leads Page module with elements and actions
"""
from base.base_page import BasePage

class FindLeadsPage(BasePage):
    """Find Leads page class with methods and selectors"""
    
    # Selectors
    FIRST_NAME_INPUT = "//input[@name='firstName']"
    LAST_NAME_INPUT = "//input[@name='lastName']"
    COMPANY_NAME_INPUT = "//input[@name='companyName']"
    FIND_LEADS_BUTTON = "//button[text()='Find Leads']"
    
    # Results table selectors
    FIRST_RESULT_LINK = "(//div[@class='x-grid3-cell-inner x-grid3-col-partyId']/a)[1]"
    NO_RECORDS_MESSAGE = "//div[text()='No records to display']"
    
    def __init__(self, page):
        super().__init__(page)
    
    def enter_first_name(self, first_name):
        """Enter first name in search field"""
        self.fill_text(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name):
        """Enter last name in search field"""
        self.fill_text(self.LAST_NAME_INPUT, last_name)
    
    def enter_company_name(self, company_name):
        """Enter company name in search field"""
        self.fill_text(self.COMPANY_NAME_INPUT, company_name)
    
    def click_find_leads(self):
        """Click Find Leads button"""
        self.click(self.FIND_LEADS_BUTTON)
        # Wait for results to load
        self.page.wait_for_load_state("networkidle")
    
    def click_first_result(self):
        """Click on the first lead in results"""
        self.wait_for_element(self.FIRST_RESULT_LINK)
        self.click(self.FIRST_RESULT_LINK)
    
    def search_by_name(self, first_name="", last_name=""):
        """
        Search for leads by name
        
        Args:
            first_name: First name to search for
            last_name: Last name to search for
        """
        if first_name:
            self.enter_first_name(first_name)
        
        if last_name:
            self.enter_last_name(last_name)
        
        self.click_find_leads()
    
    def search_by_company(self, company_name):
        """
        Search for leads by company name
        
        Args:
            company_name: Company name to search for
        """
        self.enter_company_name(company_name)
        self.click_find_leads()
    
    def are_results_found(self):
        """Check if any search results were found"""
        return not self.is_visible(self.NO_RECORDS_MESSAGE)
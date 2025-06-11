"""
Test module for find leads functionality
"""

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.my_home_page import MyHomePage
from pages.leads_page import LeadsPage
from pages.create_lead_page import CreateLeadPage
from pages.find_leads_page import FindLeadsPage
from pages.view_lead_page import ViewLeadPage
from utils.data_helper import DataHelper

class TestFindLeads:
    """Test class for find leads functionality"""
    
    @pytest.fixture(scope="function")
    def authenticated_page(self, page, test_data):
        """Fixture to perform login and return authenticated page"""
        login_page = LoginPage(page)
        home_page = HomePage(page)
        
        login_page.navigate_to_login()
        login_page.perform_login(
            test_data["valid_user"]["username"],
            test_data["valid_user"]["password"]
        )
        
        home_page.click_crm_sfa_link()
        return page
    
    @pytest.fixture(scope="function")
    def created_lead(self, authenticated_page):
        """Fixture to create a test lead and return its data"""
        lead_data = DataHelper.generate_test_lead_data()
        
        my_home_page = MyHomePage(authenticated_page)
        leads_page = LeadsPage(authenticated_page)
        create_lead_page = CreateLeadPage(authenticated_page)

        my_home_page.click_leads_tab()
        leads_page.click_create_lead()
        create_lead_page.create_new_lead(lead_data)
        my_home_page.click_leads_tab()

        return lead_data
    
    def test_find_by_first_name(self, authenticated_page, created_lead):
        """Test searching for leads by first name"""
        my_home_page = MyHomePage(authenticated_page)
        leads_page = LeadsPage(authenticated_page)
        find_leads_page = FindLeadsPage(authenticated_page)
        view_lead_page = ViewLeadPage(authenticated_page)
        
        my_home_page.click_leads_tab()
        leads_page.click_find_leads()
        #leads_page.search_created_lead(created_lead["firstName"])

        find_leads_page.search_by_name(first_name=created_lead["firstName"])
        assert find_leads_page.are_results_found(), f"No results for first name: {created_lead['firstName']}"

        find_leads_page.click_first_result()
        actual_first_name = view_lead_page.get_text(view_lead_page.FIRST_NAME)
        assert actual_first_name == created_lead["firstName"], f"Expected: {created_lead['firstName']}, Got: {actual_first_name}"

    def test_find_by_company_name(self, authenticated_page, created_lead):
        """Test searching for leads by company name"""
        my_home_page = MyHomePage(authenticated_page)
        leads_page = LeadsPage(authenticated_page)
        find_leads_page = FindLeadsPage(authenticated_page)
        view_lead_page = ViewLeadPage(authenticated_page)
        
        my_home_page.click_leads_tab()
        leads_page.click_find_leads()

        find_leads_page.search_by_company(created_lead["companyName"])
        assert find_leads_page.are_results_found(), f"No results for company: {created_lead['companyName']}"

        find_leads_page.click_first_result()
        actual_company = view_lead_page.get_text(view_lead_page.COMPANY_NAME)
        assert actual_company == created_lead["companyName"], f"Expected: {created_lead['companyName']}, Got: {actual_company}"

"""
Test module for lead creation functionality
"""

import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.my_home_page import MyHomePage
from pages.leads_page import LeadsPage
from pages.create_lead_page import CreateLeadPage
from pages.view_lead_page import ViewLeadPage
from pages.find_leads_page import FindLeadsPage
from utils.data_helper import DataHelper

class TestCreateLead:
    """Test class for lead creation functionality"""

    @pytest.fixture(scope="function")
    def lead_data(self):
        """Fixture to generate random lead data for testing"""
        return DataHelper.generate_test_lead_data()

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

    def test_create_new_lead(self, authenticated_page, lead_data):
        """Test creating a new lead"""
        my_home_page = MyHomePage(authenticated_page)
        leads_page = LeadsPage(authenticated_page)
        create_lead_page = CreateLeadPage(authenticated_page)
        view_lead_page = ViewLeadPage(authenticated_page)

        my_home_page.click_leads_tab()
        assert leads_page.verify_leads_page_loaded(), "Leads page did not load correctly"

        leads_page.click_create_lead()
        create_lead_page.create_new_lead(lead_data)

        assert view_lead_page.verify_lead_details(lead_data), "Created lead details do not match"

    def test_create_and_find_lead(self, authenticated_page, lead_data):
        """Test creating a lead and then finding it"""
        my_home_page = MyHomePage(authenticated_page)
        leads_page = LeadsPage(authenticated_page)
        create_lead_page = CreateLeadPage(authenticated_page)
        view_lead_page = ViewLeadPage(authenticated_page)
        find_leads_page = FindLeadsPage(authenticated_page)

        my_home_page.click_leads_tab()
        leads_page.click_create_lead()
        create_lead_page.create_new_lead(lead_data)
        lead_id = view_lead_page.get_lead_id()

        my_home_page.click_leads_tab()
        leads_page.click_find_leads()

        find_leads_page.search_by_name(
            first_name=lead_data["firstName"],
            last_name=lead_data["lastName"]
        )

        assert find_leads_page.are_results_found(), f"No search results found for lead ID {lead_id}"

        find_leads_page.click_first_result()
        assert view_lead_page.verify_lead_details(lead_data), "Searched lead details do not match"

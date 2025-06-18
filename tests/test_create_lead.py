import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.my_home_page import MyHomePage
from pages.leads_page import LeadsPage
from pages.create_lead_page import CreateLeadPage
from utils.data_helper import DataHelper 

class TestCreateLead:
    @pytest.fixture(scope="function")
    def authenticated_page(self, page, test_data):  # test_data comes from conftest
        login_page = LoginPage(page)
        home_page = HomePage(page)

        login_page.navigate_to_login()
        login_page.perform_login(
            test_data["valid_user"]["username"],
            test_data["valid_user"]["password"]
        )

        home_page.click_crm_sfa_link()
        return page

    @pytest.mark.parametrize("lead_data", DataHelper.read_leads_from_csv("data/leads_data.csv"))
    def test_create_new_lead(self, authenticated_page, lead_data):
        my_home_page = MyHomePage(authenticated_page)
        leads_page = LeadsPage(authenticated_page)
        create_lead_page = CreateLeadPage(authenticated_page)

        my_home_page.click_leads_tab()
        assert leads_page.verify_leads_page_loaded(), "Leads page did not load correctly"

        leads_page.click_create_lead()
        create_lead_page.create_new_lead(lead_data)

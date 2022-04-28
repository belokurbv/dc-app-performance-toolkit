import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.confluence.pages.pages import Login, AllUpdates
from util.conf import CONFLUENCE_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_pages']:
        app_specific_page_id = datasets['custom_page_id']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.wait_for_page_loaded()
    #         login_page.set_credentials(username=username, password=password)
    #         login_page.click_login_button()
    #         if login_page.is_first_login():
    #             login_page.first_user_setup()
    #         all_updates_page = AllUpdates(webdriver)
    #         all_updates_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("selenium_instantsearch")
    def measure():

        @print_timing("selenium_instantsearch:view_log_table_page")
        def view_log_table_page():
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/display/INSTASEARCH/instantsearchlogtable")
            page.wait_until_visible((By.ID, "popularTable"))
            page.wait_until_visible((By.ID, "failedTable"))
            page.wait_until_visible((By.ID, "userSearchTable"))
        view_log_table_page()


        @print_timing("selenium_instantsearch:view_macro_page_and_search")
        def view_macro_page_and_search():
            page.go_to_url(f"{CONFLUENCE_SETTINGS.server_url}/display/INSTASEARCH/instantsearchmacro")
            page.wait_until_visible((By.CLASS_NAME, "plugin_instantsearch_searchbox"))
            page.get_element((By.CLASS_NAME, "plugin_instantsearch_searchbox")).send_keys("page")
            page.wait_until_visible((By.CLASS_NAME, "plugin_instantsearch_returnedSearchResult"))
        view_macro_page_and_search()

    measure()

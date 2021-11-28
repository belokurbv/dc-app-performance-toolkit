import random
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    actions = ActionChains(webdriver)

    userId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))


    @print_timing("selenium_app_specific_user_login")
    def measure():
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.set_credentials(username=username, password=password)
            if login_page.is_first_login():
                login_page.first_login_setup()
            if login_page.is_first_login_second_page():
                login_page.first_login_second_page_setup()
            login_page.wait_for_page_loaded()
        app_specific_user_login(username='admin', password='admin')
    measure()


    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_entries")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/catalogDictionary.jspa")
        sub_measure()

        @print_timing("selenium_app_custom_action:create_entry")
        def sub_measure():
            page.wait_until_visible((By.ID, "add-record"))
            addButton = page.get_element((By.ID, "add-record"))
            addButton.click()
            page.wait_until_visible((By.ID, "clients-custom_dict_1_name"))
            entryInput = page.get_element((By.ID, "clients-custom_dict_1_name"))
            entryInput.clear()
            entryInput.send_keys(userId + "catalogtest")
            page.wait_until_visible((By.CLASS_NAME, "tl-catalog-save-cl-btn-"))
            addButton = page.get_element((By.CLASS_NAME, "tl-catalog-save-cl-btn-"))
            addButton.click()
        sub_measure()

        @print_timing("selenium_app_custom_action:create_issue_with_custom_catalog_field")
        def sub_measure():
            page.wait_until_visible((By.ID, "create_link"))
            createButton = page.wait_until_visible((By.ID, "create_link"))
            createButton.click()
            page.wait_until_visible((By.ID, "summary"))
            summaryInput = page.get_element((By.ID, "summary"))
            summaryInput.clear()
            summaryInput.send_keys(userId + "catalogtest")
            page.wait_until_visible((By.ID, "tl-ctl-dict-picker-customfield_11100-field"))
            customInput = page.get_element((By.ID, "tl-ctl-dict-picker-customfield_11100-field"))
            customInput.clear()
            customInput.send_keys("test")
            submitButton = page.wait_until_visible((By.ID, "create-issue-submit"))
            submitButton.click()
        sub_measure()
    measure()


import random
import string

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
        @print_timing("selenium_app_custom_action:create-filter")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/RapidView.jspa?rapidView=66&tab=agile-custom-filters-configuration-page")
            page.wait_until_visible((By.ID, "fieldcode-create-field"))
            input = page.get_element((By.ID, "fieldcode-create-field"))
            input.send_keys("Summary")
            page.wait_until_visible((By.XPATH, "//*[contains(text(), 'Summary')]"))
            summaryoption = page.get_element((By.XPATH, "//*[contains(text(), 'Summary')]"))
            summaryoption.click()
            addButton = page.get_elements((By.CLASS_NAME, "aui-button-primary"))
            addButton[8].click()
            page.wait_until_visible((By.XPATH, '//*[@id="agile-board-custom-filters"]/tbody[2]/tr/td[4]/a'))
            webdriver.save_screenshot(userId + 'addfilter.png')
        sub_measure()

        @print_timing("selenium_app_custom_action:use-filter")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/RapidBoard.jspa?rapidView=66&projectKey=AG&selectedIssue=AG-1")
            page.wait_until_visible((By.ID, "tl-board-custom-filter-summary"))
            filterinput = page.get_element((By.ID, "tl-board-custom-filter-summary"))
            filterinput.clear()
            filterinput.send_keys("agiletest")
            filterinput.send_keys(Keys.ENTER)
            page.wait_until_visible((By.XPATH, "//*[contains(text(), 'agiletest')]"))
        sub_measure()

        @print_timing("selenium_app_custom_action:delete-filter")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/RapidView.jspa?rapidView=66&tab=agile-custom-filters-configuration-page")
            page.wait_until_visible((By.XPATH, '//*[@id="agile-board-custom-filters"]/tbody[2]/tr/td[4]/a'))
            deletebtn = page.get_element((By.XPATH, '//*[@id="agile-board-custom-filters"]/tbody[2]/tr/td[4]/a'))
            deletebtn.click()
            page.wait_until_invisible((By.XPATH, '//*[@id="agile-board-custom-filters"]/tbody[2]/tr/td[4]/a'))
        sub_measure()
    measure()


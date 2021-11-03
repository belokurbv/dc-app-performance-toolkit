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

    userId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))


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
        @print_timing("selenium_app_custom_action:my_subscriptions_page")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/MySubscriptionsAction.jspa")
            page.wait_until_visible((By.ID, "mysubscriptionsList"))
            tabs = page.get_elements((By.CLASS_NAME, "release-report-tab"))
            tabs[1].click()
            page.wait_until_visible((By.ID, "mysubscriptionsList"))
            tabs[2].click()
            page.wait_until_visible((By.ID, "mysubscriptionsList"))
            tabs[3].click()
            page.wait_until_visible((By.ID, "mysubscriptionsList"))
            tabs[4].click()
            page.wait_until_visible((By.ID, "mysubscriptionsList"))
        sub_measure()

        @print_timing("selenium_app_custom_action:subscriptions_page")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/SubscriptionsAction!default.jspa")
            page.wait_until_visible((By.ID, "subscriptionsList"))
            tabs = page.get_elements((By.CLASS_NAME, "release-report-tab"))
            tabs[1].click()
            page.wait_until_visible((By.ID, "subscriptionsList"))
            tabs[2].click()
            page.wait_until_visible((By.ID, "subscriptionsList"))
            tabs[3].click()
            page.wait_until_visible((By.ID, "subscriptionsList"))
            tabs[4].click()
            page.wait_until_visible((By.ID, "subscriptionsList"))
        sub_measure()

        @print_timing("selenium_app_custom_action:search_by_jql")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/SubscriptionsAction!default.jspa")
            page.wait_until_visible((By.ID, "tl-subscr-filters"))
            page.get_element((By.ID, "tl-subscr-filters")).click()
            page.wait_until_visible((By.ID, "tl-subscr-filters-jql-like"))
            jqlinput = page.get_element((By.ID, "tl-subscr-filters-jql-like"))
            jqlinput.send_keys("project = 10201")
            page.get_element((By.CLASS_NAME, "tl-subscr-button-primary")).click()
            page.wait_until_visible((By.ID, "subscriptionsList"))
        sub_measure()
    measure()


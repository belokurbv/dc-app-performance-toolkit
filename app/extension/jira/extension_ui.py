import random
import string
import time

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

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
        @print_timing("selenium_app_custom_action:view_calendar")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/TeamleadCalendarAction.jspa")
            page.wait_until_visible((By.ID, "calendarz"))
        sub_measure()

        @print_timing("selenium_app_custom_action:create_issue")
        def sub_measure():
            page.wait_until_visible((By.XPATH, '//*[@id="calendar-dd"]/div[2]/div/table/tbody/tr/td/div/div/div[2]/div[2]/table/thead/tr/td[4]'))
            date = page.get_element((By.XPATH, '//*[@id="calendar-dd"]/div[2]/div/table/tbody/tr/td/div/div/div[2]/div[2]/table/thead/tr/td[4]'))
            actions.move_to_element(date).perform();
            time.sleep(1)
            actions.click().perform();
            page.wait_until_visible((By.ID, "create-calendar-issue"))
            createbtn = page.get_element((By.ID, "create-calendar-issue"))
            createbtn.click()
            page.wait_until_visible((By.ID, "summary"))
            summaryInput = page.get_element((By.ID, "summary"))
            summaryInput.clear()
            summaryInput.send_keys(userId + "calendartest")
            select = Select(webdriver.find_element_by_id("resolution"))
            select.select_by_value('10030')
            submitButton = page.get_element((By.ID, "create-issue-submit"))
            submitButton.click()
        sub_measure()

        @print_timing("selenium_app_custom_action:create_entry")
        def sub_measure():
            page.wait_until_visible((By.XPATH, '//*[@id="calendar-dd"]/div[2]/div/table/tbody/tr/td/div/div/div[2]/div[2]/table/thead/tr/td[7]'))
            date2 = page.get_element((By.XPATH, '//*[@id="calendar-dd"]/div[2]/div/table/tbody/tr/td/div/div/div[2]/div[2]/table/thead/tr/td[7]'))
            actions.move_to_element(date2).click().perform();
            page.wait_until_visible((By.ID, "create-non-jira-event"))
            createbtn = page.get_element((By.ID, "create-non-jira-event"))
            createbtn.click()
            page.wait_until_visible((By.ID, "event-name"))
            nameInput = page.get_element((By.ID, "event-name"))
            nameInput.clear()
            nameInput.send_keys(userId + "calendartest")
            submitButton = page.get_element((By.XPATH, '//*[@id="choosePopup"]/div/div[2]/button'))
            submitButton.click()
        sub_measure()
    measure()


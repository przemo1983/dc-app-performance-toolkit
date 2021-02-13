import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from util.conf import JIRA_SETTINGS
import time


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    @print_timing("selenium_app_custom_action")
    def measure():

        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible

            WebDriverWait(webdriver, 20).until(
                ec.frame_to_be_available_and_switch_to_it((By.ID, 'tr-frame-panel-results')))
            
            loginButtons = webdriver.find_elements(By.XPATH, "//a[contains(text(),  'Log in to TestRail')]")
            webdriver.save_screenshot('login_' + time.strftime("%Y%m%d-%H%M%S") + '.png')
            if len(loginButtons) > 0:
                loginButtons[0].click()

                webdriver.switch_to.window(webdriver.window_handles[1])
                
                email_add = "jira-dc@testrail.com"
                psw = "Testrail123"
                email_address = (By.ID, "name")

                page.wait_until_visible(email_address)
                
                set_email = "document.getElementById('name').value = '{}';".format(
                    email_add)
                set_password = "document.getElementById('password').value = '{}'".format(
                    psw)
                webdriver.execute_script(set_email)
                webdriver.execute_script(set_password)

                page.get_element((By.ID, "button_primary")).click()

                webdriver.close()
                webdriver.switch_to.window(webdriver.window_handles[0])
                webdriver.refresh()
                webdriver.switch_to.default_content()     
        sub_measure()
    measure()

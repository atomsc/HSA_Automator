"""
Module to set up the browser and handle login.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class BrowserSetup:
    """
    This class sets up the initial browser settings and logs in the user.
    """
    def __init__(self, url_open: str, EMAIL: str, PASSWORD: str):
        """
        Initializes the BrowserSetup instance and logs in the user.

        Parameters:
        url_open (str): URL of the login page.
        EMAIL (str): User's email address.
        PASSWORD (str): User's password.
        """
        self.url_to_open = url_open
        self.driver = None
        self.EMAIL = EMAIL
        self.PASSWORD = PASSWORD
        self.set_browser_up()
        self.login()

    def set_browser_up(self):
        """
        Sets up the Selenium WebDriver and opens the browser.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url_to_open)
        self.driver.maximize_window()
        time.sleep(3)

    def login(self):
        """
        Logs in the user using the provided email and password.
        """
        user_field = self.driver.find_element(By.ID, value="login_email")
        user_field.send_keys(self.EMAIL)
        pass_field = self.driver.find_element(By.ID, value="login_pass")
        pass_field.send_keys(self.PASSWORD)
        sign_in_button_2 = self.driver.find_element(By.ID, value="login")
        sign_in_button_2.click()

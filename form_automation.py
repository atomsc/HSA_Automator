"""
Module to automate form filling using the provided data.
"""

import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class FormAutomation:
    """
    This class automates form filling using the provided data.
    """

    def __init__(self, browser, df: pd.DataFrame):
        """
        Initializes the FormAutomation instance.

        Parameters:
        browser (BrowserSetup): Instance of the BrowserSetup class.
        df (pd.DataFrame): DataFrame containing the data to fill the form.
        """
        self.browser = browser
        self.df = df

    def fill_form(self, row: pd.Series):
        """
        Fills the form with data from a row in the DataFrame.

        Parameters:
        row (pd.Series): Row of data from the DataFrame.
        """
        date_field = self.browser.driver.find_element(By.ID, value="datepicker")
        date_field.send_keys(row['Date'])
        provider_field = self.browser.driver.find_element(By.ID, value="provider")
        provider_field.send_keys(row['Provider'])
        descript_field = self.browser.driver.find_element(By.ID, value="description")
        descript_field.send_keys(row['Type'])
        amount_field = self.browser.driver.find_element(By.ID, value="amount")
        amount_field.send_keys(row['Amount'])
        pmt_method_select = Select(self.browser.driver.find_element(By.ID, value="pmt_method"))
        pmt_method_select.select_by_visible_text(row['Payment Method'])
        from_hsa_field = self.browser.driver.find_element(By.ID, value="reimbursed_amount")
        if row['Payment Method'] == "HSA Account":
            from_hsa_field.send_keys(row['Amount'])
        else:
            from_hsa_field.send_keys(0)
        cat_select = Select(self.browser.driver.find_element(By.ID, value="category"))
        cat_select.select_by_visible_text(row['Category'])
        note = str(row['New Filename']) + str('.pdf')
        notes_field = self.browser.driver.find_element(By.ID, value="notes")
        notes_field.send_keys(note)
        save_button = self.browser.driver.find_element(By.NAME, value="create_purchase")
        save_button.click()

    def run(self):
        """
        Runs the form automation process for each row in the DataFrame.
        """
        for index, row in self.df.iterrows():
            print(row)
            time.sleep(1)
            self.fill_form(row)

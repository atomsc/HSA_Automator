"""
Module to handle the uploading of receipts.
"""

import os
import shutil
import pandas as pd
from selenium.webdriver.common.by import By


class ReceiptUploader:
    """
    This class handles the uploading of receipts.
    """

    def __init__(self, browser, df: pd.DataFrame, directory: str, destination_directory: str):
        """
        Initializes the ReceiptUploader instance.

        Parameters:
        browser (BrowserSetup): Instance of the BrowserSetup class.
        df (pd.DataFrame): DataFrame containing the data.
        directory (str): Directory containing the receipts.
        destination_directory (str): Directory to move the uploaded receipts.
        """
        self.found = None
        self.count = None
        self.browser = browser
        self.df = df
        self.directory = directory
        self.destination_directory = destination_directory

    def search_and_upload_receipt(self):
        """
        Searches for and uploads the processed receipts.
        """
        for index, row in self.df.iterrows():
            self.found = False
            self.count = 0
            if row['In HSA?'] == "Y":
                while not self.found:
                    img_elements = self.browser.driver.find_elements(By.TAG_NAME, "img")[self.count:]
                    for imm_val in img_elements:
                        if self.is_camera_image(imm_val):
                            imm_val.click()
                            self.browser.driver.implicitly_wait(10)
                            note_text = self.get_note_text()
                            if self.is_matching_receipt(note_text, row):
                                self.upload_receipt(note_text)
                                self.move_receipt(note_text)
                                self.save_and_exit()
                                self.found = True
                                break
                            else:
                                self.browser.driver.back()
                                self.browser.driver.implicitly_wait(10)
                                self.count += 1
                                break

    @staticmethod
    def is_camera_image(image_element) -> bool:
        """
        Checks if the image element is a camera image.

        Parameters:
        image_element (WebElement): Image element to check.

        Returns:
        bool: True if the image is a camera image, False otherwise.
        """
        name_value = image_element.get_attribute('src')
        return name_value.split("/")[-1] == "camera.png"

    def get_note_text(self) -> str:
        """
        Retrieves the note text from the form.

        Returns:
        str: Note text.
        """
        note_box = self.browser.driver.find_elements(By.ID, "notes")
        return note_box[0].text if note_box else ""

    @staticmethod
    def is_matching_receipt(note_text: str, row: pd.Series) -> bool:
        """
        Checks if the note text matches the receipt.

        Parameters:
        note_text (str): Note text.
        row (pd.Series): Row of data from the DataFrame.

        Returns:
        bool: True if the note text matches the receipt, False otherwise.
        """
        return note_text == f"{row['New Filename']}.pdf"

    def upload_receipt(self, note_text: str):
        """
        Uploads the receipt file.

        Parameters:
        note_text (str): Note text for the receipt file.
        """
        file_input = self.browser.driver.find_element(By.ID, "image")
        file_input.send_keys(rf'{self.directory}\{note_text}')
        description_input = self.browser.driver.find_element(By.ID, "img_description")
        description_input.send_keys("This is a receipt PDF.")
        submit_button = self.browser.driver.find_element(By.NAME, "upload_image")
        submit_button.click()

    def move_receipt(self, note_text: str):
        """
        Moves the receipt file to the destination directory.

        Parameters:
        note_text (str): Note text for the receipt file.
        """
        source_path = os.path.join(self.directory, note_text)
        destination_path = os.path.join(self.destination_directory, note_text)
        shutil.move(source_path, destination_path)

    def save_and_exit(self):
        """
        Saves the form and exits.
        """
        save_button = self.browser.driver.find_element(By.NAME, "update_purchase")
        save_button.click()
        exit_button = self.browser.driver.find_element(By.NAME, "exit_edit")
        exit_button.click()

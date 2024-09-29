"""
Main script to run the HSA receipt processing application.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from pdf_checker import PDFChecker
from user_transaction_input import UserTransactionInput
from pdf_receipt_processor import PDFReceiptProcessor
from user_input import UserInput
from dataframe_to_excel import DataFrameToExcel
from browser_setup import BrowserSetup
from form_automation import FormAutomation
from receipt_uploader import ReceiptUploader
from missing_receipt_processor import MissingReceiptProcessor


def main():
    """
    Main function to drive the entire process of handling HSA receipts.
    """
    # df = pd.DataFrame()
    df_receipts = pd.DataFrame()
    df_non_receipt = pd.DataFrame()

    # url of the login page
    url = "https://trackhsa.com/login"

    # Directory containing the receipts to be processed
    directory_path = "MAIN_PATH_OF_HSA_INFO"

    # Location of the Excel file containing HSA transactions
    excel_file_loc = "PATH_AND_FILE_OF_EXCEL_TRANSACTIONS"

    # Load environment variables from the specified .env file
    dotenv_path = ".env PASSWORD AND EMAIL/USERNAME"
    load_dotenv(dotenv_path)

    # Retrieve email and password from environment variables
    email = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_PASSWORD')

    is_new_trans = int(input("Are you entering new transactions? (1 for yes, 0 for no): "))
    if is_new_trans == 1:
        non_receipt_data = []

        # Check if PDFs exist in the directory
        pdf_checker = PDFChecker(directory_path)
        has_receipts = pdf_checker.check_pdfs_exist()

        if has_receipts:
            # Instantiate the PDFReceiptProcessor class with the directory path
            pdf_renamer = PDFReceiptProcessor(directory_path, excel_file_loc)
            pdf_renamer.rename_pdfs()  # Rename the PDFs based on extracted information
            # Convert the processed data to a DataFrame
            df_receipts = pdf_renamer.to_dataframe()

        # Ask the user if they have transactions without receipts
        user_input_handler = UserTransactionInput()
        if user_input_handler.ask_user_for_transactions_without_receipt():
            number_non_receipt_transactions = user_input_handler.get_number_of_transactions()
            for transaction_number in range(1, number_non_receipt_transactions + 1):
                user_input = UserInput('', excel_file_loc, transaction_number, False)
                user_in = user_input.get_user_inputs()
                non_receipt_data.append(user_in)
                current_non_receipt_data = user_in
                df_current_non = pd.DataFrame(current_non_receipt_data, index=[0])
                processor = DataFrameToExcel(df_current_non, excel_file_loc)
                processor.process()  # Save the updated DataFrame to the Excel file
            df_non_receipt = pd.DataFrame(non_receipt_data)

        df = pd.concat([df_receipts, df_non_receipt], axis=0)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

        # If the DataFrame is not empty, proceed with the automation tasks
        if not df.empty:
            # Initialize the browser and login using the provided url, email, and password
            browser = BrowserSetup(url, email, password)

            # Perform form automation tasks using the processed data
            form_automation = FormAutomation(browser, df)
            form_automation.run()  # Fill out the form with the data from the DataFrame

            if has_receipts:
                # Search for and upload the processed receipts
                uploader = ReceiptUploader(browser, df, directory_path, directory_path + "\Receipts")
                uploader.search_and_upload_receipt()
        else:
            # If no receipts were found or processed, notify the user
            print("NO TRANSACTIONS!")
    else:
        # Load the transactions from the Excel file
        df_transactions = pd.read_excel(excel_file_loc)
        mr = MissingReceiptProcessor(df_transactions, excel_file_loc, directory_path, url, email, password)
        mr.process_receipt_selection()


if __name__ == "__main__":
    main()

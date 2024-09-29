"""
Module to handle user inputs for receipt details.
"""

import re
import pandas as pd


class UserInput:
    """
    This class handles user inputs and validation for receipt details.
    """

    def __init__(self, filename: str, transaction_directory: str, receipt_count: int, is_receipt: bool):
        """
        Initializes the UserInput instance.

        Parameters:
        filename (str): Name of the PDF file.
        transaction_directory (str): Directory containing the transaction Excel file.
        receipt_count (int): Number of receipts processed so far.
        is_receipt (bool): Whether the input is for a receipt.
        """
        self.amount = None
        self.provider = None
        self.date = None
        self.filename = filename
        self.receipt_count = receipt_count
        self.transaction_directory = transaction_directory
        self.is_receipt = is_receipt

    def get_next_receipt_number(self) -> tuple[int, int]:
        """
        Gets the next receipt number based on existing data.

        Returns:
        tuple[int, int]: Next numbers for F and R receipts.
        """
        current_file_df = pd.read_excel(self.transaction_directory)
        receipt_list = list(current_file_df['Receipt no'])
        r_values = [int(re.findall(r'\d+', item)[0]) for item in receipt_list if 'R' in item]
        f_values = [int(re.findall(r'\d+', item)[0]) for item in receipt_list if 'F' in item]
        f_next = max(f_values) if f_values else 0
        r_next = max(r_values) if r_values else 0
        return f_next + 1, r_next + 1

    @staticmethod
    def _validate_date(date_str: str) -> bool:
        """
        Validates the date format.

        Parameters:
        date_str (str): Date string to validate.

        Returns:
        bool: True if the date is valid, False otherwise.
        """
        date_pattern = r'\b(\d{2}/\d{2}/\d{4})\b'
        if re.match(date_pattern, date_str):
            return True
        else:
            print("Invalid date format. Please enter the date in DD/MM/YYYY format.")
            return False

    @staticmethod
    def _validate_amount(amount_str: str) -> bool:
        """
        Validates the amount format.

        Parameters:
        amount_str (str): Amount string to validate.

        Returns:
        bool: True if the amount is valid, False otherwise.
        """
        amount_pattern = r'^\d+(\.\d{1,2})?$'
        if re.match(amount_pattern, amount_str):
            return True
        else:
            print("Invalid amount format. Please enter a valid number.")
            return False

    @staticmethod
    def _get_user_choice(prompt: str, choices: list[str]) -> str:
        """
        Prompts the user to choose from a list of options.

        Parameters:
        prompt (str): Prompt message for the user.
        choices (list[str]): List of choices for the user to select from.

        Returns:
        str: User's selected choice.
        """
        while True:
            print(prompt)
            for idx, choice in enumerate(choices, 1):
                print(f"{idx}. {choice}")
            try:
                selection = int(input("Choose an option by number: ").strip())
                if 1 <= selection <= len(choices):
                    return choices[selection - 1]
                else:
                    print("That's not a valid choice. Please choose again.")
            except ValueError:
                print("That's not a valid choice. Please choose again.")

    def get_user_inputs(self) -> dict:
        """
        Collects and validates user inputs for the receipt details.

        Returns:
        dict: Dictionary containing the user inputs.
        """
        valid_date = False
        valid_amount = False
        while not valid_date:
            self.date = input("Enter the date (DD/MM/YYYY): ").strip()
            valid_date = self._validate_date(self.date)
        self.provider = input("Enter the provider: ").strip()
        while not valid_amount:
            self.amount = input("Enter the amount: ").strip()
            valid_amount = self._validate_amount(self.amount)
        type_choice = self._get_user_choice("Select the type:", ["Medical", "Other"])
        category_choice = self._get_user_choice("Select the category:",
                                                ["Prescriptions", "Therapy / counseling", "Doctor", "Dental",
                                                 "Lab / Tests", "Vision"])
        payment_method_choice = self._get_user_choice("Select the payment method:", ["HSA Account", "Credit"])
        f_next, r_next = self.get_next_receipt_number()
        if payment_method_choice == "HSA Account":
            receipt_number = f"R{r_next}"
        else:
            receipt_number = f"F{f_next}"
        print(f"Suggested Receipt Number: {receipt_number}")
        while True:
            confirmation = input("Is this receipt number OK? Enter 1 for Yes, 0 for No: ").strip()
            if confirmation == '1':
                break
            elif confirmation == '0':
                receipt_number = input("Enter the correct receipt number: ").strip()
                break
            else:
                print("Invalid input. Please enter 1 for Yes or 0 for No.")
        hsa_cash_bal = "-"
        attachments = "Y" if self.is_receipt else "N"
        in_hsa = "Y" if payment_method_choice == "HSA Account" else "N"
        notes = input("NOTES: ").strip()
        new_name = f"{receipt_number}_{self.amount}"
        user_inputs = {
            'Date': self.date,
            'Provider': self.provider,
            'Amount': self.amount,
            'HSA Cash Balance': hsa_cash_bal,
            'Attachments': attachments,
            'Receipt Number': receipt_number,
            'In HSA?': in_hsa,
            'Notes': notes,
            'New Filename': new_name if new_name else self.filename,
            'Type': type_choice,
            'Category': category_choice,
            'Payment Method': payment_method_choice
        }
        return user_inputs

"""
Module to handle user prompts for transactions without receipts.
"""


class UserTransactionInput:
    """
    This class handles user prompts for transactions without receipts.
    """

    @staticmethod
    def ask_user_for_transactions_without_receipt() -> bool:
        """
        Asks the user if they have transactions without receipts.

        Returns:
        bool: True if the user has transactions without receipts, False otherwise.
        """
        response = input("Do you have transactions without receipts? (yes/no): ").strip().lower()
        return response == 'yes'

    @staticmethod
    def get_number_of_transactions() -> int:
        """
        Asks the user for the number of transactions without receipts.

        Returns:
        int: Number of transactions without receipts.
        """
        return int(input("How many transactions do you have to enter: "))

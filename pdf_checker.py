"""
Module to check if there are any PDFs in the specified directory.
"""

import os


class PDFChecker:
    """
    This class checks if there are any PDFs in the specified directory.
    """

    def __init__(self, directory_path: str):
        """
        Initializes the PDFChecker instance.

        Parameters:
        directory_path (str): Path to the directory to check for PDFs.
        """
        self.directory_path = directory_path

    def check_pdfs_exist(self) -> bool:
        """
        Checks if there are any PDF files in the directory.

        Returns:
        bool: True if there are PDF files, False otherwise.
        """
        return any(file.endswith('.pdf') for file in os.listdir(self.directory_path))

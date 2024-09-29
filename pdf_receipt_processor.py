"""
Module to process PDF receipts.
"""

import os
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from pdf_reader import PDFReader
from user_input import UserInput
from dataframe_to_excel import DataFrameToExcel
import fitz


class PDFReceiptProcessor:
    """
    This class processes PDF receipts, extracts relevant data, and renames the PDFs.
    """

    def __init__(self, directory_path: str, transaction_directory: str):
        """
        Initializes the PDFReceiptProcessor instance.

        Parameters:
        directory_path (str): Directory containing the PDF receipts.
        transaction_directory (str): Directory containing the transaction Excel file.
        """
        self.directory_path = directory_path
        self.data = []
        self.transaction_directory = transaction_directory
        self.receipt_count = 0

    @staticmethod
    def display_pdf_page(file_to_open: str, page_number: int = 0):
        """
        Displays a specific page of a PDF file.

        Parameters:
        file_to_open (str): Path to the PDF file.
        page_number (int): Page number to display (default is 0).
        """
        doc = fitz.open(file_to_open)
        page = doc.load_page(page_number)
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        fig, ax = plt.subplots(figsize=(pix.width / 100, pix.height / 100), dpi=250)
        ax.imshow(image)
        ax.axis('off')
        plt.show(block=False)

    def display_pdf_info(self, file_path: str, filename: str):
        """
        Displays information extracted from a PDF file.

        Parameters:
        file_path (str): Path to the PDF file.
        filename (str): Name of the PDF file.
        """
        pdf_reader = PDFReader(file_path)
        self.display_pdf_page(file_path)
        print(f"Filename: {filename}")
        print("\nExtracted Text:\n")
        print(pdf_reader.text)
        print("\nExtracted Information:\n")
        print("\n" + "-" * 80 + "\n")

    def rename_pdfs(self):
        """
        Renames PDF files based on extracted information.
        """
        pdf_files = [f for f in os.listdir(self.directory_path) if f.lower().endswith('.pdf')]
        if not pdf_files:
            print("No PDF files found in the directory.")
            return

        for filename in pdf_files:
            self.receipt_count += 1
            file_path = os.path.join(self.directory_path, filename)
            self.display_pdf_info(file_path, filename)
            user_input = UserInput(filename, self.transaction_directory, self.receipt_count, True)
            user_in = user_input.get_user_inputs()
            self.data = user_in
            receipt_number = user_in['Receipt Number']
            new_name = f"{receipt_number}_{user_in['Amount']}"
            if new_name:
                new_file_path = os.path.join(self.directory_path, new_name + '.pdf')
                os.rename(file_path, new_file_path)
                print(f"Renamed '{filename}' to '{new_name}.pdf'\n")
            else:
                print(f"Skipped renaming '{filename}'\n")
            df = self.to_dataframe()
            processor = DataFrameToExcel(df, self.transaction_directory)
            processor.process()

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the extracted data to a DataFrame.

        Returns:
        pd.DataFrame: DataFrame containing the extracted data.
        """
        return pd.DataFrame(self.data, index=[0])

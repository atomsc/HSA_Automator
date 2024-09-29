"""
Module to read text from PDF files.
"""

import fitz  # PyMuPDF


class PDFReader:
    """
    This class reads the text from a PDF file.
    """

    def __init__(self, file_path: str):
        """
        Initializes the PDFReader instance.

        Parameters:
        file_path (str): Path to the PDF file.
        """
        self.file_path = file_path
        self.text = self._read_pdf()

    def _read_pdf(self) -> str:
        """
        Reads and extracts text from the PDF file.

        Returns:
        str: Extracted text from the PDF file.
        """
        pdf_document = fitz.open(self.file_path)
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
        return text

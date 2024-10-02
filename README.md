# HSA Receipt Processing Application

This application automates the process of handling Health Savings Account (HSA) receipts. It includes functionality for renaming PDF files based on extracted information, uploading receipts to a web form, and updating an Excel file with transaction details.

## Features

- **PDF Renaming**: Automatically renames PDF receipts based on extracted information such as date, provider, and amount.
- **Form Automation**: Fills out forms on the HSA portal using data extracted from receipts and provided by the user.
- **Receipt Uploading**: Uploads receipts to the HSA portal.
- **Excel Update**: Updates an Excel file with transaction details and styles the data appropriately.
- **Missing Receipt Handling**: Processes transactions with missing receipts and updates the Excel file accordingly.

## Requirements

- Python 3.x
- `pandas`
- `openpyxl`
- `PyMuPDF`
- `selenium`
- `python-dotenv`
- A Chrome WebDriver

## Setup

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install Dependencies**:
    ```bash
    pip install pandas openpyxl pymupdf selenium python-dotenv
    ```

3. **Set Up Environment Variables**:
    - Create a `.env` file in the project directory with your email and password for the HSA portal:
      ```
      EMAIL_ADDRESS=your-email@example.com
      EMAIL_PASSWORD=your-password
      ```

4. **Set Up WebDriver**:
    - Download Chrome WebDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in a directory included in your system PATH.

5. **Directory Structure**:
    - Ensure your directories are structured as follows:
      ```
      project-directory/
      ├── main.py
      ├── browser_setup.py
      ├── pdf_reader.py
      ├── pdf_receipt_processor.py
      ├── user_input.py
      ├── form_automation.py
      ├── receipt_uploader.py
      ├── dataframe_to_excel.py
      ├── missing_receipt_processor.py
      ├── pdf_checker.py
      ├── user_transaction_input.py
      └── .env
      ```

## Usage

1. **Run the Application**:
    ```bash
    python main.py
    ```

2. **Follow the Prompts**:
    - The application will prompt you to enter new transactions or process missing receipts.
    - Provide necessary details when prompted, such as date, provider, amount, and other transaction details.

## File Descriptions

- **main.py**: Entry point of the application. Handles workflow for processing new transactions and missing receipts.
- **browser_setup.py**: Sets up the Selenium WebDriver and handles user login.
- **pdf_reader.py**: Reads text from PDF files using PyMuPDF.
- **pdf_receipt_processor.py**: Processes PDF receipts by extracting information and renaming files.
- **user_input.py**: Handles user input for receipt details and validates the input.
- **form_automation.py**: Automates form filling on the HSA portal using data from a DataFrame.
- **receipt_uploader.py**: Searches for and uploads receipts to the HSA portal.
- **dataframe_to_excel.py**: Processes and saves data from a DataFrame to an Excel workbook.
- **missing_receipt_processor.py**: Processes missing receipts by updating the Excel file and uploading matching receipts.
- **pdf_checker.py**: Checks if there are any PDF files in the specified directory.
- **user_transaction_input.py**: Handles user prompts for entering transactions without receipts.

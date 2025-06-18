# ResearchAI
Homemade AI, this will require some configuration to work for you!
# AI Research Assistant Setup Guide

This document provides a step-by-step guide to setting up and running the AI Research Assistant on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python:** Version 3.6 or higher. Download from [python.org](https://www.python.org/downloads/).
*   **pip:** Python's package installer (should come with Python 3).

## Step 1: Setting Up the Environment

1.  **Install Git:** If you don't have it already, install Git from [git-scm.com](https://git-scm.com/).

2.  **Clone the Repository:**
    ```
    git clone https://github.com/usrtem/ResearchAI.git
    cd <repository_directory>
    ```
    Replace `<repository_directory>` with the name of the directory.

## Step 2: Setting Up a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies for this project.

1.  **Create a Virtual Environment:**
    ```
    python -m venv venv
    ```
    This command creates a new virtual environment named `venv` in your project directory.

2.  **Activate the Virtual Environment:**
    *   On Windows:
        ```
        venv\Scripts\activate
        ```
    *   On macOS and Linux:
        ```
        source venv/bin/activate
        ```

## Step 3: Installing Dependencies

1.  **Install Required Packages:**
    ```
    pip install python-docx PyPDF2 google-generativeai tkinter beautifulsoup4 requests validators openpyxl
    ```
    This command installs the necessary Python packages, including:
    *   `python-docx`: For reading `.docx` files.
    *   `PyPDF2`: For reading `.pdf` files.
    *   `openpyxl`: For reading `.xlsx` files.
    *   `google-generativeai`: For accessing the Gemini API.
    *   `tkinter`: For the GUI.
    *   `beautifulsoup4`: For web scraping.
    *   `requests`: For making HTTP requests.
    *   `validators`: For validating URLs.

## Step 4: Configuring the API Key

1.  **Set the Environment Variable:**

    *   **Get Your API Key:** Obtain an API key from Google AI Studio.

    *   **Set the Environment Variable:** You need to set the `GOOGLE_AI_API_KEY` environment variable.

        *   **On Windows:**
            ```
            setx GOOGLE_AI_API_KEY "YOUR_API_KEY"
            ```
            (Note: This change may require a restart to take effect.)

        *   **On macOS and Linux:**
            Add the following line to your `.bashrc` or `.zshrc` file:
            ```
            export GOOGLE_AI_API_KEY="YOUR_API_KEY"
            ```
            Then, run:
            ```
            source ~/.bashrc  # or source ~/.zshrc
            ```

    Replace `"YOUR_API_KEY"` with your actual API key.

## Step 5: Setting up the Documents Directory

1.  **Create the DOCS Directory:**

    *   The script is configured to read documents from the directory `C:\Scripts\DOCS`. Create this directory on your machine.

    *   **Alternatively, you can modify the `docs_dir` variable** in the script to point to a different directory of your choice.

2.  **Place Documents:**

    *   Place any `.txt`, `.docx`, and `.pdf` documents that you want the AI to use as context into this directory.

## Step 6: Running the Application

1.  **Run the Script:**
    ```
    python your_script_name.pyw
    ```
    Replace `your_script_name.pyw` with the actual name of the Python file.

## Additional Notes

*   **Hiding the Console Window:**
    *   The script attempts to hide the console window on Windows. If you encounter issues or want to see the console output for debugging, comment out or remove the `hide_console_window()` function call in the `main()` function.

*   **Troubleshooting:**
    *   **API Key Errors:** Double-check that you have correctly set the `GOOGLE_AI_API_KEY` environment variable.
    *   **Missing Packages:** If you encounter "ModuleNotFoundError" errors, ensure that you have installed all the required packages using `pip install`.
    *   **File Access Issues:** Ensure that the script has the necessary permissions to read the files in the DOCS directory.

## Usage

1.  Run the script. A GUI window will appear.
2.  Enter your question or a URL in the text entry field.
3.  Press `Enter` or click the appropriate button to get the answer.
4.  Use the "Upload Document" button to add more documents to the DOCS directory.
5.  Click "EXIT" to close the application.
6.  IF you update the documents in the directory while the script is running, you will need to click "RESTART" prior to asking questions on the newly added/modified documents.
7.  IF you are using .xlsx files, ensure that cell data are formatted before performing analysis. For example, in order for the AI to perform math functions, the data cannot be in string format.

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on GitHub.

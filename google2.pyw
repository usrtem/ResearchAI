import os
import docx
from PyPDF2 import PdfReader
import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
import shutil
import ctypes
import requests
from bs4 import BeautifulSoup
import validators
import random
import time

# Function to get the API key from the environment variable
def get_api_key():
    """Retrieves the API key from the environment variables."""
    api_key = os.environ.get("GOOGLE_AI_API_KEY")
    if not api_key:
        raise ValueError("The GOOGLE_AI_API_KEY environment variable is not set.")
    return api_key

# Configure the API key
try:
    genai.configure(api_key=get_api_key())
except ValueError as e:
    print(f"Error configuring API key: {e}")
    exit()

# Create a model
model = genai.GenerativeModel('gemini-2.0-flash')

# Specify the directory path
docs_dir = r'C:\Scripts\DOCS'

def read_document_contents(directory):
    """Reads the contents of all supported documents in the given directory."""
    document_contents = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if filename.endswith(".txt"):  # For .txt files
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    document_contents.append(content)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
        elif filename.endswith(".docx"):  # For .docx files
            try:
                doc = docx.Document(filepath)
                content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                document_contents.append(content)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
        elif filename.endswith(".pdf"):  # For .pdf files
            try:
                pdf_reader = PdfReader(filepath)
                content = "\n".join([page.extract_text() for page in pdf_reader.pages])
                document_contents.append(content)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
        else:
            print(f"Unsupported file type: {filename}")
    
    return document_contents

# User-Agent strings to rotate
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
]

def fetch_and_extract_text_from_url(url):
    """Fetches content from a URL and extracts text using BeautifulSoup, with enhanced error handling."""
    try:
        # 1. Rotate User-Agent
        user_agent = random.choice(user_agents)
        headers = {'User-Agent': user_agent}

        # 2. Introduce a Delay
        time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds

        # 3. Fetch the Content
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4XX, 5XX)

        # 4. Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # 5. Attempt to Extract Content (More Flexible)
        content_div = soup.find('div', {'class': 'feed-shared-update-v2__description-wrapper'}) or soup.find('div', {'class': 'article'}) or soup.find('div', {'class': 'post-content'}) or soup.find('div', {'class': 'description'}) or soup.find('main', {'class': 'content'}) or soup.find('div', {'id': 'content'}) or soup.find('body')

        if not content_div:
            return "Error: Could not find main content on the page (LinkedIn might be blocking)."

        text = ' '.join(content_div.stripped_strings)
        if not text:
            return "Error: Extracted content is empty. LinkedIn might be blocking or the structure is too complex."

        return text

    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"  # Network errors, timeouts, etc.
    except Exception as e:
        return f"Error processing URL: {e}"  # BeautifulSoup errors, etc.

def generate_answer(query, document_contents, url_content=None):
    """Generates an answer based on the query, document contents, and URL content."""
    combined_content = "\n\n".join(document_contents)
    
    if url_content:
        combined_content += f"\n\nContent from URL:\n{url_content}"
    
    #Let the AI use the provided content to answer the question
    prompt = f"{query}\n\n{combined_content}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failed to generate answer."

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Mike's AI Research Assistant")
        self.document_contents = read_document_contents(docs_dir)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.text_area.config(state=tk.DISABLED)  # Make it read-only

        self.query_label = tk.Label(root, text="What would you like to ask (or provide a URL)?")
        self.query_label.pack()
        self.query_entry = tk.Entry(root, width=50)
        self.query_entry.pack(pady=5, padx=10, fill=tk.X)
        self.query_entry.bind('<Return>', self.ask_question)

        self.upload_button = tk.Button(root, text="Upload Document", command=self.upload_document)
        self.upload_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="EXIT", command=self.root.destroy)
        self.exit_button.pack(pady=5)
        
        self.restart_button = tk.Button(root, text="RESTART", command=self.restart)
        self.restart_button.pack(pady=5)

    def ask_question(self, event=None):
        query = self.query_entry.get().strip()
        
        # Check if the query is a URL
        if validators.url(query):
            self.display_text(f"Question: {query}\n")
            self.display_text(f"Fetching content from URL: {query}\n")
            url_content = fetch_and_extract_text_from_url(query)
            if "Error" in url_content:
                self.display_text(url_content + "\n")  # Display error message
                return
            answer = generate_answer(query, self.document_contents, url_content)
        else:
            self.display_text(f"Question: {query}\n")
            answer = generate_answer(query, self.document_contents)
            
        self.display_text(f"Answer: {answer}" + "\n\n" + "-"*50 + "\n")
        self.query_entry.delete(0, tk.END)  # Clear the entry

    def display_text(self, text):
        self.text_area.config(state=tk.NORMAL)  # Allow editing
        self.text_area.insert(tk.END, text)
        self.text_area.config(state=tk.DISABLED)  # Re-disable editing
        self.text_area.see(tk.END)  # Scroll to the end

    def upload_document(self):
        """Opens a file dialog and uploads the selected document to the DOCS directory."""
        filepath = filedialog.askopenfilename(title="Select Document to Upload")
        if filepath:
            try:
                # Copy the selected file to the DOCS directory
                shutil.copy(filepath, docs_dir)
                self.display_text(f"Uploaded {os.path.basename(filepath)} to {docs_dir}\n")

                # Refresh document contents
                self.document_contents = read_document_contents(docs_dir)
            except Exception as e:
                self.display_text(f"Error uploading document: {e}\n")

    def restart(self):
        """Restarts the application."""
        self.root.destroy()  # Close the current window
        root = tk.Tk()
        app = App(root)
        root.mainloop()


def main():
    hide_console_window()  # Hide the console window
    root = tk.Tk()
    app = App(root)
    root.mainloop()

def hide_console_window():
    """Hides the console window."""
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user_32.ShowWindow(whnd, 0)  # 0 = SW_HIDE

# Hide the console window
if os.name == 'nt':  # Windows
    hide_console_window()

if __name__ == "__main__":
    main()

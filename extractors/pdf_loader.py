"""
pdf_loader.py
-------------
Loads company earnings report PDFs from local storage or URLs.
Prepares them for parsing (e.g., using pdfplumber or PyMuPDF).
"""
import pdfplumber
import os
from tkinter import Tk, filedialog

def select_pdf_file(prompt_title="Select PDF"):
    root = Tk()
    root.call('wm', 'attributes', '.', '-topmost', '1')
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title=prompt_title,
        filetypes=[("PDF Files", "*.pdf")]
    )
    root.destroy()
    if file_path:
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as src, open(filename, 'wb') as dest:
            dest.write(src.read())
        print(f"File '{filename}' uploaded successfully.")
        return filename
    else:
        print("No file uploaded.")
        return None

def extract_text_from_pdf(pdf_file):
    full_text = ""
    if pdf_file:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
        print("PDF text extraction complete.")
    return full_text
    

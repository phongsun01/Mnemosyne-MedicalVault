import os
import PyPDF2
from docx import Document
import pandas as pd
from pdf2image import convert_from_path
import io
import logging

logger = logging.getLogger(__name__)

def parse_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_xlsx(file_path):
    df = pd.read_excel(file_path)
    return df.to_string()

def parse_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        logger.error(f"PDF text extraction failed: {e}")
    
    # If text is too short, consider it a scan and return images for Gemini Vision
    if len(text.strip()) < 100:
        return None, convert_from_path(file_path, first_page=1, last_page=3)
    
    return text, None

def get_file_content(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        return parse_docx(file_path), None
    elif ext in ['.xlsx', '.xls']:
        return parse_xlsx(file_path), None
    elif ext == '.pdf':
        return parse_pdf(file_path)
    elif ext in ['.txt', '.md']:
        with open(file_path, 'r') as f:
            return f.read(), None
    return None, None

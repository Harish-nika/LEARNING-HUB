__version__ = '0.2.6'

import os
import fitz  # PyMuPDF for PDF handling
import pandas as pd
import re
import pytesseract
from langdetect import detect, DetectorFactory
from icecream import ic
from collections import defaultdict
from PIL import Image
from multiprocessing import Pool, Manager
from datetime import datetime
import signal  # For handling manual interruptions
import argparse  # For argument parsing

# Disable Icecream debug output
ic.disable()

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update Tesseract path
DetectorFactory.seed = 0

checkpoint_file = "checkpoint.xlsx"  # Temporary file for checkpointing

def extract_text_from_pdf(pdf_path):
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"File {pdf_path} does not exist.")
    
    pdf_document = fitz.open(pdf_path)
    text_chunks = []
    is_scanned = False
    
    for page_num, page in enumerate(pdf_document):
        text = page.get_text("text")
        
        if not text:
            is_scanned = True
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)
        
        text_cleaned = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
        text_chunks.append(text_cleaned)
    
    pdf_document.close()
    return text_chunks, is_scanned

def detect_languages(text_chunks):
    language_counts = defaultdict(int)
    for text_chunk in text_chunks:
        try:
            detected_lang = detect(text_chunk)
            language_counts[detected_lang] += 1
        except:
            continue
    
    total_chunks = len(text_chunks)
    language_percentages = {lang: (count / total_chunks) * 100 for lang, count in language_counts.items()}
    dominant_language = max(language_percentages, key=language_percentages.get) if language_percentages else None
    
    return dominant_language, language_percentages

def process_single_file(pdf_path):
    print(f"Processing single file: {pdf_path}")
    text_chunks, is_scanned = extract_text_from_pdf(pdf_path)
    dominant_language, language_percentages = detect_languages(text_chunks)
    
    print(f"Dominant Language: {dominant_language}")
    for lang, percentage in language_percentages.items():
        print(f"- {lang}: {percentage:.2f}%")
    print(f"Is Scanned: {is_scanned}")

def main():
    parser = argparse.ArgumentParser(description="PDF Language Detection and OCR")
    parser.add_argument("input", help="Input folder or PDF file path")
    parser.add_argument("csv_file", help="CSV file containing PDF filenames", nargs='?', default=None)
    parser.add_argument("output", help="Output directory for saving results", nargs='?', default=None)
    parser.add_argument("num_processes", help="Number of processes to use", type=int, nargs='?', default=4)
    
    args = parser.parse_args()

    if args.csv_file and args.output:
        print("Batch processing is disabled in this version. Use single file processing.")
    else:
        pdf_path = args.input
        process_single_file(pdf_path)

if __name__ == "__main__":
    main()

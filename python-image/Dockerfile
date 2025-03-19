# Use an official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the required files
COPY process_pdfs.py process_pdfs.py
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Change ENTRYPOINT to accept arguments
ENTRYPOINT ["python", "process_pdfs.py"]
CMD []

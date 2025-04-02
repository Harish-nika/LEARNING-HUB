# Language Distribution Finder - Dockerized

This project is a Python-based PDF language detection tool that extracts text from PDFs, detects the dominant language, and determines whether the document is scanned. The project is containerized using Docker for easy deployment and execution.

## **Table of Contents**
- [Prerequisites](#prerequisites)
- [Containerizing the Application](#containerizing-the-application)
- [Building the Docker Image](#building-the-docker-image)
- [Running the Container](#running-the-container)
- [Debugging Inside the Container](#debugging-inside-the-container)
- [Pushing to Docker Hub](#pushing-to-docker-hub)
- [Pulling and Running the Image](#pulling-and-running-the-image)

---

## **Prerequisites**
Ensure you have the following installed:
- Docker (or Podman if using an alternative)
- Python (for local testing)

---

## **Containerizing the Application**
### **1. Create a `Dockerfile`**
Inside the project directory, create a file named `Dockerfile` with the following content:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the required files into the container
COPY process_pdfs.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the script when the container starts
ENTRYPOINT ["python", "process_pdfs.py"]
```

### **2. Create a `requirements.txt` file**
Ensure your `requirements.txt` includes all dependencies:
```txt
pymupdf
pandas
pytesseract
langdetect
icecream
pillow
```  

---

## **Building the Docker Image**
To build the Docker image, navigate to your project directory and run:

```sh
docker build -t harishkumarthesde/langdistributionfinder:latest .
```

This will create an image named `langdistributionfinder` under your Docker Hub namespace.

---

## **Running the Container**
### **1. Processing a Single PDF**
If your PDF is stored at `/home/harish/isin.pdf`, run:
```sh
docker run --rm -v /home/harish:/app harishkumarthesde/langdistributionfinder:latest /app/isin.pdf
```

### **2. Processing Multiple PDFs from a CSV**
If your project expects a CSV file listing multiple PDFs, mount the input folder and CSV like this:
```sh
docker run --rm -v /home/harish:/app harishkumarthesde/langdistributionfinder:latest /app/input_folder /app/files.csv /app/output_folder
```

---

## **Debugging Inside the Container**
If you encounter file path errors, open an interactive shell inside the container:
```sh
docker run -it --rm -v /home/harish:/app harishkumarthesde/langdistributionfinder:latest /bin/bash
```
Then, verify the files exist:
```sh
ls -l /app/isin.pdf
```
Run the script manually:
```sh
python process_pdfs.py /app/isin.pdf
```

---

## **Pushing to Docker Hub**
To upload your image to Docker Hub, first log in:
```sh
docker login
```
Then, push the image:
```sh
docker push harishkumarthesde/langdistributionfinder:latest
```

---

## **Pulling and Running the Image**
To pull the latest version of your image and run it:
```sh
docker pull harishkumarthesde/langdistributionfinder:latest
docker run --rm -v /home/harish:/app harishkumarthesde/langdistributionfinder:latest /app/isin.pdf
```

This ensures you are always using the latest version of your tool.

---

## **Conclusion**
This guide helps you containerize, build, run, and deploy your PDF processing tool using Docker. Let me know if you need any modifications! 🚀


from fastapi import FastAPI, UploadFile, File
import os
import shutil
import pytesseract
from PyPDF2 import PdfReader

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()

    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        try:
            import cv2
            img = cv2.imread(file_path)
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            return f"Error reading image: {e}"
    else:
        return "Unsupported file type."

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    extracted_text = extract_text(file_location)
    return extracted_text

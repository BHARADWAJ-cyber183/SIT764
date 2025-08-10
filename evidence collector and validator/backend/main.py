import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import shutil

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "evidence collector and validator/backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text(file_path):
    text = ""
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        text = pytesseract.image_to_string(Image.open(file_path))
    return text

# API endpoint to receive uploaded files
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Extract text
    extracted_text = extract_text(file_location)

    return {
        "filename": file.filename,
        "message": "File processed successfully!",
        "extracted_text": extracted_text
    }

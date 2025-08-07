from fastapi import FastAPI, UploadFile, File
import os, shutil
from ocr_rules import match_strategies
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

app = FastAPI()
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

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    strategy_matches = match_strategies(file_path)  # OCR logic

    return {
        "filename": file.filename,
        "extracted_text": text.strip(),
        "matched_strategies": strategy_matches
    }

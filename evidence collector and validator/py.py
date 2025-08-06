import streamlit as st
import pandas as pd
import pytesseract
import cv2
import os
from PIL import Image

# Title
st.title("🛡️ Auditor Collaboration Portal")

# Upload PDF (for future OCR work)
uploaded_file = st.file_uploader("Upload a PDF or Image", type=['pdf', 'png', 'jpg', 'jpeg'])

# File upload section
if uploaded_file is not None:
    st.success(f"Uploaded file: {uploaded_file.name}")

    # Display preview if it's an image
    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # OCR text extraction
        text = pytesseract.image_to_string(image)
        st.subheader("Extracted Text:")
        st.text_area("Text", text, height=200)

# Future Features
st.markdown("✅ Coming soon: Auto-check against Essential 8 policies")

# Footer
st.markdown("---")
st.caption("Developed for SIT764 Security Assessment Portal")

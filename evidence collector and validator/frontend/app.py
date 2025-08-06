import streamlit as st
import requests
import os

# Set page configuration
st.set_page_config(page_title="Evidence Validator", layout="centered")
st.title("📄 Evidence Collector & Validator")

# Confirmation message
st.write("✅ Frontend is working. Please upload a file to begin validation.")

# Ensure temp upload folder exists
os.makedirs("temp_uploads", exist_ok=True)

# Upload file section
uploaded = st.file_uploader("Upload Evidence File (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded:
    files = {"file": uploaded.getvalue()}
    file_name = uploaded.name

    # Save uploaded file locally
    with open(f"temp_uploads/{file_name}", "wb") as f:
        f.write(uploaded.getvalue())

    # Send file to backend FastAPI endpoint
    with open(f"temp_uploads/{file_name}", "rb") as f:
        res = requests.post("http://127.0.0.1:8000/analyze", files={"file": f})

    # Display backend response
    if res.status_code == 200:
        st.success("✅ File processed successfully!")
        st.write("🔍 Extracted Text:")
        st.code(res.text)
    else:
        st.error("❌ Failed to process file. Please ensure the backend is running.")

import streamlit as st
import requests

st.title(" Evidence Collector & Misconfiguration Validator")
st.markdown("Upload an evidence file (image/pdf) to scan for strategy misconfigurations.")

uploaded_file = st.file_uploader("Upload Evidence File", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post("http://127.0.0.1:8000/analyze", files=files)

    if response.status_code == 200:
        data = response.json()
        st.success("File processed successfully!")
        st.subheader("Extracted Text:")
        st.code(data["extracted_text"])

        st.subheader("Matched Strategies:")
        if data["matched_strategies"]:
            for match in data["matched_strategies"]:
                st.write(f"• **{match[0]}** ➝ Keyword: `{match[1]}`")
        else:
            st.warning("No strategy matched.")
    else:
        st.error("Something went wrong.")

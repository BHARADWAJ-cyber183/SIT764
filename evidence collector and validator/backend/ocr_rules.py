import pytesseract
from PIL import Image
import os

# Strategy and related keywords
strategy_rules = {
    "Application Control": ["internet explorer", "java", "ftp"],
    "Patch Applications": ["legacy", "unsupported", "old version"],
    "Configure Microsoft Office Macro Settings": ["macro", "enable content", "visual basic"],
    "User Application Hardening": ["mfa missing", "no mfa", "authentication not configured"],
    "Restrict Administrative Privileges": ["run as administrator", "user account control", "elevated"],
    # You can expand this list as needed
}

# Function to scan image and detect keywords
def match_strategies(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img).lower()
    except Exception as e:
        return f"Error reading image: {e}"

    matches = []

    for strategy, keywords in strategy_rules.items():
        for keyword in keywords:
            if keyword in text:
                matches.append((strategy, keyword))
                break  # avoid duplicate matches per strategy

    return matches

# preprocess.py

import re


def clean_text(text):
    """
    Main preprocessing function.
    """

    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove unwanted special characters
    text = re.sub(r'[^a-zA-Z0-9.,!?\'"\s:-]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text
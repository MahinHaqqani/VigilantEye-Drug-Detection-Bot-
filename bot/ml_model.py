def classify_drug_text(text):
    keywords = [ ... ]  # (Copy the full keyword list here)
    text = text.lower()
    for keyword in keywords:
        if keyword in text:
            return True, 0.92  # Hardcoded probability
    return False, 0.0

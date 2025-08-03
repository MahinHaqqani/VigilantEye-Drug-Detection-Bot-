import json

def extract_drug_words(detected_words=None):
    try:
        with open("detected_words.json", "r") as f:
            existing_words = json.load(f)
        if isinstance(existing_words, dict):
            existing_words = existing_words.get("words", [])
        elif not isinstance(existing_words, list):
            existing_words = []
    except FileNotFoundError:
        existing_words = []
    except Exception as e:
        print(f"Error reading detected_words.json: {e}")
        existing_words = []

    if detected_words:
        existing_words.extend(detected_words)
        existing_words = sorted(list(set(existing_words)))

    with open("detected_words.json", "w") as f:
        json.dump(existing_words, f)

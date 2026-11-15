import re

def normalize_text(text):
    if not text or not isinstance(text, str) or text.isspace():
        return None
    
    lowercase_text = text.lower()
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]+'," ", lowercase_text)
    normalized_text = re.sub(r'\s+', " ", cleaned_text)
    stripped_text = normalized_text.strip()
    return stripped_text
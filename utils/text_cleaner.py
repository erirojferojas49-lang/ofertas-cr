import re
import unicodedata

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = ' '.join(text.split())
    return text

def extract_price_from_text(text: str) -> float:
    patron = re.search(r'[\d.,]+', text.replace(',', ''))
    if patron:
        return float(patron.group())
    return 0.0

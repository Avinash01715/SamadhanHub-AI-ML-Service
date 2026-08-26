
from data.training_data import URGENT_KEYWORDS

def get_priority(text: str) -> str:
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in URGENT_KEYWORDS):
        return "HIGH"
    return "MEDIUM"
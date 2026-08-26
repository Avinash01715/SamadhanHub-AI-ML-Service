from data.training_data import URGENT_KEYWORDS


def get_priority(text: str) -> str:
    """
    Very simple keyword-based urgency check: if any urgent-sounding
    word/phrase appears, mark HIGH, otherwise MEDIUM.

    This is intentionally basic (no ML) -- it's a placeholder rule,
    not a trained model. Because many genuine complaints naturally
    contain words like "broken" or "not working", most submissions
    will end up HIGH. If that's too aggressive in practice, either
    trim URGENT_KEYWORDS in training_data.py or replace this with a
    trained classifier once you have labeled priority data.
    """
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in URGENT_KEYWORDS):
        return "HIGH"
    return "MEDIUM"

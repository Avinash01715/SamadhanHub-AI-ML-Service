from models.validation import is_genuine
from models.classification import classify_text
from models.deduplication import check_duplicate
from models.priority import get_priority
from models.matching import match_university


def process_submission(submission_id: str, text: str) -> dict:
    """
    Runs one submission through all 5 stages in order:
    Validation -> Classification -> Deduplication -> Priority -> University Match

    Stops early at Validation if the text looks like junk/spam --
    the remaining stages don't run on invalid input.
    """
    result = {"submission_id": submission_id}

    # STAGE 0: Validation -- is this a real complaint or junk/spam?
    if not is_genuine(text):
        result.update({
            "is_valid": False,
            "category": None,
            "category_confidence": None,
            "low_confidence_category": None,
            "is_duplicate": False,
            "duplicate_of": None,
            "priority": None,
            "matched_department": None,
        })
        return result

    result["is_valid"] = True

    # STAGE 1: Classification -- which of the 8 domains does this belong to?
    classification = classify_text(text)
    result["category"] = classification["category"]
    result["category_confidence"] = classification["confidence"]
    result["low_confidence_category"] = classification["low_confidence"]

    # STAGE 2: Deduplication -- has someone already reported this?
    is_duplicate, duplicate_of = check_duplicate(text, submission_id)
    result["is_duplicate"] = is_duplicate
    result["duplicate_of"] = duplicate_of

    # STAGE 3: Priority -- how urgent does this sound?
    result["priority"] = get_priority(text)

    # STAGE 4: University match -- which department should handle it?
    result["matched_department"] = match_university(classification["category"])

    return result

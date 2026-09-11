from models.validation import is_genuine
from models.classification import classify_text
from models.deduplication import check_duplicate
from models.priority import get_priority
from models.matching import (
    match_university,
    get_display_category,
    get_recommended_universities,
)

def _calculate_scores(classification: dict, priority: str, text: str) -> dict:
    domain_match = int(round(classification["confidence"] * 100))
    urgency = 78 if priority == "HIGH" else 55
  
    strong_urgent = ["emergency", "collapsed", "outbreak", "contaminated", "no water", "flooded"]
    text_lower = text.lower()
    for word in strong_urgent:
        if word in text_lower:
            urgency = min(98, urgency + 8)

    feasibility = 70
    if not classification["low_confidence"]:
        feasibility += 15
    if domain_match >= 80:
        feasibility += 8
    feasibility = min(96, feasibility)

    return {
        "domain_match_score": domain_match,
        "urgency_score": urgency,
        "feasibility_score": feasibility,
    }

def process_submission(submission_id: str, text: str) -> dict:
    result = {
        "submission_id": submission_id,
        "is_valid": False,
        "category": None,
        "internal_category": None,
        "domain_match_score": None,
        "urgency_score": None,
        "feasibility_score": None,
        "priority": None,
        "is_duplicate": False,
        "duplicate_of": None,
        "matched_department": None,
        "recommended_universities": [],
        "ai_summary": None,
        "low_confidence": False,
    }

    if not is_genuine(text):
        result["ai_summary"] = "Submission appears to be junk or test text. Rejected."
        return result

    result["is_valid"] = True

    classification = classify_text(text)
    internal_cat = classification["category"]
    display_cat = get_display_category(internal_cat)

    result["internal_category"] = internal_cat
    result["category"] = display_cat
    result["low_confidence"] = classification["low_confidence"]

    is_duplicate, duplicate_of = check_duplicate(text, submission_id)
    result["is_duplicate"] = is_duplicate
    result["duplicate_of"] = duplicate_of

    priority = get_priority(text)
    result["priority"] = priority

    result["matched_department"] = match_university(internal_cat)
    result["recommended_universities"] = get_recommended_universities(display_cat)

    scores = _calculate_scores(classification, priority, text)
    result.update(scores)

    if is_duplicate:
        result["ai_summary"] = f"Possible duplicate of {duplicate_of}. Manual review recommended."
    elif classification["low_confidence"]:
        result["ai_summary"] = f"Low confidence classification ({display_cat}). Consider manual review."
    else:
        result["ai_summary"] = (
            f"AI analysis complete. Strong match for {display_cat}. "
            f"Recommended routing to {result['recommended_universities'][0]}."
        )

    return result
from data.training_data import UNIVERSITY_EXPERTISE


def match_university(category: str) -> str:
    """Looks up which department/faculty handles a given category.
    Falls back to 'Unassigned' if the category isn't in the map
    (e.g. an 'uncategorized' result from low-confidence classification).
    """
    return UNIVERSITY_EXPERTISE.get(category, "Unassigned")
